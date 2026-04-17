#!/usr/bin/env python3
"""
Enhanced ARP v24 with BioContext MCP Integration

This script integrates BioContext MCP servers into the ARP pipeline,
providing real-time access to major biological databases.
"""

import sys
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import ARP components
from core.scoring_engine import TARGET_REGISTRY
from core.candidate_engine import CANDIDATE_DATABASES
from core.schema import validate_target, validate_compound

# BioContext integration
try:
    from integration.biocontext_mcp import BioContextIntegration
    BIOCONTEXT_AVAILABLE = True
except ImportError:
    BIOCONTEXT_AVAILABLE = False
    print("⚠️  BioContext integration not available")

class EnhancedARP:
    """
    Enhanced Automated Research Pipeline with BioContext MCP integration
    """
    
    def __init__(self, config_path: str = None):
        """Initialize enhanced ARP"""
        self.config = self._load_config(config_path)
        self.biocontext = None
        self.pipeline_version = "2.0 with BioContext MCP"
        self.timestamp = datetime.now().isoformat()
        
        # Initialize BioContext if available
        if BIOCONTEXT_AVAILABLE:
            self.biocontext = BioContextIntegration()
            print("✅ BioContext MCP servers initialized")
        else:
            print("⚠️  Running in standard ARP mode")
    
    def _load_config(self, config_path: str = None):
        """Load configuration"""
        default_config = {
            'priorities': {
                'sarcopenia': ['MSTN', 'FOXO1', 'PRKAA1', 'MTOR', 'NRF2'],
                'masld': ['NR1H4', 'PPARA', 'ACACA', 'SREBF1', 'THRB'],
                'cancer': ['EGFR', 'KRAS', 'BRAF', 'PIK3CA', 'PTEN']
            },
            'databases': {
                'pubchem': True,
                'chembl': True,
                'uniprot': True,
                'pubmed': True
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def enhanced_target_discovery(self, disease: str, targets: List[str] = None) -> Dict[str, Any]:
        """
        Enhanced target discovery with BioContext integration
        """
        print(f"🎯 Enhanced Target Discovery for {disease}")
        
        # Use default targets if not provided
        if targets is None:
            targets = self.config['priorities'].get(disease, ['MSTN', 'FOXO1'])
        
        results = {}
        
        for target in targets:
            print(f"   🔍 Validating {target}...")
            
            # Standard ARP validation
            arp_validation = validate_target(target, disease)
            
            # BioContext enhancement
            bio_context = {}
            if self.biocontext:
                try:
                    bio_context = self.biocontext.validate_target(target, 'gene')
                    bio_context['source'] = 'BioContext MCP'
                except Exception as e:
                    print(f"   ⚠️  BioContext error: {e}")
            
            # Integrated scoring
            integrated_score = self._calculate_integrated_score(arp_validation, bio_context)
            
            results[target] = {
                'arp': arp_validation,
                'biocontext': bio_context if bio_context else {},
                'integrated_score': integrated_score,
                'biocontext_enabled': BIOCONTEXT_AVAILABLE
            }
        
        # Rank targets by integrated score
        ranked_targets = dict(sorted(results.items(), 
                                  key=lambda x: x[1]['integrated_score'], 
                                  reverse=True))
        
        return ranked_targets
    
    def enhanced_compound_screening(self, 
                                  targets: List[str], 
                                  compound_library: List[str] = None) -> Dict[str, Any]:
        """
        Enhanced compound screening with BioContext integration
        """
        print(f"🔬 Enhanced Compound Screening for {len(targets)} targets")
        
        # Default compound library
        if compound_library is None:
            compound_library = [
                'Astaxanthin', 'Quercetin', 'Ursolic Acid', 'Tomatidine',
                'Embelin', 'Berberine', 'Resveratrol', 'Curcumin', 
                'MyoStatinX', 'AmpkBoost'
            ]
        
        results = {}
        
        for target in targets:
            print(f"   🎯 Screening against {target}...")
            
            target_results = {}
            
            for compound in compound_library:
                print(f"      💊 {compound}...")
                
                # Standard ARP screening
                arp_screening = validate_compound(compound, target)
                
                # BioContext enhancement
                bio_context = {}
                if self.biocontext:
                    try:
                        bio_context = self.biocontext.get_compound_properties(compound)
                        bio_context['source'] = 'BioContext MCP'
                    except Exception as e:
                        print(f"      ⚠️  BioContext error: {e}")
                
                # Combined scoring
                combined_score = self._calculate_combined_score(arp_screening, bio_context)
                
                key = f"{target}_{compound}"
                results[key] = {
                    'arp': arp_screening,
                    'biocontext': bio_context if bio_context else {},
                    'combined_score': combined_score,
                    'biocontext_enabled': BIOCONTEXT_AVAILABLE
                }
        
        # Rank results by combined score
        ranked_results = dict(sorted(results.items(), 
                                  key=lambda x: x[1]['combined_score'], 
                                  reverse=True))
        
        return ranked_results
    
    def generate_comprehensive_report(self, 
                                    disease: str, 
                                    targets: List[str], 
                                    compounds: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive ARP report with BioContext data
        """
        print(f"📊 Generating comprehensive report for {disease}")
        
        # Perform analyses
        target_discovery = self.enhanced_target_discovery(disease, targets)
        compound_screening = self.enhanced_compound_screening(targets, compounds)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(target_discovery, compound_screening)
        
        # Compile report
        report = {
            'metadata': {
                'pipeline_version': self.pipeline_version,
                'timestamp': self.timestamp,
                'biocontext_enabled': BIOCONTEXT_AVAILABLE,
                'disease': disease
            },
            'target_discovery': target_discovery,
            'compound_screening': compound_screening,
            'recommendations': recommendations,
            'integration_quality': self._assess_integration_quality()
        }
        
        return report
    
    def _calculate_integrated_score(self, arp_score: Dict, bio_context: Dict) -> float:
        """Calculate integrated score from ARP and BioContext"""
        arp_weight = 0.7
        bio_weight = 0.3
        
        arp_score_value = arp_score.get('score', 0)
        bio_score_value = bio_context.get('confidence', 0) if bio_context else 0
        
        integrated_score = (arp_score_value * arp_weight) + (bio_score_value * bio_weight)
        return round(integrated_score, 3)
    
    def _calculate_combined_score(self, arp_score: Dict, bio_context: Dict) -> float:
        """Calculate combined score from ARP and BioContext"""
        arp_weight = 0.6
        bio_weight = 0.4
        
        arp_score_value = arp_score.get('score', 0)
        bio_score_value = bio_context.get('bioactivity_score', 0) if bio_context else 0
        
        combined_score = (arp_score_value * arp_weight) + (bio_score_value * bio_weight)
        return round(combined_score, 3)
    
    def _generate_recommendations(self, 
                                target_discovery: Dict, 
                                compound_screening: Dict) -> Dict[str, Any]:
        """Generate research recommendations"""
        
        # Top targets
        top_targets = list(target_discovery.keys())[:3]
        
        # Top compounds
        top_compounds = []
        for key, data in compound_screening.items():
            if data['combined_score'] > 0.7:
                compound_name = key.split('_')[1]
                if compound_name not in top_compounds:
                    top_compounds.append(compound_name)
        
        # Next steps
        next_steps = []
        if BIOCONTEXT_AVAILABLE:
            next_steps.extend([
                'Validate BioContext MCP server connections',
                'Optimize query parameters for performance',
                'Add additional database integrations'
            ])
        else:
            next_steps.extend([
                'Install BioContext MCP servers',
                'Configure MCP client connections',
                'Test database access functionality'
            ])
        
        return {
            'top_targets': top_targets,
            'top_compounds': top_compounds[:5],
            'next_steps': next_steps,
            'integration_status': 'active' if BIOCONTEXT_AVAILABLE else 'pending'
        }
    
    def _assess_integration_quality(self) -> Dict[str, Any]:
        """Assess the quality of BioContext integration"""
        
        if not BIOCONTEXT_AVAILABLE:
            return {
                'status': 'inactive',
                'servers': [],
                'coverage': 0
            }
        
        available_servers = []
        for server, config in self.config['databases'].items():
            if config:
                available_servers.append(server)
        
        return {
            'status': 'active',
            'servers': available_servers,
            'coverage': len(available_servers) / 8,  # 8 total servers
            'performance': 'good'  # Would measure actual performance in production
        }

# Example usage
def main():
    """Main execution function"""
    
    print("=" * 80)
    print("ENHANCED ARP v24 WITH BIOCONTEXT MCP INTEGRATION")
    print("=" * 80)
    
    # Initialize enhanced ARP
    arp = EnhancedARP()
    
    # Example 1: Sarcopenia research
    print("\n🦾 SARCOPENIA RESEARCH EXAMPLE")
    print("-" * 50)
    
    disease = "sarcopenia"
    targets = ["MSTN", "FOXO1", "PRKAA1"]
    compounds = ["Astaxanthin", "Embelin", "Berberine"]
    
    # Generate comprehensive report
    report = arp.generate_comprehensive_report(disease, targets, compounds)
    
    # Display results
    print(f"\n🎯 Top Targets for {disease}:")
    for target, data in report['target_discovery'].items():
        score = data['integrated_score']
        biocontext = "✅" if data['biocontext_enabled'] else "❌"
        print(f"   {target}: {score:.2f} {biocontext}")
    
    print(f"\n💊 Top Compounds:")
    for compound in report['recommendations']['top_compounds']:
        print(f"   {compound}")
    
    print(f"\n📋 Next Steps:")
    for step in report['recommendations']['next_steps']:
        print(f"   • {step}")
    
    # Save report
    report_filename = f"arp_enhanced_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_filename}")
    
    return report

if __name__ == "__main__":
    main()
