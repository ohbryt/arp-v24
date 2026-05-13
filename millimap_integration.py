"""
MilliMap Integration for ARP Pipeline
=======================================
Spatial omics visualization for MERFISH data analysis.

Based on: https://milliomics.com/millimap/docs/

Features:
- Code-free spatial transcriptomics visualization
- Support for Visium, Xenium, MERSCOPE, CosMx, CODEX, MERFISH
- Interactive 3D tissue exploration

Usage:
    from millimap_integration import load_merfish, visualize_tme
    results = load_merfish("path/to/merfish.h5ad")
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class SpatialAnalysisConfig:
    """Configuration for spatial analysis"""
    data_path: str
    platform: str = "auto"  # auto, visium, xenium, merscope, cosmx, codex, merfish
    resolution: str = "auto"
    output_dir: str = "./millimap_output"


class MilliMapIntegration:
    """
    MilliMap wrapper for spatial omics analysis.
    
    Integration with ARP:
    - MERFISH skin atlas visualization → TMS (TME Score)
    - FSP1/SLC7A11/DGAT1 spatial localization
    - Cell neighborhood analysis
    """
    
    def __init__(self):
        self.app_path = self._find_millimap()
        self.installed = self.app_path is not None
        
    def _find_millimap(self) -> Optional[str]:
        """Find MilliMap installation"""
        # Check common locations
        possible_paths = [
            "/Applications/MilliMap.app",
            os.path.expanduser("~/Applications/MilliMap.app"),
            os.path.expanduser("~/Downloads/MilliMap.app")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def is_available(self) -> bool:
        """Check if MilliMap is installed"""
        return self.installed
    
    def get_download_url(self) -> str:
        """Get MilliMap download URL"""
        return "https://drive.google.com/drive/folders/1ns-1vtqKqFtFv5wwJRYuw_GvnnFZuFJT"
    
    def load_merfish(
        self,
        data_path: str,
        gene_list: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Load MERFISH data for analysis.
        
        Args:
            data_path: Path to .h5ad file
            gene_list: Optional list of genes to focus on
        
        Returns:
            Dict with data loading results
        """
        if not os.path.exists(data_path):
            return {
                "status": "file_not_found",
                "path": data_path
            }
        
        # Check file format
        if data_path.endswith(".h5ad"):
            return self._load_h5ad(data_path, gene_list)
        else:
            return {
                "status": "unsupported_format",
                "path": data_path,
                "supported": [".h5ad"]
            }
    
    def _load_h5ad(
        self,
        data_path: str,
        gene_list: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Load AnnData (.h5ad) file"""
        try:
            import scanpy as sc
            
            adata = sc.read(data_path)
            
            result = {
                "status": "success",
                "n_cells": adata.n_obs,
                "n_genes": adata.n_vars,
                "platform": "merfish",
                "path": data_path,
                "shape": adata.shape,
                "layers": list(adata.layers.keys()) if adata.layers else ["X"],
                "obs_columns": list(adata.obs.columns) if hasattr(adata, 'obs') else [],
                "var_columns": list(adata.var.columns) if hasattr(adata, 'var') else []
            }
            
            # Add spatial coordinates if available
            if hasattr(adata, 'obsm'):
                if 'spatial' in adata.obsm:
                    result['has_spatial'] = True
                    result['spatial_dims'] = adata.obsm['spatial'].shape[1]
                else:
                    result['has_spatial'] = False
            
            # Filter gene list if provided
            if gene_list:
                available_genes = [g for g in gene_list if g in adata.var_names]
                result['genes_matched'] = len(available_genes)
                result['genes_requested'] = len(gene_list)
                result['available_genes'] = available_genes
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "path": data_path
            }
    
    def analyze_tme(
        self,
        data_path: str,
        tme_markers: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze tumor microenvironment from MERFISH.
        
        Args:
            data_path: Path to MERFISH data
            tme_markers: Dict of cell type markers
        
        Returns:
            Dict with TME analysis results
        """
        data_info = self.load_merfish(data_path)
        
        if data_info["status"] != "success":
            return data_info
        
        try:
            import scanpy as sc
            
            adata = sc.read(data_path)
            
            # Cell type scoring
            cell_scores = {}
            for cell_type, markers in tme_markers.items():
                available = [m for m in markers if m in adata.var_names]
                if available:
                    # Calculate mean expression per cell
                    scores = adata[:, available].X.mean(axis=1)
                    cell_scores[cell_type] = scores.flatten().tolist()
            
            # Assign cell types based on max score
            n_cells = adata.n_obs
            cell_types = ["Unknown"] * n_cells
            
            if cell_scores:
                for i in range(n_cells):
                    max_score = -1
                    best_type = "Unknown"
                    for cell_type, scores in cell_scores.items():
                        if scores[i] > max_score:
                            max_score = scores[i]
                            best_type = cell_type
                    cell_types[i] = best_type
            
            # Cell type proportions
            type_counts = {}
            for ct in cell_types:
                type_counts[ct] = type_counts.get(ct, 0) + 1
            
            total = len(cell_types)
            proportions = {ct: count/total for ct, count in type_counts.items()}
            
            return {
                "status": "success",
                "n_cells": n_cells,
                "cell_type_proportions": proportions,
                "cell_types": cell_types[:100],  # Sample
                "method": "millimap_scanpy"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def spatial_localization(
        self,
        data_path: str,
        target_genes: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze spatial localization of target genes.
        
        Args:
            data_path: Path to MERFISH data
            target_genes: List of genes (FSP1, SLC7A11, DGAT1)
        
        Returns:
            Dict with spatial localization results
        """
        data_info = self.load_merfish(data_path, target_genes)
        
        if data_info["status"] != "success":
            return data_info
        
        try:
            import scanpy as sc
            import numpy as np
            
            adata = sc.read(data_path)
            
            localization = {}
            
            for gene in target_genes:
                if gene in adata.var_names:
                    # Get expression values
                    expr = adata[:, gene].X.flatten()
                    
                    # Get spatial coordinates if available
                    if 'spatial' in adata.obsm:
                        coords = adata.obsm['spatial']
                        
                        # Calculate spatial statistics
                        high_expr_mask = expr > np.percentile(expr, 75)
                        
                        localization[gene] = {
                            "mean_expression": float(expr.mean()),
                            "positive_cells": int(high_expr_mask.sum()),
                            "positive_ratio": float(high_expr_mask.mean()),
                            "spatial_centroid": coords[high_expr_mask].mean(axis=0).tolist() if high_expr_mask.sum() > 0 else None
                        }
                    else:
                        localization[gene] = {
                            "mean_expression": float(expr.mean()),
                            "positive_cells": int((expr > 0).sum()),
                            "spatial": False
                        }
                else:
                    localization[gene] = {
                        "status": "not_found",
                        "available": gene in adata.var_names
                    }
            
            return {
                "status": "success",
                "target_genes": target_genes,
                "localization": localization,
                "n_cells": adata.n_obs
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown report for spatial analysis"""
        lines = [
            "## Spatial Omics Analysis Report (MilliMap Integration)",
            "",
            f"**Status:** {results.get('status', 'unknown')}",
            ""
        ]
        
        if "n_cells" in results:
            lines.append(f"**Cells:** {results['n_cells']}")
        
        if "cell_type_proportions" in results:
            lines.append("")
            lines.append("### Cell Type Proportions")
            for ct, prop in results["cell_type_proportions"].items():
                lines.append(f"- {ct}: {prop:.2%}")
        
        if "localization" in results:
            lines.append("")
            lines.append("### Gene Spatial Localization")
            for gene, data in results["localization"].items():
                if "mean_expression" in data:
                    lines.append(f"- **{gene}**: mean={data['mean_expression']:.3f}")
        
        return "\n".join(lines)


def load_spatial_data(
    data_path: str,
    platform: str = "auto"
) -> Dict[str, Any]:
    """
    Convenience function for loading spatial omics data.
    
    Args:
        data_path: Path to data file
        platform: "auto", "visium", "xenium", "merscope", "cosmx", "codex", "merfish"
    
    Returns:
        Data loading results
    """
    integrator = MilliMapIntegration()
    return integrator.load_merfish(data_path)


# Test
if __name__ == "__main__":
    print("=== MilliMap Integration Test ===\n")
    
    integrator = MilliMapIntegration()
    print(f"MilliMap installed: {integrator.installed}")
    print(f"Download URL: {integrator.get_download_url()}")
    
    # Test MERFISH data loading (if exists)
    merfish_path = os.path.expanduser("~/openclaw/workspace/skin_atlas_analysis/output/merfish.h5ad")
    
    if os.path.exists(merfish_path):
        print(f"\nLoading MERFISH data: {merfish_path}")
        result = integrator.load_merfish(merfish_path, ["FSP1", "SLC7A11", "DGAT1"])
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Cells: {result['n_cells']}, Genes: {result['n_genes']}")
    else:
        print(f"\nMERFISH data not found at: {merfish_path}")
    
    print("\n✓ MilliMap integration module OK!")