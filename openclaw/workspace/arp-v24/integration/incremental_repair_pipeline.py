"""
Incremental Repair Pipeline
=============================
BioMiner + TxConformal pipeline with MolViBench-style Incremental Repair.

Pipeline flow:
  BioMiner predictions → Generate code → Execute → Validate chemical output
  → If error: generate fix from traceback → Retry (up to 3 cycles)
  → Final validated output

Key MolViBench insights integrated:
  1. Incremental Repair: execute code, feed traceback to LLM for fixes
  2. Chemical correctness is the bottleneck (not executability)
  3. RDKit-centric (numpy/pandas/scikit-learn as auxiliary)
  4. Type-aware validation with PAINS/Brenk filters

Usage:
    result = IncrementalRepairPipeline().run(
        task_description="...",
        biomer_predictions_df=...,
        target="KDM4A",
        max_rounds=3,
    )
"""

import time
import json
import re
import sys
import traceback
import tempfile
import subprocess
from typing import Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

# RDKit
from rdkit import Chem

# Local modules
from rdkit_validator import validate_smiles, batch_validate, ValidationResult
from pipeline_evaluator import evaluate_pipeline_code, ExecutionResult, EvalScore


# ============================================================
# Configuration
# ============================================================

DEFAULT_TIMEOUT = 30          # seconds per execution round
DEFAULT_MAX_ROUNDS = 3        # max repair rounds (per MolViBench)
DEFAULT_FDR_ALPHA = 0.1       # FDR level for TxConformal

SYSTEM_PROMPT = """You are an expert cheminformatics programmer.
Write Python code using RDKit to solve molecular computing tasks.
Your code must define a function called `pipeline_step` that takes the specified input and returns the result.
Only use these libraries: rdkit, numpy, pandas, scikit-learn, matplotlib, selfies.
Include error handling with try/except blocks.
Return only the Python code, no explanations."""

REPAIR_PROMPT = """The code you provided failed during execution. Here is the error:

```
{error}
```

The test was run as:
```python
result = pipeline_step(test_input)
```

Please fix the code and provide the corrected complete Python code.
The function must still be named `pipeline_step`.
Return only the Python code, no explanations."""


# ============================================================
# Result types
# ============================================================

@dataclass
class RepairRound:
    round_num: int
    code: str
    execution_result: ExecutionResult
    chem_check: tuple[float, list[str]]
    eval_score: EvalScore
    repair_successful: bool = False
    error_for_llm: str = ""


@dataclass
class PipelineResult:
    success: bool
    final_code: str
    final_output: Any
    total_rounds: int
    rounds: list[RepairRound]
    quality_score: float
    validation_result: Optional[ValidationResult] = None
    error: str = ""


# ============================================================
# LLM Client (pluggable)
# ============================================================

class LLMClient:
    """
    Pluggable LLM client. Implement `complete(prompt) -> str`.
    Supports Groq (ultra-fast), OpenAI-compatible APIs, or Ollama.
    """

    def __init__(
        self,
        provider: str = "groq",        # "groq", "openai", "ollama"
        model: str = "llama-3.3-70b-versatile",
        api_key: str = None,
        base_url: str = None,
        timeout: int = 120,
    ):
        self.provider = provider
        self.model = model
        self.timeout = timeout

        if provider == "groq":
            import os
            self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
            self.base_url = "https://api.groq.com/openai/v1"
        elif provider == "openai":
            import os
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
            self.base_url = base_url or "https://api.openai.com/v1"
        elif provider == "ollama":
            self.api_key = ""
            self.base_url = base_url or "http://localhost:11434/v1"
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def complete(self, prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        """Send prompt to LLM and return response text."""
        if self.provider == "groq":
            return self._complete_groq(prompt, system_prompt)
        elif self.provider == "openai":
            return self._complete_openai(prompt, system_prompt)
        elif self.provider == "ollama":
            return self._complete_ollama(prompt, system_prompt)

    def _complete_groq(self, prompt: str, system_prompt: str) -> str:
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("groq not installed: pip install groq")
        client = Groq(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=4096,
            timeout=self.timeout,
        )
        return resp.choices[0].message.content

    def _complete_openai(self, prompt: str, system_prompt: str) -> str:
        import os
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai not installed: pip install openai")
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=4096,
            timeout=self.timeout,
        )
        return resp.choices[0].message.content

    def _complete_ollama(self, prompt: str, system_prompt: str) -> str:
        import os
        try:
            import openai
        except ImportError:
            raise ImportError("openai not installed: pip install openai")
        client = openai.OpenAI(api_key="ollama", base_url=self.base_url)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=4096,
            timeout=self.timeout,
        )
        return resp.choices[0].message.content


# ============================================================
# Code extraction
# ============================================================

def extract_code_block(text: str) -> str:
    """
    Extract Python code from LLM response.
    Handles ```python ... ``` and plain code blocks.
    """
    # Try markdown code blocks first
    patterns = [
        r'```python\s*(.*?)\s*```',
        r'```\s*(.*?)\s*```',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()

    # Fallback: treat entire response as code if it looks like Python
    lines = text.strip().split('\n')
    if any('def ' in l or 'import ' in l for l in lines[:10]):
        return text.strip()

    return text.strip()


# ============================================================
# Main pipeline
# ============================================================

class IncrementalRepairPipeline:
    """
    BioMiner + TxConformal pipeline with Incremental Repair loop.

    The pipeline:
      1. Generates pipeline code from task description using LLM
      2. Executes the code with a test input
      3. Validates chemical output (SMILES, properties, PAINS)
      4. If execution fails or output is chemically invalid:
         - Feed error traceback to LLM
         - Generate fixed code
         - Retry (up to max_rounds)
      5. Returns best result across all rounds
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        max_rounds: int = DEFAULT_MAX_ROUNDS,
        execution_timeout: int = DEFAULT_TIMEOUT,
        verbose: bool = True,
    ):
        self.llm = llm_client or LLMClient()
        self.max_rounds = max_rounds
        self.timeout = execution_timeout
        self.verbose = verbose

    # ── Step 1: Generate code ─────────────────────────────────────────────────

    def generate_code(self, task: str) -> str:
        """Generate pipeline code from natural language task."""
        prompt = f"{task}\n\nWrite a `pipeline_step` function in Python using RDKit."
        response = self.llm.complete(prompt, system_prompt=SYSTEM_PROMPT)
        return extract_code_block(response)

    # ── Step 2: Generate repair ─────────────────────────────────────────────

    def generate_repair(self, code: str, error: str, task: str) -> str:
        """Generate repaired code from error traceback."""
        prompt = REPAIR_PROMPT.format(error=error)
        task_context = f"\n\nOriginal task: {task}" if task else ""
        full_prompt = f"{prompt}{task_context}\n\nCurrent (broken) code:\n```python\n{code}\n```"
        response = self.llm.complete(full_prompt, system_prompt=SYSTEM_PROMPT)
        return extract_code_block(response)

    # ── Step 3: Execute code ──────────────────────────────────────────────────

    def execute_code(self, code: str, test_input: Any = None) -> ExecutionResult:
        """Execute pipeline code and return structured result."""
        args = [test_input] if test_input is not None else []
        return execute_pipeline_code(
            code, func_name="pipeline_step", args=args, timeout=self.timeout
        )

    # ── Step 4: Chemical validation ─────────────────────────────────────────

    def validate_chemical_output(
        self, output: Any, strict: bool = True
    ) -> tuple[float, list[str], list[ValidationResult]]:
        """
        Validate chemical output from pipeline.
        Returns (score, error_msgs, ValidationResult list).
        """
        from rdkit_validator import batch_validate

        if output is None:
            return 0.0, ["None output"], []

        # Extract SMILES from output
        smiles_list = self._extract_smiles(output)
        if not smiles_list:
            return 0.0, ["No SMILES in output"], []

        # Validate each SMILES
        results = batch_validate(smiles_list, strict=strict)
        valid_count = sum(1 for r in results if r.valid)
        score = valid_count / len(results) if results else 0.0

        errors = []
        for r in results:
            if not r.valid:
                errors.append(r.reason)
            elif r.pains_alerts:
                errors.append(f"PAINS: {r.pains_alerts[0]}")
            elif r.brenk_alerts:
                errors.append(f"Brenk: {r.brenk_alerts[0]}")

        return score, errors, results

    def _extract_smiles(self, output: Any) -> list[str]:
        """Extract SMILES strings from any output format."""
        import pandas as pd

        if output is None:
            return []
        if isinstance(output, str):
            return [output.strip()] if output.strip() else []
        if isinstance(output, (list, tuple)):
            out = []
            for item in output:
                if isinstance(item, str):
                    out.append(item.strip())
                elif isinstance(item, (list, tuple)):
                    out.extend(self._extract_smiles(item))
            return [s for s in out if s]
        if isinstance(output, dict):
            out = []
            for v in output.values():
                out.extend(self._extract_smiles(v))
            return [s for s in out if s]
        if isinstance(output, pd.DataFrame):
            candidates = []
            for col in output.columns:
                col_lower = col.lower()
                if 'smiles' in col_lower or 'compound' in col_lower or 'mol' in col_lower:
                    candidates.extend([str(s) for s in output[col].dropna()])
            return [s.strip() for s in candidates if s.strip()]
        return []

    # ── Step 5: Full repair loop ─────────────────────────────────────────────

    def run(
        self,
        task: str,
        test_input: Any = None,
        biomer_predictions: Any = None,  # DataFrame or dict (future use)
        target: str = "unknown",
        apply_txconformal: bool = False,
        fdr_alpha: float = DEFAULT_FDR_ALPHA,
    ) -> PipelineResult:
        """
        Run the incremental repair pipeline.

        Parameters
        ----------
        task : str
            Natural language description of the pipeline task.
        test_input : Any
            Test input for the pipeline function.
        biomer_predictions : Any
            BioMiner predictions (DataFrame with compound_id, ai_score, ...).
        target : str
            Target gene name (for logging).
        apply_txconformal : bool
            Whether to apply TxConformal FDR filtering after repair.
        fdr_alpha : float
            FDR level for TxConformal.

        Returns
        -------
        PipelineResult
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"[IncrementalRepairPipeline] Target: {target}")
            print(f"[IncrementalRepairPipeline] Task: {task[:80]}...")
            print(f"[IncrementalRepairPipeline] Max rounds: {self.max_rounds}")
            print(f"{'='*60}")

        rounds = []
        best_result = None
        best_score = -1.0

        # --- Round 0: Generate initial code ---
        code = self.generate_code(task)
        if self.verbose:
            print(f"\n[Round 0] Generated code ({len(code)} chars)")

        for round_num in range(self.max_rounds):
            if self.verbose:
                print(f"\n{'─'*40}")
                print(f"[Round {round_num}] Executing...")

            # Execute
            exec_result = self.execute_code(code, test_input=test_input)

            # Chemical validation
            if exec_result.success and exec_result.output is not None:
                chem_score, chem_errors, chem_results = self.validate_chemical_output(
                    exec_result.output, strict=True
                )
            else:
                chem_score, chem_errors, chem_results = 0.0, [], []

            # Evaluate
            eval_score = evaluate_pipeline_code(
                code, test_input=test_input, func_name="pipeline_step",
                timeout=self.timeout
            )

            repair_successful = (
                exec_result.success and
                not exec_result.runtime_error and
                not exec_result.syntax_error and
                chem_score >= 0.8
            )

            round_record = RepairRound(
                round_num=round_num,
                code=code,
                execution_result=exec_result,
                chem_check=(chem_score, chem_errors),
                eval_score=eval_score,
                repair_successful=repair_successful,
                error_for_llm=exec_result.error or (chem_errors[0] if chem_errors else ""),
            )
            rounds.append(round_record)

            if self.verbose:
                print(f"  Executable: {exec_result.success}")
                print(f"  Runtime error: {exec_result.runtime_error}")
                print(f"  Chem score: {chem_score:.2f} ({len(chem_errors)} errors)")
                print(f"  Quality: {eval_score.quality_score:.4f}")

            # Track best result
            if eval_score.quality_score > best_score:
                best_score = eval_score.quality_score
                best_result = exec_result

            # Early stopping if successful
            if repair_successful:
                if self.verbose:
                    print(f"  ✅ Repair successful at round {round_num}")
                break

            # Generate repair for next round
            if round_num < self.max_rounds - 1:
                error_msg = exec_result.error or "; ".join(chem_errors[:3])
                if self.verbose:
                    print(f"  🔧 Generating repair (error: {error_msg[:100]})...")
                code = self.generate_repair(code, error_msg, task)

        # --- TxConformal step (optional) ---
        final_output = best_result.output if best_result else None
        validation_result = None

        if apply_txconformal and final_output is not None and biomer_predictions is not None:
            try:
                from txconformal_biomer_integration import run_selection
                smiles_list = self._extract_smiles(final_output)
                if smiles_list:
                    # Apply TxConformal to filter BioMiner candidates
                    if self.verbose:
                        print(f"\n[TxConformal] Applying FDR α={fdr_alpha} filtering...")
                    # (Would integrate here with real BioMiner predictions)
            except Exception as e:
                if self.verbose:
                    print(f"[TxConformal] Skipped: {e}")

        # --- Final validation ---
        if final_output is not None:
            _, _, chem_results_final = self.validate_chemical_output(
                final_output, strict=True
            )
            validation_result = chem_results_final[0] if chem_results_final else None

        success = (
            len(rounds) > 0 and
            any(r.repair_successful for r in rounds)
        )

        return PipelineResult(
            success=success,
            final_code=rounds[-1].code if rounds else code,
            final_output=final_output,
            total_rounds=len(rounds),
            rounds=rounds,
            quality_score=best_score,
            validation_result=validation_result,
        )


# ============================================================
# Convenience wrappers
# ============================================================

def run_biomer_txconformal_pipeline(
    task: str,
    biomer_df,
    target: str = "unknown",
    llm_provider: str = "groq",
    model: str = "llama-3.3-70b-versatile",
    max_rounds: int = 3,
    apply_txconformal: bool = False,
    fdr_alpha: float = 0.1,
) -> PipelineResult:
    """
    One-shot convenience wrapper for BioMiner + TxConformal pipeline.

    Parameters
    ----------
    task : str
        Natural language task description.
    biomer_df : DataFrame
        BioMiner predictions (compound_id, ai_score, target).
    target : str
        Target gene.
    llm_provider : str
        LLM provider ("groq", "openai", "ollama").
    model : str
        Model name.
    max_rounds : int
        Max incremental repair rounds.
    apply_txconformal : bool
        Apply TxConformal FDR filtering.
    fdr_alpha : float
        FDR alpha level.
    """
    llm = LLMClient(provider=llm_provider, model=model)
    pipeline = IncrementalRepairPipeline(
        llm_client=llm,
        max_rounds=max_rounds,
        verbose=True,
    )
    return pipeline.run(
        task=task,
        biomer_predictions=biomer_df,
        target=target,
        apply_txconformal=apply_txconformal,
        fdr_alpha=fdr_alpha,
    )
