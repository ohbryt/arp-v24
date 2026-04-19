"""
Analytical Integrity Framework - ARP v24
==========================================
Based on Talanta 2026 (PMID 41996874) "AI-enabled drug design" insights.
Three Pillars: Measurement Uncertainty, Data Quality, Experimental Validation.
Provides confidence intervals (95% CI) for all pipeline predictions.

Author: Demis (ARP v24)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import copy


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ConfidenceLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __repr__(self) -> str:
        return f"ConfidenceLevel.{self.value}"


class ValidationStatus(Enum):
    VERIFIED = "verified"       # Orthogonal confirmation
    PARTIAL = "partial"         # Some independent evidence
    UNVERIFIED = "unverified"   # Single source / in-silico only


class MeasurementTechnique(Enum):
    """Analytical measurement techniques with inherent uncertainty"""
    X_RAY_CRYSTALLOGRAPHY = ("xray", 0.02, "Angstrom resolution")
    CRYO_EM = ("cryoem", 0.05, "Angstrom resolution")
    NMR = ("nmr", 0.10, "ppm chemical shift")
    MASS_SPEC = ("massspec", 0.05, "m/z accuracy")
    ITC = ("itc", 0.08, "kcal/mol")
    SPR = ("spr", 0.10, "binding constant")
    FRET = ("fret", 0.15, "distance constraint")
    ALPHALISA = ("alphalisa", 0.12, "proximity assay")
    ELISA = ("elisa", 0.15, "concentration")
    qPCR = ("qpcr", 0.20, "Ct value")
    WESTERN_BLOT = ("western", 0.25, "band intensity")
    IN_SILICO = ("insilico", 0.40, "computational prediction")
    DOCKING = ("docking", 0.50, "binding score")

    def __init__(self, code: str, inherent_uncertainty: float, readout: str):
        self.code = code
        self.inherent_uncertainty = inherent_uncertainty  # Fractional uncertainty
        self.readout = readout

    @classmethod
    def from_code(cls, code: str) -> "MeasurementTechnique":
        for t in cls:
            if t.code == code:
                return t
        return cls.IN_SILICO


@dataclass
class AssayRecord:
    """Single assay measurement record"""
    assay_id: str
    technique: MeasurementTechnique
    value: float
    unit: str
    replicates: int = 1
    sd: Optional[float] = None
    sem: Optional[float] = None
    ci_95_lower: Optional[float] = None
    ci_95_upper: Optional[float] = None
    n_samples: Optional[int] = None
    p_value: Optional[float] = None
    assay_name: Optional[str] = None
    date_performed: Optional[datetime] = None
    lab_quality_rating: Optional[str] = None  # " GLP", "research", "screening"

    def __post_init__(self):
        if self.replicates > 1 and self.sd is not None:
            self.sem = self.sd / np.sqrt(self.replicates)
        if self.sem is not None and self.replicates > 1:
            # t-value approximation for 95% CI (df > 10)
            t_value = 2.228 if self.replicates <= 11 else 1.96
            margin = t_value * self.sem
            self.ci_95_lower = self.value - margin
            self.ci_95_upper = self.value + margin


# ============================================================================
# CORE DATA CLASSES
# ============================================================================

@dataclass
class UncertaintyResult:
    """
    Uncertainty quantification result with bootstrap confidence intervals.
    
    Attributes:
        point_estimate: Best estimate of the value
        ci_lower_95: Lower bound of 95% confidence interval
        ci_upper_95: Upper bound of 95% confidence interval
        confidence_level: HIGH (CI width < 10%), MEDIUM (10-25%), LOW (> 25%)
        n_bootstrap: Number of bootstrap iterations performed
        std_error: Bootstrap standard error
        method: Description of uncertainty method used
    """
    point_estimate: float
    ci_lower_95: float
    ci_upper_95: float
    confidence_level: str  # high, medium, low
    n_bootstrap: int = 1000
    std_error: Optional[float] = None
    method: str = "bootstrap"

    def __post_init__(self):
        if self.confidence_level not in ("high", "medium", "low"):
            # Auto-determine from CI width
            if self.point_estimate != 0:
                ci_width = abs(self.ci_upper_95 - self.ci_lower_95) / abs(self.point_estimate)
            else:
                ci_width = float('inf')
            
            if ci_width < 0.10:
                self.confidence_level = "high"
            elif ci_width < 0.25:
                self.confidence_level = "medium"
            else:
                self.confidence_level = "low"

    @property
    def ci_width(self) -> float:
        """Absolute width of 95% CI"""
        return self.ci_upper_95 - self.ci_lower_95

    @property
    def ci_width_fraction(self) -> float:
        """Relative CI width (coefficient of variation of the estimate)"""
        if self.point_estimate == 0:
            return float('inf')
        return self.ci_width / abs(self.point_estimate)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "point_estimate": round(self.point_estimate, 4),
            "ci_lower_95": round(self.ci_lower_95, 4),
            "ci_upper_95": round(self.ci_upper_95, 4),
            "confidence_level": self.confidence_level,
            "n_bootstrap": self.n_bootstrap,
            "std_error": round(self.std_error, 4) if self.std_error else None,
            "method": self.method,
        }


@dataclass
class AnalyticalIntegrity:
    """
    Three-pillar analytical integrity assessment.
    
    Pillar 1 - Measurement Quality: How good are the analytical techniques?
    Pillar 2 - Data Quality: How reliable/reproducible is the data?
    Pillar 3 - Validation Status: Has orthogonal confirmation been obtained?
    
    integrity_score (0-1): Weighted average - 1.0 = Gold standard, 0.0 = Unreliable
    """
    measurement_quality: float      # 0-1: Technique precision/calibration
    data_quality: float             # 0-1: Purity, consistency, reproducibility
    validation_status: str          # verified, partial, unverified
    integrity_score: float          # 0-1 weighted average

    measurement_details: Dict[str, Any] = field(default_factory=dict)
    data_quality_details: Dict[str, Any] = field(default_factory=dict)
    validation_details: Dict[str, Any] = field(default_factory=dict)
    sources: List[str] = field(default_factory=list)
    assay_records: List[AssayRecord] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.integrity_score == 0.0:
            self.integrity_score = self._compute_score()

    def _compute_score(self) -> float:
        """Compute weighted integrity score from three pillars"""
        validation_weight = 0.40 if self.validation_status == "verified" else \
                           0.25 if self.validation_status == "partial" else 0.10
        measurement_weight = 0.35
        data_weight = 0.25
        # Normalize validation to numeric
        validation_map = {"verified": 1.0, "partial": 0.5, "unverified": 0.1}
        v_score = validation_map.get(self.validation_status, 0.1)
        return (self.measurement_quality * measurement_weight +
                self.data_quality * data_weight +
                v_score * validation_weight)

    def overall_confidence(self) -> ConfidenceLevel:
        """Derive confidence level from integrity score"""
        if self.integrity_score >= 0.75:
            return ConfidenceLevel.HIGH
        elif self.integrity_score >= 0.45:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def to_dict(self) -> Dict[str, Any]:
        return {
            "measurement_quality": round(self.measurement_quality, 3),
            "data_quality": round(self.data_quality, 3),
            "validation_status": self.validation_status,
            "integrity_score": round(self.integrity_score, 3),
            "confidence": self.overall_confidence().value,
            "measurement_details": self.measurement_details,
            "data_quality_details": self.data_quality_details,
            "validation_details": self.validation_details,
            "n_sources": len(self.sources),
            "n_assay_records": len(self.assay_records),
            "caveats": self.caveats,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ExperimentalValidationRecord:
    """Track experimental validation attempts and outcomes"""
    experiment_id: str
    experiment_type: str          # "orthogonal_assay", "functional", "structural", "clinical"
    status: str                   # "passed", "failed", "pending", "inconclusive"
    result: Optional[str] = None
    agreement_with_prediction: Optional[str] = None  # "confirm", "contradict", "partial"
    technique: Optional[MeasurementTechnique] = None
    evidence_strength: float = 0.5  # 0-1
    notes: str = ""
    date: Optional[datetime] = None


@dataclass
class DataQualityAssessment:
    """Comprehensive data quality metrics"""
    purity_score: float = 0.0        # Chemical purity (HPLC/LC-MS)
    consistency_score: float = 0.0   # Cross-study agreement
    reproducibility_score: float = 0.0  # Replicate agreement
    overall_quality: float = 0.0

    missing_data_fraction: float = 0.0
    outlier_flag: bool = False
    publication_bias_flag: bool = False

    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.overall_quality == 0.0:
            self.overall_quality = (
                self.purity_score * 0.30 +
                self.consistency_score * 0.35 +
                self.reproducibility_score * 0.35
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "purity_score": round(self.purity_score, 3),
            "consistency_score": round(self.consistency_score, 3),
            "reproducibility_score": round(self.reproducibility_score, 3),
            "overall_quality": round(self.overall_quality, 3),
            "missing_data_fraction": round(self.missing_data_fraction, 3),
            "outlier_flag": self.outlier_flag,
            "publication_bias_flag": self.publication_bias_flag,
            "details": self.details,
        }


# ============================================================================
# MEASUREMENT UNCERTAINTY ENGINE
# ============================================================================

class MeasurementUncertaintyEngine:
    """
    Quantifies measurement uncertainty using bootstrap resampling
    and propagation of instrumental errors.
    """

    def __init__(self, random_seed: int = 42):
        self.rng = np.random.default_rng(random_seed)

    def bootstrap_ci(
        self,
        values: List[float],
        n_bootstrap: int = 1000,
        ci_percentile: Tuple[float, float] = (2.5, 97.5),
    ) -> UncertaintyResult:
        """
        Compute bootstrap confidence interval for a set of measurements.
        
        Args:
            values: List of measurement values
            n_bootstrap: Number of bootstrap iterations
            ci_percentile: Percentiles for CI (default: 2.5th and 97.5th = 95% CI)
        Returns:
            UncertaintyResult with point estimate and 95% CI
        """
        arr = np.array(values)
        if len(arr) < 2:
            return UncertaintyResult(
                point_estimate=arr[0] if len(arr) == 1 else 0.0,
                ci_lower_95=arr[0] if len(arr) == 1 else 0.0,
                ci_upper_95=arr[0] if len(arr) == 1 else 0.0,
                confidence_level="low",
                n_bootstrap=0,
                method="insufficient_data",
            )

        point_estimate = float(np.mean(arr))
        bootstrap_means: List[float] = []

        for _ in range(n_bootstrap):
            resample = self.rng.choice(arr, size=len(arr), replace=True)
            bootstrap_means.append(float(np.mean(resample)))

        lower_idx = int(ci_percentile[0] / 100 * n_bootstrap)
        upper_idx = int(ci_percentile[1] / 100 * n_bootstrap)
        sorted_means = sorted(bootstrap_means)
        ci_lower = sorted_means[max(0, lower_idx - 1)]
        ci_upper = sorted_means[min(len(sorted_means) - 1, upper_idx)]
        std_error = float(np.std(bootstrap_means, ddof=1))

        # Determine confidence level
        if abs(point_estimate) > 0:
            ci_width_frac = (ci_upper - ci_lower) / abs(point_estimate)
        else:
            ci_width_frac = float('inf')

        if ci_width_frac < 0.10:
            conf_level = "high"
        elif ci_width_frac < 0.25:
            conf_level = "medium"
        else:
            conf_level = "low"

        return UncertaintyResult(
            point_estimate=round(point_estimate, 6),
            ci_lower_95=round(ci_lower, 6),
            ci_upper_95=round(ci_upper, 6),
            confidence_level=conf_level,
            n_bootstrap=n_bootstrap,
            std_error=round(std_error, 6),
            method="bootstrap_percentile",
        )

    def pooled_uncertainty(
        self,
        assay_records: List[AssayRecord],
        technique_weighted: bool = True,
    ) -> UncertaintyResult:
        """
        Combine uncertainty from multiple assay records.
        Technique-weighted gives more trust to gold-standard methods.
        """
        if not assay_records:
            return UncertaintyResult(
                point_estimate=0.0, ci_lower_95=0.0, ci_upper_95=0.0,
                confidence_level="low", n_bootstrap=0, method="no_data"
            )

        # Extract values, optionally weighted by technique quality
        if technique_weighted:
            weights: List[float] = []
            values: List[float] = []
            for rec in assay_records:
                # Weight inversely proportional to inherent uncertainty
                w = 1.0 / (rec.technique.inherent_uncertainty + 0.01)
                # Adjust by number of replicates
                w *= np.sqrt(rec.replicates)
                weights.append(w)
                values.append(rec.value)

            total_weight = sum(weights)
            point_estimate = sum(w * v for w, v in zip(weights, values)) / total_weight

            # Weighted variance for CI calculation
            weighted_var = sum(w * (v - point_estimate) ** 2 for w, v in zip(weights, values)) / total_weight
            pooled_se = np.sqrt(weighted_var / len(assay_records))
            ci_lower = point_estimate - 1.96 * pooled_se
            ci_upper = point_estimate + 1.96 * pooled_se
        else:
            values = [rec.value for rec in assay_records]
            point_estimate = float(np.mean(values))
            all_sems = [rec.sem for rec in assay_records if rec.sem is not None]
            if all_sems:
                pooled_se = float(np.sqrt(sum(s**2 for s in all_sems) / len(all_sems)))
                ci_lower = point_estimate - 1.96 * pooled_se
                ci_upper = point_estimate + 1.96 * pooled_se
            else:
                ci_lower = point_estimate
                ci_upper = point_estimate

        # Use bootstrap on the values for more robust CI
        boot_result = self.bootstrap_ci(values, n_bootstrap=1000)

        return UncertaintyResult(
            point_estimate=round(point_estimate, 6),
            ci_lower_95=round(ci_lower, 6),
            ci_upper_95=round(ci_upper, 6),
            confidence_level=boot_result.confidence_level,
            n_bootstrap=boot_result.n_bootstrap,
            std_error=boot_result.std_error,
            method="pooled_uncertainty" if technique_weighted else "simple_mean",
        )

    def propagate_error(
        self,
        value: float,
        relative_uncertainties: Dict[str, float],
    ) -> UncertaintyResult:
        """
        Propagate multiple independent error sources in quadrature.
        
        Args:
            value: Nominal value
            relative_uncertainties: Dict of error_source -> fractional uncertainty
        Returns:
            UncertaintyResult with combined CI
        """
        combined_var = sum(u**2 for u in relative_uncertainties.values())
        combined_uncertainty = np.sqrt(combined_var)

        ci_lower = value * (1 - 1.96 * combined_uncertainty)
        ci_upper = value * (1 + 1.96 * combined_uncertainty)

        if combined_uncertainty < 0.05:
            conf = "high"
        elif combined_uncertainty < 0.15:
            conf = "medium"
        else:
            conf = "low"

        return UncertaintyResult(
            point_estimate=round(value, 6),
            ci_lower_95=round(ci_lower, 6),
            ci_upper_95=round(ci_upper, 6),
            confidence_level=conf,
            n_bootstrap=0,
            std_error=round(value * combined_uncertainty / 1.96, 6),
            method="error_propagation",
        )


# ============================================================================
# DATA QUALITY ASSESSOR
# ============================================================================

class DataQualityAssessor:
    """
    Assesses data quality across multiple dimensions:
    - Purity (chemical/biological)
    - Consistency (cross-study)
    - Reproducibility (replicate agreement)
    """

    # Quality benchmarks
    PURITY_BENCHMARKS = {
        "hplc": 0.95,
        "lcms": 0.90,
        "nmr": 0.85,
        "gcms": 0.88,
    }

    def assess_purity(self, reported_purity: float, method: str = "lcms") -> float:
        """Score chemical purity relative to gold-standard benchmark"""
        benchmark = self.PURITY_BENCHMARKS.get(method.lower(), 0.85)
        score = min(reported_purity / benchmark, 1.0)
        return round(score, 3)

    def assess_consistency(
        self,
        values: List[float],
        tolerance_factor: float = 2.0,
    ) -> Tuple[float, bool]:
        """
        Assess cross-study consistency.
        tolerance_factor: how many pooled SDs to allow as "consistent"
        Returns (consistency_score, outlier_flag)
        """
        if len(values) < 2:
            return 0.3, False

        arr = np.array(values)
        mean = np.mean(arr)
        sd = np.std(arr, ddof=1)

        if sd == 0:
            return 1.0, False

        cv = sd / abs(mean) if mean != 0 else float('inf')

        # CV-based scoring (lower CV = better)
        if cv < 0.10:
            score = 1.0
        elif cv < 0.25:
            score = 0.8
        elif cv < 0.50:
            score = 0.5
        else:
            score = 0.2

        # Outlier detection: values > tolerance_factor SDs from mean
        outlier = any(abs(v - mean) > tolerance_factor * sd for v in values)

        return round(score, 3), outlier

    def assess_reproducibility(
        self,
        replicates: List[float],
        expected_cv: float = 0.15,
    ) -> float:
        """
        Score replicate reproducibility.
        expected_cv: typical CV for the assay type
        """
        if len(replicates) < 2:
            return 0.3  # Insufficient data

        cv = np.std(replicates, ddof=1) / abs(np.mean(replicates)) if np.mean(replicates) != 0 else float('inf')

        if cv <= expected_cv * 0.5:
            return 1.0
        elif cv <= expected_cv:
            return 0.85
        elif cv <= expected_cv * 2:
            return 0.6
        elif cv <= expected_cv * 3:
            return 0.3
        else:
            return 0.1

    def comprehensive_assessment(
        self,
        purity: Optional[float] = None,
        purity_method: Optional[str] = None,
        consistency_values: Optional[List[float]] = None,
        replicates: Optional[List[float]] = None,
        replicate_expected_cv: float = 0.15,
        missing_fraction: float = 0.0,
        publication_bias_indicators: Optional[List[str]] = None,
    ) -> DataQualityAssessment:
        """Full data quality assessment"""
        # Purity
        if purity is not None:
            purity_score = self.assess_purity(purity, purity_method or "lcms")
        else:
            purity_score = 0.5  # Unknown

        # Consistency
        if consistency_values and len(consistency_values) >= 2:
            consistency_score, outlier_flag = self.assess_consistency(consistency_values)
        else:
            consistency_score = 0.4  # Insufficient data
            outlier_flag = False

        # Reproducibility
        if replicates and len(replicates) >= 2:
            reproducibility_score = self.assess_reproducibility(replicates, replicate_expected_cv)
        else:
            reproducibility_score = 0.4

        # Publication bias
        pub_bias = False
        if publication_bias_indicators:
            # Heuristics: only-positive-results, single-lab, small-n
            pub_bias = len(publication_bias_indicators) >= 2

        assessment = DataQualityAssessment(
            purity_score=purity_score,
            consistency_score=consistency_score,
            reproducibility_score=reproducibility_score,
            overall_quality=0.0,  # Computed in __post_init__
            missing_data_fraction=missing_fraction,
            outlier_flag=outlier_flag,
            publication_bias_flag=pub_bias,
            details={
                "purity_method": purity_method,
                "n_consistency_values": len(consistency_values) if consistency_values else 0,
                "n_replicates": len(replicates) if replicates else 0,
                "pub_bias_indicators": publication_bias_indicators or [],
            },
        )
        return assessment


# ============================================================================
# EXPERIMENTAL VALIDATION TRACKER
# ============================================================================

class ExperimentalValidationTracker:
    """
    Tracks orthogonal experimental validation across the pipeline.
    Implements the 3rd pillar of the Analytical Integrity Spectrum.
    """

    GOLD_STANDARD_TECHNIQUES = {
        MeasurementTechnique.X_RAY_CRYSTALLOGRAPHY,
        MeasurementTechnique.CRYO_EM,
        MeasurementTechnique.ISothermal_TITRATION_CALORIMETRY,
    }

    def __init__(self):
        self.validations: List[ExperimentalValidationRecord] = []

    def add_validation(
        self,
        experiment_id: str,
        experiment_type: str,
        status: str,
        result: Optional[str] = None,
        agreement: Optional[str] = None,
        technique: Optional[MeasurementTechnique] = None,
        evidence_strength: float = 0.5,
        notes: str = "",
    ) -> ExperimentalValidationRecord:
        """Record a new experimental validation"""
        record = ExperimentalValidationRecord(
            experiment_id=experiment_id,
            experiment_type=experiment_type,
            status=status,
            result=result,
            agreement_with_prediction=agreement,
            technique=technique,
            evidence_strength=evidence_strength,
            notes=notes,
            date=datetime.now(),
        )
        self.validations.append(record)
        return record

    def validation_status(self) -> ValidationStatus:
        """Determine overall validation status"""
        if not self.validations:
            return ValidationStatus.UNVERIFIED

        passed = [v for v in self.validations if v.status == "passed"]
        confirming = [v for v in self.validations if v.agreement_with_prediction == "confirm"]

        if len(confirming) >= 2:
            return ValidationStatus.VERIFIED
        elif len(passed) >= 1 and len(confirming) >= 1:
            return ValidationStatus.VERIFIED
        elif len(passed) >= 1 or len(confirming) == 1:
            return ValidationStatus.PARTIAL
        else:
            return ValidationStatus.UNVERIFIED

    def evidence_strength_score(self) -> float:
        """Aggregate evidence strength across all validations"""
        if not self.validations:
            return 0.0

        # Weight by validation type (orthogonal > functional > binding)
        type_weights = {
            "orthogonal_assay": 1.5,
            "structural": 1.3,
            "functional": 1.1,
            "clinical": 1.4,
        }

        total_weighted = 0.0
        total_weight = 0.0
        for v in self.validations:
            w = type_weights.get(v.experiment_type, 1.0)
            total_weighted += w * v.evidence_strength
            total_weight += w

        return round(total_weighted / total_weight, 3) if total_weight > 0 else 0.0

    def suggest_next_validation(
        self,
        prediction_type: str,
        current_status: ValidationStatus,
    ) -> List[Dict[str, str]]:
        """Suggest orthogonal validation experiments"""
        suggestions = []
        existing_types = {v.experiment_type for v in self.validations}

        if current_status == ValidationStatus.UNVERIFIED:
            suggestions.append({
                "priority": "high",
                "experiment_type": "orthogonal_assay",
                "recommendation": "Obtain at least 2 independent orthogonal validations",
                "techniques": "SPR, ITC, or cryo-EM for binding; cell-based orthogonal assay for activity",
            })
        elif current_status == ValidationStatus.PARTIAL:
            suggestions.append({
                "priority": "medium",
                "experiment_type": "functional",
                "recommendation": "Confirm functional relevance in disease-relevant model",
                "techniques": "Primary cell assay, organoid, or in vivo model",
            })

        if "orthogonal_assay" not in existing_types:
            suggestions.append({
                "priority": "high",
                "experiment_type": "orthogonal_assay",
                "recommendation": "Add orthogonal biophysical confirmation",
                "techniques": "ITC (gold standard), SPR, TSA",
            })

        if "structural" not in existing_types and prediction_type == "binding":
            suggestions.append({
                "priority": "medium",
                "experiment_type": "structural",
                "recommendation": "Structural validation of binding mode",
                "techniques": "X-ray crystallography or cryo-EM",
            })

        return suggestions


# ============================================================================
# ANALYTICAL INTEGRITY FRAMEWORK - MAIN ORCHESTRATOR
# ============================================================================

class AnalyticalIntegrityFramework:
    """
    Main orchestrator for the Three-Pillar Analytical Integrity Framework.
    
    Pillar 1: Measurement Uncertainty
    Pillar 2: Data Quality Assessment  
    Pillar 3: Experimental Validation
    
    Usage:
        aif = AnalyticalIntegrityFramework()
        aif.add_assay_record(...)
        aif.add_validation(...)
        integrity = aif.assess(molecule_id="DRD2_agonist_001")
    """

    def __init__(self, random_seed: int = 42):
        self.uncertainty_engine = MeasurementUncertaintyEngine(random_seed)
        self.quality_assessor = DataQualityAssessor()
        self.validation_tracker = ExperimentalValidationTracker()
        self.assay_records: Dict[str, List[AssayRecord]] = {}  # keyed by molecule_id
        self.validations: Dict[str, List[ExperimentalValidationRecord]] = {}

    def add_assay_record(
        self,
        molecule_id: str,
        assay_id: str,
        technique: MeasurementTechnique,
        value: float,
        unit: str,
        replicates: int = 1,
        sd: Optional[float] = None,
        **kwargs,
    ) -> AssayRecord:
        """Add an assay record for a molecule"""
        record = AssayRecord(
            assay_id=assay_id,
            technique=technique,
            value=value,
            unit=unit,
            replicates=replicates,
            sd=sd,
            **kwargs,
        )
        if molecule_id not in self.assay_records:
            self.assay_records[molecule_id] = []
        self.assay_records[molecule_id].append(record)
        return record

    def add_validation(
        self,
        molecule_id: str,
        experiment_id: str,
        experiment_type: str,
        status: str,
        **kwargs,
    ) -> ExperimentalValidationRecord:
        """Add an experimental validation for a molecule"""
        record = self.validation_tracker.add_validation(
            experiment_id=experiment_id,
            experiment_type=experiment_type,
            status=status,
            **kwargs,
        )
        if molecule_id not in self.validations:
            self.validations[molecule_id] = []
        self.validations[molecule_id].append(record)
        return record

    def assess_measurement_uncertainty(self, molecule_id: str) -> UncertaintyResult:
        """Pillar 1: Assess measurement uncertainty for a molecule"""
        records = self.assay_records.get(molecule_id, [])
        if not records:
            return UncertaintyResult(
                point_estimate=0.0, ci_lower_95=0.0, ci_upper_95=0.0,
                confidence_level="low", n_bootstrap=0, method="no_data"
            )
        return self.uncertainty_engine.pooled_uncertainty(records, technique_weighted=True)

    def assess_data_quality(self, molecule_id: str) -> DataQualityAssessment:
        """Pillar 2: Assess data quality for a molecule"""
        records = self.assay_records.get(molecule_id, [])

        # Extract values for consistency
        values = [r.value for r in records]
        replicates_by_assay: Dict[str, List[float]] = {}
        for r in records:
            if r.assay_id not in replicates_by_assay:
                replicates_by_assay[r.assay_id] = []
            replicates_by_assay[r.assay_id].append(r.value)

        # For reproducibility: use first assay's replicates if available
        rep_values = list(replicates_by_assay.values())[0] if replicates_by_assay else None

        return self.quality_assessor.comprehensive_assessment(
            consistency_values=values if len(values) >= 2 else None,
            replicates=rep_values if rep_values and len(rep_values) >= 2 else None,
        )

    def assess_validation_status(self, molecule_id: str) -> ValidationStatus:
        """Pillar 3: Assess validation status for a molecule"""
        vals = self.validations.get(molecule_id, [])
        if not vals:
            return ValidationStatus.UNVERIFIED

        passed = [v for v in vals if v.status == "passed"]
        confirming = [v for v in vals if v.agreement_with_prediction == "confirm"]

        if len(confirming) >= 2 or (len(passed) >= 1 and len(confirming) >= 1):
            return ValidationStatus.VERIFIED
        elif len(passed) >= 1 or len(confirming) == 1:
            return ValidationStatus.PARTIAL
        return ValidationStatus.UNVERIFIED

    def assess(self, molecule_id: str) -> AnalyticalIntegrity:
        """
        Full three-pillar analytical integrity assessment.
        
        Returns:
            AnalyticalIntegrity with all three pillars evaluated
        """
        # Pillar 1: Measurement uncertainty
        uncertainty = self.assess_measurement_uncertainty(molecule_id)
        if uncertainty.confidence_level == "high":
            mq = 0.9
        elif uncertainty.confidence_level == "medium":
            mq = 0.6
        else:
            mq = 0.3

        # Pillar 2: Data quality
        dqa = self.assess_data_quality(molecule_id)
        dq = dqa.overall_quality

        # Pillar 3: Validation status
        vs = self.assess_validation_status(molecule_id)
        vs_str = vs.value

        # Caveats
        caveats = []
        if dqa.outlier_flag:
            caveats.append("Outlier detected in cross-study data")
        if dqa.publication_bias_flag:
            caveats.append("Potential publication bias indicators present")
        if vs == ValidationStatus.UNVERIFIED:
            caveats.append("No orthogonal experimental validation available")
        elif vs == ValidationStatus.PARTIAL:
            caveats.append("Partial validation - additional orthogonal confirmation recommended")

        records = self.assay_records.get(molecule_id, [])
        sources = list(set(r.lab_quality_rating or "unknown" for r in records))

        integrity = AnalyticalIntegrity(
            measurement_quality=mq,
            data_quality=dq,
            validation_status=vs_str,
            integrity_score=0.0,  # Computed in __post_init__
            measurement_details={
                "n_records": len(records),
                "techniques": [r.technique.code for r in records],
                "uncertainty": uncertainty.to_dict(),
            },
            data_quality_details=dqa.to_dict(),
            validation_details={
                "n_validations": len(self.validations.get(molecule_id, [])),
                "suggestions": self.validation_tracker.suggest_next_validation(
                    "binding", vs
                ) if molecule_id else [],
            },
            sources=sources,
            assay_records=records,
            caveats=caveats,
        )
        return integrity

    def summary_report(self, molecule_id: str) -> Dict[str, Any]:
        """Generate a summary report for a molecule"""
        integrity = self.assess(molecule_id)
        return {
            "molecule_id": molecule_id,
            "analytical_integrity": integrity.to_dict(),
            "three_pillars": {
                "measurement_quality": {
                    "score": integrity.measurement_quality,
                    "description": self._describe_measurement_quality(integrity.measurement_quality),
                },
                "data_quality": {
                    "score": integrity.data_quality,
                    "description": self._describe_data_quality(integrity.data_quality),
                },
                "validation_status": {
                    "status": integrity.validation_status,
                    "description": self._describe_validation_status(integrity.validation_status),
                },
            },
            "recommendations": self._generate_recommendations(integrity),
        }

    def _describe_measurement_quality(self, score: float) -> str:
        if score >= 0.8:
            return "Gold-standard analytical techniques (X-ray, cryo-EM, ITC)"
        elif score >= 0.6:
            return "Established analytical methods with acceptable precision"
        elif score >= 0.4:
            return "Mixed quality techniques, some uncertainty present"
        else:
            return "High uncertainty techniques or insufficient data"

    def _describe_data_quality(self, score: float) -> str:
        if score >= 0.75:
            return "High purity, consistent across studies, reproducible"
        elif score >= 0.50:
            return "Moderate quality with some variability"
        elif score >= 0.25:
            return "Below average quality, limited reproducibility"
        else:
            return "Poor quality data or significant gaps"

    def _describe_validation_status(self, status: str) -> str:
        return {
            "verified": "Orthogonal experimental confirmation obtained",
            "partial": "Some independent validation, additional recommended",
            "unverified": "No orthogonal validation - in-silico only",
        }.get(status, "Unknown")

    def _generate_recommendations(self, integrity: AnalyticalIntegrity) -> List[str]:
        recs = []
        if integrity.measurement_quality < 0.6:
            recs.append("Consider orthogonal biophysical assay (ITC, SPR)")
        if integrity.data_quality < 0.5:
            recs.append("Cross-check with additional literature sources")
        if integrity.validation_status == "unverified":
            recs.append("Priority: obtain at least 2 orthogonal experimental validations")
        elif integrity.validation_status == "partial":
            recs.append("Confirm activity in disease-relevant functional assay")
        if integrity.integrity_score < 0.4:
            recs.append("LOW confidence: do not advance without additional validation")
        return recs


# Alias for backwards compatibility
AIF = AnalyticalIntegrityFramework


# ============================================================================
# QUICK FACTORY FUNCTIONS
# ============================================================================

def assess_binding_data(
    ki_values: List[float],
    techniques: List[str],
    replicates: Optional[List[int]] = None,
) -> Tuple[UncertaintyResult, AnalyticalIntegrity]:
    """
    Quick assessment of binding affinity data.
    
    Args:
        ki_values: List of Ki/Kd/IC50 values
        techniques: List of technique codes (e.g., ["itc", "spr"])
        replicates: Number of replicates per technique
    
    Returns:
        (UncertaintyResult, AnalyticalIntegrity)
    """
    aif = AnalyticalIntegrityFramework()
    mol_id = "_quick_binding_assessment"

    for i, (val, tech) in enumerate(zip(ki_values, techniques)):
        n_rep = replicates[i] if replicates else 1
        aif.add_assay_record(
            molecule_id=mol_id,
            assay_id=f"assay_{i}",
            technique=MeasurementTechnique.from_code(tech),
            value=val,
            unit="nM",
            replicates=n_rep,
        )

    uncertainty = aif.assess_measurement_uncertainty(mol_id)
    integrity = aif.assess(mol_id)
    return uncertainty, integrity


# ============================================================================
# TESTS
# ============================================================================

def test_bootstrap_ci():
    """Test bootstrap CI calculation"""
    engine = MeasurementUncertaintyEngine(random_seed=42)
    values = [5.2, 5.5, 4.9, 5.1, 5.3, 5.0, 5.4, 5.1, 5.2, 5.3]
    result = engine.bootstrap_ci(values, n_bootstrap=1000)
    assert result.confidence_level in ("high", "medium", "low")
    assert result.ci_lower_95 <= result.point_estimate <= result.ci_upper_95
    print(f"✓ Bootstrap CI: {result.point_estimate:.4f} [{result.ci_lower_95:.4f}, {result.ci_upper_95:.4f}] ({result.confidence_level})")


def test_analytical_integrity_framework():
    """Test the full AIF pipeline"""
    aif = AnalyticalIntegrityFramework()

    # Add assay records
    aif.add_assay_record(
        molecule_id="DRD2_agonist_001",
        assay_id="itc_001",
        technique=MeasurementTechnique.ITC,
        value=45.2,
        unit="nM",
        replicates=3,
        sd=3.1,
    )
    aif.add_assay_record(
        molecule_id="DRD2_agonist_001",
        assay_id="spr_001",
        technique=MeasurementTechnique.SPR,
        value=52.0,
        unit="nM",
        replicates=2,
        sd=5.0,
    )

    # Add validations
    aif.add_validation(
        molecule_id="DRD2_agonist_001",
        experiment_id="exp_001",
        experiment_type="orthogonal_assay",
        status="passed",
        agreement="confirm",
        technique=MeasurementTechnique.ITC,
        evidence_strength=0.85,
    )

    integrity = aif.assess("DRD2_agonist_001")
    assert integrity.integrity_score > 0
    assert integrity.validation_status in ("verified", "partial", "unverified")

    report = aif.summary_report("DRD2_agonist_001")
    print(f"✓ AIF Report: integrity_score={integrity.integrity_score:.3f}, "
          f"validation={integrity.validation_status}")
    return True


def test_pooled_uncertainty():
    """Test pooled uncertainty across techniques"""
    engine = MeasurementUncertaintyEngine()
    records = [
        AssayRecord("a1", MeasurementTechnique.ITC, 10.0, "nM", replicates=3, sd=0.5),
        AssayRecord("a2", MeasurementTechnique.SPR, 12.0, "nM", replicates=2, sd=1.0),
        AssayRecord("a3", MeasurementTechnique.ALPHALISA, 11.5, "nM", replicates=4, sd=1.5),
    ]
    result = engine.pooled_uncertainty(records, technique_weighted=True)
    assert result.point_estimate > 0
    print(f"✓ Pooled uncertainty: {result.point_estimate:.4f} [{result.ci_lower_95:.4f}, {result.ci_upper_95:.4f}]")


def test_data_quality_assessment():
    """Test data quality assessor"""
    assessor = DataQualityAssessor()
    assessment = assessor.comprehensive_assessment(
        consistency_values=[1.2, 1.35, 1.15, 1.28, 1.22],
        replicates=[1.2, 1.18, 1.25],
    )
    assert 0 <= assessment.overall_quality <= 1
    print(f"✓ Data quality: {assessment.overall_quality:.3f} (outlier={assessment.outlier_flag})")


def test_quick_assessment():
    """Test quick factory function"""
    uncertainty, integrity = assess_binding_data(
        ki_values=[45.2, 52.0, 48.5],
        techniques=["itc", "spr", "alphalisa"],
        replicates=[3, 2, 4],
    )
    assert uncertainty.point_estimate > 0
    print(f"✓ Quick assessment: IC50={uncertainty.point_estimate:.2f}nM, integrity={integrity.integrity_score:.3f}")


if __name__ == "__main__":
    print("Testing AnalyticalIntegrityFramework...")
    test_bootstrap_ci()
    test_pooled_uncertainty()
    test_data_quality_assessment()
    test_analytical_integrity_framework()
    test_quick_assessment()
    print("\n✅ All tests passed!")
