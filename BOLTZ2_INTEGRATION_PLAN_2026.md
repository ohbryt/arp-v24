# Boltz-2 Integration Plan 2026
## ARP Pipeline Upgrade: From "Last Mile Problem" Paper to Production

**Date:** 2026-05-10  
**Reference Paper:** Wang et al. 2026, *J. Chem. Inf. Model.*, PMID 42095677  
**Integration Target:** arp-v24 pipeline (`arp_cli.py`, `arp_db.py`, `arp_pipeline.py`)  
**Status:** Research Complete — Implementation Ready

---

## 1. Paper Summary: The Last Mile Problem

### 1.1 Core Problem
Docking-based virtual screening (VS) has high false-positive rates, causing expensive downstream experimental failures. Physics-based alchemical free-energy (ABFE) methods improve hit rates but are computationally prohibitive at scale.

### 1.2 Study Design
- **PDBbind set:** 632 ligand-protein complexes → assess ABFE quantitative accuracy
- **DUD-E set:** 315 binders + decoys → evaluate VS predictive power (active vs. decoy discrimination)
- **Methods benchmarked:** Alchemical ABFE, end-state physics methods, 5 ML models

### 1.3 Key Findings

| Method | PDBbind Correlation | DUD-E Enrichment | Cost |
|--------|-------------------|-----------------|------|
| Alchemical ABFE | ✅ High | ✅ Highest | ����� (very high) |
| End-state physics | ⚠️ Low | ✅ Good | ��� |
| GNINA | ✅ Moderate | ✅ Good | � |
| **Boltz-2** | ✅ Good | ✅ Good | �� |
| Most ML models | ⚠️ Training overlap | ❌ Failed | � |

### 1.4 Critical Insight
> **"A staged approach involving Boltz-2 as a primary filter followed by alchemical ABFE is likely to robustly and cost-efficiently enrich docking-based VS hit lists with true actives."**

Boltz-2 was the **only ML model** that generalized to unseen data (DUD-E) comparably to physics-based methods — while being 1000x faster than FEP.

### 1.5 Two Affinity Outputs from Boltz-2
- **`affinity_probability_binary`** (0–1): probability ligand is a binder → **hit discovery**
- **`affinity_pred_value`** (log IC50 μM): specific affinity ranking → **hit-to-lead optimization**

---

## 2. Boltz-2 Architecture Deep-Dive

### 2.1 Model Description
Boltz-2 is a biomolecular foundation model that **jointly predicts complex structure + binding affinity**, surpassing AlphaFold3 and Boltz-1. It is the first deep learning model to approach FEP accuracy at 1000x lower computational cost.

### 2.2 Licensing
**MIT License** — fully open source for academic AND commercial use.

### 2.3 Two Access Options

#### Option A: NVIDIA NIM (Cloud/Self-Hosted Container)
- **Container:** `nvcr.io/nim/mit/boltz2:1.6.0`
- **Registry:** NVIDIA NGC (`ngc.nvidia.com`)
- **API Endpoint:** `http://localhost:8000/v1/health/ready` → `/biology/mit/boltz2/predict`
- **Hardware:** A100, B200, H100, H200, GB200, RTX 6000 Ada, GH200, L40S, GB10 (DGX Spark)
- **Initial download:** 2–10 hours (100+ Mbps connection)
- **Requires:** NGC API Key, Docker, NVIDIA GPU with drivers

#### Option B: Local pip Installation (Open Source)
```bash
# Recommended GPU install
pip install boltz[cuda] -U

# Or from GitHub for daily updates
git clone https://github.com/jwohlwend/boltz.git
cd boltz && pip install -e .[cuda]

# Run inference
boltz predict input_path --use_msa_server
```
- **MSA Server:** ColabFold MSA generation (auto-enabled with `--use_msa_server`)
- **Requires:** CUDA GPU, ~16GB VRAM for typical proteins

### 2.4 Performance Benchmarks (H100 TensorRT)

**Structure Prediction:**
| Sequence Length | Time (s) |
|----------------|---------|
| ~200 aa | 1.72 |
| ~500 aa | 6.63 |
| ~1200 aa | 24.67 |
| ~2000 aa | 79.55 |

**Binding Affinity Prediction:**
| Sequence Length | Time (s) |
|----------------|---------|
| ~200 aa | 6.21 |
| ~500 aa | 10.74 |
| ~1200 aa | 29.69 |
| ~2000 aa | 81.19 |

**TensorRT vs OSS:** ~2–6x speedup on H100

### 2.5 NIM API Request Format

```python
import requests

url = "http://localhost:8000/biology/mit/boltz2/predict"
headers = {"accept": "application/json", "Content-Type": "application/json"}

payload = {
    "polymers": [
        {
            "id": "A",
            "molecule_type": "protein",
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
        }
    ],
    "ligands": [
        {
            "id": "L",
            "smiles": "CC(=O)Oc1ccccc1C(=O)O",
            "predict_affinity": True
        }
    ],
    "recycling_steps": 3,
    "sampling_steps": 50,
    "diffusion_samples": 1,
    "sampling_steps_affinity": 200,
    "diffusion_samples_affinity": 5
}

response = requests.post(url, json=payload, headers=headers)
```

**Response fields:**
- `structures[].structure` — mmCIF format structure
- `structures[].confidence_scores` — confidence per residue
- `affinities` — `{ligand_id: {affinity_pic50, affinity_pred_value, affinity_probability_binary}}`
- `metrics` — runtime metrics

---

## 3. Current ARP Architecture (What We Have)

### 3.1 Key Files
```
arp-v24/
├── arp_cli.py           # 382 lines — CLI command interface
├── arp_db.py            # 395 lines — DuckDB local cache
├── arp_pipeline.py      # ~440 lines — Integrated pipeline w/ stub BoltzIntegration
├── core/                # Scoring engine, candidate engine, modality routing
├── ai_integration/      # Molecular DL, multi-omics, SHAP analysis
└── scripts/             # Literature, infographic generation
```

### 3.2 Existing BoltzIntegration Stub (arp_pipeline.py lines 52–125)

The `BoltzIntegration` class already exists but is a **stub**:
- Checks for local `boltz` binary via `which boltz`
- Falls back to `_predict_simulated()` (random values)
- No real NIM integration
- No YAML input generation for the open-source CLI
- No affinity parsing from actual output

### 3.3 Existing Database Schema (arp_db.py)

Tables: `targets`, `pdb_structures`, `compounds`, `inhibitors`, `screening_results`, `abfe_calculations`

**Missing for Boltz-2:** No table for Boltz-2 predictions, no affinity scores stored.

---

## 4. Integration Plan

### 4.1 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     arp_pipeline.py                              │
│                  (ARP Integrated Pipeline)                       │
│                                                                  │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────────┐    │
│  │ arp_cli.py│──▶│  arp_db.py   │──▶│  BoltzIntegration   │    │
│  │  (CLI)   │   │  (DuckDB)    │   │  (NEW: boltz2_       │    │
│  └──────────┘   └──────────────┘   │     client.py)       │    │
│                                     └──────────┬───────────┘    │
│                                                │                │
│                        ┌───────────────────────┴────────────┐   │
│                        │         Route Decision              │   │
│                        │  NIM Available? → Local boltz CLI?  │   │
│                        └───────────────┬────────────────────┘   │
│                      ┌──▼──────┐              │                 │
│                      │ NVIDIA  │              │                 │
│                      │ NIM API │              │ Local pip       │
│                      │:8000    │              │ boltz CLI       │
│                      └──┬──────┘              │                 │
│                         │                     │                 │
│                    ┌────▼─────────────────────▼────┐           │
│                    │  /biology/mit/boltz2/predict   │           │
│                    │  or boltz predict input.yaml   │           │
│                    └────────────┬──────────────────┘           │
│                             ┌───▼──────┐                       │
│                             │ Boltz-2  │                        │
│                             │  Model   │                        │
│                             └───┬──────┘                       │
│                             ┌───▼──────┐                       │
│                    ┌────────│  Parse   │────────┐               │
│                    │        │ Results  │        │               │
│                    │        └──────────┘        │               │
│           ┌────────▼────────┐        ┌───────────▼──────────┐   │
│           │ Store in DuckDB│        │ ABFEIntegration      │   │
│           │ (arp_db.py)    │        │ (Stage 2: GROMACS)   │   │
│           └────────────────┘        └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Module Architecture

```
arp-v24/
├── boltz2/
│   ├── __init__.py                  # Package init
│   ├── client.py                    # Core: NIM + local CLI abstraction
│   ├── yaml_builder.py              # Build input YAML for local boltz CLI
│   ├── parser.py                    # Parse boltz JSON/mmcif output
│   ├── db.py                        # DuckDB schema for Boltz-2 results
│   └── config.py                    # Config: endpoint URL, cache, GPU selection
├── arp_pipeline.py                  # Updated: replace stub with real integration
├── arp_db.py                        # Updated: add boltz2_predictions table
└── arp_cli.py                       # Updated: new commands for Boltz-2 screening
```

---

## 5. Implementation Roadmap

### Phase 0: Environment Setup (1–2 hours)

**Step 0.1 — Choose Access Mode:**

| Mode | Pros | Cons | Best For |
|------|------|------|----------|
| **NVIDIA NIM** | Optimized TensorRT, enterprise support, easy | NGC API key needed, 2-10h first download | Production with A100/H100 |
| **Local pip (OSS)** | Free, MIT license, full control | Manual CUDA setup, slower OSS backend | Development, RTX machines |

**For Dr. OCM's Mac Mini (M4 Pro):** NIM Docker won't work (no NVIDIA GPU). Use local pip + Ollama fallback.

**Step 0.2 — Local Installation:**
```bash
# Create fresh env
conda create -n boltz2 python=3.10 -y
conda activate boltz2

# Install boltz with CUDA support
pip install boltz[cuda] -U

# Verify
boltz --version

# MSA server (optional but recommended for better accuracy)
# Uses ColabFold under the hood — no extra install needed
boltz predict input.yaml --use_msa_server
```

### Phase 1: Core Client Module (boltz2/client.py) — 3–4 hours

```python
# boltz2/client.py — Core abstraction layer

import os
import subprocess
import requests
import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

class BoltzMode(Enum):
    NIM = "nim"        # NVIDIA NIM container
    LOCAL = "local"    # pip-installed boltz CLI

@dataclass
class BoltzConfig:
    mode: BoltzMode = BoltzMode.NIM
    nim_url: str = "http://localhost:8000/biology/mit/boltz2/predict"
    nim_health: str = "http://localhost:8000/v1/health/ready"
    local_cmd: str = "boltz"
    msa_server: bool = True

class Boltz2Client:
    """
    Unified Boltz-2 client supporting both NIM and local CLI.
    
    Usage:
        client = Boltz2Client(mode=BoltzMode.LOCAL)
        result = client.predict_affinity(
            protein_sequence="MVNID...",
            ligand_smiles="CC(=O)Oc1ccccc1C(=O)O",
            protein_id="DGAT1"
        )
    """
    
    def __init__(self, config: Optional[BoltzConfig] = None):
        self.config = config or BoltzConfig()
        self._detect_mode()
    
    def _detect_mode(self) -> None:
        """Auto-detect best available mode"""
        # Try NIM first
        try:
            r = requests.get(self.config.nim_health, timeout=3)
            if r.status_code == 200:
                self.config.mode = BoltzMode.NIM
                return
        except:
            pass
        
        # Fall back to local
        try:
            subprocess.run(
                [self.config.local_cmd, "--version"],
                capture_output=True, timeout=5
            )
            self.config.mode = BoltzMode.LOCAL
        except:
            raise RuntimeError(
                "Boltz-2 not available. Install via: pip install boltz[cuda] -U"
            )
    
    def is_nim_available(self) -> bool:
        """Check if NIM is running"""
        return self.config.mode == BoltzMode.NIM
    
    def predict_affinity(
        self,
        protein_sequence: str,
        ligand_smiles: str,
        protein_id: str = "A",
        ligand_id: str = "L",
        sampling_steps: int = 50,
        sampling_steps_affinity: int = 200,
        diffusion_samples_affinity: int = 5,
    ) -> Dict[str, Any]:
        """
        Predict protein-ligand binding affinity.
        
        Returns:
            {
                "affinity_pred_value": float,   # log10(IC50) μM
                "affinity_probability_binary": float,  # 0-1 probability
                "affinity_pic50": float,         # pIC50
                "confidence_score": float,
                "structure_mmcif": str,
                "method": "boltz2-nim" | "boltz2-local"
            }
        """
        if self.config.mode == BoltzMode.NIM:
            return self._predict_via_nim(...)
        else:
            return self._predict_via_local(...)
    
    def _predict_via_nim(self, ...) -> Dict[str, Any]:
        """POST to NIM /biology/mit/boltz2/predict"""
        payload = {
            "polymers": [{
                "id": protein_id,
                "molecule_type": "protein",
                "sequence": protein_sequence
            }],
            "ligands": [{
                "id": ligand_id,
                "smiles": ligand_smiles,
                "predict_affinity": True
            }],
            "sampling_steps": sampling_steps,
            "sampling_steps_affinity": sampling_steps_affinity,
            "diffusion_samples_affinity": diffusion_samples_affinity,
            "recycling_steps": 3,
            "diffusion_samples": 1,
            "output_format": "mmcif"
        }
        
        response = requests.post(
            self.config.nim_url,
            json=payload,
            headers={"accept": "application/json", "Content-Type": "application/json"},
            timeout=120
        )
        response.raise_for_status()
        return self._parse_nim_response(response.json())
    
    def _predict_via_local(self, ...) -> Dict[str, Any]:
        """Write YAML, run `boltz predict`, parse JSON output"""
        # Generate YAML input
        yaml_content = self._build_yaml_input(protein_sequence, ligand_smiles, ...)
        
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name
        
        try:
            cmd = [self.config.local_cmd, "predict", yaml_path]
            if self.config.msa_server:
                cmd.append("--use_msa_server")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                raise RuntimeError(f"Boltz CLI failed: {result.stderr}")
            
            return self._parse_local_output(result.stdout, yaml_path)
        finally:
            os.unlink(yaml_path)
    
    def _build_yaml_input(self, ...) -> str:
        """Build YAML for boltz CLI input format"""
        # (see Section 5.2 below)
        pass
    
    def _parse_nim_response(self, response: Dict) -> Dict[str, Any]:
        """Extract affinity from NIM JSON response"""
        structure = response["structures"][0]
        affinities = structure.get("affinities", {})
        ligand_affinity = affinities.get("L", {})
        
        return {
            "affinity_pred_value": ligand_affinity.get("affinity_pred_value"),
            "affinity_probability_binary": ligand_affinity.get("affinity_probability_binary"),
            "affinity_pic50": ligand_affinity.get("affinity_pic50"),
            "confidence_score": structure.get("confidence_scores", [0])[0],
            "structure_mmcif": structure.get("structure"),
            "method": "boltz2-nim"
        }
```

### Phase 2: YAML Builder (boltz2/yaml_builder.py) — 1–2 hours

Boltz CLI uses YAML input format (not JSON like NIM):

```yaml
# Example: input.yaml for boltz CLI
protein:
  id: A
  sequence: MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN

ligands:
  - id: L
    smiles: CC(=O)Oc1ccccc1C(=O)O
    predict_affinity: true

params:
  recycling_steps: 3
  sampling_steps: 50
  sampling_steps_affinity: 200
  diffusion_samples: 1
  diffusion_samples_affinity: 5
```

### Phase 3: DuckDB Schema Extension — 1 hour

```sql
-- Add to arp_db.py init_schema()
CREATE TABLE IF NOT EXISTS boltz2_predictions (
    id INTEGER PRIMARY_KEY,
    target_uniprot VARCHAR,
    protein_sequence TEXT,
    ligand_smiles TEXT,
    affinity_pred_value DOUBLE,
    affinity_probability_binary DOUBLE,
    affinity_pic50 DOUBLE,
    confidence_score DOUBLE,
    structure_mmcif TEXT,
    method VARCHAR,  -- 'boltz2-nim' or 'boltz2-local'
    runtime_seconds DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (target_uniprot) REFERENCES targets(uniprot_id)
);

CREATE TABLE IF NOT EXISTS boltz2_screening_results (
    id INTEGER PRIMARY_KEY,
    batch_id VARCHAR,
    target_uniprot VARCHAR,
    ligand_smiles TEXT,
    rank INTEGER,
    boltz_score DOUBLE,
    affinity_probability DOUBLE,
    selected_for_abfe BOOLEAN,
    abfe_dG_kcal_mol DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Phase 4: Pipeline Integration — 2–3 hours

**Replace stub in `arp_pipeline.py`:**

```python
# OLD (stub) — lines 52-125
class BoltzIntegration:
    BOLTZ_API_URL = "https://api.boltz.nuxt.ai/predict"  # Placeholder
    BOLTZ_LOCAL_CMD = "boltz"
    
    @staticmethod
    def is_available():
        try:
            result = subprocess.run(["which", "boltz"], capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def predict_affinity(protein_pdb, ligand_sdf):
        if BoltzIntegration.is_available():
            return BoltzIntegration._predict_local(protein_pdb, ligand_sdf)
        return BoltzIntegration._predict_simulated()
```

**NEW:**
```python
from boltz2 import Boltz2Client, BoltzMode, BoltzConfig

class BoltzIntegration:
    """Boltz-2 binding affinity — Stage 1 of Last Mile Problem staged approach"""
    
    _client: Optional[Boltz2Client] = None
    
    @classmethod
    def get_client(cls) -> Boltz2Client:
        if cls._client is None:
            cls._client = Boltz2Client()
        return cls._client
    
    @classmethod
    def is_available(cls) -> bool:
        try:
            client = cls.get_client()
            return True
        except RuntimeError:
            return False
    
    @classmethod
    def predict_affinity(cls, protein_sequence: str, ligand_smiles: str, **kwargs):
        """Predict binding affinity using Boltz-2 (NIM or local)"""
        client = cls.get_client()
        return client.predict_affinity(
            protein_sequence=protein_sequence,
            ligand_smiles=ligand_smiles,
            **kwargs
        )
    
    @classmethod
    def screen_compounds(
        cls, 
        target_sequence: str, 
        ligand_smiles_list: List[str],
        top_n: int = 50
    ) -> List[Dict]:
        """
        Screen compound library using Boltz-2.
        Stage 1 of the Last Mile Problem staged approach.
        
        Args:
            target_sequence: Protein amino acid sequence
            ligand_smiles_list: List of SMILES strings
            top_n: Number of top-scoring compounds to return
        
        Returns:
            List of dicts with rank, SMILES, probability_binary, pred_value
        """
        results = []
        client = cls.get_client()
        
        for i, smiles in enumerate(ligand_smiles_list):
            try:
                result = client.predict_affinity(
                    protein_sequence=target_sequence,
                    ligand_smiles=smiles
                )
                results.append({
                    'rank': i + 1,
                    'smiles': smiles,
                    'affinity_probability': result['affinity_probability_binary'],
                    'affinity_pred_value': result['affinity_pred_value'],
                    'confidence': result['confidence_score'],
                    'method': result['method']
                })
            except Exception as e:
                print_warning(f"  Failed for SMILES {smiles[:30]}...: {e}")
        
        # Sort by probability_binary (hit discovery mode)
        results.sort(key=lambda x: x['affinity_probability'], reverse=True)
        for i, r in enumerate(results):
            r['rank'] = i + 1
        
        return results[:top_n]
```

### Phase 5: CLI Commands — 1–2 hours

```python
# Add to arp_cli.py

def cmd_boltz_screen(args):
    """
    Screen compounds using Boltz-2
    python arp_cli.py boltz-screen --target DGAT1 --smiles_file compounds.smi --top 50
    """
    from boltz2 import Boltz2Client
    import time
    
    target = args.target.upper()
    db = ARPLocalDB()
    db.connect()
    
    # Get target sequence from DB
    target_info = db.search_target(target)
    if not target_info:
        print_error(f"Target {target} not found in database")
        return
    
    # Load SMILES from file
    with open(args.smiles_file) as f:
        smiles_list = [l.strip().split(',')[0] for l in f if l.strip()]
    
    print_info(f"Screening {len(smiles_list)} compounds against {target}...")
    start = time.time()
    
    results = BoltzIntegration.screen_compounds(
        target_sequence=target_info.iloc[0]['sequence'],
        ligand_smiles_list=smiles_list,
        top_n=args.top
    )
    
    elapsed = time.time() - start
    print_success(f"Screened {len(smiles_list)} compounds in {elapsed:.1f}s")
    
    # Store results
    db.store_boltz_results(target, results)
    
    # Print top hits
    print_header(f"\n🏆 Top {args.top} Hits")
    for r in results[:args.top]:
        print(f"  #{r['rank']}: prob={r['affinity_probability']:.3f} "
              f"logIC50={r['affinity_pred_value']:.2f}  {r['smiles'][:40]}...")
    
    db.close()

def cmd_boltz_status(args):
    """Check Boltz-2 availability and mode"""
    if BoltzIntegration.is_available():
        client = BoltzIntegration.get_client()
        mode = client.config.mode.value
        print_success(f"Boltz-2 available via {mode}")
    else:
        print_error("Boltz-2 not available")
        print_info("Install: pip install boltz[cuda] -U")
```

---

## 6. CLI Command Reference

```bash
# ============================================================
# BOLTZ-2 COMMANDS
# ============================================================

# Check availability
python arp_cli.py boltz-status

# Single prediction
python arp_cli.py boltz-predict \
    --protein_sequence "MVNIDIAIAMAI..." \
    --ligand_smiles "CC(=O)Oc1ccccc1C(=O)O" \
    --target DGAT1

# Screen compound file (SMILES one per line)
python arp_cli.py boltz-screen \
    --target DGAT1 \
    --smiles_file ./compounds.smi \
    --top 50

# Full pipeline (Boltz-2 → ABFE)
python arp_pipeline.py discover DGAT1 \
    --depth full \
    --screen ./compounds.smi \
    --stage1_btz --stage2_abfe
```

---

## 7. NIM Deployment (For GPU Servers)

```bash
# Step 1: Install prerequisites
brew install docker ngccli    # macOS
# or on Linux:
# curl -fsSL https://get.docker.com | sh
# pip install ngc-cli

# Step 2: Login to NGC
ngc registry user login

# Step 3: Pull NIM container
docker pull nvcr.io/nim/mit/boltz2:1.6.0

# Step 4: Run container
export LOCAL_NIM_CACHE=~/.cache/nim
export NGC_API_KEY=<your-ngc-api-key>

docker run --rm --name boltz2 --runtime=nvidia \
  --shm-size=16G \
  -e NGC_API_KEY \
  -v $LOCAL_NIM_CACHE:/opt/nim/.cache \
  -p 8000:8000 \
  nvcr.io/nim/mit/boltz2:1.6.0

# Step 5: Health check
curl -X GET 'http://localhost:8000/v1/health/ready' \
  -H 'accept: application/json'

# Step 6: Test prediction
curl -X POST 'http://localhost:8000/biology/mit/boltz2/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "polymers": [{"id": "A", "molecule_type": "protein", "sequence": "MVNIDIAIAMAI"}],
    "ligands": [{"id": "L", "smiles": "CC(=O)O", "predict_affinity": true}],
    "sampling_steps": 50,
    "sampling_steps_affinity": 200
  }'
```

---

## 8. File Manifest (New Modules)

| File | Purpose | LOC Est. |
|------|---------|---------|
| `boltz2/__init__.py` | Package exports | ~20 |
| `boltz2/client.py` | Core NIM + local CLI client | ~200 |
| `boltz2/yaml_builder.py` | YAML input generator for local CLI | ~80 |
| `boltz2/parser.py` | Output parsers (JSON, mmCIF) | ~60 |
| `boltz2/db.py` | DuckDB insert/query for Boltz-2 results | ~100 |
| `boltz2/config.py` | Config dataclass + env var loading | ~40 |
| `boltz2/__main__.py` | CLI entry: `python -m boltz2` | ~60 |
| **Total new code** | | **~560** |

**Modified files:**
| File | Changes |
|------|---------|
| `arp_pipeline.py` | Replace stub `BoltzIntegration` class with real client |
| `arp_db.py` | Add `boltz2_predictions` and `boltz2_screening_results` tables |
| `arp_cli.py` | Add `boltz-status`, `boltz-predict`, `boltz-screen` commands |

---

## 9. Testing Plan

```python
# boltz2/test_client.py

def test_nim_mode():
    """Test against running NIM container"""
    client = Boltz2Client()
    assert client.config.mode == BoltzMode.NIM
    
    result = client.predict_affinity(
        protein_sequence="MVNIDIAIAMAI",
        ligand_smiles="CC(=O)O",
    )
    assert 0 <= result['affinity_probability_binary'] <= 1
    assert result['structure_mmcif'] is not None

def test_local_mode():
    """Test local boltz CLI"""
    client = Boltz2Client(config=BoltzConfig(mode=BoltzMode.LOCAL))
    result = client.predict_affinity(
        protein_sequence="MVNIDIAIAMAI",
        ligand_smiles="CC(=O)O",
    )
    assert result['method'] == 'boltz2-local'

def test_screening_pipeline():
    """Test full screening workflow"""
    smiles = ["CC(=O)O", "c1ccccc1", "CCO"]
    results = BoltzIntegration.screen_compounds(
        target_sequence="MVNIDIAIAMAI",
        ligand_smiles_list=smiles,
        top_n=3
    )
    assert len(results) <= 3
    assert all('affinity_probability' in r for r in results)
```

---

## 10. Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| NIM container download too slow (>10h) | Medium | Use local pip install as fallback |
| Boltz CLI output format changes | Low | Pin boltz version: `pip install boltz==1.6.0` |
| GPU OOM on large proteins | Medium | Cap sequence length at 2000 aa; skip MSA for large hits |
| NIM API auth failure | Low | Store NGC_API_KEY in env, validate on startup |
| DuckDB schema conflict | Low | `CREATE TABLE IF NOT EXISTS` handles existing DBs |

---

## 11. Quick Start Commands

```bash
# 1. Install Boltz-2 locally
conda create -n boltz2 python=3.10 -y && conda activate boltz2
pip install boltz[cuda] -U

# 2. Verify installation
boltz --version

# 3. Create boltz2/ package directory
mkdir -p arp-v24/boltz2

# 4. Create __init__.py
echo 'from .client import Boltz2Client, BoltzMode, BoltzConfig' > arp-v24/boltz2/__init__.py

# 5. Test single prediction
python -c "
from arp_v24.boltz2 import Boltz2Client
client = Boltz2Client()
print(client.predict_affinity('MVNIDIAIAMAI', 'CC(=O)O'))
"

# 6. Run full pipeline
python arp_pipeline.py discover DGAT1 --depth full --screen ./test.smi
```

---

## 12. Key References

- **Paper (PMID 42095677):** https://pubmed.ncbi.nlm.nih.gov/42095677/
- **Boltz-2 NIM Docs:** https://docs.nvidia.com/nim/bionemo/boltz2/latest/
- **GitHub (MIT licensed):** https://github.com/jwohlwend/boltz
- **Boltz-2 bioRxiv:** https://doi.org/10.1101/2025.06.14.659707
- **Boltz-1 bioRxiv:** https://doi.org/10.1101/2024.11.19.624167
- **NVIDIA NIM API Ref:** https://docs.api.nvidia.com/nim/reference/mit-boltz2

---

*Report generated: 2026-05-10. Research subagent: completed.*
