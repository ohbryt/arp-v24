# RFdiffusion2 Metallohydrolase: De Novo Enzyme Function Design
**Date:** 2026-05-13  
**Source:** Nature 2026 (s41586-025-09746-w)  
**Authors:** Kim, Woodbury, Ahern et al.  
**Lab:** Baker Lab, University of Washington IPD  
**PMID:** 41339547 | **PMC:** PMC12727532  

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Algorithm** | RFdiffusion2 (flow-matching generative model) |
| **Target** | Zinc metallohydrolase de novo design |
| **kcat/KM Improvement** | 16,000 → **53,000 M⁻¹s⁻¹** (3.3× increase) |
| **kcat** | Up to **1.5 s⁻¹** |
| **vs Natural Enzyme** | 0.05-0.5% of natural metallohydrolase efficiency |
| **Significance** | **Frontier 3: Functional Design Beyond Binding** |

---

## RFdiffusion2: Key Innovation

### vs RFdiffusion (2023)
| Aspect | RFdiffusion | RFdiffusion2 |
|--------|-------------|--------------|
| **Catalytic residue position** | Must pre-specify | **Sequence-position agnostic** |
| **Side-chain rotamer** | Must pre-specify | **Rotamer agnostic** |
| **Input** | Sequence + backbone coordinates | **Active site geometry only** |
| **Output** | Fixed scaffold | **End-to-end generation** |

### RFdiffusion2 Innovation
```
Quantum chemistry-derived active site geometry (Zn²⁺ + catalytic residues)
    ↓
RFdiffusion2 (flow-matching)
    ↓
Backbone + Sequence automatic generation
    ↓
De novo metallohydrolase enzyme
```

---

## Experimental Results

### Round 1: 96 Designs
| Metric | Value |
|--------|-------|
| Most active | kcat/KM = 16,000 M⁻¹s⁻¹ |
| Improvement | Orders-of-magnitude vs prior designed enzymes |

### Round 2: Additional 96 Designs
| Metric | Value |
|--------|-------|
| Highly active enzymes | **3 enzymes** |
| Best kcat/KM | **53,000 M⁻¹s⁻¹** |
| Best kcat | **1.5 s⁻¹** |

### Comparison to Natural Enzymes
| Enzyme Type | kcat/KM Range |
|-------------|---------------|
| Natural metallohydrolases | 10⁵ - 10⁸ M⁻¹s⁻¹ |
| RFdiffusion2 designed | ~53,000 M⁻¹s⁻¹ |
| **% of Natural** | **0.05-0.5%** |

> **First de novo enzyme design reaching industrially relevant catalytic efficiency**

---

## Baker Lab AI Enzyme Design Trio

| Paper | Journal | Target | Status |
|-------|---------|--------|--------|
| Computational Design of Metallohydrolases | **Nature 2026** | Zinc metallohydrolase | New |
| Atom-level Active Site Scaffolding | **Nature Methods 2026** | General scaffolding | Recent |
| Computational Design of Serine Hydrolases | **Science 2025** | Serine hydrolase | Published |

---

## Applications

### Industrial Enzymes
| Application | Example |
|-------------|---------|
| **PET degradation** | Plastic recycling |
| **Biofuel** | Cellulosic ethanol |
| **Chiral synthesis** | Pharmaceutical intermediates |
| **CO₂ fixation** | Carbon capture |
| **Bioremediation** | Environmental cleanup |

### Therapeutic Enzymes (ERT)
| Context | Relevance |
|---------|-----------|
| **Sangamo ST-920 Fabry** | GLA natural enzyme cDNA |
| **De novo ERT candidates** | Future de novo design targets |
| **ADAM/ADAMTS family** | Similar hydrolytic mechanism |
| **MMP family** | Matrix metalloproteinases |

### Drug Discovery
- Enzyme-based drug targets (peptidases, kinases)
- De novo enzyme-based catalysis screening
- Novel catalyst discovery for reactions

---

## Frontier 3: Functional Design Beyond Binding

### 2026 Protein Design Timeline (5/4 - 5/13)
| Date | Development | Significance |
|------|-------------|--------------|
| 5/4 | IsoDDE | Structure prediction |
| 5/5 | HelixFold-Multimer | Complex prediction |
| 5/6 | Boltz × Pfizer | Structure prediction |
| 5/7 | ABCFold + Chai-1r | Structure prediction |
| 5/8 | RFdiffusion antibody (Nature 2025) | Binder design |
| 5/9 | OpenFold3 | Learning data public |
| 5/10 | BindCraft (AF2 backprop) | Binder design |
| 5/11 | BioEmu (dynamic ensemble) | Dynamics |
| 5/12 | Nature De Novo Review + β-pairing RFdiffusion | Review + Binder |
| **5/13** | **RFdiffusion2 Metallohydrolase (Nature 2026)** | **Function** |

### Four-Axis Coverage (Complete)
| Axis | Examples |
|------|----------|
| **Prediction** | AF3, Boltz, OpenFold3, ABCFold |
| **Binder Design** | RFdiffusion antibody, BindCraft, β-pairing |
| **Dynamics** | BioEmu |
| **Function** | RFdiffusion2 metallohydrolase ← **NEW** |

---

## Paradigm: Closed vs Open

| Approach | Lab | Focus | Status |
|----------|-----|-------|--------|
| **AlphaFold3** | DeepMind (2024 Nobel) | Prediction | Closed |
| **RFdiffusion2** | Baker Lab (2024 Nobel) | Function | **Open (GitHub)** |

**GitHub:** https://github.com/baker-laboratory/Metallohydrolase_Enzyme_Design

---

## Quantum Chemistry × AI Hybrid

### Traditional Approach
```
AI learns from evolutionary information (MSA)
```

### NEW Approach (RFdiffusion2)
```
Quantum chemistry-derived active site geometry
    ↓
AI learns first-principles physics
    ↓
First-principles + generative model integration
```

**Implications:** AI for Materials, Chemistry, Catalysis

---

## ARP Pipeline Integration

### Potential Integration Points

| Component | Integration |
|-----------|-------------|
| **Boltz-2** | Structure validation of designed enzymes |
| **RFdiffusion2** | De novo enzyme generation for targets |
| **IterativeEvaluation** | Enzyme candidate screening |
| **ScoringRubric** | Catalytic efficiency scoring |

### De Novo Enzyme Targets for ARP

| Target Area | Enzyme Type | Application |
|-------------|-------------|-------------|
| **Ferroptosis** | De novo GPX4 mimetic | Antioxidant defense |
| **Sarcopenia** | De novo protease | Muscle protein turnover |
| **Cancer** | De novo nuclease | Synthetic lethality |
| **Metabolism** | De novo hydrolase | ACLY/ACSS2 inhibition |

---

## Key References

| Ref | DOI |
|-----|-----|
| Metallohydrolase Nature 2026 | 10.1038/s41586-025-09746-w |
| BioRxiv | 10.1101/2024.11.13.623507v2 |
| Serine Hydrolases Science 2025 | 10.1126/science.adu2454 |
| Active Site Scaffolding Nature Methods 2026 | 10.1038/s41592-025-02975-x |
| Nature De Novo Review Frontier 3 | 10.1038/s41586-026-10328-7 |
| Original RFdiffusion Nature 2023 | 10.1038/s41586-023-06415-8 |
| Baker Lab GitHub | github.com/baker-laboratory/Metallohydrolase_Enzyme_Design |

---

## Predictions

| Year | Prediction |
|------|------------|
| **2026** | First de novo enzyme enters clinical trials (industrial enzyme) |
| **2027** | First therapeutic de novo enzyme ERT candidate |
| **2027** | "Virtual patient + de novo enzyme + spatial AI" 3-stack integration |

---

## Tags
`#RFdiffusion2` `#Metallohydrolase` `#BakerLab` `#DeNovoEnzyme` `#FunctionalDesign` `#FrontierThree`