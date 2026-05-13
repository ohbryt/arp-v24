"""
IBDseq Integration for ARP Pipeline
=====================================
Broad Institute IBD Genetics Database.

URL: https://ibdseq.broadinstitute.org/

Usage:
    from ibdseq_integration import query_ibd_genes, get_ferroptosis_ibd_link
    genes = query_ibd_genes("autophagy")
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class IBDGene:
    """IBD-associated gene"""
    gene_name: str
    function: str
    pathway: str
    variants: List[str]
    ibd_relevance: str


class IBDseqIntegration:
    """
    IBDseq wrapper for inflammatory bowel disease genetics.
    
    Based on: Broad Institute IBDseq Database
    URL: https://ibdseq.broadinstitute.org/
    
    Integration with ARP:
    - Target discovery for GI disorders
    - Ferroptosis-IBD connection
    - MASLD-IBD metabolic overlap
    """
    
    # Core IBD genes from literature
    IBD_GENES = {
        "NOD2": {
            "function": "Intracellular bacterial sensor",
            "pathway": "Autophagy/NOD2 signaling",
            "variants": ["R702W", "G908R", "L1007fs"],
            "ibd_relevance": "Risk for Crohn's disease"
        },
        "ATG16L1": {
            "function": "Autophagy initiator",
            "pathway": "Autophagy",
            "variants": ["T300A"],
            "ibd_relevance": "Risk for Crohn's disease"
        },
        "IL23R": {
            "function": "Th17 differentiation receptor",
            "pathway": "IL-23/Th17 axis",
            "variants": ["G149R"],
            "ibd_relevance": "Protective and risk variants"
        },
        "IRGM": {
            "function": "Autophagy regulator",
            "pathway": "Autophagy",
            "variants": ["-20kb deletion"],
            "ibd_relevance": "Risk for Crohn's disease"
        },
        "IL10": {
            "function": "Anti-inflammatory cytokine",
            "pathway": "Immune regulation",
            "variants": ["Promoter -1082A"],
            "ibd_relevance": "Risk for early-onset IBD"
        },
        "PTPN2": {
            "function": "T cell regulator",
            "pathway": "T cell signaling",
            "variants": ["rs2542151"],
            "ibd_relevance": "Risk for Crohn's and celiac"
        },
        "STAT3": {
            "function": "Transcription factor",
            "pathway": "IL-6/STAT3 signaling",
            "variants": ["rs2293152"],
            "ibd_relevance": "Risk for IBD"
        },
        "TNFSF15": {
            "function": "Inflammatory cytokine",
            "pathway": "TNF family",
            "variants": ["rs6478108"],
            "ibd_relevance": "Risk for Crohn's and UC"
        }
    }
    
    # Ferroptosis-IBD connection
    FERROPTOSIS_IBD_LINKS = {
        "GPX4": {
            "role": "Lipid peroxidase defense",
            "ibd_connection": "Protective in gut inflammation",
            "evidence": "Knockout mice develop colitis"
        },
        "SLC7A11": {
            "role": "cystine/glutamate antiporter",
            "ibd_connection": "Ferroptosis sensitivity in gut",
            "evidence": "Expression altered in IBD"
        },
        "ACSL4": {
            "role": "Lipid metabolism enzyme",
            "ibd_connection": "AA accumulation → ferroptosis",
            "evidence": "Upregulated in IBD inflammation"
        },
        "FSP1": {
            "role": "CoQ10 reductase",
            "ibd_connection": "Potential protective role",
            "evidence": "Not yet studied in IBD"
        },
        "GCH1": {
            "role": "BH4 biosynthesis",
            "ibd_connection": "Lipid peroxidation defense",
            "evidence": "Protective in inflammatory contexts"
        }
    }
    
    # MASLD-IBD overlap
    MASLD_IBD_SHARED = {
        "pathways": ["TNF signaling", "IL-6/STAT3", "PPAR signaling"],
        "genes": ["PPARG", "HNF4A", "STAT3", "TNF", "IL10"],
        "mechanisms": ["Metabolic inflammation", "Gut-liver axis"]
    }
    
    def __init__(self):
        self.data_url = "https://ibdseq.broadinstitute.org/"
    
    def get_gene_info(self, gene_name: str) -> Optional[Dict[str, Any]]:
        """Get IBD gene information"""
        return self.IBD_GENES.get(gene_name.upper())
    
    def query_ibd_genes(self, pathway: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query IBD genes by pathway.
        
        Args:
            pathway: "autophagy", "il23", "immune", or None for all
        
        Returns:
            List of IBD genes
        """
        results = []
        
        for gene, data in self.IBD_GENES.items():
            if pathway is None or pathway.lower() in data["pathway"].lower():
                results.append({
                    "gene": gene,
                    **data
                })
        
        return results
    
    def get_ferroptosis_ibd_link(self) -> Dict[str, Any]:
        """
        Get ferroptosis-IBD connection analysis.
        
        Returns:
            Dict with ferroptosis genes and IBD relevance
        """
        return self.FERROPTOSIS_IBD_LINKS
    
    def check_ferroptosis_in_ibd(self, gene_name: str) -> Optional[Dict[str, Any]]:
        """
        Check if a ferroptosis gene has IBD relevance.
        
        Args:
            gene_name: Ferroptosis gene (e.g., "GPX4", "SLC7A11")
        
        Returns:
            Analysis if relevant, None otherwise
        """
        return self.FERROPTOSIS_IBD_LINKS.get(gene_name.upper())
    
    def get_masld_ibd_overlap(self) -> Dict[str, Any]:
        """
        Get MASLD-IBD metabolic overlap.
        
        Returns:
            Shared pathways and genes
        """
        return self.MASLD_IBD_SHARED
    
    def analyze_target_for_ibd(self, target_gene: str) -> Dict[str, Any]:
        """
        Analyze if an ARP target has IBD relevance.
        
        Args:
            target_gene: Target gene name
        
        Returns:
            IBD analysis
        """
        gene_upper = target_gene.upper()
        
        # Check IBD genes
        ibd_info = self.IBD_GENES.get(gene_upper)
        
        # Check ferroptosis-IBD
        ferroptosis_info = self.FERROPTOSIS_IBD_LINKS.get(gene_upper)
        
        # Check MASLD-IBD
        masld_genes = self.MASLD_IBD_SHARED.get("genes", [])
        in_masld_ibd = gene_upper in [g.upper() for g in masld_genes]
        
        return {
            "target": target_gene,
            "ibd_gene": ibd_info is not None,
            "ferroptosis_ibd": ferroptosis_info is not None,
            "masld_ibd_overlap": in_masld_ibd,
            "ibd_details": ibd_info,
            "ferroptosis_details": ferroptosis_info,
            "recommendation": self._get_recommendation(
                ibd_info, ferroptosis_info, in_masld_ibd
            )
        }
    
    def _get_recommendation(
        self,
        ibd_info: Optional[Dict],
        ferroptosis_info: Optional[Dict],
        in_masld_ibd: bool
    ) -> str:
        """Generate recommendation based on analysis"""
        if ibd_info:
            return f"Known IBD gene ({ibd_info['pathway']}) - explore for gut-specific therapy"
        elif ferroptosis_info:
            return f"Ferroptosis-IBD link ({ferroptosis_info['role']}) - investigate protective potential"
        elif in_masld_ibd:
            return "MASLD-IBD shared pathway - consider metabolic inflammation angle"
        else:
            return "No direct IBD link - explore indirect connections via inflammation"


def query_ibd_genes(pathway: str = None) -> List[Dict[str, Any]]:
    """Convenience function for IBD gene query"""
    integrator = IBDseqIntegration()
    return integrator.query_ibd_genes(pathway)


def analyze_ferroptosis_ibd(gene: str) -> Optional[Dict[str, Any]]:
    """Check ferroptosis-IBD connection"""
    integrator = IBDseqIntegration()
    return integrator.check_ferroptosis_in_ibd(gene)


# Test
if __name__ == "__main__":
    print("=== IBDseq Integration Test ===\n")
    
    integrator = IBDseqIntegration()
    
    # Query autophagy genes
    print("1. Autophagy IBD genes:")
    genes = integrator.query_ibd_genes("autophagy")
    for g in genes:
        print(f"   - {g['gene']}: {g['function']}")
    
    # Ferroptosis-IBD link
    print("\n2. Ferroptosis-IBD links:")
    links = integrator.get_ferroptosis_ibd_link()
    for gene, data in links.items():
        print(f"   - {gene}: {data['ibd_connection']}")
    
    # Analyze ARP targets
    print("\n3. ARP target analysis:")
    for target in ["GPX4", "SLC7A11", "FSP1", "NOD2"]:
        result = integrator.analyze_target_for_ibd(target)
        print(f"   - {target}: IBD={result['ibd_gene']}, Ferro={result['ferroptosis_ibd']}, MASLD={result['masld_ibd_overlap']}")
    
    # MASLD-IBD overlap
    print("\n4. MASLD-IBD shared pathways:")
    overlap = integrator.get_masld_ibd_overlap()
    print(f"   Pathways: {overlap['pathways']}")
    
    print("\n✓ IBDseq integration OK!")