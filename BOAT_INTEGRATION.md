# BOAT Integration for ARP v24 Drug Discovery

## AstraZeneca BOAT (Bayesian Optimization of Antibody Traits)

**Repository:** https://github.com/AstraZeneca/boat  
**Purpose:** Multi-objective Bayesian optimization for antibody lead optimization

---

## Installation

```bash
cd ~/.openclaw/workspace/arp-v24/boat
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[plms]"
```

---

## Basic Usage

```python
from boat.bayesopt.mo_loop import MOBayesOptOnSequences
from boat.scoring_function.fake import FakeScoringFunction

loop = MOBayesOptOnSequences(
    scoring_functions=[FakeScoringFunction()],
    n_init=8,
    n_iter=5,
)
loop.run()
```

---

## Integration with ARP v24

BOAT can be used for:

1. **Antibody/Peptide Lead Optimization**
   - Multi-objective optimization (affinity, developability, stability)
   - Sequence-space exploration with genetic algorithms

2. **Drug Candidate Scoring**
   - PLM-based encodings for sequence features
   - Bayesian optimization for property prediction

3. **ADMET Optimization**
   - Multi-objective optimization with multiple property predictors
   - Liability filtering for developability

---

## Module Structure

| Module | Purpose |
|--------|---------|
| `boat.bayesopt` | Bayesian optimization (BoTorch/GPyTorch) |
| `boat.genetic_algorithm` | GA operators for sequence search |
| `boat.scoring_function` | Unified scoring interfaces |
| `boat.biologics` | Sequence manipulation, developability |

---

## Dependencies

- Python 3.10/3.11/3.12
- PyTorch ≥2.0
- BoTorch ≥0.9
- GPyTorch ≥1.9
- scikit-learn ≥1.3

---

## Example: Multi-Objective Optimization

```python
from boat.bayesopt.mo_loop import MOBayesOptOnSequences
from boat.scoring_function import YourScoringFunction

# Define multiple objectives
scoring_functions = [
    YourScoringFunction(objective='affinity'),
    YourScoringFunction(objective='developability'),
    YourScoringFunction(objective='stability'),
]

loop = MOBayesOptOnSequences(
    scoring_functions=scoring_functions,
    n_init=8,
    n_iter=10,
    acquisition='EHVI',  # Expected Hypervolume Improvement
)
loop.run()
```

---

## Connection to ARP Pipeline

BOAT can integrate with:
- `arp_v24/de_novo_peptide.py` - Peptide generation
- `arp_v24/candidate_engine.py` - Candidate scoring
- `arp_v24/screening/` - Property prediction

For antibody drug discovery:
- CDR loop optimization
- Humanization scoring
- Developability filters (aggregation, immunogenicity)
