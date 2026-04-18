"""
Qwen3.6-35B-A3B SubAgent Configuration for ARP Pipeline

Integration of Qwen3.6-35B-A3B as a specialized subagent for:
- Code generation and pipeline automation
- Scientific literature analysis
- Report writing and documentation
- Biomedical research tasks

Model: Qwen/Qwen3.6-35B-A3B
Provider: HuggingFace / SGLang / vLLM
Context: 262K tokens (1M+ extended)
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Qwen36Config:
    """Configuration for Qwen3.6-35B-A3B subagent"""
    
    # Model identification
    model_name: str = "Qwen/Qwen3.6-35B-A3B"
    model_type: str = "causal_language_model_with_vision"
    
    # Architecture
    total_parameters: int = 35_000_000_000  # 35B
    activated_parameters: int = 3_000_000_000  # 3B (MoE)
    num_experts: int = 256
    activated_experts: int = 9  # 8 routed + 1 shared
    
    # Context and capabilities
    context_length: int = 262_144  # 262K native
    max_context: int = 1_010_000  # Extended
    vision_support: bool = True
    
    # Serving configuration
    default_port: int = 8000
    recommended_framework: str = "sglang"  # or "vllm"
    
    # Performance settings
    temperature: float = 0.6
    top_p: float = 0.95
    max_tokens: int = 8192
    
    # Tool use
    tool_use_enabled: bool = True
    reasoning_parser: str = "qwen3"
    tool_call_parser: str = "qwen3_coder"


class Qwen36SubAgent:
    """Qwen3.6-35B-A3B SubAgent for ARP Pipeline"""
    
    def __init__(self, config: Optional[Qwen36Config] = None):
        self.config = config or Qwen36Config()
        self.name = "Qwen3.6-35B-A3B"
        self.status = "initialized"
        self.api_endpoint = None
        
    def setup_api(self, 
                 framework: str = "sglang",
                 port: int = 8000,
                 tensor_parallel: int = 8) -> str:
        """
        Setup API endpoint for Qwen3.6-35B-A3B
        
        Args:
            framework: "sglang" or "vllm"
            port: Port number
            tensor_parallel: Number of GPUs for tensor parallelism
            
        Returns:
            API endpoint URL
        """
        self.api_endpoint = f"http://localhost:{port}/v1"
        
        if framework == "sglang":
            cmd = f"""python -m sglang.launch_server \\
  --model-path {self.config.model_name} \\
  --port {port} \\
  --tp-size {tensor_parallel} \\
  --mem-fraction-static 0.8 \\
  --context-length {self.config.context_length} \\
  --reasoning-parser {self.config.reasoning_parser}"""
        else:  # vllm
            cmd = f"""vllm serve {self.config.model_name} \\
  --port {port} \\
  --tensor-parallel-size {tensor_parallel} \\
  --max-model-len {self.config.context_length} \\
  --reasoning-parser {self.config.reasoning_parser}"""
        
        return cmd
    
    def get_system_prompt(self, task_type: str) -> str:
        """Get specialized system prompt for different task types"""
        
        prompts = {
            "code_generation": """You are Qwen3.6, an expert AI coding assistant for the ARP (Autonomous Research Pipeline) system.

Your task is to generate, optimize, and debug Python code for drug discovery pipelines.

Capabilities:
- Python, JavaScript, Shell scripting
- Scientific computing (NumPy, Pandas, RDKit)
- API integrations (PubChem, ChEMBL, UniProt)
- Pipeline orchestration code
- Test generation and documentation

Guidelines:
1. Write clean, documented code
2. Follow PEP 8 style guidelines
3. Include type hints for functions
4. Add docstrings for complex logic
5. Handle errors gracefully
6. Write unit tests for critical functions

Output format:
```python
# Your code here
```
""",
            
            "literature_analysis": """You are Qwen3.6, an expert biomedical research analyst.

Your task is to analyze scientific literature, extract insights, and summarize findings.

Capabilities:
- PubMed/MEDLINE literature search and synthesis
- Clinical trial data interpretation
- Mechanism of action analysis
- Target validation evidence
- ADMET prediction interpretation

Guidelines:
1. Provide evidence-based analysis
2. Cite primary literature sources
3. Assess study quality and limitations
4. Identify knowledge gaps
5. Suggest next research directions

Output format:
## Summary
## Key Findings
## Evidence Assessment
## Research Gaps
## Recommendations
""",
            
            "report_writing": """You are Qwen3.6, an expert scientific writer for biomedical research.

Your task is to write comprehensive research reports, grant proposals, and documentation.

Capabilities:
- Research report structure and formatting
- Scientific writing (Korean/English bilingual)
- Data visualization descriptions
- Grant application narratives
- Protocol development

Guidelines:
1. Clear, concise writing style
2. Proper scientific nomenclature
3. Logical flow and structure
4. Evidence-based conclusions
5. Proper citations and references

Output format:
# Title
## Abstract
## Introduction
## Methods
## Results
## Discussion
## Conclusion
## References
""",
            
            "biomedical_research": """You are Qwen3.6, an expert biomedical research AI for the ARP drug discovery system.

Your task is to assist with target discovery, compound analysis, and therapeutic development.

Capabilities:
- Target identification and prioritization
- Pathway analysis (TGF-β, AMPK, YAP/TAZ, etc.)
- Compound property analysis (ADMET, drug-likeness)
- Biomarker identification
- Clinical trial design considerations

Available disease areas:
- Sarcopenia (muscle wasting)
- Cardiac Fibrosis
- Heart Failure (HFrEF/HFpEF)
- MASLD/NASH
- Lung Fibrosis

Target classes:
- Cytokines (IL-11, IL-6)
- Enzymes (LOXL2, PIN1)
- Transcription factors (YAP/TAZ, MRTF-A)
- Receptors (NPRC, FAP)

Guidelines:
1. Evidence-based reasoning
2. Consider translational potential
3. Address safety and efficacy
4. Reference clinical development stage
5. Suggest experimental validation

Output format:
## Target/Compound Overview
## Mechanism of Action
## Evidence Summary
## Development Considerations
## Recommendations
"""
        }
        
        return prompts.get(task_type, prompts["biomedical_research"])
    
    def generate_task_prompt(self, 
                           task: str, 
                           context: Optional[Dict[str, Any]] = None) -> str:
        """Generate detailed task prompt with context"""
        
        prompt = f"## Task\n{task}\n\n"
        
        if context:
            prompt += "## Context\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        prompt += """## Instructions
1. Analyze the task carefully
2. Provide a comprehensive response
3. Include specific details and reasoning
4. Suggest actionable recommendations
5. Cite relevant sources where applicable
"""
        
        return prompt
    
    def create_api_request(self,
                          messages: List[Dict[str, str]],
                          task_type: str = "biomedical_research") -> Dict[str, Any]:
        """Create API request payload"""
        
        return {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "max_tokens": self.config.max_tokens,
            "stream": False
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities summary"""
        
        return {
            "model": self.config.model_name,
            "type": self.config.model_type,
            "parameters": {
                "total": f"{self.config.total_parameters:,}",
                "activated": f"{self.config.activated_parameters:,}",
                "experts": self.config.num_experts,
                "activated_experts": self.config.activated_experts
            },
            "context": {
                "native": f"{self.config.context_length:,}",
                "extended": f"{self.config.max_context:,}"
            },
            "vision": self.config.vision_support,
            "tasks": [
                "code_generation",
                "literature_analysis", 
                "report_writing",
                "biomedical_research"
            ],
            "benchmarks": {
                "swe_bench_verified": "75.0%",
                "coding_agent": "Best among 35B models",
                "mmlu_pro": "86.1%",
                "context_length": "262K tokens"
            }
        }


def setup_qwen36_subagent() -> Qwen36SubAgent:
    """Setup and return Qwen3.6-35B-A3B subagent instance"""
    
    config = Qwen36Config()
    agent = Qwen36SubAgent(config)
    
    print("=" * 60)
    print("Qwen3.6-35B-A3B SubAgent Configuration")
    print("=" * 60)
    print(f"Model: {config.model_name}")
    print(f"Parameters: {config.total_parameters:,} total / {config.activated_parameters:,} active")
    print(f"Experts: {config.num_experts} (activated: {config.activated_experts})")
    print(f"Context: {config.context_length:,} tokens (max: {config.max_context:,})")
    print(f"Vision: {'Yes' if config.vision_support else 'No'}")
    print()
    print("Capabilities:")
    for task in ["code_generation", "literature_analysis", "report_writing", "biomedical_research"]:
        print(f"  • {task}")
    print()
    print("Setup Commands:")
    print()
    print("SGLang (recommended):")
    print(agent.setup_api("sglang"))
    print()
    print("vLLM:")
    print(agent.setup_api("vllm"))
    print()
    
    return agent


if __name__ == "__main__":
    agent = setup_qwen36_subagent()
    
    # Display full capabilities
    caps = agent.get_capabilities()
    print("Full Capabilities:")
    print(json.dumps(caps, indent=2))