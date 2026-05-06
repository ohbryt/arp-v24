#!/usr/bin/env python3
"""
AFSample2 Batch Analysis Script
Analyzes conformational ensembles for all ARP target proteins.

Usage:
    python batch_analyze.py --base_dir ./output --output ./reports
    python batch_analyze.py --targets KDM4A SLC7A11 DGAT1 GPX4 YARS2
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Import the ensemble analyzer
sys.path.insert(0, str(Path(__file__).parent))
from analyze_ensemble import EnsembleAnalyzer


# Target proteins with metadata
TARGETS = {
    "KDM4A": {
        "uniprot": "O75164",
        "gene": "KDM4A",
        "name": "Lysine-specific demethylase 4A",
        "length": 359,
        "function": "Histone lysine demethylase"
    },
    "SLC7A11": {
        "uniprot": "Q9UPY5", 
        "gene": "SLC7A11",
        "name": "Cystine/glutamate transporter",
        "length": 501,
        "function": "Amino acid transport"
    },
    "DGAT1": {
        "uniprot": "O75907",
        "gene": "DGAT1", 
        "name": "Diacylglycerol O-acyltransferase 1",
        "length": 488,
        "function": "Lipid metabolism"
    },
    "GPX4": {
        "uniprot": "P36969",
        "gene": "GPX4",
        "name": "Phospholipid hydroperoxide glutathione peroxidase",
        "length": 197,
        "function": "Antioxidant defense"
    },
    "YARS2": {
        "uniprot": "Q9Y2Z4",
        "gene": "YARS2",
        "name": "Tyrosine--tRNA ligase, mitochondrial",
        "length": 471,
        "function": "Mitochondrial translation"
    }
}


def analyze_target(target_name: str, target_dir: str, output_dir: str) -> Dict:
    """Analyze a single target protein."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {target_name}")
    print(f"{'='*60}")
    print(f"Target directory: {target_dir}")
    print(f"Output directory: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if PDB files exist
    pdb_files = list(Path(target_dir).glob("*.pdb"))
    if not pdb_files:
        print(f"Warning: No PDB files found in {target_dir}")
        return {
            "target": target_name,
            "status": "no_data",
            "message": "No PDB files found"
        }
    
    print(f"Found {len(pdb_files)} PDB structures")
    
    # Initialize analyzer
    analyzer = EnsembleAnalyzer(target_dir)
    
    if len(analyzer.structures) < 2:
        print(f"Warning: Only {len(analyzer.structures)} structure(s) found. Need at least 2 for analysis.")
        return {
            "target": target_name,
            "status": "insufficient_data",
            "n_structures": len(analyzer.structures)
        }
    
    # Run all analyses
    results = {
        "target": target_name,
        "metadata": TARGETS.get(target_name, {}),
        "status": "success",
        "n_structures": len(analyzer.structures),
        "timestamp": datetime.now().isoformat()
    }
    
    # 1. RMSD matrix calculation
    print("\n[1/5] Calculating RMSD matrix...")
    rmsd_df = analyzer.calculate_rmsd_matrix()
    results["rmsd_stats"] = {
        "mean": float(np.nanmean(analyzer.rmsd_matrix[np.triu_indices(len(analyzer.rmsd_matrix), k=1)])),
        "median": float(np.nanmedian(analyzer.rmsd_matrix[np.triu_indices(len(analyzer.rmsd_matrix), k=1)])),
        "max": float(np.nanmax(analyzer.rmsd_matrix)),
        "min": float(np.nanmin(analyzer.rmsd_matrix[np.triu_indices(len(analyzer.rmsd_matrix), k=1)])),
        "std": float(np.nanstd(analyzer.rmsd_matrix[np.triu_indices(len(analyzer.rmsd_matrix), k=1)]))
    }
    
    # Save RMSD matrix
    rmsd_file = f"{output_dir}/{target_name}_rmsd_matrix.csv"
    rmsd_df.to_csv(rmsd_file)
    print(f"  Saved: {rmsd_file}")
    
    # 2. Conformation clustering
    print("\n[2/5] Clustering conformations...")
    n_clusters = min(3, len(analyzer.structures) - 1)
    if n_clusters >= 2:
        cluster_results = analyzer.cluster_conformations(n_clusters=n_clusters, method='kmeans')
        results["clusters"] = {
            "method": "kmeans",
            "n_clusters": n_clusters,
            "distribution": {},
            "pca_explained_variance": cluster_results.get("pca_explained_variance", [])
        }
        
        # Cluster distribution
        for label in cluster_results["labels"]:
            label_str = str(label)
            if label_str not in results["clusters"]["distribution"]:
                results["clusters"]["distribution"][label_str] = 0
            results["clusters"]["distribution"][label_str] += 1
        
        # Save cluster assignments
        cluster_file = f"{output_dir}/{target_name}_clusters.csv"
        cluster_results["dataframe"].to_csv(cluster_file, index=False)
        print(f"  Saved: {cluster_file}")
    else:
        print("  Skipping clustering (need >= 3 structures)")
        results["clusters"] = {"status": "skipped", "reason": "insufficient structures"}
    
    # 3. Flexible region identification
    print("\n[3/5] Identifying flexible regions...")
    flex_results = analyzer.identify_flexible_regions(threshold=2.0)
    results["flexibility"] = {
        "threshold_angstroms": 2.0,
        "n_flexible_regions": len(flex_results.get("regions", [])),
        "n_flexible_residues": flex_results.get("n_flexible_residues", 0),
        "regions": flex_results.get("regions", [])
    }
    
    # Save flexible regions
    flex_file = f"{output_dir}/{target_name}_flexible_regions.json"
    with open(flex_file, 'w') as f:
        json.dump(flex_results, f, indent=2)
    print(f"  Saved: {flex_file}")
    
    # 4. Domain motions
    print("\n[4/5] Calculating domain motions...")
    motion_results = analyzer.calculate_domain_motions()
    results["domain_motions"] = motion_results
    
    # 5. Generate full report
    print("\n[5/5] Generating comprehensive report...")
    report = analyzer.generate_report(f"{output_dir}/{target_name}")
    
    # Save target-specific report
    report_file = f"{output_dir}/{target_name}_report.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Saved: {report_file}")
    
    print(f"\nCompleted analysis for {target_name}")
    
    return results


def generate_combined_report(all_results: List[Dict], output_dir: str):
    """Generate combined report across all targets."""
    print(f"\n{'='*60}")
    print("GENERATING COMBINED REPORT")
    print(f"{'='*60}")
    
    combined = {
        "timestamp": datetime.now().isoformat(),
        "n_targets": len(all_results),
        "targets": {}
    }
    
    for result in all_results:
        target_name = result["target"]
        combined["targets"][target_name] = result
    
    # Cross-target comparison
    rmsd_means = []
    for result in all_results:
        if "rmsd_stats" in result:
            rmsd_means.append({
                "target": result["target"],
                "mean_rmsd": result["rmsd_stats"]["mean"]
            })
    
    combined["cross_target_comparison"] = {
        "conformational_diversity_ranking": sorted(rmsd_means, key=lambda x: x["mean_rmsd"], reverse=True),
        "most_flexible": rmsd_means[0]["target"] if rmsd_means else None,
        "most_rigid": rmsd_means[-1]["target"] if rmsd_means else None
    }
    
    # Save combined report
    combined_file = f"{output_dir}/combined_report.json"
    with open(combined_file, 'w') as f:
        json.dump(combined, f, indent=2)
    print(f"Combined report saved: {combined_file}")
    
    # Generate summary CSV
    summary_data = []
    for result in all_results:
        row = {
            "target": result["target"],
            "gene": result.get("metadata", {}).get("gene", ""),
            "function": result.get("metadata", {}).get("function", ""),
            "length_aa": result.get("metadata", {}).get("length", ""),
            "n_structures": result.get("n_structures", 0),
            "status": result.get("status", "unknown"),
        }
        
        if "rmsd_stats" in result:
            row.update({
                "mean_rmsd_A": round(result["rmsd_stats"]["mean"], 3),
                "median_rmsd_A": round(result["rmsd_stats"]["median"], 3),
                "max_rmsd_A": round(result["rmsd_stats"]["max"], 3),
                "std_rmsd_A": round(result["rmsd_stats"]["std"], 3)
            })
        
        if "flexibility" in result:
            row.update({
                "n_flexible_regions": result["flexibility"]["n_flexible_regions"],
                "n_flexible_residues": result["flexibility"]["n_flexible_residues"]
            })
        
        if "clusters" in result and "distribution" in result["clusters"]:
            row["n_clusters"] = len(result["clusters"]["distribution"])
        
        summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = f"{output_dir}/summary_comparison.csv"
    summary_df.to_csv(summary_file, index=False)
    print(f"Summary comparison saved: {summary_file}")
    
    # Print summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(summary_df.to_string(index=False))
    print("="*80)
    
    return combined


def main():
    parser = argparse.ArgumentParser(description='AFSample2 Batch Analysis for ARP Targets')
    parser.add_argument('--base_dir', '-b', default='./output',
                       help='Base directory containing target subdirectories')
    parser.add_argument('--output', '-o', default='./reports',
                       help='Output directory for analysis results')
    parser.add_argument('--targets', '-t', nargs='+',
                       choices=list(TARGETS.keys()),
                       default=list(TARGETS.keys()),
                       help='Targets to analyze (default: all)')
    parser.add_argument('--flexibility_threshold', '-f', type=float, default=2.0,
                       help='RMSF threshold (Å) for flexible region identification')
    
    args = parser.parse_args()
    
    print("AFSample2 Batch Analysis for ARP Target Proteins")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Base directory: {args.base_dir}")
    print(f"Output directory: {args.output}")
    print(f"Targets: {args.targets}")
    print(f"Flexibility threshold: {args.flexibility_threshold} Å")
    
    os.makedirs(args.output, exist_ok=True)
    
    results = []
    
    for target in args.targets:
        target_dir = os.path.join(args.base_dir, target)
        target_output = os.path.join(args.output, target)
        
        # Try lowercase directory name as fallback
        if not os.path.exists(target_dir):
            target_dir_lower = os.path.join(args.base_dir.lower(), target)
            if os.path.exists(target_dir_lower):
                target_dir = target_dir_lower
        
        if not os.path.exists(target_dir):
            print(f"\nWarning: Directory not found for {target}: {target_dir}")
            print("  This target will be marked as 'not_found'")
            results.append({
                "target": target,
                "status": "not_found",
                "directory": target_dir
            })
            continue
        
        result = analyze_target(target, target_dir, target_output)
        results.append(result)
    
    # Generate combined report
    if any(r.get("status") == "success" for r in results):
        combined = generate_combined_report(results, args.output)
        
        # Save all results
        all_results_file = f"{args.output}/all_results.json"
        with open(all_results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nAll results saved: {all_results_file}")
    
    print("\n" + "="*60)
    print("BATCH ANALYSIS COMPLETE")
    print("="*60)
    
    # Print status summary
    status_counts = {}
    for r in results:
        status = r.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())