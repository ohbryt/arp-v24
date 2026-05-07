"""
RDKit Chemical Validator
=========================
Validates molecules for drug-likeness using RDKit.
Checks: SMILES canonicalization, MW, LogP, HBA, HBD, TPSA, PAINS/Brenk filters, stereochemistry.

Based on MolViBench insights:
  - Chemical correctness is the bottleneck, not executability
  - MW 150-800, LogP -1 to 6, HBA 1-10, HBD 0-6, TPSA 40-200 are drug-likeness bounds
"""

from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, QED, AllChem
from rdkit.Chem.FilterCatalog import FilterCatalogParams, FilterCatalog
import warnings
from typing import NamedTuple


# ============================================================
# Constants (drug-likeness bounds from Lipinski + literature)
# ============================================================

MW_BOUNDS       = (150.0, 800.0)      # g/mol
LOGP_BOUNDS     = (-1.0, 6.0)
HBA_BOUNDS      = (1, 10)
HBD_BOUNDS      = (0, 6)
TPSA_BOUNDS     = (40.0, 200.0)
ROTBOND_BOUNDS  = (0, 10)
N_HETEROATOMS   = (1, 20)
N_RINGS         = (1, 8)
N_AROMATIC_RINGS = (0, 7)

# PAINS alerts: Level A/B/C
# Brenk filter: more stringent for reactive groups


# ============================================================
# Result types
# ============================================================

class ValidationResult(NamedTuple):
    valid: bool
    smiles: str           # canonical SMILES
    molecule: object      # RDKit mol object (or None)
    reason: str           # Human-readable reason
    properties: dict      # All computed properties
    pains_alerts: list    # List of PAINS alert names
    brenk_alerts: list    # List of Brenk filter alert names
    issues: list          # List of (property, value, expected) tuples


# ============================================================
# Core validator
# ============================================================

def validate_smiles(smiles: str, strict: bool = True) -> ValidationResult:
    """
    Validate a SMILES string and compute molecular properties.

    Parameters
    ----------
    smiles : str
        Input SMILES string (non-canonical OK).
    strict : bool
        If True, apply Lipinski drug-likeness filters (MW, LogP, HBA, HBD, TPSA).
        If False, only check parseability.

    Returns
    -------
    ValidationResult
    """
    issues = []
    pains_alerts = []
    brenk_alerts = []

    if not smiles or not isinstance(smiles, str):
        return ValidationResult(
            valid=False, smiles="", molecule=None,
            reason="Empty or invalid input",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )

    # --- Parse SMILES ---
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return ValidationResult(
            valid=False, smiles=smiles, molecule=None,
            reason="SMILES could not be parsed",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )

    # --- Canonicalize ---
    try:
        canonical = Chem.MolToSmiles(mol)
        # Re-parse canonical to ensure validity
        mol = Chem.MolFromSmiles(canonical)
        if mol is None:
            return ValidationResult(
                valid=False, smiles=smiles, molecule=None,
                reason="Canonical SMILES re-parse failed",
                properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
            )
    except Exception as e:
        return ValidationResult(
            valid=False, smiles=smiles, molecule=None,
            reason=f"Canonicalization error: {e}",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )

    # --- Compute properties ---
    try:
        mw       = Descriptors.MolWt(mol)
        logp     = Descriptors.MolLogP(mol)
        num_hba  = Lipinski.NumHAcceptors(mol)
        num_hbd  = Lipinski.NumHDonors(mol)
        tpsa     = Descriptors.TPSA(mol)
        num_rot  = Lipinski.NumRotatableBonds(mol)
        num_het  = Descriptors.NumHeteroatoms(mol)
        num_rings = Descriptors.RingCount(mol)
        num_aromatic = Descriptors.NumAromaticRings(mol)
        qed_score = QED.qed(mol)
    except Exception as e:
        return ValidationResult(
            valid=False, smiles=canonical, molecule=mol,
            reason=f"Property calculation error: {e}",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )

    properties = {
        "mw": round(mw, 3),
        "logp": round(logp, 3),
        "hba": num_hba,
        "hbd": num_hbd,
        "tpsa": round(tpsa, 3),
        "rotbonds": num_rot,
        "n_heteroatoms": num_het,
        "n_rings": num_rings,
        "n_aromatic_rings": num_aromatic,
        "qed": round(qed_score, 4),
    }

    # --- Check stereochemistry ---
    has_stereo = len(Chem.FindMolChiralCenters(mol)) > 0
    properties["has_stereo"] = has_stereo

    # --- Check aromatic nitro (common false positive alert) ---
    aromatic_nitro = _has_aromatic_nitro(mol)
    properties["aromatic_nitro"] = aromatic_nitro

    # --- Strict mode: Lipinski drug-likeness ---
    if strict:
        issues = []

        if not (MW_BOUNDS[0] <= mw <= MW_BOUNDS[1]):
            issues.append(("MW", round(mw, 2), f"{MW_BOUNDS[0]}-{MW_BOUNDS[1]}"))
        if not (LOGP_BOUNDS[0] <= logp <= LOGP_BOUNDS[1]):
            issues.append(("LogP", round(logp, 2), f"{LOGP_BOUNDS[0]}-{LOGP_BOUNDS[1]}"))
        if not (HBA_BOUNDS[0] <= num_hba <= HBA_BOUNDS[1]):
            issues.append(("HBA", num_hba, f"{HBA_BOUNDS[0]}-{HBA_BOUNDS[1]}"))
        if not (HBD_BOUNDS[0] <= num_hbd <= HBD_BOUNDS[1]):
            issues.append(("HBD", num_hbd, f"{HBD_BOUNDS[0]}-{HBD_BOUNDS[1]}"))
        if not (TPSA_BOUNDS[0] <= tpsa <= TPSA_BOUNDS[1]):
            issues.append(("TPSA", round(tpsa, 2), f"{TPSA_BOUNDS[0]}-{TPSA_BOUNDS[1]}"))
        if not (ROTBOND_BOUNDS[0] <= num_rot <= ROTBOND_BOUNDS[1]):
            issues.append(("RotBonds", num_rot, f"{ROTBOND_BOUNDS[0]}-{ROTBOND_BOUNDS[1]}"))

        # PAINS filter (use catalog)
        try:
            catalog_params = FilterCatalogParams()
            catalog_params.AddFilter(FilterCatalogParams.FilterCatalogs.PAINS)
            catalog = FilterCatalog(catalog_params)
            matches = catalog.GetMatches(mol)
            pains_alerts = [str(m.GetDescription()) for m in matches]
        except Exception:
            pains_alerts = []

        # Brenk filter (more stringent reactive groups)
        try:
            brenk_params = FilterCatalogParams()
            brenk_params.AddFilter(FilterCatalogParams.FilterCatalogs.Brenk)
            brenk_catalog = FilterCatalog(brenk_params)
            brenk_matches = brenk_catalog.GetMatches(mol)
            brenk_alerts = [str(m.GetDescription()) for m in brenk_matches]
        except Exception:
            brenk_alerts = []

    # --- Determine validity ---
    if strict and issues:
        reason = f"Lipinski violations: {', '.join(f'{i[0]}={i[1]}(exp:{i[2]})' for i in issues)}"
        return ValidationResult(
            valid=False, smiles=canonical, molecule=mol,
            reason=reason, properties=properties,
            pains_alerts=pains_alerts, brenk_alerts=brenk_alerts, issues=issues
        )

    if strict and pains_alerts:
        reason = f"PAINS alerts: {', '.join(pains_alerts[:3])}"
        return ValidationResult(
            valid=False, smiles=canonical, molecule=mol,
            reason=reason, properties=properties,
            pains_alerts=pains_alerts, brenk_alerts=brenk_alerts, issues=issues
        )

    if strict and brenk_alerts:
        reason = f"Brenk alerts: {', '.join(brenk_alerts[:3])}"
        return ValidationResult(
            valid=False, smiles=canonical, molecule=mol,
            reason=reason, properties=properties,
            pains_alerts=pains_alerts, brenk_alerts=brenk_alerts, issues=issues
        )

    reason = "Valid" if not issues else f"Passed with notes: {', '.join(i[0] for i in issues)}"
    return ValidationResult(
        valid=True, smiles=canonical, molecule=mol,
        reason=reason, properties=properties,
        pains_alerts=pains_alerts, brenk_alerts=brenk_alerts, issues=issues
    )


def validate_mol(mol) -> ValidationResult:
    """
    Validate an RDKit mol object.
    Returns canonical SMILES and all properties.
    """
    if mol is None:
        return ValidationResult(
            valid=False, smiles="", molecule=None,
            reason="None molecule",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )
    try:
        canonical = Chem.MolToSmiles(mol)
        return validate_smiles(canonical, strict=True)
    except Exception as e:
        return ValidationResult(
            valid=False, smiles="", molecule=mol,
            reason=f"Error: {e}",
            properties={}, pains_alerts=[], brenk_alerts=[], issues=[]
        )


# ============================================================
# Utility helpers
# ============================================================

def _has_aromatic_nitro(mol) -> bool:
    """Check for aromatic nitro groups (potential false positive PAINS)."""
    try:
        nitro_pattern = Chem.MolFromSmarts("[N+](=O)c1ccccc1")
        return mol.HasSubstructMatch(nitro_pattern)
    except Exception:
        return False


def canonicalize_smiles(smiles: str) -> str:
    """Convert any SMILES to canonical form. Returns empty string if invalid."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return ""
        return Chem.MolToSmiles(mol)
    except Exception:
        return ""


def get_property_summary(mol) -> dict:
    """Return a one-line summary dict of molecular properties."""
    if mol is None:
        return {}
    return {
        "mw":    round(Descriptors.MolWt(mol), 2),
        "logp":  round(Descriptors.MolLogP(mol), 2),
        "hba":   Lipinski.NumHAcceptors(mol),
        "hbd":   Lipinski.NumHDonors(mol),
        "tpsa":  round(Descriptors.TPSA(mol), 2),
        "qed":   round(QED.qed(mol), 4),
    }


def batch_validate(smiles_list: list[str], strict: bool = True) -> list[ValidationResult]:
    """Validate a list of SMILES strings."""
    return [validate_smiles(s, strict=strict) for s in smiles_list]


def filter_valid(smiles_list: list[str], strict: bool = True) -> list[str]:
    """Return only the valid canonical SMILES from a list."""
    results = batch_validate(smiles_list, strict=strict)
    return [r.smiles for r in results if r.valid and r.smiles]
