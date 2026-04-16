# ARP Research Pipeline - Production Skills

**Version**: 1.0  
**For**: AI agents conducting drug discovery research  
**Based on**: agent-skills by addyosmani (adapted for biomedical research)

---

## Core Commands

| Command | Purpose | When |
|---------|---------|------|
| `/spec` | Research spec before experiments | Starting new research |
| `/plan` | Task breakdown | Have spec, need tasks |
| `/build` | Implement candidate generation | One target at a time |
| `/test` | Validate (ADMET, Docking) | Built candidates |
| `/review` | Quality review | Before conclusions |
| `/ship` | Finalize & report | Research complete |

---

## Development Lifecycle

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  SPEC   │ → │  PLAN    │ → │  BUILD   │ → │  TEST    │ → │  REVIEW  │
│ Research │   │  Tasks   │   │  Synth   │   │  ADMET   │   │ Quality  │
│   PRD    │   │   WBS    │   │ Candidate │   │  Docking │   │  Gate    │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                                     ↓
                                                              ┌──────────┐
                                                              │  SHIP    │
                                                              │  Report  │
                                                              └──────────┘
```

---

## Skill 1: Research Spec (`/spec`)

**Before any experiment, write a research spec.**

### Template

```markdown
# Research Spec: [Disease] - [Target/Treatment]

## 1. Objective
What should exist that doesn't?

## 2. Research Questions
- Q1: [specific question]
- Q2: [specific question]

## 3. Pipeline Steps
- Step 1: [what]
- Step 2: [what]

## 4. Quality Gates
- Gate A: [criterion]
- Gate B: [criterion]

## 5. Boundaries
- In scope: [what]
- Out of scope: [what]

## 6. Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Anti-Rationalization Table

| Instead of... | Write... |
|---------------|----------|
| "Explore potential targets" | "Identify 5 NASH-relevant targets" |
| "Test some compounds" | "Screen 1000 compounds against target X" |
| "Get good results" | "Achieve IC50 < 1µM" |

---

## Skill 2: Task Breakdown (`/plan`)

**Break spec into small, verifiable tasks.**

### Task Template

```markdown
## Task: [Name]
- **Size**: XS / S / M / L / XL
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
- **Dependencies**: [other tasks]
- **Verification**: [how to verify]
```

### Size Guidelines

| Size | Time | Lines | Description |
|------|------|-------|-------------|
| XS | 15min | 10 | Single function fix |
| S | 1h | 30 | One small module |
| M | 2-4h | 100 | One feature |
| L | 1-2d | 300 | Multi-feature |
| XL | 1w | 1000 | Epic |

---

## Skill 3: Incremental Build (`/build`)

**Build thin vertical slices.**

### Principles

1. **One target at a time** - Don't batch
2. **Test after each** - Verify before next
3. **Commit frequently** - Small, atomic commits
4. **Feature flags** - Disable non-essential

### Anti-Patterns

| Bad | Good |
|-----|------|
| Generate 100 candidates at once | Generate 5, validate, repeat |
| "Perfect" ADMET first | Quick filter, refine later |
| Wait for all data | Use available, update later |

---

## Skill 4: Validation Testing (`/test`)

**ADMET → Docking → Synthesis planning**

### Test Pyramid

```
         ┌─────────┐
        │   In Vivo  │  5% - Validation
       ┌───────────┐
      │  In Vitro   │  15% - Extended assays
     ┌─────────────┐
    │  ADMET/Dock   │  80% - In silico filters
   └─────────────────┘
```

### Quality Gates

| Gate | Criterion | Action if Fail |
|------|-----------|----------------|
| ADMET | Lipinski ≤1 violation | Flag, continue anyway |
| Binding | Score ≥ 0.7 | Prioritize for synthesis |
| SA Score | ≤ 0.6 | Feasible synthesis |
| Selectivity | >10x vs off-targets | Flag concerns |

---

## Skill 5: Research Review (`/review`)

**Five-axis review before conclusions.**

### Review Checklist

- [ ] **Biological validity**: Does mechanism make sense?
- [ ] **Chemical plausibility**: Synthetically accessible?
- [ ] **Clinical translation**: Validated in relevant models?
- [ ] **Novelty**: Not just reformulated existing?
- [ ] **Reproducibility**: Methods described clearly?

### Severity Labels

| Label | Meaning | Action |
|-------|---------|--------|
| Critical | Invalidates conclusion | Must fix |
| Major | Significant concern | Should address |
| Minor | Small improvement | Consider |
| FYI | Note only | Acknowledge |

---

## Skill 6: Ship & Report (`/ship`)

**Ship research with full provenance.**

### Report Template

```markdown
# Research Report: [Title]

## Executive Summary
[2-3 sentences]

## Methods
### Pipeline
- Tool 1: [what]
- Tool 2: [what]

### Quality Control
- [x] ADMET passed
- [x] Docking validated
- [x] Synthesis feasible

## Results
### Candidates
| ID | Target | Score | ADMET | SA |
|----|--------|-------|-------|----|

### Top Recommendation
[Lead candidate with rationale]

## Limitations
[Honest assessment]

## Next Steps
1. [Immediate next]
2. [3-month]
3. [1-year]

## References
[All sources cited]
```

---

## ARP-Specific Skills

### Skill: Target Validation

```python
def validate_target(gene_name, disease):
    """Check target is valid for disease"""
    # 1. Gene-disease association
    # 2. Expression in relevant tissue
    # 3. Known drugability
    # 4. Existing compounds
    return ValidationResult(passed=True, concerns=[])
```

### Skill: ADMET Filter

```python
def filter_admet(candidates):
    """Lipinski + extended filters"""
    passed = []
    for c in candidates:
        if c.lipinski_violations <= 1:
            if c.mw < 500 and c.logp < 5:
                if c.tpsa < 140:
                    passed.append(c)
    return passed
```

### Skill: Binding Prediction

```python
def predict_binding(smiles, target):
    """Predict binding affinity"""
    # Use RDKit descriptors + heuristics
    # Based on known actives for target class
    return BindingScore(score=0.8, confidence="moderate")
```

---

## Context for ARP

When starting a research session:

1. **Read context files** (SOUL.md, AGENTS.md, MEMORY.md)
2. **Check recent work** (memory/YYYY-MM-DD.md)
3. **Define scope** with `/spec`
4. **Break into tasks** with `/plan`
5. **Build incrementally** with `/build`
6. **Validate** with `/test`
7. **Review** with `/review`
8. **Report** with `/ship`

---

*Based on agent-skills by addyosmani, adapted for biomedical research*
