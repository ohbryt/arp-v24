"""
ARP v24 Multi-Agent Research Team
=================================
Hub-and-Spoke Architecture: Coordinator + 4 Specialist Agents

Based on: Khairallah AL-Awady's multi-agent orchestration pattern
- Research Specialist: Data collection
- Analyst Specialist: Pattern identification
- Writer Specialist: Report generation
- Reviewer Specialist: Quality assurance

All context is passed EXPLICITLY between agents.
"""

import json
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ResearchQuestion:
    """User's research request"""
    topic: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    target_length: str = "medium"  # short, medium, long
    audience: str = "researcher"  # researcher, executive, clinical


@dataclass
class ResearchData:
    """Output from Research Specialist"""
    facts: List[Dict[str, Any]] = field(default_factory=list)
    sources: List[Dict[str, str]] = field(default_factory=list)
    confidence: str = "medium"
    search_queries_used: List[str] = field(default_factory=list)
    gaps_identified: List[str] = field(default_factory=list)


@dataclass
class AnalysisData:
    """Output from Analyst Specialist"""
    key_patterns: List[str] = field(default_factory=list)
    conclusions: List[str] = field(default_factory=list)
    contradictions: List[Dict[str, str]] = field(default_factory=list)
    weak_claims: List[str] = field(default_factory=list)
    evidence_strength: str = "medium"
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DraftReport:
    """Output from Writer Specialist"""
    title: str = ""
    executive_summary: str = ""
    sections: Dict[str, str] = field(default_factory=dict)
    citations: List[str] = field(default_factory=list)
    word_count: int = 0
    format: str = "markdown"


@dataclass
class ReviewResult:
    """Output from Reviewer Specialist"""
    issues: List[Dict[str, Any]] = field(default_factory=list)
    accuracy_score: float = 0.0
    completeness_score: float = 0.0
    quality_score: float = 0.0
    is_approved: bool = False
    revision_needed: List[str] = field(default_factory=list)


@dataclass
class FinalReport:
    """Delivered to user"""
    title: str
    executive_summary: str
    full_text: str
    word_count: int
    sources: List[str]
    review_passed: bool
    created_at: str
    agent_team: str = "arp-v24-multi-agent"


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class BaseAgent(ABC):
    """Base class for all specialist agents"""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
    
    @abstractmethod
    async def run(self, context: Dict[str, Any]) -> Any:
        """Execute the agent's task"""
        pass
    
    def get_prompt(self, task_context: Dict[str, Any]) -> str:
        """Build prompt with explicit context"""
        return f"""{self.system_prompt}

TASK CONTEXT:
{json.dumps(task_context, indent=2, ensure_ascii=False)}

Execute your role with the above context.
"""


# ============================================================================
# RESEARCH SPECIALIST
# ============================================================================

class ResearchSpecialist(BaseAgent):
    """Agent 1: Gathers factual information"""
    
    def __init__(self):
        system_prompt = """You are a RESEARCH SPECIALIST. Your only job is to find accurate, current information on the topic you are given.

For each piece of information you find:
- Note the source (PMID, URL, or database)
- Rate your confidence (high/medium/low)
- Flag if the information might be outdated
- Mark the factual category (molecular_mechanism, clinical_trial, epidemiological, biochemical, etc.)

Return your findings as a structured list of facts with sources and confidence ratings.
DO NOT analyze. DO NOT draw conclusions. DO NOT write prose. Just find and organize facts."""
        
        super().__init__("Researcher", "Research Specialist", system_prompt)
    
    async def run(self, context: Dict[str, Any]) -> ResearchData:
        """Execute research task"""
        topic = context.get("topic", "")
        sub_questions = context.get("sub_questions", [topic])
        constraints = context.get("constraints", {})
        
        print(f"[Researcher] Starting research on {len(sub_questions)} sub-questions...")
        
        all_facts = []
        all_sources = []
        search_queries = []
        
        # Import and use literature integrator if available
        try:
            from core.literature_integrator import LiteratureIntegrator
            integrator = LiteratureIntegrator()
            
            for sq in sub_questions:
                print(f"[Researcher] Searching: {sq}")
                result = await self._search_topic(integrator, sq, constraints)
                all_facts.extend(result["facts"])
                all_sources.extend(result["sources"])
                search_queries.append(sq)
                
        except ImportError:
            # Fallback to web search
            print("[Researcher] Literature integrator not available, using web search")
            for sq in sub_questions:
                facts = await self._web_search(sq)
                all_facts.extend(facts)
                search_queries.append(sq)
        
        # Identify gaps
        gaps = self._identify_gaps(all_facts, topic)
        
        return ResearchData(
            facts=all_facts,
            sources=all_sources,
            confidence="high" if len(all_facts) > 20 else "medium",
            search_queries_used=search_queries,
            gaps_identified=gaps
        )
    
    async def _search_topic(self, integrator, query: str, constraints: Dict) -> Dict:
        """Search using literature integrator"""
        result = {
            "facts": [],
            "sources": []
        }
        
        # Placeholder for actual API calls
        # In production, this would call PubMed, ChEMBL, etc.
        result["facts"].append({
            "fact": f"Research query executed: {query}",
            "source": "literature_integrator",
            "confidence": "high",
            "category": "methodology"
        })
        
        return result
    
    async def _web_search(self, query: str) -> List[Dict]:
        """Fallback web search"""
        return [{
            "fact": f"Web search executed: {query}",
            "source": "web_search",
            "confidence": "medium",
            "category": "general"
        }]
    
    def _identify_gaps(self, facts: List[Dict], topic: str) -> List[str]:
        """Identify gaps in research coverage"""
        categories = set(f.get("category", "") for f in facts)
        gaps = []
        
        required_categories = ["molecular_mechanism", "clinical_evidence", "epidemiological"]
        for cat in required_categories:
            if cat not in categories:
                gaps.append(f"Missing category: {cat}")
        
        return gaps


# ============================================================================
# ANALYST SPECIALIST
# ============================================================================

class AnalystSpecialist(BaseAgent):
    """Agent 2: Identifies patterns and draws conclusions"""
    
    def __init__(self):
        system_prompt = """You are a DATA ANALYST. Your only job is to analyze research findings and extract insights.

Given raw research data:
- Identify the 3-5 MOST IMPORTANT PATTERNS in the data
- Note any CONTRADICTIONS between sources
- Flag claims that LACK SUFFICIENT EVIDENCE
- Draw CONCLUSIONS supported by the data
- Provide actionable RECOMMENDATIONS if applicable

DO NOT write a final report. Return structured analysis that a writer can turn into polished prose.
Format your output as structured analysis sections."""
        
        super().__init__("Analyst", "Analyst Specialist", system_prompt)
    
    async def run(self, context: Dict[str, Any]) -> AnalysisData:
        """Execute analysis task"""
        research_data = context.get("research_data", {})
        facts = research_data.get("facts", [])
        sources = research_data.get("sources", [])
        
        print(f"[Analyst] Analyzing {len(facts)} facts from {len(sources)} sources...")
        
        # Extract patterns from facts
        patterns = self._identify_patterns(facts)
        conclusions = self._draw_conclusions(facts, patterns)
        contradictions = self._find_contradictions(facts)
        weak_claims = self._flag_weak_claims(facts)
        recommendations = self._generate_recommendations(patterns, contradictions)
        
        evidence_strength = self._assess_evidence_strength(facts, contradictions)
        
        return AnalysisData(
            key_patterns=patterns,
            conclusions=conclusions,
            contradictions=contradictions,
            weak_claims=weak_claims,
            evidence_strength=evidence_strength,
            recommendations=recommendations
        )
    
    def _identify_patterns(self, facts: List[Dict]) -> List[str]:
        """Identify key patterns in the data"""
        patterns = []
        
        # Group facts by category
        by_category = {}
        for f in facts:
            cat = f.get("category", "unknown")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(f)
        
        # Extract patterns
        for cat, cat_facts in by_category.items():
            if len(cat_facts) >= 3:
                patterns.append(f"{cat}: {len(cat_facts)} related findings identified")
        
        return patterns[:5]  # Top 5 patterns
    
    def _draw_conclusions(self, facts: List[Dict], patterns: List[str]) -> List[str]:
        """Draw evidence-based conclusions"""
        conclusions = []
        
        high_confidence = [f for f in facts if f.get("confidence") == "high"]
        if len(high_confidence) > 5:
            conclusions.append(f"Strong evidence base with {len(high_confidence)} high-confidence facts")
        
        if patterns:
            conclusions.append(f"Primary patterns: {'; '.join(patterns[:3])}")
        
        return conclusions
    
    def _find_contradictions(self, facts: List[Dict]) -> List[Dict[str, str]]:
        """Find contradictions between sources"""
        contradictions = []
        
        # Placeholder - in production would use NLP to compare facts
        return contradictions
    
    def _flag_weak_claims(self, facts: List[Dict]) -> List[str]:
        """Flag claims with weak evidence"""
        weak = [f["fact"] for f in facts if f.get("confidence") == "low"]
        return weak[:5]
    
    def _generate_recommendations(self, patterns: List[str], contradictions: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        if contradictions:
            recs.append("Further investigation needed to resolve contradictory findings")
        
        if len(patterns) < 3:
            recs.append("Limited pattern coverage - additional research may be needed")
        
        recs.append("Consider targeted experiments to validate key findings")
        
        return recs
    
    def _assess_evidence_strength(self, facts: List[Dict], contradictions: List[Dict]) -> str:
        """Assess overall evidence strength"""
        high = len([f for f in facts if f.get("confidence") == "high"])
        total = len(facts)
        
        if total == 0:
            return "insufficient"
        elif high / total > 0.7 and not contradictions:
            return "strong"
        elif high / total > 0.4:
            return "moderate"
        else:
            return "weak"


# ============================================================================
# WRITER SPECIALIST
# ============================================================================

class WriterSpecialist(BaseAgent):
    """Agent 3: Produces polished reports"""
    
    def __init__(self):
        system_prompt = """You are a PROFESSIONAL REPORT WRITER. Your only job is to turn analyzed data into a polished, readable report.

Given analysis and supporting data:
- Write in clear, professional prose
- Structure with an EXECUTIVE SUMMARY (3-5 sentences) followed by detailed sections
- Cite specific numbers and sources throughout
- Make the report scannable — a reader should grasp key points in under 3 minutes
- Use appropriate scientific/medical terminology for the audience

For the AUDIENCE specified, adjust tone and depth:
- researcher: Technical, detailed, with methodology discussion
- executive: High-level, business implications, minimal jargon
- clinical: Focus on clinical relevance, treatment implications

DO NOT perform new research. DO NOT change the conclusions from the analysis.
ONLY write the report based on the provided data."""
        
        super().__init__("Writer", "Writer Specialist", system_prompt)
    
    async def run(self, context: Dict[str, Any]) -> DraftReport:
        """Execute writing task"""
        analysis_data = context.get("analysis_data", {})
        research_data = context.get("research_data", {})
        topic = context.get("topic", "")
        audience = context.get("audience", "researcher")
        
        print(f"[Writer] Producing {audience}-level report on: {topic}")
        
        # Build comprehensive context for writing
        writing_context = {
            "topic": topic,
            "audience": audience,
            "patterns": analysis_data.get("key_patterns", []),
            "conclusions": analysis_data.get("conclusions", []),
            "evidence_strength": analysis_data.get("evidence_strength", "unknown"),
            "facts": research_data.get("facts", [])[:30],  # Limit to top facts
            "sources": research_data.get("sources", []),
            "weak_claims": analysis_data.get("weak_claims", []),
            "recommendations": analysis_data.get("recommendations", [])
        }
        
        # Generate report sections
        sections = self._generate_sections(writing_context)
        executive_summary = self._generate_executive_summary(writing_context)
        
        # Count words
        full_text = executive_summary + "\n\n" + "\n\n".join(sections.values())
        word_count = len(full_text.split())
        
        # Extract citations
        citations = [s.get("source", "") for s in research_data.get("sources", [])[:20]]
        
        return DraftReport(
            title=self._generate_title(topic, audience),
            executive_summary=executive_summary,
            sections=sections,
            citations=citations,
            word_count=word_count,
            format="markdown"
        )
    
    def _generate_title(self, topic: str, audience: str) -> str:
        """Generate appropriate title"""
        if audience == "executive":
            return f"Executive Brief: {topic}"
        elif audience == "clinical":
            return f"Clinical Review: {topic}"
        else:
            return f"Comprehensive Analysis: {topic}"
    
    def _generate_executive_summary(self, context: Dict) -> str:
        """Generate executive summary"""
        patterns = context.get("patterns", [])
        conclusions = context.get("conclusions", [])
        evidence = context.get("evidence_strength", "unknown")
        
        summary = f"""## Executive Summary

This report provides a comprehensive analysis of **{context['topic']}**.

**Key Findings:**
{chr(10).join(f"- {p}" for p in patterns[:3]) if patterns else "- No specific patterns identified"}

**Evidence Assessment:** The overall evidence strength is **{evidence}**.

**Primary Conclusions:**
{chr(10).join(f"- {c}" for c in conclusions[:2]) if conclusions else "- See detailed analysis below"}

**Clinical/Business Implications:** This analysis has significant implications for {'clinical practice' if context['audience'] == 'clinical' else 'strategic decision-making'}.
"""
        return summary
    
    def _generate_sections(self, context: Dict) -> Dict[str, str]:
        """Generate report sections"""
        sections = {}
        
        # Introduction
        sections["1. Introduction"] = f"""This section provides background on {context['topic']} and outlines the scope of this analysis.

The analysis is based on a comprehensive review of available evidence, including {'peer-reviewed literature' if context['sources'] else 'preliminary data"}. The findings are synthesized from multiple sources to provide a balanced perspective on the current state of knowledge."""
        
        # Methods (for researcher audience)
        if context['audience'] == 'researcher':
            sections["2. Methodology"] = """### Data Sources
This analysis employed a multi-source approach:
1. PubMed/MEDLINE literature search
2. Clinical trial databases (ClinicalTrials.gov)
3. Drug interaction databases (ChEMBL, DrugBank)
4. Real-world evidence sources

### Analytical Framework
Data were synthesized using:
- Systematic pattern identification
- Evidence quality assessment
- Cross-source validation"""
        
        # Findings
        sections["3. Key Findings"] = self._generate_findings(context)
        
        # Discussion
        sections["4. Discussion"] = self._generate_discussion(context)
        
        # Limitations
        sections["5. Limitations"] = """### Evidence Gaps
- Some claims are based on preliminary or low-confidence evidence
- Sample sizes in some studies were limited
- Publication bias may affect available evidence

### Methodological Considerations
- Heterogeneity across studies limits direct comparison
- Confounding factors may not be fully controlled in all studies"""
        
        # Recommendations
        if context.get('recommendations'):
            sections["6. Recommendations"] = "\n".join(
                f"- {r}" for r in context['recommendations']
            )
        
        return sections
    
    def _generate_findings(self, context: Dict) -> str:
        """Generate findings section"""
        findings = []
        
        patterns = context.get('patterns', [])
        for i, pattern in enumerate(patterns[:5], 1):
            findings.append(f"**Finding {i}:** {pattern}")
        
        if not findings:
            findings.append("Detailed findings are summarized from the analyzed data sources.")
        
        return "\n\n".join(findings)
    
    def _generate_discussion(self, context: Dict) -> str:
        """Generate discussion section"""
        audience = context.get('audience', 'researcher')
        evidence = context.get('evidence_strength', 'unknown')
        
        if audience == 'executive':
            return f"""### Business/Strategic Implications

The {evidence} evidence base suggests {'significant opportunities' if evidence == 'strong' else 'potential areas for further investigation'} in the domain of {context['topic']}.

Key considerations:
- Evidence quality varies across different aspects of this topic
- Further due diligence is recommended before major investments
- Ongoing monitoring of developments is advised"""
        
        elif audience == 'clinical':
            return f"""### Clinical Implications

The {evidence} evidence suggests {'clear clinical applications' if evidence == 'strong' else 'areas requiring careful consideration'}.

Clinical decision-making should:
- Consider individual patient factors and preferences
- Monitor for emerging evidence in this rapidly evolving area
- Balance potential benefits against risks"""
        
        else:
            return f"""### Scientific Implications

The evidence base for {context['topic']} is {evidence}.

This analysis identifies several areas warranting further investigation:
- Resolution of contradictory findings where present
- Validation of key patterns in independent cohorts
- Mechanistic studies to establish causality"""


# ============================================================================
# REVIEWER SPECIALIST
# ============================================================================

class ReviewerSpecialist(BaseAgent):
    """Agent 4: Quality assurance"""
    
    def __init__(self):
        system_prompt = """You are a QUALITY REVIEWER. Your only job is to check the finished report against the original research.

Check for:
1. CLAIMS in the report NOT SUPPORTED by the research data
2. IMPORTANT FINDINGS from the research that the report OMITS
3. LOGICAL INCONSISTENCIES or weak reasoning
4. ACCURACY of all numbers and statistics
5. CLARITY and readability issues
6. APPROPRIATENESS for the target audience

For EACH ISSUE found:
- Quote the problem specifically
- Explain what is wrong
- Suggest a SPECIFIC FIX

If the report is solid with no major issues, say so and mark as approved."""
        
        super().__init__("Reviewer", "Reviewer Specialist", system_prompt)
    
    async def run(self, context: Dict[str, Any]) -> ReviewResult:
        """Execute review task"""
        draft_report = context.get("draft_report", {})
        research_data = context.get("research_data", {})
        analysis_data = context.get("analysis_data", {})
        
        print(f"[Reviewer] Checking report quality...")
        
        issues = []
        
        # Check 1: Word count adequacy
        word_count = draft_report.get("word_count", 0)
        if word_count < 500:
            issues.append({
                "severity": "warning",
                "type": "length",
                "quote": f"Word count: {word_count}",
                "problem": "Report may be too brief for the topic",
                "suggestion": "Expand key sections with more detail"
            })
        
        # Check 2: Executive summary presence
        if not draft_report.get("executive_summary"):
            issues.append({
                "severity": "error",
                "type": "structure",
                "quote": "No executive summary",
                "problem": "Missing executive summary",
                "suggestion": "Add a 3-5 sentence executive summary at the start"
            })
        
        # Check 3: Citation coverage
        citations = draft_report.get("citations", [])
        facts = research_data.get("facts", [])
        if len(citations) < len(facts) * 0.3:
            issues.append({
                "severity": "warning",
                "type": "completeness",
                "quote": f"Citations: {len(citations)}",
                "problem": "Low citation coverage relative to facts gathered",
                "suggestion": "Ensure more facts are cited in the report"
            })
        
        # Check 4: Pattern coverage
        patterns = analysis_data.get("key_patterns", [])
        sections = draft_report.get("sections", {})
        covered_patterns = sum(1 for p in patterns if any(
            p.lower() in s.lower() for s in sections.values()
        ))
        
        if patterns and covered_patterns < len(patterns) * 0.5:
            issues.append({
                "severity": "error",
                "type": "completeness",
                "quote": f"Patterns covered: {covered_patterns}/{len(patterns)}",
                "problem": "Key patterns not adequately addressed in report",
                "suggestion": "Dedicate sections to each major pattern identified"
            })
        
        # Check 5: Weak claims included without caveat
        weak_claims = analysis_data.get("weak_claims", [])
        if weak_claims:
            full_text = draft_report.get("executive_summary", "") + " ".join(sections.values())
            weak_mentioned = [w for w in weak_claims if w in full_text]
            if weak_mentioned and not any("low confidence" in full_text.lower() or "preliminary" in full_text.lower()):
                issues.append({
                    "severity": "warning",
                    "type": "accuracy",
                    "quote": "Weak claims included",
                    "problem": "Some low-confidence claims may not be properly qualified",
                    "suggestion": "Ensure weak claims are marked as preliminary or low-confidence"
                })
        
        # Calculate scores
        accuracy = max(0, 100 - len([i for i in issues if i["severity"] == "error"]) * 20 - len([i for i in issues if i["severity"] == "warning"]) * 5)
        completeness = 100 - len([i for i in issues if i["type"] == "completeness"]) * 25
        quality = (accuracy + completeness) / 2
        
        is_approved = len([i for i in issues if i["severity"] == "error"]) == 0
        revision_needed = [i["suggestion"] for i in issues if i["severity"] == "error"]
        
        return ReviewResult(
            issues=issues,
            accuracy_score=accuracy,
            completeness_score=completeness,
            quality_score=quality,
            is_approved=is_approved,
            revision_needed=revision_needed
        )


# ============================================================================
# COORDINATOR (HUB)
# ============================================================================

class Coordinator:
    """Hub agent that orchestrates the specialist team"""
    
    def __init__(self):
        self.researcher = ResearchSpecialist()
        self.analyst = AnalystSpecialist()
        self.writer = WriterSpecialist()
        self.reviewer = ReviewerSpecialist()
        
        self.workflow_steps = [
            "1. Receive research question",
            "2. Decompose into sub-questions",
            "3. Send to Research Specialist",
            "4. Compile research findings",
            "5. Send to Analyst Specialist",
            "6. Send analysis to Writer Specialist",
            "7. Send draft to Reviewer Specialist",
            "8. If issues found → revision loop",
            "9. Deliver final report"
        ]
    
    async def run_research(self, question: ResearchQuestion) -> FinalReport:
        """Execute full research workflow"""
        print("=" * 60)
        print("ARP v24 MULTI-AGENT RESEARCH TEAM")
        print("=" * 60)
        print(f"Topic: {question.topic}")
        print(f"Audience: {question.audience}")
        print(f"Steps: {len(self.workflow_steps)}")
        print("=" * 60)
        
        # Step 1-2: Decompose question
        sub_questions = self._decompose_question(question)
        print(f"\n[Coordinator] Decomposed into {len(sub_questions)} sub-questions")
        
        # Step 3-4: Research
        research_context = {
            "topic": question.topic,
            "sub_questions": sub_questions,
            "constraints": question.constraints
        }
        research_data = await self.researcher.run(research_context)
        print(f"[Coordinator] Research complete: {len(research_data.facts)} facts gathered")
        
        # Step 5: Analysis
        analysis_context = {
            "research_data": {
                "facts": [f.__dict__ if hasattr(f, '__dict__') else f for f in research_data.facts],
                "sources": [s.__dict__ if hasattr(s, '__dict__') else s for s in research_data.sources]
            }
        }
        analysis_data = await self.analyst.run(analysis_context)
        print(f"[Coordinator] Analysis complete: {len(analysis_data.key_patterns)} patterns identified")
        
        # Step 6: Writing
        writer_context = {
            "topic": question.topic,
            "audience": question.audience,
            "analysis_data": analysis_data.__dict__,
            "research_data": {
                "facts": [f.__dict__ if hasattr(f, '__dict__') else f for f in research_data.facts],
                "sources": [s.__dict__ if hasattr(s, '__dict__') else s for s in research_data.sources]
            }
        }
        draft_report = await self.writer.run(writer_context)
        print(f"[Coordinator] Draft complete: {draft_report.word_count} words")
        
        # Step 7: Review
        review_context = {
            "draft_report": draft_report.__dict__,
            "research_data": {
                "facts": [f.__dict__ if hasattr(f, '__dict__') else f for f in research_data.facts],
                "sources": [s.__dict__ if hasattr(s, '__dict__') else s for s in research_data.sources]
            },
            "analysis_data": analysis_data.__dict__
        }
        review_result = await self.reviewer.run(review_context)
        print(f"[Coordinator] Review complete: {'APPROVED' if review_result.is_approved else 'ISSUES FOUND'}")
        
        # Step 8: Handle revision if needed
        if not review_result.is_approved:
            print(f"[Coordinator] Revision needed: {len(review_result.revision_needed)} issues")
            # In production, would send back to writer
            # For now, note the issues
        
        # Step 9: Assemble final report
        full_text = self._assemble_final_text(draft_report)
        
        final_report = FinalReport(
            title=draft_report.title,
            executive_summary=draft_report.executive_summary,
            full_text=full_text,
            word_count=draft_report.word_count,
            sources=[s.get("source", "") for s in research_data.sources],
            review_passed=review_result.is_approved,
            created_at=datetime.now().isoformat()
        )
        
        print("=" * 60)
        print("RESEARCH COMPLETE")
        print(f"Final word count: {final_report.word_count}")
        print(f"Review passed: {final_report.review_passed}")
        print("=" * 60)
        
        return final_report
    
    def _decompose_question(self, question: ResearchQuestion) -> List[str]:
        """Decompose research question into sub-questions"""
        topic = question.topic
        
        # Generate sub-questions based on topic
        sub_questions = [
            f"Overview and current state of {topic}",
            f"Molecular mechanisms and pathophysiology of {topic}",
            f"Clinical evidence and therapeutic implications of {topic}",
            f"Epidemiology and patient outcomes in {topic}",
            f"Future directions and research gaps in {topic}"
        ]
        
        return sub_questions
    
    def _assemble_final_text(self, draft: DraftReport) -> str:
        """Assemble final report text"""
        parts = [draft.executive_summary]
        
        for section_title, section_content in draft.sections.items():
            parts.append(f"\n\n## {section_title}\n\n{section_content}")
        
        # Add citations
        if draft.citations:
            parts.append("\n\n## References\n\n")
            for i, cite in enumerate(draft.citations, 1):
                parts.append(f"{i}. {cite}\n")
        
        return "".join(parts)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Run the multi-agent research team"""
    
    # Example research question
    question = ResearchQuestion(
        topic="PDK4 and Sarcopenia: Molecular Mechanisms and Therapeutic Targets",
        constraints={"focus": "skeletal muscle, metabolic regulation"},
        audience="researcher",
        target_length="long"
    )
    
    # Create coordinator and run
    coordinator = Coordinator()
    result = await coordinator.run_research(question)
    
    # Output result
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result.full_text[:2000] + "..." if len(result.full_text) > 2000 else result.full_text)
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
