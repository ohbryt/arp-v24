#!/usr/bin/env python3
"""
Boltz-2 Client: Integration with NVIDIA NIM or local boltz2
===========================================================
Based on BOLTZ2_INTEGRATION_PLAN_2026.md
Reference: Wang et al. 2026, J Chem Inf Model - "The Last Mile Problem"

Usage:
    from boltz2_client import Boltz2Client
    client = Boltz2Client()
    result = client.predict(pdb_file="protein.pdb", ligand_sdf="compound.sdf")
    
    CLI commands:
    python boltz2_client.py status
    python boltz2_client.py predict --pdb protein.pdb --ligand compound.sdf
    python boltz2_client.py screen --target protein.pdb --library /path/to/compounds/
"""

import json
import subprocess
import os
import glob
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

# ============================================================
# CONFIGURATION
# ============================================================
BOLTZ2_CLI_PATH = "/Users/ocm/Library/Python/3.14/bin/boltz2"

@dataclass
class Boltz2Config:
    """Boltz-2 configuration"""
    mode: str = "local"  # "local" or "nimgateway" (NVIDIA NIM)
    
    # NVIDIA NIM settings  
    nimp_url: str = "https://health.api.nvidia.com/v1/biology/mit/boltz2/predict"
    nimp_api_key: Optional[str] = None  # From NVIDIA NGC API key
    
    # Common settings
    affinity_threshold: float = 0.5  # Binary hit threshold (0-1)

class Boltz2Client:
    """
    Boltz-2 client for protein structure + binding affinity prediction.
    
    Access modes:
    1. Local (Mac M4 Pro): pip install boltz2-python-client
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
                    [BOLTZ2_CLI_PATH, "--help"],
                    capture_output=True, text=True, timeout=10
                )
                if "Boltz-2 Python Client CLI" in result.stdout:
                    self.available = True
                    self.mode = "local"
                    return
            except Exception as e:
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
            "recommendation": self._get_recommendation(),
            "note": self._get_status_note()
        }
    
    def _get_status_note(self) -> str:
        """Get detailed status note"""
        if self.mode == "local":
            return (
                "Client installed. To run predictions, you need:\n"
                "  1. Local server: docker run -p 8000:8000 nvidia/boltz2\n"
                "  2. Or use NVIDIA NIM: set --endpoint-type nvidia_hosted --api-key YOUR_KEY\n"
                "  Current CLI is the client only - needs backend to run predictions."
            )
        return ""
    
    def _get_recommendation(self) -> str:
        """Get setup recommendation based on environment"""
        if self.available:
            return f"Boltz-2 ready in {self.mode} mode"
        
        if self.config.mode == "local":
            return (
                "Install: python3 -m pip install boltz2-python-client --user"
            )
        elif self.config.mode == "nimgateway":
            return "Set NVIDIA NGC API key or switch to local mode"
        
        return "Boltz-2 not available"
    
    def health_check(self) -> Dict[str, Any]:
        """Run boltz2 health check"""
        try:
            result = subprocess.run(
                [BOLTZ2_CLI_PATH, "health"],
                capture_output=True, text=True, timeout=30
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.returncode != 0 else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def metadata(self) -> Dict[str, Any]:
        """Get Boltz-2 service metadata"""
        try:
            result = subprocess.run(
                [BOLTZ2_CLI_PATH, "metadata"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                # Parse JSON output
                try:
                    return json.loads(result.stdout)
                except:
                    return {"raw": result.stdout}
            return {"error": result.stderr.strip()}
        except Exception as e:
            return {"error": str(e)}
    
    def predict(
        self, 
        pdb_file: str,
        ligand_sdf: Optional[str] = None,
        sequence: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run Boltz-2 prediction.
        
        Args:
            pdb_file: PDB file path (protein structure)
            ligand_sdf: SDF file path (ligand, optional for apo prediction)
            sequence: Protein sequence (alternative to PDB file)
        
        Returns:
            Dict with prediction results
        """
        if not self.available:
            return {
                "error": "Boltz-2 not available",
                "status": self.status()
            }
        
        if self.mode == "local":
            return self._predict_local(pdb_file, ligand_sdf, sequence)
        elif self.mode == "nimgateway":
            return self._predict_nimgateway(pdb_file, ligand_sdf)
    
    def _predict_local(
        self,
        pdb_file: str,
        ligand_sdf: Optional[str],
        sequence: Optional[str]
    ) -> Dict[str, Any]:
        """Run prediction using local boltz2 CLI"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            if ligand_sdf:
                # Protein-ligand complex prediction
                # Copy files to temp dir
                import shutil
                pdb_copy = shutil.copy(pdb_file, tmpdir)
                lig_copy = shutil.copy(ligand_sdf, tmpdir)
                
                # boltz2 ligand --pdb <pdb> --ligand <sdf> [options]
                cmd = [
                    BOLTZ2_CLI_PATH,
                    "ligand",
                    "--pdb", pdb_copy,
                    "--ligand", lig_copy,
                    "--outdir", tmpdir
                ]
            else:
                # Protein only prediction
                cmd = [
                    BOLTZ2_CLI_PATH,
                    "protein",
                    "--pdb", pdb_file,
                    "--outdir", tmpdir
                ]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 min timeout for structure prediction
                )
                
                if result.returncode != 0:
                    return {
                        "error": "boltz2 prediction failed",
                        "stderr": result.stderr,
                        "returncode": result.returncode,
                        "stdout": result.stdout
                    }
                
                # Parse output - look for affinity values
                output = {
                    "status": "completed",
                    "pdb": pdb_file,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
                # Parse affinity from output
                for line in result.stdout.split('\n'):
                    line_lower = line.lower()
                    if 'affinity' in line_lower or 'probability' in line_lower:
                        parts = line.split()
                        for i, p in enumerate(parts):
                            if 'affinity' in p.lower() and i+1 < len(parts):
                                try:
                                    output['affinity_pred_value'] = float(parts[i+1])
                                except:
                                    pass
                
                # Look for output files
                output_files = list(Path(tmpdir).glob("*"))
                if output_files:
                    output['output_files'] = [str(f) for f in output_files]
                
                return output
            
            except subprocess.TimeoutExpired:
                return {"error": "Prediction timeout (>10 min)"}
            except Exception as e:
                return {"error": str(e)}
    
    def _predict_nimgateway(
        self,
        pdb_file: str,
        ligand_sdf: Optional[str]
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
        }
        
        if ligand_sdf:
            with open(ligand_sdf, 'r') as f:
                payload["ligand"] = f.read()
        
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
        target_pdb: str,
        library_dir: str,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Screen multiple compounds against a target using Boltz-2 screen.
        
        Args:
            target_pdb: Target protein PDB
            library_dir: Directory containing SDF compound files
            threshold: Hit threshold (0-1)
        
        Returns:
            List of hits with affinity predictions
        """
        # Find all SDF files
        sdf_files = glob.glob(f"{library_dir}/*.sdf")
        
        if not sdf_files:
            return [{"error": f"No SDF files found in {library_dir}"}]
        
        print(f"🔬 Screening {len(sdf_files)} compounds...")
        
        hits = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # boltz2 screen <target> <compounds_csv>
            # Need to create a CSV of compound files
            compound_csv = Path(tmpdir) / "compounds.csv"
            with open(compound_csv, 'w') as f:
                f.write("compound_file\n")
                for sdf in sdf_files:
                    f.write(f"{sdf}\n")
            
            cmd = [
                BOLTZ2_CLI_PATH,
                "screen",
                target_pdb,
                str(compound_csv),
                "--outdir", tmpdir
            ]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1 hour for screening
                )
                
                # Parse output for hits
                for line in result.stdout.split('\n'):
                    # Look for ranked compounds with scores
                    if any(x in line.lower() for x in ['hit', 'score', 'rank', 'affinity']):
                        hits.append({"raw": line})
                
                return {
                    "status": "completed",
                    "hits": hits,
                    "total_compounds": len(sdf_files),
                    "stdout": result.stdout[:5000],  # First 5000 chars
                    "stderr": result.stderr[:1000]
                }
            
            except subprocess.TimeoutExpired:
                return {"error": "Screening timeout (>1 hour)"}
            except Exception as e:
                return {"error": str(e)}
    
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
            interp = "⚠️ No probability score (prediction completed)"
        
        if log_ic50 is not None:
            # Convert log IC50 to actual IC50
            try:
                ic50_nm = 10 ** (-log_ic50) * 1e9  # Convert M to nM
                interp += f", IC50 estimate: {ic50_nm:.1f} nM"
            except:
                interp += f", log IC50: {log_ic50}"
        
        return interp


# ============================================================
# CLI FUNCTIONS
# ============================================================
def boltz_status():
    """Check Boltz-2 status"""
    client = Boltz2Client()
    status = client.status()
    
    print("\n🔧 Boltz-2 Status")
    print("=" * 50)
    print(f"Available: {'✅' if status['available'] else '❌'}")
    print(f"Mode: {status['mode']}")
    print(f"Config: {status['config_mode']}")
    print(f"Affinity threshold: {status['affinity_threshold']}")
    print(f"\nRecommendation: {status['recommendation']}")
    
    # Try health check
    health = client.health_check()
    print(f"\nHealth check:")
    if health.get('success'):
        print(f"  ✅ {health.get('output', 'OK')}")
    else:
        print(f"  ❌ {health.get('error', 'Failed')}")
    
    # Get metadata
    metadata = client.metadata()
    if 'model_name' in metadata:
        print(f"\nModel: {metadata.get('model_name')}")
    print()


def boltz_predict(pdb_file: str, ligand_sdf: str = None):
    """Run single prediction"""
    if not os.path.exists(pdb_file):
        print(f"❌ PDB file not found: {pdb_file}")
        return
    
    if ligand_sdf and not os.path.exists(ligand_sdf):
        print(f"❌ Ligand file not found: {ligand_sdf}")
        return
    
    client = Boltz2Client()
    
    print(f"\n🔬 Boltz-2 Prediction")
    print("=" * 50)
    print(f"Protein: {pdb_file}")
    if ligand_sdf:
        print(f"Ligand: {ligand_sdf}")
    print()
    
    result = client.predict(pdb_file, ligand_sdf)
    print(client.interpret_affinity(result))
    
    if "stdout" in result:
        print("\n--- Output (first 1000 chars) ---")
        print(result["stdout"][:1000])
    
    return result


def boltz_screen(target_pdb: str, library_dir: str, threshold: float = 0.5):
    """Screen compound library"""
    if not os.path.exists(target_pdb):
        print(f"❌ Target PDB not found: {target_pdb}")
        return
    
    if not os.path.isdir(library_dir):
        print(f"❌ Library directory not found: {library_dir}")
        return
    
    print(f"\n🔬 Boltz-2 Virtual Screening")
    print("=" * 50)
    print(f"Target: {target_pdb}")
    print(f"Library: {library_dir}")
    print(f"Threshold: {threshold}")
    print()
    
    client = Boltz2Client()
    result = client.screen_compounds(target_pdb, library_dir, threshold)
    
    print("\n--- Result ---")
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"Status: {result.get('status')}")
        print(f"Total compounds: {result.get('total_compounds', 'N/A')}")
        if "stdout" in result:
            print("\nOutput:")
            print(result["stdout"][:2000])
    
    return result


# ============================================================
# MAIN CLI
# ============================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Boltz-2 Client for ARP")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # status
    subparsers.add_parser("status", help="Check Boltz-2 status")
    
    # predict
    predict_parser = subparsers.add_parser("predict", help="Run single prediction")
    predict_parser.add_argument("--pdb", required=True, help="PDB file")
    predict_parser.add_argument("--ligand", help="Ligand SDF file")
    
    # screen
    screen_parser = subparsers.add_parser("screen", help="Screen compound library")
    screen_parser.add_argument("--target", required=True, help="Target PDB")
    screen_parser.add_argument("--library", required=True, help="SDF library directory")
    screen_parser.add_argument("--threshold", type=float, default=0.5)
    
    args = parser.parse_args()
    
    if args.command == "status":
        boltz_status()
    elif args.command == "predict":
        boltz_predict(args.pdb, args.ligand)
    elif args.command == "screen":
        boltz_screen(args.target, args.library, args.threshold)
    else:
        parser.print_help()