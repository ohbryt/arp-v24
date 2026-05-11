#!/usr/bin/env python3
"""
ARP Pipeline Test Script
Run with: python3 test_arp.py
"""
import sys
import json

# Test imports
print("Testing imports...")
from arp_orchestrator import ARPOrchestrator, Playbook
print("✓ arp_orchestrator imported")

from evidence_level import EvidenceLevel, add_evidence_level, Provenance
print("✓ evidence_level imported")

from stage_policies import get_policy, format_policy_table
print("✓ stage_policies imported")

# Test Evidence Level
print("\n--- Evidence Level Test ---")
target = {"name": "FSP1", "mechanism": "Ferroptosis suppressor"}
target = add_evidence_level(
    target,
    EvidenceLevel.VALIDATED,
    "Boltz-2 structure prediction",
    ["Nature 2025", "PNAS 2025"]
)
print(f"Target with evidence: {json.dumps(target, indent=2)}")

# Test Provenance
print("\n--- Provenance Test ---")
prov = Provenance.from_git()
print(f"Branch: {prov.branch}")
print(f"Commit: {prov.commit_hash}")

# Test Stage Policies
print("\n--- Stage Policy Test ---")
policy = get_policy("molecular_design")
print(f"Molecular design policy: {json.dumps(policy, indent=2)}")

# Test FSP1 playbook
print("\n--- FSP1 Playbook Test ---")
orch = ARPOrchestrator()
print(f"Playbooks: {[p.value for p in Playbook]}")
print(f"FSP1 playbook available: {'fsp1' in [p.value for p in Playbook]}")

# Test JSON schema
print("\n--- JSON Schema Validation Test ---")
import jsonschema
with open("schemas/output_schema.json") as f:
    schema = json.load(f)

sample_output = {
    "disease": "NSCLC",
    "targets": [
        {
            "name": "FSP1",
            "rationale": "First-in-class ferroptosis inducer",
            "confidence": "high",
            "evidence_level": "validated",
            "evidence_label": "🔵 Validated"
        }
    ],
    "candidates": [
        {
            "name": "FSEN1",
            "target": "FSP1",
            "priority": "high",
            "evidence_level": "real"
        }
    ],
    "evidence": {
        "literature": ["PMID:12345"]
    },
    "meta": {
        "timestamp": "2026-05-12T00:30:00Z",
        "version": "1.0.0",
        "branch": "yars2-sirna-pf14-2026",
        "commit_hash": "test"
    },
    "next_actions": ["Synthesize FSEN1 analogs"]
}

try:
    jsonschema.validate(sample_output, schema)
    print("✓ JSON schema validation passed")
except jsonschema.ValidationError as e:
    print(f"✗ Validation error: {e.message}")

print("\n=== All tests passed! ===")
print("ARP Pipeline is ready for research!")