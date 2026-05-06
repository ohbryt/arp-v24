# AtlasAI: Multi-Agent Reasoning for Human Protein Atlas
**bioRxiv | Green et al. (KTH, Karolinska, King's College London) | 2026-04-24**

## Overview
AtlasAI is a multi-agent system for natural language querying of the Human Protein Atlas database.

**Key Stats:**
- 26M immunohistochemistry images
- 20,162 genes
- 64 cell lines
- 17 cancer types
- 44 normal tissues

## Architecture

### 5 Specialized Agents
| Agent | Function |
|-------|----------|
| Deep Research | Multi-constraint DB queries (e.g., "kinases enriched in brain but absent from blood") |
| Investigator | Gene page information extraction |
| Refinement | Query refinement |
| Interpretation | Results interpretation |
| ASO (Autonomous Scientific Orchestrator) | Multi-step research coordination + tool orchestration |

### Autonomous Scientific Orchestrator (ASO)
- Accepts research objective
- Independently coordinates agents through tool selection
- **Code-level validation** at each step
- **Artifact store** — persists every intermediate output
- **No hallucination** — outputs constrained to externally computed artifacts

## Key Results

### Performance
| Metric | AtlasAI | Frontier Models |
|--------|---------|----------------|
| Task Resolution | **100%** | Lower |
| Computational Cost | **1×** | 56-240× higher |
| Hallucination | **Zero** | Present |

### ASO Evaluation
- **486 genes** identified
- **1,006 measurements** retrieved
- **12 publication-ready visualizations** generated
- **Zero human intervention**

## Relevance to ARP

### 1. Target Expression Analysis
Our 5 targets in Human Protein Atlas:
- KDM4A — tissue-specific expression
- SLC7A11 — cancer vs normal tissue
- DGAT1 — metabolic tissue distribution
- GPX4 — oxidative stress tissues
- YARS2 — mitochondrial-enriched tissues

### 2. Multi-Agent Architecture Reference
```
AtlasAI Architecture → ARP Pipeline Design
├── Deep Research Agent → Literature Search Agent
├── Investigator Agent → Target Analysis Agent
├── Refinement Agent → Hypothesis Refinement
├── Interpretation Agent → Results Synthesis
└── ASO → Orchestration Layer
```

### 3. Anti-Hallucination Strategy
AtlasAI's approach:
1. **Constraint to computed artifacts** — only use verified outputs
2. **Semantic validation** — validate intermediate reasoning
3. **Error recovery** — autonomous error correction
4. **Audit trails** — complete reproducibility

→ Apply to our BioMiner + literature pipeline

## How to Use

### Human Protein Atlas Query Example
```
Query: "Find genes enriched in lung cancer, involved in ferroptosis, and prognostic in NSCLC"
AtlasAI Process:
1. Deep Research → Identify ferroptosis-related genes
2. Investigator → Extract lung cancer expression
3. Refinement → Add prognostic filter
4. Interpretation → Generate survival plots
```

## Next Steps for ARP
- [ ] Deploy AtlasAI sidebar for our target genes
- [ ] Query expression in lung vs normal tissue
- [ ] Check subcellular localization
- [ ] Validate with our spatial transcriptomics data
- [ ] Integrate with our multi-agent pipeline

## Reference
- DOI: https://doi.org/10.21203/rs.3.rs-9452188/v1
- Human Protein Atlas: https://www.proteinatlas.org
