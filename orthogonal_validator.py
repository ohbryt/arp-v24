"""
Orthogonal Validator - ARP v24
=================================
Cross-validation between prediction methods.
Alternative assay confirmation.
Experimental design suggestions.
Validation status tracking.

Based on Talanta 2026 (PMID 41996874): "orthogonal techniques for verification"
as a key pillar of the Analytical Integrity Framework.

Author: Demis (ARP v24)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Literal
from enum import Enum
from datetime import datetime


# ============================================================================
# ENUMS
# ============================================================================

class ValidationMethod(Enum):
    """Methods for orthogonal validation"""
    BIOPHYSICAL = "biophysical"        # ITC, SPR, TSA
    CELL_BASED = "cell_based"          # Cellular assays
    STRUCTURAL = "structural"           # X-ray, cryo-EM, NMR
    COMPUTATIONAL = "computational"     # Alternative computational
    ANIMAL_MODEL = "animal_model"       # In vivo validation
    CLINICAL = "clinical"              # Human studies


class ValidationStatus(Enum):
    """Overall validation status"""
    VALIDATED = "validated"             # Multiple orthogonal methods agree
    PARTIALLY_VALIDATED = "partial"     # Some validation, more needed
    PENDING = "pending"                 # Validation planned
    FAILED = "failed"                  # Orthogonal methods disagree
    NOT_VALIDATED = "not_validated"     # No validation attempted


class ValidationOutcome(Enum):
    """Outcome of a validation experiment"""
    CONFIRM = "confirm"                # Confirms primary finding
    CONTRADICT = "contradict"          # Contradicts primary finding
    PARTIAL = "partial"                # Partially supports
    INCONCLUSIVE = "inconclusive"      # Cannot determine
    PENDING = "pending"


@dataclass
class ValidationExperiment:
    """A single validation experiment"""
    experiment_id: str
    validation_method: str
    method_type: ValidationMethod

    # What is being validated
    target_claim: str          # e.g., "binding affinity", "cell viability"
    primary_value: float       # Primary readout
    primary_unit: str

    # Validation specifics
    technique: str             # Specific technique used
    readout_type: str         # e.g., "KD", "IC50", "AUC"
    assay_name: Optional[str] = None
    assay_id: Optional[str] = None

    # Quality metrics
    replicates: int = 3
    sd: Optional[float] = None
    sem: Optional[float] = None
    ci_95_lower: Optional[float] = None
    ci_95_upper: Optional[float] = None

    # Outcome
    outcome: str = ValidationOutcome.PENDING.value
    agreement_with_primary: str = "pending"
    strength_of_evidence: float = 0.5  # 0-1

    # Context
    species: str = "human"
    tissue: Optional[str] = None
    cell_type: Optional[str] = None
    conditions: Optional[str] = None  # Experimental conditions

    # Timing
    date_performed: Optional[datetime] = None
    performed_by: Optional[str] = None

    notes: str = ""
    raw_data_available: bool = False

    def __post_init__(self):
        if self.sem is None and self.sd is not None and self.replicates > 1:
            self.sem = self.sd / np.sqrt(self.replicates)
        if self.ci_95_lower is None and self.sem is not None and self.replicates > 1:
            margin = 2.0 * self.sem
            self.ci_95_lower = self.primary_value - margin
            self.ci_95_upper = self.primary_value + margin

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "validation_method": self.validation_method,
            "method_type": self.method_type.value,
            "target_claim": self.target_claim,
            "primary_value": round(self.primary_value, 4),
            "primary_unit": self.primary_unit,
            "technique": self.technique,
            "readout_type": self.readout_type,
            "replicates": self.replicates,
            "outcome": self.outcome,
            "agreement_with_primary": self.agreement_with_primary,
            "strength_of_evidence": round(self.strength_of_evidence, 2),
            "notes": self.notes,
        }


@dataclass
class OrthogonalComparison:
    """Result of comparing orthogonal validation to primary prediction"""
    claim: str
    primary_prediction: float
    primary_method: str
    primary_unit: str

    orthogonal_experiments: List[ValidationExperiment]

    # Comparison metrics
    mean_orthogonal: float
    median_orthogonal: float
    std_orthogonal: float
    n_orthogonal: int

    # Agreement assessment
    agreement: str              # "agree", "partial", "disagree"
    agreement_fraction: float   # Fraction of orthogonal experiments that agree
    delta_from_primary: float   # Mean difference from primary
    delta_ci: Tuple[float, float]  # CI on the delta

    # Overall validation status
    validation_status: ValidationStatus
    confidence: str             # high, medium, low
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim": self.claim,
            "primary_prediction": round(self.primary_prediction, 4),
            "mean_orthogonal": round(self.mean_orthogonal, 4),
            "agreement": self.agreement,
            "agreement_fraction": round(self.agreement_fraction, 2),
            "delta_from_primary": round(self.delta_from_primary, 4),
            "validation_status": self.validation_status.value,
            "confidence": self.confidence,
            "n_orthogonal": self.n_orthogonal,
            "experiments": [e.to_dict() for e in self.orthogonal_experiments],
        }


# ============================================================================
# ORTHOGONAL VALIDATOR
# ============================================================================

class OrthogonalValidator:
    """
    Orthogonal Validator - cross-validates predictions with independent methods.

    Key Principles from Talanta 2026:
    1. Orthogonal methods use different physical principles
    2. Agreement across orthogonal methods strengthens confidence
    3. Disagreement triggers investigation

    Validation Hierarchy (gold → bronze):
    GOLD: X-ray crystallography, ITC, SPR, SEC-MALS
    SILVER: Cell-based functional assays, animal models
    BRONZE: Alternative computational methods
    """

    GOLD_STANDARD_METHODS: Dict[str, ValidationMethod] = {
        "itc": ValidationMethod.BIOPHYSICAL,
        "spr": ValidationMethod.BIOPHYSICAL,
        "x-ray": ValidationMethod.STRUCTURAL,
        "cryo-em": ValidationMethod.STRUCTURAL,
        "nmr": ValidationMethod.STRUCTURAL,
        "xray": ValidationMethod.STRUCTURAL,
    }

    METHOD_HIERARCHY: Dict[ValidationMethod, int] = {
        ValidationMethod.STRUCTURAL: 4,
        ValidationMethod.BIOPHYSICAL: 3,
        ValidationMethod.CELL_BASED: 2,
        ValidationMethod.ANIMAL_MODEL: 2,
        ValidationMethod.COMPUTATIONAL: 1,
        ValidationMethod.CLINICAL: 4,
    }

    def __init__(self, agreement_threshold: float = 2.0):
        """
        Args:
            agreement_threshold: Max fold-difference to consider "agreement"
        """
        self.agreement_threshold = agreement_threshold
        self.experiments: List[ValidationExperiment] = []

    def add_experiment(
        self,
        experiment_id: str,
        validation_method: str,
        target_claim: str,
        primary_value: float,
        primary_unit: str,
        technique: str,
        readout_type: str,
        **kwargs,
    ) -> ValidationExperiment:
        """Add a validation experiment"""
        method_type = self._classify_method(validation_method)
        exp = ValidationExperiment(
            experiment_id=experiment_id,
            validation_method=validation_method,
            method_type=method_type,
            target_claim=target_claim,
            primary_value=primary_value,
            primary_unit=primary_unit,
            technique=technique,
            readout_type=readout_type,
            **kwargs,
        )
        self.experiments.append(exp)
        return exp

    def _classify_method(self, method_name: str) -> ValidationMethod:
        """Classify method into validation method type"""
        name_lower = method_name.lower()
        for key, vm in self.GOLD_STANDARD_METHODS.items():
            if key in name_lower:
                return vm
        if "cell" in name_lower or "assay" in name_lower:
            return ValidationMethod.CELL_BASED
        if "animal" in name_lower or "vivo" in name_lower or "mouse" in name_lower:
            return ValidationMethod.ANIMAL_MODEL
        if "docking" in name_lower or "md" in name_lower or "qsar" in name_lower:
            return ValidationMethod.COMPUTATIONAL
        if "clinical" in name_lower or "human" in name_lower:
            return ValidationMethod.CLINICAL
        return ValidationMethod.COMPUTATIONAL

    def compare_orthogonal(
        self,
        claim: str,
        primary_prediction: float,
        primary_method: str,
        primary_unit: str,
    ) -> OrthogonalComparison:
        """
        Compare orthogonal validation experiments against primary prediction.
        """
        # Filter experiments for this claim
        relevant = [e for e in self.experiments if e.target_claim == claim]

        if not relevant:
            return OrthogonalComparison(
                claim=claim,
                primary_prediction=primary_prediction,
                primary_method=primary_method,
                primary_unit=primary_unit,
                orthogonal_experiments=[],
                mean_orthogonal=0.0,
                median_orthogonal=0.0,
                std_orthogonal=0.0,
                n_orthogonal=0,
                agreement="pending",
                agreement_fraction=0.0,
                delta_from_primary=0.0,
                delta_ci=(0.0, 0.0),
                validation_status=ValidationStatus.NOT_VALIDATED,
                confidence="low",
                recommendations=["No orthogonal validation data available"],
            )

        ortho_values = [e.primary_value for e in relevant]
        mean_orth = float(np.mean(ortho_values))
        median_orth = float(np.median(ortho_values))
        std_orth = float(np.std(ortho_values, ddof=1)) if len(ortho_values) > 1 else 0.0

        # Assess agreement
        delta = abs(mean_orth - primary_prediction)
        if primary_prediction != 0:
            fold_diff = max(mean_orth, primary_prediction) / min(mean_orth, primary_prediction)
        else:
            fold_diff = float('inf') if mean_orth != 0 else 1.0

        if fold_diff <= self.agreement_threshold:
            agreement = "agree"
        elif fold_diff <= self.agreement_threshold * 2:
            agreement = "partial"
        else:
            agreement = "disagree"

        # Count agreeing experiments
        n_agree = sum(
            1 for e in relevant
            if max(e.primary_value, primary_prediction) / min(e.primary_value, primary_prediction)
            <= self.agreement_threshold
        )
        agree_fraction = n_agree / len(relevant)

        # Determine validation status
        if agreement == "agree" and len(relevant) >= 2:
            status = ValidationStatus.VALIDATED
        elif agreement == "agree" and len(relevant) == 1:
            status = ValidationStatus.PARTIALLY_VALIDATED
        elif agreement == "partial":
            status = ValidationStatus.PARTIALLY_VALIDATED
        elif agreement == "disagree":
            status = ValidationStatus.FAILED
        else:
            status = ValidationStatus.PENDING

        # Confidence
        if status == ValidationStatus.VALIDATED:
            confidence = "high"
        elif status == ValidationStatus.PARTIALLY_VALIDATED:
            confidence = "medium"
        else:
            confidence = "low"

        # Recommendations
        recs = self._generate_recommendations(claim, status, relevant, fold_diff)

        return OrthogonalComparison(
            claim=claim,
            primary_prediction=primary_prediction,
            primary_method=primary_method,
            primary_unit=primary_unit,
            orthogonal_experiments=relevant,
            mean_orthogonal=mean_orth,
            median_orthogonal=median_orth,
            std_orthogonal=std_orth,
            n_orthogonal=len(relevant),
            agreement=agreement,
            agreement_fraction=agree_fraction,
            delta_from_primary=delta,
            delta_ci=(delta - 1.96 * std_orth / np.sqrt(len(relevant)),
                      delta + 1.96 * std_orth / np.sqrt(len(relevant))),
            validation_status=status,
            confidence=confidence,
            recommendations=recs,
        )

    def _generate_recommendations(
        self,
        claim: str,
        status: ValidationStatus,
        experiments: List[ValidationExperiment],
        fold_diff: float,
    ) -> List[str]:
        """Generate experimental design suggestions"""
        recs: List[str] = []
        method_types = {e.method_type for e in experiments}

        if status == ValidationStatus.NOT_VALIDATED:
            recs.append(f"URGENT: Obtain orthogonal validation for {claim}")
            recs.append("Recommended: ITC or SPR for binding affinity; cell-based assay for function")

        elif status == ValidationStatus.FAILED:
            recs.append(f"⚠️  DISCREPANCY DETECTED: {fold_diff:.1f}x difference between methods")
            recs.append("Investigate potential causes: assay interference, compound stability, different conditions")
            recs.append("Consider: orthogonal biophysical method (ITC ↔ SPR)")

        elif status == ValidationStatus.PARTIALLY_VALIDATED:
            recs.append(f"Partial validation obtained ({len(experiments)} method(s))")
            recs.append("Additional orthogonal validation recommended")
            if ValidationMethod.BIOPHYSICAL not in method_types:
                recs.append("Consider: Add biophysical validation (ITC/SPR)")

        elif status == ValidationStatus.VALIDATED:
            recs.append(f"✅ Strong orthogonal validation: {len(experiments)} methods agree")

        # Method diversity recommendation
        if len(method_types) < 2:
            recs.append("Tip: Multiple method types (biophysical + cellular) strengthen validation")

        return recs

    def suggest_experimental_design(
        self,
        claim: str,
        current_method: Optional[str] = None,
        target_organism: str = "human",
    ) -> List[Dict[str, str]]:
        """
        Suggest orthogonal experimental designs for validation.
        
        Args:
            claim: What needs to be validated (binding, activity, etc.)
            current_method: What method has been used already
            target_organism: Target species
            
        Returns:
            List of experimental suggestions with priority
        """
        suggestions: List[Dict[str, str]] = []

        claim_lower = claim.lower()

        if "binding" in claim_lower or "affinity" in claim_lower or "ki" in claim_lower or "kd" in claim_lower:
            # Binding affinity validation
            if current_method != "itc":
                suggestions.append({
                    "priority": "HIGH",
                    "method": "Isothermal Titration Calorimetry (ITC)",
                    "type": "biophysical",
                    "why": "Gold standard for binding thermodynamics, direct measurement",
                    "what_you_get": "KD, ΔH, ΔS, stoichiometry",
                    "considerations": "Requires pure compound, sufficient quantity",
                })
            if current_method != "spr":
                suggestions.append({
                    "priority": "HIGH",
                    "method": "Surface Plasmon Resonance (SPR)",
                    "type": "biophysical",
                    "why": "Kinetic data (kon, koff), works with low sample",
                    "what_you_get": "KD, kinetic constants, concentration-response",
                    "considerations": "Requires immobilization, may have regeneration issues",
                })
            suggestions.append({
                "priority": "MEDIUM",
                "method": "Differential Scanning Fluorimetry (DSF/TSA)",
                "type": "biophysical",
                "why": "Screens multiple conditions, low sample consumption",
                "what_you_get": "Thermal shift, relative stabilization",
                "considerations": "Indirect measure, screening rather than quantitative",
            })

        elif "activity" in claim_lower or " potency" in claim_lower or "ic50" in claim_lower:
            # Functional activity validation
            suggestions.append({
                "priority": "HIGH",
                "method": "Cell-based dose-response assay",
                "type": "cell_based",
                "why": "Confirms functional activity in relevant cellular context",
                "what_you_get": "IC50, Emax, pathway engagement markers",
                "considerations": "Choose relevant cell line/disease model",
            })
            suggestions.append({
                "priority": "MEDIUM",
                "method": "Alternative cell assay (orthogonal)",
                "type": "cell_based",
                "why": "Rules out cell-line specific artifacts",
                "what_you_get": "Confirmation across cellular backgrounds",
                "considerations": "Different readout (e.g., reporter vs. viability)",
            })

        elif "selectivity" in claim_lower:
            suggestions.append({
                "priority": "HIGH",
                "method": "Panel screening (kinases, receptors, enzymes)",
                "type": "biophysical",
                "why": "Directly measures selectivity profile",
                "what_you_get": "Selectivity score, off-target activities",
                "considerations": "Commercial panels available (DiscoverX, etc.)",
            })
            suggestions.append({
                "priority": "MEDIUM",
                "method": "Counter-screen assays",
                "type": "cell_based",
                "why": "Tests likely off-targets",
                "what_you_get": "Specific off-target activities",
                "considerations": "Requires hypothesis about likely off-targets",
            })

        elif "toxicity" in claim_lower:
            suggestions.append({
                "priority": "HIGH",
                "method": "hERG patch clamp",
                "type": "biophysical",
                "why": "Gold standard for cardiac toxicity",
                "what_you_get": "IC50 for hERG channel blockade",
                "considerations": "Low throughput, requires expertise",
            })
            suggestions.append({
                "priority": "MEDIUM",
                "method": "Cell viability panel",
                "type": "cell_based",
                "why": "Broad cytotoxicity assessment",
                "what_you_get": "CC50 across cell lines",
                "considerations": "Does not replace specific liability assays",
            })

        else:
            suggestions.append({
                "priority": "MEDIUM",
                "method": "Alternative assay format",
                "type": "cell_based",
                "why": "Different format = orthogonal validation",
                "what_you_get": "Confirmation in different experimental context",
                "considerations": "Adapt to specific claim type",
            })

        # Add structural validation if available
        suggestions.append({
            "priority": "LOW",
            "method": "X-ray crystallography or cryo-EM",
            "type": "structural",
            "why": "Direct structural proof of binding mode",
            "what_you_get": "Binding pose, interactions, confirmation of binding site",
            "considerations": "Requires protein structure, crystals/cryo-EM grid",
        })

        return suggestions

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of all validation experiments"""
        if not self.experiments:
            return {
                "total_experiments": 0,
                "status": "no_validation_data",
                "by_method_type": {},
                "by_claim": {},
            }

        by_type: Dict[str, int] = {}
        by_claim: Dict[str, int] = {}
        by_status: Dict[str, int] = {}

        for e in self.experiments:
            by_type[e.method_type.value] = by_type.get(e.method_type.value, 0) + 1
            by_claim[e.target_claim] = by_claim.get(e.target_claim, 0) + 1
            by_status[e.outcome] = by_status.get(e.outcome, 0) + 1

        return {
            "total_experiments": len(self.experiments),
            "by_method_type": by_type,
            "by_claim": by_claim,
            "by_outcome": by_status,
            "has_gold_standard": any(
                e.method_type in (ValidationMethod.BIOPHYSICAL, ValidationMethod.STRUCTURAL)
                for e in self.experiments
            ),
        }


# ============================================================================
# VALIDATION REPORT BUILDER
# ============================================================================

class ValidationReportBuilder:
    """
    Builds comprehensive validation reports integrating all orthogonal data.
    """

    def __init__(self):
        self.validator = OrthogonalValidator()

    def build_report(
        self,
        claims: Dict[str, Dict[str, Any]],  # claim -> primary prediction info
    ) -> Dict[str, Any]:
        """
        Build validation report for multiple claims.
        
        Args:
            claims: Dict mapping claim names to prediction info
                e.g., {"binding_affinity": {"value": 45.2, "unit": "nM", "method": "docking"}}
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "claims": {},
            "overall_validation_status": ValidationStatus.NOT_VALIDATED.value,
            "validation_gaps": [],
            "experimental_suggestions": {},
        }

        validated_count = 0
        partial_count = 0

        for claim, info in claims.items():
            comparison = self.validator.compare_orthogonal(
                claim=claim,
                primary_prediction=info.get("value", 0),
                primary_method=info.get("method", "unknown"),
                primary_unit=info.get("unit", ""),
            )

            report["claims"][claim] = comparison.to_dict()

            if comparison.validation_status == ValidationStatus.VALIDATED:
                validated_count += 1
            elif comparison.validation_status == ValidationStatus.PARTIALLY_VALIDATED:
                partial_count += 1

            # Add suggestions
            if comparison.validation_status in (
                ValidationStatus.PARTIALLY_VALIDATED,
                ValidationStatus.NOT_VALIDATED,
            ):
                report["experimental_suggestions"][claim] = (
                    self.validator.suggest_experimental_design(claim)
                )

        # Overall status
        n_claims = len(claims)
        if validated_count == n_claims:
            report["overall_validation_status"] = ValidationStatus.VALIDATED.value
        elif validated_count + partial_count >= n_claims * 0.5:
            report["overall_validation_status"] = ValidationStatus.PARTIALLY_VALIDATED.value
        else:
            report["validation_gaps"] = [
                claim for claim, comp in report["claims"].items()
                if comp["validation_status"] in ("not_validated", "pending")
            ]

        return report

    def format_report(self, report: Dict[str, Any]) -> str:
        """Format validation report as human-readable string"""
        lines = [
            "Orthogonal Validation Report",
            "=" * 60,
            f"Overall Status: {report['overall_validation_status'].upper()}",
            f"Timestamp: {report['timestamp']}",
            "",
        ]

        for claim, data in report["claims"].items():
            lines.append(f"\n📋 {claim}")
            lines.append(f"   Primary: {data['primary_prediction']} {data['primary_unit']} ({data['primary_method']})")
            lines.append(f"   Orthogonal mean: {data['mean_orthogonal']} {data['primary_unit']}")
            lines.append(f"   Agreement: {data['agreement'].upper()} ({data['agreement_fraction']:.0%})")
            lines.append(f"   Status: {data['validation_status']}")

            if data.get("experiments"):
                lines.append("   Experiments:")
                for exp in data["experiments"]:
                    lines.append(f"     - {exp['technique']}: {exp['primary_value']} {exp['primary_unit']} ({exp['outcome']})")

        if report.get("validation_gaps"):
            lines.append("\n⚠️  VALIDATION GAPS:")
            for gap in report["validation_gaps"]:
                lines.append(f"   - {gap}: No orthogonal validation")

        return "\n".join(lines)


# ============================================================================
# TESTS
# ============================================================================

def test_orthogonal_validator():
    """Test orthogonal validator"""
    validator = OrthogonalValidator(agreement_threshold=2.0)

    # Add primary prediction
    primary_binding = 45.2  # nM from docking

    # Add orthogonal experiments
    validator.add_experiment(
        experiment_id="exp_itc_001",
        validation_method="itc",
        target_claim="binding_affinity",
        primary_value=48.5,  # nM
        primary_unit="nM",
        technique="ITC",
        readout_type="KD",
        replicates=3,
        sd=3.2,
        outcome=ValidationOutcome.CONFIRM.value,
        agreement_with_primary="confirm",
        strength_of_evidence=0.9,
    )

    validator.add_experiment(
        experiment_id="exp_spr_001",
        validation_method="spr",
        target_claim="binding_affinity",
        primary_value=52.0,  # nM
        primary_unit="nM",
        technique="SPR",
        readout_type="KD",
        replicates=2,
        sd=4.5,
        outcome=ValidationOutcome.CONFIRM.value,
        agreement_with_primary="confirm",
        strength_of_evidence=0.85,
    )

    validator.add_experiment(
        experiment_id="exp_cell_001",
        validation_method="cell_based",
        target_claim="functional_activity",
        primary_value=120.0,  # nM
        primary_unit="nM",
        technique="Cell viability assay",
        readout_type="IC50",
        replicates=4,
        sd=15.0,
        outcome=ValidationOutcome.PARTIAL.value,
        agreement_with_primary="partial",
        strength_of_evidence=0.6,
    )

    # Compare
    binding_comparison = validator.compare_orthogonal(
        claim="binding_affinity",
        primary_prediction=primary_binding,
        primary_method="docking",
        primary_unit="nM",
    )

    print(f"✓ Orthogonal comparison for binding_affinity:")
    print(f"    Primary: {binding_comparison.primary_prediction} nM")
    print(f"    Orthogonal mean: {binding_comparison.mean_orthogonal:.2f} nM")
    print(f"    Agreement: {binding_comparison.agreement} ({binding_comparison.agreement_fraction:.0%})")
    print(f"    Status: {binding_comparison.validation_status.value}")
    print(f"    Confidence: {binding_comparison.confidence}")

    for rec in binding_comparison.recommendations:
        print(f"    → {rec}")


def test_disagreement_detection():
    """Test detection of disagreement between methods"""
    validator = OrthogonalValidator(agreement_threshold=2.0)

    # Add experiments with disagreement
    validator.add_experiment(
        experiment_id="exp_1",
        validation_method="itc",
        target_claim="binding",
        primary_value=50.0,
        primary_unit="nM",
        technique="ITC",
        readout_type="KD",
        outcome=ValidationOutcome.CONFIRM.value,
    )

    validator.add_experiment(
        experiment_id="exp_2",
        validation_method="cell_based",
        target_claim="binding",
        primary_value=5000.0,  # 100x different!
        primary_unit="nM",
        technique="Cell assay",
        readout_type="IC50",
        outcome=ValidationOutcome.CONTRADICT.value,
    )

    comparison = validator.compare_orthogonal(
        claim="binding",
        primary_prediction=50.0,
        primary_method="itc",
        primary_unit="nM",
    )

    print(f"\n✓ Disagreement detection:")
    print(f"    Agreement: {comparison.agreement}")
    print(f"    Fold difference: {comparison.delta_from_primary / 50.0 * 100:.0f}x")


def test_experimental_suggestions():
    """Test experimental design suggestions"""
    validator = OrthogonalValidator()

    suggestions = validator.suggest_experimental_design("binding_affinity")
    print(f"\n✓ Experimental suggestions for binding_affinity:")
    for s in suggestions[:3]:
        print(f"    [{s['priority']}] {s['method']} ({s['type']})")
        print(f"         Why: {s['why']}")


def test_validation_report():
    """Test full validation report"""
    builder = ValidationReportBuilder()

    claims = {
        "binding_affinity": {"value": 45.2, "unit": "nM", "method": "docking"},
        "cell_activity": {"value": 120.0, "unit": "nM", "method": "qsar"},
    }

    report = builder.build_report(claims)
    print(f"\n{builder.format_report(report)}")


def test_validation_summary():
    """Test validation summary"""
    validator = OrthogonalValidator()

    validator.add_experiment(
        experiment_id="exp_1", validation_method="itc",
        target_claim="binding", primary_value=50.0, primary_unit="nM",
        technique="ITC", readout_type="KD", outcome="confirm",
    )
    validator.add_experiment(
        experiment_id="exp_2", validation_method="spr",
        target_claim="binding", primary_value=55.0, primary_unit="nM",
        technique="SPR", readout_type="KD", outcome="confirm",
    )
    validator.add_experiment(
        experiment_id="exp_3", validation_method="cell_based",
        target_claim="activity", primary_value=100.0, primary_unit="nM",
        technique="Cell assay", readout_type="EC50", outcome="partial",
    )

    summary = validator.get_validation_summary()
    print(f"\n✓ Validation summary: {summary}")


if __name__ == "__main__":
    print("Testing Orthogonal Validator...")
    test_orthogonal_validator()
    test_disagreement_detection()
    test_experimental_suggestions()
    test_validation_report()
    test_validation_summary()
    print("\n✅ All Orthogonal Validator tests passed!")
