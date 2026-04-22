# Cardiac-Homing Peptide-GDF10-Fc Fusion Protein
## Antigen Synthesis Sequence Document

**Document Type:** Protein Sequence for Antigen Synthesis  
**Date:** April 22, 2026  
**Purpose:** Commission antigen synthesis for Cardiac-Homing Peptide-GDF10-Fc  
**Expression System:** CHO cells (recommended) or HEK293

---

## 1. Construct Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Fusion Protein Architecture                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [C7 Homing] ─ [Linker] ─ [GDF10 Mature] ─ [Linker] ─ [hIgG1 Fc]   │
│                                                                      │
│      8 aa      10 aa       ~160 aa        10 aa       ~230 aa       │
│                                                                      │
│  Total: ~418 amino acids (without signal peptide)                     │
│  Total with signal peptide: ~440 amino acids                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Domain Details

| Domain | Amino Acids | Length | Source |
|--------|------------|--------|--------|
| **C7 Cardiac-Homing** | 1-8 | 8 aa | Synthetic |
| **Linker 1** | 9-18 | 10 aa | (GGGGS)₂ |
| **GDF10 Mature** | 19-178 | 160 aa | Human GDF10 (P55107:300-459) |
| **Linker 2** | 179-188 | 10 aa | (GGGGS)₂ |
| **hIgG1 Fc** | 189-418 | 230 aa | Human IgG1 |

---

## 2. Component Sequences

### 2.1 C7 Cardiac-Homing Peptide

```
Name:     C7 (Cardiac-homing)
Target:   Cardiac myosin binding protein C
Sequence: APWHLSSQ
Length:   8 amino acids

Note: This peptide homes specifically to cardiomyocytes
```

### 2.2 Flexible Linker (GGGGS)₂

```
Sequence: GGGGSGGGGS
Length:   10 amino acids
Purpose:  Flexibility between domains, prevents steric hindrance
```

### 2.3 Human GDF10 Mature Domain (P55107:300-459)

```
Source:     UniProt P55107 (GDF10_HUMAN)
Positions:  300-459 (mature region, C-terminal)
Length:     160 amino acids

Sequence:
300 GPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRKDRRKKGQEVF
350 FMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPK
400 S FDAYYCAGACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDK
450 MNSLGVLFLDENRNVVLKVYPNMSVDTCACR

Full mature domain (160 aa):
GPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRKDRRKKGQEVFMAASQVLDFDEK
TMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDAYYCAGACEFPMPKIVRPSNH
ATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLKVYPNMSVDTCACR
```

### 2.4 Human IgG1 Fc Region

```
Source:     Human IgG1 (hinge + CH2 + CH3)
Positions:  Hinge (226-230) + CH2 (231-340) + CH3 (341-476)
Length:     ~230 amino acids

Hinge Region:
DKTHTCPPCP

CH2 Domain (partial, critical for function):
APELLGGP SVFLFPPKP KDTLMISRT PEVTCVVVD VSHEDPEVK FNWYVDGVE
VHNAKTKP REEQYNSTYR VVSVLTVLHQ DWLNGKEYKC RVSNKALPAP IEKTISKAK

CH3 Domain:
GQPREPQVY TLPPSREEMT KNQVSLTCLVK GFYPSDIAV EWESNGQPEN NYKTTPPVLD
SDGSFFLYS KLTVDKSRWQ QGNVFSCSVM HEALHNHYTQ KSLSLSPGK

Full Fc sequence (230 aa):
DKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVE
VHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQ
VYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKL
TVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK
```

---

## 3. Complete Construct (DNA & Protein)

### 3.1 Amino Acid Sequence

```
APWHLSSQGGGGSGGGGSSGPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRKD
RRKKGQEVFMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDA
YYCAGACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLK
VYPNMSVDTCACRGGGGSGGGGSDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVT
CVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCK
VSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNG
QPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK
```

**Total Length: 418 amino acids**  
**Molecular Weight: ~46.5 kDa** (without glycosylation)  
**pI: ~8.5**

### 3.2 Codon-Optimized DNA Sequence (E. coli/CHO compatible)

```
# For mammalian expression (CHO/HEK293):
ATGGCGCCGTGGCACTTGAGCTCTCAGTGCGGTGGTGGCGGCAGCGGTGGTGGTAGCGGTCC
GCTGCAGGACAACGAGCTGCCAGGTCTGGACGAGAGGCCTCCAAGAGCTCACGCTCAGCACT
TCCACAAGCACCAACTGTGGCCTTCCCCGTTCCGCGCTCAAGCCTAGACCTGGCAGAAAGGA
CCGGCGGAAGAAGCAGGGCCAGGAGGTCTTCATGGCGGCGTCCCAAGTCTTGGACTTCGACG
AAAAGACCATGCAAAAGGCTAGGCGGAAGCAATGGGACGAGCCCAGAGTGTGTTCCCGGAGGT
TACAAGCTGGTGGACTTCGCTGACATAGGCTGGAACGAGTGGATCATCTCCCCCAAGTCTTT
CGACGCTTACTACTGTGCTGGTGCCTGTGAGTTCCCAATGCCTAAGATCGTGCGCCCTTCCA
ACCACGCCACCATCCAGTCCATCGTCAGAGCTGTTGGCATCATCCCTGGTATCCCTGAGCCTT
GCTGTCCGGACAAGATGAACTCTCTGGGTGTGCTGTTCCTGGACGAGAACCGCAACGTCGTT
CTCAAGGTCTACCCCAACATGTCTGTGGACACCTGCGCTTGCAGGGGTGGTGGCAGCGGTGG
TGGTAGCGACAAGACCCACACCTGCCCTCCTTGTCCAGCTCCTGAACTTGGTGGTCCATCAG
TCTTCCTGTTCCCTCCCAAGCCTAAGGACACCCTCATGATCTCCAGAACCCCTGAGGTGACC
TGTGTGGTGGTGGACGTTTCTCACGAGGACCCCGAGGTCAAGTTCAACTGGTACGTGGACGG
CGTGGAAGTCCACAACGCCAAGACCAAGCCTAGAGAGGAGCAATACAACAGCACCTACCGGGT
GGTGTCCGTGCTGACCGTGTTGCACCAAGACTGGCTCAACGGCAAAGAGTACAAGTGCAAAGT
GTCCAACAAGGCTCTGCCTGCTCCTATCGAGAAGACCATCTCCAAGGCCAAGGGCCAACCCAG
AGAGCCACAAGTCTACCTGCCAACCTTCCCTCGGAGGGAGATGACCAAGAACCAAGTGTCCC
TGACCTGCCTGGTGAAGGGTTTCTACCCTTCCGACATTGCTGTGGAGTGGGAGTCCAACGGG
CAGCCCGAGAACAACTACAAGACCACCCCTCCCGTGCTGGACTCCGACGGCTCCTTCTTCTT
GTACTCTAAGCTGACCGTGGACAAGTCCAGATGGCAGCAGGGCAACGTCTTCTCCTGCTCTG
TGATGCACGAGGCTCTGCACAACCACTACACCCAGAAGTCCCTGTCCCTGTCCCCGGGAAAG
TGA
```

**Note:** This is a codon-optimized sequence for high expression in mammalian cells.

---

## 4. Expression Recommendations

### 4.1 Expression System

| System | Pros | Cons |
|--------|------|------|
| **CHO cells** | Proper glycosylation, FDA-approved | Higher cost |
| **HEK293** | High yield, easy transfection | Different glycosylation |
| **E. coli** | Fast, cheap | No glycosylation, inclusion bodies |

**Recommendation:** CHO cells for therapeutic development

### 4.2 Purification Strategy

| Step | Method |
|------|--------|
| **Capture** | Protein A/G affinity chromatography |
| **Polishing** | Ion exchange (CEX or AEX) |
| **Final** | Size exclusion chromatography (SEC) |

### 4.3 Quality Control

| Test | Method | Acceptance Criteria |
|------|--------|-------------------|
| **Purity** | SDS-PAGE | >95% |
| **Identity** | Western blot | Anti-GDF10, Anti-Fc |
| **Aggregation** | SEC-HPLC | <5% aggregates |
| **Endotoxin** | LAL | <10 EU/mg |
| **Bioactivity** | Smad reporter assay | EC50 < 100 nM |

---

## 5. Alternative: Shorter Construct (Research Grade)

If cost is a concern, consider this shorter version:

### 5.1 C7-GDF10 Mature (Without Fc)

```
APWHLSSQGGGGSGGGGSSGPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRKD
RRKKGQEVFMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDA
YYCAGACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLK
VYPNMSVDTCACR
```

**Length:** 188 amino acids  
**MW:** ~21 kDa  
**Advantage:** Lower cost, suitable for initial validation

### 5.2 Fc-Only with GDF10 RGD Modifications

If direct cardiac targeting is not critical, consider:
- GDF10-Fc (without C7 peptide)
- Add RGD motif for integrin targeting
- Use cardiac-specific formulation (liposome, NP)

---

## 6. Vendor Recommendations

### For Antigen Synthesis (Peptide):

| Vendor | Quality | Turnaround | Notes |
|--------|---------|------------|-------|
| **GenScript** | High | 2-3 weeks | GMP available |
| **ChinaPeptides** | High | 1-2 weeks | Cost-effective |
| **AnaSpec** | High | 2-3 weeks | FBI-free |
| **21st Century Bio** | High | 2-4 weeks | Modified peptides |

### For Recombinant Expression:

| Vendor | Service | Notes |
|--------|---------|-------|
| **GenScript** | CHO expression | End-to-end service |
| **Lonza** | CHO expression | GMP manufacturing |
| **Catalent** | Biologics | Full service |

---

## 7. Summary for Antigen Commission

### Recommended Construct:

**Cardiac-Homing Peptide-GDF10-Fc Fusion**

```
C7 Peptide (APWHLSSQ) + (GGGGS)₂ + GDF10 Mature (160 aa) + (GGGGS)₂ + hIgG1 Fc (230 aa)

Total: 418 amino acids
Expression: CHO cells (mammalian)
Purity required: >95%
Endotoxin: <10 EU/mg
Bioactivity: Smad1/5/8 phosphorylation EC50 < 100 nM
```

### For Initial Screening:

Use the shorter version (C7-GDF10, 188 aa) first to validate:
1. Cardiac homing specificity
2. GDF10 bioactivity
3. Binding to cardiac receptors

Then proceed to full Fc fusion for extended half-life studies.

---

## 8. Contacts for Synthesis

### GenScript (Recommended)
- Website: www.genscript.com
- Service: Peptide synthesis + Recombinant protein
- Quote: www.genscript.com/quote.html

### ChinaPeptides
- Website: www.chinapeptides.com
- Service: Peptide synthesis
- Cost-effective for larger quantities

---

*Document generated by ARP v24 Research Pipeline · April 2026*  
*For laboratory use and antigen synthesis commissioning only*
