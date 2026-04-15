"""
ARP v24 - Disease-Specific Weight Configurations

Each disease has a unique weight matrix for 8 scoring dimensions.
Weights sum to 1.0 for each disease.
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class Disease(Enum):
    MASLD = "masld"
    SARCOPENIA = "sarcopenia"
    LUNG_FIBROSIS = "lung_fibrosis"
    HEART_FAILURE = "heart_failure"
    CANCER = "cancer"
    GENERIC = "generic"


@dataclass
class WeightConfig:
    genetic_causality: float = 0.10
    disease_context: float = 0.15
    perturbation_rescue: float = 0.20
    tissue_specificity: float = 0.10
    druggability: float = 0.10
    safety: float = 0.15
    translation: float = 0.10
    competitive_novelty: float = 0.10

    def validate(self) -> bool:
        total = (
            self.genetic_causality + self.disease_context
            + self.perturbation_rescue + self.tissue_specificity
            + self.druggability + self.safety
            + self.translation + self.competitive_novelty
        )
        return abs(total - 1.0) < 0.001


@dataclass
class PenaltyConfig:
    name: str
    description: str
    default_severity: float
    applicable_diseases: List[Disease]


DISEASE_WEIGHTS: Dict[Disease, WeightConfig] = {
    Disease.MASLD: WeightConfig(
        genetic_causality=0.05, disease_context=0.25,
        perturbation_rescue=0.15, tissue_specificity=0.20,
        druggability=0.10, safety=0.20, translation=0.05, competitive_novelty=0.00,
    ),
    Disease.SARCOPENIA: WeightConfig(
        genetic_causality=0.05, disease_context=0.15,
        perturbation_rescue=0.25, tissue_specificity=0.20,
        druggability=0.10, safety=0.20, translation=0.05, competitive_novelty=0.00,
    ),
    Disease.LUNG_FIBROSIS: WeightConfig(
        genetic_causality=0.05, disease_context=0.25,
        perturbation_rescue=0.20, tissue_specificity=0.15,
        druggability=0.10, safety=0.15, translation=0.10, competitive_novelty=0.00,
    ),
    Disease.HEART_FAILURE: WeightConfig(
        genetic_causality=0.05, disease_context=0.20,
        perturbation_rescue=0.20, tissue_specificity=0.10,
        druggability=0.05, safety=0.25, translation=0.15, competitive_novelty=0.00,
    ),
    Disease.CANCER: WeightConfig(
        genetic_causality=0.20, disease_context=0.20,
        perturbation_rescue=0.20, tissue_specificity=0.00,
        druggability=0.05, safety=0.15, translation=0.15, competitive_novelty=0.05,
    ),
    Disease.GENERIC: WeightConfig(
        genetic_causality=0.15, disease_context=0.15,
        perturbation_rescue=0.20, tissue_specificity=0.10,
        druggability=0.15, safety=0.15, translation=0.05, competitive_novelty=0.05,
    ),
}


DISEASE_PENALTIES: Dict[Disease, List[PenaltyConfig]] = {
    Disease.MASLD: [
        PenaltyConfig("hepatotoxicity", "Drug-induced liver injury", 0.20, [Disease.MASLD]),
        PenaltyConfig("dyslipidemia_worsening", "Worsening blood lipid profile", 0.15, [Disease.MASLD]),
        PenaltyConfig("weight_gain", "Unwanted weight gain", 0.10, [Disease.MASLD]),
    ],
    Disease.SARCOPENIA: [
        PenaltyConfig("tumor_growth_concern", "Potential to promote cancer", 0.20, [Disease.SARCOPENIA]),
        PenaltyConfig("immunosuppression", "Immune system suppression", 0.15, [Disease.SARCOPENIA]),
        PenaltyConfig("cardiac_adverse_effects", "Cardiovascular side effects", 0.10, [Disease.SARCOPENIA]),
    ],
    Disease.LUNG_FIBROSIS: [
        PenaltyConfig("wound_healing_inhibition", "Impairing tissue repair", 0.20, [Disease.LUNG_FIBROSIS]),
        PenaltyConfig("epithelial_regeneration_impairment", "Preventing lung repair", 0.20, [Disease.LUNG_FIBROSIS]),
    ],
    Disease.HEART_FAILURE: [
        PenaltyConfig("qtc_herg_risk", "QT prolongation risk", 0.20, [Disease.HEART_FAILURE]),
        PenaltyConfig("contractility_worsening", "Negative inotropic effect", 0.15, [Disease.HEART_FAILURE]),
        PenaltyConfig("pro_arrhythmia", "Pro-arrhythmic potential", 0.20, [Disease.HEART_FAILURE]),
    ],
    Disease.CANCER: [
        PenaltyConfig("pan_essential_gene", "Essential in normal tissues", 0.25, [Disease.CANCER]),
        PenaltyConfig("resistance_bypass_likely", "Cancer will likely bypass", 0.15, [Disease.CANCER]),
    ],
}


MODALITY_PREFERENCES: Dict[Disease, Dict[str, float]] = {
    Disease.MASLD: {"small_molecule": 0.90, "liver_targeted_oligo": 0.80, "peptide_analog": 0.60, "biologic": 0.50},
    Disease.SARCOPENIA: {"biologic": 0.85, "peptide": 0.80, "small_molecule": 0.70, "oligo": 0.50},
    Disease.LUNG_FIBROSIS: {"inhaled_small_molecule": 0.90, "small_molecule": 0.80, "biologic": 0.70, "antibody": 0.65},
    Disease.HEART_FAILURE: {"small_molecule": 0.90, "biologic": 0.70, "antibody": 0.65},
    Disease.CANCER: {"small_molecule": 0.85, "degrader": 0.80, "antibody": 0.75, "adc": 0.70, "biologic": 0.60},
}


TARGET_CLASS_MODALITY: Dict[str, Dict[str, float]] = {
    "extracellular_ligand": {"biologic": 0.95, "peptide": 0.80, "antibody": 0.90, "small_molecule": 0.40},
    "kinase": {"small_molecule": 0.90, "degrader": 0.60, "biologic": 0.50},
    "enzyme": {"small_molecule": 0.85, "oligo": 0.65, "biologic": 0.50},
    "transcription_factor": {"oligo": 0.75, "degrader": 0.70, "small_molecule": 0.40},
    "nuclear_receptor": {"small_molecule": 0.95, "peptide": 0.30},
    "gpcr": {"small_molecule": 0.85, "peptide": 0.75, "biologic": 0.60},
    "transporter": {"small_molecule": 0.90},
    "ion_channel": {"small_molecule": 0.90},
    "cell_surface_antigen": {"antibody": 0.95, "adc": 0.90},
}


def get_disease_weights(disease: Disease) -> WeightConfig:
    return DISEASE_WEIGHTS.get(disease, DISEASE_WEIGHTS[Disease.GENERIC])

def get_modality_score(disease: Disease, modality: str) -> float:
    return MODALITY_PREFERENCES.get(disease, {}).get(modality, 0.5)

def get_penalties_for_disease(disease: Disease) -> List[PenaltyConfig]:
    return DISEASE_PENALTIES.get(disease, [])
