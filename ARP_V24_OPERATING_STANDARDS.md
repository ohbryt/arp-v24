# ARP v24 Operating Standards: Naming & Structure
**Date:** 2026-05-12  
**Version:** 1.0  
**Status:** ACTIVE  

---

## 1. Branch Naming Convention

```
main                    ← stable, production
feat/<feature>          ← new features
fix/<bug>               ← bug fixes
exp/<experiment>        ← experiments (current: exp/sirna-pf14-2026)
chore/<ops>             ← operations
refactor/<area>         ← refactoring
```

**Rules:**
- Use lowercase + hyphens only
- No target names in branch names
- Branch = what you DO, not what you study

**Examples:**
| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `yars2-sirna-pf14-2026` | `exp/sirna-pf14-2026` |
| `fsp1-pipeline` | `feat/ferroptosis-platform` |
| `dgat1-masld` | `exp/masld-targets-2026` |

---

## 2. Directory Structure

```
arp-v24/
│
├── arp/                    ← Core source code (STABLE)
│   ├── __init__.py
│   ├── orchestrator.py     ← Main entry point
│   ├── boltz2_client.py
│   └── ...
│
├── targets/                ← SCIENTIFIC TARGETS ★
│   ├── targets.json        ← Target registry
│   ├── YARS2/             ← yars2 STAYS HERE
│   ├── DGAT1/
│   ├── FSP1/
│   └── ...
│
├── experiments/            ← Experiment-specific (EPHEMERAL)
│   └── sirna-pf14-2026/   ← current experiment
│       ├── data/
│       ├── notebooks/
│       └── results/
│
├── reports/                ← Output reports
│   ├── yars2/              ← target-based
│   ├── dgat1/
│   └── fsp1/
│
├── evidence/              ← Raw evidence
├── docs/                  ← Documentation
├── configs/               ← Configuration
│   └── pipeline.yaml
├── .github/               ← CI/CD
└── README.md
```

---

## 3. Target Registry (targets/targets.json)

```json
{
  "targets": [
    {"id": "YARS2", "aliases": ["yars2"], "status": "active"},
    {"id": "DGAT1", "aliases": ["DGAT1"], "status": "active"},
    {"id": "FSP1", "aliases": ["FSP1", "AIFM2"], "status": "active"},
    {"id": "SLC7A11", "aliases": ["SLC7A11", "xCT"], "status": "active"}
  ]
}
```

**Rule:** Target names exist ONLY in targets/ registry and reports/.

---

## 4. File Naming Rules

| Category | Pattern | Example |
|----------|---------|---------|
| **Reports** | `{Target}_{Topic}_{Year}.md` | `FSP1_DEVELOPMENT_PLAN_2026.md` |
| **Code** | `{module}_{purpose}.py` | `arp_orchestrator.py`, `boltz2_client.py` |
| **Config** | `{type}.yaml` or `*.json` | `pipeline.yaml`, `targets.json` |
| **Evidence** | `{target}_{type}_{date}.json` | `fsp1_bioactivity_2026-05.json` |

---

## 5. Config Fields (configs/pipeline.yaml)

```yaml
pipeline:
  version: "24.0"
  experiment_id: "sirna-pf14-2026"  # WHAT we're doing
  branch: "exp/sirna-pf14-2026"
  
targets:
  primary: ["YARS2"]
  secondary: ["DGAT1", "FSP1"]     # WHAT we're studying
  
metadata:
  created: "2026-03-01"
  owner: "DRCMOH"
```

**Critical separation:**
- `target_id` = scientific (YARS2, FSP1)
- `experiment_id` = operational (sirna-pf14-2026)

---

## 6. Commit Message Format

```
<type>(<scope>): <description>

Types: feat, fix, refactor, docs, test, chore
Scope: target name OR module name

Examples:
feat(fsp1): add FSP1 inhibitor design report
fix(arp): correct boltz2 client import path
refactor(targets): add target registry
docs(sirna): update delivery protocol
```

---

## 7. CI/CD Standards

```yaml
# .github/workflows/ci.yml
on:
  push:
    branches: [main, exp/*, feat/*]  # NOT target names
  pull_request:
    branches: [main]
```

**Rule:** CI triggers on experiment/feature branches, NOT target-specific branches.

---

## 8. Module Classification

| Module | Type | Example |
|--------|------|---------|
| `arp_orchestrator.py` | CORE (arp-specific) | No target name |
| `boltz2_client.py` | CORE (arp-specific) | No target name |
| `iterative_evaluation.py` | CORE (arp-specific) | No target name |
| `evidence_level.py` | UTIL (arp-specific) | Generic |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | REPORT (target-specific) | Has target name |

---

## 9. Quick Reference Card

```
BRANCH:     exp/<what-you-do>
TARGET:     targets/<TARGET>/      ← yars2 here
REPORTS:    reports/<target>/       ← yars2 here
EXPERIMENTS: experiments/<exp-id>/   ← ephemeral
CONFIG:     configs/pipeline.yaml
REGISTRY:   targets/targets.json
```

```
CHECKLIST before committing:
□ Branch name = exp/* or feat/* or fix/* (NO target name)
□ Reports go to reports/<target>/ (HAS target name)
□ Code module = generic name (NO target name)
□ Config has both target_id AND experiment_id
□ Commit message: type(scope): description
```

---

## 10. Migration Guide (Current → Standard)

**Step 1:** Rename branch
```bash
git checkout yars2-sirna-pf14-2026
git branch -m exp/sirna-pf14-2026
git push origin -u exp/sirna-pf14-2026
git push origin --delete yars2-sirna-pf14-2026
```

**Step 2:** Move reports
```bash
mkdir -p reports/yars2
git mv *yars2*.md reports/yars2/
```

**Step 3:** Create registry
```bash
mkdir -p targets
cat > targets/targets.json << 'EOF'
{"targets": [{"id": "YARS2", "aliases": ["yars2"], "status": "active"}]}
EOF
```

**Step 4:** Update configs
```bash
cat > configs/pipeline.yaml << 'EOF'
pipeline:
  version: "24.0"
  experiment_id: "sirna-pf14-2026"
  branch: "exp/sirna-pf14-2026"
targets:
  primary: ["YARS2"]
EOF
```

---

## Summary

| Concept | Rule |
|---------|------|
| **Branch** | exp/feat/fix/<what-you-do> |
| **Target** | targets/<TARGET>/ (scientific) |
| **Report** | reports/<target>/ (target-based) |
| **Code** | generic module names (arp-specific) |
| **Config** | has BOTH target_id AND experiment_id |

---

*Standard version 1.0 | Created 2026-05-12 | Author: DRCMOH*