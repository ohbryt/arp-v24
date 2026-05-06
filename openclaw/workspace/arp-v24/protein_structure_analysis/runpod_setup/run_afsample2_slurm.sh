#!/bin/bash
#==============================================================================
# Slurm Batch Submission Script for AFSample2
# For HPC clusters with GPU nodes
#
# Usage:
#   sbatch run_afsample2_slurm.sh           # Run all targets
#   sbatch --job-name=KDM4A run_afsample2_slurm.sh KDM4A
#==============================================================================

#SBATCH --job-name=afsample2_batch
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --time=72:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=${USER}@example.com

# Configuration
export OUTPUT_BASE="${SLURM_SUBMIT_DIR}/output"
export NUM_SAMPLES=20
export AFSAMPLE2_REPO="https://github.com/mevalon/afsample2.git"

# Target proteins
TARGETS=("KDM4A" "SLC7A11" "DGAT1" "GPX4" "YARS2")

# Modules (adjust for your HPC environment)
module load python/3.10
module load cuda/12.0
module load cudnn/8.9

# Create directories
mkdir -p "${OUTPUT_BASE}" "${OUTPUT_BASE}/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${OUTPUT_BASE}/logs/slurm.log"
}

# Clone/install AFSample2 if needed
if [[ ! -d "./afsample2" ]]; then
    log "Cloning AFSample2..."
    git clone "${AFSAMPLE2_REPO}"
fi

cd afsample2

# Create conda environment if needed
if [[ ! -d "./afsample2_env" ]]; then
    log "Creating conda environment..."
    conda env create -f environment.yml
fi

# Activate environment
source activate afsample2_env

log "Starting AFSample2 batch processing on $(hostname)"
log "SLURM_JOB_ID: ${SLURM_JOB_ID}"
log "GPU: ${CUDA_VISIBLE_DEVICES}"

# Process each target
for target in "${TARGETS[@]}"; do
    log "=========================================="
    log "Processing ${target}"
    log "=========================================="
    
    fasta_file="./fasta/${target}.fasta"
    output_dir="${OUTPUT_BASE}/${target}"
    
    mkdir -p "${output_dir}"
    
    # Run AFSample2
    python run_afsample2.py \
        --fasta "${fasta_file}" \
        --num_samples "${NUM_SAMPLES}" \
        --output_dir "${output_dir}" \
        --gpu \
        2>&1 | tee "${OUTPUT_BASE}/logs/${target}.log"
    
    if [[ $? -eq 0 ]]; then
        log "Completed ${target}"
    else
        log "Failed ${target}"
    fi
done

# Run analysis
log "Running ensemble analysis..."

cd "${SLURM_SUBMIT_DIR}"

python3 << 'PYEOF'
import sys
sys.path.insert(0, './runpod_setup')
from batch_analyze import analyze_target, generate_combined_report
import os

OUTPUT_BASE = os.environ.get('OUTPUT_BASE', './output')
targets = ["KDM4A", "SLC7A11", "DGAT1", "GPX4", "YARS2"]
results = []

for target in targets:
    target_dir = f"{OUTPUT_BASE}/{target}"
    target_output = f"{OUTPUT_BASE}/reports/{target}"
    
    if os.path.exists(target_dir):
        result = analyze_target(target, target_dir, target_output)
        results.append(result)

if results:
    generate_combined_report(results, f"{OUTPUT_BASE}/reports")
PYEOF

log "Batch processing complete!"
log "Output saved to: ${OUTPUT_BASE}"