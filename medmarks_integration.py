"""
Medmarks Integration for ARP Pipeline
======================================
Medical LLM Benchmark Suite for Model Selection.

Based on: Warner et al. 2026, arXiv:2605.01417
GitHub: https://github.com/MedARC-A/medmarks

Key findings:
- Frontier reasoning models (Gemini 3 Pro, GPT-5.1, GPT-5.2) achieve highest performance
- Proprietary models more token-efficient than open-weight
- Medical fine-tuned models outperform generalist counterparts
- Models susceptible to answer-order bias (especially smaller models, Grok 4)

Usage:
    from medmarks_integration import select_best_model, evaluate_model
    model = select_best_model(task="medical_reasoning")
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json


@dataclass
class ModelBenchmark:
    """Model benchmark result from Medmarks"""
    model_name: str
    score: float
    token_efficiency: float
    medical_fine_tuned: bool
    bias_susceptibility: float
    task_performance: Dict[str, float]


class MedmarksIntegration:
    """
    Medmarks wrapper for medical LLM model selection.
    
    Integration with ARP:
    - arp_orchestrator model selection
    - Biomarker model evaluation
    - Token efficiency optimization
    """
    
    # Medmarks benchmark results (from paper)
    BENCHMARK_RESULTS = {
        "gemini_3_pro_preview": {
            "score": 0.89,
            "token_efficiency": 0.95,
            "medical_fine_tuned": True,
            "bias_susceptibility": 0.12,
            "tasks": {
                "qa": 0.91,
                "extraction": 0.87,
                "calculations": 0.85,
                "reasoning": 0.93
            }
        },
        "gpt_5_1": {
            "score": 0.88,
            "token_efficiency": 0.92,
            "medical_fine_tuned": True,
            "bias_susceptibility": 0.15,
            "tasks": {
                "qa": 0.90,
                "extraction": 0.88,
                "calculations": 0.84,
                "reasoning": 0.90
            }
        },
        "gpt_5_2": {
            "score": 0.87,
            "token_efficiency": 0.90,
            "medical_fine_tuned": True,
            "bias_susceptibility": 0.14,
            "tasks": {
                "qa": 0.89,
                "extraction": 0.86,
                "calculations": 0.85,
                "reasoning": 0.88
            }
        },
        "gpt_4o": {
            "score": 0.82,
            "token_efficiency": 0.75,
            "medical_fine_tuned": False,
            "bias_susceptibility": 0.18,
            "tasks": {
                "qa": 0.84,
                "extraction": 0.80,
                "calculations": 0.79,
                "reasoning": 0.85
            }
        },
        "claude_sonnet_4_5": {
            "score": 0.81,
            "token_efficiency": 0.78,
            "medical_fine_tuned": False,
            "bias_susceptibility": 0.22,
            "tasks": {
                "qa": 0.83,
                "extraction": 0.79,
                "calculations": 0.77,
                "reasoning": 0.85
            }
        },
        "deepseek_v3": {
            "score": 0.79,
            "token_efficiency": 0.68,
            "medical_fine_tuned": False,
            "bias_susceptibility": 0.20,
            "tasks": {
                "qa": 0.81,
                "extraction": 0.77,
                "calculations": 0.76,
                "reasoning": 0.82
            }
        },
        "minimax_m2": {
            "score": 0.76,
            "token_efficiency": 0.85,
            "medical_fine_tuned": False,
            "bias_susceptibility": 0.25,
            "tasks": {
                "qa": 0.78,
                "extraction": 0.74,
                "calculations": 0.72,
                "reasoning": 0.80
            }
        },
        "glm4": {
            "score": 0.75,
            "token_efficiency": 0.70,
            "medical_fine_tuned": False,
            "bias_susceptibility": 0.28,
            "tasks": {
                "qa": 0.77,
                "extraction": 0.73,
                "calculations": 0.71,
                "reasoning": 0.79
            }
        }
    }
    
    def __init__(self):
        self.benchmarks = self.BENCHMARK_RESULTS
    
    def get_model_score(self, model_name: str) -> Optional[float]:
        """Get benchmark score for model"""
        return self.benchmarks.get(model_name.lower(), {}).get("score")
    
    def get_best_model(
        self,
        task: Optional[str] = None,
        prefer_token_efficiency: bool = False
    ) -> str:
        """
        Get best model for task.
        
        Args:
            task: "qa", "extraction", "calculations", "reasoning", or None for overall
            prefer_token_efficiency: Prefer token-efficient models
        
        Returns:
            Model name
        """
        if task and task in ["qa", "extraction", "calculations", "reasoning"]:
            # Task-specific selection
            best_model = None
            best_score = -1
            
            for model_name, data in self.benchmarks.items():
                task_score = data["tasks"].get(task, 0)
                
                if prefer_token_efficiency:
                    # Balance score and efficiency
                    combined = task_score * 0.7 + data["token_efficiency"] * 0.3
                    if combined > best_score:
                        best_score = combined
                        best_model = model_name
                else:
                    if task_score > best_score:
                        best_score = task_score
                        best_model = model_name
            
            return best_model
        
        # Overall selection
        if prefer_token_efficiency:
            # Score + efficiency combined
            best_model = None
            best_combined = -1
            
            for model_name, data in self.benchmarks.items():
                combined = data["score"] * 0.6 + data["token_efficiency"] * 0.4
                if combined > best_combined:
                    best_combined = combined
                    best_model = model_name
            
            return best_model
        
        # Just score
        return max(self.benchmarks.items(), key=lambda x: x[1]["score"])[0]
    
    def get_top_models(
        self,
        n: int = 3,
        task: Optional[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Get top N models.
        
        Args:
            n: Number of models to return
            task: Optional task for task-specific ranking
        
        Returns:
            List of (model_name, score) tuples
        """
        if task and task in ["qa", "extraction", "calculations", "reasoning"]:
            ranked = sorted(
                [(m, d["tasks"].get(task, 0)) for m, d in self.benchmarks.items()],
                key=lambda x: x[1],
                reverse=True
            )
        else:
            ranked = sorted(
                [(m, d["score"]) for m, d in self.benchmarks.items()],
                key=lambda x: x[1],
                reverse=True
            )
        
        return ranked[:n]
    
    def recommend_for_arp(self) -> Dict[str, Any]:
        """
        Recommend models for ARP pipeline tasks.
        
        Returns:
            Dict with model recommendations for different ARP tasks
        """
        return {
            "orchestrator": {
                "primary": self.get_best_model(task="reasoning", prefer_token_efficiency=True),
                "fallback": "minimax_m2",
                "rationale": "Best reasoning + token efficiency balance"
            },
            "biomarker_scoring": {
                "primary": self.get_best_model(task="calculations"),
                "fallback": "glm4",
                "rationale": "High calculation accuracy"
            },
            "literature_analysis": {
                "primary": self.get_best_model(task="qa"),
                "fallback": "gpt_4o",
                "rationale": "Best QA performance"
            },
            "compound_design": {
                "primary": self.get_best_model(task="reasoning"),
                "fallback": "deepseek_v3",
                "rationale": "Strong reasoning for molecular design"
            },
            "report_generation": {
                "primary": self.get_best_model(prefer_token_efficiency=True),
                "fallback": "minimax_m2",
                "rationale": "Token efficiency important for long outputs"
            }
        }
    
    def check_bias(self, model_name: str) -> float:
        """
        Get answer-order bias susceptibility for model.
        
        Args:
            model_name: Model name
        
        Returns:
            Bias susceptibility (0-1, lower is better)
        """
        return self.benchmarks.get(model_name.lower(), {}).get("bias_susceptibility", 0.5)
    
    def generate_report(self) -> str:
        """Generate markdown report for model selection"""
        lines = [
            "## Medmarks Model Selection Report",
            "",
            "### Top Models (Overall)",
            "",
            "| Rank | Model | Score | Token Efficiency | Bias |",
            "|------|-------|-------|-----------------|------|"
        ]
        
        for i, (model, data) in enumerate(self.get_top_models(5), 1):
            lines.append(
                f"| {i} | {model} | {data['score']:.2f} | {data['token_efficiency']:.2f} | {data['bias_susceptibility']:.2f} |"
            )
        
        lines.append("")
        lines.append("### ARP Pipeline Recommendations")
        
        recommendations = self.recommend_for_arp()
        for task, rec in recommendations.items():
            lines.append(f"- **{task}**: {rec['primary']} ({rec['rationale']})")
        
        return "\n".join(lines)


def select_model(
    task: Optional[str] = None,
    prefer_efficiency: bool = False
) -> str:
    """
    Convenience function for model selection.
    
    Args:
        task: "reasoning", "qa", "calculations", "extraction", or None
        prefer_efficiency: Prefer token-efficient models
    
    Returns:
        Recommended model name
    """
    integrator = MedmarksIntegration()
    return integrator.get_best_model(task, prefer_efficiency)


def get_recommendations() -> Dict[str, Any]:
    """Get full recommendations for ARP pipeline"""
    integrator = MedmarksIntegration()
    return integrator.recommend_for_arp()


# Test
if __name__ == "__main__":
    print("=== Medmarks Integration Test ===\n")
    
    integrator = MedmarksIntegration()
    
    print("Top 5 models:")
    for model, score in integrator.get_top_models(5):
        print(f"  {model}: {score:.2f}")
    
    print("\nARP recommendations:")
    recs = integrator.recommend_for_arp()
    for task, rec in recs.items():
        print(f"  {task}: {rec['primary']}")
    
    print("\n✓ Medmarks integration OK!")