"""
MedSci Skills Registry for ARP v24

Comprehensive registry mapping all 32 medsci-skills to their locations,
purposes, and integration status within the ARP pipeline.

Skills Source: /Users/ocm/.openclaw/workspace/medsci-skills/skills/
Integration Target: /Users/ocm/.openclaw/workspace/arp-v24/

Usage:
    from skills.med_sci_registry import MedSciRegistry
    registry = MedSciRegistry()
    registry.list_all()
    registry.get_skill_info('write-paper')
    registry.get_skill_path('search-lit')
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import os

# Path constants
MEDSCI_SKILLS_PATH = "/Users/ocm/.openclaw/workspace/medsci-skills/skills"
ARP_V24_PATH = "/Users/ocm/.openclaw/workspace/arp-v24"
INTEGRATION_PATH = os.path.join(ARP_V24_PATH, "integration")
SKILLS_PATH = os.path.join(ARP_V24_PATH, "skills")


@dataclass
class SkillInfo:
    """Information about a single medsci skill"""
    name: str
    skill_dir: str
    purpose: str
    arp_use_case: str
    integration_status: str  # 'integrated' | 'planned' | 'pending' | 'reference'
    key_files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    reporting_guideline: Optional[str] = None
    api_class: Optional[str] = None


class MedSciRegistry:
    """
    Central registry for all 32 medsci-skills.
    Provides metadata, paths, and integration status for each skill.
    """
    
    # All 32 medsci skills with full metadata
    SKILLS: Dict[str, SkillInfo] = {
        "add-journal": SkillInfo(
            name="add-journal",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "add-journal"),
            purpose="Add new journal profiles to the journal database for submission targeting",
            arp_use_case="Extend journal database with custom journals; extract metadata from author guidelines",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="AddJournal"
        ),
        
        "analyze-stats": SkillInfo(
            name="analyze-stats",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "analyze-stats"),
            purpose="Generate R/Python code for statistical analysis of medical research data",
            arp_use_case="Table 1 demographics, diagnostic accuracy (AUC/ROC/Sensitivity/Specificity), "
                        "meta-analysis stats, agreement (ICC/Kappa), regression (logistic/linear/Cox), "
                        "propensity score (PSM/IPTW), repeated measures (ANOVA/Mixed/GEE)",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="AnalyzeStats",
            dependencies=["clean-data"]
        ),
        
        "author-strategy": SkillInfo(
            name="author-strategy",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "author-strategy"),
            purpose="PubMed author profile analysis and strategy for bibliometric analysis",
            arp_use_case="Analyze publication history, H-index patterns, collaboration networks",
            integration_status="planned",
            key_files=["SKILL.md"]
        ),
        
        "batch-cohort": SkillInfo(
            name="batch-cohort",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "batch-cohort"),
            purpose="N×M analysis templates for batch cohort studies",
            arp_use_case="Multi-arm comparison studies, factorial designs, stratified analyses",
            integration_status="planned",
            key_files=["SKILL.md"]
        ),
        
        "calc-sample-size": SkillInfo(
            name="calc-sample-size",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "calc-sample-size"),
            purpose="Sample size calculation for 11 tests including Cox EPV, power analysis, IRB justification text",
            arp_use_case="Pre-study power analysis; IRB protocol sample size justification; "
                        "support: t-test, Chi-square, McNemar, log-rank, Cox regression, ANOVA, "
                        "correlation, AUC comparison, sensitivity analysis",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="CalcSampleSize",
            dependencies=["design-study"]
        ),
        
        "check-reporting": SkillInfo(
            name="check-reporting",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "check-reporting"),
            purpose="Check manuscript compliance with 33 medical research reporting guidelines",
            arp_use_case="Pre-submission compliance audit; quality control in manuscript pipeline",
            integration_status="integrated",
            key_files=["SKILL.md", "references/checklists/"],
            reporting_guideline="STROBE, CONSORT, STARD, STARD-AI, TRIPOD, TRIPOD+AI, PRISMA 2020, "
                               "PRISMA-DTA, PRISMA-P, ARRIVE, CARE, SPIRIT, CLAIM, MI-CLEAR-LLM, "
                               "SQUIRE 2.0, CLEAR, MOOSE, GRRAS, SWiM, AMSTAR 2, QUADAS-2, QUADAS-C, "
                               "RoB 2, ROBINS-I, ROBINS-E, ROBIS, ROB-ME, PROBAST, PROBAST+AI, "
                               "NOS, COSMIN, RoB NMA",
            api_class="CheckReporting",
            dependencies=["write-paper"]
        ),
        
        "clean-data": SkillInfo(
            name="clean-data",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "clean-data"),
            purpose="Data profiling, missing value flagging, outlier detection, cleaning code generation",
            arp_use_case="Pre-analysis data quality assessment; data preparation pipeline",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="CleanData",
            dependencies=["deidentify"]
        ),
        
        "cross-national": SkillInfo(
            name="cross-national",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "cross-national"),
            purpose="Cross-national comparison study design and analysis",
            arp_use_case="Multi-country epidemiological studies; international health comparisons",
            integration_status="planned",
            key_files=["SKILL.md"],
            dependencies=["design-study", "analyze-stats"]
        ),
        
        "deidentify": SkillInfo(
            name="deidentify",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "deidentify"),
            purpose="De-identify clinical data containing PHI/PII before LLM processing; standalone Python CLI",
            arp_use_case="PHI safety gate before any data-handling skill; patient data anonymization",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="Deidentify",
            dependencies=[]
        ),
        
        "design-study": SkillInfo(
            name="design-study",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "design-study"),
            purpose="Study design review; identify leakage/bias; pick reporting guideline; validate analysis plan",
            arp_use_case="Pre-protocol study design validation; methodology quality check",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="DesignStudy"
        ),
        
        "fill-protocol": SkillInfo(
            name="fill-protocol",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "fill-protocol"),
            purpose="Protocol completion and gap filling",
            arp_use_case="Complete partially drafted protocols; add missing sections",
            integration_status="planned",
            key_files=["SKILL.md"],
            dependencies=["write-protocol"]
        ),
        
        "find-cohort-gap": SkillInfo(
            name="find-cohort-gap",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "find-cohort-gap"),
            purpose="Research gap finder for cohort studies",
            arp_use_case="Identify underexplored research questions in existing cohort literature",
            integration_status="planned",
            key_files=["SKILL.md"],
            dependencies=["search-lit"]
        ),
        
        "find-journal": SkillInfo(
            name="find-journal",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "find-journal"),
            purpose="Journal recommendation based on abstract/scope matching; 93 journal profiles",
            arp_use_case="Post-rejection re-targeting; journal selection for new submissions",
            integration_status="integrated",
            key_files=["SKILL.md", "references/journal_profiles/"],
            api_class="FindJournal",
            dependencies=["write-paper"]
        ),
        
        "fulltext-retrieval": SkillInfo(
            name="fulltext-retrieval",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "fulltext-retrieval"),
            purpose="Batch download open-access PDFs by DOI using Unpaywall, PMC, OpenAlex APIs",
            arp_use_case="Systematic review full-text collection; literature review PDF gathering",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="FulltextRetrieval",
            dependencies=["search-lit"]
        ),
        
        "grant-builder": SkillInfo(
            name="grant-builder",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "grant-builder"),
            purpose="Grant proposal generator: significance, innovation, approach, milestones",
            arp_use_case="NIH/NSF grant drafting; funding application preparation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="GrantBuilder",
            dependencies=["search-lit", "design-study"]
        ),
        
        "humanize": SkillInfo(
            name="humanize",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "humanize"),
            purpose="Remove AI writing patterns from manuscript text",
            arp_use_case="Post-LLM writing polish; AI pattern removal for natural prose",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="Humanize",
            dependencies=["write-paper"]
        ),
        
        "intake-project": SkillInfo(
            name="intake-project",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "intake-project"),
            purpose="New or messy project folder classification and scaffolding",
            arp_use_case="Project initialization; workspace organization; classify project type",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="IntakeProject"
        ),
        
        "lit-sync": SkillInfo(
            name="lit-sync",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "lit-sync"),
            purpose="Zotero + Obsidian sync for literature management",
            arp_use_case="Literature management workflow; reference synchronization",
            integration_status="reference",
            key_files=["SKILL.md"],
            api_class="LitSync",
            dependencies=["search-lit"]
        ),
        
        "ma-scout": SkillInfo(
            name="ma-scout",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "ma-scout"),
            purpose="Meta-analysis scout for identifying existing systematic reviews",
            arp_use_case="Pre-meta-analysis landscape assessment; avoid duplication",
            integration_status="planned",
            key_files=["SKILL.md"],
            dependencies=["search-lit"]
        ),
        
        "make-figures": SkillInfo(
            name="make-figures",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "make-figures"),
            purpose="Publication-ready figures: ROC curves, forest plots, flow diagrams, Kaplan-Meier, Bland-Altman",
            arp_use_case="Visual abstracts, CONSORT/STARD/PRISMA diagrams, performance curves, "
                        "graphical abstracts",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="MakeFigures",
            dependencies=["analyze-stats"]
        ),
        
        "manage-project": SkillInfo(
            name="manage-project",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "manage-project"),
            purpose="Project scaffolding, progress tracking, checklists and timelines",
            arp_use_case="Project initialization; milestone tracking; submission checklists",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="ManageProject",
            dependencies=["intake-project"]
        ),
        
        "meta-analysis": SkillInfo(
            name="meta-analysis",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "meta-analysis"),
            purpose="Full systematic review pipeline: protocol, search, screening, extraction, synthesis, PRISMA-DTA",
            arp_use_case="End-to-end meta-analysis from question to forest plots; systematic review automation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="MetaAnalysis",
            dependencies=["search-lit", "fulltext-retrieval", "analyze-stats", "make-figures"]
        ),
        
        "orchestrate": SkillInfo(
            name="orchestrate",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "orchestrate"),
            purpose="Entry point orchestrator for ambiguous or multi-step requests; skill routing",
            arp_use_case="Main entry point for medsci-skills; routes to appropriate skill(s); "
                        "manages multi-step workflows including PHI safety gate",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="Orchestrate",
            dependencies=["all"]
        ),
        
        "peer-review": SkillInfo(
            name="peer-review",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "peer-review"),
            purpose="Peer review preparation; journal scope-aware review",
            arp_use_case="Pre-submission peer review simulation; reviewer comments preparation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="PeerReview",
            dependencies=["write-paper", "find-journal"]
        ),
        
        "present-paper": SkillInfo(
            name="present-paper",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "present-paper"),
            purpose="Academic talk preparation: paper analysis, script drafting, slide notes, Q&A prep",
            arp_use_case="Conference presentation; journal club preparation; academic talks",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="PresentPaper",
            dependencies=["write-paper"]
        ),
        
        "publish-skill": SkillInfo(
            name="publish-skill",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "publish-skill"),
            purpose="Package personal skills for open-source distribution",
            arp_use_case="Skill sharing; distribute custom skills to other researchers",
            integration_status="reference",
            key_files=["SKILL.md"],
            api_class="PublishSkill"
        ),
        
        "replicate-study": SkillInfo(
            name="replicate-study",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "replicate-study"),
            purpose="Study replication planning and execution",
            arp_use_case="Validate published findings; replication studies",
            integration_status="planned",
            key_files=["SKILL.md"],
            dependencies=["search-lit", "design-study"]
        ),
        
        "revise": SkillInfo(
            name="revise",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "revise"),
            purpose="Parse reviewer comments; generate point-by-point response; track changes",
            arp_use_case="Revision letter drafting; response to reviewers; resubmission preparation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="Revise",
            dependencies=["write-paper"]
        ),
        
        "search-lit": SkillInfo(
            name="search-lit",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "search-lit"),
            purpose="PubMed literature search, citation verification, BibTeX generation",
            arp_use_case="Literature search for evidence; citation verification; reference building",
            integration_status="integrated",
            key_files=["SKILL.md", "references/"],
            api_class="SearchLit",
            dependencies=[]
        ),
        
        "self-review": SkillInfo(
            name="self-review",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "self-review"),
            purpose="Pre-submission self-check from reviewer perspective; 10 categories",
            arp_use_case="Final quality gate before submission; internal review simulation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="SelfReview",
            dependencies=["write-paper"]
        ),
        
        "write-paper": SkillInfo(
            name="write-paper",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "write-paper"),
            purpose="IMRAD manuscript writing: 8-phase pipeline from outline to submission-ready",
            arp_use_case="Full manuscript drafting; supports original articles, case reports, "
                        "meta-analyses, AI validation studies, animal studies, technical notes, NHIS cohorts",
            integration_status="integrated",
            key_files=["SKILL.md", "references/"],
            api_class="WritePaper",
            dependencies=["search-lit", "analyze-stats", "make-figures", "check-reporting", "self-review"]
        ),
        
        "write-protocol": SkillInfo(
            name="write-protocol",
            skill_dir=os.path.join(MEDSCI_SKILLS_PATH, "write-protocol"),
            purpose="IRB/ethics protocol drafting: 4 core sections + 6 skeleton sections with TODO markers",
            arp_use_case="Ethics submission preparation; IRB protocol drafting; research protocol generation",
            integration_status="integrated",
            key_files=["SKILL.md"],
            api_class="WriteProtocol",
            dependencies=["design-study", "calc-sample-size", "search-lit"]
        ),
    }
    
    # Skill categories for organization
    SKILL_CATEGORIES = {
        "Literature & Research": [
            "search-lit", "fulltext-retrieval", "lit-sync", 
            "find-cohort-gap", "ma-scout", "author-strategy"
        ],
        "Study Design & Protocol": [
            "design-study", "write-protocol", "calc-sample-size",
            "fill-protocol", "replicate-study"
        ],
        "Data Handling": [
            "deidentify", "clean-data", "intake-project"
        ],
        "Statistical Analysis": [
            "analyze-stats", "batch-cohort", "cross-national"
        ],
        "Visualization": [
            "make-figures"
        ],
        "Manuscript Writing": [
            "write-paper", "humanize", "self-review", "revise",
            "present-paper", "peer-review"
        ],
        "Publishing & Submission": [
            "find-journal", "add-journal", "check-reporting", 
            "grant-builder", "manage-project"
        ],
        "Meta-Analysis & Reviews": [
            "meta-analysis"
        ],
        "Skill Development": [
            "publish-skill"
        ],
        "Orchestration": [
            "orchestrate"
        ]
    }
    
    # Common multi-skill workflows
    WORKFLOWS = {
        "new_project": ["intake-project", "search-lit", "design-study", "manage-project"],
        "data_to_manuscript": ["manage-project", "analyze-stats", "make-figures", "write-paper"],
        "draft_to_submission": ["self-review", "check-reporting", "search-lit", "manage-project"],
        "post_rejection": ["revise", "analyze-stats", "make-figures"],
        "meta_analysis": ["search-lit", "fulltext-retrieval", "meta-analysis"],
        "grant_writing": ["search-lit", "grant-builder"],
        "new_study_protocol": ["search-lit", "design-study", "calc-sample-size", "write-protocol"],
        "phi_pipeline": ["deidentify", "clean-data", "analyze-stats", "make-figures", "write-paper"],
        "full_submission": ["write-paper", "self-review", "check-reporting", "find-journal", "write-paper"],
        "case_report": ["search-lit", "write-paper", "self-review", "check-reporting", "find-journal"]
    }
    
    def __init__(self):
        self._load_integration_status()
    
    def _load_integration_status(self):
        """Load integration status from existing integration files"""
        integrated_skills = []
        
        # Check which skills have been integrated
        for skill_name, skill_info in self.SKILLS.items():
            integration_file = os.path.join(INTEGRATION_PATH, f"{skill_name.replace('-', '_')}.py")
            if os.path.exists(integration_file):
                skill_info.integration_status = "integrated"
                integrated_skills.append(skill_name)
    
    def list_all(self) -> List[str]:
        """Return list of all skill names"""
        return list(self.SKILLS.keys())
    
    def list_integrated(self) -> List[str]:
        """Return list of integrated skill names"""
        return [k for k, v in self.SKILLS.items() if v.integration_status == "integrated"]
    
    def list_by_category(self, category: str) -> List[str]:
        """Return skills in a category"""
        return self.SKILL_CATEGORIES.get(category, [])
    
    def get_skill_info(self, skill_name: str) -> Optional[SkillInfo]:
        """Get full info for a skill"""
        return self.SKILLS.get(skill_name)
    
    def get_skill_path(self, skill_name: str) -> Optional[str]:
        """Get the filesystem path for a skill"""
        skill = self.SKILLS.get(skill_name)
        return skill.skill_dir if skill else None
    
    def get_dependencies(self, skill_name: str) -> List[str]:
        """Get dependencies for a skill"""
        skill = self.SKILLS.get(skill_name)
        return skill.dependencies if skill else []
    
    def get_reporting_guidelines(self) -> List[str]:
        """Get all supported reporting guidelines from check-reporting"""
        check_skill = self.SKILLS.get("check-reporting")
        if check_skill and check_skill.reporting_guideline:
            return [rg.strip() for rg in check_skill.reporting_guideline.split(",")]
        return []
    
    def get_workflow(self, workflow_name: str) -> List[str]:
        """Get the skill sequence for a workflow"""
        return self.WORKFLOWS.get(workflow_name, [])
    
    def get_category_for_skill(self, skill_name: str) -> Optional[str]:
        """Get the category containing a skill"""
        for category, skills in self.SKILL_CATEGORIES.items():
            if skill_name in skills:
                return category
        return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of all skills"""
        summary = {
            "total_skills": len(self.SKILLS),
            "integrated": len(self.list_integrated()),
            "by_category": {},
            "by_status": {},
            "reporting_guidelines": self.get_reporting_guidelines(),
            "available_workflows": list(self.WORKFLOWS.keys())
        }
        
        for category, skills in self.SKILL_CATEGORIES.items():
            summary["by_category"][category] = len(skills)
        
        for skill_name, skill_info in self.SKILLS.items():
            status = skill_info.integration_status
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        return summary
    
    def print_summary(self):
        """Print a formatted summary of all skills"""
        summary = self.get_summary()
        
        print("=" * 70)
        print("MEDSCI-SKILLS REGISTRY SUMMARY (ARP v24 Integration)")
        print("=" * 70)
        print(f"Total Skills: {summary['total_skills']}")
        print(f"Integrated:   {summary['integrated']}")
        print(f"\nBy Status:")
        for status, count in summary["by_status"].items():
            print(f"  {status}: {count}")
        
        print(f"\nBy Category:")
        for category, count in summary["by_category"].items():
            print(f"  {category}: {count}")
        
        print(f"\nReporting Guidelines ({len(summary['reporting_guidelines'])}):")
        print(f"  {', '.join(summary['reporting_guidelines'][:10])}...")
        
        print(f"\nAvailable Workflows:")
        for workflow, skills in self.WORKFLOWS.items():
            print(f"  {workflow}: {' -> '.join(skills)}")


def med_sci_registry_example():
    """Example usage of the MedSci registry"""
    registry = MedSciRegistry()
    
    # Print summary
    registry.print_summary()
    
    # Get info for specific skill
    print("\n" + "=" * 70)
    print("Example: write-paper skill info")
    print("=" * 70)
    info = registry.get_skill_info("write-paper")
    if info:
        print(f"Name: {info.name}")
        print(f"Purpose: {info.purpose}")
        print(f"ARP Use Case: {info.arp_use_case}")
        print(f"Dependencies: {info.dependencies}")
        print(f"API Class: {info.api_class}")
    
    # Show workflow
    print("\n" + "=" * 70)
    print("Example: data_to_manuscript workflow")
    print("=" * 70)
    workflow = registry.get_workflow("data_to_manuscript")
    print(" -> ".join(workflow))
    
    return registry


if __name__ == "__main__":
    med_sci_registry_example()
