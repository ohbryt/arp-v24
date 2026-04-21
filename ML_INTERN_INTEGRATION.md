# Hugging Face ml-intern Integration for ARP v24

## ml-intern: Open-Source ML Engineer

**Repository:** https://github.com/huggingface/ml-intern  
**Purpose:** Autonomous ML agent that reads papers, trains models, and ships ML code

---

## Installation

```bash
cd ~/.openclaw/workspace/arp-v24
git clone https://github.com/huggingface/ml-intern.git
cd ml-intern
uv sync
uv tool install -e .
```

**CLI Location:** `~/.local/bin/ml-intern`

---

## Setup

Create `.env` file:

```bash
# Hugging Face token (required)
HF_TOKEN=<your-hf-token>

# GitHub PAT (for code search)
GITHUB_TOKEN=<github-pat>

# Anthropic API key (if using Claude models)
ANTHROPIC_API_KEY=<your-key>
```

---

## Usage Modes

### Interactive Mode (Chat)
```bash
ml-intern
```

### Headless Mode (Single Prompt)
```bash
ml-intern "fine-tune llama on my dataset"
ml-intern --no-stream "research about one-carbon metabolism"
```

### Options
```bash
--model <model>          # e.g., anthropic/claude-opus-4-6
--max-iterations <n>     # Max iterations (default 300)
--no-stream             # Disable streaming
```

---

## Architecture

```
User Input → Agentic Loop (max 300 iterations)
├── ContextManager (auto-compaction at 170k tokens)
├── ToolRouter
│   ├── HF docs & research
│   ├── HF repos, datasets, jobs, papers
│   ├── GitHub code search
│   ├── Sandbox & local tools
│   ├── Planning
│   └── MCP server tools
├── Doom Loop Detector
└── litellm (multi-provider LLM)
```

---

## Events Emitted

| Event | Description |
|-------|-------------|
| `processing` | Starting to process user input |
| `ready` | Agent ready for input |
| `assistant_chunk` | Streaming token chunk |
| `assistant_message` | Complete LLM response |
| `tool_call` | Tool being called |
| `tool_output` | Tool execution result |

---

## Integration with ARP v24

### 1. Literature Research
```bash
ml-intern "find recent papers about MTHFD2 cancer metabolism 2024-2025"
```

### 2. Dataset Discovery
```bash
ml-intern "find drug sensitivity datasets on Hugging Face"
```

### 3. Model Training
```bash
ml-intern "fine-tune a model for cancer metabolic pathway prediction"
```

### 4. Code Development
```bash
ml-intern "write a PyTorch module for SHMT1 activity prediction"
```

### 5. Multi-Agent Research
Can work alongside other agents for parallel research tasks.

---

## Dependencies

- Python ≥3.11
- litellm (multi-provider LLM)
- huggingface-hub
- datasets
- fastmcp (MCP server)
- rich (terminal UI)

---

## Key Features for ARP

| Feature | ARP Use Case |
|---------|--------------|
| Paper reading | Literature review automation |
| HF datasets access | Training data discovery |
| Model shipping | Deploy trained models to HF Hub |
| GitHub integration | Code search and collaboration |
| MCP tools | Extend with custom tools |

---

## Example: Literature Research

```python
# In Python or CLI
ml-intern "Research recent advances in one-carbon metabolism 
for cancer therapy, focusing on 2024-2025 publications"
```

---

## Connection to BOAT

BOAT (AstraZeneca) + ml-intern (HuggingFace) = **Full ML Pipeline**

- **BOAT**: Bayesian optimization for antibody/peptide design
- **ml-intern**: Research, paper reading, model training, deployment
- **Together**: End-to-end AI-driven drug discovery
