---
name: drug-discovery-task-execution
description: Executes drug discovery tasks using vertical slicing. Use when implementing a task from the drug discovery plan. Uses incremental implementation with verification at each step.
---

# Drug Discovery Task Execution

## Overview

Execute drug discovery tasks using vertical slicing - implement, verify, commit each slice before moving on. Based on agent-skills/incremental-implementation.

## When to Use

- Implementing a task from the drug discovery plan
- Running virtual screening, ADMET, or candidate analysis
- Implementing new pipeline components
- Any task touching multiple files or stages

**When NOT to use:** Single-file changes, trivial literature lookups, well-defined quick tasks.

## Process

### Step 1: Understand the Task

Before writing any code:

- Read the task description and acceptance criteria
- Check relevant existing code and data
- Identify dependencies and prerequisites
- Plan the minimal slice needed

**Do NOT over-engineer.** Deliver working results, not perfect architecture.

### Step 2: Implement the Minimal Slice

Build the smallest working version:

```python
# Example: DGAT1 Virtual Screening
# Bad: Build entire screening pipeline first
# Good: Screen 100 compounds, verify it works, then scale

def screen_compounds(target, compounds, threshold=7.0):
    """Minimal working version"""
    hits = []
    for smi in compounds:
        score = docking_score(target, smi)
        if score > threshold:
            hits.append((smi, score))
    return hits
```

### Step 3: Verify

Before proceeding, verify:

- [ ] Code runs without errors
- [ ] Results are reasonable (known actives rank high)
- [ ] Output format is correct
- [ ] Can be viewed in output/report

```bash
# Verification commands
python3 -c "from dgat1_screen import screen_compounds; print('Import OK')"
python3 dgat1_screen.py --test  # Test on known actives
python3 dgat1_screen.py --run  # Full run
```

### Step 4: Document

Create/update report:

```markdown
## Task 3 Results: Virtual Screening

**Compounds screened:** 1000
**Hits selected:** 47 (score > 7.0)
**Top hit:** SMILES_xxx (score: 8.5)

**Verification:**
- [ ] Known actives rank in top 10%
- [ ] Screen completed in < 5 min
- [ ] Output saved to results.csv
```

### Step 5: Commit

Commit with clear message:

```
feat(dgat1): add virtual screening for 1000 compounds

- Screen 1000 compounds using OpenBabel docking
- 47 hits selected (score > 7.0)
- Known inhibitor ranks #3
- Results saved to dgat1_hits.csv
```

## Vertical Slicing Examples

### Bad (Horizontal)
```
Task: "Complete DGAT1 analysis"
├── All literature
├── All structures
├── All screening
└── All ADMET
→ Never delivers working results
```

### Good (Vertical)
```
Task 1: DGAT1 target report (literature + summary)
Task 2: DGAT1 screening 1000 compounds → hits
Task 3: DGAT1 ADMET top 50 hits
Task 4: DGAT1 candidates → report
→ Each delivers working output
```

## Anti-Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll add verification later" | Without verification, you don't know if it works. |
| "I need to build the perfect pipeline" | Minimal working version > perfect plans. |
| "This is too small to commit" | Small, focused commits are easier to review and revert. |
| "I can skip the report" | Reports are how others verify your work. |

## Red Flags

- Implementation without running test cases
- Results saved but not verified
- No documentation of what was done
- Commits that are too large (>10 files)
- Skipping intermediate checkpoints

## Verification Checklist

Before marking task complete:

- [ ] Code runs successfully
- [ ] Results are reproducible
- [ ] Known benchmarks pass (e.g., known actives rank high)
- [ ] Report generated and readable
- [ ] Committed to repository
- [ ] Task plan updated with completion status