# MedSci Skills Integration for ARP v24

> **Comprehensive integration of 32 medical research skills into ARP v24**
> Source: `/Users/ocm/.openclaw/workspace/medsci-skills/` → Target: `/Users/ocm/.openclaw/workspace/arp-v24/`

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [All 32 Skills](#all-32-skills)
5. [Python API Reference](#python-api-reference)
6. [Workflows](#workflows)
7. [Reporting Guidelines](#reporting-guidelines)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This integration brings the complete **medsci-skills** bundle into ARP v24, providing:

- **32 specialized medical research skills**
- **Unified Python API** for all skills
- **Workflow orchestration** for multi-step processes
- **PHI safety gate** for data handling
- **33 reporting guidelines** for compliance checking
- **8-phase IMRAD manuscript pipeline**

---

## Quick Start

```python
# Import the integration
from integration.med_sci_integration import MedSciIntegration

# Initialize
medsci = MedSciIntegration()

# 1. Literature Search
results = medsci.search_lit.search("MASLD cardiovascular outcomes", max_results=50)

# 2. Sample Size Calculation
ss = medsci.calc_sample_size.calculate(
    test_type="t_test",
    effect_size=0.5,
    power=0.8
)
print(f"Required N: {ss['total_n']}")

# 3. Compliance Check
report = medsci.check_reporting.check(
    "manuscript/manuscript.md",
    "STROBE"
)
print(f"Compliance: {report.compliance_percentage:.1f}%")

# 4. Write Manuscript
project = medsci.write_paper.write(
    project_dir=".",
    title="Association of BMI with Cardiovascular Outcomes",
    paper_type="original_article",
    target_journal="Radiology",
    research_question="Does elevated BMI predict CV outcomes in T2D?",
    autonomous=True
)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ARP v24                                  │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Integration  │    │   Skills     │    │  References  │      │
│  │              │    │              │    │              │      │
│  │ medsci_      │    │ medsci_      │    │ checklists/  │      │
│  │ integration  │───▶│ orchestrate  │    │ journal_     │      │
│  │ .py          │    │ .py          │    │ profiles/    │      │
│  │              │    │              │    │              │      │
│  │ compliance_  │    │ medsci_      │    │ paper_       │      │
│  │ checker.py   │    │ registry.py  │    │ types/       │      │
│  │              │    │              │    │              │      │
│  │ manuscript_   │    └──────────────┘    └──────────────┘      │
│  │ writer.py    │                                                 │
│  │              │                                                 │
│  │ literature_  │                                                 │
│  │ search.py    │                                                 │
│  └──────────────┘                                                 │
│         │                                                        │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    medsci-skills (Source)                        │
│                                                                 │
│  skills/                                                         │
│  ├── search-lit/          Literature search                      │
│  ├── write-paper/         IMRAD manuscript writing               │
│  ├── check-reporting/     33 reporting guidelines                │
│  ├── analyze-stats/       Statistical code generation           │
│  ├── calc-sample-size/    Sample size calculations              │
│  ├── make-figures/         Publication-ready figures             │
│  ├── meta-analysis/        Systematic review pipeline             │
│  ├── deidentify/           PHI removal                           │
│  ├── clean-data/           Data profiling & cleaning             │
│  ├── find-journal/         93 journal profiles                   │
│  ├── write-protocol/       IRB protocol drafting                 │
│  ├── grant-builder/        Grant proposal structure              │
│  ├── present-paper/        Presentation preparation              │
│  ├── revise/               Reviewer response                      │
│  ├── self-review/          Pre-submission review                 │
│  ├── orchestrate/          Entry point orchestrator              │
│  ├── manage-project/       Project scaffolding                    │
│  ├── intake-project/      Project classification                  │
│  ├── fulltext-retrieval/   PDF download                          │
│  ├── design-study/        Study design validation                │
│  ├── peer-review/         Peer review simulation                 │
│  ├── humanize/            AI pattern removal                    │
│  ├── add-journal/         Journal profile management             │
│  ├── lit-sync/            Zotero + Obsidian sync               │
│  ├── deidentify/          PHI detection                          │
│  ├── batch-cohort/        N×M analysis                           │
│  ├── cross-national/      Cross-national studies                 │
│  ├── find-cohort-gap/     Research gap finder                   │
│  ├── ma-scout/           Meta-analysis scout                   │
│  ├── replicate-study/    Replication planning                    │
│  ├── fill-protocol/      Protocol completion                    │
│  ├── publish-skill/      Skill packaging                        │
│  └── author-strategy/   Author profile analysis                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## All 32 Skills

| # | Skill | Category | Status | Purpose |
|---|-------|----------|--------|---------|
| 1 | search-lit | Literature | ✅ Integrated | PubMed search, citation verification |
| 2 | write-paper | Writing | ✅ Integrated | IMRAD 8-phase manuscript pipeline |
| 3 | check-reporting | Compliance | ✅ Integrated | 33 reporting guidelines |
| 4 | analyze-stats | Statistics | ✅ Integrated | R/Python code generation |
| 5 | calc-sample-size | Statistics | ✅ Integrated | Sample size & power analysis |
| 6 | make-figures | Visualization | ✅ Integrated | ROC, forest plots, flow diagrams |
| 7 | meta-analysis | Review | ✅ Integrated | Systematic review pipeline |
| 8 | deidentify | Data | ✅ Integrated | PHI/PII removal |
| 9 | clean-data | Data | ✅ Integrated | Data profiling & cleaning |
| 10 | write-protocol | Protocol | ✅ Available | IRB protocol drafting |
| 11 | find-journal | Publishing | ✅ Available | Journal recommendation |
| 12 | add-journal | Publishing | ✅ Available | Journal profile management |
| 13 | grant-builder | Grant | ✅ Available | Grant proposal structure |
| 14 | present-paper | Presentation | ✅ Available | Academic talk preparation |
| 15 | revise | Revision | ✅ Available | Reviewer response letters |
| 16 | self-review | Quality | ✅ Available | Pre-submission review |
| 17 | peer-review | Review | ✅ Available | Peer review simulation |
| 18 | humanize | Writing | ✅ Available | AI pattern removal |
| 19 | manage-project | Project | ✅ Available | Project scaffolding |
| 20 | intake-project | Project | ✅ Available | Project classification |
| 21 | fulltext-retrieval | Literature | ✅ Available | PDF download |
| 22 | design-study | Methodology | ✅ Available | Study design validation |
| 23 | orchestrate | Orchestration | ✅ Integrated | Skill routing & workflows |
| 24 | lit-sync | Literature | ✅ Reference | Zotero + Obsidian sync |
| 25 | author-strategy | Literature | ✅ Reference | Author profile analysis |
| 26 | batch-cohort | Statistics | ✅ Reference | N×M analysis templates |
| 27 | cross-national | Statistics | ✅ Reference | Cross-national studies |
| 28 | find-cohort-gap | Literature | ✅ Reference | Research gap finder |
| 29 | ma-scout | Review | ✅ Reference | Meta-analysis scout |
| 30 | replicate-study | Methodology | ✅ Reference | Replication planning |
| 31 | fill-protocol | Protocol | ✅ Reference | Protocol completion |
| 32 | publish-skill | Development | ✅ Reference | Skill packaging |

✅ **Integrated** = Full Python API available
✅ **Available** = Skill source accessible
✅ **Reference** = Integration reference available

---

## Python API Reference

### MedSciIntegration

Main class providing unified access to all skills.

```python
from integration.med_sci_integration import MedSciIntegration

medsci = MedSciIntegration()

# Access integrated skills
medsci.search_lit      # LiteratureSearch
medsci.check_reporting # CheckReportingWrapper
medsci.write_paper     # WritePaperWrapper
medsci.analyze_stats   # AnalyzeStatsWrapper
medsci.calc_sample_size # CalcSampleSizeWrapper
medsci.clean_data      # CleanDataWrapper
medsci.deidentify      # DeidentifyWrapper
medsci.make_figures    # MakeFiguresWrapper
medsci.meta_analysis   # MetaAnalysisWrapper

# Orchestration
result = medsci.orchestrate("Help me write a paper about MASLD")
```

### LiteratureSearch

```python
from integration.literature_search import LiteratureSearch

search = LiteratureSearch()

# Search PubMed
results = search.search("MASLD cardiovascular outcomes", max_results=50)

# Verify citations
verified = search.pubmed.verify_citations(["10.1016/...", "PMID"])

# Export
bibtex = search.to_bibtex(pmids=["12345678"])
markdown = search.to_markdown(results)
```

### ComplianceChecker

```python
from integration.compliance_checker import ComplianceChecker

checker = ComplianceChecker()

# Auto-detect guideline
guidelines = checker.auto_detect_guideline("manuscript/manuscript.md")

# Check compliance
report = checker.check_compliance("manuscript/manuscript.md", "STROBE")

# Check multiple guidelines
reports = checker.check_multiple_guidelines(
    "manuscript/manuscript.md",
    ["STARD", "STARD-AI"]
)
```

### ManuscriptWriter

```python
from integration.manuscript_writer import ManuscriptWriter, PAPER_TYPES

writer = ManuscriptWriter()

# List paper types
print(writer.list_paper_types())

# Write manuscript
project = writer.write_manuscript(
    project_dir=".",
    title="Study Title",
    paper_type="original_article",
    target_journal="Radiology",
    research_question="...",
    autonomous=True
)

# Write case report
project = writer.write_case_report(
    project_dir=".",
    title="A Rare Case of...",
    case_description="...",
    target_journal="Case Reports"
)
```

### Sample Size Calculation

```python
# Two-sample t-test
ss = medsci.calc_sample_size.calculate(
    test_type="t_test",
    effect_size=0.5,
    power=0.8,
    alpha=0.05
)
print(f"N per group: {ss['n_per_group']}")
print(f"IRB text: {ss['irb_text']}")

# Chi-square test
ss = medsci.calc_sample_size.calculate(
    test_type="chi_square",
    effect_size=0.3,
    power=0.8
)

# Cox regression / Log-rank
ss = medsci.calc_sample_size.calculate(
    test_type="log_rank",
    effect_size=0.5,  # HR
    power=0.8
)

# Correlation
ss = medsci.calc_sample_size.calculate(
    test_type="correlation",
    effect_size=0.3,  # r
    power=0.8
)
```

### Statistical Analysis Code Generation

```python
# Generate R code
code = medsci.analyze_stats.generate_code(
    test_type="t_test",
    variables={"var1": "age", "group": "treatment"}
)

# Generate Python code for various tests
tests = medsci.analyze_stats.list_tests()
for test in tests:
    print(test)
```

### Figure Generation

```python
# Generate figure code
code = medsci.make_figures.generate_figure(
    "roc_curve",
    output_path="analysis/figures/roc.png"
)

# Get required figures for study type
required = medsci.make_figures.get_required_figures("rct")
print(f"RCT figures: {required}")
# ['consort_diagram', 'forest_plot', 'kaplan_meier']
```

---

## Workflows

### Using the Orchestrator

```python
from skills.med_sci_orchestrate import MedSciOrchestrator

orchestrator = MedSciOrchestrator()

# Route a request
result = orchestrator.route("Find papers about MASLD")
print(f"Intent: {result['intent']}")  # literature_search
print(f"Skill: {result['skill']}")     # search-lit

# Run predefined workflow
result = orchestrator.run_workflow(
    "data_to_manuscript",
    project_dir="."
)
```

### Available Workflows

| Workflow | Description | PHI Gate |
|----------|-------------|----------|
| `new_project` | Start new research project | No |
| `data_to_manuscript` | Raw data → submission-ready manuscript | Yes |
| `draft_to_submission` | Draft → submission-ready | No |
| `post_rejection` | Handle reviewer comments | No |
| `meta_analysis` | Full systematic review pipeline | No |
| `phi_pipeline` | PHI-safe data → manuscript | Yes |
| `new_study_protocol` | Design new study → IRB protocol | No |
| `full_submission` | Complete pipeline → journal submission | No |
| `case_report` | Case description → published case report | Yes |

### PHI Safety Gate

The orchestrator automatically checks for PHI before routing to data-handling skills:

```python
# Check if PHI gate is needed
phi_check = orchestrator.phi_gate_check("project_dir/")
print(f"PHI Gate Needed: {phi_check['phi_gate_needed']}")
```

---

## Reporting Guidelines

### Primary Guidelines (22)

| Guideline | Version | Study Type |
|-----------|---------|------------|
| STROBE | 2007 | Observational studies |
| CONSORT | 2010 | Randomized controlled trials |
| STARD | 2015 | Diagnostic accuracy |
| STARD-AI | 2025 | AI diagnostic accuracy |
| TRIPOD | 2015 | Prediction models (classic) |
| TRIPOD+AI | 2024 | AI/ML prediction models |
| PRISMA 2020 | 2020 | Systematic reviews |
| PRISMA-DTA | 2018 | DTA systematic reviews |
| PRISMA-P | 2015 | Review protocols |
| CARE | 2016 | Case reports |
| SPIRIT | 2013 | Study protocols |
| ARRIVE | 2.0 | Animal studies |
| CLAIM | 2024 | AI in medical imaging |
| SQUIRE | 2.0 | Quality improvement |
| CLEAR | 2023 | Radiomics |
| MOOSE | 2000 | Meta-analysis of observational |
| GRRAS | 2011 | Reliability/agreement |
| SWiM | 2020 | Synthesis without meta-analysis |
| AMSTAR 2 | 2017 | Systematic review quality |
| MI-CLEAR-LLM | 2025 | LLM accuracy evaluation |
| NOS | Ottawa | Newcastle-Ottawa Scale |
| COSMIN | 2020 | Measurement properties |

### Risk of Bias Tools (11)

| Tool | Version | Purpose |
|------|---------|---------|
| QUADAS-2 | 2011 | DTA risk of bias |
| QUADAS-C | 2021 | Comparative DTA |
| RoB 2 | 2019 | RCT risk of bias |
| ROBINS-I | 2016 | Non-randomized interventions |
| ROBINS-E | 2024 | Non-randomized exposures |
| ROBIS | 2016 | Systematic review bias |
| ROB-ME | 2023 | Missing evidence bias |
| PROBAST | 2019 | Prediction model bias |
| PROBAST+AI | 2025 | AI prediction model bias |
| RoB NMA | 2024 | Network meta-analysis |
| AMSTAR 2 | 2017 | Review quality |

---

## Examples

### Example 1: Full Literature Review

```python
from integration.med_sci_integration import MedSciIntegration

medsci = MedSciIntegration()

# Search for relevant literature
results = medsci.search_lit.search(
    "MASLD cardiovascular outcomes",
    max_results=100,
    publication_type="Clinical Trial[pt]"
)

# Filter to recent high-quality studies
recent = [r for r in results if int(r.pub_date[:4]) >= 2020]
print(f"Recent studies (2020+): {len(recent)}")

# Verify citations
pmids = [r.pmid for r in recent[:20]]
verified = medsci.search_lit.verify(pmids)

# Generate BibTeX for references
bibtex = medsci.search_lit.to_bibtex(pmids)
with open("references.bib", "w") as f:
    f.write(bibtex)
```

### Example 2: Sample Size Justification for IRB

```python
from integration.med_sci_integration import MedSciIntegration

medsci = MedSciIntegration()

# Calculate sample size for primary endpoint
ss = medsci.calc_sample_size.calculate(
    test_type="t_test",
    effect_size=0.5,  # Medium effect size (Cohen's d)
    power=0.8,
    alpha=0.05,
    ratio=1.0  # Equal groups
)

print(f"""
=== SAMPLE SIZE JUSTIFICATION ===

Primary Endpoint: Difference in HbA1c reduction
Statistical Test: Two-sample t-test (independent groups)
Effect Size: Cohen's d = 0.5 (medium)
Significance Level: α = 0.05 (two-sided)
Power: 80%

Required Sample Size:
- Group A (Intervention): {ss['n_per_group'][0]} participants
- Group B (Control): {ss['n_per_group'][1]} participants
- Total: {ss['total_n']} participants

Allowing for 20% dropout:
- Adjusted total: {int(ss['total_n'] * 1.2)} participants

R Code:
{ss['r_code']}

IRB Justification Text:
{ss['irb_text']}
""")
```

### Example 3: Compliance Audit

```python
from integration.compliance_checker import ComplianceChecker

checker = ComplianceChecker()

# Check STROBE compliance
report = checker.check_compliance(
    "manuscript/manuscript.md",
    "STROBE",
    output_path="qc/strobe_checklist.md"
)

print(f"""
=== STROBE COMPLIANCE REPORT ===

Manuscript: {report.manuscript_title}
Guideline: {report.guideline}
Date: {report.date}

Compliance: {report.compliance_percentage:.1f}%

Summary:
- PRESENT: {report.summary['PRESENT']}
- PARTIAL: {report.summary['PARTIAL']}
- MISSING: {report.summary['MISSING']}
- N/A: {report.summary['N/A']}

Priority Action Items:
""")

for action in report.action_items[:5]:
    print(f"  [{action['status']}] Item {action['item_number']}: {action['item_name']}")
```

### Example 4: Figure Generation

```python
from integration.med_sci_integration import MedSciIntegration

medsci = MedSciIntegration()

# Get required figures for diagnostic accuracy study
required = medsci.make_figures.get_required_figures("diagnostic_accuracy")
print(f"Required figures: {required}")

# Generate code for each figure
for fig_type in required:
    code = medsci.make_figures.generate_figure(
        fig_type,
        output_path=f"analysis/figures/{fig_type}.py"
    )
    print(f"Generated: {fig_type}.py")

# Save all code
with open("analysis/generate_figures.py", "w") as f:
    for fig_type in required:
        code = medsci.make_figures.generate_figure(fig_type)
        f.write(f"# {'='*60}\n")
        f.write(f"# {fig_type.upper()}\n")
        f.write(f"# {'='*60}\n\n")
        f.write(code)
        f.write("\n\n")
```

### Example 5: PHI-Safe Data Pipeline

```python
from skills.med_sci_orchestrate import MedSciOrchestrator

orchestrator = MedSciOrchestrator()

# Check PHI status
phi_check = orchestrator.phi_gate_check("data/")

if phi_check['phi_gate_needed']:
    print("⚠️ PHI detected in data files!")
    print("Recommended: Run deidentification first")
    
    # Generate deidentification code
    medsci = MedSciIntegration()
    deid_code = medsci.deidentify.generate_code(
        "data/raw_patient_data.csv",
        output_path="data/deidentified.py"
    )
    
    print(f"\nDeidentification code saved to: data/deidentified.py")
    print("Run: python data/deidentified.py")
else:
    print("✅ No PHI gate needed - proceeding with analysis")
    
    # Run data-to-manuscript workflow
    result = orchestrator.run_workflow(
        "data_to_manuscript",
        project_dir="data/"
    )
```

---

## Troubleshooting

### Import Errors

If you get import errors, ensure the integration path is correct:

```python
import sys
sys.path.insert(0, '/Users/ocm/.openclaw/workspace/arp-v24')

from integration.med_sci_integration import MedSciIntegration
```

### NCBI API Rate Limits

The PubMed search uses NCBI's E-utilities. With an API key, you get 10 requests/second.
Without an API key, you get 3 requests/second.

```python
import os
os.environ['NCBI_API_KEY'] = 'your-api-key'

from integration.literature_search import LiteratureSearch
```

### Missing Checklists

If checklist files are missing, they will be generated from built-in knowledge:

```python
checker = ComplianceChecker()
# Will use built-in checklist if file not found
report = checker.check_compliance("manuscript.md", "STROBE")
```

### Pandoc for DOCX

To generate Word documents, install pandoc:

```bash
# macOS
brew install pandoc

# Linux
sudo apt install pandoc

# Windows
choco install pandoc
```

---

## File Structure

```
arp-v24/
├── integration/
│   ├── med_sci_integration.py       # Unified Python API
│   ├── compliance_checker.py       # 33 reporting guidelines
│   ├── manuscript_writer.py        # 8-phase IMRAD pipeline
│   ├── literature_search.py        # PubMed wrapper
│   └── references/
│       └── checklists/             # 30+ checklist files
│           ├── STROBE.md
│           ├── CONSORT.md
│           ├── PRISMA_2020.md
│           ├── STARD.md
│           ├── STARD_AI.md
│           ├── TRIPOD.md
│           ├── TRIPOD_AI.md
│           └── ... (25 more)
├── skills/
│   ├── med_sci_orchestrate.py      # Workflow orchestrator
│   ├── med_sci_registry.py         # Skill registry
│   └── medsci/
│       └── SKILL.md               # This integration's skill doc
└── MEDSCI_INTEGRATION_README.md   # This file
```

---

## Integration Status

```
Total Skills: 32
├── Integrated (Python API): 9
│   ├── search-lit
│   ├── write-paper
│   ├── check-reporting
│   ├── analyze-stats
│   ├── calc-sample-size
│   ├── make-figures
│   ├── meta-analysis
│   ├── deidentify
│   └── clean-data
├── Orchestrated: 1
│   └── orchestrate
└── Available (Source): 22
    ├── find-journal, add-journal
    ├── write-protocol, grant-builder
    ├── present-paper, revise, self-review
    └── ... (more)
```

---

*Last Updated: 2026-04-18*
*Integrated for ARP v24 | Based on medsci-skills bundle*
