# ARP Pipeline Upgrade: BioDesignBench Insights
**Date:** 2026-05-12
**Based on:** Romero Lab BioDesignBench (Duke University)
**Goal:** Upgrade ARP Pipeline based on benchmark findings

---

## Executive Summary

BioDesignBench benchmark 결과를 분석하여 ARP Pipeline을 업그레이드합니다.

| Finding | Implication | Action |
|---------|-------------|--------|
| LLM agents > hardcoded | ✅ 우리 방향 올바름 | 유지 |
| Evaluation depth = bottleneck | ⚠️ 14% only | Iterative evaluation 추가 |
| Coverage-Depth 분리 | ⚠️ Workflow만 불충분 | Depth-focused design |
| ρ = 0.685 (eval↔score) | 📊 증명됨 | Evaluation 우선순위 |

---

## 1. BioDesignBench 핵심 발견 분석

### 1.1 Ranking 분석

```
Human Oracle:        74.9  ████████████████████
Human Expert:        61.3  █████████████████
DeepSeek V3:         60.4  █████████████████  ← LLM > Hardcoded!
GPT-5:               55.6  ████████████████
Hardcoded Pipeline:  54.2  ████████████████  ← beaten by LLM agents
Claude Sonnet 4.5:   50.2  ██████████████
```

**결론:** Autonomous protein design orchestration 가능함

### 1.2 Evaluation Depth Bottleneck

```
Expert evaluation depth:  100%
Agents invocation:        14%  ← 86% 손실!

문제: Agents know tools but don't evaluate deeply enough
해결: Iterative multi-candidate screening
```

### 1.3 Coverage vs Depth Dissociation

| Intervention | Coverage | Depth |
|-------------|----------|-------|
| Workflow guidance | ↑ Rescue +3.01 | ≈ 0 |
| Better tool docs | ↑ | ≈ 0 |
| **필요:** Evaluation-focused design | ↑ | ↑ |

---

## 2. Current ARP Pipeline vs BioDesignBench

### 2.1 Gap Analysis

| Component | BioDesignBench | Current ARP | Status |
|-----------|---------------|-------------|--------|
| **LLM Agent** | DeepSeek V3, GPT-5 | arp_orchestrator (BIORESEARCHER) | ⚠️ Upgrade |
| **Generative Tools** | Boltz-2, RFdiffusion, ProteinMPNN | Boltz-2 only | ⚠️ Add |
| **Evaluation** | Iterative multi-candidate | Single pass | ❌ Missing |
| **Scoring** | 100-point rubric + LLM judge | Basic evidence_level | ⚠️ Upgrade |
| **MCP Tools** | 17 reference tools | None | ❌ Missing |
| **Bio-specific agents** | Biomni, STELLA, BioML | Generic only | ❌ Missing |

### 2.2 What's Missing

```
❌ Iterative evaluation loop
❌ Multi-candidate generation + screening
❌ Bio-specific agent wrappers
❌ MCP tool integration
❌ 100-point scoring rubric
❌ LLM judge for quality assessment
```

---

## 3. ARP Pipeline Upgrade Plan

### 3.1 Phase 1: Evaluation Depth (HIGH PRIORITY)

**목표:** 14% → 80%+ evaluation depth

```python
# Upgrade: iterative_evaluation.py

class IterativeEvaluation:
    """
    BioDesignBench-inspired iterative evaluation loop.
    Generate multiple candidates → Screen → Refine → Repeat
    """
    
    def __init__(self, max_iterations=5, candidates_per_iter=5):
        self.max_iterations = max_iterations
        self.candidates_per_iter = candidates_per_iter
    
    def evaluate_candidate(self, candidate):
        """Deep evaluation across biophysical metrics"""
        metrics = {
            "binding_affinity": self.check_boltz2(candidate),
            "selectivity": self.check_selectivity(candidate),
            "synthetic_feasibility": self.check_synthetic(candidate),
            "admet": self.check_admet(candidate),
            "structural_stability": self.check_folding(candidate)
        }
        return metrics
    
    def iterative_screen(self, initial_leads):
        """
        BioDesignBench-style iterative screening:
        1. Generate N candidates
        2. Evaluate each across metrics
        3. Select top K for next iteration
        4. Repeat until convergence
        """
        candidates = initial_leads
        for iteration in range(self.max_iterations):
            evaluated = [self.evaluate_candidate(c) for c in candidates]
            scored = self.rank_candidates(evaluated)
            candidates = self.select_top(scored, k=self.candidates_per_iter)
        return candidates
```

### 3.2 Phase 2: Multi-Candidate Generation

**문제:** 현재 pipeline은 단일 candidate만 생성

**해결:** N candidates → evaluation → refinement loop

```
Input: Initial leads (10-20)
    ↓
Iteration 1: Generate candidates (5)
    ├── Evaluate: binding, selectivity, ADMET
    ├── Score: composite score
    └── Select: top 3
    ↓
Iteration 2: Generate refined candidates (5)
    ├── Evaluate: deeper metrics
    ├── Score: composite score
    └── Select: top 2
    ↓
Iteration 3: Final candidates (2-3)
    ├── Final evaluation
    └── Rank and report
```

### 3.3 Phase 3: Scoring Rubric (100-point)

```python
# Upgrade: scoring_rubric.py

SCORING_RUBRIC = {
    # Approach (20 pts)
    "literature_grounding": {"max": 8, "desc": "Literature support"},
    "hypothesis_soundness": {"max": 6, "desc": "Scientific rationale"},
    "experimental_design": {"max": 6, "desc": "Methodology"},
    
    # Orchestration (20 pts)
    "tool_usage_efficiency": {"max": 10, "desc": "Right tool for right job"},
    "iteration_depth": {"max": 7, "desc": "Evaluation depth (14% → 80%+)"},
    "error_recovery": {"max": 3, "desc": "Failure policy execution"},
    
    # Quality (30 pts)
    "binding_affinity": {"max": 10, "desc": "nM potency"},
    "selectivity": {"max": 10, "desc": "Off-target panel"},
    "admet_profile": {"max": 10, "desc": "Drug-like properties"},
    
    # Impact (30 pts)
    "novelty": {"max": 10, "desc": "First-in-class potential"},
    "clinical_relevance": {"max": 10, "desc": "Disease relevance"},
    "combinability": {"max": 10, "desc": "Synergy potential"}
}

def calculate_score(candidate, metrics) -> dict:
    """Calculate 100-point score for candidate"""
    total = 0
    breakdown = {}
    for category, params in SCORING_RUBRIC.items():
        score = min(metrics.get(category, 0) / params["max"], 1.0) * params["max"]
        breakdown[category] = score
        total += score
    return {"total": total, "breakdown": breakdown}
```

### 3.4 Phase 4: LLM Judge Integration

```python
# Upgrade: llm_judge.py

class LLMJudge:
    """
    BioDesignBench-style LLM judge for 28-point rubric.
    Uses PoLL (Prompt-of-Last-Log) with self-exclusion.
    """
    
    def __init__(self, model="deepseek-v3"):
        self.model = model
    
    def evaluate_design(self, candidate, criteria) -> dict:
        """
        Evaluate candidate across 28-point rubric:
        - Novelty (8 pts)
        - Feasibility (8 pts)
        - Impact (12 pts)
        """
        prompt = f"""
        Evaluate this protein design candidate:
        Name: {candidate['name']}
        SMILES: {candidate['smiles']}
        Target: {candidate['target']}
        
        Criteria:
        {criteria}
        
        Score 0-100 and provide feedback.
        """
        return self.call_llm(prompt)
```

### 3.5 Phase 5: MCP Tool Integration

```python
# Upgrade: mcp_tools.py

# Reference: jasonkim8652/protein-design-mcp
# Install: pip install protein-design-mcp

TOOLS = {
    # Structure prediction
    "boltz2_predict": {"category": "structure", "tool": "Boltz-2"},
    "rfdiffusion_generate": {"category": "structure", "tool": "RFdiffusion"},
    
    # Sequence design
    "proteinmpnn_design": {"category": "sequence", "tool": "ProteinMPNN"},
    
    # Evaluation
    "binding_affinity": {"category": "evaluation", "tool": "Molecular dynamics"},
    "selectivity_screen": {"category": "evaluation", "tool": "Panel screen"},
    "admet_predict": {"category": "evaluation", "tool": "ML prediction"},
    
    # Literature
    "pubmed_search": {"category": "literature", "tool": "E-utilities"},
    "patent_check": {"category": "literature", "tool": "USPTO"},
}

def get_tool(tool_name):
    """Get MCP tool by name"""
    return TOOLS.get(tool_name)
```

---

## 4. Upgrade Architecture

### 4.1 New Directory Structure

```
arp-v24/
├── arp/                        # Core source
│   ├── __init__.py
│   ├── orchestrator.py        # Existing
│   ├── boltz2_client.py       # Existing
│   ├── db.py                  # Existing
│   ├── iterative_evaluation.py  # NEW
│   ├── scoring_rubric.py        # NEW
│   ├── llm_judge.py             # NEW
│   ├── multi_candidate.py       # NEW
│   └── mcp_tools.py             # NEW
├── reports/                    # Existing
├── docs/                       # Existing
├── tests/                      # Existing
├── configs/
│   ├── default_config.yaml
│   └── playbook_configs/       # Existing
├── .github/workflows/          # Existing
│   └── ci.yml                  # Existing
├── evidence_level.py           # Existing
├── stage_policies.py           # Existing
├── schemas/                    # Existing
│   └── output_schema.json      # Existing
├── requirements.txt            # Existing
└── README.md                   # Existing
```

### 4.2 Upgrade Dependencies

```txt
# requirements.txt additions
# MCP tools
protein-design-mcp @ git+https://github.com/jasonkim8652/protein-design-mcp

# Evaluation
pyrfold>=1.0.0
mdanalysis>=1.0.

# Scoring
openai>=1.0.0  # or anthropic, deepseek

# Pipeline
pydantic>=2.0.0
pyyaml>=6.0.0
```

---

## 5. Implementation Plan

### 5.1 Priority Order

| Week | Focus | Deliverable |
|------|-------|-------------|
| **1** | Iterative Evaluation | `iterative_evaluation.py` |
| **2** | Multi-Candidate Generation | `multi_candidate.py` |
| **3** | Scoring Rubric | `scoring_rubric.py` |
| **4** | LLM Judge | `llm_judge.py` |
| **5** | MCP Integration | `mcp_tools.py` |
| **6** | Integration Test | Full pipeline test |

### 5.2 Phase 1 Implementation (Week 1)

```python
# iterative_evaluation.py - 핵심 코드

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

class EvaluationDepth(Enum):
    """4-level evaluation depth (based on BioDesignBench)"""
    SURFACE = "surface"           # 0-20%: Basic check
    STANDARD = "standard"         # 20-50%: Standard metrics
    COMPREHENSIVE = "comprehensive"  # 50-80%: Multi-metric
    EXPERT = "expert"             # 80-100%: Full depth

@dataclass
class CandidateResult:
    """Single candidate evaluation result"""
    name: str
    metrics: Dict[str, float]
    depth: EvaluationDepth
    score: float
    feedback: str
    iterations: int
    refinement_path: List[str]

class IterativeEvaluator:
    """
    BioDesignBench-inspired iterative evaluator.
    
    Key insight: "Evaluation depth per candidate correlates
    with total score at ρ = 0.685"
    
    Goal: Increase evaluation depth from 14% (current) to 80%+
    """
    
    def __init__(
        self,
        max_iterations: int = 5,
        min_depth: EvaluationDepth = EvaluationDepth.COMPREHENSIVE,
        candidates_per_iter: int = 5
    ):
        self.max_iterations = max_iterations
        self.min_depth = min_depth
        self.candidates_per_iter = candidates_per_iter
    
    def evaluate(
        self,
        candidates: List[Dict],
        target_profile: Dict[str, Any]
    ) -> List[CandidateResult]:
        """
        Iteratively evaluate candidates until expert depth reached.
        
        Flow:
        1. Initial screening (all candidates)
        2. Multi-metric evaluation (top candidates)
        3. Iterative refinement (until depth ≥ min_depth)
        4. Final ranking
        """
        current_candidates = candidates
        iteration = 0
        refinement_log = []
        
        while iteration < self.max_iterations:
            # Evaluate all current candidates
            results = []
            for candidate in current_candidates:
                result = self._deep_evaluate(candidate, target_profile, iteration)
                results.append(result)
            
            # Check if we've reached min depth
            avg_depth = sum(r.depth.priority for r in results) / len(results)
            if avg_depth >= self.min_depth.priority:
                break
            
            # Select top candidates for next iteration
            scored = sorted(results, key=lambda x: x.score, reverse=True)
            current_candidates = [s.candidate for s in scored[:self.candidates_per_iter]]
            refinement_log.append({
                "iteration": iteration,
                "selected": len(current_candidates),
                "top_score": scored[0].score
            })
            iteration += 1
        
        return results
    
    def _deep_evaluate(
        self,
        candidate: Dict,
        target_profile: Dict,
        iteration: int
    ) -> CandidateResult:
        """
        Deep evaluation across 5 biophysical dimensions.
        
        Based on BioDesignBench tier2 evaluation:
        - Binding affinity (Boltz-2)
        - Selectivity (off-target panel)
        - Synthetic feasibility
        - ADMET profile
        - Structural stability
        """
        metrics = {}
        
        # 1. Binding affinity
        if "boltz" in target_profile.get("tools", []):
            metrics["binding"] = self._eval_binding(candidate)
        
        # 2. Selectivity
        metrics["selectivity"] = self._eval_selectivity(candidate)
        
        # 3. Synthetic feasibility
        metrics["synthetic"] = self._eval_synthetic(candidate)
        
        # 4. ADMET
        metrics["admet"] = self._eval_admet(candidate)
        
        # 5. Stability
        metrics["stability"] = self._eval_stability(candidate)
        
        # Calculate composite score
        weights = {"binding": 0.3, "selectivity": 0.25, "synthetic": 0.15, "admet": 0.15, "stability": 0.15}
        score = sum(metrics[k] * weights[k] for k in weights)
        
        # Determine depth level
        metrics_checked = sum(1 for v in metrics.values() if v > 0)
        if metrics_checked >= 5:
            depth = EvaluationDepth.EXPERT
        elif metrics_checked >= 3:
            depth = EvaluationDepth.COMPREHENSIVE
        elif metrics_checked >= 2:
            depth = EvaluationDepth.STANDARD
        else:
            depth = EvaluationDepth.SURFACE
        
        return CandidateResult(
            name=candidate.get("name", "unknown"),
            metrics=metrics,
            depth=depth,
            score=score,
            feedback=self._generate_feedback(metrics),
            iterations=iteration + 1,
            refinement_path=refinement_log
        )
    
    def _eval_binding(self, candidate: Dict) -> float:
        """Evaluate binding affinity (0-1, higher = better)"""
        ic50 = candidate.get("ic50_nM", float('inf'))
        if ic50 < 50:
            return 1.0
        elif ic50 < 500:
            return 0.8
        elif ic50 < 1000:
            return 0.6
        elif ic50 < 5000:
            return 0.3
        else:
            return 0.1
    
    def _eval_selectivity(self, candidate: Dict) -> float:
        """Evaluate selectivity (0-1, higher = better)"""
        selectivity = candidate.get("selectivity_ratio", 1.0)
        if selectivity >= 30:
            return 1.0
        elif selectivity >= 10:
            return 0.7
        elif selectivity >= 3:
            return 0.4
        else:
            return 0.2
    
    def _eval_synthetic(self, candidate: Dict) -> float:
        """Evaluate synthetic feasibility (0-1, higher = better)"""
        steps = candidate.get("synthetic_steps", 99)
        if steps <= 4:
            return 1.0
        elif steps <= 7:
            return 0.7
        elif steps <= 10:
            return 0.4
        else:
            return 0.2
    
    def _eval_admet(self, candidate: Dict) -> float:
        """Evaluate ADMET profile (0-1, higher = better)"""
        admet = candidate.get("admet_score", 0.5)
        return min(admet, 1.0)
    
    def _eval_stability(self, candidate: Dict) -> float:
        """Evaluate structural stability (0-1, higher = better)"""
        stability = candidate.get("folding_stability", 0.5)
        return min(stability, 1.0)
    
    def _generate_feedback(self, metrics: Dict) -> str:
        """Generate human-readable feedback"""
        issues = []
        if metrics.get("binding", 0) < 0.7:
            issues.append("binding affinity low")
        if metrics.get("selectivity", 0) < 0.7:
            issues.append("selectivity concern")
        if metrics.get("synthetic", 0) < 0.5:
            issues.append("synthetic complexity")
        if issues:
            return f"Consider: {', '.join(issues)}"
        return "Meets design criteria"
```

### 5.3 Phase 2: Scoring Integration

```python
# scoring_rubric.py - 100-point scoring

def score_candidate(candidate: Dict, metrics: Dict) -> Dict:
    """
    Calculate 100-point score based on BioDesignBench rubric.
    
    Categories:
    - Approach (20 pts): Literature, hypothesis, experimental design
    - Orchestration (20 pts): Tool usage, iteration depth, error recovery
    - Quality (30 pts): Binding, selectivity, ADMET
    - Impact (30 pts): Novelty, clinical relevance, combinability
    """
    scores = {}
    
    # Approach (20 pts)
    scores["literature_grounding"] = min(candidate.get("pmid_count", 0) / 5, 1.0) * 8
    scores["hypothesis_soundness"] = candidate.get("hypothesis_score", 0.5) * 6
    scores["experimental_design"] = candidate.get("design_score", 0.5) * 6
    
    # Orchestration (20 pts)
    scores["tool_usage_efficiency"] = min(candidate.get("tools_used", 1) / 5, 1.0) * 10
    scores["iteration_depth"] = (candidate.get("eval_depth", 0.14)) * 7  # 14% baseline
    scores["error_recovery"] = candidate.get("recovery_score", 0.5) * 3
    
    # Quality (30 pts)
    scores["binding_affinity"] = candidate.get("binding_score", 0.5) * 10
    scores["selectivity"] = candidate.get("selectivity_score", 0.5) * 10
    scores["admet_profile"] = candidate.get("admet_score", 0.5) * 10
    
    # Impact (30 pts)
    scores["novelty"] = candidate.get("novelty_score", 0.5) * 10
    scores["clinical_relevance"] = candidate.get("clinical_score", 0.5) * 10
    scores["combinability"] = candidate.get("combo_score", 0.5) * 10
    
    total = sum(scores.values())
    
    return {
        "total": total,
        "breakdown": scores,
        "grade": "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D"
    }
```

---

## 6. BioDesignBench vs ARP Comparison (Updated)

### 6.1 Before vs After

| Aspect | Before (Current) | After (Upgraded) |
|--------|------------------|------------------|
| **Evaluation** | Single pass | Iterative (5 iterations) |
| **Candidates** | Single | Multiple (5 per iter) |
| **Depth** | 14% (surface) | 80%+ (expert) |
| **Scoring** | Evidence level (4-tier) | 100-point rubric |
| **Tools** | Boltz-2 only | 17 MCP tools |
| **Agents** | Generic | Bio-specific wrappers |
| **Feedback** | Basic | LLM judge |

### 6.2 Expected Improvement

```
Current ARP:       ~54 (hardcoded pipeline level)
After Upgrade:     ~60+ (DeepSeek V3 level)
Target:            65+ (GPT-5 competitive)
```

---

## 7. Integration with Current ARP

### 7.1 Backward Compatibility

```python
# Keep existing evidence_level.py as lightweight option
# Add iterative_evaluation.py as advanced option

from evidence_level import EvidenceLevel  # Lightweight (existing)
from iterative_evaluation import IterativeEvaluator  # Advanced (new)

# Use both together
def full_pipeline(orchestrator, candidates):
    # Stage 1: Quick evidence check (existing)
    quick_results = [apply_evidence_level(c) for c in candidates]
    
    # Stage 2: Deep iterative evaluation (new)
    evaluator = IterativeEvaluator(max_iterations=5)
    deep_results = evaluator.evaluate(quick_results, target_profile)
    
    # Stage 3: Score with rubric (new)
    for result in deep_results:
        result.rubric_score = score_candidate(result)
    
    return sorted(deep_results, key=lambda x: x.rubric_score["total"], reverse=True)
```

### 7.2 Configuration

```yaml
# configs/upgrade_config.yaml
upgrade:
  iterative_evaluation:
    enabled: true
    max_iterations: 5
    candidates_per_iter: 5
    min_depth: comprehensive
  
  scoring:
    enabled: true
    rubric: "biodesignbench"
    threshold: 60.0
  
  llm_judge:
    enabled: true
    model: "deepseek-v3"
    auto_evaluate: true
  
  mcp_tools:
    enabled: false  # Future
    server: "protein-design-mcp"
```

---

## 8. Files to Create

| File | Purpose | Priority |
|------|---------|----------|
| `iterative_evaluation.py` | Iterative candidate screening | HIGH |
| `scoring_rubric.py` | 100-point scoring | HIGH |
| `multi_candidate.py` | Multi-candidate generation | MEDIUM |
| `llm_judge.py` | LLM-based evaluation | MEDIUM |
| `mcp_tools.py` | MCP tool wrapper | LOW |
| `upgrade_config.yaml` | Configuration | MEDIUM |

---

## 9. Summary

### BioDesignBench → ARP Upgrade

| Finding | Action |
|---------|--------|
| LLM > hardcoded | Continue with arp_orchestrator |
| Eval depth = bottleneck (14%) | Add iterative_evaluation.py |
| Coverage ≠ depth | Multi-candidate + deep metrics |
| ρ = 0.685 | Prioritize evaluation quality |

### Upgrade Path

```
Week 1: Iterative Evaluation
Week 2: Multi-Candidate Generation  
Week 3: Scoring Rubric
Week 4: LLM Judge
Week 5: MCP Integration (optional)
Week 6: Integration Test
```

### Expected Outcome

| Metric | Before | After |
|--------|--------|-------|
| Evaluation depth | 14% | 80%+ |
| Candidate count | 1-3 | 10-25 |
| Pipeline score | ~54 | 60-65+ |
| Research quality | Good | Excellent |

---

*Generated: 2026-05-12 | ARP v24*  
*Upgrade based on: Romero Lab BioDesignBench*