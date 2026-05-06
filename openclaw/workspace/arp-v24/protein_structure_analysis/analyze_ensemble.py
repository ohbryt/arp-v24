#!/usr/bin/env python3
"""
AFSample2 Ensemble Analysis Script
Analyzes conformational diversity from AlphaFold2 sample runs.

Usage:
    python analyze_ensemble.py --input_dir ./output/KDM4A --output ./reports/KDM4A
    python analyze_ensemble.py --input_dir ./output --targets KDM4A SLC7A11 DGAT1 GPX4 YARS2
"""

import argparse
import os
import json
import warnings
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
import pandas as pd

# Try Biopython first, fallback to minimal parser
try:
    from Bio.PDB import PDBParser, Superimposer, PDBIO, Select
    from Bio import pairwise2
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False
    warnings.warn("Biopython not available. Using simplified PDB parsing.")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    warnings.warn("Matplotlib not available. Plotting disabled.")

try:
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("Scikit-learn not available. Clustering disabled.")


class PDBParserSimple:
    """Minimal PDB parser when Biopython unavailable."""
    
    def __init__(self):
        self.structures = {}
    
    def parse(self, pdb_file: str, model_id: int = 0) -> 'Structure':
        """Parse PDB file and return structure object."""
        structure = Structure(model_id)
        current_residue = None
        current_chain = None
        
        with open(pdb_file, 'r') as f:
            for line in f:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    serial = int(line[6:11].strip())
                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    chain_id = line[21:22].strip()
                    res_num = int(line[22:26].strip())
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    
                    if chain_id != current_chain:
                        current_chain = chain_id
                        if chain_id not in structure.chains:
                            structure.chains[chain_id] = Chain(chain_id)
                    
                    residue_key = (res_num, res_name)
                    if residue_key not in structure.chains[chain_id].residues:
                        current_residue = Residue(res_num, res_name)
                        structure.chains[chain_id].residues[residue_key] = current_residue
                    else:
                        current_residue = structure.chains[chain_id].residues[residue_key]
                    
                    atom = Atom(serial, atom_name, x, y, z)
                    current_residue.atoms[atom_name] = atom
        
        return structure


class Structure:
    def __init__(self, model_id: int = 0):
        self.model_id = model_id
        self.chains = {}


class Chain:
    def __init__(self, chain_id: str):
        self.chain_id = chain_id
        self.residues = {}


class Residue:
    def __init__(self, res_num: int, res_name: str):
        self.res_num = res_num
        self.res_name = res_name
        self.atoms = {}


class Atom:
    def __init__(self, serial: int, name: str, x: float, y: float, z: float):
        self.serial = serial
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    
    def coord(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])


class EnsembleAnalyzer:
    """Analyze conformational ensembles from AFSample2 runs."""
    
    def __init__(self, input_dir: str, reference_pdb: Optional[str] = None):
        """
        Initialize analyzer.
        
        Args:
            input_dir: Directory containing PDB files
            reference_pdb: Optional reference PDB for RMSD calculation
        """
        self.input_dir = Path(input_dir)
        self.pdb_files = sorted(self.input_dir.glob("*.pdb"))
        self.structures = []
        self.reference = None
        
        if reference_pdb and os.path.exists(reference_pdb):
            self.load_structure(reference_pdb, as_reference=True)
        
        self._load_all_structures()
    
    def _load_all_structures(self):
        """Load all PDB structures in input directory."""
        if BIOPYTHON_AVAILABLE:
            parser = PDBParser(QUIET=True)
        else:
            parser = PDBParserSimple()
        
        for pdb_file in self.pdb_files:
            try:
                if BIOPYTHON_AVAILABLE:
                    structure = parser.get_structure('ensemble', str(pdb_file))
                    # Get first model, first chain, CA atoms
                    self.structures.append(structure)
                else:
                    structure = parser.parse(str(pdb_file))
                    self.structures.append(structure)
            except Exception as e:
                warnings.warn(f"Failed to parse {pdb_file}: {e}")
        
        print(f"Loaded {len(self.structures)} structures from {self.input_dir}")
    
    def load_structure(self, pdb_file: str, as_reference: bool = False):
        """Load a single structure."""
        if BIOPYTHON_AVAILABLE:
            parser = PDBParser(QUIET=True)
            structure = parser.get_structure('ref', pdb_file)
        else:
            parser = PDBParserSimple()
            structure = parser.parse(pdb_file)
        
        if as_reference:
            self.reference = structure
        return structure
    
    def extract_ca_coords(self, structure) -> np.ndarray:
        """Extract CA atom coordinates from structure."""
        coords = []
        
        if BIOPYTHON_AVAILABLE:
            for model in structure:
                for chain in model:
                    for residue in chain:
                        if residue.id[0] == ' ':
                            if 'CA' in residue:
                                ca = residue['CA']
                                coords.append(ca.get_coord())
        else:
            for chain in structure.chains.values():
                for residue in chain.residues.values():
                    if 'CA' in residue.atoms:
                        coords.append(residue.atoms['CA'].coord())
        
        return np.array(coords) if coords else np.array([])
    
    def calculate_rmsd_matrix(self) -> pd.DataFrame:
        """
        Calculate pairwise RMSD between all structures.
        
        Returns:
            DataFrame with RMSD matrix
        """
        n = len(self.structures)
        rmsd_matrix = np.zeros((n, n))
        
        coords_list = [self.extract_ca_coords(s) for s in self.structures]
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(coords_list[i]) == 0 or len(coords_list[j]) == 0:
                    rmsd = np.nan
                else:
                    # Align structures using rotation matrix
                    coords_ref = coords_list[i]
                    coords_mobile = coords_list[j]
                    
                    # Simple RMSD (no alignment)
                    rmsd = self._rmsd_no_align(coords_ref, coords_mobile)
                
                rmsd_matrix[i, j] = rmsd
                rmsd_matrix[j, i] = rmsd
        
        # Create DataFrame with sample names
        sample_names = [f"sample_{i+1:03d}" for i in range(n)]
        rmsd_df = pd.DataFrame(rmsd_matrix, index=sample_names, columns=sample_names)
        
        self.rmsd_matrix = rmsd_matrix
        self.rmsd_df = rmsd_df
        
        return rmsd_df
    
    def _rmsd_no_align(self, coords1: np.ndarray, coords2: np.ndarray) -> float:
        """Calculate RMSD without structural alignment."""
        min_len = min(len(coords1), len(coords2))
        if min_len == 0:
            return np.nan
        
        diff = coords1[:min_len] - coords2[:min_len]
        return np.sqrt(np.mean(np.sum(diff**2, axis=1)))
    
    def superimpose_structures(self, reference_idx: int = 0) -> List[np.ndarray]:
        """
        Superimpose all structures onto reference using CA atoms.
        
        Args:
            reference_idx: Index of reference structure
            
        Returns:
            List of transformed coordinate arrays
        """
        if not BIOPYTHON_AVAILABLE:
            warnings.warn("Biopython required for superimposition")
            return [self.extract_ca_coords(s) for s in self.structures]
        
        ref_structure = self.structures[reference_idx]
        ref_coords = self.extract_ca_coords(ref_structure)
        
        # Get CA atoms for superimposer
        ref_atoms = []
        ref_structure_list = list(ref_structure.get_models()[0].get_chains()[0].get_residues())
        
        superimposer = Superimposer()
        fixed_atoms = []
        moving_atoms_list = []
        
        for model in ref_structure.get_models():
            for chain in model:
                for residue in chain:
                    if residue.id[0] == ' ' and 'CA' in residue:
                        fixed_atoms.append(residue['CA'])
        
        superimposed_coords = []
        for structure in self.structures:
            moving_atoms = []
            for model in structure.get_models():
                for chain in model:
                    for residue in chain:
                        if residue.id[0] == ' ' and 'CA' in residue:
                            moving_atoms.append(residue['CA'])
            
            if len(fixed_atoms) == len(moving_atoms) and len(fixed_atoms) > 0:
                superimposer.set_reference(fixed_atoms)
                superimposer.apply(moving_atoms)
                coords = np.array([a.get_coord() for a in moving_atoms])
            else:
                coords = self.extract_ca_coords(structure)
            
            superimposed_coords.append(coords)
        
        return superimposed_coords
    
    def cluster_conformations(self, n_clusters: int = 3, method: str = 'kmeans') -> Dict:
        """
        Cluster conformations by structural similarity.
        
        Args:
            n_clusters: Number of clusters
            method: 'kmeans' or 'dbscan'
            
        Returns:
            Dictionary with cluster assignments and metrics
        """
        if not SKLEARN_AVAILABLE:
            warnings.warn("Scikit-learn required for clustering")
            return {}
        
        # Calculate RMSD matrix first
        if not hasattr(self, 'rmsd_matrix'):
            self.calculate_rmsd_matrix()
        
        # Flatten upper triangle of RMSD matrix for clustering
        upper_tri_indices = np.triu_indices(len(self.rmsd_matrix), k=1)
        rmsd_features = self.rmsd_matrix[upper_tri_indices]
        
        # Create feature matrix using MDS-like approach
        n = len(self.rmsd_matrix)
        features = np.zeros((n, n))
        for i in range(n):
            features[i] = self.rmsd_matrix[i]
        
        # PCA for dimensionality reduction
        pca = PCA(n_components=min(10, n-1))
        features_reduced = pca.fit_transform(features)
        
        # Cluster
        if method == 'kmeans':
            clusterer = KMeans(n_clusters=min(n_clusters, n), random_state=42, n_init=10)
            labels = clusterer.fit_predict(features_reduced)
        elif method == 'dbscan':
            clusterer = DBSCAN(eps=2.0, min_samples=2)
            labels = clusterer.fit_predict(features_reduced)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Calculate cluster statistics
        cluster_stats = {}
        for label in set(labels):
            if label == -1:
                continue
            cluster_indices = np.where(labels == label)[0]
            if len(cluster_indices) > 1:
                cluster_rmsd = self.rmsd_matrix[np.ix_(cluster_indices, cluster_indices)]
                cluster_stats[int(label)] = {
                    'size': len(cluster_indices),
                    'mean_intra_rmsd': np.mean(cluster_rmsd[np.triu_indices(len(cluster_indices), k=1)]),
                    'members': cluster_indices.tolist()
                }
        
        self.cluster_labels = labels
        self.cluster_stats = cluster_stats
        
        # Create output dataframe
        sample_names = [f"sample_{i+1:03d}" for i in range(n)]
        cluster_df = pd.DataFrame({
            'sample': sample_names,
            'cluster': labels
        })
        
        return {
            'labels': labels,
            'stats': cluster_stats,
            'dataframe': cluster_df,
            'pca_explained_variance': pca.explained_variance_ratio_.tolist()
        }
    
    def identify_flexible_regions(self, threshold: float = 2.0) -> Dict:
        """
        Identify flexible regions based on positional variance.
        
        Args:
            threshold: RMSF threshold (Å) for defining flexible regions
            
        Returns:
            Dictionary with flexible region information
        """
        if len(self.structures) < 2:
            warnings.warn("Need at least 2 structures for flexibility analysis")
            return {}
        
        # Superimpose structures
        superimposed = self.superimpose_structures()
        
        # Stack coordinates
        max_len = max(len(c) for c in superimposed)
        coords_stacked = np.zeros((len(superimposed), max_len, 3))
        mask = np.zeros((len(superimposed), max_len), dtype=bool)
        
        for i, coords in enumerate(superimposed):
            coords_stacked[i, :len(coords)] = coords
            mask[i, :len(coords)] = True
        
        # Calculate per-residue RMSF (Root Mean Square Fluctuation)
        valid_mask = mask.all(axis=0)
        coords_valid = coords_stacked[:, valid_mask, :]
        
        mean_pos = np.mean(coords_valid, axis=0)
        diff = coords_valid - mean_pos[np.newaxis, :, :]
        rmsf = np.sqrt(np.mean(np.sum(diff**2, axis=2), axis=0))
        
        # Identify flexible regions (above threshold)
        flexible_mask = rmsf > threshold
        flexible_regions = []
        current_region = None
        
        residue_indices = np.where(valid_mask)[0]
        
        for idx, res_idx in enumerate(residue_indices):
            if flexible_mask[idx]:
                if current_region is None:
                    current_region = {'start': res_idx, 'end': res_idx, 'rmsf_values': []}
                current_region['end'] = res_idx
                current_region['rmsf_values'].append(rmsf[idx])
            else:
                if current_region is not None:
                    current_region['mean_rmsf'] = np.mean(current_region['rmsf_values'])
                    current_region['max_rmsf'] = np.max(current_region['rmsf_values'])
                    flexible_regions.append(current_region)
                    current_region = None
        
        if current_region is not None:
            current_region['mean_rmsf'] = np.mean(current_region['rmsf_values'])
            current_region['max_rmsf'] = np.max(current_region['rmsf_values'])
            flexible_regions.append(current_region)
        
        # Format regions
        for region in flexible_regions:
            region['length'] = region['end'] - region['start'] + 1
            del region['rmsf_values']  # Clean up
        
        self.flexible_regions = flexible_regions
        self.rmsf = rmsf
        
        return {
            'regions': flexible_regions,
            'rmsf_per_residue': rmsf.tolist(),
            'threshold': threshold,
            'n_flexible_residues': int(np.sum(flexible_mask))
        }
    
    def calculate_domain_motions(self) -> Dict:
        """Calculate domain-level motions using normal mode analysis approximation."""
        if len(self.structures) < 2:
            return {}
        
        superimposed = self.superimpose_structures()
        
        # Simple approximation: calculate centers of mass for N/C terminal halves
        motions = []
        for i, coords in enumerate(superimposed):
            if len(coords) < 20:
                continue
            mid = len(coords) // 2
            n_term_center = np.mean(coords[:mid], axis=0)
            c_term_center = np.mean(coords[mid:], axis=0)
            motion_vec = c_term_center - n_term_center
            motions.append({
                'sample': f'sample_{i+1:03d}',
                'n_term_center': n_term_center.tolist(),
                'c_term_center': c_term_center.tolist(),
                'motion_vector': motion_vec.tolist(),
                'motion_magnitude': np.linalg.norm(motion_vec)
            })
        
        return {'domain_motions': motions}
    
    def generate_report(self, output_prefix: str = "ensemble_analysis"):
        """Generate comprehensive analysis report."""
        print(f"\n{'='*60}")
        print("CONFORMATIONAL ENSEMBLE ANALYSIS REPORT")
        print(f"{'='*60}\n")
        
        # Basic stats
        print(f"Total structures analyzed: {len(self.structures)}")
        print(f"Input directory: {self.input_dir}\n")
        
        # RMSD statistics
        if hasattr(self, 'rmsd_matrix'):
            upper_tri = self.rmsd_matrix[np.triu_indices(len(self.rmsd_matrix), k=1)]
            print(f"RMSD Statistics:")
            print(f"  Mean pairwise RMSD: {np.nanmean(upper_tri):.3f} Å")
            print(f"  Median pairwise RMSD: {np.nanmedian(upper_tri):.3f} Å")
            print(f"  Max pairwise RMSD: {np.nanmax(upper_tri):.3f} Å")
            print(f"  Min pairwise RMSD: {np.nanmin(upper_tri):.3f} Å\n")
        
        # Cluster statistics
        if hasattr(self, 'cluster_stats'):
            print("Cluster Distribution:")
            for label, stats in self.cluster_stats.items():
                print(f"  Cluster {label}: {stats['size']} samples (intra-RMSF: {stats['mean_intra_rmsd']:.3f} Å)")
            print()
        
        # Flexible regions
        if hasattr(self, 'flexible_regions') and self.flexible_regions:
            print(f"Flexible Regions (RMSF > 2.0 Å):")
            for i, region in enumerate(self.flexible_regions[:10]):  # Top 10
                print(f"  Region {i+1}: Res {region['start']}-{region['end']} "
                      f"(len={region['length']}, mean_RMSF={region['mean_rmsf']:.2f} Å)")
            if len(self.flexible_regions) > 10:
                print(f"  ... and {len(self.flexible_regions) - 10} more regions")
            print()
        
        # Save report to JSON
        report = {
            'n_structures': len(self.structures),
            'input_dir': str(self.input_dir),
            'rmsd_stats': {
                'mean': float(np.nanmean(upper_tri)),
                'median': float(np.nanmedian(upper_tri)),
                'max': float(np.nanmax(upper_tri)),
                'min': float(np.nanmin(upper_tri))
            } if hasattr(self, 'rmsd_matrix') else None,
            'clusters': self.cluster_stats if hasattr(self, 'cluster_stats') else None,
            'flexible_regions': self.flexible_regions if hasattr(self, 'flexible_regions') else None
        }
        
        report_file = f"{output_prefix}_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {report_file}")
        
        # Save RMSD matrix
        if hasattr(self, 'rmsd_df'):
            rmsd_file = f"{output_prefix}_rmsd_matrix.csv"
            self.rmsd_df.to_csv(rmsd_file)
            print(f"RMSD matrix saved to: {rmsd_file}")
        
        # Save cluster assignments
        if hasattr(self, 'cluster_labels'):
            cluster_df = pd.DataFrame({
                'sample': [f"sample_{i+1:03d}" for i in range(len(self.cluster_labels))],
                'cluster': self.cluster_labels.tolist()
            })
            cluster_file = f"{output_prefix}_clusters.csv"
            cluster_df.to_csv(cluster_file, index=False)
            print(f"Cluster assignments saved to: {cluster_file}")
        
        # Generate plots
        if MATPLOTLIB_AVAILABLE:
            self._generate_plots(output_prefix)
        
        return report
    
    def _generate_plots(self, output_prefix: str):
        """Generate visualization plots."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # 1. RMSD heatmap
        if hasattr(self, 'rmsd_matrix') and len(self.rmsd_matrix) > 0:
            ax1 = axes[0, 0]
            sns.heatmap(self.rmsd_matrix, ax=ax1, cmap='viridis',
                       xticklabels=5, yticklabels=5)
            ax1.set_title('Pairwise RMSD Matrix')
            ax1.set_xlabel('Sample')
            ax1.set_ylabel('Sample')
        
        # 2. Cluster distribution
        if hasattr(self, 'cluster_labels'):
            ax2 = axes[0, 1]
            unique, counts = np.unique(self.cluster_labels, return_counts=True)
            colors = plt.cm.Set2(np.linspace(0, 1, len(unique)))
            ax2.bar(unique, counts, color=colors)
            ax2.set_title('Cluster Distribution')
            ax2.set_xlabel('Cluster')
            ax2.set_ylabel('Count')
        
        # 3. RMSF plot
        if hasattr(self, 'rmsf') and len(self.rmsf) > 0:
            ax3 = axes[1, 0]
            ax3.plot(self.rmsf, linewidth=0.5)
            ax3.axhline(y=2.0, color='r', linestyle='--', label='Flexibility threshold')
            ax3.set_title('Per-Residue RMSF')
            ax3.set_xlabel('Residue Index')
            ax3.set_ylabel('RMSF (Å)')
            ax3.legend()
        
        # 4. PCA/t-SNE of conformations
        if hasattr(self, 'cluster_labels') and SKLEARN_AVAILABLE:
            try:
                ax4 = axes[1, 1]
                features = np.zeros((len(self.rmsd_matrix), len(self.rmsd_matrix)))
                for i in range(len(self.rmsd_matrix)):
                    features[i] = self.rmsd_matrix[i]
                
                pca = PCA(n_components=2)
                coords_2d = pca.fit_transform(features)
                
                scatter = ax4.scatter(coords_2d[:, 0], coords_2d[:, 1],
                                     c=self.cluster_labels, cmap='Set2', s=50)
                ax4.set_title('PCA of Conformational Space')
                ax4.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
                ax4.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
                plt.colorbar(scatter, ax=ax4, label='Cluster')
            except Exception as e:
                warnings.warn(f"PCA plot failed: {e}")
        
        plt.tight_layout()
        plot_file = f"{output_prefix}_plots.png"
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Plots saved to: {plot_file}")


def analyze_single_target(target_dir: str, output_dir: str) -> Dict:
    """Analyze a single target directory."""
    target_name = Path(target_dir).name
    print(f"\n{'#'*50}")
    print(f"Analyzing: {target_name}")
    print(f"{'#'*50}")
    
    analyzer = EnsembleAnalyzer(target_dir)
    analyzer.calculate_rmsd_matrix()
    
    if len(analyzer.structures) >= 3:
        analyzer.cluster_conformations(n_clusters=min(3, len(analyzer.structures)))
    
    analyzer.identify_flexible_regions(threshold=2.0)
    analyzer.calculate_domain_motions()
    
    output_prefix = f"{output_dir}/{target_name}"
    report = analyzer.generate_report(output_prefix)
    
    return report


def main():
    parser = argparse.ArgumentParser(description='AFSample2 Ensemble Analysis')
    parser.add_argument('--input_dir', '-i', help='Input directory with PDB files')
    parser.add_argument('--output', '-o', default='./reports', help='Output directory')
    parser.add_argument('--targets', '-t', nargs='+', 
                       help='Target names when input_dir contains multiple target folders')
    parser.add_argument('--num_clusters', '-n', type=int, default=3,
                       help='Number of clusters for conformation clustering')
    parser.add_argument('--flexibility_threshold', '-f', type=float, default=2.0,
                       help='RMSF threshold (Å) for flexible region identification')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    if args.input_dir:
        # Single target analysis
        analyzer = EnsembleAnalyzer(args.input_dir)
        analyzer.calculate_rmsd_matrix()
        
        if len(analyzer.structures) >= args.num_clusters:
            analyzer.cluster_conformations(n_clusters=args.num_clusters)
        
        analyzer.identify_flexible_regions(threshold=args.flexibility_threshold)
        analyzer.calculate_domain_motions()
        
        output_prefix = f"{args.output}/{Path(args.input_dir).name}"
        analyzer.generate_report(output_prefix)
    
    elif args.targets:
        # Multiple targets
        results = []
        for target in args.targets:
            target_dir = f"./output/{target}"
            if os.path.exists(target_dir):
                result = analyze_single_target(target_dir, args.output)
                results.append({
                    'target': target,
                    'result': result
                })
            else:
                print(f"Warning: Directory not found: {target_dir}")
        
        # Save combined report
        combined_file = f"{args.output}/combined_report.json"
        with open(combined_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nCombined report saved to: {combined_file}")
    
    else:
        parser.print_help()
        print("\nError: Must specify either --input_dir or --targets")


if __name__ == "__main__":
    main()