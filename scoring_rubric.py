"""
ARP Scoring Rubric
==================
100-point scoring system inspired by BioDesignBench evaluation.

Based on BioDesignBench findings:
- "Evaluation depth per candidate correlates with total score at ρ = 0.685"
- Top-tier LLMs beat hardcoded pipeline (60.4 vs 54.2)

Usage:
    from scoring_rubric import score_candidate, format_score_report
    result = score_candidate(candidate, metrics)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class ScoreGrade(Enum):
    """Letter grades based on total score"""
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
    
    @classmethod
    def from_score(cls, score: float) -> "ScoreGrade":
        if score >= 90: return cls.A_PLUS
        elif score >= 80: return cls.A
        elif score >= 70: return cls.B_PLUS
        elif score >= 60: return cls.B
        elif score >= 50: return cls.C
        elif score >= 40: return cls.D
        else: return cls.F


@dataclass
class RubricScore:
    """Individual rubric score breakdown"""
    # Approach (20 pts)
    literature_grounding: float = 0.0
    hypothesis_soundness: float = 0.0
    experimental_design: float = 0.0
    
    # Orchestration (20 pts)
    tool_usage_efficiency: float = 0.0
    iteration_depth: float = 0.0  # BioDesignBench: 14% baseline → target 80%+
    error_recovery: float = 0.0
    
    # Quality (30 pts)
    binding_affinity: float = 0.0
    selectivity: float = 0.0
    admet_profile: float = 0.0
    
    # Impact (30 pts)
    novelty: float = 0.0
    clinical_relevance: float = 0.0
    combinability: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "literature_grounding": self.literature_grounding,
            "hypothesis_soundness": self.hypothesis_soundness,
            "experimental_design": self.experimental_design,
            "tool_usage_efficiency": self.tool_usage_efficiency,
            "iteration_depth": self.iteration_depth,
            "error_recovery": self.error_recovery,
            "binding_affinity": self.binding_affinity,
            "selectivity": self.selectivity,
            "admet_profile": self.admet_profile,
            "novelty": self.novelty,
            "clinical_relevance": self.clinical_relevance,
            "combinability": self.combinability
        }


@dataclass
class ScoreResult:
    """Complete score result with breakdown"""
    total: float
    grade: str
    breakdown: RubricScore
    
    # Category totals
    approach_score: float = 0.0
    orchestration_score: float = 0.0
    quality_score: float = 0.0
    impact_score: float = 0.0
    
    # Detailed feedback
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "grade": self.grade,
            "approach_score": self.approach_score,
            "orchestration_score": self.orchestration_score,
            "quality_score": self.quality_score,
            "impact_score": self.impact_score,
            "breakdown": self.breakdown.to_dict(),
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations
        }


# Rubric configuration (based on BioDesignBench 100-point system)
RUBRIC_CONFIG = {
    "approach": {
        "max_points": 20,
        "literature_grounding": {"max": 8, "desc": "PMID count, citation quality"},
        "hypothesis_soundness": {"max": 6, "desc": "Scientific rationale, mechanism clarity"},
        "experimental_design": {"max": 6, "desc": "Methodology soundness"}
    },
    "orchestration": {
        "max_points": 20,
        "tool_usage_efficiency": {"max": 10, "desc": "Right tool for right job"},
        "iteration_depth": {"max": 7, "desc": "Deep evaluation (14% → 80%+)"},
        "error_recovery": {"max": 3, "desc": "Failure policy execution"}
    },
    "quality": {
        "max_points": 30,
        "binding_affinity": {"max": 10, "desc": "nM potency"},
        "selectivity": {"max": 10, "desc": "Off-target selectivity ratio"},
        "admet_profile": {"max": 10, "desc": "Drug-like properties"}
    },
    "impact": {
        "max_points": 30,
        "novelty": {"max": 10, "desc": "First-in-class potential"},
        "clinical_relevance": {"max": 10, "desc": "Disease relevance, unmet need"},
        "combinability": {"max": 10, "desc": "Synergy potential, combination therapy"}
    }
}


def score_candidate(
    candidate: Dict,
    metrics: Optional[Dict] = None,
    context: Optional[Dict] = None
) -> ScoreResult:
    """
    Calculate 100-point score based on BioDesignBench rubric.
    
    Args:
        candidate: Candidate dict with name, smiles, target, etc.
        metrics: Optional dict with biophysical metrics
        context: Optional dict with disease, literature references, etc.
    
    Returns:
        ScoreResult with total, grade, breakdown
    """
    metrics = metrics or {}
    context = context or {}
    
    rubric = RubricScore()
    strengths = []
    weaknesses = []
    recommendations = []
    
    # ============================================
    # APPROACH (20 pts)
    # ============================================
    
    # Literature grounding (0-8 pts)
    pmid_count = len(context.get("pmids", []))
    if pmid_count >= 10:
        rubric.literature_grounding = 8.0
        strengths.append("Strong literature support")
    elif pmid_count >= 5:
        rubric.literature_grounding = 6.0
    elif pmid_count >= 2:
        rubric.literature_grounding = 4.0
    else:
        rubric.literature_grounding = 2.0
        weaknesses.append("Limited literature support")
    
    # Hypothesis soundness (0-6 pts)
    hypothesis = candidate.get("hypothesis_score", 0.5)
    rubric.hypothesis_soundness = hypothesis * 6
    if hypothesis >= 0.8:
        strengths.append("Strong mechanistic hypothesis")
    
    # Experimental design (0-6 pts)
    design = candidate.get("design_score", 0.5)
    rubric.experimental_design = design * 6
    if design >= 0.8:
        strengths.append("Rigorous experimental design")
    
    approach_score = rubric.literature_grounding + rubric.hypothesis_soundness + rubric.experimental_design
    
    # ============================================
    # ORCHESTRATION (20 pts)
    # ============================================
    
    # Tool usage efficiency (0-10 pts)
    tools_used = candidate.get("tools_used", [])
    tool_count = len(tools_used)
    if tool_count >= 5:
        rubric.tool_usage_efficiency = 10.0
    elif tool_count >= 3:
        rubric.tool_usage_efficiency = 7.0
    elif tool_count >= 2:
        rubric.tool_usage_efficiency = 5.0
    else:
        rubric.tool_usage_efficiency = 3.0
    
    # Iteration depth (0-7 pts)
    # BioDesignBench: "Evaluation depth per candidate correlates with score at ρ = 0.685"
    # Current agents: 14% depth. Target: 80%+
    eval_depth = candidate.get("evaluation_depth", 0.14)  # 14% baseline
    rubric.iteration_depth = min(eval_depth, 1.0) * 7  # Scale to 0-7
    
    if eval_depth >= 0.8:
        strengths.append("Expert-level evaluation depth")
    elif eval_depth < 0.3:
        weaknesses.append("Shallow evaluation - need iterative depth")
        recommendations.append("Add multi-candidate iterative screening")
    
    # Error recovery (0-3 pts)
    recovery = candidate.get("recovery_score", 0.5)
    rubric.error_recovery = recovery * 3
    
    orchestration_score = rubric.tool_usage_efficiency + rubric.iteration_depth + rubric.error_recovery
    
    # ============================================
    # QUALITY (30 pts)
    # ============================================
    
    # Binding affinity (0-10 pts)
    ic50 = candidate.get("ic50_nM", float('inf'))
    if ic50 < 50:
        rubric.binding_affinity = 10.0
        strengths.append(f"Excellent potency: {ic50} nM")
    elif ic50 < 200:
        rubric.binding_affinity = 8.0
    elif ic50 < 500:
        rubric.binding_affinity = 6.0
    elif ic50 < 1000:
        rubric.binding_affinity = 4.0
    else:
        rubric.binding_affinity = 2.0
        weaknesses.append(f"Weak potency: {ic50} nM")
    
    # Selectivity (0-10 pts)
    selectivity = candidate.get("selectivity_ratio", 1.0)
    if selectivity >= 50:
        rubric.selectivity = 10.0
    elif selectivity >= 30:
        rubric.selectivity = 8.0
        strengths.append(f"High selectivity: {selectivity}x")
    elif selectivity >= 10:
        rubric.selectivity = 6.0
    elif selectivity >= 3:
        rubric.selectivity = 4.0
    else:
        rubric.selectivity = 2.0
        weaknesses.append(f"Low selectivity: {selectivity}x")
    
    # ADMET profile (0-10 pts)
    admet_score = candidate.get("admet_score", 0.5)
    rubric.admet_profile = admet_score * 10
    if admet_score >= 0.8:
        strengths.append("Excellent ADMET profile")
    elif admet_score < 0.4:
        weaknesses.append("Suboptimal ADMET")
        recommendations.append("Improve solubility/metabolic stability")
    
    quality_score = rubric.binding_affinity + rubric.selectivity + rubric.admet_profile
    
    # ============================================
    # IMPACT (30 pts)
    # ============================================
    
    # Novelty (0-10 pts)
    novelty = candidate.get("novelty_score", 0.5)
    rubric.novelty = novelty * 10
    if novelty >= 0.9:
        strengths.append("First-in-class potential")
    elif novelty < 0.4:
        weaknesses.append("Incremental innovation only")
    
    # Clinical relevance (0-10 pts)
    clinical = candidate.get("clinical_score", 0.5)
    rubric.clinical_relevance = clinical * 10
    if clinical >= 0.8:
        strengths.append("High clinical relevance")
    
    # Combinability (0-10 pts)
    combo = candidate.get("combo_score", 0.5)
    rubric.combinability = combo * 10
    if combo >= 0.8:
        strengths.append("Strong combination therapy potential")
    
    impact_score = rubric.novelty + rubric.clinical_relevance + rubric.combinability
    
    # ============================================
    # TOTAL
    # ============================================
    total = approach_score + orchestration_score + quality_score + impact_score
    grade = ScoreGrade.from_score(total).value
    
    return ScoreResult(
        total=total,
        grade=grade,
        breakdown=rubric,
        approach_score=approach_score,
        orchestration_score=orchestration_score,
        quality_score=quality_score,
        impact_score=impact_score,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations
    )


def format_score_report(result: ScoreResult, candidate_name: str = "Candidate") -> str:
    """Format score result as human-readable markdown report"""
    lines = [
        f"## Score Report: {candidate_name}",
        "",
        f"**Total Score:** {result.total:.1f}/100 | **Grade:** {result.grade}",
        "",
        f"| Category | Score | Max |",
        f"|----------|-------|-----|",
        f"| Approach | {result.approach_score:.1f} | 20 |",
        f"| Orchestration | {result.orchestration_score:.1f} | 20 |",
        f"| Quality | {result.quality_score:.1f} | 30 |",
        f"| Impact | {result.impact_score:.1f} | 30 |",
        "",
    ]
    
    if result.strengths:
        lines.append("### Strengths")
        for s in result.strengths:
            lines.append(f"- ✅ {s}")
        lines.append("")
    
    if result.weaknesses:
        lines.append("### Weaknesses")
        for w in result.weaknesses:
            lines.append(f"- ⚠️ {w}")
        lines.append("")
    
    if result.recommendations:
        lines.append("### Recommendations")
        for r in result.recommendations:
            lines.append(f"- 💡 {r}")
        lines.append("")
    
    return "\n".join(lines)


def format_score_json(result: ScoreResult) -> str:
    """Format score result as JSON"""
    return json.dumps(result.to_dict(), indent=2)


# Comparison function for multiple candidates
def compare_candidates(results: List[ScoreResult], names: List[str] = None) -> str:
    """Compare multiple candidates and rank them"""
    sorted_results = sorted(zip(results, names or [f"Candidate {i}"], range(len(results))), 
                          key=lambda x: x[0].total, reverse=True)
    
    lines = ["## Candidate Comparison", ""]
    lines.append("| Rank | Candidate | Score | Grade |")
    lines.append("|------|-----------|-------|-------|")
    
    for rank, (result, name, _) in enumerate(sorted_results, 1):
        lines.append(f"| {rank} | {name} | {result.total:.1f} | {result.grade} |")
    
    return "\n".join(lines)


# Test
if __name__ == "__main__":
    test_candidate = {
        "name": "ARP-FSP1-001",
        "target": "FSP1",
        "ic50_nM": 45.0,
        "selectivity_ratio": 35.0,
        "admet_score": 0.75,
        "novelty_score": 0.9,
        "clinical_score": 0.85,
        "combo_score": 0.8,
        "evaluation_depth": 0.85,  # Expert level
        "tools_used": ["boltz2", "pubmed", "admet_pred"],
        "hypothesis_score": 0.9,
        "design_score": 0.85
    }
    
    test_context = {
        "pmids": ["PMID:12345", "PMID:67890", "PMID:11111", "PMID:22222", "PMID:33333"]
    }
    
    print("=== ARP Scoring Rubric Test ===\n")
    
    result = score_candidate(test_candidate, context=test_context)
    print(format_score_report(result, "ARP-FSP1-001"))
    print("\n--- JSON ---")
    print(format_score_json(result))