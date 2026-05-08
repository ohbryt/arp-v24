---
name: drug-discovery-planning
description: Breaks drug discovery projects into implementable tasks. Use when you have a target (e.g., DGAT1, SLC7A11) and need to plan the discovery pipeline from literature to candidate nomination. Based on agent-skills/planning-and-task-breakdown.
---

# Drug Discovery Planning and Task Breakdown

## Overview

Decompose drug discovery projects into small, verifiable tasks with explicit acceptance criteria. Each task should be small enough to implement, test, and verify in a single focused session. Based on agent-skills/planning-and-task-breakdown.

## When to Use

- You have a target (e.g., DGAT1, YARS2) and need to plan discovery
- Starting a new pipeline (virtual screening → ADMET → candidates)
- Task feels too large or vague to start
- Parallel work possible across multiple agents
- Need to communicate scope to collaborators

**When NOT to use:** Simple literature searches, single-file analysis, well-defined single tasks.

## The Drug Discovery Planning Process

### Step 1: Enter Research Mode

Before writing any code, operate in read-only mode:

- Read relevant literature and target information (UniProt, PDB, ChEMBL)
- Identify existing data and pipeline components
- Map dependencies: target ID → literature → screening → ADMET → candidates
- Note risks and unknowns (novel targets, data gaps)

**Do NOT run heavy computations during planning.** The output is a plan document.

### Step 2: Identify the Dependency Graph

Map what depends on what:

```
Target ID (UniProt, PDB structures)
    │
    ├── Literature Survey
    │       │
    │       ├── Target Biology (function, pathways)
    │       │       │
    │       │       └── Disease Relevance (oncology, etc.)
    │       │
    │       └── Known Inhibitors (ChEMBL, drugs)
    │
    ├── Virtual Screening
    │       ├── Structure Prep (AlphaFold, PDB)
    │       │       │
    │       │       ├── Pharmacophore Model
    │       │       │       │
    │       │       └── Docking/HTVS
    │       │
    │       └── Hit Selection (score threshold)
    │
    ├── ADMET Prediction
    │       ├── Physicochemical (LogP, TPSA, MW)
    │       │       │
    │       ├── Safety (hERG, CYP)
    │       │       │
    │       └── Pharmacokinetics (permeability, solubility)
    │
    └── Candidate Nomination
            ├── Priority Score
            ├── NLA-style Reasoning
            └── Benchmark (TargetBench comparison)
```

Implementation order follows bottom-up: target ID → literature → screening → ADMET → candidates.

### Step 3: Slice Vertically

Instead of building all literature, then all screening, then all ADMET — build one complete path at a time:

**Bad (horizontal slicing):**
```
Task 1: Complete all literature survey
Task 2: Build all virtual screening protocols
Task 3: Complete all ADMET predictions
Task 4: Connect everything
```

**Good (vertical slicing):**
```
Task 1: DGAT1 target report (literature + biology)
Task 2: DGAT1 virtual screening (1000 compounds)
Task 3: DGAT1 ADMET analysis (top 50 compounds)
Task 4: DGAT1 candidate nomination (top 10)
```

Each vertical slice delivers working, analyzable results.

### Step 4: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Literature verified: N papers, M databases
- [ ] Code runs: `python3 pipeline.py --target DGAT1`
- [ ] Results: M hits from N compounds screened

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `arp-v24/dgat1_analysis.py`
- `arp-v24/reports/dgat1_task1.md`

**Estimated scope:** [XS: 1 file | S: 2-3 files | M: 4-6 files | L: 7+ files]
```

### Step 5: Order and Checkpoint

Arrange tasks so that:

1. Dependencies are satisfied (build foundation first)
2. Each task leaves the system in a working state
3. Verification checkpoints occur after every 2-3 tasks
4. High-risk tasks (novel targets) are early (fail fast)

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3
- [ ] Target validated: UniProt confirmed, PDB available
- [ ] Literature complete: N papers cited
- [ ] Screening protocol: validated on known actives
- [ ] Review with team before proceeding
```

## Task Sizing Guidelines

| Size | Scope | Example |
|------|-------|---------|
| **XS** | Single file, one function | Get UniProt ID for target |
| **S** | 2-3 files, one module | Literature search for one target |
| **M** | 4-6 files, one pipeline stage | Virtual screening 1000 compounds |
| **L** | 7+ files, multi-stage | Complete DGAT1 → candidate pipeline |

If a task is L or larger, break it down further.

## Drug Discovery Plan Template

```markdown
# Drug Discovery Plan: [Target Name]

## Overview
[One paragraph summary of target and therapeutic area]

## Target Information
| Item | Value |
|------|-------|
| UniProt ID | O75907 (DGAT1) |
| Gene | DGAT1 |
| PDB Structures | 6VP0, 6VYI, 6VZ1, 8ESM |
| Clinical Stage | Preclinical |

## Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

## Task List

### Phase 1: Target Validation
- [ ] Task 1: Literature survey (N papers)
- [ ] Task 2: Target biology summary

### Checkpoint: Target Validation
- [ ] Target validated in UniProt
- [ ] N papers cited
- [ ] Disease relevance confirmed

### Phase 2: Virtual Screening
- [ ] Task 3: Structure preparation (PDB/AlphaFold)
- [ ] Task 4: Pharmacophore model
- [ ] Task 5: Run HTVS (N compounds)
- [ ] Task 6: Hit selection (score > X)

### Checkpoint: Virtual Screening
- [ ] M hits selected
- [ ] Hits validated on known actives
- [ ] Review with team

### Phase 3: ADMET Analysis
- [ ] Task 7: Physicochemical prediction (M hits)
- [ ] Task 8: Safety profiling (hERG, CYP)
- [ ] Task 9: Priority ranking

### Checkpoint: ADMET
- [ ] N candidates with ADMET profile
- [ ] TargetBench scores calculated
- [ ] NLA-style reasoning generated

### Phase 4: Candidate Nomination
- [ ] Task 10: Final candidate selection
- [ ] Task 11: Generate report (MD/PDF)
- [ ] Task 12: Upload to GitHub

### Checkpoint: Complete
- [ ] M candidates nominated
- [ ] Reports generated
- [ ] Ready for experimental validation

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [No PDB structure] | High | Use AlphaFold prediction |
| [Limited literature] | Medium | Expand to other species |
| [Low hit rate] | Medium | Adjust pharmacophore |

## Open Questions
- [Question needing human input]
```

## Parallelization Opportunities

When multiple agents or sessions are available:

- **Safe to parallelize:** Literature for multiple targets, ADMET for different compound sets, report generation
- **Must be sequential:** Target validation → screening → ADMET (dependency chain)
- **Needs coordination:** Shared pipeline modules (define interfaces first)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you end up with fragmented analysis. 10 minutes of planning saves hours. |
| "The tasks are obvious" | Write them down anyway. Explicit tasks surface hidden dependencies. |
| "Planning is overhead" | Planning is the task. Research without a plan is just searching. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries. |

## Red Flags

- Starting virtual screening without literature validation
- Tasks that say "analyze target" without acceptance criteria
- No verification steps in the plan
- All tasks are L-sized (too large)
- No checkpoints between phases
- Dependency order isn't considered

## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] No task is L-sized or larger
- [ ] Checkpoints exist between major phases
- [ ] The human has reviewed and approved the plan