# AFSample2 실행 프롬프트 (1번 - 컴퓨터에서 직접 실행)

## 사전 준비

### 1. Docker 설치 확인
터미널에서 다음 명령어 실행:
```bash
docker --version
```
**결과:** Docker version 20.x.x 이상이면 OK

Docker 없으면 설치: https://www.docker.com/products/docker-desktop/

---

### 2. 작업 폴더 생성
```bash
mkdir -p ~/AFSample2_workspace
cd ~/AFSample2_workspace

# 구조 생성
mkdir -p inputs outputs databases
```

---

### 3. 타겟 FASTA 파일 다운로드
```bash
cd ~/AFSample2_workspace/inputs

# KDM4A (359 aa)
curl -s https://rest.uniprot.org/uniprotkb/O75164.fasta > KDM4A.fasta

# SLC7A11 (501 aa)  
curl -s https://rest.uniprot.org/uniprotkb/Q9UPY5.fasta > SLC7A11.fasta

# DGAT1 (488 aa)
curl -s https://rest.uniprot.org/uniprotkb/O75907.fasta > DGAT1.fasta

# GPX4 (197 aa)
cat > GPX4.fasta << 'EOF'
>sp|P36904|GPX4_HUMAN Phospholipid hydroperoxide glutathione peroxidase OS=Homo sapiens OX=9606 GN=GPX4 PE=1 SV=3
MARTLAAVFLLVVVSLGSAQGQNKQGRWSTCKKNGKPVVNMYQQLNRKEDKNNCDLQEK
MSQCRKLRPSGRDWVCPTGRGVLVKFLVPVPGYQSSVKQRMKLYLKYIPCGFCFTPSDE
IKQMRPSLRQLVYGAIQLPLLKAHQIGPFAFRKALEVKQKGGQEPNKTEAAGCLGAEVDQ
DGVDVLSVNAGKRGNGQKGNSQTPKCCPFCTPPGKRLLQVGNAVPRRPGQGGNAGKS
EOF

# YARS2 (471 aa)
curl -s https://rest.uniprot.org/uniprotkb/Q9Y2Z4.fasta > YARS2.fasta

# 확인
ls -la *.fasta
```

**예상 결과:**
```
KDM4A.fasta
SLC7A11.fasta
DGAT1.fasta
GPX4.fasta
YARS2.fasta
```

---

## Docker 실행

### 4. AFSample2 Docker 이미지 다운로드
```bash
cd ~/AFSample2_workspace

docker pull kyogesh/afsample2:v1.1
```
⚠️ **다운로드 크기: 약 20-30GB** ( alphafold 데이터베이스 포함)

인터넷 연결에 따라 30분~2시간 소요

---

### 5. AFSample2 실행 (KDM4A 단독 테스트)

```bash
cd ~/AFSample2_workspace

docker run --gpus 1 \
  --rm \
  -v $(pwd)/inputs:/inputs \
  -v $(pwd)/outputs:/outputs \
  kyogesh/afsample2:v1.1 \
  --method afsample2 \
  --fasta_paths /inputs/KDM4A.fasta \
  --nstruct 5 \
  --msa_rand_fraction 0.20 \
  --model_preset=monomer \
  --output_dir /outputs/
```

**설명:**
- `--gpus 1`: GPU 1개 사용 (GPU 없으면 `--gpus 0` 또는 제거)
- `--nstruct 5`: 5개 구조 예측 (1개당 약 10-30분)
- `--msa_rand_fraction 0.20`: MSA의 20% 무작위화 → conformational diversity

---

### 6. 결과 확인
```bash
cd ~/AFSample2_workspace

# 출력 디렉토리 확인
ls -la outputs/

# KDM4A 결과
ls -la outputs/KDM4A/

# 구조 파일 (PDB)
ls outputs/KDM4A/*.pdb 2>/dev/null | head -5
```

**예상 결과:**
```
KDM4A/
├── KDM4A_unrelaxed_rank_1.pdb
├── KDM4A_unrelaxed_rank_2.pdb
├── KDM4A_unrelaxed_rank_3.pdb
├── KDM4A_unrelaxed_rank_4.pdb
└── KDM4A_unrelaxed_rank_5.pdb
```

---

## 전체 타겟 실행 (선택)

### 7. 모든 타겟 동시 예측
```bash
cd ~/AFSample2_workspace

docker run --gpus 1 \
  --rm \
  -v $(pwd)/inputs:/inputs \
  -v $(pwd)/outputs:/outputs \
  kyogesh/afsample2:v1.1 \
  --method afsample2 \
  --fasta_paths /inputs/KDM4A.fasta \
  --fasta_paths /inputs/SLC7A11.fasta \
  --fasta_paths /inputs/DGAT1.fasta \
  --fasta_paths /inputs/GPX4.fasta \
  --fasta_paths /inputs/YARS2.fasta \
  --nstruct 10 \
  --msa_rand_fraction 0.20 \
  --model_preset=monomer \
  --output_dir /outputs/
```

⏱️ **예상 시간:**
- GPU 있음: 약 2-4시간
- GPU 없음: 12-24시간 이상

---

## 문제 해결

### GPU 인식 안 될 때
```bash
# NVIDIA GPU 확인
nvidia-smi

# Docker GPU 지원 확인
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 메모리 부족 시
```bash
# nstruct 줄이기 (5 → 3)
--nstruct 3
```

### 실행 로그 보기
```bash
docker logs -f <container_id>
```

---

## 다음 단계 (2번 프롬프트용)

결과 PDB 파일들로:
1. PyMOL에서 구조 시각화
2. conformational diversity 분석 (RMSD 계산)
3. drug binding site flexibility 확인
