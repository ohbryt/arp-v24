"""
ARP v24 - Antimicrobial Peptide (AMP) Integration

Based on: Zhou et al. 2026 - "Artificial intelligence drives the identification 
and screening of novel antibiotics and antimicrobial peptides"
Brief Bioinform. 2026

Integration:
1. AI-discovered antibiotics (Halicin, Abaucin)
2. Attentive Fingerprint methodology
3. AlphaFold2 structure-based screening
4. Federated learning for multi-site collaboration
"""

# ============================================================================
# ANTIMICROBIAL COMPOUNDS DATABASE
# ============================================================================
# From Zhou et al. 2026 - AI-driven antibiotic discovery

ANTIMICROBIAL_COMPOUNDS = {
    # Target: DNA Gyrase (Halicin)
    "DNA_GYRASE": [
        {
            "name": "Halicin",
            "stage": "preclinical",
            "smiles": "CC1=NN=C(CN1C(=O)C2=C(C(=CC=C2)Cl)[N+](=O)[O-])/C=C/C3=CC=C(C=C3)[N+](=O)[O-]",
            "mechanism": "AI-discovered",
            "note": "Originally discovered by AI for C. difficile",
            "activity": "IC50: 0.1-1 µM",
            "source": "Zhou et al. 2026"
        },
    ],
    # Target: RNA Polymerase (Abaucin)
    "RNA_POL": [
        {
            "name": "Abaucin",
            "stage": "preclinical", 
            "mechanism": "AI-discovered",
            "note": "Narrow-spectrum for A. baumannii",
            "activity": "MIC: 0.5-2 µg/mL",
            "source": "Zhou et al. 2026"
        },
    ],
    # AI-Screened compounds
    "UNKNOWN_TARGET": [
        {
            "name": "ZINC01318774",
            "stage": "preclinical",
            "mechanism": "AI-screened",
            "note": "Active against A. baumannii",
            "source": "Zhou et al. 2026"
        },
    ],
    # AI-Designed novel molecules (Attentive Fingerprint)
    "AI_DESIGNED": [
        {
            "name": "AI-AMP-01",
            "stage": "discovery",
            "mechanism": "AttentiveFingerprint-generated",
            "note": "Novel AMP from generative AI",
            "source": "Zhou et al. 2026"
        },
        {
            "name": "AI-AMP-02",
            "stage": "discovery",
            "mechanism": "AttentiveFingerprint-generated"
        },
        {
            "name": "AI-AMP-03",
            "stage": "discovery", 
            "mechanism": "AttentiveFingerprint-generated"
        },
    ],
}


# ============================================================================
# ENDOGENOUS AMPS (Human)
# ============================================================================

HUMAN_AMPS = {
    "LL37": {
        "name": "LL37 (Cathelicidin)",
        "sequence": "LLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES",
        "stage": "clinical",
        "mechanism": "membrane-disrupting AMP",
        "indications": ["cathelicidin deficiency", "infected wounds"],
        "source": "endogenous"
    },
    "HNP1": {
        "name": "Alpha-defensin HNP1",
        "sequence": "ACTCYCRETGTAICFSYGIPAKIKTGGTCIYQGRLLAFAC",
        "stage": "clinical",
        "mechanism": "neutrophil defensin",
        "source": "endogenous"
    },
}


# ============================================================================
# AI METHODS FROM THE PAPER
# ============================================================================

AI_METHODS = {
    "Attentive_Fingerprint": {
        "description": "Graph neural network with attention mechanism",
        "input": "Molecular graph (atoms=nodes, bonds=edges)",
        "output": "Antimicrobial activity prediction",
        "implementation": "Message passing + attention weighting",
        "papers": ["Zhou et al. 2026"]
    },
    "AlphaFold2_Screening": {
        "description": "Structure-based virtual screening",
        "steps": ["Protein structure prediction", "Active site prediction", "Molecular docking", "Biological screening"],
        "use": "Target validation and binding affinity"
    },
    "Chemprop_Federated": {
        "description": "Federated learning for multi-site collaboration",
        "features": ["Local MIC standardization", "Batch correction", "Cross-site harmonization"],
        "model": "Chemprop with federated averaging"
    }
}


# ============================================================================
# SCREENING PIPELINE
# ============================================================================

def get_antimicrobial_candidates(target=None):
    """
    Get antimicrobial candidates, optionally filtered by target.
    
    Args:
        target: Optional target filter (DNA_GYRASE, RNA_POL, etc.)
    
    Returns:
        List of candidate dictionaries
    """
    results = []
    
    for t, compounds in ANTIMICROBIAL_COMPOUNDS.items():
        if target is None or t == target:
            for c in compounds:
                c_copy = c.copy()
                c_copy["target"] = t
                results.append(c_copy)
    
    # Add human AMPs
    if target is None or target == "HUMAN_AMP":
        for name, info in HUMAN_AMPS.items():
            results.append({
                "name": info["name"],
                "stage": info["stage"],
                "mechanism": info["mechanism"],
                "target": "HUMAN_AMP",
                "source": "endogenous"
            })
    
    return results


def print_antimicrobial_report():
    """Print a formatted report of all antimicrobial candidates"""
    
    print("="*70)
    print("ANTIMICROBIAL CANDIDATES - Based on Zhou et al. 2026")
    print("="*70)
    print()
    
    print("## AI-DISCOVERED ANTIBIOTICS")
    print("-"*70)
    for target, compounds in ANTIMICROBIAL_COMPOUNDS.items():
        print(f"\nTarget: {target}")
        for c in compounds:
            print(f"  • {c['name']} ({c['stage']})")
            print(f"    Mechanism: {c.get('mechanism', 'N/A')}")
            if c.get('note'):
                print(f"    Note: {c['note']}")
    
    print()
    print("## HUMAN ENDOGENOUS AMPS")
    print("-"*70)
    for name, info in HUMAN_AMPS.items():
        print(f"\n  • {info['name']}")
        print(f"    Sequence: {info['sequence'][:40]}...")
        print(f"    Mechanism: {info['mechanism']}")
    
    print()
    print("## AI METHODS (from the paper)")
    print("-"*70)
    for method, info in AI_METHODS.items():
        print(f"\n  • {method}")
        print(f"    {info['description']}")
    
    print()
    print("="*70)


if __name__ == "__main__":
    print_antimicrobial_report()
