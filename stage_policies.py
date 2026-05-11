"""
ARP Pipeline Stage Failure Policies
====================================

Defines retry, timeout, fallback for each pipeline stage.
"""

STAGE_POLICIES = {
    "literature_search": {
        "retry": 3,
        "timeout_seconds": 120,
        "fallback": "cache_or_placeholder",
        "skip_on_failure": False,
        "partial_result": True,
        "alert_on_failure": True,
        "description": "PubMed literature search and PMCID retrieval"
    },
    
    "target_validation": {
        "retry": 2,
        "timeout_seconds": 300,
        "fallback": "heuristic_mode",
        "skip_on_failure": False,
        "partial_result": True,
        "alert_on_failure": True,
        "description": "Validate targets via UniProt, structural analysis"
    },
    
    "molecular_design": {
        "retry": 1,
        "timeout_seconds": 600,
        "fallback": "template_based",
        "skip_on_failure": True,
        "partial_result": True,
        "alert_on_failure": True,
        "description": "Boltz-2 structure prediction, compound design"
    },
    
    "admet_prediction": {
        "retry": 2,
        "timeout_seconds": 180,
        "fallback": "historical_data",
        "skip_on_failure": True,
        "partial_result": True,
        "alert_on_failure": False,
        "description": "ADMET prediction via ML models"
    },
    
    "biomarker_analysis": {
        "retry": 2,
        "timeout_seconds": 240,
        "fallback": "signature_based",
        "skip_on_failure": True,
        "partial_result": True,
        "alert_on_failure": False,
        "description": "ML biomarker scoring (FRS, NRF2, TMS, CBMS)"
    },
    
    "screening": {
        "retry": 1,
        "timeout_seconds": 300,
        "fallback": "rule_based",
        "skip_on_failure": True,
        "partial_result": True,
        "alert_on_failure": True,
        "description": "Virtual screening, hit calling"
    },
    
    "synthetic_lethal": {
        "retry": 2,
        "timeout_seconds": 180,
        "fallback": "literature_based",
        "skip_on_failure": True,
        "partial_result": True,
        "alert_on_failure": False,
        "description": "SL pair identification via co-essentiality"
    },
    
    "report_generation": {
        "retry": 0,
        "timeout_seconds": 60,
        "fallback": "basic_template",
        "skip_on_failure": False,
        "partial_result": True,
        "alert_on_failure": False,
        "description": "Markdown report generation"
    }
}


def get_policy(stage: str) -> dict:
    """Get policy for a stage"""
    return STAGE_POLICIES.get(stage, {
        "retry": 1,
        "timeout_seconds": 120,
        "fallback": "skip",
        "skip_on_failure": True,
        "partial_result": False,
        "alert_on_failure": True,
        "description": f"Unknown stage: {stage}"
    })


def format_policy_table() -> str:
    """Format policies as markdown table"""
    lines = ["## Stage Failure Policies", ""]
    lines.append("| Stage | Retry | Timeout | Fallback | Skip on Fail | Alert |")
    lines.append("|-------|-------|---------|----------|--------------|-------|")
    for stage, policy in STAGE_POLICIES.items():
        lines.append(f"| {stage} | {policy['retry']} | {policy['timeout_seconds']}s | {policy['fallback']} | {policy['skip_on_failure']} | {policy['alert_on_failure']} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_policy_table())