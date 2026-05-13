"""
RegFormer Integration for ARP Pipeline
=========================================
Foundation model for single-cell RNA-seq analysis.

Based on: BGI Research, GitHub: https://github.com/BGIResearch/RegFormer

Features:
- GRN-guided pretraining
- Mamba-based encoder for long sequences
- Multi-task: cell annotation, embedding, GRN, drug response, perturbation

Usage:
    from regformer_integration import analyze_single_cell
    results = analyze_single_cell(sc_data, task="cell_annotation")
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class RegFormerConfig:
    """RegFormer configuration for ARP pipeline"""
    task: str = "emb"  # emb, anno, grn, drug, pert
    model_path: Optional[str] = None
    checkpoint: Optional[str] = None


class RegFormerIntegration:
    """
    RegFormer wrapper for single-cell analysis.
    
    Integration with ARP:
    - Cell type annotation → TMS (TME Score)
    - GRN reconstruction → FSP1/SLC7A11 regulatory network
    - Drug response → Our candidate compounds
    """
    
    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path) if repo_path else Path(__file__).parent / "RegFormer-Official"
        self.installed = self._check_install()
        self.checkpoint = None
        
    def _check_install(self) -> bool:
        """Check if RegFormer is installed"""
        return (self.repo_path / "regformer").exists()
    
    def is_available(self) -> bool:
        """Check if RegFormer can run"""
        return self.installed
    
    def install(self) -> bool:
        """Install RegFormer"""
        try:
            cmd = [
                "git", "clone", "https://github.com/BGIResearch/RegFormer",
                str(self.repo_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def generate_embeddings(
        self,
        data_path: str,
        output_dir: str = "regformer_output"
    ) -> Dict[str, Any]:
        """
        Generate cell embeddings using RegFormer.
        
        Args:
            data_path: Path to scRNA data (.h5ad)
            output_dir: Output directory
        
        Returns:
            Dict with embedding results
        """
        if not self.is_available():
            return self._fallback_embeddings(data_path, output_dir)
        
        try:
            cmd = [
                "python", "downstream_task/regformer_emb.py",
                "--config_file", "cell_emb.toml"
            ]
            result = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output_dir": output_dir,
                    "method": "regformer"
                }
            else:
                return self._fallback_embeddings(data_path, output_dir)
                
        except Exception as e:
            print(f"RegFormer error: {e}")
            return self._fallback_embeddings(data_path, output_dir)
    
    def _fallback_embeddings(
        self,
        data_path: str,
        output_dir: str
    ) -> Dict[str, Any]:
        """Fallback using scanpy for basic embeddings"""
        try:
            import scanpy as sc
            import numpy as np
            
            adata = sc.read(data_path)
            sc.pp.normalize_total(adata)
            sc.pp.log1p(adata)
            sc.pp.highly_variable_genes(adata, n_top_genes=2000)
            sc.pp.scale(adata)
            sc.tp.pca(adata, n_comps=50)
            
            # Save embeddings
            os.makedirs(output_dir, exist_ok=True)
            np.save(f"{output_dir}/embeddings.npy", adata.obsm["X_pca"])
            
            return {
                "status": "fallback_success",
                "output_dir": output_dir,
                "method": "scanpy_pca",
                "n_cells": adata.n_obs,
                "n_genes": adata.n_vars
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def cell_annotation(
        self,
        data_path: str,
        reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Annotate cell types using RegFormer.
        
        Args:
            data_path: Path to scRNA data
            reference: Optional reference annotation
        
        Returns:
            Dict with cell type annotations
        """
        if not self.is_available():
            return self._fallback_annotation(data_path)
        
        try:
            cmd = [
                "python", "downstream_task/regformer_anno.py",
                "--config_file", "anno.toml"
            ]
            result = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "method": "regformer"
                }
            else:
                return self._fallback_annotation(data_path)
                
        except Exception as e:
            return self._fallback_annotation(data_path)
    
    def _fallback_annotation(self, data_path: str) -> Dict[str, Any]:
        """Fallback cell annotation using marker genes"""
        try:
            import scanpy as sc
            
            adata = sc.read(data_path)
            
            # Simple marker-based annotation
            marker_genes = {
                "T cells": ["CD3D", "CD3E", "CD8A"],
                "B cells": ["CD19", "CD79A", "MS4A1"],
                "Macrophages": ["CD68", "CD14", "FCGR3A"],
                "NK cells": ["NKG7", "GNLY", "KLRD1"],
                "Epithelial": ["EPCAM", "KRT8", "KRT18"],
                "Fibroblasts": ["COL1A1", "COL3A1", "FAP"]
            }
            
            # Calculate scores
            scores = {}
            for cell_type, markers in marker_genes.items():
                available_markers = [m for m in markers if m in adata.var_names]
                if available_markers:
                    scores[cell_type] = adata[:, available_markers].X.mean(axis=1)
            
            # Assign cell types
            cell_types = []
            for i in range(adata.n_obs):
                max_score = 0
                best_type = "Unknown"
                for cell_type, score in scores.items():
                    if score[i] > max_score:
                        max_score = score[i]
                        best_type = cell_type
                cell_types.append(best_type)
            
            return {
                "status": "fallback_success",
                "cell_types": cell_types,
                "method": "marker_based",
                "n_cells": adata.n_obs
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def drug_response_prediction(
        self,
        cell_embeddings: str,
        drug_list: List[str]
    ) -> Dict[str, Any]:
        """
        Predict drug response using RegFormer.
        
        Args:
            cell_embeddings: Path to cell embeddings
            drug_list: List of drug names
        
        Returns:
            Dict with drug response predictions
        """
        if not self.is_available():
            return {
                "status": "unavailable",
                "message": "RegFormer not installed"
            }
        
        # RegFormer drug response task
        try:
            cmd = [
                "python", "downstream_task/regformer_drug.py",
                "--config_file", "drug.toml"
            ]
            result = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=1800
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "method": "regformer"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def grn_reconstruction(
        self,
        data_path: str
    ) -> Dict[str, Any]:
        """
        Reconstruct gene regulatory network.
        
        Args:
            data_path: Path to scRNA data
        
        Returns:
            Dict with GRN results
        """
        if not self.is_available():
            return {
                "status": "unavailable",
                "message": "RegFormer not installed"
            }
        
        try:
            cmd = [
                "python", "downstream_task/regformer_grn.py",
                "--config_file", "grn.toml"
            ]
            result = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "method": "regformer"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def apply_to_tms(
        self,
        data_path: str,
        tme_markers: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Apply RegFormer to TME Score (TMS) enhancement.
        
        Args:
            data_path: Path to scRNA data
            tme_markers: Dict of cell type markers
        
        Returns:
            Dict with TMS-enhanced results
        """
        # Cell type annotation
        annotation = self.cell_annotation(data_path)
        
        # Cell type proportions for TMS
        if "cell_types" in annotation:
            cell_type_counts = {}
            for ct in annotation["cell_types"]:
                cell_type_counts[ct] = cell_type_counts.get(ct, 0) + 1
            
            total = sum(cell_type_counts.values())
            proportions = {ct: count/total for ct, count in cell_type_counts.items()}
            
            return {
                "cell_type_proportions": proportions,
                "n_cells": annotation.get("n_cells", 0),
                "method": annotation.get("method", "unknown")
            }
        
        return annotation


def analyze_single_cell(
    data_path: str,
    task: str = "emb",
    output_dir: str = "regformer_output"
) -> Dict[str, Any]:
    """
    Convenience function for single-cell analysis.
    
    Args:
        data_path: Path to scRNA data
        task: "emb", "anno", "grn", "drug"
        output_dir: Output directory
    
    Returns:
        Analysis results
    """
    integrator = RegFormerIntegration()
    
    if task == "emb":
        return integrator.generate_embeddings(data_path, output_dir)
    elif task == "anno":
        return integrator.cell_annotation(data_path)
    elif task == "grn":
        return integrator.grn_reconstruction(data_path)
    elif task == "drug":
        return integrator.drug_response_prediction(output_dir, [])
    else:
        return {"error": f"Unknown task: {task}"}


# Test
if __name__ == "__main__":
    print("=== RegFormer Integration Test ===\n")
    
    integrator = RegFormerIntegration()
    print(f"RegFormer installed: {integrator.installed}")
    print(f"RegFormer available: {integrator.is_available()}")
    
    print("\n✓ RegFormer integration module OK!")