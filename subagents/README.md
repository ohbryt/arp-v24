# Qwen3.6-35B-A3B SubAgent for ARP Pipeline

## Overview

**Qwen3.6-35B-A3B** from Alibaba is integrated as a specialized subagent for the Enhanced ARP (Autonomous Research Pipeline) v24 system.

## Model Specifications

| Spec | Value |
|------|-------|
| **Model** | Qwen/Qwen3.6-35B-A3B |
| **Parameters** | 35B total / 3B activated (MoE) |
| **Experts** | 256 (8 routed + 1 shared) |
| **Context Length** | 262K tokens (1M+ extended) |
| **Vision** | Yes (Vision Encoder included) |
| **License** | Apache 2.0 |

## Capabilities

### 1. Code Generation
- Pipeline automation scripts
- Scientific computing (NumPy, Pandas, RDKit)
- API integrations
- Test generation

### 2. Literature Analysis
- PubMed/MEDLINE synthesis
- Clinical trial interpretation
- Mechanism of action analysis
- Target validation

### 3. Report Writing
- Research reports (Korean/English)
- Grant proposals
- Protocol documentation
- Scientific publications

### 4. Biomedical Research
- Target discovery and prioritization
- Pathway analysis
- ADMET interpretation
- Clinical development planning

## Benchmark Performance

| Benchmark | Score | Notes |
|-----------|-------|-------|
| SWE-bench Verified | **75.0%** | Best among 35B models |
| Coding Agent | **Best** | Repository-level reasoning |
| MMLU-Pro | 86.1% | General knowledge |
| Context Length | 262K | Long document processing |

## Setup

### 1. SGLang (Recommended)

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen3.6-35B-A3B \
  --port 8000 \
  --tp-size 8 \
  --mem-fraction-static 0.8 \
  --context-length 262144 \
  --reasoning-parser qwen3
```

### 2. vLLM

```bash
vllm serve Qwen/Qwen3.6-35B-A3B \
  --port 8000 \
  --tensor-parallel-size 8 \
  --max-model-len 262144 \
  --reasoning-parser qwen3
```

### 3. Tool Use

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen3.6-35B-A3B \
  --tool-call-parser qwen3_coder
```

## Usage in ARP Pipeline

```python
from subagents.qwen36_agent import Qwen36SubAgent, setup_qwen36_subagent

# Setup agent
agent = setup_qwen36_subagent()

# Get specialized prompt
system_prompt = agent.get_system_prompt("code_generation")

# Generate task prompt
task = "Write a function to calculate Lipinski's rule of 5"
context = {
    "input": "SMILES string",
    "output": "Dictionary with MW, LogP, HBA, HBD",
    "libraries": "RDKit"
}
prompt = agent.generate_task_prompt(task, context)

# Create API request
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
]
request = agent.create_api_request(messages)
```

## Integration with ARP v24

The Qwen3.6-35B-A3B subagent is designed to work with:

- **ARP v22**: Disease pack targets and pathways
- **BioContext MCP**: Real-time database access
- **DrugBLIP**: 3D molecular docking
- **CLAIRE**: Protein design
- **Cocrystal Predictor**: Bioavailability enhancement
- **FoliStatin-X**: Natural compound formulation

## Task Specialization

### Code Generation
```
System: Expert coding assistant for drug discovery pipelines
Focus: Python, APIs, RDKit, scientific computing
```

### Literature Analysis
```
System: Biomedical research analyst
Focus: Target validation, mechanism of action, evidence synthesis
```

### Report Writing
```
System: Scientific writer (bilingual KR/EN)
Focus: Research reports, grants, protocols
```

### Biomedical Research
```
System: Drug discovery expert
Focus: Targets, pathways, compounds, clinical development
```

## Model Advantages for ARP

1. **Long Context**: Analyze entire papers (262K tokens)
2. **Coding Ability**: SWE-bench 75% - pipeline automation
3. **Multimodal**: Vision + text for figure analysis
4. **Multilingual**: Korean + English documentation
5. **Efficient**: 3B active params (vs 100B+ models)
6. **Apache 2.0**: Commercial use allowed

## Resources

- **Model**: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
- **GitHub**: https://github.com/QwenLM/Qwen3.6
- **Blog**: https://qwen.ai

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | 2026-04-18 | Initial integration |

---

**Note**: This subagent requires GPU infrastructure with ~8x80GB VRAM for optimal performance.