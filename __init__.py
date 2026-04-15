"""
ARP v24 - Working Drug Discovery Pipeline

A truly functional drug discovery pipeline built on proven v22 engines
with bug fixes, real API integration, and end-to-end execution.

Engines:
  1. Disease -> Target (scoring + prioritization)
  2. Target -> Modality (routing + assay recommendation)
  3. Modality -> Candidate (compound lookup + live ChEMBL enrichment)

API Integrations:
  - PubMed (NCBI E-utilities)
  - ClinicalTrials.gov (API v2)
  - ChEMBL (REST API v34)

Usage:
    from pipeline import run_pipeline
    result = run_pipeline("masld", top_n=5)
"""

__version__ = "24.0.0"
__author__ = "Brown Biotech"
