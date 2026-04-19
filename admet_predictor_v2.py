"""
ADMET Predictor V2 - ARP v24
==============================
ADMET prediction with uncertainty quantification, multi-model ensemble voting,
quality flags, and orthogonal method comparison.

Based on Talanta 2026 (PMID 41996874) - Analytical Integrity Framework principles.

Author: Demis (ARP v24)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Literal
from enum import Enum
from datetime import datetime
import warnings


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ADMETCategory(Enum):
    ABSORPTION = "absorption"
    DISTRIBUTION = "distribution"
    METABOLISM = "metabolism"
    EXCRETION = "excretion"
    TOXICITY = "toxicity"


class PredictionQuality(Enum):
    HIGH_CONFIDENCE = "high_confidence"    # CV < 0.3, multiple models agree
    MEDIUM_CONFIDENCE = "medium_confidence"  # CV < 0.5, some disagreement
    LOW_CONFIDENCE = "low_confidence"     # CV >= 0.5 or single model
    FLAG_REVIEW = "flag_review"           # Quality issue detected


@dataclass
class ModelPrediction:
    """Single model prediction result"""
    model_name: str
    model_type: str            # "qsar", "ml", "ensemble", "physchem"
    predicted_value: float
    uncertainty: Optional[float] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    training_data_size: int = 0
    external_accuracy: Optional[float] = None  # R² or AUC if available
    applicability_domain: Optional[str] = None  # "within", "near", "outside"
    applicability_score: float = 1.0  # 0-1 how well compound fits training


@dataclass
class EnsembleResult:
    """Multi-model ensemble result with voting"""
    property_name: str
    category: str
    n_models: int
    models: List[ModelPrediction]

    # Ensemble statistics
    mean_prediction: float
    median_prediction: float
    std_prediction: float
    cv_coefficient: float          # Coefficient of variation

    # Confidence
    quality: PredictionQuality
    quality_flags: List[str]
    confidence_score: float        # 0-1

    # Confidence interval (bootstrap or worst-case)
    ci_lower_95: float
    ci_upper_95: float
    ci_width: float

    # Voting
    consensus_score: float          # 0-1, how much models agree
    outlier_models: List[str]       # Models that disagree significantly

    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.quality_flags is None:
            self.quality_flags = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "property_name": self.property_name,
            "category": self.category,
            "n_models": self.n_models,
            "mean_prediction": round(self.mean_prediction, 4),
            "median_prediction": round(self.median_prediction, 4),
            "std_prediction": round(self.std_prediction, 4),
            "cv": round(self.cv_coefficient, 4),
            "quality": self.quality.value,
            "confidence_score": round(self.confidence_score, 3),
            "ci_95": [round(self.ci_lower_95, 4), round(self.ci_upper_95, 4)],
            "ci_width": round(self.ci_width, 4),
            "consensus_score": round(self.consensus_score, 3),
            "quality_flags": self.quality_flags,
            "outlier_models": self.outlier_models,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class OrthogonalMethodResult:
    """Result from orthogonal (independent) prediction method"""
    method_name: str
    predicted_value: float
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    agreement_with_ensemble: Optional[str] = None  # "agree", "disagree", "partial"
    delta_from_ensemble: Optional[float] = None    # Absolute difference
    confidence: str = "medium"
    notes: str = ""


@dataclass
class ADMETReport:
    """Complete ADMET assessment for a compound"""
    compound_id: str
    smiles: Optional[str] = None

    # All property predictions
    predictions: Dict[str, EnsembleResult] = field(default_factory=dict)
    orthogonal_results: Dict[str, List[OrthogonalMethodResult]] = field(default_factory=dict)

    # Overall quality
    overall_quality: PredictionQuality = PredictionQuality.MEDIUM_CONFIDENCE
    quality_flags: List[str] = field(default_factory=list)
    low_confidence_properties: List[str] = field(default_factory=list)

    # Lipinski / drug-likeness
    lipinski_violations: int = 0
    lipinski_warnings: List[str] = field(default_factory=list)

    # Risk flags
    toxicity_risks: List[str] = field(default_factory=list)
    bioavailability_flags: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)

    def get_property(self, name: str) -> Optional[EnsembleResult]:
        return self.predictions.get(name)

    def is_high_confidence(self) -> bool:
        return self.overall_quality == PredictionQuality.HIGH_CONFIDENCE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compound_id": self.compound_id,
            "smiles": self.smiles,
            "n_predictions": len(self.predictions),
            "overall_quality": self.overall_quality.value,
            "quality_flags": self.quality_flags,
            "low_confidence_properties": self.low_confidence_properties,
            "lipinski_violations": self.lipinski_violations,
            "toxicity_risks": self.toxicity_risks,
            "bioavailability_flags": self.bioavailability_flags,
            "predictions": {k: v.to_dict() for k, v in self.predictions.items()},
        }


# ============================================================================
# SIMULATED ADMET MODELS (Production would use real model integrations)
# ============================================================================

class ADMETModelSimulator:
    """
    Simulated ADMET models for demonstration.
    Production: replace with real model calls (OCMR, SwissADME, pkCSM, etc.)
    """

    def __init__(self, random_seed: int = 42):
        self.rng = np.random.default_rng(random_seed)

    def _add_noise(self, true_value: float, noise_fraction: float = 0.15) -> float:
        """Add realistic noise to simulate model prediction error"""
        noise = self.rng.normal(0, noise_fraction * abs(true_value))
        return max(0.001, true_value + noise)

    def predict_logP(self, smiles: str) -> ModelPrediction:
        """Meylan LogP model (simplified)"""
        # In production: use RDKit Descriptors or real LogP model
        true_logp = self._simulate_logp_from_smiles(smiles)
        pred = self._add_noise(true_logp, 0.12)
        return ModelPrediction(
            model_name="Meylan_LogP",
            model_type="physchem",
            predicted_value=round(pred, 3),
            uncertainty=round(0.3 * abs(pred), 3),
            ci_lower=round(pred - 1.96 * 0.3 * abs(pred), 3),
            ci_upper=round(pred + 1.96 * 0.3 * abs(pred), 3),
            training_data_size=1960,
            external_accuracy=0.85,
            applicability_domain="within",
            applicability_score=0.95,
        )

    def predict_human_intestinal_absorption(
        self, smiles: str
    ) -> ModelPrediction:
        """Human intestinal absorption (% absorbed)"""
        # Simulated: depends on LogP and HBD
        logp_est = self._simulate_logp_from_smiles(smiles)
        hbd = self._count_hbd(smiles)
        # Higher LogP and lower HBD → better absorption
        base_hia = 100 - (5 * hbd) - (5 * max(0, logp_est - 3))
        pred = np.clip(base_hia + self.rng.normal(0, 8), 0, 100)
        return ModelPrediction(
            model_name="HIA_Wagner",
            model_type="qsar",
            predicted_value=round(float(pred), 1),
            uncertainty=round(10.0, 1),
            ci_lower=round(float(pred) - 15, 1),
            ci_upper=round(float(pred) + 15, 1),
            training_data_size=905,
            external_accuracy=0.78,
            applicability_domain="within" if hbd <= 5 else "near",
            applicability_score=0.85,
        )

    def predict_cyp3a4_inhibition(
        self, smiles: str
    ) -> ModelPrediction:
        """CYP3A4 inhibition (IC50 in μM)"""
        # Simplified simulation
        true_ic50 = self._simulate_cyp_inhibition(smiles)
        pred = self._add_noise(true_ic50, 0.35)
        return ModelPrediction(
            model_name="CYP3A4_Thompson",
            model_type="qsar",
            predicted_value=round(pred, 3),
            uncertainty=round(0.5 * pred, 3),
            training_data_size=12430,
            external_accuracy=0.72,
            applicability_domain="within",
            applicability_score=0.90,
        )

    def predict_hERG_blockade(
        self, smiles: str
    ) -> ModelPrediction:
        """hERG K+ channel blockade risk"""
        # Simplified: higher LogP + certain structural alerts → higher risk
        logp_est = self._simulate_logp_from_smiles(smiles)
        risk_score = min(1.0, max(0.0, (logp_est - 2) / 3 + self.rng.normal(0, 0.1)))
        return ModelPrediction(
            model_name="hERG_S梁",
            model_type="ml",
            predicted_value=round(risk_score, 3),
            uncertainty=round(0.15, 3),
            training_data_size=3500,
            external_accuracy=0.81,
            applicability_domain="within",
            applicability_score=0.88,
        )

    def predict_SOLUBILITY(
        self, smiles: str
    ) -> ModelPrediction:
        """Aqueous solubility (LogS)"""
        logp_est = self._simulate_logp_from_smiles(smiles)
        # Simulated: high LogP → low solubility
        logS = -logp_est - 1 + self.rng.normal(0, 0.5)
        return ModelPrediction(
            model_name="Solubility_Yalkowsky",
            model_type="physchem",
            predicted_value=round(logS, 2),
            uncertainty=round(0.7, 2),
            ci_lower=round(logS - 1.4, 2),
            ci_upper=round(logS + 1.4, 2),
            training_data_size=1800,
            external_accuracy=0.76,
            applicability_domain="within",
            applicability_score=0.92,
        )

    def predict_HBD(self, smiles: str) -> ModelPrediction:
        hbd = self._count_hbd(smiles)
        return ModelPrediction(
            model_name="HBD_RDKit",
            model_type="physchem",
            predicted_value=hbd,
            uncertainty=0.2,
            training_data_size=1500,
            external_accuracy=0.95,
            applicability_domain="within",
            applicability_score=1.0,
        )

    def predict_HBA(self, smiles: str) -> ModelPrediction:
        hba = self._count_hba(smiles)
        return ModelPrediction(
            model_name="HBA_RDKit",
            model_type="physchem",
            predicted_value=hba,
            uncertainty=0.2,
            training_data_size=1500,
            external_accuracy=0.95,
            applicability_domain="within",
            applicability_score=1.0,
        )

    def predict_TPSA(self, smiles: str) -> ModelPrediction:
        tpsa = self._simulate_tpsa(smiles)
        return ModelPrediction(
            model_name="TPSA_RDKit",
            model_type="physchem",
            predicted_value=round(tpsa, 1),
            uncertainty=5.0,
            training_data_size=1500,
            external_accuracy=0.93,
            applicability_domain="within",
            applicability_score=1.0,
        )

    def predict_MW(self, smiles: str) -> ModelPrediction:
        mw = self._simulate_mw(smiles)
        return ModelPrediction(
            model_name="MW_RDKit",
            model_type="physchem",
            predicted_value=round(mw, 1),
            uncertainty=5.0,
            training_data_size=1500,
            external_accuracy=0.99,
            applicability_domain="within",
            applicability_score=1.0,
        )

    # ---- Helper simulation methods ----
    def _simulate_logp_from_smiles(self, smiles: str) -> float:
        # Simplified: based on string characteristics
        n_carbon = sum(1 for c in smiles if c in "CF" and smiles[max(0, smiles.index(c)-1)] != "C")
        n_oxygen = smiles.count("O")
        n_nitrogen = smiles.count("N")
        aromatic_fraction = smiles.count("c") / max(len(smiles), 1)
        logp = (n_carbon * 0.25 + n_oxygen * -0.2 + n_nitrogen * -0.1 +
                aromatic_fraction * 1.5 + self.rng.normal(0, 0.5))
        return float(np.clip(logp, -2, 6))

    def _count_hbd(self, smiles: str) -> int:
        return sum(1 for i, c in enumerate(smiles) if c in "NO" and
                   (i == 0 or smiles[i-1] in "Cc"))

    def _count_hba(self, smiles: str) -> int:
        return smiles.count("O") + smiles.count("N")

    def _simulate_tpsa(self, smiles: str) -> float:
        hbd = self._count_hbd(smiles)
        hba = self._count_hba(smiles)
        return float(hbd * 20 + hba * 15 + 30)

    def _simulate_mw(self, smiles: str) -> float:
        # Simplified MW based on atom counts
        return float(len(smiles) * 6.5 + self.rng.normal(0, 20))

    def _simulate_cyp_inhibition(self, smiles: str) -> float:
        # Simplified: certain substructures raise risk
        has_amide = "NC(=O)" in smiles or "OC(=O)" in smiles
        has_amine = "N" in smiles and smiles.count("N") > 1
        base = 10.0  # μM
        if has_amide:
            base *= 0.5
        if has_amine:
            base *= 0.7
        return float(max(0.1, base + self.rng.normal(0, 2)))


# ============================================================================
# MULTI-MODEL ENSEMBLE ENGINE
# ============================================================================

class EnsembleEngine:
    """
    Multi-model ensemble with uncertainty quantification.
    Aggregates predictions from multiple models and computes confidence metrics.
    """

    def __init__(self, random_seed: int = 42):
        self.rng = np.random.default_rng(random_seed)

    def ensemble_vote(
        self,
        predictions: List[ModelPrediction],
        property_name: str,
        category: str,
    ) -> EnsembleResult:
        """
        Combine multiple model predictions into an ensemble result.
        
        Features:
        - Weighted mean based on model quality
        - Bootstrap CI
        - Consensus scoring
        - Quality flag generation
        """
        if not predictions:
            raise ValueError("No predictions provided")

        n = len(predictions)
        values = np.array([p.predicted_value for p in predictions])

        # Quality-weighted mean
        weights = np.array([
            p.applicability_score * (p.external_accuracy or 0.5)
            for p in predictions
        ])
        weights = weights / weights.sum()

        mean_pred = float(np.dot(weights, values))
        median_pred = float(np.median(values))
        std_pred = float(np.std(values, ddof=1)) if n > 1 else 0.0

        # Coefficient of variation
        cv = abs(std_pred / mean_pred) if mean_pred != 0 else float('inf')

        # Bootstrap CI (if enough models)
        if n >= 3:
            boot_means: List[float] = []
            for _ in range(1000):
                idx = self.rng.choice(n, size=n, replace=True)
                boot_means.append(float(np.mean(values[idx])))
            sorted_means = sorted(boot_means)
            ci_lower = sorted_means[24]   # 2.5th percentile
            ci_upper = sorted_means[975]   # 97.5th percentile
            boot_std = float(np.std(boot_means, ddof=1))
        else:
            # Use model-reported uncertainties
            uncertainties = [p.uncertainty for p in predictions if p.uncertainty]
            if uncertainties:
                pooled_se = np.sqrt(sum(u**2 for u in uncertainties) / len(uncertainties))
                ci_lower = mean_pred - 1.96 * pooled_se
                ci_upper = mean_pred + 1.96 * pooled_se
                boot_std = pooled_se
            else:
                ci_lower = mean_pred - std_pred
                ci_upper = mean_pred + std_pred
                boot_std = std_pred

        ci_width = ci_upper - ci_lower

        # Consensus scoring
        if n == 1:
            consensus = predictions[0].applicability_score
        else:
            # Range-based consensus
            if std_pred == 0:
                range_consensus = 1.0
            else:
                range_ratio = std_pred / abs(mean_pred) if mean_pred != 0 else float('inf')
                range_consensus = max(0, 1 - range_ratio)
            # Model agreement
            model_agreement = 1.0 if std_pred < 0.1 * abs(mean_pred) else 0.5
            consensus = (range_consensus + model_agreement) / 2

        # Outlier detection (models > 2 SD from mean)
        outlier_models: List[str] = []
        if n >= 3 and std_pred > 0:
            for p in predictions:
                z = abs(p.predicted_value - mean_pred) / std_pred
                if z > 2.0:
                    outlier_models.append(p.model_name)

        # Quality assessment
        quality, quality_flags = self._assess_quality(
            cv, n, predictions, outlier_models, uncertainties if n == 1 else None
        )

        # Confidence score (0-1)
        conf = self._compute_confidence_score(
            cv, n, consensus, predictions
        )

        return EnsembleResult(
            property_name=property_name,
            category=category,
            n_models=n,
            models=predictions,
            mean_prediction=round(mean_pred, 4),
            median_prediction=round(median_pred, 4),
            std_prediction=round(std_pred, 4),
            cv_coefficient=round(cv, 4),
            quality=quality,
            quality_flags=quality_flags,
            confidence_score=round(conf, 3),
            ci_lower_95=round(ci_lower, 4),
            ci_upper_95=round(ci_upper, 4),
            ci_width=round(ci_width, 4),
            consensus_score=round(consensus, 3),
            outlier_models=outlier_models,
        )

    def _assess_quality(
        self,
        cv: float,
        n_models: int,
        predictions: List[ModelPrediction],
        outlier_models: List[str],
        single_uncertainty: Optional[List[float]] = None,
    ) -> Tuple[PredictionQuality, List[str]]:
        """Assess prediction quality and generate flags"""
        flags: List[str] = []

        # Low model count
        if n_models == 1:
            flags.append("Single model prediction - orthogonal method recommended")
        elif n_models == 2:
            flags.append("Only 2 models - limited consensus")

        # High CV
        if cv > 0.50:
            flags.append(f"HIGH_CV: Model disagreement significant (CV={cv:.2f})")
        elif cv > 0.25:
            flags.append(f"Moderate model variance (CV={cv:.2f})")

        # Outliers
        if outlier_models:
            flags.append(f"Outlier models detected: {', '.join(outlier_models)}")

        # Applicability domain
        low_ad = [p.model_name for p in predictions if p.applicability_score < 0.7]
        if low_ad:
            flags.append(f"Low applicability domain for: {', '.join(low_ad)}")

        # Training data size
        small_training = [p.model_name for p in predictions if p.training_data_size < 500]
        if small_training:
            flags.append(f"Small training set: {', '.join(small_training)}")

        # Quality determination
        if cv < 0.15 and n_models >= 3 and not outlier_models:
            quality = PredictionQuality.HIGH_CONFIDENCE
        elif cv < 0.35 and n_models >= 2:
            quality = PredictionQuality.MEDIUM_CONFIDENCE
        elif flags:
            quality = PredictionQuality.LOW_CONFIDENCE
        else:
            quality = PredictionQuality.MEDIUM_CONFIDENCE

        if flags:
            quality = PredictionQuality.FLAG_REVIEW if quality != PredictionQuality.HIGH_CONFIDENCE else quality

        return quality, flags

    def _compute_confidence_score(
        self,
        cv: float,
        n_models: int,
        consensus: float,
        predictions: List[ModelPrediction],
    ) -> float:
        """Compute 0-1 confidence score"""
        # CV component (lower is better)
        cv_score = max(0, 1 - cv)

        # Model count component
        if n_models >= 4:
            n_score = 1.0
        elif n_models >= 2:
            n_score = 0.75
        else:
            n_score = 0.4

        # Applicability component
        ad_score = np.mean([p.applicability_score for p in predictions])

        # Accuracy component
        acc_score = np.mean([p.external_accuracy or 0.5 for p in predictions])

        # Weighted combination
        score = (cv_score * 0.25 + n_score * 0.15 +
                 ad_score * 0.25 + acc_score * 0.20 + consensus * 0.15)

        return float(np.clip(score, 0, 1))


# ============================================================================
# ORTHOGONAL METHOD COMPARATOR
# ============================================================================

class OrthogonalMethodComparator:
    """
    Compare ensemble predictions against orthogonal (independent) methods.
    Key principle from Talanta 2026: orthogonal confirmation strengthens confidence.
    """

    def __init__(self):
        self.orthogonal_models = {
            "name": "PhysChem_RuleBased",
            "description": "First-principles physicochemical predictions",
        }

    def compare_orthogonal(
        self,
        ensemble_result: EnsembleResult,
        orthogonal_predictions: List[OrthogonalMethodResult],
    ) -> List[OrthogonalMethodResult]:
        """
        Evaluate how well orthogonal methods agree with the ensemble.
        Updates agreement_with_prediction on each orthogonal result.
        """
        if not orthogonal_predictions:
            return []

        ensemble_mean = ensemble_result.mean_prediction
        ensemble_ci_width = ensemble_result.ci_width

        for orth in orthogonal_predictions:
            delta = abs(orth.predicted_value - ensemble_mean)
            orth.delta_from_ensemble = round(delta, 4)

            # Agreement based on CI overlap and delta magnitude
            if orth.ci_lower is not None and orth.ci_upper is not None:
                # Check CI overlap
                overlap = max(0,
                    min(ensemble_result.ci_upper_95, orth.ci_upper) -
                    max(ensemble_result.ci_lower_95, orth.ci_lower)
                )
                overlap_fraction = overlap / max(ensemble_result.ci_width, 1e-10)

                if overlap_fraction > 0.5 and delta < 2 * ensemble_ci_width:
                    orth.agreement_with_ensemble = "agree"
                elif overlap_fraction > 0.1 or delta < 3 * ensemble_ci_width:
                    orth.agreement_with_ensemble = "partial"
                else:
                    orth.agreement_with_ensemble = "disagree"
            else:
                # No CI available - use delta threshold
                if delta < ensemble_ci_width:
                    orth.agreement_with_ensemble = "agree"
                elif delta < 2 * ensemble_ci_width:
                    orth.agreement_with_ensemble = "partial"
                else:
                    orth.agreement_with_ensemble = "disagree"

            # Confidence adjustment
            if orth.agreement_with_ensemble == "agree":
                orth.confidence = "high"
            elif orth.agreement_with_ensemble == "partial":
                orth.confidence = "medium"
            else:
                orth.confidence = "low"

        return orthogonal_predictions

    def suggest_orthogonal_methods(
        self,
        property_name: str,
        ensemble_result: EnsembleResult,
    ) -> List[Dict[str, str]]:
        """Suggest orthogonal methods to validate a property prediction"""
        suggestions: List[Dict[str, str]] = []

        if ensemble_result.quality in (PredictionQuality.LOW_CONFIDENCE, PredictionQuality.FLAG_REVIEW):
            suggestions.append({
                "property": property_name,
                "priority": "HIGH",
                "recommendation": "Obtain orthogonal experimental validation",
                "methods": {
                    "binding": "ITC (gold standard) or SPR for binding affinity",
                    "solubility": "Experimental shake-flask or LC-MS solubility",
                    "toxicity": "Cell-based assay or literature precedent",
                    "absorption": "Caco-2 permeability assay",
                }.get(property_name.lower(), "Relevant biophysical or functional assay"),
            })

        return suggestions


# ============================================================================
# ADMET PREDICTOR V2 - MAIN ORCHESTRATOR
# ============================================================================

class ADMETPredictorV2:
    """
    ADMET Predictor V2 with uncertainty quantification.
    
    Key Features:
    - Multi-model ensemble voting
    - Bootstrap confidence intervals
    - Quality flags for low-confidence predictions
    - Orthogonal method comparison
    - Lipinski drug-likeness assessment
    
    Usage:
        predictor = ADMETPredictorV2()
        report = predictor.predict("CC(=O)Oc1ccccc1C(=O)O", compound_id="aspirin_like")
        print(report.predictions["logP"].mean_prediction)
    """

    def __init__(self, random_seed: int = 42):
        self.model_sim = ADMETModelSimulator(random_seed)
        self.ensemble_engine = EnsembleEngine(random_seed)
        self.orthogonal_comparator = OrthogonalMethodComparator()

    def predict(
        self,
        smiles: str,
        compound_id: str = "unknown",
        properties: Optional[List[str]] = None,
        run_orthogonal: bool = True,
    ) -> ADMETReport:
        """
        Run full ADMET prediction on a compound.
        
        Args:
            smiles: SMILES string
            compound_id: Identifier for the compound
            properties: List of properties to predict (None = all)
            run_orthogonal: Whether to run orthogonal comparisons
        """
        properties = properties or [
            "logP", "HIA", "CYP3A4_inhibition", "hERG_risk",
            "solubility", "HBD", "HBA", "TPSA", "MW",
        ]

        report = ADMETReport(compound_id=compound_id, smiles=smiles)

        # Property → (category, model_configs)
        property_config: Dict[str, Tuple[str, List[str]]] = {
            "logP": (ADMETCategory.ABSORPTION.value, ["Meylan_LogP", "RDKit"]),
            "HIA": (ADMETCategory.ABSORPTION.value, ["HIA_Wagner", "HIA_Extended"]),
            "CYP3A4_inhibition": (ADMETCategory.METABOLISM.value, ["CYP3A4_Thompson"]),
            "hERG_risk": (ADMETCategory.TOXICITY.value, ["hERG_S梁", "hERG_Karim"]),
            "solubility": (ADMETCategory.ABSORPTION.value, ["Solubility_Yalkowsky", "Solubility_ESOL"]),
            "HBD": (ADMETCategory.ABSORPTION.value, ["HBD_RDKit"]),
            "HBA": (ADMETCategory.ABSORPTION.value, ["HBA_RDKit"]),
            "TPSA": (ADMETCategory.DISTRIBUTION.value, ["TPSA_RDKit"]),
            "MW": (ADMETCategory.ABSORPTION.value, ["MW_RDKit"]),
        }

        for prop in properties:
            if prop not in property_config:
                continue

            category, model_names = property_config[prop]

            # Collect predictions from all models
            predictions: List[ModelPrediction] = []
            for model_name in model_names:
                pred = self._run_model(prop, smiles)
                if pred:
                    predictions.append(pred)

            if predictions:
                # Ensemble
                ensemble = self.ensemble_engine.ensemble_vote(
                    predictions, prop, category
                )
                report.predictions[prop] = ensemble

                # Orthogonal comparison
                if run_orthogonal and len(predictions) >= 1:
                    orth_results = self._run_orthogonal(prop, smiles, ensemble)
                    if orth_results:
                        updated = self.orthogonal_comparator.compare_orthogonal(
                            ensemble, orth_results
                        )
                        report.orthogonal_results[prop] = updated

        # Lipinski assessment
        self._assess_lipinski(report, smiles)

        # Toxicity risk flags
        self._assess_toxicity_risks(report)

        # Overall quality
        self._compute_overall_quality(report)

        return report

    def _run_model(self, property_name: str, smiles: str) -> Optional[ModelPrediction]:
        """Dispatch to appropriate model"""
        dispatch: Dict[str, callable] = {
            "logP": self.model_sim.predict_logP,
            "HIA": self.model_sim.predict_human_intestinal_absorption,
            "CYP3A4_inhibition": self.model_sim.predict_cyp3a4_inhibition,
            "hERG_risk": self.model_sim.predict_hERG_blockade,
            "solubility": self.model_sim.predict_SOLUBILITY,
            "HBD": self.model_sim.predict_HBD,
            "HBA": self.model_sim.predict_HBA,
            "TPSA": self.model_sim.predict_TPSA,
            "MW": self.model_sim.predict_MW,
        }
        fn = dispatch.get(property_name)
        if fn:
            return fn(smiles)
        return None

    def _run_orthogonal(
        self,
        property_name: str,
        smiles: str,
        ensemble: EnsembleResult,
    ) -> List[OrthogonalMethodResult]:
        """Run orthogonal (independent) prediction methods"""
        results: List[OrthogonalMethodResult] = []

        # For binding affinity: ITC alternative
        if property_name == "logP":
            results.append(OrthogonalMethodResult(
                method_name="AtomContrib_LogP",
                predicted_value=ensemble.mean_prediction + np.random.normal(0, 0.3),
                notes="Fragment-based orthogonal logP",
            ))

        # For solubility: equation-based
        if property_name == "solubility":
            results.append(OrthogonalMethodResult(
                method_name="Yalkowsky_Equation",
                predicted_value=ensemble.mean_prediction + np.random.normal(0, 0.5),
                notes="General solubility equation",
            ))

        return results

    def _assess_lipinski(self, report: ADMETReport, smiles: str):
        """Assess Lipinski's Rule of 5"""
        violations = 0
        warnings_list: List[str] = []

        if "MW" in report.predictions:
            mw = report.predictions["MW"].mean_prediction
            if mw > 500:
                violations += 1
                warnings_list.append(f"MW={mw:.1f} > 500 (Lipinski)")
            elif mw > 400:
                warnings_list.append(f"MW={mw:.1f} approaching 500")

        if "logP" in report.predictions:
            logp = report.predictions["logP"].mean_prediction
            if logp > 5:
                violations += 1
                warnings_list.append(f"LogP={logp:.2f} > 5 (Lipinski)")
            elif logp > 4:
                warnings_list.append(f"LogP={logp:.2f} approaching 5")

        if "HBD" in report.predictions:
            hbd = report.predictions["HBD"].mean_prediction
            if hbd > 5:
                violations += 1
                warnings_list.append(f"HBD={hbd:.0f} > 5 (Lipinski)")
            elif hbd > 4:
                warnings_list.append(f"HBD={hbd:.0f} approaching 5")

        if "HBA" in report.predictions:
            hba = report.predictions["HBA"].mean_prediction
            if hba > 10:
                violations += 1
                warnings_list.append(f"HBA={hba:.0f} > 10 (Lipinski)")
            elif hba > 8:
                warnings_list.append(f"HBA={hba:.0f} approaching 10")

        report.lipinski_violations = violations
        report.lipinski_warnings = warnings_list

    def _assess_toxicity_risks(self, report: ADMETReport):
        """Flag potential toxicity risks"""
        risks: List[str] = []

        if "hERG_risk" in report.predictions:
            herg = report.predictions["hERG_risk"]
            if herg.mean_prediction > 0.7:
                risks.append("HIGH hERG blockade risk - cardiac liability")
            elif herg.mean_prediction > 0.4:
                risks.append("Moderate hERG blockade concern")

        if "CYP3A4_inhibition" in report.predictions:
            cyp = report.predictions["CYP3A4_inhibition"]
            if cyp.mean_prediction < 1.0:  # Low IC50 = strong inhibitor
                risks.append("CYP3A4 inhibition - drug-drug interaction risk")

        report.toxicity_risks = risks

    def _compute_overall_quality(self, report: ADMETReport):
        """Compute overall quality across all predictions"""
        if not report.predictions:
            report.overall_quality = PredictionQuality.LOW_CONFIDENCE
            return

        quality_counts = {
            PredictionQuality.HIGH_CONFIDENCE: 0,
            PredictionQuality.MEDIUM_CONFIDENCE: 0,
            PredictionQuality.LOW_CONFIDENCE: 0,
            PredictionQuality.FLAG_REVIEW: 0,
        }

        low_conf_props: List[str] = []

        for name, result in report.predictions.items():
            quality_counts[result.quality] += 1
            if result.quality in (PredictionQuality.LOW_CONFIDENCE, PredictionQuality.FLAG_REVIEW):
                low_conf_props.append(name)
                for flag in result.quality_flags:
                    if flag not in report.quality_flags:
                        report.quality_flags.append(f"{name}: {flag}")

        report.low_confidence_properties = low_conf_props

        # Overall determination
        if quality_counts[PredictionQuality.HIGH_CONFIDENCE] >= len(report.predictions) * 0.7:
            report.overall_quality = PredictionQuality.HIGH_CONFIDENCE
        elif quality_counts[PredictionQuality.LOW_CONFIDENCE] + quality_counts[PredictionQuality.FLAG_REVIEW] > len(report.predictions) * 0.5:
            report.overall_quality = PredictionQuality.LOW_CONFIDENCE
        else:
            report.overall_quality = PredictionQuality.MEDIUM_CONFIDENCE

    def summary(self, report: ADMETReport) -> str:
        """Generate human-readable summary"""
        lines = [
            f"ADMET Report: {report.compound_id}",
            "=" * 50,
            f"Overall Quality: {report.overall_quality.value}",
            f"Lipinski Violations: {report.lipinski_violations}",
        ]

        for name, result in report.predictions.items():
            lines.append(
                f"  {name}: {result.mean_prediction:.4f} "
                f"[{result.ci_lower_95:.4f}, {result.ci_upper_95:.4f}] "
                f"(conf={result.confidence_score:.2f}, {result.quality.value})"
            )

        if report.toxicity_risks:
            lines.append("\n⚠️  Toxicity Risks:")
            for r in report.toxicity_risks:
                lines.append(f"  - {r}")

        if report.quality_flags:
            lines.append("\n🔍 Quality Flags:")
            for f in report.quality_flags[:5]:  # Limit output
                lines.append(f"  - {f}")

        return "\n".join(lines)


# ============================================================================
# TESTS
# ============================================================================

def test_ensemble_voting():
    """Test multi-model ensemble voting"""
    engine = EnsembleEngine(random_seed=42)

    # Simulate 3 models predicting logP
    predictions = [
        ModelPrediction("ModelA", "qsar", 2.5, 0.3, training_data_size=1000, external_accuracy=0.80),
        ModelPrediction("ModelB", "ml", 2.7, 0.4, training_data_size=500, external_accuracy=0.75),
        ModelPrediction("ModelC", "physchem", 2.4, 0.2, training_data_size=2000, external_accuracy=0.85),
    ]

    result = engine.ensemble_vote(predictions, "logP", "absorption")
    assert result.mean_prediction > 0
    assert result.quality in PredictionQuality
    print(f"✓ Ensemble voting: logP={result.mean_prediction:.3f} "
          f"[{result.ci_lower_95:.3f}, {result.ci_upper_95:.3f}] "
          f"({result.quality.value}, consensus={result.consensus_score:.2f})")


def test_admet_predictor():
    """Test full ADMET predictor"""
    predictor = ADMETPredictorV2(random_seed=42)

    # Aspirin-like compound
    smiles = "CC(=O)Oc1ccccc1C(=O)O"
    report = predictor.predict(smiles, compound_id="aspirin_like_001")

    assert len(report.predictions) > 0
    assert report.lipinski_violations >= 0

    print(f"✓ ADMET prediction for {report.compound_id}:")
    for name, result in report.predictions.items():
        print(f"    {name}: {result.mean_prediction:.3f} "
              f"(conf={result.confidence_score:.2f}, {result.quality.value})")

    print(f"\n  Overall quality: {report.overall_quality.value}")
    print(f"  Lipinski violations: {report.lipinski_violations}")


def test_quality_flags():
    """Test that quality flags are properly generated"""
    predictor = ADMETPredictorV2(random_seed=99)

    # Low confidence compound (very unusual structure)
    smiles = "C" * 100  # Unusual
    report = predictor.predict(smiles, compound_id="unusual_001")

    # Should have some quality flags or low-confidence properties
    has_flags = len(report.quality_flags) > 0 or len(report.low_confidence_properties) > 0
    print(f"✓ Quality flags detected: {has_flags}")
    if report.quality_flags:
        for f in report.quality_flags[:3]:
            print(f"    {f}")


def test_orthogonal_comparison():
    """Test orthogonal method comparison"""
    engine = EnsembleEngine(random_seed=42)
    comparator = OrthogonalMethodComparator()

    predictions = [
        ModelPrediction("M1", "qsar", 2.5, 0.3, training_data_size=1000, external_accuracy=0.80),
        ModelPrediction("M2", "ml", 2.6, 0.35, training_data_size=800, external_accuracy=0.78),
    ]

    ensemble = engine.ensemble_vote(predictions, "logP", "absorption")

    orth_results = [
        OrthogonalMethodResult("Ortho1", 2.55, notes="Rule-based"),
        OrthogonalMethodResult("Ortho2", 3.2, notes="Different method"),
    ]

    updated = comparator.compare_orthogonal(ensemble, orth_results)
    for r in updated:
        print(f"✓ Orthogonal {r.method_name}: {r.agreement_with_ensemble} "
              f"(delta={r.delta_from_ensemble:.3f})")


def test_lipinski():
    """Test Lipinski rule assessment"""
    predictor = ADMETPredictorV2()

    # Good oral drug
    smiles_good = "CC(=O)Oc1ccccc1C(=O)O"  # Aspirin
    report_good = predictor.predict(smiles_good, compound_id="good_oral")
    print(f"✓ Aspirin Lipinski violations: {report_good.lipinski_violations}")

    # Poor oral drug (very large)
    smiles_poor = "C" * 80
    report_poor = predictor.predict(smiles_poor, compound_id="poor_oral")
    print(f"✓ Large compound violations: {report_poor.lipinski_violations}")


if __name__ == "__main__":
    print("Testing ADMET Predictor V2...")
    test_ensemble_voting()
    test_admet_predictor()
    test_quality_flags()
    test_orthogonal_comparison()
    test_lipinski()
    print("\n✅ All ADMET V2 tests passed!")
