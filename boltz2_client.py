#!/usr/bin/env python3
"""
Boltz-2 Client: Integration with NVIDIA NIM or local boltz
===========================================================
Based on BOLTZ2_INTEGRATION_PLAN_2026.md

Usage:
    from boltz2_client import Boltz2Client
    client = Boltz2Client()
    result = client.predict(pdb_file="protein.pdb", ligand_sdf="compound.sdf")
"""

import json
import subprocess
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

# ============================================================
# CONFIGURATION
# ============================================================
@dataclass
class Boltz2Config:
    """Boltz-2 configuration"""
    mode: str = "local"  # "local" or "nimgateway" (NVIDIA NIM)
    
    # Local mode settings
    local_conda_env: str = "boltz2"
    local_model_path: Optional[str] = None
    
    # NVIDIA NIM settings  
    nimp_url: str = "https://health.api.nvidia.com/v1/biology/mit/boltz2/predict"
    nimp_api_key: Optional[str] = None  # From NVIDIA NGC API key
    
    # Common settings
    affinity_threshold: float = 0.5  # Binary hit threshold (0-1)
    affinity_unit: str = "prob"  # "prob" or "log_ic50"

class Boltz2Client:
    """
    Boltz-2 client for protein structure + binding affinity prediction.
    
    Access modes:
    1. Local (Mac M4 Pro): pip install boltz[cuda]
    2. NVIDIA NIM (GPU server): Docker container with TensorRT optimization
    
    Reference: Wang et al. 2026, J Chem Inf Model - "The Last Mile Problem"
    Boltz-2 was the only ML model that generalized to unseen DUD-E data.
    """
    
    def __init__(self, config: Optional[Boltz2Config] = None):
        self.config = config or Boltz2Config()
        self._check_availability()
    
    def _check_availability(self):
        """Check if Boltz-2 is available"""
        self.available = False
        self.mode = "unavailable"
        
        if self.config.mode == "local":
            try:
                result = subprocess.run(
                    ["which", "boltz"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    self.available = True
                    self.mode = "local"
                    return
            except:
                pass
            
            # Check if in conda env
            try:
                result = subprocess.run(
                    ["conda", "run", "-n", self.config.local_conda_env, "which", "boltz"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    self.available = True
                    self.mode = "local_conda"
                    return
            except:
                pass
        
        elif self.config.mode == "nimgateway":
            if self.config.nimp_api_key:
                self.available = True
                self.mode = "nimgateway"
    
    def status(self) -> Dict[str, Any]:
        """Check Boltz-2 status"""
        return {
            "available": self.available,
            "mode": self.mode,
            "config_mode": self.config.mode,
            "affinity_threshold": self.config.affinity_threshold,
            "recommendation": self._get_recommendation()
        }
    
    def _get_recommendation(self) -> str:
        """Get setup recommendation based on environment"""
        if self.available:
            return f"Boltz-2 ready in {self.mode} mode"
        
        if self.config.mode == "local":
            return (
                "Install: conda create -n boltz2 && conda activate boltz2 && "
                "pip install boltz[cuda] -U"
            )
        elif self.config.mode == "nimgateway":
            return "Set NVIDIA NGC API key or switch to local mode"
        
        return "Boltz-2 not available"
    
    def predict(
        self, 
        pdb_file: str,
        ligand_sdf: Optional[str] = None,
        chains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run Boltz-2 prediction.
        
        Args:
            pdb_file: PDB file path (protein structure)
            ligand_sdf: SDF file path (ligand, optional for apo prediction)
            chains: Chain IDs to predict (e.g., ["A", "B"] for hetero complexes)
        
        Returns:
            Dict with:
            - affinity_probability_binary: 0-1 (hit discovery)
            - affinity_pred_value: log IC50 (lead optimization)
            - structure: predicted complex structure
            - timing: inference time
        """
        if not self.available:
            return {
                "error": "Boltz-2 not available",
                "status": self.status()
            }
        
        if self.mode.startswith("local"):
            return self._predict_local(pdb_file, ligand_sdf, chains)
        elif self.mode == "nimgateway":
            return self._predict_nimgateway(pdb_file, ligand_sdf, chains)
    
    def _predict_local(
        self,
        pdb_file: str,
        ligand_sdf: Optional[str],
        chains: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Run prediction using local boltz CLI"""
        
        # Build YAML input
        yaml_content = self._build_input_yaml(pdb_file, ligand_sdf, chains)
        
        # Save to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name
        
        try:
            # Run boltz predict
            cmd = ["boltz", "predict", yaml_path, "--outdir", os.path.dirname(pdb_file)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )
            
            if result.returncode != 0:
                return {
                    "error": "boltz predict failed",
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            
            # Parse output
            return self._parse_boltz_output(result.stdout, pdb_file)
        
        finally:
            os.unlink(yaml_path)
    
    def _build_input_yaml(
        self,
        pdb_file: str,
        ligand_sdf: Optional[str],
        chains: Optional[List[str]]
    ) -> str:
        """Build boltz input YAML"""
        
        yaml = f"""model:
  name: boltz2_1
  config:
    diffusion:
      sampling_steps: 200
      channels: 384
      blocks: 18

input:
  pdb: {pdb_file}
"""
        if ligand_sdf:
            yaml += f"  ligand: {ligand_sdf}\n"
        
        if chains:
            yaml += f"  chains: {','.join(chains)}\n"
        
        yaml += """
output:
  directory: .
  log: true
"""
        return yaml
    
    def _parse_boltz_output(self, stdout: str, pdb_file: str) -> Dict[str, Any]:
        """Parse boltz CLI output"""
        
        # Parse affinity predictions from stdout
        # Format varies - capture key metrics
        output = {
            "status": "completed",
            "pdb": pdb_file,
            "timing": "unknown",  # Would parse from logs
        }
        
        # Look for affinity values
        for line in stdout.split('\n'):
            if 'affinity' in line.lower() or 'probability' in line.lower():
                # Parse affinity prediction
                parts = line.split()
                for i, p in enumerate(parts):
                    if 'affinity' in p.lower() and i+1 < len(parts):
                        try:
                            output['affinity_pred_value'] = float(parts[i+1])
                        except:
                            pass
        
        return output
    
    def _predict_nimgateway(
        self,
        pdb_file: str,
        ligand_sdf: Optional[str],
        chains: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Run prediction via NVIDIA NIM Gateway"""
        import requests
        
        # Read PDB file
        with open(pdb_file, 'r') as f:
            pdb_content = f.read()
        
        # Prepare request
        payload = {
            "pdb": pdb_content,
            "model_name": "boltz2_1",
            "diffusion_sampling_steps": 200,
        }
        
        if ligand_sdf:
            with open(ligand_sdf, 'r') as f:
                payload["ligand"] = f.read()
        
        if chains:
            payload["chain_ids"] = chains
        
        # Call NIM API
        headers = {
            "Authorization": f"Bearer {self.config.nimp_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                self.config.nimp_url,
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"NIM API error: {response.status_code}",
                    "detail": response.text
                }
        except Exception as e:
            return {"error": str(e)}
    
    def screen_compounds(
        self,
        pdb_file: str,
        sdf_files: List[str],
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Screen multiple compounds against a target.
        
        Args:
            pdb_file: Target protein PDB
            sdf_files: List of compound SDF files
            threshold: Hit threshold (0-1)
        
        Returns:
            List of hits with affinity predictions
        """
        hits = []
        
        print(f"🔬 Screening {len(sdf_files)} compounds...")
        
        for i, sdf in enumerate(sdf_files):
            result = self.predict(pdb_file, sdf)
            
            if "error" not in result:
                prob = result.get("affinity_probability_binary", 0)
                if prob >= threshold:
                    hits.append({
                        "compound": sdf,
                        "affinity_probability": prob,
                        "affinity_log_ic50": result.get("affinity_pred_value"),
                        "rank": len(hits)
                    })
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{len(sdf_files)} ({len(hits)} hits)")
        
        # Sort by affinity probability
        hits.sort(key=lambda x: x["affinity_probability"], reverse=True)
        
        return hits
    
    def interpret_affinity(self, result: Dict[str, Any]) -> str:
        """
        Interpret Boltz-2 affinity prediction for human readability.
        """
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        prob = result.get("affinity_probability_binary")
        log_ic50 = result.get("affinity_pred_value")
        
        if prob is not None:
            if prob >= 0.8:
                likely = "✅ High"
            elif prob >= 0.5:
                likely = "⚠️ Moderate"
            else:
                likely = "❌ Low"
            
            interp = f"{likely} affinity (probability: {prob:.3f})"
        else:
            interp = "No probability score"
        
        if log_ic50 is not None:
            # Convert log IC50 to actual IC50
            ic50_nm = 10 ** (-log_ic50) * 1e9  # Convert M to nM
            interp += f", IC50 estimate: {ic50_nm:.1f} nM"
        
        return interp


# ============================================================
# CLI INTEGRATION
# ============================================================
def boltz_status():
    """Check Boltz-2 status"""
    client = Boltz2Client()
    status = client.status()
    
    print("\n🔧 Boltz-2 Status")
    print("=" * 40)
    print(f"Available: {'✅' if status['available'] else '❌'}")
    print(f"Mode: {status['mode']}")
    print(f"Config: {status['config_mode']}")
    print(f"Affinity threshold: {status['affinity_threshold']}")
    print(f"\nRecommendation:")
    print(f"  {status['recommendation']}")
    print()


def boltz_predict(pdb_file: str, ligand_sdf: str = None):
    """Run single prediction"""
    client = Boltz2Client()
    
    print(f"\n🔬 Boltz-2 Prediction")
    print("=" * 40)
    print(f"Protein: {pdb_file}")
    if ligand_sdf:
        print(f"Ligand: {ligand_sdf}")
    print()
    
    result = client.predict(pdb_file, ligand_sdf)
    print(client.interpret_affinity(result))
    
    return result


def boltz_screen(pdb_file: str, sdf_dir: str, threshold: float = 0.5):
    """Screen compound library"""
    import glob
    
    sdf_files = glob.glob(f"{sdf_dir}/*.sdf")
    
    print(f"\n🔬 Boltz-2 Virtual Screening")
    print("=" * 40)
    print(f"Target: {pdb_file}")
    print(f"Library: {sdf_dir}")
    print(f"Compounds: {len(sdf_files)}")
    print(f"Threshold: {threshold}")
    print()
    
    client = Boltz2Client()
    hits = client.screen_compounds(pdb_file, sdf_files, threshold)
    
    print(f"\n✅ Found {len(hits)} hits:")
    print(f"{'Rank':<6} {'Probability':<14} {'IC50 (nM)':<12}")
    print("-" * 35)
    for hit in hits[:20]:
        log_ic50 = hit.get('affinity_log_ic50')
        ic50_str = f"{10**(-log_ic50)*1e9:.1f}" if log_ic50 else "N/A"
        print(f"{hit['rank']:<6} {hit['affinity_probability']:<14.3f} {ic50_str:<12}")
    
    return hits


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Boltz-2 Client")
    subparsers = parser.add_subparsers(dest="command")
    
    # status
    subparsers.add_parser("status", help="Check Boltz-2 status")
    
    # predict
    predict_parser = subparsers.add_parser("predict", help="Run single prediction")
    predict_parser.add_argument("--pdb", required=True, help="PDB file")
    predict_parser.add_argument("--ligand", help="Ligand SDF file")
    
    # screen
    screen_parser = subparsers.add_parser("screen", help="Screen compound library")
    screen_parser.add_argument("--pdb", required=True, help="Target PDB")
    screen_parser.add_argument("--library", required=True, help="SDF library dir")
    screen_parser.add_argument("--threshold", type=float, default=0.5)
    
    args = parser.parse_args()
    
    if args.command == "status":
        boltz_status()
    elif args.command == "predict":
        boltz_predict(args.pdb, args.ligand)
    elif args.command == "screen":
        boltz_screen(args.pdb, args.library, args.threshold)
    else:
        parser.print_help()