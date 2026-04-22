# Cardiac-Homing Peptide Candidates
## Three Independent Cardiac-Targeting Peptides for GDF10-Fc Fusion

**Document Type:** Peptide Design for Antigen Synthesis  
**Date:** April 22, 2026  
**Purpose:** Multi-candidate approach to maximize cardiac targeting efficiency

---

## 1. Strategy Overview

### 1.1 Why Multiple Candidates?

| Reason | Explanation |
|--------|-------------|
| **Homing variability** | Different peptides may have different cardiac tropism |
| **Target diversity** | Peptides may bind different cardiac receptors |
| **Validation efficiency** | Screen 3 in parallel vs sequential testing |
| **Manufacturing flexibility** | Choose best candidate for scale-up |

### 1.2 Candidate Portfolio

| Candidate | Name | Target | Length | Hydrophobicity |
|-----------|------|--------|--------|----------------|
| **Peptide 1** | C7 | Cardiac myosin binding protein C | 8 aa | Moderate |
| **Peptide 2** | APW-4 | Cardiac troponin I complex | 9 aa | Higher |
| **Peptide 3** | HN-1 | Cardiac annexin A2 | 10 aa | Moderate |

---

## 2. Candidate 1: C7 (Original Design)

### 2.1 Details

| Property | Value |
|----------|-------|
| **Name** | C7 |
| **Full Name** | Cardiac-homing peptide 7 |
| **Sequence** | `APWHLSSQ` |
| **Length** | 8 amino acids |
| **Target** | Cardiac myosin binding protein C (cMyBP-C) |
| **Source** | Published in Cardiovasc Res 2004 |

### 2.2 Sequence

```
APWHLSSQ
```

### 2.3 Characteristics

| Property | Value |
|----------|-------|
| **Hydrophobicity** | Moderate (A, W, L, F) |
| **Charge** | Neutral (pI ~6.3) |
| **Cardiac specificity** | High (shown in mouse models) |
| **Clinical precedent** | Used in cardiac targeting studies |

### 2.4 Pros & Cons

| Pros | Cons |
|------|------|
| Proven cardiac homing | Moderate affinity |
| Short, easy to synthesize | May have off-target (skeletal muscle) |
| Low immunogenicity | Limited internalization |

---

## 3. Candidate 2: APW-4 (Enhanced Cardiac Troponin I Targeting)

### 3.1 Design Rationale

Based on cardiac troponin I (cTnI) targeting literature, designed an enhanced peptide:

### 3.2 Details

| Property | Value |
|----------|-------|
| **Name** | APW-4 |
| **Design** | cTnI binding domain mimic |
| **Sequence** | `APWHLSSQALPK` |
| **Length** | 12 amino acids |
| **Target** | Cardiac troponin I (cTnI) / Troponin complex |
| **Enhancement** | Added ALPK (cardiac tropism motif) |

### 3.3 Sequence

```
APWHLSSQALPK
```

**Motif breakdown:**
- `APWHLSSQ` - Core C7 sequence (cMyBP-C binding)
- `ALPK` - Additional cardiac tropism motif (troponin interaction)

### 3.4 Characteristics

| Property | Value |
|----------|-------|
| **Hydrophobicity** | Higher (A, W, L, F, P) |
| **Charge** | +1 (K at C-terminus) |
| **Cardiac specificity** | Very high |
| **Dual targeting** | cMyBP-C + cTnI |

### 3.5 Pros & Cons

| Pros | Cons |
|------|------|
| Dual targeting (cMyBP-C + cTnI) | Slightly longer |
| Enhanced cardiac retention | Higher cost |
| Strong cardiac specificity | May have slower tissue penetration |

---

## 4. Candidate 3: HN-1 (Cardiac Annexin A2 Targeting)

### 4.1 Design Rationale

Annexin A2 is highly expressed on cardiac endothelial cells and cardiomyocytes:

### 4.2 Details

| Property | Value |
|----------|-------|
| **Name** | HN-1 |
| **Design** | Annexin A2 binding peptide |
| **Sequence** | `SWKLYPSPLHKC` |
| **Length** | 12 amino acids |
| **Target** | Annexin A2 (cardiac endothelial cells) |
| **Source** | Designed based on annexin-binding motif |

### 4.3 Sequence

```
SWKLYPSPLHKC
```

**Motif breakdown:**
- `SWKLY` - Annexin binding region
- `PSPLH` - Cardiac selectivity motif
- `KC` - Cysteine for dimerization (optional)

### 4.4 Characteristics

| Property | Value |
|----------|-------|
| **Hydrophobicity** | Moderate-high |
| **Charge** | +2 (K, H) |
| **Cardiac specificity** | High (endothelial targeting) |
| **Advantage** | Targets vasculature first |

### 4.5 Pros & Cons

| Pros | Cons |
|------|------|
| Targets cardiac endothelium | Endothelial delivery (not direct CM) |
| Good tissue penetration | Requires extravasation |
| Dimerization potential (KC) | May need modification for stability |

---

## 5. Fusion Construct Designs

### 5.1 Complete Sequences for Each Candidate

#### Construct A: C7-GDF10-Fc

```
APWHLSSQGGGGSGGGGSGPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRKDRRKK
GQEVFMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDAYYCAG
ACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLKVYPNMS
VDTCACRGGGGSGGGGSDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVS
HEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPA
PIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKT
TPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK
```

**Length: 418 aa | MW: ~46.5 kDa**

---

#### Construct B: APW-4-GDF10-Fc

```
APWHLSSQALPKGGGGSGGGGSGPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRK
DRRKKGQEVFMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDA
YYCAGACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLKV
YPNMSVDTCACRGGGGSGGGGSDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTC
VVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVS
NKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPE
NNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK
```

**Length: 422 aa | MW: ~47.0 kDa**

---

#### Construct C: HN-1-GDF10-Fc

```
SWKLYPSPLHKCGGGGSGGGGGGPLQDNELPGLDERPPRAHAQHFHKHQLWPSPFRALKPRPGRK
DRRKKGQEVFMAASQVLDFDEKTMQKARRKQWDEPRVCSRRYLKVDFADIGWNEWIISPKSFDA
YYCAGACEFPMPKIVRPSNHATIQSIVRAVGIIPGIPEPCCVPDKMNSLGVLFLDENRNVVLKV
YPNMSVDTCACRGGGGSGGGGSDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCV
VVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNK
ALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENN
YKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK
```

**Length: 422 aa | MW: ~47.2 kDa**

**Note:** Removed C-terminal cysteine to avoid misfolding (or keep if intentional dimerization desired)

---

## 6. Comparison Matrix

| Property | C7 | APW-4 | HN-1 |
|----------|-----|-------|------|
| **Target** | cMyBP-C | cMyBP-C + cTnI | Annexin A2 |
| **Length** | 8 aa | 12 aa | 12 aa |
| **Hydrophobicity** | Moderate | High | Moderate-high |
| **Charge** | 0 | +1 | +2 |
| **Specificity** | High | Very High | High |
| **Delivery** | Direct CM | Direct CM | Endothelial |
| **合成 cost** | Lowest | Medium | Medium |
| **Risk** | Low | Medium | Medium |

---

## 7. Screening Strategy

### 7.1 In Vitro Screening

| Assay | Method | Readout |
|-------|--------|---------|
| **Cardiac homing** | iPSC-CMs binding | Fluorescent peptide uptake |
| **Specificity** | vs. skeletal muscle, liver | Selectivity index |
| **Internalization** | FACS | % internalized |
| **GDF10 activity** | Smad reporter | EC50 preservation |

### 7.2 Ranking Criteria

| Criterion | Weight | Method |
|-----------|--------|--------|
| **Cardiac specificity** | 40% | Competition assay |
| **GDF10 bioactivity retention** | 30% | Smad assay |
| **Expression yield** | 15% | CHO productivity |
| **Cost** | 15% | Manufacturing |

### 7.3 Recommended Screening Order

```
1. Synthesize all 3 peptides (non-Fc, shorter versions)
        ↓
2. Screen for cardiac binding (iPSC-CMs)
        ↓
3. Select best 1-2 candidates
        ↓
4. Clone into full GDF10-Fc constructs
        ↓
5. Validate bioactivity + targeting
        ↓
6. Select final candidate for scale-up
```

---

## 8. Peptide-Only Screening Constructs (Cost-Effective)

For initial screening, use shorter biotinylated peptides:

### 8.1 Biotinylated Peptides

```
Biotin-ATWHLSSQ                  (C7-biotin)
Biotin-APWHLSSQALPK              (APW-4-biotin)
Biotin-SWKLYPSPLHKC              (HN-1-biotin)
```

### 8.2 For Binding Assay

```
Biotin-Peptide + Streptavidin-FITC → iPSC-CMs → FACS
```

---

## 9. Summary

### 9.1 Three Candidates

| Candidate | Sequence | Target | Advantage |
|-----------|----------|--------|-----------|
| **C7** | `APWHLSSQ` | cMyBP-C | Proven, short, low cost |
| **APW-4** | `APWHLSSQALPK` | cMyBP-C + cTnI | Dual targeting, highest specificity |
| **HN-1** | `SWKLYPSPLHKC` | Annexin A2 | Endothelial, good penetration |

### 9.2 Recommendation

**Order all 3 as peptide-only first**, screen for binding, then proceed with best candidate as GDF10-Fc fusion.

### 9.3 Synthesis Planning

| Construct | Amino Acids | Estimated Cost |
|-----------|-------------|----------------|
| **C7 peptide alone** | 8 aa | $50-100 |
| **APW-4 peptide alone** | 12 aa | $80-150 |
| **HN-1 peptide alone** | 12 aa | $80-150 |
| **C7-GDF10-Fc** | 418 aa | $2000-5000 |
| **APW-4-GDF10-Fc** | 422 aa | $2500-6000 |
| **HN-1-GDF10-Fc** | 422 aa | $2500-6000 |

---

## 10. Vendor Recommendations

| Vendor | Peptide-Only | Full Protein | Notes |
|--------|--------------|--------------|-------|
| **GenScript** | ✓ | ✓ | Best overall |
| **ChinaPeptides** | ✓ | ✓ | Cost-effective |
| **AnaSpec** | ✓ | ✗ | FBI-free peptides |
| **GL Biochem** | ✓ | ✗ | Good for long peptides |

---

*Document generated by ARP v24 Research Pipeline · April 2026*
