# Improved BioMiner + TxConformal Pipeline
## MolViBench-Inspired Incremental Repair

Based on **MolViBench** (arxiv:2605.02351) — *Evaluating LLMs on Molecular Vibe Coding*.

---

## Key Insights from MolViBench

| Insight | Implication for Our Pipeline |
|---------|------------------------------|
| Chemical correctness is the bottleneck, NOT executability | Validate SMILES + properties at every step |
| Incremental Repair (execute → traceback → fix → retry) achieves 39.7% Pass@1 | Implement repair loop with max 3 rounds |
| All models < 10% on L5 (end-to-end pipelines) | Target L4 complexity, be realistic |
| Type-aware output comparison handles float tolerances & canonical SMILES | Use RDKit canonical SMILES equivalence |
| AST-based API-semantic verification | Check RDKit function usage correctness |

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK INPUT                               │
│  "Filter BioMiner KDM4A candidates with MW 200-600..."    │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  LLM (Groq Llama 3.3 70B)                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SYSTEM PROMPT: RDKit-only, pipeline_step function    │   │
│  └─────────────────────────────────────────────────────┘   │
│                      ▼                                      │
│  Generated Python Code (RDKit-centric)                      │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  EXECUTE (subprocess, 30s timeout)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ pipeline_step(biomer_df, target="KDM4A")            │   │
│  │ → returns: filtered DataFrame or SMILES list         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  CHEMICAL VALIDATION (RDKitValidator)                      │
│  1. SMILES canonicalization → re-parse check               │
│  2. Lipinski checks: MW 150-800, LogP -1-6, HBA 1-10      │
│  3. PAINS / Brenk filter alerts                            │
│  4. Stereochemistry verification                           │
│  5. QED score (drug-likeness)                              │
└──────────────┬────────────────────────┬────────────────────┘
               │ PASS (score ≥ 0.8)      │ FAIL
               ▼                         ▼
┌──────────────────────────┐  ┌───────────────────────────────────────────┐
│  TxConformal FDR Filter  │  │  REPAIR LOOP (up to 3 rounds)              │
│  (optional, α=0.1)       │  │  ┌─────────────────────────────────────┐   │
│                          │  │  │ Extract traceback error              │   │
│  BH Benjamini-Hochberg    │  │  │ Feed to LLM with REPAIR_PROMPT       │   │
│  at α=0.1                 │  │  │ Generate fixed code                  │   │
│                          │  │  │ Execute again                       │   │
│  Output: validated       │  │  │ Validate again                       │   │
│  candidates ranked by     │  │  └─────────────────────────────────────┘   │
│  p-value                 │  │         │                                  │
└──────────┬───────────────┘  │         ▼                                  │
           │                  │  [Next Round]                              │
           ▼                  └───────────────────────────────────────────┘
┌──────────────────────────┐
│  FINAL OUTPUT            │
│  - Best code across rounds
│  - Validated SMILES      │
│  - Quality score         │
│  - ValidationReport      │
└──────────────────────────┘
```

---

## Module Reference

### 1. `rdkit_validator.py`

Validates molecules for drug-likeness using RDKit.

```python
from rdkit_validator import validate_smiles, batch_validate, filter_valid

# Single SMILES validation
result = validate_smiles("CCO")  # ethanol
assert result.valid
print(result.smiles)           # canonical: "CCO"
print(result.properties["mw"]) # 46.07
print(result.pains_alerts)     # []

# Batch validation
results = batch_validate(["CCO", "invalid"], strict=True)
valid_smiles = filter_valid(["CCO", "c1ccccc1"])

# Properties checked:
#   MW 150-800, LogP -1-6, HBA 1-10, HBD 0-6, TPSA 40-200
#   PAINS (A/B/C alerts), Brenk filter (reactive groups)
```

### 2. `pipeline_evaluator.py`

MolViBench-style pipeline evaluation.

```python
from pipeline_evaluator import evaluate_pipeline_code, EvalScore

score = evaluate_pipeline_code(
    code_str=generated_code,
    test_input=some_input,
    func_name="pipeline_step",
    timeout=30,
)
print(score.quality_score)    # 0-1 composite
print(score.executability)    # 0-1
print(score.chemical_correctness)  # 0-1
print(score.api_correctness)  # 0-1 (AST-based)
```

### 3. `incremental_repair_pipeline.py`

Main pipeline with incremental repair loop.

```python
from incremental_repair_pipeline import (
    IncrementalRepairPipeline, LLMClient, run_biomer_txconformal_pipeline
)

# Using Groq (ultra-fast, free tier)
llm = LLMClient(provider="groq", model="llama-3.3-70b-versatile")
pipeline = IncrementalRepairPipeline(llm_client=llm, max_rounds=3)

result = pipeline.run(
    task="Filter BioMiner SLC7A11 predictions for MW 300-600, "
         "apply PAINS filter, return top 20 by ai_score",
    biomer_predictions=biomer_df,
    target="SLC7A11",
    apply_txconformal=True,
    fdr_alpha=0.1,
)

print(result.quality_score)    # Best quality across all rounds
print(result.total_rounds)      # How many rounds were needed
print(result.success)           # Did any round succeed?
```

---

## LLM Configuration

### Groq (Recommended — Ultra-fast)
```python
import os
os.environ["GROQ_API_KEY"] = "your_key"
llm = LLMClient(provider="groq", model="llama-3.3-70b-versatile")
# Llama 3.3 70B: ~0.6s/response (17x faster than local Ollama)
```

### OpenAI Compatible
```python
llm = LLMClient(
    provider="openai",
    model="gpt-4o",
    base_url="https://api.openai.com/v1",
)
```

### Ollama (Local fallback)
```python
llm = LLMClient(
    provider="ollama",
    model="qwen2.5-coder-32b",
    base_url="http://localhost:11434/v1",
)
```

---

## MolViBench Evaluation Levels

Our pipeline targets **L4** (multi-step reasoning) and **L5** (end-to-end pipelines):

| Level | Description | Example Task |
|-------|-------------|--------------|
| L1 | Single API recall | `Descriptors.MolWt(mol)` |
| L2 | Molecular transformation | `CanonizeSMILES + AddHs` |
| L3 | Complex operations | Find MCS between two molecules |
| **L4** | Multi-step reasoning | Filter by MW + LogP + PAINS + sort by QED |
| **L5** | End-to-end pipeline | BioMiner filter → TxConformal FDR → output SMILES |

---

## Integration with Existing TxConformal Script

The existing `txconformal_biomer_integration.py` generates synthetic data.
Upgrade path:

```python
from incremental_repair_pipeline import IncrementalRepairPipeline, LLMClient
from rdkit_validator import batch_validate

# 1. Load BioMiner predictions (or synthetic)
biomer_df = ...

# 2. Run pipeline with chemical validation
pipeline = IncrementalRepairPipeline(max_rounds=3)
result = pipeline.run(
    task="From BioMiner predictions for KDM4A with ai_score > 0.7, "
         "filter by MW 200-700, apply PAINS filter, "
         "return canonical SMILES sorted by score",
    biomer_predictions=biomer_df,
    target="KDM4A",
)

# 3. Apply TxConformal FDR control (optional)
# (Integrates with existing run_selection from txconformal_biomer_integration.py)

# 4. Final chemical validation of selected candidates
smiles_list = [row['smiles'] for row in result.final_output]
validated = batch_validate(smiles_list, strict=True)
```

---

## Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `executability` | Code runs without syntax/runtime errors | ≥ 0.95 |
| `chemical_correctness` | Output SMILES parseable + drug-like | ≥ 0.80 |
| `api_correctness` | RDKit APIs used semantically correctly | ≥ 0.70 |
| `quality_score` | Weighted composite (0.3/0.4/0.15/0.15) | ≥ 0.75 |

---

## MolViBench Best Practices Integrated

1. **Incremental Repair Loop**: Execute → error → feed traceback → fix → retry (max 3 rounds)
2. **Type-aware comparison**: Canonical SMILES equivalence, float tolerances (atol=0.01)
3. **Chemical validation**: MW, LogP, HBA, HBD, TPSA ranges + PAINS + Brenk
4. **API semantic verification**: AST-based RDKit function call checking
5. **Subprocess isolation**: Safe execution of LLM-generated code
6. **RDKit-only constraint**: No external cheminformatics (numpy/pandas as auxiliary)

---

## Dependencies

```
rdkit
groq>=0.1.0           # optional, for Groq LLM
openai>=1.0.0        # optional, for OpenAI-compatible LLMs
txconformal          # from ~/openclaw/workspace/arp-v24/TxConformal
pandas, numpy         # auxiliary
```
