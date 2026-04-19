"""
ARP v24 Upgraded Orchestrator
=============================

Integrates all new Talanta 2026-inspired modules:
- Analytical Integrity Framework
- ADMET Predictor V2 (with Uncertainty Quantification)
- Literature Integrator V2 (with Analytical Integrity Spectrum)
- Activity Cliff Detector
- Orthogonal Validator
- Confidence Scorer

This orchestrator implements a sequential validation pipeline with
confidence-propagation through all stages.

Author: ARP v24 Team
Created: 2026-04-19
Based on: Talanta 2026 (PMID 41996874)
"""

import json
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Import new modules
from analytical_integrity_framework import (
    AnalyticalIntegrityFramework,
    MeasurementQuality,
    DataQuality,
    ValidationStatus
)
from admet_predictor_v2 import (
    ADMETPredictorV2,
    UncertaintyResult,
    ADMETPrediction
)
from literature_integrator_v2 import (
    LiteratureIntegratorV2,
    SourceCredibility,
    ConflictDetection
)
from activity_cliff_detector import (
    ActivityCliffDetector,
    ActivityCliffAlert,
    SARMolecule
)
from orthogonal_validator import (
    OrthogonalValidator,
    ValidationResult,
    CrossValidationResult
)
from confidence_scorer import (
    ConfidenceScorer,
    ConfidenceLevel,
    EvidenceStrength
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class PipelineStage(Enum):
    """Pipeline stages with confidence propagation"""
    LITERATURE_SEARCH = "literature_search"
    TARGET_ANALYSIS = "target_analysis"
    LITERATURE_INTEGRATION = "literature_integration"
    PHARMACOPHORE_SCREEN = "pharmacophore_screen"
    ADMET_PREDICTION = "admet_prediction"
    ACTIVITY_CLIFF_CHECK = "activity_cliff_check"
    ORTHOGONAL_VALIDATION = "orthogonal_validation"
    CONFIDENCE_SCORING = "confidence_scoring"
    CANDIDATE_RANKING = "candidate_ranking"


@dataclass
class StageResult:
    """Result from each pipeline stage"""
    stage: PipelineStage
    data: Any
    confidence: ConfidenceLevel
    integrity_score: float  # 0-1 from AnalyticalIntegrityFramework
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0


@dataclass
class CandidateCompound:
    """Final candidate with full confidence profile"""
    compound_id: str
    smiles: str
    name: str = ""
    
    # Scores from each stage
    admet_score: float = 0.0
    literature_score: float = 0.0
    pharmacophore_score: float = 0.0
    
    # Uncertainty (from ADMET V2)
    admet_uncertainty: Optional[UncertaintyResult] = None
    
    # Integrity (from Analytical Framework)
    integrity: Optional[object] = None
    
    # Activity cliffs
    activity_cliff: Optional[ActivityCliffAlert] = None
    
    # Validation
    orthogonal_validation: Optional[ValidationResult] = None
    
    # Overall confidence
    overall_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    evidence_strength: EvidenceStrength = EvidenceStrength.MODERATE
    
    # Final composite score
    composite_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "compound_id": self.compound_id,
            "name": self.name,
            "smiles": self.smiles,
            "admet_score": self.admet_score,
            "literature_score": self.literature_score,
            "pharmacophore_score": self.pharmacophore_score,
            "overall_confidence": self.overall_confidence.value,
            "evidence_strength": self.evidence_strength.value,
            "composite_score": self.composite_score,
            "has_activity_cliff": self.activity_cliff.detected if self.activity_cliff else False,
            "orthogonal_validated": self.orthogonal_validation.passed if self.orthogonal_validation else False
        }


@dataclass
class PipelineReport:
    """Final pipeline report with uncertainty"""
    pipeline_version: str = "2.0"
    created_at: str = ""
    disease_area: str = ""
    target: str = ""
    
    # Stage results
    stage_results: List[StageResult] = field(default_factory=list)
    
    # Candidates
    candidates: List[CandidateCompound] = field(default_factory=list)
    
    # Overall metrics
    total_compounds_analyzed: int = 0
    high_confidence_candidates: int = 0
    medium_confidence_candidates: int = 0
    low_confidence_candidates: int = 0
    
    # Integrity summary
    avg_integrity_score: float = 0.0
    verified_count: int = 0
    partial_count: int = 0
    unverified_count: int = 0
    
    # Activity cliff summary
    cliffs_detected: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "pipeline_version": self.pipeline_version,
            "created_at": self.created_at,
            "disease_area": self.disease_area,
            "target": self.target,
            "total_compounds": self.total_compounds_analyzed,
            "high_confidence": self.high_confidence_candidates,
            "medium_confidence": self.medium_confidence_candidates,
            "low_confidence": self.low_confidence_candidates,
            "avg_integrity_score": self.avg_integrity_score,
            "verified": self.verified_count,
            "partial": self.partial_count,
            "unverified": self.unverified_count,
            "cliffs_detected": self.cliffs_detected,
            "candidates": [c.to_dict() for c in self.candidates]
        }


# ============================================================================
# UPGRADED ORCHESTRATOR
# ============================================================================

class ARP24UpgradedOrchestrator:
    """
    ARP v24 Upgraded Orchestrator with Talanta 2026-inspired enhancements.
    
    Key Features:
    - Analytical Integrity Framework integration
    - Uncertainty quantification throughout
    - Activity cliff detection
    - Orthogonal validation
    - Multi-level confidence scoring
    - Sequential validation pipeline
    """
    
    def __init__(self, disease_area: str = "", target: str = ""):
        """Initialize orchestrator with disease area and target"""
        self.disease_area = disease_area
        self.target = target
        
        # Initialize all modules
        self.analytical_framework = AnalyticalIntegrityFramework()
        self.admet_v2 = ADMETPredictorV2()
        self.literature_v2 = LiteratureIntegratorV2()
        self.activity_cliff = ActivityCliffDetector()
        self.orthogonal_validator = OrthogonalValidator()
        self.confidence_scorer = ConfidenceScorer()
        
        # Pipeline config
        self.config = {
            "min_confidence_for_candidate": ConfidenceLevel.MEDIUM,
            "min_integrity_score": 0.5,
            "bootstrap_iterations": 100,
            "activity_cliff_threshold": 1.5,  # log units
            "orthogonal_methods_required": 2
        }
        
        self.stage_results: List[StageResult] = []
    
    async def run_pipeline(self, 
                          smiles_list: List[str],
                          disease_area: str = "",
                          target: str = "",
                          literature_queries: List[str] = None) -> PipelineReport:
        """
        Run the complete upgraded pipeline.
        
        Args:
            smiles_list: List of compound SMILES to analyze
            disease_area: Disease area (e.g., "sarcopenia", "MASLD")
            target: Target protein (e.g., "PDK4", "FOXO1")
            literature_queries: Queries for literature search
            
        Returns:
            PipelineReport with all results and confidence profiles
        """
        print("=" * 70)
        print("ARP v24 UPGRADED PIPELINE (Talanta 2026 Enhanced)")
        print("=" * 70)
        print(f"Disease: {disease_area or self.disease_area}")
        print(f"Target: {target or self.target}")
        print(f"Compounds: {len(smiles_list)}")
        print("=" * 70)
        
        # Initialize report
        report = PipelineReport(
            created_at=datetime.now().isoformat(),
            disease_area=disease_area or self.disease_area,
            target=target or self.target
        )
        
        # ===== STAGE 1: Literature Search =====
        print("\n[Stage 1/8] Literature Search...")
        stage1_result = await self._stage_literature_search(literature_queries or [f"{target or disease_area} treatment"])
        self.stage_results.append(stage1_result)
        report.stage_results.append(stage1_result)
        
        # ===== STAGE 2: Literature Integration with Analytical Integrity =====
        print("\n[Stage 2/8] Literature Integration (Analytical Integrity Spectrum)...")
        stage2_result = await self._stage_literature_integration(stage1_result)
        self.stage_results.append(stage2_result)
        report.stage_results.append(stage2_result)
        
        # ===== STAGE 3: ADMET Prediction with Uncertainty =====
        print("\n[Stage 3/8] ADMET Prediction (Uncertainty Quantification)...")
        admet_results = []
        for smiles in smiles_list:
            result = await self._stage_admet_prediction(smiles)
            admet_results.append(result)
        report.stage_results.append(StageResult(
            stage=PipelineStage.ADMET_PREDICTION,
            data=admet_results,
            confidence=self._aggregate_confidence([r.confidence for r in admet_results]),
            integrity_score=sum(r.integrity.integrity_score for r in admet_results) / len(admet_results) if admet_results else 0
        ))
        
        # ===== STAGE 4: Activity Cliff Detection =====
        print("\n[Stage 4/8] Activity Cliff Detection...")
        cliff_results = await self._stage_activity_cliff_check(smiles_list)
        report.stage_results.append(StageResult(
            stage=PipelineStage.ACTIVITY_CLIFF_CHECK,
            data=cliff_results,
            confidence=self._aggregate_confidence([r.confidence for r in cliff_results]),
            integrity_score=sum(r.integrity_score for r in cliff_results) / len(cliff_results) if cliff_results else 1.0
        ))
        report.cliffs_detected = sum(1 for r in cliff_results if r.detected)
        
        # ===== STAGE 5: Orthogonal Validation =====
        print("\n[Stage 5/8] Orthogonal Validation...")
        validation_results = await self._stage_orthogonal_validation(admet_results)
        report.stage_results.append(StageResult(
            stage=PipelineStage.ORTHOGONAL_VALIDATION,
            data=validation_results,
            confidence=self._aggregate_confidence([r.confidence for r in validation_results]),
            integrity_score=sum(r.integrity.integrity_score for r in validation_results) / len(validation_results) if validation_results else 0
        ))
        
        # ===== STAGE 6: Confidence Scoring =====
        print("\n[Stage 6/8] Confidence Scoring...")
        candidates = await self._stage_confidence_scoring(
            smiles_list, admet_results, cliff_results, validation_results, stage2_result
        )
        report.candidates = candidates
        
        # ===== STAGE 7: Candidate Ranking =====
        print("\n[Stage 7/8] Candidate Ranking...")
        ranked_candidates = await self._stage_candidate_ranking(candidates)
        report.candidates = ranked_candidates
        
        # ===== STAGE 8: Report Generation =====
        print("\n[Stage 8/8] Report Generation...")
        report = self._generate_report(report, candidates)
        
        # Print summary
        self._print_summary(report)
        
        return report
    
    async def _stage_literature_search(self, queries: List[str]) -> StageResult:
        """Stage 1: Literature search"""
        start = asyncio.get_event_loop().time()
        
        try:
            # Use literature integrator v2
            results = await asyncio.get_event_loop().run_in_executor(
                None,
                self.literature_v2.search_and_integrate,
                queries
            )
            
            confidence = ConfidenceLevel.HIGH if len(results.get("sources", [])) > 5 else ConfidenceLevel.MEDIUM
            integrity = self.analytical_framework.assess_integrity(
                source_types=["pubmed", "clinical_trial"] if len(results.get("sources", [])) > 3 else ["pubmed"]
            )
            
            return StageResult(
                stage=PipelineStage.LITERATURE_SEARCH,
                data=results,
                confidence=confidence,
                integrity_score=integrity.integrity_score,
                metadata={"query_count": len(queries), "result_count": len(results.get("sources", []))}
            )
        except Exception as e:
            return StageResult(
                stage=PipelineStage.LITERATURE_SEARCH,
                data={},
                confidence=ConfidenceLevel.LOW,
                integrity_score=0.0,
                errors=[str(e)]
            )
    
    async def _stage_literature_integration(self, prev_result: StageResult) -> StageResult:
        """Stage 2: Literature integration with Analytical Integrity Spectrum"""
        start = asyncio.get_event_loop().time()
        
        try:
            data = prev_result.data
            conflicts = self.literature_v2.detect_conflicts(data.get("claims", []))
            
            confidence = ConfidenceLevel.HIGH if len(conflicts) == 0 else ConfidenceLevel.MEDIUM
            integrity = self.analytical_framework.assess_integrity(
                source_types=data.get("source_types", ["pubmed"])
            )
            
            return StageResult(
                stage=PipelineStage.LITERATURE_INTEGRATION,
                data={"conflicts": conflicts, "integrated_data": data},
                confidence=confidence,
                integrity_score=integrity.integrity_score,
                warnings=[f"Conflict detected: {c}" for c in conflicts[:3]] if conflicts else []
            )
        except Exception as e:
            return StageResult(
                stage=PipelineStage.LITERATURE_INTEGRATION,
                data={},
                confidence=ConfidenceLevel.LOW,
                integrity_score=0.0,
                errors=[str(e)]
            )
    
    async def _stage_admet_prediction(self, smiles: str) -> ADMETPrediction:
        """Stage 3: ADMET prediction with uncertainty quantification"""
        try:
            # Run ADMET V2 with uncertainty
            result = self.admet_v2.predict_with_uncertainty(smiles)
            
            # Assess integrity
            integrity = self.analytical_framework.assess_integrity(
                source_types=["admet_predictor", "ensemble"]
            )
            
            result.integrity = integrity
            result.confidence = self._calculate_admet_confidence(result)
            
            return result
        except Exception as e:
            return ADMETPrediction(
                smiles=smiles,
                error=str(e),
                confidence=ConfidenceLevel.LOW
            )
    
    async def _stage_activity_cliff_check(self, smiles_list: List[str]) -> List[ActivityCliffAlert]:
        """Stage 4: Activity cliff detection"""
        alerts = []
        
        try:
            molecules = [SARMolecule(smiles=s, compound_id=str(i)) for i, s in enumerate(smiles_list)]
            alerts = self.activity_cliff.detect_cliffs(molecules)
        except Exception as e:
            print(f"Activity cliff detection error: {e}")
        
        return alerts
    
    async def _stage_orthogonal_validation(self, admet_results: List[ADMETPrediction]) -> List[ValidationResult]:
        """Stage 5: Orthogonal validation"""
        results = []
        
        for result in admet_results:
            if result.error:
                continue
                
            try:
                # Cross-validate between methods
                cross_result = self.orthogonal_validator.cross_validate(
                    primary_prediction=result.to_dict(),
                    alternative_predictions=[]  # Would include multiple method results
                )
                results.append(cross_result)
            except Exception as e:
                print(f"Orthogonal validation error: {e}")
        
        return results
    
    async def _stage_confidence_scoring(self, 
                                        smiles_list: List[str],
                                        admet_results: List[ADMETPrediction],
                                        cliff_results: List[ActivityCliffAlert],
                                        validation_results: List[ValidationResult],
                                        literature_result: StageResult) -> List[CandidateCompound]:
        """Stage 6: Calculate confidence scores for all candidates"""
        candidates = []
        
        for i, smiles in enumerate(smiles_list):
            compound = CandidateCompound(
                compound_id=f"CAND_{i+1:03d}",
                smiles=smiles
            )
            
            # ADMET score and uncertainty
            if i < len(admet_results):
                admet = admet_results[i]
                compound.admet_score = admet.composite_score if not admet.error else 0
                compound.admet_uncertainty = admet.uncertainty
            
            # Literature score
            compound.literature_score = literature_result.data.get("score", 0.5)
            
            # Activity cliff
            if i < len(cliff_results):
                compound.activity_cliff = cliff_results[i]
            
            # Orthogonal validation
            if i < len(validation_results):
                compound.orthogonal_validation = validation_results[i]
            
            # Overall confidence
            compound = self.confidence_scorer.calculate_overall_confidence(compound)
            
            candidates.append(compound)
        
        return candidates
    
    async def _stage_candidate_ranking(self, candidates: List[CandidateCompound]) -> List[CandidateCompound]:
        """Stage 7: Rank candidates by composite score"""
        # Calculate composite score incorporating confidence and uncertainty
        for c in candidates:
            # Base score from ADMET
            score = c.admet_score * 0.4 + c.literature_score * 0.3 + c.pharmacophore_score * 0.3
            
            # Penalize for activity cliffs
            if c.activity_cliff and c.activity_cliff.detected:
                score *= 0.7
            
            # Penalize for low confidence
            if c.overall_confidence == ConfidenceLevel.LOW:
                score *= 0.5
            elif c.overall_confidence == ConfidenceLevel.MEDIUM:
                score *= 0.8
            
            # Incorporate uncertainty penalty
            if c.admet_uncertainty:
                ci_width = c.admet_uncertainty.ci_upper_95 - c.admet_uncertainty.ci_lower_95
                uncertainty_penalty = min(1.0, ci_width / 2)  # Wider CI = more penalty
                score *= (1 - uncertainty_penalty * 0.3)
            
            c.composite_score = round(score, 4)
        
        # Sort by composite score
        candidates.sort(key=lambda x: x.composite_score, reverse=True)
        
        return candidates
    
    def _generate_report(self, report: PipelineReport, candidates: List[CandidateCompound]) -> PipelineReport:
        """Generate final report"""
        report.candidates = candidates
        report.total_compounds_analyzed = len(candidates)
        
        # Count confidence levels
        for c in candidates:
            if c.overall_confidence == ConfidenceLevel.HIGH:
                report.high_confidence_candidates += 1
            elif c.overall_confidence == ConfidenceLevel.MEDIUM:
                report.medium_confidence_candidates += 1
            else:
                report.low_confidence_candidates += 1
        
        # Integrity stats
        integrity_scores = [s.integrity_score for s in self.stage_results if s.integrity_score > 0]
        report.avg_integrity_score = sum(integrity_scores) / len(integrity_scores) if integrity_scores else 0
        
        for s in self.stage_results:
            if hasattr(s.data, 'get') and s.data.get('integrity'):
                status = s.data['integrity'].validation_status
                if status == ValidationStatus.VERIFIED:
                    report.verified_count += 1
                elif status == ValidationStatus.PARTIAL:
                    report.partial_count += 1
                else:
                    report.unverified_count += 1
        
        return report
    
    def _print_summary(self, report: PipelineReport):
        """Print pipeline summary"""
        print("\n" + "=" * 70)
        print("PIPELINE EXECUTION SUMMARY")
        print("=" * 70)
        print(f"Total compounds: {report.total_compounds_analyzed}")
        print(f"\nConfidence Distribution:")
        print(f"  HIGH:   {report.high_confidence_candidates}")
        print(f"  MEDIUM: {report.medium_confidence_candidates}")
        print(f"  LOW:    {report.low_confidence_candidates}")
        print(f"\nAnalytical Integrity:")
        print(f"  Average Score: {report.avg_integrity_score:.3f}")
        print(f"  Verified: {report.verified_count}")
        print(f"  Partial:  {report.partial_count}")
        print(f"  Unverified: {report.unverified_count}")
        print(f"\nActivity Cliffs Detected: {report.cliffs_detected}")
        print("\nTop 5 Candidates:")
        for i, c in enumerate(report.candidates[:5], 1):
            print(f"  {i}. {c.compound_id} (Score: {c.composite_score:.4f}, "
                  f"Confidence: {c.overall_confidence.value}, "
                  f"Cliff: {'YES' if c.activity_cliff and c.activity_cliff.detected else 'NO'})")
        print("=" * 70)
    
    def _aggregate_confidence(self, confidences: List[ConfidenceLevel]) -> ConfidenceLevel:
        """Aggregate multiple confidence levels"""
        if not confidences:
            return ConfidenceLevel.LOW
        
        high_count = sum(1 for c in confidences if c == ConfidenceLevel.HIGH)
        medium_count = sum(1 for c in confidences if c == ConfidenceLevel.MEDIUM)
        
        if high_count == len(confidences):
            return ConfidenceLevel.HIGH
        elif high_count + medium_count == len(confidences):
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _calculate_admet_confidence(self, result: ADMETPrediction) -> ConfidenceLevel:
        """Calculate confidence for ADMET prediction"""
        if result.error:
            return ConfidenceLevel.LOW
        
        # Check uncertainty width
        if result.uncertainty:
            ci_width = result.uncertainty.ci_upper_95 - result.uncertainty.ci_lower_95
            if ci_width < 0.5 and result.uncertainty.confidence_level == "high":
                return ConfidenceLevel.HIGH
            elif ci_width < 1.0:
                return ConfidenceLevel.MEDIUM
            else:
                return ConfidenceLevel.LOW
        
        return ConfidenceLevel.MEDIUM


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Example usage of the upgraded orchestrator"""
    
    # Example compounds
    example_smiles = [
        "CC(=O)Oc1ccccc1C(=O)O",  # Aspirin
        "Cn1cnc2c1c(=O)n(c(=O)n2C)C",  # Caffeine
        "CC(C)CC(C)C(=O)O",  # Ibuprofen-like
    ]
    
    # Run pipeline
    orchestrator = ARP24UpgradedOrchestrator(
        disease_area="sarcopenia",
        target="PDK4"
    )
    
    report = await orchestrator.run_pipeline(
        smiles_list=example_smiles,
        disease_area="Sarcopenia",
        target="PDK4",
        literature_queries=["PDK4 inhibitors sarcopenia", "muscle atrophy treatment"]
    )
    
    # Output JSON report
    print("\nJSON Report:")
    print(json.dumps(report.to_dict(), indent=2))
    
    return report


if __name__ == "__main__":
    asyncio.run(main())
