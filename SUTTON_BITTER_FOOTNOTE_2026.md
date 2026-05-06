# Sutton's Bitter Footnote in Small Molecule Drug Discovery
**Author:** Sylvain Gariel | X/Twitter Thread
**Date:** May 2026

## Executive Summary

The Bitter Lesson (Sutton 2019) has arrived in sequence biology and protein structure, but **stalled in small-molecule drug discovery on hard targets**. This analysis explains why, what actually works, and the strategic implications.

---

## Part 1: Where Bitter Lesson Won and Why

### Winning Domains
| Domain | Models | Why Scale Works |
|--------|--------|-----------------|
| Genome biology | Evo 2 (9T nucleotides) | DNA = 4-letter alphabet, nature already ran the experiment |
| Protein structure | AlphaFold 2/3, RoseTTAFold, ESMFold | 200K+ PDB structures, training = biosphere |
| Protein design | RFdiffusion, ProteinMPNN, ProGen3 | Tens of billions of natural examples |

**Key insight:** Training distribution IS the biosphere. Scale + general methods win.

---

## Part 2: Where It Stalled and Why

### The Hard Truth About Small Molecules

**Problem:** Small molecules engage targets with only a handful of atoms
- Getting potency AND selectivity together on hard targets is NOT free
- The chemistry that drives potency ≠ chemistry that drives selectivity
- Both battles must be won at the level of individual interactions

### Two-Atom Selectivity: Xanomeline/Cobenfy

**BMS paid $14B for Karuna** → Cobenfy (xanomeline + trospium)

**Selectivity mechanism (Powers et al., Nature Chemical Biology, 2022):**
- M1/M4 preferred over M2/M3
- **2 atoms decide** receptor selectivity:
  - M4 has Leucine at key position
  - M2 has bulkier Phenylalanine
- Plus small network of salt bridges in 2nd extracellular loop
- You cannot find this without: right simulation, right question, enough sampling

**Why AlphaFold can't find this:**
- PDB doesn't contain this mechanism
- Requires extensive all-atom MD with proper sampling

### Transient State Drug Design: KRAS

| Drug | Mechanism | Outcome |
|------|----------|---------|
| Sotorasib/Adagrasib | G12C covalent inhibitor | ~6 month PFS, fast resistance |
| Daraxonrasib | Tri-complex (CypA + KRAS) | **13.2 month OS** in pancreatic cancer Phase 3 |

**Revolution Medicines stock +41%, $27B market cap, Merck circled at $30B**

**Key insight:** 
- Sotorasib = fits KRAS ground state
- Daraxonrasib = designs molecule whose induced ternary complex fits a **transient state**

### Why AlphaFold Doesn't Close the Gap

**AlphaFold 2:**
- Predicts single structure = weighted average of low-energy conformations
- Insensitive to point mutations (Pak et al. 2023: no correlation AF confidence vs experimental ddG)
- Biased toward dominant conformations

**AlphaFold 3 (Zheng et al. 2025):**
- Excels on static protein-ligand complexes
- Struggles with conformational changes >5Å RMSD
- Persistent bias toward active GPCR conformations
- Poor on ternary complexes
- No reliable affinity ranking

**The fundamental problem:**
> "The PDB contains wild-type folds, not thermodynamic landscapes. A network that learned to reproduce the PDB learned to reproduce folds."

---

## Part 3: The Measurement Problem

### Why Data Doesn't Scale

**Example: GPCR structural biology**
- Brian Kobilka won 201 Nobel for first active-state GPCR structures
- Methods: thermostabilizing mutations, fusion proteins, engineered nanobodies, LCP crystallography
- Even with cryo-EM, inactive-state GPCRs remain hard

**Cryo-EM costs:**
- Single high-quality structure: months + $100K-500K
- Dataset for foundation model: hundreds of millions of dollars + many years away

**The bitter footnote:**
> "The data side does not cheapen on the same curve [as compute]."

---

## Part 4: What Actually Works

### Physics-Informed AI

**Not replacing MD with AI — augmenting MD with AI**

| Approach | Examples | Current Status |
|---------|----------|---------------|
| Learned conformational ensembles | Bowman lab, Noé Boltzmann generators, AlphaFlow, BioEmu | Reproduce experimental observables |
| ML force fields | ANI, NequIP, MACE | Quantum chemistry accuracy + NN speed |
| Closed-loop chemistry | Active learning | Model chooses next experiment |
| MD + AI hybrid | D.E. Shaw Anton + ML | GPCR/kinase dynamics for 2 decades |

### Clinical Track Record

| Method | Approved Drugs |
|-------|-------------|
| Physics-informed AI (new) | **ZERO** |
| Xanomeline (classical) | Cobenfy 2024 |
| MD + medicinal chemistry | Daraxonrasib 2026 |

---

## Part 5: Strategic Implications

### For Drug Discovery Programs

1. **For hard targets (GPCR, ion channels, transcription factors):**
   - Pure generative AI ≠ sufficient
   - Need: physics-based augmentation + conformational ensembles
   - Key metric: MD-accessible dynamics, not benchmark accuracy

2. **Validation is the bottleneck:**
   > "Raising the quantity of hypotheses without improving validation produces no medicines."
   - TxConformal approach: FDR control + tight coupling of generation to decision

3. **What would change assessment:**
   - Foundation model trained on sequences + structures + MD ensembles + dense ddG
   - Predicts state-resolved conformational ensembles at experimental accuracy
   - Generalizes outside training set
   - **This breakthrough has not arrived.**

### For ARP Pipeline

| Our Tool | Relevance | Assessment |
|---------|-----------|------------|
| AFSample2 | Conformational ensembles | **Critical** for transient states |
| LinkLlama | Learned conformational ensembles | **Critical** for dynamics |
| TxConformal | FDR control for hits | **Critical** for validation |
| Pure generative AI | Molecule generation | **Insufficient alone** |

### The Actual Bitter Lesson in Drug Discovery

> "The field that wins the next decade of drug discovery will accept that it is operating in a regime where data has to be generated against the specific target, state, and mutant of interest, where dynamics rather than structure is the substrate of selectivity, where MD is still the workhorse and AI earns its place by augmenting it."

**Benchmark wins do not pay for Phase 3 trials.**

---

## References

### AlphaFold Limitations
- Pak et al. PLOS One 2023 (1,154 mutations, 800 GFP variants)
- Buel & Walters Nat Struct Mol Biol 2022
- Zheng et al. bioRxiv 2025 (AF3 assessment)
- Chib et al. arXiv 2025 (GPCR bias)

### Case Studies
- Powers et al. Nature Chem Biol 2022 (xanomeline selectivity)
- Ostrem et al. Nature 2013 (KRAS G12C discovery)
- Revolution Medicines RASolute 302 Phase 3 results (April 2026)

### Physics-Informed AI
- Noé et al. Science 2019 (Boltzmann generators)
- Jing et al. ICML 2024 (AlphaFlow)
- Lewis et al. bioRxiv 2024 (BioEmu)
- Batatia et al. NeurIPS 2022 (MACE)
- D.E. Shaw Research (Anton MD)
