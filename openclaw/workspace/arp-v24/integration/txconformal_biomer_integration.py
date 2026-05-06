"""
TxConformal + BioMiner Integration
====================================
Takes BioMiner/AI predictions for drug targets, applies conformal FDR control
(Benjamini–Hochberg at α=0.1), and outputs filtered high-confidence candidates.

Target genes: KDM4A, SLC7A11, DGAT1 (ferroptosis/cancer relevance)

Usage:
    python txconformal_biomer_integration.py

The script:
  1. Loads or creates synthetic BioMiner predictions (compounds × targets)
  2. Splits into calibration (known active/inactive) and test (virtual library) sets
  3. Runs TxConformal with BH selection at α=0.1
  4. Reports selected compounds per target with p-values and estimated FDP
"""

import numpy as np
import pandas as pd
from pathlib import Path

# TxConformal core
from txconformal import TxConformal
from txconformal.features.providers import FeaturesProvider


# =============================================================================
# 1. Synthetic BioMiner data (swap this block for real BioMiner CSV/JSON)
# =============================================================================
def generate_synthetic_biomer_predictions(
    n_calib: int = 300,
    n_test: int = 500,
    targets: list[str] = None,
    rng: np.random.Generator = None,
) -> dict[str, pd.DataFrame]:
    """
    Generate synthetic BioMiner-style prediction tables for test targets.

    Each target gets:
      - calib_preds:  ground-truth labels (0/1) + AI scores for n_calib compounds
      - test_preds:   AI scores only for n_test virtual-library compounds

    In synthetic data, higher score = more likely active.
    We inject ~15% truly active compounds in calib, with elevated scores.
    """
    if targets is None:
        targets = ["KDM4A", "SLC7A11", "DGAT1"]
    if rng is None:
        rng = np.random.default_rng(42)

    results = {}
    for gene in targets:
        # --- Calibration set: known ground truth ---
        n_active = int(0.15 * n_calib)
        y_calib = np.array([1] * n_active + [0] * (n_calib - n_active))
        rng.shuffle(y_calib)

        # AI scores: active compounds get higher scores on average
        f_calib = np.where(
            y_calib == 1,
            rng.uniform(0.55, 0.95, n_calib),
            rng.uniform(0.05, 0.50, n_calib),
        )
        # Slight noise / batch effects (covariate shift)
        f_calib += rng.normal(0.0, 0.05, n_calib)
        f_calib = np.clip(f_calib, 0.0, 1.0)

        # --- Test set: virtual library, scores only ---
        f_test = rng.uniform(0.05, 0.90, n_test)
        f_test = np.clip(f_test, 0.0, 1.0)

        # Compound IDs
        calib_ids = [f"CALIB_{gene}_{i:04d}" for i in range(n_calib)]
        test_ids  = [f"TEST_{gene}_{i:04d}"  for i in range(n_test)]

        calib_df = pd.DataFrame({
            "compound_id": calib_ids,
            "target": gene,
            "y_true": y_calib,          # ground truth (for eval only)
            "ai_score": f_calib,         # BioMiner AI score
        })
        test_df = pd.DataFrame({
            "compound_id": test_ids,
            "target": gene,
            "ai_score": f_test,
        })
        results[gene] = {"calib": calib_df, "test": test_df}

    return results


# =============================================================================
# 2. Load real BioMiner predictions (stub — replace with actual I/O)
# =============================================================================
def load_biomer_predictions(
    path: str | Path = "biomer_predictions.csv",
) -> dict[str, pd.DataFrame]:
    """
    Load real BioMiner predictions from a CSV file.

    Expected CSV format (one row per compound-target pair):
        compound_id, target, ai_score, [y_true]

    Returns a dict: {gene: {"calib": DataFrame, "test": DataFrame}}
    Split by whether y_true is present (calib) or missing (test).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"BioMiner predictions not found: {p}")

    df = pd.read_csv(p)
    required = ["compound_id", "target", "ai_score"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")

    out = {}
    for gene, grp in df.groupby("target"):
        if "y_true" in grp.columns:
            out[gene] = {
                "calib": grp.dropna(subset=["y_true"]),
                "test":  grp[grp["y_true"].isna()],
            }
        else:
            # No labels — treat entire file as test set
            out[gene] = {"calib": pd.DataFrame(), "test": grp}
    return out


# =============================================================================
# 3. Run TxConformal selection per target
# =============================================================================
def run_selection(
    f_calib: np.ndarray,
    y_calib: np.ndarray,
    f_test: np.ndarray,
    *,
    method: str = "bh",
    alpha: float = 0.1,
    score_name: str = "clip",
    M: float = 100.0,
) -> dict:
    """
    Run TxConformal fit + select for one target.

    Parameters
    ----------
    f_calib : array (n_calib,)
        AI prediction scores for calibration compounds.
    y_calib : array (n_calib,)
        Binary ground-truth labels for calibration compounds (0=inactive, 1=active).
    f_test : array (n_test,)
        AI prediction scores for test/virtual-library compounds.
    method : str
        Selection method: 'bh' (Benjamini–Hochberg), 'top_k', 'fp_budget', 'tp_min'.
    alpha : float
        FDR level for BH method.

    Returns
    -------
    dict with keys: selected_idx, threshold, p_values, p_sel, fdp_est, result_obj
    """
    cutoff_calib = np.full_like(f_calib, 0.5)  # treat score > 0.5 as "selected"
    cutoff_test  = np.full_like(f_test,  0.5)

    # Build FeaturesProvider
    prov = FeaturesProvider(
        f_calib=f_calib,
        f_test=f_test,
    )
    prov.prepare(quantiles=10)

    # TxConformal pipeline
    tx = TxConformal(score_name=score_name, M=M)
    result = tx.fit_select(
        prov=prov,
        y_calib=y_calib,
        cutoff=cutoff_calib,
        method=method,
        alpha=alpha,
        print_level=-1,
    )

    return {
        "selected_idx":  result.idx,
        "threshold":    result.threshold,
        "p_values":     result.p_values,
        "p_sel":        result.p_sel,
        "fdp_est":      result.fdp_est,
        "fdp_est_CI":   result.fdp_est_CI,
        "method":       result.method,
        "alpha":        alpha,
        "n_selected":  len(result.idx),
        "result_obj":   result,
    }


# =============================================================================
# 4. Main pipeline
# =============================================================================
def main(
    biomer_path: str | Path | None = None,
    targets: list[str] = None,
    method: str = "bh",
    alpha: float = 0.1,
    n_calib: int = 300,
    n_test: int = 500,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Full pipeline: load/create predictions → run TxConformal → collect results.
    """
    if targets is None:
        targets = ["KDM4A", "SLC7A11", "DGAT1"]

    # --- Load or generate predictions ---
    if biomer_path and Path(biomer_path).exists():
        raw = load_biomer_predictions(biomer_path)
    else:
        print("[TxConformal] No real BioMiner data found — generating synthetic test data")
        raw = generate_synthetic_biomer_predictions(
            n_calib=n_calib, n_test=n_test, targets=targets
        )

    # --- Run selection per target ---
    all_selected = []
    summary_rows = []

    for gene in targets:
        if gene not in raw:
            print(f"[WARN] No data for target {gene}, skipping.")
            continue

        calib_df = raw[gene]["calib"]
        test_df  = raw[gene]["test"]

        if calib_df.empty or test_df.empty:
            print(f"[WARN] Empty dataset for {gene}, skipping.")
            continue

        f_calib = calib_df["ai_score"].values
        y_calib = calib_df["y_true"].values
        f_test  = test_df["ai_score"].values
        test_ids = test_df["compound_id"].values

        print(f"\n{'='*60}")
        print(f"Target: {gene}")
        print(f"  Calibration: {len(f_calib)} compounds ({int(y_calib.sum())} active)")
        print(f"  Test set:    {len(f_test)} compounds")

        sel = run_selection(
            f_calib, y_calib, f_test,
            method=method, alpha=alpha,
        )

        # --- Build selected candidates table ---
        if sel["n_selected"] > 0:
            selected_ids = test_ids[sel["selected_idx"]]
            selected_scores = f_test[sel["selected_idx"]]
            selected_p      = sel["p_sel"][sel["selected_idx"]]

            sel_df = pd.DataFrame({
                "compound_id": selected_ids,
                "target":      gene,
                "ai_score":   selected_scores,
                "p_value":    selected_p,
                "p_value_rank": np.argsort(np.argsort(selected_p)) + 1,
            })
            # Sort by p-value (most significant first)
            sel_df = sel_df.sort_values("p_value").reset_index(drop=True)
            all_selected.append(sel_df)

            print(f"  ➜ SELECTED: {sel['n_selected']} compounds (FDP est: {sel['fdp_est']:.3f})")
            if sel["fdp_est_CI"]:
                print(f"    FDP 95% CI: [{sel['fdp_est_CI'][0]:.3f}, {sel['fdp_est_CI'][1]:.3f}]")
        else:
            print(f"  ➜ No compounds passed FDR {alpha} threshold")
            sel_df = pd.DataFrame(columns=["compound_id","target","ai_score","p_value","p_value_rank"])
            all_selected.append(sel_df)

        summary_rows.append({
            "target":      gene,
            "method":      method,
            "alpha":       alpha,
            "n_calib":     len(f_calib),
            "n_active_calib": int(y_calib.sum()),
            "n_test":      len(f_test),
            "n_selected":  sel["n_selected"],
            "threshold":   round(sel["threshold"], 4),
            "fdp_est":     round(sel["fdp_est"], 4),
        })

    # --- Compile output ---
    summary_df  = pd.DataFrame(summary_rows)
    selected_df = pd.concat(all_selected, ignore_index=True) if all_selected else pd.DataFrame()

    print(f"\n{'='*60}")
    print("SUMMARY TABLE")
    print("=" * 60)
    print(summary_df.to_string(index=False))

    if output_path:
        out_path = Path(output_path)
        summary_df.to_csv(out_path.with_suffix(".summary.csv"), index=False)
        if not selected_df.empty:
            selected_df.to_csv(out_path.with_suffix(".selected.csv"), index=False)
        print(f"\nSaved: {out_path.with_suffix('.summary.csv')}")
        print(f"Saved: {out_path.with_suffix('.selected.csv')}")

    return selected_df


# =============================================================================
# 5. CLI entry point
# =============================================================================
if __name__ == "__main__":
    import argparse, textwrap, sys

    parser = argparse.ArgumentParser(
        prog="txconformal_biomer_integration.py",
        description="TxConformal FDR control for BioMiner drug-discovery predictions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples
            --------
            # Synthetic test run
            python txconformal_biomer_integration.py --alpha 0.1 --method bh

            # With real BioMiner CSV
            python txconformal_biomer_integration.py --biomer-path biomer_predictions.csv

            # Higher tolerance FDR
            python txconformal_biomer_integration.py --alpha 0.2 --method bh --n-calib 500
        """),
    )
    parser.add_argument("--biomer-path",  default=None,   help="Path to BioMiner CSV (optional)")
    parser.add_argument("--targets",     nargs="+",      default=["KDM4A","SLC7A11","DGAT1"],
                        help="Target gene names")
    parser.add_argument("--method",      default="bh",   choices=["bh","top_k","fp_budget","tp_min"],
                        help="Selection method (default: bh)")
    parser.add_argument("--alpha",       type=float,     default=0.1,
                        help="FDR level for BH method (default: 0.1)")
    parser.add_argument("--n-calib",     type=int,       default=300,
                        help="Size of calibration set for synthetic data")
    parser.add_argument("--n-test",      type=int,       default=500,
                        help="Size of test set for synthetic data")
    parser.add_argument("--output",      default=None,
                        help="Output CSV stem (adds .summary.csv and .selected.csv)")

    args = parser.parse_args()

    out = main(
        biomer_path=args.biomer_path,
        targets=args.targets,
        method=args.method,
        alpha=args.alpha,
        n_calib=args.n_calib,
        n_test=args.n_test,
        output_path=args.output,
    )

    print(f"\n✅ Pipeline complete. {len(out)} total candidates selected across all targets.")
    sys.exit(0)
