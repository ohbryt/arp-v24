# ARP Pipeline Enhancement: Complete Integration
**Date:** 2026-05-11  
**Version:** Final  
**Based on:** 6 cutting-edge papers in AI-driven drug discovery

---

## Executive Summary

ARP Pipeline을 6개 최신 논문 기반으로全面統合합니다:

| # | Paper | Key Insight | ARP Integration |
|---|-------|-------------|-----------------|
| 1 | **Pharmaceuticals 2026** | Rentosertib AI pathway | FSP1 template |
| 2 | **Briefings in Bioinformatics 2026** | Boltz-2 affinity | boltz2_client.py |
| 3 | **medRxiv 2026** | PD Union PK/PD | Dose prediction |
| 4 | **bioRxiv 2026** | SLiMNet motifs | ESM2 + Boltz-2 |
| 5 | **Nature 2025** | FSP1 lung cancer | Triple ferroptosis |
| 6 | **bioRxiv 2026** | ImmuneKG | TME enhancement |

---

## 1. Reference Cases: Success Stories

### 1.1 Rentosertib (Pharmaceuticals 2026)

| Metric | Value |
|--------|-------|
| Target | TNIK (AI-discovered) |
| Indication | Idiopathic Pulmonary Fibrosis |
| Timeline | ~18 months to preclinical |
| Cost | ~$150K (self-reported) |
| Phase IIa | +98.4 mL FVC vs placebo ✅ |

**Our FSP1 analog:**
- Same AI-driven target ID → FSP1 (first-in-class)
- Same generative chemistry → Boltz-2 + FSEN1/viFSP1 leads
- Timeline: 30-42 months to IND

---

## 2. Complete Technology Stack

### 2.1 Layers

| Layer | Tools | Purpose |
|-------|-------|---------|
| **Knowledge Graphs** | ImmuneKG, PrimeKG | Target discovery |
| **Protein LLMs** | ESM2, Boltz-2 | Structure + motifs |
| **Motif Discovery** | SLiMNet | SLiM detection |
| **Target ID** | arp_orchestrator.py | Playbook orchestration |
| **Molecular Design** | LinkLlama | Linker design |
| **ML Biomarkers** | scikit-learn, XGBoost, PyTorch | Patient stratification |
| **PK/PD** | PD Union framework | Dose modeling |
| **GNN** | HeteroPNA-Attn | ImmuneKG (future) |

### 2.2 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARP v24: COMPLETE PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DATA LAYER                                                       │
│  ├── Multi-omics (scanpy, pandas)                                │
│  ├── Knowledge Graphs (ImmuneKG, PrimeKG)                         │
│  └── Literature (PubMed, patents)                                 │
│                                                                  │
│  TARGET DISCOVERY                                                 │
│  ├── arp_orchestrator.py (playbooks)                            │
│  ├── ImmuneKG (immune diseases)                                  │
│  └── GNN scoring (HeteroPNA-Attn)                               │
│                                                                  │
│  MOLECULAR DESIGN                                                 │
│  ├── ESM2 (embeddings) → SLiMNet (motifs)                     │
│  └── Boltz-2 (structure + affinity)                             │
│                                                                  │
│  BIOMARKER STRATIFICATION                                        │
│  ├── ML (FRS, NRF2, TMS, CBMS)                                │
│  ├── TME Score (ImmuneKG-enhanced)                              │
│  └── PD Union (PK/PD modeling)                                  │
│                                                                  │
│  CLINICAL TRANSLATION                                            │
│  ├── Patient selection (CBMS-based)                              │
│  ├── Combination (RT, ICI, chemo)                               │
│  └── Dose prediction (PD Union)                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Novel AI Models Summary

### 3.1 Boltz-2 (Briefings in Bioinformatics 2026)

| Feature | Value |
|---------|-------|
| Function | Protein structure + affinity prediction |
| Special | Affinity module for binding estimation |
| Benchmark | Best for drug discovery |

### 3.2 PD Union (medRxiv 2026)

| Feature | Value |
|---------|-------|
| Function | Automated PK/PD modeling |
| Performance | NRMSE 0.146, 14/15 studies outperformed |
| Benefit | Mechanistic + interpretable |

### 3.3 SLiMNet (bioRxiv 2026)

| Feature | Value |
|---------|-------|
| Function | Short Linear Motif detection |
| Performance | AUCROC 0.81 |
| Use | FSP1/SLC7A11/GPX4 interaction sites |

### 3.4 ImmuneKG (bioRxiv 2026)

| Feature | Value |
|---------|-------|
| Function | Immune-cell knowledge graph |
| Performance | Hits@100 = 0.99 |
| Use | TME Score enhancement, ICI response |

---

## 4. ARP Programs

### 4.1 Triple Ferroptosis Platform (NSCLC)

```
┌─────────────────────────────────────────────────────┐
│          Triple Ferroptosis Induction                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  FSP1 → CoQ → CoQH2 (ferroptosis defense)         │
│      ↓                                               │
│  SLC7A11 → cystine → GSH → GPX4                    │
│      ↓                                               │
│  DGAT1 → lipid droplets → PUFA accumulation         │
│      ↓                                               │
│  = Maximum ferroptosis without normal toxicity       │
└─────────────────────────────────────────────────────┘
```

### 4.2 Dual ACLY/ACSS2 (MASH)

```
Acetyl-CoA sources:
├── ACLY (glucose → acetyl-CoA)
└── ACSS2 (acetate → acetyl-CoA)

Dual block → NO BYPASS → Steatosis + Fibrosis ↓
```

---

## 5. ML Biomarkers

### 5.1 Composite Biomarker Score (CBMS)

```
CBMS = 0.30 × FRS + 0.25 × NRF2 + 0.25 × TMS + 0.20 × TFCS
```

| Score | Method | Purpose |
|-------|-------|---------|
| FRS | LASSO + RF (24 genes) | Ferroptosis competence |
| NRF2 | ssGSEA | KEAP1/NRF2 pathway |
| TMS | CIBERSORTx + RF | TME (ImmuneKG-enhanced) |
| TFCS | XGBoost | Triple combo response |

### 5.2 Patient Stratification

| CBMS Range | Treatment |
|-----------|----------|
| ≥75 | FSP1i monotherapy |
| 50-74 | FSP1i + radiotherapy |
| 25-49 | FSP1i + pembrolizumab |

---

## 6. Clinical Development

### 6.1 FSP1 Program (NSCLC)

| Parameter | Value |
|-----------|-------|
| Target | FSP1 (first-in-class) |
| Indication | KEAP1/STK11/NFE2L2-altered LUAD |
| Biomarker | FSP1 IHC + KEAP1/STK11 genotype + CBMS |
| Timeline | 33-42 months to IND |
| Cost | $15-35M |

### 6.2 ACLY/ACSS2 Program (MASH)

| Parameter | Value |
|-----------|-------|
| Target | Dual ACLY + ACSS2 |
| Indication | MASH F2-F3 |
| Biomarker | MRI-PDFF ≥30%, fibrosis markers |
| Timeline | 30-39 months to IND |
| Cost | $12-28M |

---

## 7. Timeline

```
2026 Q2-Q3   Target Discovery (ImmuneKG + arp_orchestrator)
2026 Q3-Q4   Molecular Design (ESM2 + SLiMNet + Boltz-2)
2026 Q4      ML Biomarkers (FRS, CBMS, TME)
2027 Q1-Q2   Lead Optimization
2027 Q3-Q4   IND-Enabling Studies
2028 Q1      IND Filing
2028 Q4      Phase I Start
```

---

## 8. Key References

1. **Pharmaceuticals 2026** (doi:10.3390/xxx)
   - Generative AI in drug discovery
   - Rentosertib: AI-discovered target → Phase IIa

2. **Briefings in Bioinformatics 2026** (doi:10.1093/bib/xxx)
   - Boltz-2 benchmarking for protein-aptamer
   - Affinity prediction module

3. **medRxiv 2026** (doi:10.64898/2026.05.05.26352278)
   - PD Union: Automated PK/PD modeling
   - NRMSE 0.146, 14/15 outperformed

4. **bioRxiv 2026** (doi:10.64898/2026.05.04.722713)
   - SLiMNet: Short Linear Motif detection
   - ESM2 embeddings + siamese networks

5. **Nature 2025** (doi:10.1038/s41586-025-09710-8)
   - FSP1 in lung cancer: 80% tumor reduction

6. **bioRxiv 2026** (doi:10.64898/2026.04.30.721823)
   - ImmuneKG: Immune-cell knowledge graph
   - Hits@100 = 0.99

---

## 9. Files in arp-v24/

| File | Content |
|------|---------|
| `ARP_PIPELINE_ENHANCEMENT_2026.md` | This document |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | FSP1 preclinical |
| `ML_BIOMARKER_STRATEGY_2026.md` | ML biomarkers |
| `ACLY_ACSS2_DEVELOPMENT_PLAN_2026.md` | MASH program |
| `boltz2_client.py` | Boltz-2 integration |
| `arp_orchestrator.py` | Playbooks |

---

## 10. Conclusion

6개 논문의 인사이트를 통합하여 완성된 AI-driven drug discovery pipeline:

- **Rentosertib model**: AI target → Phase IIa 성공
- **Boltz-2**: 구조 + 결합력 예측
- **PD Union**: PK/PD 자동화
- **SLiMNet**: 단백질 모티프 발견
- **ImmuneKG**: 면역세포 네트워크
- **Nature FSP1**: 폐암 ferroptosis 표적

**ARP v24 = Rentosertib 다음 세대의 AI drug discovery platform**

---

*Generated: 2026-05-11 | ARP v24*  
*Integration: 6 papers + complete pipeline*  
*GitHub: github.com/ohbryt/arp-v24 (yars2-sirna-pf14-2026)*