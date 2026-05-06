#!/bin/bash
#==============================================================================
# AFSample2 Batch Execution Script for ARP Target Proteins
# Targets: KDM4A, SLC7A11, DGAT1, GPX4, YARS2
#
# Usage:
#   ./run_afsample2_batch.sh           # Run all targets
#   ./run_afsample2_batch.sh KDM4A    # Run single target
#   ./run_afsample2_batch.sh --dry-run # Show commands without executing
#==============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_BASE="${OUTPUT_BASE:-./output}"
FASTA_DIR="${SCRIPT_DIR}/fasta"
LOG_DIR="${SCRIPT_DIR}/logs"
NUM_SAMPLES="${NUM_SAMPLES:-20}"
AFSAMPLE2_REPO="${AFSAMPLE2_REPO:-https://github.com/mevalon/afsample2.git}"
AFSAMPLE2_BRANCH="${AFSAMPLE2_BRANCH:-main}"

# Target proteins with UniProt IDs
declare -A TARGETS=(
    ["KDM4A"]="O75164"
    ["SLC7A11"]="Q9UPY5"
    ["DGAT1"]="O75907"
    ["GPX4"]="P36969"
    ["YARS2"]="Q9Y2Z4"
)

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_DIR}/batch.log"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "${LOG_DIR}/batch.log" >&2
}

create_fasta_files() {
    log "Creating FASTA files..."
    
    mkdir -p "${FASTA_DIR}"
    
    # KDM4A (359 aa) - Lysine-specific demethylase 4A
    cat > "${FASTA_DIR}/KDM4A.fasta" << 'FASTA_EOF'
>sp|O75164|KDM4A_HUMAN Lysine-specific demethylase 4A OS=Homo sapiens OX=9606 GN=KDM4A PE=1 SV=2
MASESETLNPSARIMTFYPTMEEFRNFSRYIAYIESQGAHRAGLAKVVPPKEWKPRASYD
DIDDLVIPAPIQQLVTGQSGLFTQYNIQKKAMTVREFRKIANSDKYCTPRYSEFEELERK
YWKNLTFNPPIYGADVNGTLYEKHVDEWNIGRLRTILDLVEKESGITIEGVNTPYLYFGM
WKTSFAWHTEDMDLYSINYLHFGEPKSWYSVPPEHGKRLERLAKGFFPGSAQSCEAFLRH
KMTLISPLMLKKYGIPFDKVTQEAGEFMITFPYGYHAGFNHGFNCAESTNFATRRWIEYG
KQAVLCSCRKDMVKISMDVFVRKFQPERYKLWKAGKDNTVIDHTLPTPEAAEFLKESELP
PRAGNEEECPEEDMEGVEDGEEGDLKTSLAKHRIGTKRHRVCLEIPQEVSQSELFPKEDL
SSEQYEMTECPAALAPVRPTHSSVRQVEDGLTFPDYSDSTEVKFEELKNVKLEEEDEEEE
QAAAALDLSVNPASVGGRLVFSGSKKKSSSSLGSGSSRDSISSDSETSEPLSCRAQGQTG
VLTVHSYAKGDGRVTVGEPCTRKKGSAARSFSERELAEVADEYMFSLEENKKSKGRRQPL
SKLPRHHPLVLQECVSDDETSEQLTPEEEAEETEAWAKPLSQLWQNRPPNFEAEKEFNET
MAQQAPHCAVCMIFQTYHQVEFGGFNQNCGNASDLAPQKQRTKPLIPEMCFTSTGCSTDI
NLSTPYLEEDGTSILVSCKKCSVRVHASCYGVPPAKASEDWMCSRCSANALEEDCCLCSL
RGGALQRANDDRWVHVSCAVAILEARFVNIAERSPVDVSKIPLPRFKLKCIFCKKRRKRT
AGCCVQCSHGRCPTAFHVSCAQAAGVMMQPDDWPFVVFITCFRHKIPNLERAKGALQSIT
AGQKVISKHKNGRFYQCEVVRLTTETFYEVNFDDGSFSDNLYPEDIVSQDCLQFGPPAEG
EVVQVRWTDGQVYGAKFVASHPIQMYQVEFEDGSQLVVKRDDVYTLDEELPKRVKSRLSV
ASDMRFNEIFTEKEVKQEKKRQRVINSRYREDYIEPALYRAIME
FASTA_EOF

    # SLC7A11 (501 aa) - Cystine/glutamate transporter (xCT)
    cat > "${FASTA_DIR}/SLC7A11.fasta" << 'FASTA_EOF'
>sp|Q9UPY5|XCT_HUMAN Cystine/glutamate transporter OS=Homo sapiens OX=9606 GN=SLC7A11 PE=1 SV=1
MVRKPVVSTISKGGYLQGNVNGRLPSLGNKEPPGQEKVQLKRKVTLLRGVSIIIGTIIGA
GIFISPKGVLQNTGSVGMSLTIWTVCGVLSLFGALSYAELGTTIKKSGGHYTYILEVFGP
LPAFVRVWVELLIIRPAATAVISLAFGRYILEPFFIQCEIPELAIKLITAVGITVVMVLN
SMSVSWSARIQIFLTFCKLTAILIIIVPGVMQLIKGQTQNFKDAFSGRDSSITRLPLAFY
YGMYAYAGWFYLNFVTEEVENPEKTIPLAICISMAIVTIGYVLTNVAYFTTINAEELLLS
NAVAVTFSERLLGNFSLAVPIFVALSCFGSMNGGVFAVSRLFYVASREGHLPEILSMIHV
RKHTPLPAVIVLHPLTMIMLFSGDLDSLLNFLSFARWLFIGLAVAGLIYLRYKCPDMHRP
FKVPLFIPALFSFTCLFMVALSLYSDPFSTGIGFVITLTGVPAYYLFIIWDKKPRWFRIM
SEKITRTLQIILEVVPEEDKL
FASTA_EOF

    # DGAT1 (488 aa) - Diacylglycerol O-acyltransferase 1
    cat > "${FASTA_DIR}/DGAT1.fasta" << 'FASTA_EOF'
>sp|O75907|DGAT1_HUMAN Diacylglycerol O-acyltransferase 1 OS=Homo sapiens OX=9606 GN=DGAT1 PE=1 SV=2
MGDRGSSRRRRTGSRPSSHGGGGPAAAEEEVRDAAAGPDVGAAGDAPAPAPNKDGDAGVG
SGHWELRCHRLQDSLFSSDSGFSNYRGILNWCVVMLILSNARLFLENLIKYGILVDPIQV
VSLFLKDPYSWPAPCLVIAANVFAVAAFQVEKRLAVGALTEQAGLLLHVANLATILCFPA
AVVLLVESITPVGSLLALMAHTILFLKLFSYRDVNSWCRRARAKAASAGKKASSAAAPHT
VSYPDNLTYRDLYYFLFAPTLCYELNFPRSPRIRKRFLLRRILEMLFFTQLQVGLIQQWM
VPTIQNSMKPFKDMDYSRIIERLLKLAVPNHLIWLIFFYWLFHSCLNAVAELMQFGDREF
YRDWWNSESVTYFWQNWNIPVHKWCIRHFYKPMLRRGSSKWMARTGVFLASAFFHEYLVS
VPLRMFRLWAFTGMMAQIPLAWFVGRFFQGNYGNAAVWLSLIIGQPIAVLMYVHDYYVLN
YEAPAAEA
FASTA_EOF

    # GPX4 (197 aa) - Phospholipid hydroperoxide glutathione peroxidase
    cat > "${FASTA_DIR}/GPX4.fasta" << 'FASTA_EOF'
>sp|P36969|GPX4_HUMAN Phospholipid hydroperoxide glutathione peroxidase GPX4 OS=Homo sapiens OX=9606 GN=GPX4 PE=1 SV=3
MSLGRLCRLLKPALLCGALAAPGLAGTMCASRDDWRCARSMHEFSAKDIDGHMVNLDKYR
GFVCIVTNVASQUGKTEVNYTQLVDLHARYAECGLRILAFPCNQFGKQEPGSNEEIKEFA
AGYNVKFDMFSKICVNGDDAHPLWKWMKIQPKGKGILGNAIKWNFTKFLIDKNGCVVKRY
GPMEEPLVIEKDLPHYF
FASTA_EOF

    # YARS2 (471 aa) - Tyrosine--tRNA ligase, mitochondrial
    cat > "${FASTA_DIR}/YARS2.fasta" << 'FASTA_EOF'
>sp|Q9Y2Z4|SYYM_HUMAN Tyrosine--tRNA ligase, mitochondrial OS=Homo sapiens OX=9606 GN=YARS2 PE=1 SV=2
MAAPILRSFSWGRWSGTLNLSVLLPLGLRKAHSGAQGLLAAQKARGLFKDFFPETGTKIE
LPELFDRGTASFPQTIYCGFDPTADSLHVGHLLALLGLFHLQRAGHNVIALVGGATARLG
DPSGRTKEREALETERVRANARALRLGLEALAANHQQLFTDGRSWGSFTVLDNSAWYQKQ
HLVDFLAAVGGHFRMGTLLSRQSVQLRLKSPEGMSLAEFFYQVLQAYDFYYLFQRYGCRV
QLGGSDQLGNIMSGYEFINKLTGEDVFGITVPLITSTTGAKLGKSAGNAVWLNRDKTSPF
ELYQFFVRQPDDSVERYLKLFTFLPLPEIDHIMQLHVKEPERRGPQKRLAAEVTKLVHGR
EGLDSAKRCTQALYHSSIDALEVMSDQELKELFKEAPFSEFFLDPGTSVLDTCRKANAIP
DGPRGYRMITEGGVSINHQQVTNPESVLIVGQHILKNGLSLLKIGKRNFYIIKWLQL
FASTA_EOF

    log "FASTA files created in ${FASTA_DIR}"
}

run_single_target() {
    local target=$1
    local uniprot=$2
    local fasta_file="${FASTA_DIR}/${target}.fasta"
    local output_dir="${OUTPUT_BASE}/${target}"
    local log_file="${LOG_DIR}/${target}.log"
    
    log "=========================================="
    log "Processing ${target} (UniProt: ${uniprot})"
    log "FASTA: ${fasta_file}"
    log "Output: ${output_dir}"
    log "=========================================="
    
    # Check FASTA file exists
    if [[ ! -f "${fasta_file}" ]]; then
        error "FASTA file not found: ${fasta_file}"
        return 1
    fi
    
    # Create output directory
    mkdir -p "${output_dir}"
    
    # Check if AFSample2 is installed
    if ! command -v run_afsample2.py &> /dev/null; then
        log "AFSample2 not found in PATH. Checking for local installation..."
        
        if [[ ! -d "${SCRIPT_DIR}/afsample2" ]]; then
            log "Cloning AFSample2 repository..."
            git clone --branch "${AFSAMPLE2_BRANCH}" "${AFSAMPLE2_REPO}" "${SCRIPT_DIR}/afsample2"
        fi
        
        export PATH="${SCRIPT_DIR}/afsample2:$PATH"
    fi
    
    # Run AFSample2
    local start_time=$(date +%s)
    
    log "Starting AFSample2 run (${NUM_SAMPLES} samples)..."
    
    # Check if Python script or Docker
    if command -v run_afsample2.py &> /dev/null; then
        # Python execution
        python3 run_afsample2.py \
            --fasta "${fasta_file}" \
            --num_samples "${NUM_SAMPLES}" \
            --output_dir "${output_dir}" \
            2>&1 | tee "${log_file}"
    elif command -v docker &> /dev/null && docker images | grep -q alphafold; then
        # Docker execution
        docker run --gpus all \
            -v "${OUTPUT_BASE}:/output" \
            alphafold/afsample2:latest \
            python run_afsample2.py \
            --fasta "/output/${target}.fasta" \
            --num_samples "${NUM_SAMPLES}" \
            --output_dir "/output/${target}" \
            2>&1 | tee "${log_file}"
    else
        log "AFSample2 not available. Skipping structure generation."
        log "Prepare for remote execution: rsync -avz ./fasta user@remote:/path/to/afsample2/"
        return 0
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log "Completed ${target} in $((duration / 60))m ${duration}s"
    
    # Count generated PDB files
    if [[ -d "${output_dir}" ]]; then
        local pdb_count=$(find "${output_dir}" -name "*.pdb" 2>/dev/null | wc -l)
        log "Generated ${pdb_count} PDB structures"
    fi
    
    return 0
}

run_analysis() {
    local target=$1
    local output_dir="${OUTPUT_BASE}/${target}"
    local report_dir="${OUTPUT_BASE}/reports/${target}"
    
    if [[ ! -d "${output_dir}" ]] || [[ -z "$(ls -A ${output_dir}/*.pdb 2>/dev/null)" ]]; then
        log "No PDB files found for ${target}. Skipping analysis."
        return 1
    fi
    
    log "Running ensemble analysis for ${target}..."
    
    mkdir -p "${report_dir}"
    
    python3 "${SCRIPT_DIR}/analyze_ensemble.py" \
        --input_dir "${output_dir}" \
        --output "${report_dir}" \
        --num_clusters 3 \
        --flexibility_threshold 2.0 \
        2>&1 | tee "${LOG_DIR}/${target}_analysis.log"
    
    return $?
}

setup_environment() {
    mkdir -p "${OUTPUT_BASE}" "${LOG_DIR}" "${FASTA_DIR}"
    log "Environment setup complete"
    log "Output base: ${OUTPUT_BASE}"
    log "Log directory: ${LOG_DIR}"
}

print_summary() {
    log ""
    log "=========================================="
    log "BATCH EXECUTION SUMMARY"
    log "=========================================="
    log "Targets processed: ${#TARGETS[@]}"
    log "Samples per target: ${NUM_SAMPLES}"
    log "Output directory: ${OUTPUT_BASE}"
    log ""
    log "Results:"
    
    for target in "${!TARGETS[@]}"; do
        local output_dir="${OUTPUT_BASE}/${target}"
        if [[ -d "${output_dir}" ]]; then
            local pdb_count=$(find "${output_dir}" -name "*.pdb" 2>/dev/null | wc -l)
            local size=$(du -sh "${output_dir}" 2>/dev/null | cut -f1)
            log "  ${target}: ${pdb_count} structures (${size})"
        else
            log "  ${target}: NOT GENERATED"
        fi
    done
    
    log ""
    log "Next steps:"
    log "  1. Copy results: rsync -avz user@remote:${OUTPUT_BASE} ./"
    log "  2. Run combined analysis: python analyze_ensemble.py --targets KDM4A SLC7A11 DGAT1 GPX4 YARS2"
    log "=========================================="
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    # Parse arguments
    local targets_to_run=()
    local dry_run=false
    
    if [[ $# -eq 0 ]]; then
        targets_to_run=("${!TARGETS[@]}")
    else
        for arg in "$@"; do
            case "$arg" in
                --dry-run)
                    dry_run=true
                    ;;
                --help|-h)
                    echo "Usage: $0 [target1 target2 ...] [--dry-run]"
                    echo "Targets: ${!TARGETS[@]}"
                    exit 0
                    ;;
                *)
                    if [[ -n "${TARGETS[$arg]}" ]]; then
                        targets_to_run+=("$arg")
                    else
                        error "Unknown target: $arg"
                        exit 1
                    fi
                    ;;
            esac
        done
    fi
    
    if $dry_run; then
        log "DRY RUN MODE - Commands that would be executed:"
        for target in "${targets_to_run[@]}"; do
            log "  ./run_afsample2_batch.sh $target"
        done
        exit 0
    fi
    
    setup_environment
    create_fasta_files
    
    log ""
    log "Starting AFSample2 batch processing..."
    log "Targets: ${targets_to_run[*]}"
    log ""
    
    local failed=()
    
    # Run for each target
    for target in "${targets_to_run[@]}"; do
        local uniprot="${TARGETS[$target]}"
        
        if ! run_single_target "$target" "$uniprot"; then
            failed+=("$target")
        fi
        
        # Run analysis after each target
        run_analysis "$target" || log "Analysis for $target failed or skipped"
        
        log ""
    done
    
    # Print summary
    print_summary
    
    # Exit with error if any targets failed
    if [[ ${#failed[@]} -gt 0 ]]; then
        error "Failed targets: ${failed[*]}"
        return 1
    fi
    
    return 0
}

main "$@"