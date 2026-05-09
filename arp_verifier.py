#!/usr/bin/env python3
"""
ARP Verifier System: Drug Discovery Quality Gates
===================================================
Based on Harness Verifier Design: taste → rubric → measurement

Framework:
- 80% quantitative signals (mechanical)
- 20% taste residue (human gate)
- Hierarchical: working verifier (fast) → final verifier (thorough)

Usage:
    from arp_verifier import ARPVerifier
    verifier = ARPVerifier()
    result = verifier.verify_compound(smiles="CCO", name="Ethanol")
    result = verifier.verify_target(uniprot_id="Q9Y2D6")
    result = verifier.verify_literature(pmid="35641621")
"""

from dataclasses import dataclass, field
from typing import Optional
import re

# ============================================================
# RESULT TYPES
# ============================================================
@dataclass
class VerifierSignal:
    """Single verification signal"""
    name: str
    value: any
    threshold: str
    passed: bool
    method: str  # quantitative, persona-llm, human
    details: str = ""

@dataclass
class VerifierResult:
    """Overall verification result"""
    passed: bool
    score: float  # 0-1
    signals: list[VerifierSignal] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    
    def summary(self) -> str:
        passed_count = sum(1 for s in self.signals if s.passed)
        total_count = len(self.signals)
        return f"{passed_count}/{total_count} signals passed (score: {self.score:.2f})"

# ============================================================
# SMILES VALIDITY VERIFIERS
# ============================================================
class SMILESVerifier:
    """Verify SMILES string validity and drug-likeness"""
    
    @staticmethod
    def is_valid_smiles(smiles: str) -> VerifierSignal:
        """Quantitative: RDKit SMILES sanitization"""
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            return VerifierSignal(
                name="smiles_validity",
                value="Valid",
                threshold="Must parse without error",
                passed=mol is not None,
                method="quantitative",
                details="RDKit MolFromSmiles" if mol else "Failed to parse"
            )
        except ImportError:
            # Fallback: basic syntax check
            valid_chars = set("BCNOPSFIHcnops[]()=#-+\\/@%{}")
            has_atom = any(c.isalpha() for c in smiles)
            passed = has_atom and all(c in valid_chars or c.isspace() for c in smiles)
            return VerifierSignal(
                name="smiles_validity",
                value="Valid (fallback)" if passed else "Invalid",
                threshold="Basic syntax check",
                passed=passed,
                method="quantitative",
                details="RDKit not available - basic syntax only"
            )

    @staticmethod
    def molecular_weight(smiles: str) -> VerifierSignal:
        """Quantitative: MW 150-800 Da (drug-like)"""
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                mw = Chem.Descriptors.MolWt(mol)
                passed = 150 <= mw <= 800
                return VerifierSignal(
                    name="molecular_weight",
                    value=f"{mw:.1f} Da",
                    threshold="150-800 Da",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'OUT OF RANGE'}"
                )
        except:
            pass
        return VerifierSignal(
            name="molecular_weight",
            value="N/A",
            threshold="150-800 Da",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

    @staticmethod
    def logp(smiles: str) -> VerifierSignal:
        """Quantitative: XLogP3 -2 to 10"""
        try:
            from rdkit import Chem
            from rdkit.Chem import Crippen
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                logp = Crippen.MolLogP(mol)
                passed = -2 <= logp <= 10
                return VerifierSignal(
                    name="logp",
                    value=f"{logp:.2f}",
                    threshold="-2 to 10",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'OUT OF RANGE'}"
                )
        except:
            pass
        return VerifierSignal(
            name="logp",
            value="N/A",
            threshold="-2 to 10",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

    @staticmethod
    def tpsa(smiles: str) -> VerifierSignal:
        """Quantitative: TPSA 20-200 Å² (oral bioavailability)"""
        try:
            from rdkit import Chem
            from rdkit.Chem import Descriptors
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                tpsa = Descriptors.TPSA(mol)
                passed = 20 <= tpsa <= 200
                return VerifierSignal(
                    name="tpsa",
                    value=f"{tpsa:.1f} Å²",
                    threshold="20-200 Å²",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'OUT OF RANGE'}"
                )
        except:
            pass
        return VerifierSignal(
            name="tpsa",
            value="N/A",
            threshold="20-200 Å²",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

    @staticmethod
    def hba_hbd(smiles: str) -> VerifierSignal:
        """Quantitative: HBA ≤5, HBD ≤3 (Lipinski's rule)"""
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                hba = Chem.Lipinski.NumHAcceptors(mol)
                hbd = Chem.Lipinski.NumHDonors(mol)
                passed = hba <= 5 and hbd <= 3
                return VerifierSignal(
                    name="hba_hbd",
                    value=f"HBA={hba}, HBD={hbd}",
                    threshold="HBA≤5, HBD≤3",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'FAIL'} (HBA={hba}, HBD={hbd})"
                )
        except:
            pass
        return VerifierSignal(
            name="hba_hbd",
            value="N/A",
            threshold="HBA≤5, HBD≤3",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

    @staticmethod
    def rotatable_bonds(smiles: str) -> VerifierSignal:
        """Quantitative: ≤10 rotatable bonds (oral bioavailability)"""
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                rb = Chem.Lipinski.NumRotatableBonds(mol)
                passed = rb <= 10
                return VerifierSignal(
                    name="rotatable_bonds",
                    value=str(rb),
                    threshold="≤10",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'HIGH (may affect oral bioavailability)'}"
                )
        except:
            pass
        return VerifierSignal(
            name="rotatable_bonds",
            value="N/A",
            threshold="≤10",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

    @staticmethod
    def ring_count(smiles: str) -> VerifierSignal:
        """Quantitative: ≥1 ring (drug-like scaffold)"""
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                rings = Chem.Lipinski.RingCount(mol)
                passed = rings >= 1
                return VerifierSignal(
                    name="ring_count",
                    value=str(rings),
                    threshold="≥1",
                    passed=passed,
                    method="quantitative",
                    details=f"{'OK' if passed else 'No rings - may be too flexible'}"
                )
        except:
            pass
        return VerifierSignal(
            name="ring_count",
            value="N/A",
            threshold="≥1",
            passed=False,
            method="quantitative",
            details="Could not calculate"
        )

# ============================================================
# TARGET VERIFIERS
# ============================================================
class TargetVerifier:
    """Verify target (protein) information validity"""
    
    UNIPROT_PATTERN = re.compile(r'^[A-NR-Z][0-9][A-Z0-9]{2}[0-9]$|^[A-NR-Z][0-9]{2}[A-Z0-9]{3}[0-9]$|^[OPQ][0-9][A-Z0-9]{3}[0-9]$')
    
    @staticmethod
    def uniprot_id(uniprot_id: str) -> VerifierSignal:
        """Quantitative: UniProt ID format validation"""
        if not uniprot_id:
            return VerifierSignal(
                name="uniprot_id_format",
                value="",
                threshold="6 or 10 characters (e.g., Q9Y2D6)",
                passed=False,
                method="quantitative",
                details="Empty value"
            )
        
        # Remove version suffix (e.g., Q9Y2D6.1 → Q9Y2D6)
        clean_id = uniprot_id.split('.')[0]
        passed = bool(TargetVerifier.UNIPROT_PATTERN.match(clean_id))
        
        return VerifierSignal(
            name="uniprot_id_format",
            value=uniprot_id,
            threshold="UniProt format (e.g., Q9Y2D6)",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid format'}"
        )

    @staticmethod
    def gene_name(gene_name: str) -> VerifierSignal:
        """Quantitative: Gene name format (1-10 uppercase letters)"""
        if not gene_name:
            return VerifierSignal(
                name="gene_name_format",
                value="",
                threshold="1-10 uppercase letters (e.g., DGAT1)",
                passed=False,
                method="quantitative",
                details="Empty value"
            )
        
        pattern = re.compile(r'^[A-Z][A-Z0-9]{0,9}$')
        passed = bool(pattern.match(gene_name))
        
        return VerifierSignal(
            name="gene_name_format",
            value=gene_name,
            threshold="Gene name format",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid format'}"
        )

    @staticmethod
    def protein_length(length: int) -> VerifierSignal:
        """Quantitative: Protein length 50-5000 AA"""
        if not length:
            return VerifierSignal(
                name="protein_length",
                value="N/A",
                threshold="50-5000 AA",
                passed=False,
                method="quantitative",
                details="No length provided"
            )
        
        passed = 50 <= length <= 5000
        
        return VerifierSignal(
            name="protein_length",
            value=f"{length} AA",
            threshold="50-5000 AA",
            passed=passed,
            method="quantitative",
            details=f"{'OK' if passed else 'OUT OF RANGE'}"
        )

# ============================================================
# PDB VERIFIERS
# ============================================================
class PDBVerifier:
    """Verify PDB structure information"""
    
    PDB_PATTERN = re.compile(r'^[0-9][A-Za-z0-9]{3}$')
    
    @staticmethod
    def pdb_id(pdb_id: str) -> VerifierSignal:
        """Quantitative: PDB ID format (4 characters, first digit)"""
        if not pdb_id:
            return VerifierSignal(
                name="pdb_id_format",
                value="",
                threshold="4 characters (e.g., 7K4G)",
                passed=False,
                method="quantitative",
                details="Empty value"
            )
        
        pdb_id = pdb_id.lower()
        passed = bool(PDBVerifier.PDB_PATTERN.match(pdb_id))
        
        return VerifierSignal(
            name="pdb_id_format",
            value=pdb_id.upper(),
            threshold="4 characters (first is digit)",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid format'}"
        )

    @staticmethod
    def resolution(resolution: float) -> VerifierSignal:
        """Quantitative: X-ray resolution ≤3.0 Å (good quality)"""
        if resolution is None:
            return VerifierSignal(
                name="resolution",
                value="N/A",
                threshold="≤3.0 Å (high quality)",
                passed=False,
                method="quantitative",
                details="No resolution provided"
            )
        
        passed = resolution <= 3.0
        
        return VerifierSignal(
            name="resolution",
            value=f"{resolution:.2f} Å",
            threshold="≤3.0 Å",
            passed=passed,
            method="quantitative",
            details=f"{'High quality' if passed else 'Low resolution (may affect docking)'}"
        )

# ============================================================
# LITERATURE VERIFIERS
# ============================================================
class LiteratureVerifier:
    """Verify literature citation validity"""
    
    PMID_PATTERN = re.compile(r'^\d{6,10}$')
    DOI_PATTERN = re.compile(r'^(10\.\d{4,}/\S+)$')
    
    @staticmethod
    def pmid(pmid: str) -> VerifierSignal:
        """Quantitative: PMID format (6-10 digits)"""
        if not pmid:
            return VerifierSignal(
                name="pmid_format",
                value="",
                threshold="6-10 digits (e.g., 35641621)",
                passed=False,
                method="quantitative",
                details="Empty value"
            )
        
        # Remove any prefix
        pmid_clean = re.sub(r'^(PMID:?|pmid:)\s*', '', pmid.strip(), flags=re.IGNORECASE)
        passed = bool(LiteratureVerifier.PMID_PATTERN.match(pmid_clean))
        
        return VerifierSignal(
            name="pmid_format",
            value=pmid,
            threshold="6-10 digits",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid format'}"
        )

    @staticmethod
    def doi(doi: str) -> VerifierSignal:
        """Quantitative: DOI format (10.xxxx/...)"""
        if not doi:
            return VerifierSignal(
                name="doi_format",
                value="",
                threshold="10.xxxx/... (e.g., 10.1021/acs.jmedchem.2c00474)",
                passed=False,
                method="quantitative",
                details="Empty value"
            )
        
        passed = bool(LiteratureVerifier.DOI_PATTERN.match(doi.strip()))
        
        return VerifierSignal(
            name="doi_format",
            value=doi,
            threshold="DOI format",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid format'}"
        )

    @staticmethod
    def year_range(year: int) -> VerifierSignal:
        """Quantitative: Publication year 1990-current+1"""
        if not year:
            return VerifierSignal(
                name="publication_year",
                value="N/A",
                threshold="1990-2027",
                passed=False,
                method="quantitative",
                details="No year provided"
            )
        
        passed = 1990 <= year <= 2027
        
        return VerifierSignal(
            name="publication_year",
            value=str(year),
            threshold="1990-2027",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Out of range'}"
        )

# ============================================================
# IC50 VERIFIERS
# ============================================================
class ActivityVerifier:
    """Verify biological activity data (IC50, Ki, etc.)"""
    
    @staticmethod
    def ic50_nm(ic50: float) -> VerifierSignal:
        """Quantitative: IC50 0.001 nM to 100 μM (valid drug-like range)"""
        if ic50 is None:
            return VerifierSignal(
                name="ic50_range",
                value="N/A",
                threshold="0.001 nM - 100,000 nM (100 μM)",
                passed=False,
                method="quantitative",
                details="No IC50 provided"
            )
        
        passed = 0.001 <= ic50 <= 100000
        
        return VerifierSignal(
            name="ic50_range",
            value=f"{ic50:.3f} nM",
            threshold="0.001 nM - 100 μM",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'OUT OF RANGE'}"
        )

    @staticmethod
    def ic50_unit(unit: str) -> VerifierSignal:
        """Quantitative: IC50 unit validation"""
        valid_units = {'nM', 'μM', 'uM', 'mM', 'pM', 'nM'}
        if not unit:
            return VerifierSignal(
                name="ic50_unit",
                value="N/A",
                threshold="nM, μM, mM, pM",
                passed=False,
                method="quantitative",
                details="No unit provided"
            )
        
        # Normalize
        unit_clean = unit.strip().replace(' ', '').replace('u', 'μ')
        passed = unit_clean in valid_units
        
        return VerifierSignal(
            name="ic50_unit",
            value=unit,
            threshold="nM, μM, mM, pM",
            passed=passed,
            method="quantitative",
            details=f"{'Valid' if passed else 'Invalid unit'}"
        )

# ============================================================
# MAIN VERIFIER CLASS
# ============================================================
class ARPVerifier:
    """
    Drug Discovery Verifier System
    
    Design based on Harness Verifier principles:
    - Quantitative signals first (80%)
    - Persona-LLM for nuanced checks (15%)
    - Human gate for taste residue (5%)
    """
    
    def __init__(self):
        self.smiles_verifier = SMILESVerifier()
        self.target_verifier = TargetVerifier()
        self.pdb_verifier = PDBVerifier()
        self.literature_verifier = LiteratureVerifier()
        self.activity_verifier = ActivityVerifier()
    
    def verify_compound(self, smiles: str, name: str = "") -> VerifierResult:
        """
        Full compound verification (working verifier)
        
        Returns VerifierResult with signals:
        - SMILES validity
        - Molecular weight
        - LogP
        - TPSA
        - HBA/HBD
        - Rotatable bonds
        - Ring count
        """
        signals = []
        errors = []
        warnings = []
        
        # 1. SMILES validity (critical - fail fast)
        val_signal = self.smiles_verifier.is_valid_smiles(smiles)
        signals.append(val_signal)
        if not val_signal.passed:
            errors.append(f"Invalid SMILES: {smiles}")
            return VerifierResult(passed=False, score=0.0, signals=signals, errors=errors)
        
        # 2-7. Drug-likeness checks
        signals.append(self.smiles_verifier.molecular_weight(smiles))
        signals.append(self.smiles_verifier.logp(smiles))
        signals.append(self.smiles_verifier.tpsa(smiles))
        signals.append(self.smiles_verifier.hba_hbd(smiles))
        signals.append(self.smiles_verifier.rotatable_bonds(smiles))
        signals.append(self.smiles_verifier.ring_count(smiles))
        
        # Calculate score
        passed_count = sum(1 for s in signals if s.passed)
        total_count = len(signals)
        score = passed_count / total_count if total_count > 0 else 0.0
        
        # Warnings for borderline values
        mw_signal = signals[1]  # molecular_weight
        if mw_signal.passed and mw_signal.value:
            try:
                mw_val = float(mw_signal.value.replace(" Da", ""))
                if mw_val > 600:
                    warnings.append(f"MW {mw_val:.0f} is high (>600 Da) - may affect oral bioavailability")
            except:
                pass
        
        return VerifierResult(
            passed=score >= 0.7,  # 70% threshold for working verifier
            score=score,
            signals=signals,
            warnings=warnings,
            errors=errors
        )
    
    def verify_target(self, uniprot_id: str = "", gene_name: str = "", 
                      protein_length: int = None) -> VerifierResult:
        """
        Target verification (working verifier)
        
        Returns VerifierResult with signals:
        - UniProt ID format
        - Gene name format
        - Protein length
        """
        signals = []
        errors = []
        
        if uniprot_id:
            signals.append(self.target_verifier.uniprot_id(uniprot_id))
            if not signals[-1].passed:
                errors.append(f"Invalid UniProt ID: {uniprot_id}")
        
        if gene_name:
            signals.append(self.target_verifier.gene_name(gene_name))
            if not signals[-1].passed:
                errors.append(f"Invalid gene name: {gene_name}")
        
        if protein_length:
            signals.append(self.target_verifier.protein_length(protein_length))
        
        passed_count = sum(1 for s in signals if s.passed)
        total_count = len(signals)
        score = passed_count / total_count if total_count > 0 else 0.0
        
        return VerifierResult(
            passed=score >= 0.5 if signals else False,  # At least ID or gene name
            score=score,
            signals=signals,
            warnings=[],
            errors=errors
        )
    
    def verify_pdb_structure(self, pdb_id: str, resolution: float = None) -> VerifierResult:
        """
        PDB structure verification (working verifier)
        """
        signals = []
        errors = []
        
        signals.append(self.pdb_verifier.pdb_id(pdb_id))
        if not signals[-1].passed:
            errors.append(f"Invalid PDB ID: {pdb_id}")
        
        if resolution is not None:
            signals.append(self.pdb_verifier.resolution(resolution))
        
        passed_count = sum(1 for s in signals if s.passed)
        total_count = len(signals)
        score = passed_count / total_count if total_count > 0 else 0.0
        
        return VerifierResult(
            passed=score >= 0.5,
            score=score,
            signals=signals,
            warnings=[],
            errors=errors
        )
    
    def verify_literature(self, pmid: str = "", doi: str = "", 
                          year: int = None) -> VerifierResult:
        """
        Literature citation verification (working verifier)
        """
        signals = []
        errors = []
        
        if pmid:
            signals.append(self.literature_verifier.pmid(pmid))
            if not signals[-1].passed:
                errors.append(f"Invalid PMID: {pmid}")
        
        if doi:
            signals.append(self.literature_verifier.doi(doi))
            if not signals[-1].passed:
                errors.append(f"Invalid DOI: {doi}")
        
        if year:
            signals.append(self.literature_verifier.year_range(year))
        
        passed_count = sum(1 for s in signals if s.passed)
        total_count = len(signals)
        score = passed_count / total_count if total_count > 0 else 0.0
        
        return VerifierResult(
            passed=score >= 0.5,
            score=score,
            signals=signals,
            warnings=[],
            errors=errors
        )
    
    def verify_ic50(self, ic50: float, unit: str = "nM") -> VerifierResult:
        """
        IC50 activity verification (working verifier)
        """
        signals = []
        errors = []
        
        signals.append(self.activity_verifier.ic50_nm(ic50))
        if not signals[-1].passed:
            errors.append(f"IC50 {ic50} out of valid range")
        
        signals.append(self.activity_verifier.ic50_unit(unit))
        if not signals[-1].passed:
            errors.append(f"Invalid IC50 unit: {unit}")
        
        passed_count = sum(1 for s in signals if s.passed)
        total_count = len(signals)
        score = passed_count / total_count if total_count > 0 else 0.0
        
        return VerifierResult(
            passed=score >= 1.0,  # Both must pass
            score=score,
            signals=signals,
            warnings=[],
            errors=errors
        )
    
    def print_result(self, result: VerifierResult, title: str = "Verification Result"):
        """Pretty print verification result"""
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
        print(f"Score: {result.score:.0%}")
        print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
        print(f"\nSignals:")
        for signal in result.signals:
            status = '✅' if signal.passed else '❌'
            print(f"  {status} {signal.name}: {signal.value} (threshold: {signal.threshold})")
            if signal.details:
                print(f"      → {signal.details}")
        
        if result.warnings:
            print(f"\n⚠️  Warnings:")
            for w in result.warnings:
                print(f"  - {w}")
        
        if result.errors:
            print(f"\n❌ Errors:")
            for e in result.errors:
                print(f"  - {e}")
        
        print(f"\nMethod breakdown:")
        methods = {}
        for s in result.signals:
            methods[s.method] = methods.get(s.method, 0) + 1
        for m, c in methods.items():
            print(f"  - {m}: {c} signal(s)")
        
        print(f"{'='*60}\n")


# ============================================================
# CLI USAGE
# ============================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ARP Verifier System")
    parser.add_argument("--smiles", help="SMILES string to verify")
    parser.add_argument("--uniprot", help="UniProt ID to verify")
    parser.add_argument("--pdb", help="PDB ID to verify")
    parser.add_argument("--pmid", help="PMID to verify")
    parser.add_argument("--ic50", type=float, help="IC50 value to verify")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    verifier = ARPVerifier()
    
    if args.smiles:
        result = verifier.verify_compound(args.smiles)
        verifier.print_result(result, f"Compound: {args.smiles}")
    
    if args.uniprot:
        result = verifier.verify_target(uniprot_id=args.uniprot)
        verifier.print_result(result, f"Target: {args.uniprot}")
    
    if args.pdb:
        result = verifier.verify_pdb_structure(args.pdb)
        verifier.print_result(result, f"PDB: {args.pdb}")
    
    if args.pmid:
        result = verifier.verify_literature(pmid=args.pmid)
        verifier.print_result(result, f"Literature: {args.pmid}")
    
    if args.ic50 is not None:
        result = verifier.verify_ic50(args.ic50)
        verifier.print_result(result, f"IC50: {args.ic50} nM")
    
    # If no specific args, run demo
    if not any([args.smiles, args.uniprot, args.pdb, args.pmid, args.ic50]):
        print("🔍 ARP Verifier System - Demo Mode\n")
        
        # Demo compounds
        demo_compounds = [
            ("CCO", "Ethanol (simple)"),
            ("CC(=O)Oc1ccccc1C(=O)O", "Aspirin"),
            ("Cc1ccc(cc1)C(c2ccccc2)N3CCN(CC3)C", "Diphenhydramine"),
            ("CC(C)Cc1ccc(cc1)CHC2CCOCC2", "Ibuprofen core"),
        ]
        
        for smiles, name in demo_compounds:
            result = verifier.verify_compound(smiles)
            status = "✅" if result.passed else "❌"
            print(f"{status} {name}: {result.summary()}")
        
        print("\n" + "="*60)
        print("📊 Target Examples:")
        demo_targets = ["Q9Y2D6", "P00533", "DGAT1_HUMAN"]
        for target in demo_targets:
            result = verifier.verify_target(uniprot_id=target)
            status = "✅" if result.passed else "❌"
            print(f"{status} {target}: {result.summary()}")
        
        print("\n" + "="*60)
        print("📚 Literature Examples:")
        demo_pmids = ["35641621", "37248321", "ABC123"]
        for pmid in demo_pmids:
            result = verifier.verify_literature(pmid=pmid)
            status = "✅" if result.passed else "❌"
            print(f"{status} PMID:{pmid}: {result.summary()}")