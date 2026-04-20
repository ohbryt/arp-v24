# ARP v24 - Integrated Research Stack

**Updated:** 2026-04-20  
**Purpose:** Comprehensive biomedical AI research platform for drug discovery

---

## 1. Core AI/LLM Stack

### Groq (Ultra-fast LLM)
```python
from integration.groq_client import summarize, analyze_paper, literature_review
# Speed: 0.6s/summary (17x faster than Ollama!)
```

### Local Models
- Ollama (backup)
- Claude Code / Codex (coding agent)

---

## 2. Literature & Web Research

### Firecrawl (Web Agent)
```python
from integration.firecrawl_integration import research_topic, FirecrawlClient
# Web scraping + autonomous research
```

### Chrome DevTools MCP (Browser Automation)
```javascript
// Setup in ~/.openclaw/openclaw.json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
# Use cases: PubMed scraping, ClinicalTrials automation, screenshots
```

### Tavily Search (Alternative)
```python
# Available as tavily-search skill
```

---

## 3. Molecular Property Prediction

### UMSGFNet (Communications Chemistry 2026)
**Paper:** DOI 10.1038/s42004-026-02010-w

**Key features:**
- Multi-scale graph-fingerprint network
- Atom-level + substructure-level representation
- Memory mechanism for long-range dependencies
- Adaptive weighting of graph + fingerprint features

**Integration:** Use as baseline model for molecular property prediction

---

## 4. Virtual Screening Pipeline

### Horseshoe Crab Peptide Study (2026)
**PMID:** 41999784  
**Workflow:**
```
In silico (trypsin digestion + 6 ML predictors + safety profiling)
    ↓
Virtual screening (multi-criteria ranking)
    ↓
Top candidates synthesized
    ↓
In vitro validation (MTT assay, AO/PI, qRT-PCR)
    ↓
Mechanistic validation (apoptosis pathway)
```

**ARP equivalent:** `ai_metabolic_pipeline.py` + `ai_multitarget_pipeline.py`

---

## 5. Data Validation

### Copy-Paste Detective
**GitHub:** https://github.com/markusenglund/copy-paste-detective

**Purpose:** Detect copy-paste errors in scientific datasets

**Usage:**
```bash
npx copy-paste-detective --dataset your_data.csv
```

**Integration:** Validate all generated datasets before publication

---

## 6. Loop-Think Recurrent Reasoning

```python
from loopthink_integration import MultiHopDiseaseReasoner
# Multi-hop reasoning for target-disease pathways
```

---

## 7. Onco-omics Targets

### One-Carbon Metabolism Deep Review
**Files:** 
- `ONE_CARBON_METABOLISM_DEEP_REVIEW.md` (28KB)
- `ONE_CARBON_METABOLISM_DEEP_REVIEW.pdf` (37KB)

**Targets:**
| Target | Cancer | Stage |
|--------|--------|-------|
| MTHFD2 | 19 tumors ↑ | Phase 1 |
| PHGDH | TNBC 40%, Melanoma 40% | Preclinical |
| MAT2A | MTAP-deleted 30% | Phase 1 |
| SHMT2 | DLBCL, renal | Preclinical |

### Cancer/Metabolic Targets (5-target unified)
**Files:**
- `UNIFIED_5TARGET_AI_PRECISION_ONCOLOGY_REPORT.md`
- `REG3A/PHGDH/ASNS/SLC7A5/GPR81_CANCER_METABOLIC_REPORT.md`

---

## 8. Journal-Ready Output

### Molecular Cancer Submission
**File:** `MOLECULAR_CANCER_OCM_REVIEW.md` (17KB)  
**Journal:** Molecular Cancer (IF 33.9)  
**Format:** Full review article with tables, references, highlights

### PDF Generation
```bash
python3 make_pdf.py  # ReportLab-based
```

---

## 9. Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ARP v24 INPUT                            │
│  (disease query, target gene, literature search)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Literature Collection                                      │
│  - PubMed API (api/pubmed.py)                              │
│  - Firecrawl (web scraping)                                │
│  - Chrome DevTools (automated browsing)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  AI Analysis (Groq/LLM)                                     │
│  - Paper summarization                                     │
│  - Literature review                                       │
│  - Hypothesis generation                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Target Prioritization (Engine 1)                          │
│  - DiseaseEngine (core/scoring_engine.py)                   │
│  - TARGET_REGISTRY (5 diseases, 33+ targets)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Modality Routing (Engine 2)                               │
│  - ModalityRouter (core/modality_routing.py)               │
│  - AssayEngine                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Candidate Generation (Engine 3)                              │
│  - CandidateEngine (core/candidate_engine.py)                │
│  - ADMET prediction                                         │
│  - UMSGFNet-style molecular property prediction             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Validation & Output                                        │
│  - Copy-paste data validation                              │
│  - Loop-Think multi-hop reasoning                          │
│  - PDF/markdown report generation                          │
│  - Journal-formatted output (Molecular Cancer)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Quick Reference Commands

### Literature Search
```python
from api.pubmed import LiteratureIntegrator
result = LiteratureIntegrator().get_sync("PHGDH", "cancer")
```

### Web Research
```python
from integration.firecrawl_integration import research_topic
result = research_topic("PHGDH inhibitors clinical trials 2024", max_sources=10)
```

### Multi-hop Reasoning
```python
from loopthink_integration import MultiHopDiseaseReasoner
result = MultiHopDiseaseReasoner().query("PHGDH → serine → TNBC")
```

### Run Pipeline
```bash
cd arp-v24
python3 -c "from pipeline import ARPv24Pipeline; p = ARPv24Pipeline(); p.run('cancer', top_n=5).print_summary()"
```

### AutoRun x100
```bash
python3 -c "from autorun100 import main; import sys; sys.argv=['','-d','masld','-n','100']; main()"
```

### Data Validation
```bash
npx copy-paste-detective --dataset your_data.csv
```

---

## 11. ARP Files Summary

| Category | Key Files |
|----------|-----------|
| **Pipeline** | `pipeline.py`, `ai_metabolic_pipeline.py`, `ai_multitarget_pipeline.py` |
| **Reports** | `ONE_CARBON_METABOLISM_DEEP_REVIEW.md`, `MOLECULAR_CANCER_OCM_REVIEW.md` |
| **Integrations** | `integration/groq_client.py`, `firecrawl_integration.py`, `loopthink_integration.py` |
| **Tests** | `tests/test_pipeline_integration.py`, `tests/test_candidate_engine.py` |
| **Utilities** | `autorun100.py`, `make_pdf.py`, `convert_to_pdf.py` |

---

## 12. Active Research Areas

1. **One-Carbon Metabolism** - MTHFD2, PHGDH, SHMT2, MAT2A
2. **Cancer/Metabolic Targets** - REG3A, PHGDH, ASNS, SLC7A5, GPR81
3. **Virtual Screening** - In silico → In vitro workflow
4. **Molecular Property Prediction** - UMSGFNet-based DL models
5. **Multi-hop Reasoning** - Loop-Think for pathway analysis
6. **Data Validation** - Copy-paste error detection

---

_Last updated: 2026-04-20_