"""
ARP v24 - Loop-Think Recurrent Reasoning Integration

Loop-Think: Recurrent-depth transformers for multi-hop compositional reasoning.
Paper: https://github.com/OSU-NLP-Group/Loop-Think-Generalize

Key concepts:
- Recurrent-depth transformers (RDT) = iterative computation over same layers
- Systematic generalization = combine unseen knowledge combinations
- Recursion extrapolation = scale inference-time recurrence for deeper reasoning
- Three-stage grokking: memorization → ID generalization → systematic generalization

Integration with ARP:
- Multi-hop target-disease pathway reasoning
- Drug mechanism chain reasoning (target → pathway → disease)
- Hypothesis generation with iterative refinement
- "Overthinking" mitigation via adaptive halting
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from enum import Enum
import time


class RecurrenceType(Enum):
    """Inference recurrence types from Loop-Think."""
    FIXED = "fixed"           # Fixed recurrence steps
    DYNAMIC = "dynamic"       # Adaptive based on difficulty
    ADAPTIVE = "adaptive"     # Halting when confidence met


@dataclass
class ReasoningState:
    """Current state of multi-hop reasoning."""
    hop: int
    max_hops: int
    entities: List[str]          # Current entity chain
    relations: List[str]        # Current relation chain
    confidence: float           # 0-1 confidence score
    is_complete: bool = False
    reasoning_trace: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hop": self.hop,
            "max_hops": self.max_hops,
            "entities": self.entities,
            "relations": self.relations,
            "confidence": self.confidence,
            "is_complete": self.is_complete,
            "trace_length": len(self.reasoning_trace),
        }


@dataclass
class ReasoningResult:
    """Complete multi-hop reasoning result."""
    query: str
    answer: str
    hops: int
    total_steps: int           # Total recurrence steps used
    reasoning_chain: List[Dict[str, Any]]
    confidence: float
    is_systematic: bool        # Used unseen knowledge combination
    execution_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "answer": self.answer,
            "hops": self.hops,
            "total_steps": self.total_steps,
            "reasoning_chain": self.reasoning_chain,
            "confidence": self.confidence,
            "is_systematic": self.is_systematic,
            "execution_time": round(self.execution_time, 3),
        }


class RecurrentReasoner:
    """
    Loop-Think inspired recurrent reasoning for ARP.
    
    Uses iterative computation (recurrence) to achieve:
    - Systematic generalization: combine knowledge in new ways
    - Recursion extrapolation: extend to deeper reasoning chains
    
    Key features:
    - Configurable recurrence depth
    - Adaptive halting to prevent overthinking
    - Reasoning trace for interpretability
    """
    
    def __init__(
        self,
        max_hops: int = 5,
        recurrence: int = 3,
        recurrence_type: RecurrenceType = RecurrenceType.FIXED,
        min_confidence: float = 0.8,
        max_overthinking_hops: int = 10,
    ):
        self.max_hops = max_hops
        self.recurrence = recurrence
        self.recurrence_type = recurrence_type
        self.min_confidence = min_confidence
        self.max_overthinking_hops = max_overthinking_hops
        
        # Internal state
        self.current_state: Optional[ReasoningState] = None
        self.reasoning_history: List[ReasoningResult] = []
        
    def reset(self):
        """Reset internal state."""
        self.current_state = None
        self.reasoning_history = []
    
    def reason(
        self,
        query: str,
        knowledge_graph: Dict[str, List[Dict]],
        context: Optional[Dict[str, Any]] = None,
    ) -> ReasoningResult:
        """
        Perform multi-hop reasoning using recurrent computation.
        
        Args:
            query: Reasoning query (e.g., "PHGDH → ? → cancer")
            knowledge_graph: Dict of entity → [{relation, target, confidence}]
            context: Additional context (disease, tissue, etc.)
            
        Returns:
            ReasoningResult with answer and trace
        """
        start_time = time.time()
        self.reset()
        
        # Parse query to extract entities and hops
        entities, target_hops = self._parse_query(query)
        
        # Initialize state
        self.current_state = ReasoningState(
            hop=0,
            max_hops=target_hops,
            entities=entities,
            relations=[],
            confidence=0.0,
            is_complete=False,
            reasoning_trace=[],
        )
        
        # Recurrent reasoning loop
        total_steps = 0
        chain = []
        
        while not self.current_state.is_complete and total_steps < self.max_overthinking_hops:
            # Single recurrence step
            step_result = self._single_reasoning_step(knowledge_graph, context)
            
            chain.append(step_result)
            total_steps += 1
            
            # Update state
            self.current_state.hop = step_result["hop"]
            self.current_state.entities.append(step_result["next_entity"])
            self.current_state.relations.append(step_result["relation"])
            self.current_state.confidence = step_result["confidence"]
            
            # Check completion
            self.current_state.is_complete = (
                step_result["is_terminal"] or
                step_result["hop"] >= self.current_state.max_hops
            )
            
            # Adaptive halting (prevent overthinking)
            if self.recurrence_type == RecurrenceType.ADAPTIVE:
                if step_result["confidence"] >= self.min_confidence and step_result["is_terminal"]:
                    self.current_state.is_complete = True
        
        # Determine if systematic (used unseen combination)
        is_systematic = self._check_systematicity(chain, knowledge_graph)
        
        # Build answer
        answer = self._build_answer(chain)
        
        return ReasoningResult(
            query=query,
            answer=answer,
            hops=self.current_state.hop,
            total_steps=total_steps,
            reasoning_chain=chain,
            confidence=self.current_state.confidence,
            is_systematic=is_systematic,
            execution_time=time.time() - start_time,
        )
    
    def _parse_query(self, query: str) -> tuple:
        """Parse query to extract entities and target hops."""
        # Simple parsing: "A → B → C" format
        if "→" in query:
            entities = [e.strip() for e in query.split("→")]
        elif "->" in query:
            entities = [e.strip() for e in query.split("->")]
        elif "|" in query:
            entities = [e.strip() for e in query.split("|")]
        else:
            entities = [query.strip()]
        
        target_hops = len(entities) - 1 if len(entities) > 1 else self.max_hops
        return entities[:1], target_hops  # Start with first entity
    
    def _single_reasoning_step(
        self,
        knowledge_graph: Dict[str, List[Dict]],
        context: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Single step of recurrent reasoning."""
        current_entity = self.current_state.entities[-1]
        
        # Get possible transitions
        transitions = knowledge_graph.get(current_entity, [])
        
        if not transitions:
            return {
                "hop": self.current_state.hop + 1,
                "next_entity": None,
                "relation": None,
                "confidence": 0.0,
                "is_terminal": True,
                "reasoning": "No transitions found",
            }
        
        # Score transitions (simplified - would use embeddings in real impl)
        scored_transitions = []
        for t in transitions:
            score = t.get("confidence", 0.5)
            # Context boosting
            if context:
                if t.get("disease") == context.get("disease"):
                    score *= 1.2
                if t.get("tissue") == context.get("tissue"):
                    score *= 1.1
            scored_transitions.append((t, score))
        
        # Select best transition
        best = max(scored_transitions, key=lambda x: x[1])
        transition, score = best
        
        return {
            "hop": self.current_state.hop + 1,
            "next_entity": transition["target"],
            "relation": transition.get("relation", "unknown"),
            "confidence": score,
            "is_terminal": transition.get("is_terminal", False),
            "reasoning": transition.get("mechanism", ""),
        }
    
    def _check_systematicity(
        self,
        chain: List[Dict],
        knowledge_graph: Dict[str, List[Dict]],
    ) -> bool:
        """Check if reasoning used unseen (systematic) knowledge combination."""
        # Simplified: check if any hop combination was rare in training
        # Real implementation would compare to training distribution
        return len(chain) >= 3  # Multi-hop is typically systematic
    
    def _build_answer(self, chain: List[Dict]) -> str:
        """Build natural language answer from chain."""
        if not chain:
            return "No reasoning chain built"
        
        parts = []
        for step in chain:
            if step["relation"] and step["next_entity"]:
                parts.append(f"{step['relation']} → {step['next_entity']}")
        
        return " → ".join(parts) if parts else "Incomplete reasoning"


class MultiHopDiseaseReasoner:
    """
    High-level disease reasoning using recurrent computation.
    
    Example queries:
    - "PHGDH → serine → TNBC → dependency"
    - "MTHFD2 → NADPH → hypoxia → cancer"
    - "SHMT2 → glycine → lymphoma → epigenetic"
    """
    
    def __init__(self, config: Optional[Dict] = None):
        config = config or {}
        self.max_hops = config.get("max_hops", 5)
        self.recurrence = config.get("recurrence", 3)
        self.recurrence_type = RecurrenceType[
            config.get("recurrence_type", "FIXED").upper()
        ]
        
        self.reasoner = RecurrentReasoner(
            max_hops=self.max_hops,
            recurrence=self.recurrence,
            recurrence_type=self.recurrence_type,
        )
        
        # Build default knowledge graph
        self.knowledge_graph = self._build_default_graph()
    
    def _build_default_graph(self) -> Dict[str, List[Dict]]:
        """Build default OCM knowledge graph."""
        return {
            # PHGDH pathway
            "PHGDH": [
                {"target": "serine", "relation": "biosynthesizes", "confidence": 0.95, "is_terminal": False},
                {"target": "SAM", "relation": "supports", "confidence": 0.85, "is_terminal": False},
            ],
            "serine": [
                {"target": "SHMT2", "relation": "converted_by", "confidence": 0.90, "is_terminal": False},
                {"target": "glycine", "relation": "becomes", "confidence": 0.95, "is_terminal": False},
            ],
            "SHMT2": [
                {"target": "mitochondrial_folate", "relation": "feeds", "confidence": 0.90, "is_terminal": False},
                {"target": "NADPH", "relation": "produces", "confidence": 0.85, "is_terminal": False},
            ],
            
            # MTHFD2 pathway
            "MTHFD2": [
                {"target": "formate", "relation": "produces", "confidence": 0.95, "is_terminal": False},
                {"target": "NADPH", "relation": "generates", "confidence": 0.88, "is_terminal": False},
                {"target": "purine", "relation": "supports", "confidence": 0.90, "is_terminal": False},
            ],
            "formate": [
                {"target": "cytosolic_folate", "relation": "replenishes", "confidence": 0.92, "is_terminal": False},
            ],
            
            # Cancer targets
            "TNBC": [
                {"target": "PHGDH", "relation": "amplifies", "confidence": 0.88, "is_terminal": True},
            ],
            "melanoma": [
                {"target": "PHGDH", "relation": "amplifies", "confidence": 0.85, "is_terminal": True},
            ],
            "lymphoma": [
                {"target": "SHMT2", "relation": "depends_on", "confidence": 0.87, "is_terminal": True},
            ],
            
            # Epigenetic
            "SAM": [
                {"target": "DNA_methylation", "relation": "donates_to", "confidence": 0.92, "is_terminal": False},
            ],
            "DNA_methylation": [
                {"target": "tumor_suppressor", "relation": "regulates", "confidence": 0.85, "is_terminal": False},
            ],
            
            # Metabolic disease
            "diabetes": [
                {"target": "homocysteine", "relation": "elevates", "confidence": 0.80, "is_terminal": False},
            ],
            "homocysteine": [
                {"target": "beta_cell", "relation": "damages", "confidence": 0.82, "is_terminal": True},
            ],
        }
    
    def query(self, query: str, disease_context: Optional[str] = None) -> ReasoningResult:
        """
        Query the multi-hop disease reasoner.
        
        Args:
            query: Reasoning chain (e.g., "PHGDH → serine → cancer")
            disease_context: Optional disease context for context boosting
            
        Returns:
            ReasoningResult with full trace
        """
        context = {"disease": disease_context} if disease_context else None
        return self.reasoner.reason(query, self.knowledge_graph, context)
    
    def add_knowledge(
        self,
        entity: str,
        relation: str,
        target: str,
        confidence: float = 0.8,
        is_terminal: bool = False,
    ):
        """Add knowledge to the graph."""
        if entity not in self.knowledge_graph:
            self.knowledge_graph[entity] = []
        
        self.knowledge_graph[entity].append({
            "target": target,
            "relation": relation,
            "confidence": confidence,
            "is_terminal": is_terminal,
        })
    
    def explain_mechanism(self, target: str, disease: str) -> str:
        """Explain mechanism from target to disease."""
        query = f"{target} → {disease}"
        result = self.query(query, disease_context=disease)
        
        explanation = f"**Mechanism: {target} → {disease}**\n\n"
        explanation += f"Confidence: {result.confidence:.2f}\n"
        explanation += f"Hops: {result.hops}\n"
        explanation += f"Steps used: {result.total_steps}\n\n"
        
        explanation += "**Reasoning chain:**\n"
        for i, step in enumerate(result.reasoning_chain):
            explanation += f"{i+1}. {step['relation']} → {step['next_entity']} "
            explanation += f"(conf: {step['confidence']:.2f})\n"
        
        return explanation


def main():
    """Demo of Loop-Think reasoning integration."""
    print("=" * 60)
    print("  Loop-Think Recurrent Reasoning for ARP v24")
    print("=" * 60)
    
    # Initialize reasoner
    reasoner = MultiHopDiseaseReasoner({
        "max_hops": 5,
        "recurrence": 3,
        "recurrence_type": "FIXED",
    })
    
    # Demo queries
    queries = [
        "PHGDH → serine → TNBC",
        "MTHFD2 → NADPH → cancer",
        "SHMT2 → glycine → lymphoma",
        "diabetes → homocysteine → beta_cell",
    ]
    
    print("\n📚 Multi-hop reasoning results:\n")
    
    for query in queries:
        result = reasoner.query(query)
        
        print(f"Query: {query}")
        print(f"  Answer: {result.answer}")
        print(f"  Hops: {result.hops}, Steps: {result.total_steps}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Systematic: {'✓' if result.is_systematic else '✗'}")
        print(f"  Time: {result.execution_time:.3f}s")
        print()
    
    # Demo mechanism explanation
    print("\n🔬 Mechanism explanation:")
    print(reasoner.explain_mechanism("PHGDH", "TNBC"))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()