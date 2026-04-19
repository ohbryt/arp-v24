"""
Confidence Scorer - ARP v24
===========================
Multi-level confidence (high/medium/low).
Evidence strength scoring.
Data quality weighting.
Final confidence calculation.

Integrates all pipeline modules and produces a unified confidence assessment.

Based on Talanta 2026 (PMID 41996874) - Analytical Integrity Framework.

Author: Demis (ARP v24)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Literal
from enum import Enum
from datetime import datetime


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ConfidenceLevel(Enum):
    """Overall confidence levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

    def __repr__(self) -> str:
        return f"ConfidenceLevel.{self.name}"


class EvidenceStrength(Enum):
    """Evidence strength tiers"""
    STRONG = "strong"       # Multiple orthogonal lines of evidence
    MODERATE = "moderate"  # Some supporting evidence
    WEAK = "weak"          # Limited evidence
    NEGLIGIBLE = "negligible"  # Little to no supporting evidence


@dataclass
class ConfidenceComponent:
    """Individual component contributing to confidence"""
    component_name: str
    score: float           # 0-1 contribution
    weight: float          # How much this matters (0-1)
    evidence_quality: str   # high, medium, low
    description: str
    source_modules: List[str] = field(default_factory=list)  # Where this came from
    raw_data: Dict[str, Any] = field(default_factory=dict)
    caveats: List[str] = field(default_factory=list)

    def weighted_contribution(self) -> float:
        """Score × weight"""
        return self.score * self.weight

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component_name,
            "score": round(self.score, 3),
            "weight": round(self.weight, 3),
            "weighted_contribution": round(self.weighted_contribution(), 3),
            "evidence_quality": self.evidence_quality,
            "description": self.description,
            "source_modules": self.source_modules,
            "caveats": self.caveats,
        }


@dataclass
class ConfidenceScore:
    """
    Unified confidence score integrating all assessment dimensions.
    
    The confidence score is a weighted combination of:
    1. Data Quality (weight: 0.20)
    2. Measurement Quality (weight: 0.20)
    3. Validation Status (weight: 0.25)
    4. Evidence Strength (weight: 0.20)
    5. Consistency (weight: 0.15)
    
    Final score: 0-1, mapped to HIGH (>0.75), MEDIUM (0.45-0.75), LOW (<0.45)
    """
    # Final assessment
    overall_score: float         # 0-1
    confidence_level: str         # high, medium, low, very_low
    confidence_category: str      # descriptive category

    # Component breakdown
    components: List[ConfidenceComponent] = field(default_factory=list)

    # Evidence chain
    evidence_strength: str       # strong, moderate, weak, negligible
    evidence_sources: List[str] = field(default_factory=list)
    conflicting_evidence: List[str] = field(default_factory=list)

    # Quality dimensions (0-1 scale)
    data_quality_score: float = 0.0
    measurement_quality_score: float = 0.0
    validation_quality_score: float = 0.0
    evidence_strength_score: float = 0.0
    consistency_score: float = 0.0

    # Warnings and caveats
    confidence_warnings: List[str] = field(default_factory=list)
    major_caveats: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)

    # Decision support
    recommendation: str = ""      # "advance", "caution", "do_not_advance"
    advancement_criteria_met: bool = False
    criteria_gaps: List[str] = field(default_factory=list)

    # Metadata
    target_id: Optional[str] = None
    molecule_id: Optional[str] = None
    disease: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.confidence_level not in ("high", "medium", "low", "very_low"):
            self._compute_level_from_score()
        if not self.recommendation:
            self._compute_recommendation()

    def _compute_level_from_score(self):
        if self.overall_score >= 0.75:
            self.confidence_level = "high"
        elif self.overall_score >= 0.50:
            self.confidence_level = "medium"
        elif self.overall_score >= 0.25:
            self.confidence_level = "low"
        else:
            self.confidence_level = "very_low"

    def _compute_recommendation(self):
        if self.overall_score >= 0.70 and not self.red_flags:
            self.recommendation = "advance"
            self.advancement_criteria_met = True
        elif self.overall_score >= 0.50 and len(self.red_flags) == 0:
            self.recommendation = "advance_with_monitoring"
            self.advancement_criteria_met = True
        elif self.overall_score >= 0.40 and len(self.red_flags) <= 1:
            self.recommendation = "caution"
            self.advancement_criteria_met = False
        else:
            self.recommendation = "do_not_advance"
            self.advancement_criteria_met = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": round(self.overall_score, 3),
            "confidence_level": self.confidence_level,
            "confidence_category": self.confidence_category,
            "evidence_strength": self.evidence_strength,
            "data_quality_score": round(self.data_quality_score, 3),
            "measurement_quality_score": round(self.measurement_quality_score, 3),
            "validation_quality_score": round(self.validation_quality_score, 3),
            "evidence_strength_score": round(self.evidence_strength_score, 3),
            "consistency_score": round(self.consistency_score, 3),
            "components": [c.to_dict() for c in self.components],
            "recommendation": self.recommendation,
            "advancement_criteria_met": self.advancement_criteria_met,
            "criteria_gaps": self.criteria_gaps,
            "confidence_warnings": self.confidence_warnings,
            "red_flags": self.red_flags,
            "major_caveats": self.major_caveats,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_summary(self) -> str:
        """One-line summary"""
        emoji = {
            "high": "🟢",
            "medium": "🟡",
            "low": "🟠",
            "very_low": "🔴",
        }.get(self.confidence_level, "⚪️")

        return (
            f"{emoji} {self.confidence_level.upper()} confidence "
            f"(score={self.overall_score:.2f}) — {self.recommendation.replace('_', ' ').upper()}"
        )


# ============================================================================
# EVIDENCE STRENGTH CALCULATOR
# ============================================================================

class EvidenceStrengthCalculator:
    """
    Calculates evidence strength based on:
    - Number of independent lines of evidence
    - Quality of each evidence source
    - Consistency across sources
    - Orthogonality
    """

    # Evidence type weights
    EVIDENCE_TYPE_WEIGHTS: Dict[str, float] = {
        "clinical_trial": 1.0,
        "human_study": 0.95,
        "animal_model": 0.60,
        "cell_based": 0.50,
        "biophysical": 0.80,
        "structural": 0.85,
        "computational": 0.30,
        "literature": 0.50,
        "in_silico": 0.20,
    }

    # Evidence quality multipliers
    QUALITY_MULTIPLIERS: Dict[str, float] = {
        "high": 1.0,
        "medium": 0.7,
        "low": 0.4,
        "unknown": 0.3,
    }

    def calculate(
        self,
        evidence_items: List[Dict[str, Any]],
    ) -> Tuple[float, EvidenceStrength, List[str]]:
        """
        Calculate overall evidence strength.
        
        Args:
            evidence_items: List of evidence dicts with keys:
                - type: Evidence type (computational, biophysical, etc.)
                - quality: Quality level (high, medium, low)
                - is_orthogonal: Whether this is orthogonal to other evidence
                - agreement: How well it agrees with other evidence
        
        Returns:
            (strength_score 0-1, EvidenceStrength enum, list of notes)
        """
        if not evidence_items:
            return 0.1, EvidenceStrength.NEGLIGIBLE, ["No evidence provided"]

        scores: List[float] = []
        notes: List[str] = []
        orthogonal_count = 0
        types_seen: Set[str] = set()

        for item in evidence_items:
            ev_type = item.get("type", "unknown")
            quality = item.get("quality", "unknown")
            is_orthogonal = item.get("is_orthogonal", False)
            agreement = item.get("agreement", "unknown")

            # Base score
            base_weight = self.EVIDENCE_TYPE_WEIGHTS.get(ev_type, 0.3)
            quality_mult = self.QUALITY_MULTIPLIERS.get(quality, 0.3)

            # Orthogonality bonus
            ortho_bonus = 0.2 if is_orthogonal else 0.0
            orthogonal_count += 1 if is_orthogonal else 0

            # Agreement penalty
            if agreement == "disagree":
                base_weight *= 0.5
                notes.append(f"{ev_type} shows disagreement")
            elif agreement == "partial":
                base_weight *= 0.8

            item_score = min(base_weight * quality_mult + ortho_bonus, 1.0)
            scores.append(item_score)
            types_seen.add(ev_type)

        # Aggregate
        n_items = len(scores)
        mean_score = float(np.mean(scores))

        # Diversity bonus (multiple independent types)
        diversity_bonus = min(0.15 * (len(types_seen) - 1), 0.30)

        # Orthogonality bonus (if 2+ orthogonal methods)
        ortho_bonus = min(0.2 * (orthogonal_count - 1), 0.4) if orthogonal_count >= 2 else 0.0

        final_score = min(mean_score + diversity_bonus + ortho_bonus, 1.0)

        # Evidence strength
        if final_score >= 0.75:
            strength = EvidenceStrength.STRONG
        elif final_score >= 0.50:
            strength = EvidenceStrength.MODERATE
        elif final_score >= 0.25:
            strength = EvidenceStrength.WEAK
        else:
            strength = EvidenceStrength.NEGLIGIBLE

        return round(final_score, 3), strength, notes

    def calculate_from_confidence_components(
        self,
        components: List[ConfidenceComponent],
    ) -> Tuple[float, EvidenceStrength]:
        """Calculate evidence strength from confidence components"""
        evidence_items = []
        for c in components:
            ev_type = c.source_modules[0] if c.source_modules else "unknown"
            evidence_items.append({
                "type": ev_type,
                "quality": c.evidence_quality,
                "is_orthogonal": len(c.source_modules) > 1,
                "agreement": "confirm" if c.score > 0.6 else "partial",
            })
        score, strength, _ = self.calculate(evidence_items)
        return score, strength


# ============================================================================
# DATA QUALITY WEIGHTING ENGINE
# ============================================================================

class DataQualityWeighter:
    """
    Weights confidence contributions by data quality.
    Implements the Analytical Integrity Spectrum weighting.
    """

    QUALITY_WEIGHTS: Dict[str, float] = {
        "analytical_integrity": 0.20,
        "literature_quality": 0.20,
        "assay_quality": 0.20,
        "validation_status": 0.25,
        "consistency": 0.15,
    }

    def compute_weighted_score(
        self,
        quality_scores: Dict[str, float],
        raw_scores: Dict[str, float],
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute weighted confidence score.
        
        Args:
            quality_scores: Quality of each data source (0-1)
            raw_scores: Raw confidence scores (0-1)
        
        Returns:
            (weighted_score, contributions_by_component)
        """
        contributions: Dict[str, float] = {}
        total_weight = 0.0
        weighted_sum = 0.0

        for component, weight in self.QUALITY_WEIGHTS.items():
            quality = quality_scores.get(component, 0.5)
            raw = raw_scores.get(component, 0.5)

            # Quality-adjusted score = raw * quality
            adjusted = raw * quality
            contribution = adjusted * weight
            contributions[component] = contribution

            weighted_sum += contribution
            total_weight += weight

        # Normalize
        normalized_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return round(normalized_score, 3), contributions

    def quality_gate(
        self,
        quality_scores: Dict[str, float],
        minimum_quality: float = 0.30,
    ) -> Tuple[bool, List[str]]:
        """
        Check if data quality meets minimum standards.
        
        Returns:
            (passes_gate, list of failures)
        """
        failures = []
        for component, weight in self.QUALITY_WEIGHTS.items():
            quality = quality_scores.get(component, 0.0)
            if quality < minimum_quality:
                failures.append(
                    f"{component}: quality={quality:.2f} < threshold={minimum_quality}"
                )
        return len(failures) == 0, failures


# ============================================================================
# CONFIDENCE SCORER - MAIN
# ============================================================================

class ConfidenceScorer:
    """
    Main confidence scoring engine.
    
    Integrates all pipeline modules to produce unified confidence assessment:
    1. Analytical Integrity Framework → measurement quality
    2. ADMET Predictor V2 → ADMET confidence
    3. Literature Integrator V2 → evidence quality
    4. Activity Cliff Detector → SAR cliff warnings
    5. Orthogonal Validator → validation confidence
    
    Usage:
        scorer = ConfidenceScorer()
        scorer.add_component(name="binding", score=0.85, weight=0.3, ...)
        scorer.add_component(name="admet", score=0.70, weight=0.25, ...)
        confidence = scorer.calculate_confidence()
    """

    def __init__(self):
        self.evidence_calculator = EvidenceStrengthCalculator()
        self.quality_weighter = DataQualityWeighter()
        self.components: List[ConfidenceComponent] = []
        self.evidence_items: List[Dict[str, Any]] = []

    def add_component(
        self,
        name: str,
        score: float,
        weight: float,
        quality: str,
        description: str,
        source_modules: Optional[List[str]] = None,
        raw_data: Optional[Dict[str, Any]] = None,
        caveats: Optional[List[str]] = None,
    ) -> ConfidenceComponent:
        """Add a confidence component"""
        component = ConfidenceComponent(
            component_name=name,
            score=float(np.clip(score, 0, 1)),
            weight=float(np.clip(weight, 0, 1)),
            evidence_quality=quality,
            description=description,
            source_modules=source_modules or [],
            raw_data=raw_data or {},
            caveats=caveats or [],
        )
        self.components.append(component)
        return component

    def add_evidence_item(
        self,
        evidence_type: str,
        quality: str,
        is_orthogonal: bool = False,
        agreement: str = "unknown",
        **kwargs,
    ) -> None:
        """Add an evidence item for strength calculation"""
        self.evidence_items.append({
            "type": evidence_type,
            "quality": quality,
            "is_orthogonal": is_orthogonal,
            "agreement": agreement,
            **kwargs,
        })

    def calculate_confidence(
        self,
        target_id: Optional[str] = None,
        molecule_id: Optional[str] = None,
        disease: Optional[str] = None,
    ) -> ConfidenceScore:
        """
        Calculate unified confidence score.
        
        This is the main entry point - call this after adding components.
        """
        if not self.components:
            return ConfidenceScore(
                overall_score=0.1,
                confidence_level="very_low",
                confidence_category="No assessment data",
                evidence_strength=EvidenceStrength.NEGLIGIBLE.value,
                major_caveats=["No confidence components provided"],
                target_id=target_id,
                molecule_id=molecule_id,
                disease=disease,
            )

        # Compute component scores
        component_scores = {c.component_name: c.score for c in self.components}
        component_weights = {c.component_name: c.weight for c in self.components}

        # Weighted sum of component scores
        weighted_sum = sum(c.weighted_contribution() for c in self.components)
        total_weight = sum(c.weight for c in self.components)
        base_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Quality scores
        quality_scores = {c.component_name: c.score * (0.5 if c.evidence_quality == "low" else 1.0)
                         for c in self.components}
        measurement_quality = np.mean([
            c.score for c in self.components
            if "measurement" in c.component_name.lower() or "analytical" in c.component_name.lower()
        ]) if any("measurement" in c.component_name.lower() for c in self.components) else base_score

        validation_quality = np.mean([
            c.score for c in self.components
            if "validation" in c.component_name.lower()
        ]) if any("validation" in c.component_name.lower() for c in self.components) else base_score

        # Evidence strength
        if self.evidence_items:
            ev_score, ev_strength, ev_notes = self.evidence_calculator.calculate(self.evidence_items)
        else:
            ev_score, ev_strength = self.evidence_calculator.calculate_from_confidence_components(
                self.components
            )
            ev_notes = []

        # Consistency score (based on component score variance)
        if len(self.components) >= 2:
            scores = [c.score for c in self.components]
            variance = float(np.var(scores))
            consistency_score = max(0, 1 - variance * 2)
        else:
            consistency_score = base_score

        # Data quality score (average of quality-adjusted components)
        quality_adjusted = []
        for c in self.components:
            q_mult = {"high": 1.0, "medium": 0.75, "low": 0.5, "unknown": 0.4}.get(
                c.evidence_quality, 0.5
            )
            quality_adjusted.append(c.score * q_mult)
        data_quality = float(np.mean(quality_adjusted))

        # Final score combines all factors
        overall = (
            base_score * 0.35 +
            data_quality * 0.20 +
            ev_score * 0.25 +
            consistency_score * 0.10 +
            validation_quality * 0.10
        )
        overall = float(np.clip(overall, 0, 1))

        # Warnings and flags
        warnings = []
        flags = []
        caveats = []

        for c in self.components:
            if c.evidence_quality == "low":
                warnings.append(f"Low-quality evidence for {c.component_name}")
            if c.score < 0.3:
                flags.append(f"Weak evidence: {c.component_name}")
            caveats.extend(c.caveats)

        if consistency_score < 0.5:
            warnings.append("Low consistency across evidence sources")

        if ev_strength == EvidenceStrength.WEAK:
            flags.append("Evidence strength is WEAK")

        # Determine level
        if overall >= 0.75:
            level = "high"
            category = "Strong confidence - well-supported by quality evidence"
        elif overall >= 0.55:
            level = "medium"
            category = "Moderate confidence - some supporting evidence"
        elif overall >= 0.35:
            level = "low"
            category = "Low confidence - limited or inconsistent evidence"
        else:
            level = "very_low"
            category = "Very low confidence - insufficient evidence"

        # Red flags
        red = []
        if any("hERG" in c.component_name and c.score > 0.6 for c in self.components):
            red.append("hERG liability detected")
        if any("activity_cliff" in c.component_name and c.score > 0.5 for c in self.components):
            red.append("Activity cliff detected - SAR may be unreliable")
        if any("conflicting" in str(c.raw_data).lower() for c in self.components):
            red.append("Conflicting evidence detected")

        # Recommendation
        if level == "high" and not red:
            recommendation = "advance"
            criteria_met = True
            gaps = []
        elif level in ("high", "medium") and len(red) == 0:
            recommendation = "advance_with_monitoring"
            criteria_met = True
            gaps = []
        elif level == "medium" and len(red) <= 1:
            recommendation = "caution"
            criteria_met = False
            gaps = ["Consider additional validation"]
        else:
            recommendation = "do_not_advance"
            criteria_met = False
            gaps = ["Insufficient confidence for advancement", "Additional validation required"]

        return ConfidenceScore(
            overall_score=round(overall, 3),
            confidence_level=level,
            confidence_category=category,
            components=self.components,
            evidence_strength=ev_strength.value,
            evidence_sources=list(set(
                m for c in self.components for m in c.source_modules
            )),
            conflicting_evidence=ev_notes,
            data_quality_score=round(data_quality, 3),
            measurement_quality_score=round(measurement_quality, 3),
            validation_quality_score=round(validation_quality, 3),
            evidence_strength_score=round(ev_score, 3),
            consistency_score=round(consistency_score, 3),
            confidence_warnings=warnings,
            major_caveats=caveats[:5],
            red_flags=red,
            recommendation=recommendation,
            advancement_criteria_met=criteria_met,
            criteria_gaps=gaps,
            target_id=target_id,
            molecule_id=molecule_id,
            disease=disease,
        )

    def reset(self):
        """Clear all components and evidence for reuse"""
        self.components = []
        self.evidence_items = []


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================

def integrate_analytical_integrity(
    scorer: ConfidenceScorer,
    integrity_dict: Dict[str, Any],
) -> None:
    """Integrate Analytical Integrity Framework results into confidence scorer"""
    ai_data = integrity_dict.get("analytical_integrity", {})

    # Measurement quality
    mq_score = ai_data.get("measurement_quality", 0.5)
    scorer.add_component(
        name="analytical_integrity_measurement",
        score=mq_score,
        weight=0.20,
        quality="high" if mq_score > 0.7 else "medium" if mq_score > 0.4 else "low",
        description=f"Measurement quality: {ai_data.get('measurement_details', {}).get('n_records', 0)} records",
        source_modules=["analytical_integrity_framework"],
        raw_data=ai_data.get("measurement_details", {}),
    )

    # Data quality
    dq_data = ai_data.get("data_quality_details", {})
    dq_score = dq_data.get("overall_quality", 0.5)
    scorer.add_component(
        name="analytical_integrity_data_quality",
        score=dq_score,
        weight=0.20,
        quality="high" if dq_score > 0.7 else "medium" if dq_score > 0.4 else "low",
        description=f"Data quality: purity={dq_data.get('purity_score', 'N/A')}",
        source_modules=["analytical_integrity_framework"],
        raw_data=dq_data,
    )

    # Validation status
    vs = ai_data.get("validation_status", "unverified")
    vs_score = {"verified": 1.0, "partial": 0.6, "unverified": 0.2}.get(vs, 0.2)
    scorer.add_component(
        name="analytical_integrity_validation",
        score=vs_score,
        weight=0.25,
        quality="high" if vs == "verified" else "medium" if vs == "partial" else "low",
        description=f"Validation status: {vs}",
        source_modules=["analytical_integrity_framework"],
    )


def integrate_admet_results(
    scorer: ConfidenceScorer,
    admet_report: Dict[str, Any],
) -> None:
    """Integrate ADMET Predictor V2 results"""
    pred = admet_report.get("predictions", {})

    if not pred:
        return

    # Overall ADMET quality
    admet_confidence = np.mean([
        r.get("confidence_score", 0.5) for r in pred.values()
    ]) if pred else 0.5

    quality_map = {
        "high_confidence": "high",
        "medium_confidence": "medium",
        "low_confidence": "low",
        "flag_review": "low",
    }

    overall_quality = admet_report.get("overall_quality", "low_confidence")
    q = quality_map.get(overall_quality, "low")

    scorer.add_component(
        name="admet_profile",
        score=admet_confidence,
        weight=0.15,
        quality=q,
        description=f"ADMET quality: {overall_quality}",
        source_modules=["admet_predictor_v2"],
        raw_data={"lipinski_violations": admet_report.get("lipinski_violations", 0)},
    )

    # Toxicity risks
    tox_risks = admet_report.get("toxicity_risks", [])
    if tox_risks:
        tox_score = 1.0 - min(len(tox_risks) * 0.2, 0.8)
        scorer.add_component(
            name="toxicity_risk",
            score=tox_score,
            weight=0.10,
            quality="medium",
            description=f"Toxicity risks: {', '.join(tox_risks[:2])}",
            source_modules=["admet_predictor_v2"],
            caveats=[f"⚠️ {r}" for r in tox_risks],
        )


def integrate_activity_cliff(
    scorer: ConfidenceScorer,
    cliff_summary: Dict[str, Any],
) -> None:
    """Integrate Activity Cliff Detector results"""
    total_cliffs = cliff_summary.get("total_cliffs", 0)
    extreme_cliffs = len(cliff_summary.get("extreme_cliffs", []))

    if total_cliffs == 0:
        # No cliffs = good SAR coverage
        cliff_score = 0.9
        quality = "high"
        desc = "No activity cliffs detected - SAR appears smooth"
    else:
        # Cliffs reduce confidence
        cliff_score = max(0.2, 1.0 - (total_cliffs * 0.1) - (extreme_cliffs * 0.2))
        quality = "low" if extreme_cliffs > 0 else "medium"
        desc = f"{total_cliffs} cliffs detected ({extreme_cliffs} extreme)"

    scorer.add_component(
        name="activity_cliff_sar",
        score=cliff_score,
        weight=0.15,
        quality=quality,
        description=desc,
        source_modules=["activity_cliff_detector"],
        caveats=["⚠️ Activity cliff: SAR may be unreliable at cliff positions"] if total_cliffs > 0 else [],
    )


# ============================================================================
# TESTS
# ============================================================================

def test_confidence_components():
    """Test adding confidence components"""
    scorer = ConfidenceScorer()

    scorer.add_component(
        name="binding_affinity",
        score=0.85,
        weight=0.30,
        quality="high",
        description="Strong binding from ITC and SPR",
        source_modules=["analytical_integrity_framework", "orthogonal_validator"],
    )

    scorer.add_component(
        name="cell_activity",
        score=0.70,
        weight=0.25,
        quality="medium",
        description="Cell assay confirms activity",
        source_modules=["literature_integrator_v2"],
    )

    confidence = scorer.calculate_confidence(target_id="THRB", molecule_id="resmetirom_001", disease="MASLD")
    print(f"✓ Confidence: {confidence.to_summary()}")
    print(f"    Overall: {confidence.overall_score:.3f}")
    print(f"    Level: {confidence.confidence_level}")
    print(f"    Recommendation: {confidence.recommendation}")
    return confidence


def test_evidence_strength():
    """Test evidence strength calculation"""
    calc = EvidenceStrengthCalculator()

    evidence = [
        {"type": "biophysical", "quality": "high", "is_orthogonal": True, "agreement": "confirm"},
        {"type": "structural", "quality": "high", "is_orthogonal": True, "agreement": "confirm"},
        {"type": "cell_based", "quality": "medium", "is_orthogonal": False, "agreement": "confirm"},
        {"type": "computational", "quality": "medium", "is_orthogonal": False, "agreement": "partial"},
    ]

    score, strength, notes = calc.calculate(evidence)
    print(f"✓ Evidence strength: {strength.value} (score={score:.3f})")
    if notes:
        for n in notes:
            print(f"    {n}")


def test_confidence_with_red_flags():
    """Test confidence scoring with red flags"""
    scorer = ConfidenceScorer()

    scorer.add_component(
        name="binding_affinity",
        score=0.80,
        weight=0.30,
        quality="high",
        description="Strong binding",
        source_modules=["analytical_integrity_framework"],
    )

    # Add activity cliff
    scorer.add_component(
        name="activity_cliff_sar",
        score=0.30,
        weight=0.15,
        quality="low",
        description="Major activity cliff detected",
        source_modules=["activity_cliff_detector"],
        raw_data={"extreme_cliffs": 2},
    )

    # Add hERG liability
    scorer.add_component(
        name="herg_liability",
        score=0.75,  # High risk
        weight=0.10,
        quality="medium",
        description="hERG IC50 = 2μM - cardiac risk",
        source_modules=["admet_predictor_v2"],
    )

    confidence = scorer.calculate_confidence()
    print(f"\n✓ Confidence with red flags: {confidence.to_summary()}")
    print(f"    Red flags: {confidence.red_flags}")
    print(f"    Recommendation: {confidence.recommendation}")
    print(f"    Overall: {confidence.overall_score:.3f}")


def test_quality_gate():
    """Test data quality gate"""
    weighter = DataQualityWeighter()

    quality_scores = {
        "analytical_integrity": 0.85,
        "literature_quality": 0.60,
        "assay_quality": 0.45,
        "validation_status": 0.70,
        "consistency": 0.80,
    }

    passes, failures = weighter.quality_gate(quality_scores, minimum_quality=0.30)
    print(f"\n✓ Quality gate: {'PASS' if passes else 'FAIL'}")
    if failures:
        for f in failures:
            print(f"    {f}")


def test_full_integration():
    """Test full integration flow"""
    scorer = ConfidenceScorer()

    # Simulate integrating from all modules
    scorer.add_component(
        name="analytical_integrity",
        score=0.82,
        weight=0.25,
        quality="high",
        description="Three-pillar integrity: verified, high quality",
        source_modules=["analytical_integrity_framework"],
    )

    scorer.add_component(
        name="literature_support",
        score=0.75,
        weight=0.20,
        quality="medium",
        description="Multiple clinical trials support target",
        source_modules=["literature_integrator_v2"],
    )

    scorer.add_component(
        name="admet_profile",
        score=0.68,
        weight=0.15,
        quality="medium",
        description="Acceptable ADMET, 1 Lipinski violation",
        source_modules=["admet_predictor_v2"],
    )

    scorer.add_component(
        name="orthogonal_validation",
        score=0.85,
        weight=0.25,
        quality="high",
        description="ITC and SPR both confirm binding",
        source_modules=["orthogonal_validator"],
    )

    scorer.add_component(
        name="activity_cliff_sar",
        score=0.90,
        weight=0.15,
        quality="high",
        description="Smooth SAR, no major cliffs",
        source_modules=["activity_cliff_detector"],
    )

    confidence = scorer.calculate_confidence(
        target_id="THRB",
        molecule_id="MGL_3196_analog",
        disease="MASLD",
    )

    print(f"\n{'='*60}")
    print(f"FINAL CONFIDENCE ASSESSMENT")
    print(f"{'='*60}")
    print(f"\n{confidence.to_summary()}")
    print(f"\n📊 Score Breakdown:")
    print(f"   Data Quality:    {confidence.data_quality_score:.2f}")
    print(f"   Measurement:     {confidence.measurement_quality_score:.2f}")
    print(f"   Validation:     {confidence.validation_quality_score:.2f}")
    print(f"   Evidence:        {confidence.evidence_strength_score:.2f}")
    print(f"   Consistency:     {confidence.consistency_score:.2f}")
    print(f"\n🔍 Components:")
    for c in confidence.components:
        print(f"   [{c.evidence_quality.upper():6}] {c.component_name}: {c.score:.2f} (w={c.weight})")
    print(f"\n💡 Recommendation: {confidence.recommendation.upper()}")
    if confidence.criteria_gaps:
        print(f"   Gaps: {', '.join(confidence.criteria_gaps)}")

    return confidence


if __name__ == "__main__":
    print("Testing Confidence Scorer...")
    test_evidence_strength()
    test_confidence_components()
    test_quality_gate()
    test_confidence_with_red_flags()
    test_full_integration()
    print("\n✅ All Confidence Scorer tests passed!")
