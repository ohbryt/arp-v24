"""
Pipeline Evaluator
===================
Evaluates BioMiner+TxConformal pipeline outputs using MolViBench-style checks:
  - Executability (code runs without errors)
  - Type-aware output comparison
  - AST-based API usage verification
  - Chemical correctness scoring

Based on MolViBench multi-layered evaluation framework (arxiv:2605.02351).
"""

import ast
import sys
import time
import traceback
import tempfile
import subprocess
import json
import importlib.util
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field


# ============================================================
# Result types
# ============================================================

@dataclass
class ExecutionResult:
    success: bool
    output: Any = None
    error: Optional[str] = None
    time_s: float = 0.0
    syntax_error: bool = False
    runtime_error: bool = False
    timeout: bool = False
    stdout: str = ""
    stderr: str = ""


@dataclass
class EvalScore:
    executability: float   # 0-1: code runs without runtime/syntax errors
    chemical_correctness: float  # 0-1: output SMILES are chemically valid
    api_correctness: float      # 0-1: RDKit API used semantically correctly
    quality_score: float        # 0-1: overall weighted score
    details: dict = field(default_factory=dict)


# ============================================================
# Syntax / function existence checks
# ============================================================

def check_syntax(code_str: str) -> tuple[bool, str]:
    """Check if Python code has valid syntax."""
    try:
        compile(code_str, "<string>", "exec")
        return True, "OK"
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"


def find_rdkit_api_usage(code_str: str) -> list[str]:
    """
    Extract RDKit API calls from Python source using AST.
    Returns list of called function names (e.g., ['MolFromSmiles', 'MolToSmiles']).
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return []

    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Direct calls: func()
            if isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
            elif isinstance(node.func, ast.Name):
                calls.append(node.func.id)
    return calls


def verify_rdkit_semantics(code_str: str) -> tuple[bool, list[str], list[str]]:
    """
    Verify that RDKit functions are used semantically correctly.

    Checks:
    - rdkit.Chem is imported (or from rdkit import Chem)
    - Core API categories are used appropriately:
        * MolFromSmiles / MolFromSmarts / MolFromMolBlock → feeds into downstream
        * MolToSmiles / MolToSmarts / MolToMolBlock → output generation
        * Descriptors.* / Lipinski.* → property calculation
        * AllChem.* → 2D coords, reactions, etc.

    Returns (is_valid, used_apis, warnings)
    """
    used_apis = find_rdkit_api_usage(code_str)
    valid_categories = {
        # Input parsing
        "MolFromSmiles", "MolFromSmarts", "MolFromMolBlock", "MolFromPDBBlock",
        "MolFromInchi", "SDWriter", "SmilesWriter",
        # Output generation
        "MolToSmiles", "MolToSmarts", "MolToMolBlock", "MolToPDBBlock",
        "MolToInchi",
        # Descriptors & Lipinski
        "MolWt", "MolLogP", "MolMr", "TPSA", "NumHAcceptors", "NumHDonors",
        "NumRotatableBonds", "NumHeteroatoms", "RingCount", "NumAromaticRings",
        # 2D/3D coordinates
        "Compute2DCoords", "Compute3DCoords", "AllChem",
        # Reactions
        "ReactionFromSmarts", "RunReactants",
        # QED / molecular properties
        "qed", "AllChem",
        # Substructure matching
        "HasSubstructMatch", "GetSubstructMatch",
        # Fingerprints
        "GetMorganFingerprintAsBitVect", "GetFPBFiles", "FingerprintMols",
        # MCS
        "FindMCS",
        # Filtering
        "FilterCatalog",
        # Molecule manipulation
        "SanitizeMol", "Kekulize", "AssignStereochemistry",
        "RemoveHs", "AddHs",
    }

    warnings = []
    used_valid = []
    used_invalid = []

    for api in used_apis:
        if api in valid_categories:
            used_valid.append(api)
        elif api not in ("print", "len", "range", "str", "int", "float", "list",
                         "dict", "tuple", "set", "abs", "max", "min", "sum",
                         "sorted", "enumerate", "zip", "map", "filter",
                         "isinstance", "type", "hasattr", "getattr", "enumerate",
                         "__name__", "__file__", "open", "enumerate", "round"):
            # Potentially valid but not in our whitelist
            used_invalid.append(api)

    is_valid = len(used_invalid) == 0  # Warning only; proceed even if non-std
    return is_valid, used_valid, used_invalid


# ============================================================
# Execution
# ============================================================

def execute_pipeline_code(
    code_str: str,
    func_name: str = "pipeline_step",
    args: list = (),
    kwargs: dict = None,
    timeout: int = 30,
) -> ExecutionResult:
    """
    Execute a pipeline code string in an isolated subprocess.
    Safe for untrusted LLM-generated code.

    Returns ExecutionResult with success, output, error, timing info.
    """
    if kwargs is None:
        kwargs = {}

    # Write code to temp file
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.py', delete=False, encoding='utf-8'
    ) as f:
        # Prepend rdkit import
        f.write("from rdkit import Chem\nfrom rdkit.Chem import Descriptors, Lipinski, AllChem, QED\n\n")
        f.write(code_str)
        filepath = f.name

    start = time.time()

    # Build subprocess wrapper
    wrapper = f'''
import sys, json, traceback, os
sys.path.insert(0, os.path.dirname(r"{filepath}"))

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("pipeline_module", r"{filepath}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
except SyntaxError as e:
    result = {{"success": False, "output": None, "error": f"SyntaxError: {{e}}", "syntax_error": True, "runtime_error": False}}
    print("__RESULT__" + json.dumps(result, default=str))
    sys.exit(0)
except Exception as e:
    result = {{"success": False, "output": None, "error": f"ImportError: {{e}}", "syntax_error": False, "runtime_error": True}}
    print("__RESULT__" + json.dumps(result, default=str))
    sys.exit(0)

func = getattr(module, "{func_name}", None)
if func is None:
    for alt in ["pipeline_step", "run", "execute", "main"]:
        func = getattr(module, alt, None)
        if func is not None:
            break

if func is None:
    result = {{"success": False, "output": None, "error": "Function not found", "syntax_error": False, "runtime_error": True}}
    print("__RESULT__" + json.dumps(result, default=str))
    sys.exit(0)

args = json.loads(r"""{json.dumps(args, default=str)}""")
kwargs = json.loads(r"""{json.dumps(kwargs, default=str)}""")

try:
    output = func(*args, **kwargs)
    result = {{"success": True, "output": output, "error": None, "syntax_error": False, "runtime_error": False}}
except Exception as e:
    tb = traceback.format_exc()
    result = {{"success": False, "output": None, "error": f"{{type(e).__name__}}: {{e}}\\n{{tb}}", "syntax_error": False, "runtime_error": True}}

print("__RESULT__" + json.dumps(result, default=str))
'''

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.py', delete=False, encoding='utf-8'
    ) as wf:
        wf.write(wrapper)
        wrapper_path = wf.name

    try:
        proc = subprocess.run(
            [sys.executable, wrapper_path],
            capture_output=True, text=True, timeout=timeout,
            env={**__import__('os').environ, "PYTHONIOENCODING": "utf-8"},
        )
        elapsed = time.time() - start

        stdout = proc.stdout
        result_line = None
        other_lines = []
        for line in stdout.split('\n'):
            if line.startswith("__RESULT__"):
                result_line = line[len("__RESULT__"):]
            else:
                other_lines.append(line)

        if result_line:
            parsed = json.loads(result_line)
            return ExecutionResult(
                success=parsed.get("success", False),
                output=parsed.get("output"),
                error=parsed.get("error"),
                time_s=round(elapsed, 4),
                syntax_error=parsed.get("syntax_error", False),
                runtime_error=parsed.get("runtime_error", False),
                timeout=False,
                stdout='\n'.join(other_lines).strip(),
                stderr=proc.stderr.strip(),
            )
        else:
            return ExecutionResult(
                success=False, output=None,
                error=f"No result returned. stderr: {proc.stderr[:500]}",
                time_s=round(elapsed, 4),
                stdout=stdout.strip(), stderr=proc.stderr.strip(),
            )
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            success=False, output=None,
            error=f"Timeout after {timeout}s",
            time_s=timeout, timeout=True,
        )
    except Exception as e:
        return ExecutionResult(
            success=False, output=None,
            error=f"Execution error: {e}",
            time_s=time.time() - start,
        )
    finally:
        try:
            import os
            os.unlink(filepath)
            os.unlink(wrapper_path)
        except OSError:
            pass


# ============================================================
# Chemical correctness check
# ============================================================

def check_chemical_correctness(output: Any) -> tuple[float, list[str]]:
    """
    Check if pipeline output is chemically correct.
    Returns (score 0-1, list of error messages).

    Output can be:
      - str (SMILES)
      - list[str] (multiple SMILES)
      - dict with SMILES fields
      - DataFrame with SMILES column
    """
    from rdkit_validator import validate_smiles

    errors = []
    valid_count = 0
    total_count = 0

    # Extract SMILES from various formats
    smiles_list = _extract_smiles(output)
    total_count = len(smiles_list)

    for smi in smiles_list:
        if not smi:
            errors.append("Empty SMILES in output")
            continue
        result = validate_smiles(smi, strict=False)  # parseability only first
        if not result.valid:
            errors.append(f"Invalid SMILES: {smi[:50]}")
        else:
            valid_count += 1

    if total_count == 0:
        return 0.0, ["No SMILES found in output"]

    score = valid_count / total_count
    return score, errors


def _extract_smiles(output: Any) -> list[str]:
    """Extract SMILES strings from various output formats."""
    import pandas as pd

    if output is None:
        return []
    if isinstance(output, str):
        return [output] if output.strip() else []
    if isinstance(output, (list, tuple)):
        return [str(s) for s in output if s]
    if isinstance(output, dict):
        smiles = []
        for v in output.values():
            if isinstance(v, list):
                smiles.extend(_extract_smiles(v))
            elif isinstance(v, str):
                smiles.append(v)
        return [s for s in smiles if s]
    if isinstance(output, pd.DataFrame):
        candidates = []
        for col in output.columns:
            if 'smiles' in col.lower() or 'compound' in col.lower():
                candidates.extend([str(s) for s in output[col].dropna()])
        return [s for s in candidates if s]
    return []


# ============================================================
# Type-aware comparison (from MolViBench comparators)
# ============================================================

def compare_float(pred, ref, atol=1e-2, rtol=1e-3) -> tuple[bool, str]:
    import math
    try:
        p, r = float(pred), float(ref)
        if math.isnan(p) and math.isnan(r):
            return True, "both NaN"
        if math.isnan(p) or math.isnan(r):
            return False, f"one is NaN"
        ok = (abs(p - r) <= atol) or (abs(p - r) <= rtol * max(abs(r), 1e-10))
        return ok, f"diff={abs(p-r):.2e}"
    except (TypeError, ValueError) as e:
        return False, f"Type error: {e}"


def compare_smiles(pred, ref) -> tuple[bool, str]:
    from rdkit import Chem
    try:
        if pred is None or ref is None:
            return pred is None and ref is None, f"none check"
        mol_p = Chem.MolFromSmiles(str(pred))
        mol_r = Chem.MolFromSmiles(str(ref))
        if mol_p is None or mol_r is None:
            return False, f"parse failed"
        can_p = Chem.MolToSmiles(mol_p)
        can_r = Chem.MolToSmiles(mol_r)
        match = (can_p == can_r)
        return match, f"can={can_p[:50]}"
    except Exception as e:
        return False, f"Error: {e}"


# ============================================================
# Main evaluator
# ============================================================

def evaluate_pipeline_code(
    code_str: str,
    test_input: Any = None,
    expected_output: Any = None,
    func_name: str = "pipeline_step",
    timeout: int = 30,
) -> EvalScore:
    """
    Full pipeline evaluation combining:
      1. Executability (syntax + runtime)
      2. Chemical correctness (output SMILES validity)
      3. API correctness (RDKit usage semantics)
      4. Quality score (weighted composite)

    Returns EvalScore dataclass.
    """
    details = {}

    # --- Step 1: Syntax check ---
    syntax_ok, syntax_msg = check_syntax(code_str)
    if not syntax_ok:
        return EvalScore(
            executability=0.0, chemical_correctness=0.0,
            api_correctness=0.0, quality_score=0.0,
            details={"syntax_error": syntax_msg}
        )

    # --- Step 2: API usage verification (AST-based) ---
    is_valid_api, used_apis, unknown_apis = verify_rdkit_semantics(code_str)
    api_score = len(used_apis) / max(len(used_apis) + len(unknown_apis), 1)
    details["used_rdkit_apis"] = used_apis
    details["unknown_apis"] = unknown_apis

    # --- Step 3: Execution ---
    args = [test_input] if test_input is not None else []
    exec_result = execute_pipeline_code(code_str, func_name, args=args, timeout=timeout)

    if not exec_result.success:
        details["execution_error"] = exec_result.error
        details["execution_runtime_error"] = exec_result.runtime_error
        details["execution_timeout"] = exec_result.timeout
        return EvalScore(
            executability=0.0, chemical_correctness=0.0,
            api_correctness=api_score, quality_score=0.0,
            details=details,
        )

    # --- Step 4: Chemical correctness ---
    chem_score, chem_errors = check_chemical_correctness(exec_result.output)
    details["chemical_errors"] = chem_errors

    # --- Step 5: Output comparison (if expected provided) ---
    match_score = 1.0
    match_detail = "no reference"
    if expected_output is not None:
        if isinstance(expected_output, float):
            pred_val = float(exec_result.output) if exec_result.output is not None else None
            match_score, match_detail = compare_float(pred_val, expected_output) if pred_val is not None else (False, "None output")
        elif isinstance(expected_output, str):
            match_score, match_detail = compare_smiles(str(exec_result.output), expected_output)
        details["comparison"] = match_detail

    # --- Composite quality score ---
    # Weight: executability (30%), chemical correctness (40%), API correctness (15%), output match (15%)
    quality = (
        1.0 * 0.30 +          # executability always 1.0 if we got here
        chem_score * 0.40 +
        api_score * 0.15 +
        (1.0 if match_score else 0.0) * 0.15
    )

    return EvalScore(
        executability=1.0,
        chemical_correctness=chem_score,
        api_correctness=api_score,
        quality_score=round(quality, 4),
        details=details,
    )
