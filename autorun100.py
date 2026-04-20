#!/usr/bin/env python3
"""
ARP v24 AutoRun x100
====================
Run the full pipeline 100 times and collect statistics

Usage:
    python3 autorun100.py --disease masld --n 100
    python3 autorun100.py --disease cancer --n 50 --top-n 10
"""

import sys
import json
import argparse
import time
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, '/Users/ocm/.openclaw/workspace/arp-v24')
from pipeline import ARPv24Pipeline, PipelineResult


def run_single(disease: str, top_n: int, iteration: int) -> dict:
    """Run single pipeline iteration"""
    pipeline = ARPv24Pipeline()
    result = pipeline.run(disease, top_n=top_n, run_engine2=True, run_engine3=True)
    return result


def collect_stats(result: PipelineResult) -> dict:
    """Extract statistics from pipeline result"""
    stats = {
        "targets_returned": len(result.targets),
        "execution_time": result.execution_time_seconds,
        "literature_status": result.literature_status.value,
        "warnings_count": len(result.warnings),
        "errors_count": len(result.errors),
    }
    
    # Top target scores
    if result.targets:
        top = result.targets[0]
        stats["top_gene"] = top.gene_name
        stats["top_score"] = round(top.priority_score, 4)
        stats["top_modalities"] = top.recommended_modalities[:2] if top.recommended_modalities else []
    
    # Engine 2/3 coverage
    stats["engine2_runs"] = len(result.engine2_results)
    stats["engine3_runs"] = len(result.engine3_results)
    
    # Engine 3 candidate quality
    all_candidates = []
    for gene, data in result.engine3_results.items():
        for c in data.get("top_10", []):
            all_candidates.append({
                "gene": gene,
                "name": c.get("name"),
                "composite_score": c.get("composite_score"),
                "modality": c.get("modality"),
            })
    
    if all_candidates:
        stats["best_candidate"] = max(all_candidates, key=lambda x: x["composite_score"])["name"]
        stats["best_candidate_score"] = max(c["composite_score"] for c in all_candidates)
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="ARP v24 AutoRun x100")
    parser.add_argument("-d", "--disease", default="masld", 
                        help="Disease: masld, sarcopenia, lung_fibrosis, heart_failure, cancer")
    parser.add_argument("-n", "--n_iterations", type=int, default=100)
    parser.add_argument("-t", "--top-n", type=int, default=10, help="Number of targets per run")
    parser.add_argument("-o", "--output", help="Output JSON file")
    args = parser.parse_args()
    
    disease = args.disease
    n_iterations = args.n_iterations
    top_n = args.top_n
    
    print("=" * 70)
    print(f"  ARP v24 AutoRun x{n_iterations}")
    print("=" * 70)
    print(f"  Disease: {disease}")
    print(f"  Top targets per run: {top_n}")
    print(f"  Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    all_stats = []
    best_score = 0
    best_result = None
    
    scores_over_time = []
    execution_times = []
    
    for i in range(1, n_iterations + 1):
        iter_start = time.time()
        result = run_single(disease, top_n, i)
        iter_time = time.time() - iter_start
        
        stats = collect_stats(result)
        stats["iteration"] = i
        stats["wall_time"] = round(iter_time, 2)
        all_stats.append(stats)
        
        execution_times.append(iter_time)
        scores_over_time.append(stats.get("top_score", 0) or 0)
        
        # Track best
        if stats.get("top_score", 0) > best_score:
            best_score = stats["top_score"]
            best_result = result
        
        # Progress every 10 iterations
        if i % 10 == 0:
            recent = scores_over_time[-10:]
            print(f"\n📊 Progress: {i}/{n_iterations}")
            print(f"   Avg time: {sum(execution_times[-10:])/10:.1f}s")
            print(f"   Recent scores: {sum(recent)/len(recent):.4f}")
            if best_result:
                print(f"   Best so far: {best_result.targets[0].gene_name} = {best_score:.4f}")
    
    # Calculate overall statistics
    all_scores = [s.get("top_score", 0) or 0 for s in all_stats]
    
    print("\n" + "=" * 70)
    print("  AUTORUN x100 COMPLETE")
    print("=" * 70)
    
    print(f"\n📈 Target Score Statistics:")
    print(f"   Mean:   {sum(all_scores)/len(all_scores):.4f}")
    print(f"   Std:    {((sum((s - sum(all_scores)/len(all_scores))**2 for s in all_scores)/len(all_scores))**0.5):.4f}")
    print(f"   Max:    {max(all_scores):.4f}")
    print(f"   Min:    {min(all_scores):.4f}")
    
    print(f"\n⏱️  Execution Time:")
    print(f"   Mean:   {sum(execution_times)/len(execution_times):.2f}s")
    print(f"   Total:  {sum(execution_times):.1f}s")
    
    # Gene frequency
    gene_counts = defaultdict(int)
    for s in all_stats:
        gene_counts[s.get("top_gene", "UNKNOWN")] += 1
    
    print(f"\n🧬 Top Gene Frequency:")
    for gene, count in sorted(gene_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"   {gene}: {count}/{n_iterations} ({100*count/n_iterations:.0f}%)")
    
    # Modality distribution
    modality_counts = defaultdict(int)
    for s in all_stats:
        for mod in s.get("top_modalities", []):
            modality_counts[mod] += 1
    
    print(f"\n🎯 Modality Distribution:")
    for mod, count in sorted(modality_counts.items(), key=lambda x: -x[1]):
        print(f"   {mod}: {count}")
    
    print(f"\n🏆 Best Result:")
    if best_result and best_result.targets:
        top = best_result.targets[0]
        print(f"   Gene: {top.gene_name}")
        print(f"   Score: {best_score:.4f}")
        print(f"   Modalities: {top.recommended_modalities[:3]}")
    
    # Save results
    output = {
        "version": "24.0",
        "disease": disease,
        "n_iterations": n_iterations,
        "top_n": top_n,
        "timestamp": datetime.now().isoformat(),
        "statistics": {
            "scores": {
                "mean": sum(all_scores) / len(all_scores),
                "std": ((sum((s - sum(all_scores)/len(all_scores))**2 for s in all_scores) / len(all_scores))**0.5),
                "max": max(all_scores),
                "min": min(all_scores),
            },
            "execution_time": {
                "mean": sum(execution_times) / len(execution_times),
                "total": sum(execution_times),
            },
            "gene_frequency": dict(gene_counts),
            "modality_distribution": dict(modality_counts),
        },
        "all_stats": all_stats,
        "best": {
            "gene": best_result.targets[0].gene_name if best_result and best_result.targets else None,
            "score": best_score,
            "modalities": best_result.targets[0].recommended_modalities[:3] if best_result and best_result.targets else [],
        }
    }
    
    filename = args.output or f"arp_v24_{disease}_autorun{n_iterations}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n💾 Results saved: {filename}")
    print("=" * 70)
    
    return output


if __name__ == "__main__":
    main()