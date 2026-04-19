"""
Activity Cliff Detector - ARP v24
===================================
Detects activity cliffs: small structural changes → large activity changes.
SAR (Structure-Activity Relationship) analysis.
Pharmacophore change alerts.
Integration with pharmacophore module.

Based on Talanta 2026 (PMID 41996874) - "activity cliff insensitivity" limitation of QSAR.

Author: Demis (ARP v24)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from datetime import datetime
import hashlib


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class CliffSeverity(Enum):
    """Severity of activity cliff"""
    EXTREME = "extreme"   # >100x activity difference
    MAJOR = "major"       # 10-100x activity difference
    MODERATE = "moderate" # 3-10x activity difference
    MILD = "mild"         # 2-3x activity difference
    NONE = "none"         # <2x - not a cliff


class PharmacophoreChange(Enum):
    """Type of pharmacophore change"""
    NEW_H_BOND_DONOR = "new_hbd"
    LOST_H_BOND_DONOR = "lost_hbd"
    NEW_H_BOND_ACCEPTOR = "new_hba"
    LOST_H_BOND_ACCEPTOR = "lost_hba"
    NEW_AROMATIC = "new_aromatic"
    LOST_AROMATIC = "lost_aromatic"
    NEW_HYDROPHOBIC = "new_hydrophobic"
    LOST_HYDROPHOBIC = "lost_hydrophobic"
    NEW_CHARGE = "new_charge"
    LOST_CHARGE = "lost_charge"
    NEW_HETEROATOM = "new_heteroatom"
    LOST_HETEROATOM = "lost_heteroatom"
    RING_CHANGE = "ring_change"
    STEREO_CHANGE = "stereo_change"
    NONE = "none"


@dataclass
class MolecularFragment:
    """Represents a molecular fragment or substructure"""
    fragment_id: str
    smarts_pattern: str
    description: str
    pharmacophore_type: str  # "hbd", "hba", "hydrophobic", "aromatic", "acidic", "basic"
    occurrence_count: int = 1


@dataclass
class CompoundRecord:
    """A compound with activity and structural data"""
    compound_id: str
    smiles: str
    activity_value: float           # IC50, Ki, EC50, etc.
    activity_unit: str = "nM"
    activity_type: str = "IC50"    # IC50, Ki, Kd, EC50, etc.
    activity_flag: str = "active"   # "active", "inactive", "partial"

    # Structural features
    mw: Optional[float] = None
    logp: Optional[float] = None
    tpsa: Optional[float] = None
    hbd: Optional[int] = None
    hba: Optional[int] = None
    rotatable_bonds: Optional[int] = None

    # Fragments
    fragments: List[str] = field(default_factory=list)  # Fragment IDs present
    pharmacophores: List[str] = field(default_factory=list)  # Pharmacophore types present

    # Source
    source_id: Optional[str] = None
    assay_name: Optional[str] = None
    notes: str = ""

    def pActivity(self) -> float:
        """Convert to pActivity (-log10(activity in M))"""
        if self.activity_value <= 0:
            return 0.0
        # Convert to M if in nM
        if self.activity_unit == "nM":
            activity_m = self.activity_value * 1e-9
        elif self.activity_unit == "uM":
            activity_m = self.activity_value * 1e-6
        else:
            activity_m = self.activity_value
        return -np.log10(activity_m)


@dataclass
class StructuralDifference:
    """Describes structural difference between two compounds"""
    change_type: PharmacophoreChange
    description: str
    fragment_added: Optional[str] = None
    fragment_removed: Optional[str] = None
    position: Optional[str] = None  # e.g., "position 3", "ring A"
    relevance_to_activity: str = "unknown"  # "likely_causal", "may_contribute", "unknown"


@dataclass
class ActivityCliffAlert:
    """
    Alert for a detected activity cliff.
    
    Attributes:
        detected: Whether an activity cliff was detected
        cliff_magnitude: Delta pActivity (e.g., 2.0 = 100x activity difference)
        structural_change: Human-readable description
        confidence: cliff confidence based on data quality
        cliff_id: Unique identifier
        compound_pair: The two compounds involved
        structural_differences: List of specific structural changes
    """
    detected: bool
    cliff_magnitude: float          # Delta pActivity
    severity: str                  # extreme, major, moderate, mild, none
    structural_change: str
    confidence: str               # high, medium, low
    cliff_id: Optional[str] = None

    # Involved compounds
    compound_a_id: Optional[str] = None
    compound_b_id: Optional[str] = None
    activity_a: Optional[float] = None
    activity_b: Optional[float] = None
    activity_ratio: Optional[float] = None  # x-fold difference

    # Pharmacophore changes
    pharmacophore_changes: List[StructuralDifference] = field(default_factory=list)
    pharmacophore_alert: bool = False
    pharmacophore_alert_message: Optional[str] = None

    # SAR notes
    sar_hypothesis: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.cliff_id is None and self.detected:
            self.cliff_id = hashlib.md5(
                f"{self.compound_a_id}_{self.compound_b_id}".encode()
            ).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cliff_id": self.cliff_id,
            "detected": self.detected,
            "cliff_magnitude": round(self.cliff_magnitude, 2),
            "severity": self.severity,
            "structural_change": self.structural_change,
            "confidence": self.confidence,
            "compound_pair": [self.compound_a_id, self.compound_b_id],
            "activity_ratio": round(self.activity_ratio, 1) if self.activity_ratio else None,
            "pharmacophore_alert": self.pharmacophore_alert,
            "sar_hypothesis": self.sar_hypothesis,
            "notes": self.notes,
            "timestamp": self.timestamp.isoformat(),
        }


# ============================================================================
# FRAGMENT & PHARMACOPHORE EXTRACTION
# ============================================================================

class FragmentLibrary:
    """
    Library of common molecular fragments for SAR analysis.
    Production: use RDKit's functional group patterns.
    """

    # Common pharmacophore fragments
    FRAGMENTS: Dict[str, MolecularFragment] = {
        "benzene": MolecularFragment("benzene", "c1ccccc1", "Benzene ring", "aromatic"),
        "phenyl": MolecularFragment("phenyl", "c1ccccc1", "Phenyl group", "aromatic"),
        "aniline": MolecularFragment("aniline", "Nc1ccccc1", "Aniline (primary aromatic amine)", "hbd"),
        "carboxylic_acid": MolecularFragment("carboxylic_acid", "C(=O)O", "Carboxylic acid", "acidic"),
        "sulfonamide": MolecularFragment("sulfonamide", "S(=O)(=O)N", "Sulfonamide", "hba"),
        "amide": MolecularFragment("amide", "C(=O)N", "Amide", "hba"),
        "ester": MolecularFragment("ester", "C(=O)O", "Ester", "hba"),
        "alcohol": MolecularFragment("alcohol", "CO", "Alcohol (primary/secondary)", "hbd"),
        "morpholine": MolecularFragment("morpholine", "C1COCCN1", "Morpholine", "hba"),
        "piperazine": MolecularFragment("piperazine", "C1CNCCN1", "Piperazine", "hba"),
        "pyridine": MolecularFragment("pyridine", "c1ccncc1", "Pyridine (aromatic N)", "hba"),
        "pyrrole": MolecularFragment("pyrrole", "c1cc[nH]c1", "Pyrrole (aromatic N-H)", "hbd"),
        "imidazole": MolecularFragment("imidazole", "c1cnc[nH]1", "Imidazole", "hbd"),
        "triazole": MolecularFragment("triazole", "c1nnnn1", "Triazole", "hba"),
        "alkyl_ether": MolecularFragment("alkyl_ether", "CO", "Alkyl ether", "hba"),
        "alkyl_amine": MolecularFragment("alkyl_amine", "CN", "Alkyl amine", "hba"),
        "aryl_fluoride": MolecularFragment("aryl_f", "Fc", "Aryl fluoride", "hydrophobic"),
        "aryl_chloride": MolecularFragment("aryl_cl", "Clc", "Aryl chloride", "hydrophobic"),
        "aryl_bromide": MolecularFragment("aryl_br", "Brc", "Aryl bromide", "hydrophobic"),
        "cf3": MolecularFragment("cf3", "FC(F)F", "Trifluoromethyl", "hydrophobic"),
        "cyclopentyl": MolecularFragment("cyclopentyl", "C1CCCC1", "Cyclopentyl", "hydrophobic"),
        "cyclohexyl": MolecularFragment("cyclohexyl", "C1CCCCC1", "Cyclohexyl", "hydrophobic"),
        "tert_butyl": MolecularFragment("tert_butyl", "C(C)(C)C", "tert-Butyl", "hydrophobic"),
        "acetyl": MolecularFragment("acetyl", "CC(=O)", "Acetyl group", "hba"),
    }

    @classmethod
    def get_fragment(cls, name: str) -> Optional[MolecularFragment]:
        return cls.FRAGMENTS.get(name)

    @classmethod
    def list_fragments(cls) -> List[str]:
        return list(cls.FRAGMENTS.keys())


class PharmacophoreAnalyzer:
    """
    Analyzes pharmacophore features for SAR context.
    Detects pharmacophore changes between compound pairs.
    """

    # Pharmacophore feature definitions
    FEATURE_PATTERNS: Dict[str, List[str]] = {
        "hbd": ["aniline", "alcohol", "pyrrole", "imidazole", "alkyl_amine"],
        "hba": ["amide", "ester", "morpholine", "piperazine", "pyridine", "triazole", "alkyl_ether", "sulfonamide", "carboxylic_acid"],
        "hydrophobic": ["aryl_fluoride", "aryl_chloride", "aryl_bromide", "cf3", "cyclopentyl", "cyclohexyl", "tert_butyl", "benzene"],
        "aromatic": ["benzene", "phenyl", "pyridine", "pyrrole", "imidazole"],
        "acidic": ["carboxylic_acid"],
        "basic": ["alkyl_amine", "morpholine", "piperazine", "pyridine"],
    }

    def extract_pharmacophores(self, fragments: List[str]) -> Set[str]:
        """Extract pharmacophore features from fragment list"""
        features: Set[str] = set()
        for frag in fragments:
            for feature, frags in self.FEATURE_PATTERNS.items():
                if frag in frags:
                    features.add(feature)
        return features

    def detect_pharmacophore_changes(
        self,
        fragments_a: List[str],
        fragments_b: List[str],
    ) -> List[StructuralDifference]:
        """Detect pharmacophore changes between two fragment lists"""
        set_a = set(fragments_a)
        set_b = set(fragments_b)

        changes: List[StructuralDifference] = []

        # New features in B
        for frag in set_b - set_a:
            f_obj = FragmentLibrary.get_fragment(frag)
            if f_obj:
                # Determine change type
                if f_obj.pharmacophore_type in ("hbd", "hba", "hydrophobic", "aromatic"):
                    change_type = self._feature_to_change(f"new_{f_obj.pharmacophore_type}")
                else:
                    change_type = PharmacophoreChange.NEW_HETEROATOM

                changes.append(StructuralDifference(
                    change_type=change_type,
                    description=f"New {f_obj.pharmacophore_type} group: {f_obj.description}",
                    fragment_added=frag,
                    relevance_to_activity="likely_causal",
                ))

        # Lost features from A
        for frag in set_a - set_b:
            f_obj = FragmentLibrary.get_fragment(frag)
            if f_obj:
                if f_obj.pharmacophore_type in ("hbd", "hba", "hydrophobic", "aromatic"):
                    change_type = self._feature_to_change(f"lost_{f_obj.pharmacophore_type}")
                else:
                    change_type = PharmacophoreChange.LOST_HETEROATOM

                changes.append(StructuralDifference(
                    change_type=change_type,
                    description=f"Lost {f_obj.pharmacophore_type} group: {f_obj.description}",
                    fragment_removed=frag,
                    relevance_to_activity="likely_causal",
                ))

        return changes

    def _feature_to_change(self, feature: str) -> PharmacophoreChange:
        """Map feature string to PharmacophoreChange enum"""
        mapping = {
            "new_hbd": PharmacophoreChange.NEW_H_BOND_DONOR,
            "lost_hbd": PharmacophoreChange.LOST_H_BOND_DONOR,
            "new_hba": PharmacophoreChange.NEW_H_BOND_ACCEPTOR,
            "lost_hba": PharmacophoreChange.LOST_H_BOND_ACCEPTOR,
            "new_hydrophobic": PharmacophoreChange.NEW_HYDROPHOBIC,
            "lost_hydrophobic": PharmacophoreChange.LOST_HYDROPHOBIC,
            "new_aromatic": PharmacophoreChange.NEW_AROMATIC,
            "lost_aromatic": PharmacophoreChange.LOST_AROMATIC,
        }
        return mapping.get(feature, PharmacophoreChange.NONE)

    def assess_pharmacophore_alert(
        self,
        changes: List[StructuralDifference],
    ) -> Tuple[bool, Optional[str]]:
        """
        Assess whether pharmacophore changes are likely responsible for activity cliff.
        
        Returns:
            (is_alert, alert_message)
        """
        if not changes:
            return False, None

        # High-impact changes that often cause cliffs
        high_impact = {
            PharmacophoreChange.NEW_H_BOND_DONOR,
            PharmacophoreChange.LOST_H_BOND_DONOR,
            PharmacophoreChange.NEW_CHARGE,
            PharmacophoreChange.LOST_CHARGE,
            PharmacophoreChange.NEW_AROMATIC,
            PharmacophoreChange.LOST_AROMATIC,
        }

        high_impact_changes = [c for c in changes if c.change_type in high_impact]

        if len(high_impact_changes) >= 2:
            return True, (
                f"HIGH ALERT: Multiple high-impact pharmacophore changes detected. "
                f"{'; '.join(c.description for c in high_impact_changes[:3])}"
            )

        critical_changes = [c for c in changes if c.relevance_to_activity == "likely_causal"]
        if len(critical_changes) >= 1:
            return True, (
                f"Pharmacophore change likely responsible for activity cliff: "
                f"{critical_changes[0].description}"
            )

        return False, None


# ============================================================================
# ACTIVITY CLIFF DETECTOR
# ============================================================================

class ActivityCliffDetector:
    """
    Detects activity cliffs in SAR data.

    Activity Cliff: A pair of structurally similar compounds with significantly
    different biological activities. Classic QSAR challenge - smooth interpolation
    models fail at cliffs.

    Thresholds (configurable):
    - Structural similarity: Tanimoto >= 0.5 (similar scaffolds)
    - Activity ratio: >= 3-fold (delta pActivity >= 0.48)
    - Moderate cliff: >= 10-fold
    - Major cliff: >= 100-fold

    Based on Talanta 2026: "activity cliff insensitivity" is a key QSAR limitation.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.50,
        cliff_threshold_ratio: float = 3.0,  # 3-fold minimum for cliff
        major_cliff_ratio: float = 10.0,
        extreme_cliff_ratio: float = 100.0,
    ):
        self.similarity_threshold = similarity_threshold
        self.cliff_threshold_ratio = cliff_threshold_ratio
        self.major_cliff_ratio = major_cliff_ratio
        self.extreme_cliff_ratio = extreme_cliff_ratio
        self.fragment_analyzer = PharmacophoreAnalyzer()

    def compute_similarity(
        self,
        fragments_a: List[str],
        fragments_b: List[str],
    ) -> float:
        """
        Compute Tanimoto-like similarity based on fragments.
        Production: use RDKit fingerprints (Morgan, MACCS, etc.)
        """
        if not fragments_a and not fragments_b:
            return 0.0

        set_a = set(fragments_a)
        set_b = set(fragments_b)

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        if union == 0:
            return 0.0
        return intersection / union

    def detect_cliff(
        self,
        compound_a: CompoundRecord,
        compound_b: CompoundRecord,
    ) -> ActivityCliffAlert:
        """
        Detect activity cliff between two compounds.
        
        Returns:
            ActivityCliffAlert with detection results
        """
        # Compute structural similarity
        similarity = self.compute_similarity(
            compound_a.fragments,
            compound_b.fragments,
        )

        # Not structurally similar = not a cliff
        if similarity < self.similarity_threshold:
            return ActivityCliffAlert(
                detected=False,
                cliff_magnitude=0.0,
                severity=CliffSeverity.NONE.value,
                structural_change="Structurally dissimilar compounds",
                confidence="low",
                compound_a_id=compound_a.compound_id,
                compound_b_id=compound_b.compound_id,
                activity_a=compound_a.activity_value,
                activity_b=compound_b.activity_value,
                notes=[f"Similarity={similarity:.2f} < threshold={self.similarity_threshold}"],
            )

        # Compute activity ratio
        if compound_a.activity_value == 0 or compound_b.activity_value == 0:
            return ActivityCliffAlert(
                detected=False,
                cliff_magnitude=0.0,
                severity=CliffSeverity.NONE.value,
                structural_change="Cannot compute ratio (zero activity)",
                confidence="low",
                compound_a_id=compound_a.compound_id,
                compound_b_id=compound_b.compound_id,
            )

        ratio = max(compound_a.activity_value, compound_b.activity_value) / \
                min(compound_a.activity_value, compound_b.activity_value)

        # pActivity delta (more symmetric metric)
        pAct_a = compound_a.pActivity()
        pAct_b = compound_b.pActivity()
        delta_pAct = abs(pAct_a - pAct_b)

        # Determine severity
        if ratio >= self.extreme_cliff_ratio:
            severity = CliffSeverity.EXTREME
        elif ratio >= self.major_cliff_ratio:
            severity = CliffSeverity.MAJOR
        elif ratio >= self.cliff_threshold_ratio:
            severity = CliffSeverity.MODERATE
        elif ratio >= 2.0:
            severity = CliffSeverity.MILD
        else:
            severity = CliffSeverity.NONE

        detected = severity != CliffSeverity.NONE

        # Detect pharmacophore changes
        pharm_changes = self.fragment_analyzer.detect_pharmacophore_changes(
            compound_a.fragments,
            compound_b.fragments,
        )
        pharm_alert, pharm_msg = self.fragment_analyzer.assess_pharmacophore_alert(pharm_changes)

        # Build structural change description
        if compound_a.fragments and compound_b.fragments:
            added = set(compound_b.fragments) - set(compound_a.fragments)
            removed = set(compound_a.fragments) - set(compound_b.fragments)
            structural_desc = f"Similarity={similarity:.2f}. "
            if added:
                structural_desc += f"Added: {', '.join(added)}. "
            if removed:
                structural_desc += f"Removed: {', '.join(removed)}. "
        else:
            structural_desc = f"Similar compounds (similarity={similarity:.2f})"

        # Confidence assessment
        if compound_a.activity_flag == "active" and compound_b.activity_flag == "inactive":
            confidence = "high"
        elif detected and len(pharm_changes) > 0:
            confidence = "high"
        elif detected and similarity > 0.7:
            confidence = "medium"
        else:
            confidence = "low"

        # SAR hypothesis
        sar_hypothesis = None
        if detected:
            more_active = compound_a if pAct_a > pAct_b else compound_b
            less_active = compound_b if pAct_a > pAct_b else compound_a
            sar_hypothesis = (
                f"{more_active.compound_id} ({more_active.activity_type}={more_active.activity_value:.2f}{more_active.activity_unit}) "
                f"is {ratio:.1f}x more active than {less_active.compound_id}. "
                f"Hypothesis: {structural_desc[:100]}"
            )

        return ActivityCliffAlert(
            detected=detected,
            cliff_magnitude=round(delta_pAct, 2),
            severity=severity.value,
            structural_change=structural_desc,
            confidence=confidence,
            compound_a_id=compound_a.compound_id,
            compound_b_id=compound_b.compound_id,
            activity_a=compound_a.activity_value,
            activity_b=compound_b.activity_value,
            activity_ratio=round(ratio, 1),
            pharmacophore_changes=pharm_changes,
            pharmacophore_alert=pharm_alert,
            pharmacophore_alert_message=pharm_msg,
            sar_hypothesis=sar_hypothesis,
        )

    def scan_for_cliffs(
        self,
        compounds: List[CompoundRecord],
    ) -> List[ActivityCliffAlert]:
        """
        Scan a series of compounds for all pairwise activity cliffs.
        
        Args:
            compounds: List of CompoundRecords with activity data
        Returns:
            List of detected ActivityCliffAlerts (sorted by severity)
        """
        alerts: List[ActivityCliffAlert] = []
        n = len(compounds)

        for i in range(n):
            for j in range(i + 1, n):
                alert = self.detect_cliff(compounds[i], compounds[j])
                if alert.detected:
                    alerts.append(alert)

        # Sort by cliff magnitude descending
        alerts.sort(key=lambda a: a.cliff_magnitude, reverse=True)
        return alerts

    def get_cliff_summary(
        self,
        alerts: List[ActivityCliffAlert],
    ) -> Dict[str, Any]:
        """Generate summary statistics for cliff alerts"""
        if not alerts:
            return {
                "total_cliffs": 0,
                "by_severity": {},
                "pharmacophore_alerts": 0,
                "extreme_cliffs": [],
            }

        by_severity: Dict[str, int] = {}
        for a in alerts:
            by_severity[a.severity] = by_severity.get(a.severity, 0) + 1

        return {
            "total_cliffs": len(alerts),
            "by_severity": by_severity,
            "pharmacophore_alerts": sum(1 for a in alerts if a.pharmacophore_alert),
            "extreme_cliffs": [
                {
                    "id": a.cliff_id,
                    "magnitude": a.cliff_magnitude,
                    "ratio": a.activity_ratio,
                    "pair": [a.compound_a_id, a.compound_b_id],
                }
                for a in alerts if a.severity == CliffSeverity.EXTREME.value
            ][:5],  # Top 5 extreme
            "top_cliffs": [
                {
                    "id": a.cliff_id,
                    "magnitude": a.cliff_magnitude,
                    "ratio": a.activity_ratio,
                    "pair": [a.compound_a_id, a.compound_b_id],
                    "pharm_alert": a.pharmacophore_alert,
                }
                for a in alerts[:10]
            ],
        }


# ============================================================================
# SAR ANALYZER
# ============================================================================

class SARAnalyzer:
    """
    Structure-Activity Relationship analyzer.
    Identifies key structural features associated with activity.
    """

    def __init__(self):
        self.fragment_library = FragmentLibrary()

    def analyze(
        self,
        compounds: List[CompoundRecord],
    ) -> Dict[str, Any]:
        """
        Perform SAR analysis on a series of compounds.
        
        Returns:
            SAR analysis with feature importance and trends
        """
        if len(compounds) < 3:
            return {"status": "insufficient_data", "n_compounds": len(compounds)}

        # Separate active and inactive
        actives = [c for c in compounds if c.activity_flag == "active"]
        inactives = [c for c in compounds if c.activity_flag == "inactive"]

        if not actives or not inactives:
            return {"status": "no_activity_range", "n_actives": len(actives), "n_inactives": len(inactives)}

        # Fragment frequency analysis
        active_fragments: Dict[str, int] = {}
        inactive_fragments: Dict[str, int] = {}

        for c in actives:
            for f in c.fragments:
                active_fragments[f] = active_fragments.get(f, 0) + 1
        for c in inactives:
            for f in c.fragments:
                inactive_fragments[f] = inactive_fragments.get(f, 0) + 1

        # Compute fragment enrichment
        all_frags = set(active_fragments) | set(inactive_fragments)
        enrichment: Dict[str, Dict[str, Any]] = {}

        for frag in all_frags:
            a_freq = active_fragments.get(frag, 0) / len(actives) if actives else 0
            i_freq = inactive_fragments.get(frag, 0) / len(inactives) if inactives else 0

            if i_freq == 0 and a_freq > 0:
                ratio = float('inf')
            elif a_freq == 0:
                ratio = 0
            else:
                ratio = a_freq / (i_freq + 0.01)

            enrichment[frag] = {
                "active_frequency": round(a_freq, 3),
                "inactive_frequency": round(i_freq, 3),
                "enrichment_ratio": round(ratio, 2) if ratio != float('inf') else float('inf'),
                "association": "activity" if ratio > 2 else ("inactivity" if ratio < 0.5 else "neutral"),
            }

        # Sort by enrichment
        sorted_fragments = sorted(
            enrichment.items(),
            key=lambda x: x[1]["enrichment_ratio"] if x[1]["enrichment_ratio"] != float('inf') else 999,
            reverse=True,
        )

        # Key activity drivers
        activity_drivers = [
            {"fragment": f, **d}
            for f, d in sorted_fragments
            if d["association"] == "activity" and d["enrichment_ratio"] > 2
        ]

        # Key activity killers
        activity_killers = [
            {"fragment": f, **d}
            for f, d in sorted_fragments
            if d["association"] == "inactivity"
        ]

        return {
            "status": "complete",
            "n_compounds": len(compounds),
            "n_actives": len(actives),
            "n_inactives": len(inactives),
            "activity_drivers": activity_drivers[:10],
            "activity_killers": activity_killers[:10],
            "fragment_enrichment": dict(sorted_fragments[:20]),
            "total_fragments_analyzed": len(all_frags),
        }

    def summarize_sar(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable SAR summary"""
        if analysis.get("status") != "complete":
            return f"SAR Analysis: {analysis.get('status')}"

        lines = [
            f"SAR Analysis ({analysis['n_compounds']} compounds)",
            "=" * 50,
            f"Actives: {analysis['n_actives']}, Inactives: {analysis['n_inactives']}",
            "",
        ]

        if analysis.get("activity_drivers"):
            lines.append("🎯 Activity Drivers (enriched in active compounds):")
            for d in analysis["activity_drivers"][:5]:
                lines.append(
                    f"  • {d['fragment']}: "
                    f"freq={d['active_frequency']:.0%} active vs "
                    f"{d['inactive_frequency']:.0%} inactive "
                    f"(enrichment={d['enrichment_ratio']:.1f}x)"
                )

        if analysis.get("activity_killers"):
            lines.append("\n⚠️  Activity Killers (enriched in inactive compounds):")
            for k in analysis["activity_killers"][:5]:
                lines.append(
                    f"  • {k['fragment']}: "
                    f"freq={k['active_frequency']:.0%} active vs "
                    f"{k['inactive_frequency']:.0%} inactive"
                )

        return "\n".join(lines)


# ============================================================================
# TESTS
# ============================================================================

def test_compound_records():
    """Test compound record creation and pActivity"""
    compounds = [
        CompoundRecord("cpd_A", "CCO", 100, "nM", fragments=["alcohol", "ethyl"]),
        CompoundRecord("cpd_B", "CCCO", 1000, "nM", fragments=["alcohol", "propyl"]),
    ]
    assert compounds[0].pActivity() > compounds[1].pActivity()
    print(f"✓ Compound pActivity: A={compounds[0].pActivity():.2f}, B={compounds[1].pActivity():.2f}")


def test_pharmacophore_extraction():
    """Test pharmacophore feature extraction"""
    analyzer = PharmacophoreAnalyzer()
    features = analyzer.extract_pharmacophores(["aniline", "benzene", "amide"])
    print(f"✓ Pharmacophores: {features}")
    assert "hbd" in features
    assert "aromatic" in features
    assert "hba" in features


def test_pharmacophore_change_detection():
    """Test detection of pharmacophore changes"""
    analyzer = PharmacophoreAnalyzer()
    changes = analyzer.detect_pharmacophore_changes(
        ["aniline", "benzene"],
        ["amide", "benzene"],  # Lost aniline, gained amide
    )
    print(f"✓ Pharmacophore changes: {len(changes)}")
    for c in changes:
        print(f"    {c.change_type.value}: {c.description}")

    alert, msg = analyzer.assess_pharmacophore_alert(changes)
    print(f"    Alert: {alert}, Message: {msg}")


def test_activity_cliff_detection():
    """Test activity cliff detection"""
    detector = ActivityCliffDetector()

    # Major cliff: similar structures, very different activity
    cpd1 = CompoundRecord(
        "resmetirom", "CC(=O)Oc1ccccc1C(=O)Nc1ccc(O)cc1",
        100, "nM",
        fragments=["benzene", "amide", "phenol"],
    )
    cpd2 = CompoundRecord(
        "resmetirom_analog", "CC(=O)Oc1ccccc1C(=O)Nc1ccc(Cl)cc1",
        5000, "nM",  # 50x less active
        fragments=["benzene", "amide", "aryl_chloride"],  # Cl replaces OH
    )

    alert = detector.detect_cliff(cpd1, cpd2)
    print(f"✓ Cliff detected: {alert.detected}")
    print(f"    Severity: {alert.severity}, Magnitude: {alert.cliff_magnitude}")
    print(f"    Structural: {alert.structural_change[:60]}")
    if alert.pharmacophore_alert:
        print(f"    ⚠️  {alert.pharmacophore_alert_message}")


def test_cliff_scan():
    """Test scanning multiple compounds for cliffs"""
    detector = ActivityCliffDetector()

    compounds = [
        CompoundRecord("cpd_1", "CCO", 50, "nM", fragments=["alcohol"], activity_flag="active"),
        CompoundRecord("cpd_2", "CCCO", 55, "nM", fragments=["alcohol"], activity_flag="active"),
        CompoundRecord("cpd_3", "CCS", 40, "nM", fragments=["thiol"], activity_flag="active"),
        CompoundRecord("cpd_4", "CC(=O)O", 5000, "nM", fragments=["carboxylic_acid"], activity_flag="inactive"),
        CompoundRecord("cpd_5", "CC(=O)N", 6000, "nM", fragments=["amide"], activity_flag="inactive"),
    ]

    alerts = detector.scan_for_cliffs(compounds)
    summary = detector.get_cliff_summary(alerts)

    print(f"✓ Cliff scan: {summary['total_cliffs']} cliffs detected")
    print(f"    By severity: {summary['by_severity']}")
    print(f"    Pharmacophore alerts: {summary['pharmacophore_alerts']}")


def test_sar_analyzer():
    """Test SAR analysis"""
    analyzer = SARAnalyzer()

    compounds = [
        CompoundRecord("active_1", "CCO", 50, "nM", fragments=["alcohol", "benzene"], activity_flag="active"),
        CompoundRecord("active_2", "CCCO", 60, "nM", fragments=["alcohol", "benzene"], activity_flag="active"),
        CompoundRecord("active_3", "c1ccccc1CO", 45, "nM", fragments=["benzene", "alcohol"], activity_flag="active"),
        CompoundRecord("inactive_1", "CC(=O)O", 5000, "nM", fragments=["carboxylic_acid"], activity_flag="inactive"),
        CompoundRecord("inactive_2", "CCS", 6000, "nM", fragments=["thiol"], activity_flag="inactive"),
    ]

    result = analyzer.analyze(compounds)
    print(f"✓ SAR Analysis: {result['status']}")
    print(analyzer.summarize_sar(result))


if __name__ == "__main__":
    print("Testing Activity Cliff Detector...")
    test_compound_records()
    test_pharmacophore_extraction()
    test_pharmacophore_change_detection()
    test_activity_cliff_detection()
    test_cliff_scan()
    test_sar_analyzer()
    print("\n✅ All Activity Cliff Detector tests passed!")
