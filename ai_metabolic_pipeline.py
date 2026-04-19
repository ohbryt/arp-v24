"""
PHGDH AI-Driven Metabolic Dependency Analysis Pipeline
=====================================================

A complete, executable pipeline for:
1. PHGDH dependency scoring
2. Tumor stratification
3. Survival analysis
4. Drug combination prediction
5. Digital twin simulation

Usage:
    python ai_metabolic_pipeline.py --input data.csv --output results/

Requirements:
    pip install pandas numpy scikit-learn lifelines umap-learn scipy matplotlib seaborn

Author: ARP v24 Framework
Version: 2.0 (2026-04-19)
"""

import os
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ML libraries
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Survival analysis
from lifelines import KaplanMeierFitter, CoxPHFitter, NelsonAalenFitter
from lifelines.statistics import logrank_test

# Visualization
import umap.umap_ as umap

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Pipeline configuration."""
    
    # PHGDH pathway genes for scoring
    PHGDH_PATHWAY_GENES = [
        'PHGDH',      # Phosphoglycerate dehydrogenase
        'PSAT1',      # Phosphoserine aminotransferase
        'PSPH',       # Phosphoserine phosphatase
        'SHMT1',      # Serine hydroxymethyltransferase (cytosolic)
        'SHMT2',      # Serine hydroxymethyltransferase (mitochondrial)
        'MTHFD1',     # Methylenetetrahydrofolate dehydrogenase (cytosolic)
        'MTHFD2',     # Methylenetetrahydrofolate dehydrogenase (mitochondrial)
        'MTHFD2L',    # Methylenetetrahydrofolate dehydrogenase (like)
        'GLYCTK',     # Glycerate kinase
    ]
    
    # Extended metabolic genes
    METABOLIC_GENES = [
        # Glycolysis
        'HK2', 'PFKM', 'PKM', 'LDHA', 'LDHB',
        # Glutamine metabolism
        'GLS', 'GLS2', 'GLUD1', 'GLUD2',
        # Serine/glycine pathway
        *PHGDH_PATHWAY_GENES,
        # One-carbon metabolism
        'MTHFR', 'TYMS', 'ATIC',
        # NADPH production
        'IDH1', 'IDH2', 'IDH3A', 'ME1', 'ME2', 'MPC1', 'MPC2',
        # Ferroptosis-related
        'GPX4', 'SLC7A11', 'SLC3A2', 'FTH1', 'FTL',
        # mTOR pathway
        'MTOR', 'RPS6KB1', 'RPS6KB2', 'AKT1', 'AKT2',
    ]
    
    # Thresholds
    PHGDH_HIGH_THRESHOLD = 0.65
    PHGDH_MODERATE_THRESHOLD = 0.40
    
    # Colors
    COLORS = {
        'PHGDH_high': '#E63946',
        'PHGDH_low': '#457B9D',
        'PHGDH_moderate': '#F4A261',
    }
    
    # Output directory
    OUTPUT_DIR = Path('phgdh_analysis_results')


# =============================================================================
# DATA LOADING
# =============================================================================

def load_tcga_data(data_dir='data/tcga'):
    """
    Load TCGA data.
    
    In production, this would download from GDC API.
    For demo, we create synthetic data.
    """
    print("\n" + "="*60)
    print("LOADING DATA")
    print("="*60)
    
    # Check for real data first
    rna_file = Path(data_dir) / 'tcga_rna_expression.csv'
    survival_file = Path(data_dir) / 'tcga_survival.csv'
    
    if rna_file.exists() and survival_file.exists():
        print(f"Loading TCGA data from {data_dir}")
        df_rna = pd.read_csv(rna_file, index_col=0)
        df_surv = pd.read_csv(survival_file, index_col=0)
        
        # Merge
        df = df_rna.join(df_surv, how='inner')
        print(f"  Loaded {len(df)} samples")
        return df
    
    # Generate synthetic data for demonstration
    print("Generating synthetic TCGA-like data for demonstration...")
    np.random.seed(42)
    
    n_samples = 500
    n_genes = len(Config.METABOLIC_GENES)
    
    # Create expression matrix
    expr_data = np.random.randn(n_samples, n_genes) + 2
    # Add PHGDH-high cluster
    high_mask = np.random.choice(n_samples, int(n_samples * 0.35), replace=False)
    expr_data[high_mask, :7] += 1.5  # PHGDH pathway genes higher
    
    df = pd.DataFrame(
        expr_data,
        columns=Config.METABOLIC_GENES,
        index=[f'TCGA_{i:04d}' for i in range(n_samples)]
    )
    
    # Add survival data
    df['OS_time'] = np.random.exponential(36, n_samples)  # months
    df['OS_event'] = np.random.binomial(1, 0.6, n_samples)  # 60% events
    df['PFS_time'] = np.random.exponential(24, n_samples)
    df['PFS_event'] = np.random.binomial(1, 0.5, n_samples)
    df['cancer_type'] = np.random.choice(
        ['BRCA', 'LUAD', 'COAD', 'PAAD', 'SKCM', 'OV', 'KIRC'],
        n_samples
    )
    
    # Add PHGDH cluster labels (for evaluation)
    df['true_PHGDH_cluster'] = 0
    df.loc[df.index[high_mask], 'true_PHGDH_cluster'] = 1
    
    print(f"  Generated {len(df)} synthetic samples")
    return df


def load_ccle_data(data_dir='data/ccle'):
    """Load CCLE cell line data."""
    print(f"\nLoading CCLE data from {data_dir}")
    
    ccle_file = Path(data_dir) / 'ccle_expression.csv'
    
    if ccle_file.exists():
        df = pd.read_csv(ccle_file, index_col=0)
        print(f"  Loaded {len(df)} cell lines")
        return df
    
    # Generate synthetic CCLE data
    np.random.seed(123)
    
    n_samples = 200
    n_genes = len(Config.METABOLIC_GENES)
    
    expr_data = np.random.randn(n_samples, n_genes) + 2
    high_mask = np.random.choice(n_samples, int(n_samples * 0.38), replace=False)
    expr_data[high_mask, :7] += 1.8
    
    df = pd.DataFrame(
        expr_data,
        columns=Config.METABOLIC_GENES,
        index=[f'CCLE_{i:04d}' for i in range(n_samples)]
    )
    df['cancer_type'] = np.random.choice(
        ['BREAST', 'LUNG', 'COLON', 'PANCREAS', 'MELANOMA'],
        n_samples
    )
    df['PHGDH_essentiality'] = np.where(
        high_mask,
        np.random.choice([-1.5, -2.0, -2.5], len(high_mask)),
        np.random.choice([0.2, 0.5, 0.8], len(high_mask))
    )
    
    print(f"  Generated {len(df)} synthetic cell lines")
    return df


# =============================================================================
# PHGDH SCORING
# =============================================================================

def calculate_phgdh_score(df, genes=None, method='mean'):
    """
    Calculate PHGDH dependency score.
    
    Parameters:
    -----------
    df : DataFrame
        Gene expression data (samples × genes)
    genes : list, optional
        Genes to include in score
    method : str
        'mean', 'median', 'weighted', 'pca', 'rf'
    
    Returns:
    --------
    Series : PHGDH score for each sample
    """
    print("\n" + "="*60)
    print("CALCULATING PHGDH SCORE")
    print("="*60)
    
    if genes is None:
        genes = Config.PHGDH_PATHWAY_GENES
    
    # Filter to available genes
    available_genes = [g for g in genes if g in df.columns]
    print(f"Using {len(available_genes)} genes: {available_genes}")
    
    expr_subset = df[available_genes].copy()
    
    if method == 'mean':
        score = expr_subset.mean(axis=1)
        
    elif method == 'median':
        score = expr_subset.median(axis=1)
        
    elif method == 'weighted':
        # Weight PHGDH higher than other pathway genes
        weights = np.array([1.5 if g == 'PHGDH' else 1.0 for g in available_genes])
        weights = weights / weights.sum() * len(weights)
        score = (expr_subset * weights).sum(axis=1)
        
    elif method == 'pca':
        # PCA-based score
        scaler = StandardScaler()
        expr_scaled = scaler.fit_transform(expr_subset)
        pca = PCA(n_components=1)
        score = pca.fit_transform(expr_scaled).flatten()
        
    elif method == 'rf':
        # Random Forest-based importance
        scaler = StandardScaler()
        X = scaler.fit_transform(expr_subset)
        y = df.get('true_PHGDH_cluster', None)
        
        if y is not None:
            rf = RandomForestClassifier(n_estimators=100, random_state=42)
            rf.fit(X, y)
            score = pd.Series(rf.predict_proba(X)[:, 1], index=df.index)
        else:
            # Unsupervised: use first principal component
            pca = PCA(n_components=1)
            score = pca.fit_transform(X).flatten()
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Normalize to 0-1
    score = (score - score.min()) / (score.max() - score.min())
    
    print(f"PHGDH score range: {score.min():.3f} - {score.max():.3f}")
    print(f"PHGDH score mean: {score.mean():.3f}")
    
    return score


def classify_phgdh_dependency(score, threshold_high=0.65, threshold_low=0.35):
    """
    Classify tumors based on PHGDH score.
    
    Returns:
    --------
    Series : Classification (high, moderate, low)
    """
    classification = pd.Series('low', index=score.index)
    classification[score >= threshold_high] = 'high'
    classification[(score > threshold_low) & (score < threshold_high)] = 'moderate'
    
    counts = classification.value_counts()
    print(f"\nPHGDH Classification:")
    for cat in ['high', 'moderate', 'low']:
        if cat in counts:
            pct = counts[cat] / len(classification) * 100
            print(f"  {cat.upper()}: {counts[cat]} ({pct:.1f}%)")
    
    return classification


# =============================================================================
# CLUSTERING
# =============================================================================

def perform_clustering(df, genes, n_clusters=2, method='kmeans'):
    """
    Perform unsupervised clustering on metabolic genes.
    """
    print("\n" + "="*60)
    print("PERFORMING CLUSTERING")
    print("="*60)
    
    # Prepare data
    X = df[genes].copy()
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    if method == 'kmeans':
        clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        
    elif method == 'hierarchical':
        clusterer = AgglomerativeClustering(n_clusters=n_clusters)
        
    else:
        raise ValueError(f"Unknown method: {method}")
    
    labels = clusterer.fit_predict(X_scaled)
    
    # Evaluate clustering
    sil_score = silhouette_score(X_scaled, labels)
    ch_score = calinski_harabasz_score(X_scaled, labels)
    
    print(f"Method: {method.upper()}")
    print(f"Silhouette Score: {sil_score:.3f}")
    print(f"Calinski-Harabasz Score: {ch_score:.1f}")
    
    # Map clusters to PHGDH high/low
    cluster_means = pd.DataFrame(X, columns=genes).groupby(labels).mean()
    phgdh_means = cluster_means['PHGDH'].sort_values(ascending=False)
    
    cluster_map = {}
    for i, cluster_id in enumerate(phgdh_means.index):
        if i == 0:
            cluster_map[cluster_id] = 'PHGDH_high'
        else:
            cluster_map[cluster_id] = 'PHGDH_low'
    
    cluster_labels = pd.Series([cluster_map[l] for l in labels], index=df.index)
    
    print(f"\nCluster mapping:")
    for old, new in cluster_map.items():
        count = (labels == old).sum()
        print(f"  Cluster {old} → {new}: {count} samples")
    
    return cluster_labels, labels


def dimensionality_reduction(df, genes, method='umap', n_components=2):
    """
    Reduce dimensionality for visualization.
    """
    print(f"\nDimensionality reduction: {method.upper()}")
    
    X = df[genes].copy()
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)
    
    if method == 'umap':
        reducer = umap.UMAP(
            n_components=n_components,
            random_state=42,
            n_neighbors=15,
            min_dist=0.3
        )
        
    elif method == 'tsne':
        reducer = TSNE(
            n_components=n_components,
            random_state=42,
            perplexity=30
        )
        
    elif method == 'pca':
        reducer = PCA(n_components=n_components, random_state=42)
        
    else:
        raise ValueError(f"Unknown method: {method}")
    
    embedding = reducer.fit_transform(X_scaled)
    
    result = pd.DataFrame(
        embedding,
        columns=[f'{method.upper()}_{i+1}' for i in range(n_components)],
        index=df.index
    )
    
    return result


# =============================================================================
# SURVIVAL ANALYSIS
# =============================================================================

def survival_analysis(df, score_col='PHGDH_score', time_col='OS_time', event_col='OS_event'):
    """
    Perform comprehensive survival analysis.
    """
    print("\n" + "="*60)
    print("SURVIVAL ANALYSIS")
    print("="*60)
    
    # Prepare data
    df_surv = df[[score_col, time_col, event_col]].dropna()
    
    # Classification
    df_surv['PHGDH_group'] = 'low'
    df_surv.loc[df_surv[score_col] >= Config.PHGDH_HIGH_THRESHOLD, 'PHGDH_group'] = 'high'
    df_surv.loc[
        (df_surv[score_col] > Config.PHGDH_MODERATE_THRESHOLD) & 
        (df_surv[score_col] < Config.PHGDH_HIGH_THRESHOLD), 
        'PHGDH_group'
    ] = 'moderate'
    
    # Kaplan-Meier
    kmf = KaplanMeierFitter()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot by group
    for group in ['high', 'moderate', 'low']:
        mask = df_surv['PHGDH_group'] == group
        if mask.sum() > 0:
            kmf.fit(
                df_surv.loc[mask, time_col],
                event_observed=df_surv.loc[mask, event_col],
                label=f'PHGDH-{group.upper()} (n={mask.sum()})'
            )
            kmf.plot_survival_function(ax=axes[0])
    
    axes[0].set_title('Kaplan-Meier Survival by PHGDH Group', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Time (months)')
    axes[0].set_ylabel('Survival Probability')
    
    # PHGDH score as continuous
    axes[1].hist(df_surv[score_col], bins=50, edgecolor='black', alpha=0.7)
    axes[1].axvline(Config.PHGDH_HIGH_THRESHOLD, color='red', linestyle='--', label='High threshold')
    axes[1].axvline(Config.PHGDH_MODERATE_THRESHOLD, color='orange', linestyle='--', label='Moderate threshold')
    axes[1].set_title('PHGDH Score Distribution', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('PHGDH Score')
    axes[1].set_ylabel('Count')
    axes[1].legend()
    
    plt.tight_layout()
    
    # Save figure
    output_path = Config.OUTPUT_DIR / 'survival_analysis.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()
    
    # Log-rank test
    high_mask = df_surv['PHGDH_group'] == 'high'
    low_mask = df_surv['PHGDH_group'] == 'low'
    
    if high_mask.sum() > 0 and low_mask.sum() > 0:
        results = logrank_test(
            df_surv.loc[high_mask, time_col],
            df_surv.loc[low_mask, time_col],
            event_observed_A=df_surv.loc[high_mask, event_col],
            event_observed_B=df_surv.loc[low_mask, event_col]
        )
        
        print(f"\nLog-rank test (High vs Low):")
        print(f"  Test statistic: {results.test_statistic:.3f}")
        print(f"  P-value: {results.p_value:.2e}")
    
    # Cox proportional hazards
    df_surv['PHGDH_high'] = (df_surv['PHGDH_group'] == 'high').astype(int)
    
    cph = CoxPHFitter()
    try:
        cph.fit(df_surv[[time_col, event_col, 'PHGDH_high', score_col]], 
                duration_col=time_col, 
                event_col=event_col)
        
        print("\nCox Proportional Hazards Model:")
        cph.print_summary()
        
        # Forest plot
        fig, ax = plt.subplots(figsize=(8, 4))
        cph.plot(ax=ax)
        ax.set_title('Cox PH Forest Plot', fontsize=12, fontweight='bold')
        
        output_path = Config.OUTPUT_DIR / 'cox_forest_plot.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {output_path}")
        plt.close()
        
    except Exception as e:
        print(f"Cox fitting failed: {e}")
    
    return df_surv


# =============================================================================
# DRUG PREDICTION
# =============================================================================

def predict_drug_combination(df, phgdh_score):
    """
    Predict optimal drug combinations based on PHGDH profile.
    
    Returns:
    --------
    DataFrame : Drug recommendations
    """
    print("\n" + "="*60)
    print("DRUG COMBINATION PREDICTION")
    print("="*60)
    
    recommendations = []
    
    for idx, row in df.iterrows():
        score = row[phgdh_score]
        
        # ROS signature (simplified proxy from GSS/GPX4)
        ros_genes = ['GPX4', 'SLC7A11', 'FTH1']
        available_ros = [g for g in ros_genes if g in row.index]
        
        if available_ros:
            ros_signature = row[available_ros].mean()
        else:
            ros_signature = 0
        
        # Primary recommendation
        if score >= Config.PHGDH_HIGH_THRESHOLD:
            if ros_signature > 1.5:
                therapy = "PHGDH inhibitor + GLS inhibitor + Ferroptosis inducer"
                confidence = 0.89
                rationale = "PHGDH-high + high ROS = ferroptosis vulnerability"
            else:
                therapy = "PHGDH inhibitor + GLS inhibitor"
                confidence = 0.82
                rationale = "PHGDH-high with standard combination"
                
        elif score >= Config.PHGDH_MODERATE_THRESHOLD:
            therapy = "GLS inhibitor + mTOR inhibitor"
            confidence = 0.74
            rationale = "Moderate PHGDH, alternative targeting"
            
        else:
            therapy = "Standard of care + metabolic monitoring"
            confidence = 0.65
            rationale = "Low PHGDH, standard approach"
        
        recommendations.append({
            'sample': idx,
            'PHGDH_score': score,
            'ROS_signature': ros_signature,
            'therapy': therapy,
            'confidence': confidence,
            'rationale': rationale
        })
    
    df_rec = pd.DataFrame(recommendations)
    
    print("\nRecommendation Summary:")
    print(df_rec['therapy'].value_counts())
    
    return df_rec


# =============================================================================
# DIGITAL TWIN SIMULATION
# =============================================================================

def simulate_treatment_response(phgdh_baseline, therapy_combo, n_days=28):
    """
    Simple ODE-based simulation of treatment response.
    
    Parameters:
    -----------
    phgdh_baseline : float
        Initial PHGDH activity (0-1)
    therapy_combo : list
        Therapies to simulate
    n_days : int
        Simulation duration
    
    Returns:
    --------
    dict : Time series of metabolic state
    """
    # Initialize state
    state = {
        'PHGDH': [phgdh_baseline],
        'GLS': [1.0],
        'NADPH': [1.0],
        'ROS': [0.5],
        'Viability': [1.0],
        'Ferroptosis_risk': [0.1]
    }
    
    dt = 1  # 1 day
    
    for day in range(n_days):
        # Current values
        phgdh = state['PHGDH'][-1]
        gls = state['GLS'][-1]
        nadph = state['NADPH'][-1]
        ros = state['ROS'][-1]
        
        # Apply therapy effects
        phgdh_effect = 1.0
        gls_effect = 1.0
        ferroptosis_effect = 0
        
        for therapy in therapy_combo:
            if therapy == 'PHGDH_inhibitor':
                phgdh_effect = 0.3  # 70% inhibition
            elif therapy == 'GLS_inhibitor':
                gls_effect = 0.4  # 60% inhibition
            elif therapy == 'Ferroptosis_inducer':
                ferroptosis_effect = 1.5
        
        # Update PHGDH (compensatory upregulation)
        # When inhibited, PHGDH tries to compensate
        phgdh_inhibition = phgdh_effect
        compensation = 0.1 * (1 - phgdh_inhibition)  # Compensation proportional to inhibition
        new_phgdh = phgdh * phgdh_inhibition + compensation
        new_phgdh = min(2.0, max(0.1, new_phgdh))  # Bounds
        
        # Update GLS
        new_gls = gls * gls_effect
        
        # Update NADPH (depends on PHGDH and GLS)
        phgdh_nadph = 0.4 * new_phgdh
        gls_nadph = 0.3 * new_gls
        nadph_production = phgdh_nadph + gls_nadph
        nadph_consumption = 0.3 + 0.2 * ros
        new_nadph = nadph + 0.1 * (nadph_production - nadph_consumption)
        new_nadph = min(2.0, max(0.2, new_nadph))
        
        # Update ROS
        ros_production = 0.3 + 0.2 * (1 - new_nadph)
        ros_detox = 0.4 * new_nadph
        new_ros = ros + 0.1 * (ros_production - ros_detox)
        new_ros = min(3.0, max(0.1, new_ros))
        
        # Calculate viability
        metabolic_health = (new_nadph / 2) * (1 / (1 + new_ros))
        new_viability = 0.7 + 0.3 * metabolic_health
        
        # Ferroptosis risk
        fp_risk = (new_ros * ferroptosis_effect) / (new_nadph * (1 + 0.5 * ferroptosis_effect))
        new_fp_risk = min(1.0, fp_risk)
        
        # Apply ferroptosis
        if new_fp_risk > 0.7:
            new_viability *= (1 - 0.3 * (new_fp_risk - 0.7))
        
        # Store
        state['PHGDH'].append(new_phgdh)
        state['GLS'].append(new_gls)
        state['NADPH'].append(new_nadph)
        state['ROS'].append(new_ros)
        state['Viability'].append(new_viability)
        state['Ferroptosis_risk'].append(new_fp_risk)
    
    return state


def run_digital_twin(df, phgdh_score_col='PHGDH_score', n_samples=10):
    """
    Run digital twin simulation for patient cohort.
    """
    print("\n" + "="*60)
    print("DIGITAL TWIN SIMULATION")
    print("="*60)
    
    # Select samples
    sample_indices = np.random.choice(df.index, min(n_samples, len(df)), replace=False)
    
    # Therapy combinations to test
    therapies = [
        ['PHGDH_inhibitor'],
        ['GLS_inhibitor'],
        ['PHGDH_inhibitor', 'GLS_inhibitor'],
        ['PHGDH_inhibitor', 'Ferroptosis_inducer'],
        ['PHGDH_inhibitor', 'GLS_inhibitor', 'Ferroptosis_inducer'],
    ]
    
    results = []
    
    for sample in sample_indices:
        phgdh_score = df.loc[sample, phgdh_score_col]
        
        for therapy in therapies:
            sim = simulate_treatment_response(phgdh_score, therapy)
            
            results.append({
                'sample': sample,
                'therapy': ' + '.join(therapy),
                'final_viability': sim['Viability'][-1],
                'final_phgdh': sim['PHGDH'][-1],
                'final_nadph': sim['NADPH'][-1],
                'final_ros': sim['ROS'][-1],
                'final_ferroptosis_risk': sim['Ferroptosis_risk'][-1],
                'phgdh_score': phgdh_score
            })
    
    df_results = pd.DataFrame(results)
    
    # Find optimal therapy per sample
    df_optimal = df_results.loc[df_results.groupby('sample')['final_viability'].idxmin()]
    
    print("\nOptimal Therapy by Sample:")
    print(df_optimal[['sample', 'phgdh_score', 'therapy', 'final_viability']].to_string())
    
    # Summary
    print("\nTherapy Effectiveness Summary:")
    summary = df_results.groupby('therapy').agg({
        'final_viability': 'mean',
        'final_ros': 'mean',
        'final_ferroptosis_risk': 'mean'
    }).round(3)
    print(summary)
    
    return df_results, df_optimal


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_visualizations(df, phgdh_score_col='PHGDH_score', cluster_col='cluster'):
    """
    Create comprehensive visualization dashboard.
    """
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # 1. UMAP + Clustering
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # UMAP colored by PHGDH score
    umap_result = dimensionality_reduction(df, Config.PHGDH_PATHWAY_GENES, method='umap')
    
    ax = axes[0, 0]
    scatter = ax.scatter(
        umap_result['UMAP_1'],
        umap_result['UMAP_2'],
        c=df[phgdh_score_col],
        cmap='RdYlBu_r',
        alpha=0.6,
        s=20
    )
    ax.set_title('UMAP: PHGDH Pathway Genes', fontsize=12, fontweight='bold')
    ax.set_xlabel('UMAP 1')
    ax.set_ylabel('UMAP 2')
    plt.colorbar(scatter, ax=ax, label='PHGDH Score')
    
    # Cluster distribution
    ax = axes[0, 1]
    cluster_counts = df[cluster_col].value_counts()
    colors = [Config.COLORS.get(c, '#888888') for c in cluster_counts.index]
    ax.pie(cluster_counts, labels=cluster_counts.index, autopct='%1.1f%%', colors=colors)
    ax.set_title('PHGDH Cluster Distribution', fontsize=12, fontweight='bold')
    
    # Gene expression heatmap
    ax = axes[1, 0]
    top_samples = df.nlargest(50, phgdh_score_col).index
    expr_subset = df.loc[top_samples, Config.PHGDH_PATHWAY_GENES]
    expr_scaled = (expr_subset - expr_subset.mean()) / expr_subset.std()
    
    sns.heatmap(
        expr_scaled.T,
        cmap='RdYlBu_r',
        ax=ax,
        cbar_kws={'label': 'Z-score'}
    )
    ax.set_title('Top 50 PHGDH-High: Gene Expression', fontsize=12, fontweight='bold')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Genes')
    
    # PHGDH score distribution by cluster
    ax = axes[1, 1]
    for cluster in df[cluster_col].unique():
        mask = df[cluster_col] == cluster
        ax.hist(
            df.loc[mask, phgdh_score_col],
            bins=30,
            alpha=0.6,
            label=f'Cluster {cluster}',
            color=Config.COLORS.get(cluster, '#888888')
        )
    ax.axvline(Config.PHGDH_HIGH_THRESHOLD, color='red', linestyle='--', label='High threshold')
    ax.set_title('PHGDH Score Distribution by Cluster', fontsize=12, fontweight='bold')
    ax.set_xlabel('PHGDH Score')
    ax.set_ylabel('Count')
    ax.legend()
    
    plt.tight_layout()
    
    output_path = Config.OUTPUT_DIR / 'clustering_visualization.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()
    
    # 2. Pathway diagram
    create_pathway_diagram()


def create_pathway_diagram():
    """
    Create metabolic pathway diagram.
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(8, 9.5, 'PHGDH Metabolic Network in Cancer', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Nodes
    nodes = {
        'Glucose': (2, 6),
        '3-PG': (4, 6),
        'PHGDH': (6, 6),
        '3-PHP': (8, 6),
        'Serine': (10, 6),
        'Glycine': (11, 4),
        'Cysteine': (11, 8),
        'One-Carbon': (13, 6),
        'NADPH': (13, 4),
        'ROS': (13, 8),
        'GLS': (4, 3),
        'Glu': (6, 3),
        'GLS2': (8, 3),
    }
    
    # Draw nodes
    for name, (x, y) in nodes.items():
        if name == 'PHGDH':
            color = '#E63946'
            size = 0.4
        elif name in ['NADPH', 'ROS']:
            color = '#F4A261'
            size = 0.3
        else:
            color = '#457B9D'
            size = 0.25
            
        circle = plt.Circle((x, y), size, color=color, ec='black', lw=1)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Arrows (simplified)
    arrows = [
        ('Glucose', '3-PG'),
        ('3-PG', 'PHGDH'),
        ('PHGDH', '3-PHP'),
        ('3-PHP', 'Serine'),
        ('Serine', 'Glycine'),
        ('Serine', 'Cysteine'),
        ('Glycine', 'One-Carbon'),
        ('Cysteine', 'One-Carbon'),
        ('One-Carbon', 'NADPH'),
        ('NADPH', 'ROS'),
        ('Glucose', 'GLS'),
        ('GLS', 'Glu'),
        ('Glu', 'GLS2'),
    ]
    
    for start, end in arrows:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        ax.annotate('', xy=(x2-0.3, y2), xytext=(x1+0.3, y1),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1))
    
    # Legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor='#E63946', label='PHGDH (Target)'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#F4A261', label='NADPH/ROS'),
        plt.Rectangle((0, 0), 1, 1, facecolor='#457B9D', label='Metabolites'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    
    output_path = Config.OUTPUT_DIR / 'pathway_diagram.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def main():
    """Main pipeline execution."""
    
    parser = argparse.ArgumentParser(description='PHGDH AI Analysis Pipeline')
    parser.add_argument('--input', type=str, default='data',
                       help='Input data directory')
    parser.add_argument('--output', type=str, default='phgdh_analysis_results',
                       help='Output directory')
    parser.add_argument('--tcga', action='store_true',
                       help='Load TCGA data')
    parser.add_argument('--ccle', action='store_true',
                       help='Load CCLE data')
    
    args = parser.parse_args()
    
    # Create output directory
    global Config
    Config.OUTPUT_DIR = Path(args.output)
    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("PHGDH AI-DRIVEN METABOLIC DEPENDENCY ANALYSIS PIPELINE")
    print("="*70)
    print(f"Version: 2.0")
    print(f"Date: 2026-04-19")
    print(f"Output: {Config.OUTPUT_DIR}")
    print("="*70)
    
    # Step 1: Load data
    if args.tcga:
        df = load_tcga_data(args.input)
    elif args.ccle:
        df = load_ccle_data(args.input)
    else:
        df = load_tcga_data(args.input)
    
    # Step 2: Calculate PHGDH score
    df['PHGDH_score'] = calculate_phgdh_score(df, method='mean')
    
    # Step 3: Classify
    df['PHGDH_class'] = classify_phgdh_dependency(df['PHGDH_score'])
    
    # Step 4: Clustering
    df['cluster'], _ = perform_clustering(df, Config.PHGDH_PATHWAY_GENES)
    
    # Step 5: Survival analysis (if survival data available)
    if 'OS_time' in df.columns:
        survival_results = survival_analysis(df)
        df = df.join(survival_results[['PHGDH_group']], rsuffix='_surv')
    
    # Step 6: Drug prediction
    df_rec = predict_drug_combination(df, 'PHGDH_score')
    df = df.join(df_rec.set_index('sample'))
    
    # Step 7: Digital twin simulation
    if len(df) <= 100:
        sim_results, optimal_therapy = run_digital_twin(df, n_samples=len(df))
    else:
        sim_results, optimal_therapy = run_digital_twin(df, n_samples=50)
    
    # Step 8: Visualizations
    create_visualizations(df)
    
    # Save results
    df.to_csv(Config.OUTPUT_DIR / 'analysis_results.csv')
    df_rec.to_csv(Config.OUTPUT_DIR / 'drug_recommendations.csv', index=False)
    sim_results.to_csv(Config.OUTPUT_DIR / 'simulation_results.csv', index=False)
    
    print("\n" + "="*70)
    print("PIPELINE COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {Config.OUTPUT_DIR}")
    print("\nOutput files:")
    for f in Config.OUTPUT_DIR.glob('*'):
        print(f"  - {f.name}")
    print("="*70)
    
    return df


if __name__ == '__main__':
    main()
