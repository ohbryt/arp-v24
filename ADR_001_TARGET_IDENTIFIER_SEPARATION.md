# ARP v24 Architecture Decision: Target vs Identifier Separation
**Date:** 2026-05-12  
**Author:** 오창명 (DRCMOH)  
**Type:** Architecture Decision Record (ADR)  
**Status:** Proposed  

---

## Context

현재 `yars2-sirna-pf14-2026` 브랜치명은 **타겟명 + 프로젝트 + 실험 + 연도**가 섞여 있음.

**문제점:**
- 브랜치가 타겟에 종속됨
- 같은 브랜치에 다른 타겟 작업 섞기 어려움
- 검색/운영/릴리즈에서 혼동
- yars2가 문서/코드/브랜치 전반에 섞여 있음

---

## Decision

### 1. Name Classification

| Type | yars2 | Example |
|------|-------|---------|
| **Scientific Target** | ✅ KEEP | `targets/YARS2/`, `reports/yars2/`, docs |
| **Branch Name** | ❌ REMOVE | use `exp/sirna-pf14-2026` |
| **Module/Package** | ❌ REMOVE | use `arp_orchestrator.py` |
| **CLI Command** | ❌ REMOVE | use `arp` or `arp-pipeline` |
| **Deployment ID** | ❌ REMOVE | use `v24`, `2026.05` |

### 2. Branch Naming Convention

```
main                    ← stable, production-ready
├── feat/<feature>      ← new features
├── fix/<bug>           ← bug fixes  
├── exp/<experiment>    ← experiments ← THIS IS WHERE WE ARE
├── chore/<ops>         ← operations
└── refactor/<area>     ← refactoring
```

**Current:**
- `yars2-sirna-pf14-2026` ❌ (target + project + year mixed)

**Proposed:**
- `exp/sirna-pf14-2026` ✅ (experiment-based)
- `feat/arp-orchestrator-v2`
- `fix/local-db-layer`

### 3. Directory Structure

```
arp-v24/
├── main/                    ← stable code
├── arp/                     ← source code (arp_orchestrator.py, etc.)
├── experiments/             ← experiment-specific code
│   └── sirna-pf14-2026/    ← current experiment
├── targets/                 ← SCIENTIFIC TARGETS
│   ├── YARS2/              ← yars2 STAYS HERE
│   ├── PF14/
│   ├── DGAT1/
│   ├── FSP1/
│   └── ...
├── reports/                 ← outputs organized by target
│   ├── yars2/
│   ├── dgat1/
│   ├── fsp1/
│   └── ...
├── evidence/               ← experimental evidence
├── docs/                   ← documentation
└── .github/                ← CI/CD
```

### 4. Target Registry

```json
// targets/targets.json
{
  "targets": [
    {
      "target_id": "YARS2",
      "aliases": ["YARS2", "yars2", "Tyrosyl-tRNA Synthetase"],
      "project_tags": ["sarcopenia", "sirna", "pf14", "lung"],
      "status": "active",
      "created": "2026-03-01"
    },
    {
      "target_id": "PF14",
      "aliases": ["PF14", "pf14"],
      "project_tags": ["lung", "sirna"],
      "status": "active"
    },
    {
      "target_id": "DGAT1",
      "aliases": ["DGAT1"],
      "project_tags": ["masld", "nsclc", "ferroptosis"],
      "status": "active"
    },
    {
      "target_id": "FSP1",
      "aliases": ["FSP1", "AIFM2"],
      "project_tags": ["nsclc", "ferroptosis"],
      "status": "active"
    }
  ]
}
```

### 5. Config Separation

```yaml
# configs/pipeline.yaml
pipeline:
  version: "24.0"
  experiment_id: "sirna-pf14-2026"
  workstream: "lung-cancer"
  
experiment:
  branch: "exp/sirna-pf14-2026"
  started: "2026-03-01"
  status: "active"

targets:
  primary: ["YARS2"]
  secondary: ["DGAT1", "FSP1"]
  
metadata:
  target_id: "YARS2"      # Scientific name
  project_tags: ["sarcopenia", "sirna"]
```

### 6. Files to Move/Rename

**Move to targets/YARS2/**
```bash
reports/YARS2_YARS2_Delivery_Plan_2026.md  → targets/YARS2/
reports/AAV_shYARS2_*.md                   → targets/YARS2/
```

**Keep in place (experiment code)**
```bash
arp_orchestrator.py    ← NO CHANGE (arp-specific)
boltz2_client.py        ← NO CHANGE
iterative_evaluation.py ← NO CHANGE
```

---

## Implementation Plan

### Phase 1: Immediate (P0)
- [ ] Create `targets/targets.json` registry
- [ ] Rename branch `yars2-sirna-pf14-2026` → `exp/sirna-pf14-2026`
- [ ] Move target-specific reports to `targets/YARS2/`
- [ ] Update .gitignore with new structure

### Phase 2: Short-term (P1)
- [ ] Create `configs/pipeline.yaml` 
- [ ] Separate experiment metadata from target metadata
- [ ] Update arp_orchestrator.py to use registry

### Phase 3: Refinement (P2)
- [ ] Full directory restructuring
- [ ] CI/CD updates
- [ ] Documentation template unification

---

## Consequences

**Positive:**
- Clear separation of concerns
- Reusable branch names
- Easier collaboration
- Better searchability

**Negative:**
- Requires branch rename (breaking change for references)
- Need to update all references to current branch name
- Migration of some files

**Risks:**
- Old links/bookmarks may break
- Team needs to learn new convention

---

## References

- This ADR inspired by user's architecture feedback (2026-05-12)
- Based on GitHub flow + target-centric naming

---

*Decision status: PENDING APPROVAL*
*Proposed by: 오창명 (DRCMOH)*
*Date: 2026-05-12*