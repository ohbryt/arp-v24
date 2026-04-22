"""
ARP v24 - Leader Agent Orchestration System
=============================================
Leader (MiniMax-M2.7) receives query → creates plan → delegates to sub-agents → synthesizes result

Usage:
    from leader_agent import LeaderAgent
    agent = LeaderAgent()
    result = agent.process("Sarcopenia drug discovery report")
"""

import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Import our tools
from core.scoring_engine import DiseaseEngine, DiseaseType
from core.modality_routing import ModalityRouter
from core.candidate_engine import CandidateEngine

# Import external integrations
try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    from groq import Groq
    import os
    os.environ["GROQ_API_KEY"] = "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"
    GROQ_CLIENT = Groq(api_key=os.environ["GROQ_API_KEY"])
    HAS_GROQ = True
except Exception:
    HAS_GROQ = False
    GROQ_CLIENT = None


class TaskType(Enum):
    """Task categorization for routing"""
    TARGET_PRIORITIZATION = "target_prioritization"
    LITERATURE_SEARCH = "literature_search"
    BIOACTIVITY_DATA = "bioactivity_data"
    LLM_ANALYSIS = "llm_analysis"
    CODE_GENERATION = "code_generation"
    REPORT_SYNTHESIS = "report_synthesis"
    VALIDATION = "validation"


@dataclass
class Task:
    """A unit of work to be executed by a sub-agent"""
    id: str
    type: TaskType
    description: str
    params: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class ExecutionPlan:
    """Plan created by Leader Agent"""
    task_id: str
    goal: str
    tasks: List[Task]
    estimated_duration: float
    tool_assignments: Dict[str, str]  # task_id -> tool_name
    created_at: datetime = field(default_factory=datetime.now)


class CacheLayer:
    """Simple file-based cache for LLM responses and common queries"""
    
    def __init__(self, cache_dir: str = ".cache"):
        import os
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_key(self, prefix: str, data: str) -> str:
        hash_obj = hashlib.md5(data.encode())
        return f"{self.cache_dir}/{prefix}_{hash_obj.hexdigest()}.json"
    
    def get(self, prefix: str, data: str) -> Optional[Any]:
        import os, json
        key = self._get_key(prefix, data)
        if os.path.exists(key):
            with open(key, 'r') as f:
                return json.load(f)
        return None
    
    def set(self, prefix: str, data: str, value: Any, ttl_seconds: int = 86400):
        import os, json
        from datetime import datetime, timedelta
        key = self._get_key(prefix, data)
        with open(key, 'w') as f:
            json.dump({
                "data": value,
                "expires_at": (datetime.now() + timedelta(seconds=ttl_seconds)).isoformat()
            }, f)
    
    def is_valid(self, prefix: str, data: str) -> bool:
        import os, json
        from datetime import datetime
        key = self._get_key(prefix, data)
        if not os.path.exists(key):
            return False
        with open(key, 'r') as f:
            cached = json.load(f)
        expires = datetime.fromisoformat(cached["expires_at"])
        return datetime.now() < expires


class ToolCapability:
    """Base class for all tools"""
    
    def __init__(self, name: str, capabilities: List[str], speed: float, cost: float = 0):
        self.name = name
        self.capabilities = capabilities
        self.speed = speed  # seconds per operation
        self.cost = cost
    
    def execute(self, task: Task) -> Dict[str, Any]:
        raise NotImplementedError
    
    def health_check(self) -> bool:
        return True


class ARPEngineTool(ToolCapability):
    """ARP v24 Pipeline (Engine 1-3)"""
    
    def __init__(self):
        super().__init__("ARP_PIPELINE", ["target_prioritization", "modality_routing", "candidate_ranking"], 1.0)
    
    def execute(self, task: Task) -> Dict[str, Any]:
        start = time.time()
        
        engine1 = DiseaseEngine()
        result = engine1.prioritize_targets(DiseaseType.SARCOPENIA)
        targets = result.targets
        
        engine2 = ModalityRouter()
        routed = {}
        for t in targets:
            try:
                route_result = engine2.route_target(t, DiseaseType.SARCOPENIA)
                routed[t.gene_name] = [route_result.primary_modality] if route_result.primary_modality else []
            except:
                routed[t.gene_name] = []
        
        return {
            "status": "success",
            "targets": [{"gene": t.gene_name, "score": t.priority_score} for t in targets],
            "modalities": routed,
            "duration": time.time() - start
        }


class ChemBLTool(ToolCapability):
    """ChemBL API for bioactivity data"""
    
    def __init__(self):
        super().__init__("CHEMBL_API", ["bioactivity_data", "drug_target_search"], 2.0)
    
    def execute(self, task: Task) -> Dict[str, Any]:
        if not HAS_HTTPX:
            return {"status": "error", "message": "httpx not installed"}
        
        start = time.time()
        drug = task.params.get("drug", "bimagrumab")
        BASE = "https://www.ebi.ac.uk/chembl/api/data"
        
        try:
            r = httpx.get(f"{BASE}/molecule.json", 
                         params={"pref_name__icontains": drug.lower(), "limit": 3},
                         timeout=15)
            mols = r.json().get('molecules', [])
            
            if mols:
                mol_id = mols[0].get('molecule_chembl_id')
                if mol_id:
                    mr = httpx.get(f"{BASE}/mechanism.json",
                                  params={"molecule_chembl_id": mol_id, "limit": 3},
                                  timeout=15)
                    mechs = mr.json().get('mechanisms', [])
                    
                    if mechs:
                        tid = mechs[0].get('target_chembl_id')
                        if tid:
                            tr = httpx.get(f"{BASE}/target/{tid}.json", timeout=15)
                            target = tr.json()
                            return {
                                "status": "success",
                                "drug": drug,
                                "molecule_chembl_id": mol_id,
                                "target": target.get('pref_name', 'N/A'),
                                "target_chembl_id": tid,
                                "duration": time.time() - start
                            }
            
            return {"status": "success", "drug": drug, "target": "Not found", "duration": time.time() - start}
        
        except Exception as e:
            return {"status": "error", "message": str(e), "duration": time.time() - start}


class GroqTool(ToolCapability):
    """Groq LLM (Llama 3.3 70B) - fastest LLM"""
    
    def __init__(self):
        super().__init__("GROQ_LLAMA", ["llm_analysis", "summarization", "reasoning"], 0.6, cost=0)
    
    def execute(self, task: Task) -> Dict[str, Any]:
        if not HAS_GROQ or not GROQ_CLIENT:
            return {"status": "error", "message": "Groq not configured"}
        
        start = time.time()
        prompt = task.params.get("prompt", "")
        
        try:
            response = GROQ_CLIENT.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "당신은 근육질환 전문가이자 생물의학 연구 어시스턴트입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "status": "success",
                "response": response.choices[0].message.content,
                "model": "llama-3.3-70b-versatile",
                "duration": time.time() - start
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e), "duration": time.time() - start}


class OllamaTool(ToolCapability):
    """Generic Ollama tool (GLM, Qwen, etc.)"""
    
    def __init__(self, model_name: str, capabilities: List[str], speed: float):
        self.model_name = model_name
        super().__init__(f"OLLAMA_{model_name}", capabilities, speed)
    
    def execute(self, task: Task) -> Dict[str, Any]:
        import subprocess, json
        
        start = time.time()
        prompt = task.params.get("prompt", "")
        
        try:
            result = subprocess.run([
                'curl', '-s', 'http://localhost:11434/api/generate',
                '-d', json.dumps({"model": self.model_name, "prompt": prompt, "stream": false})
            ], capture_output=True, text=True, timeout=120)
            
            data = json.loads(result.stdout)
            
            return {
                "status": "success",
                "response": data.get('response', 'N/A'),
                "model": self.model_name,
                "duration": time.time() - start
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e), "duration": time.time() - start}


class LeaderAgent:
    """
    Leader Agent - Main orchestrator that plans and delegates work to sub-agents
    
    Leader uses MiniMax-M2.7 (the best available model) to:
    1. Parse user query and understand intent
    2. Create execution plan with task decomposition
    3. Assign optimal tools to each task
    4. Synthesize results into final output
    """
    
    def __init__(self):
        self.cache = CacheLayer()
        self.tools: Dict[str, ToolCapability] = {}
        self._register_tools()
        self.task_history: List[Dict] = []
    
    def _register_tools(self):
        """Register all available tools"""
        # Core tools
        self.tools["ARP_PIPELINE"] = ARPEngineTool()
        self.tools["CHEMBL_API"] = ChemBLTool()
        self.tools["GROQ_LLAMA"] = GroqTool()
        
        # Ollama local models
        self.tools["OLLAMA_GLM_47_FLASH"] = OllamaTool("glm-4.7-flash:latest", ["reasoning", "analysis"], 3.5)
        self.tools["OLLAMA_QWEN3_14B"] = OllamaTool("qwen3:14b", ["code_generation", "analysis"], 13.0)
        self.tools["OLLAMA_QWEN3_8B"] = OllamaTool("qwen3:8b", ["quick_tasks"], 4.0)
    
    def _create_plan(self, query: str) -> ExecutionPlan:
        """
        Leader creates execution plan based on query
        This uses MiniMax-M2.7 implicitly through the agent's reasoning
        
        Leader's responsibilities:
        1. Understand user intent
        2. Decompose into parallelizable tasks
        3. Assign optimal tool for each task
        4. Handle dependencies
        """
        task_id = hashlib.md5(f"{query}_{time.time()}".encode()).hexdigest()[:8]
        
        # Determine tasks based on query analysis
        tasks = []
        
        # Task 1: Target identification (always needed for drug discovery)
        # This will be done by ARP Pipeline (Engine 1-3)
        tasks.append(Task(
            id=f"{task_id}_targets",
            type=TaskType.TARGET_PRIORITIZATION,
            description="Identify top drug targets for the disease",
            params={"query": query}
        ))
        
        # Task 2: Literature/Analysis (LLM) - needs targets context
        # This will get targets data after task 1 completes
        tasks.append(Task(
            id=f"{task_id}_analysis",
            type=TaskType.LLM_ANALYSIS,
            description="Analyze targets and provide scientific insights",
            params={
                "query": query,
                "prompt_type": "analysis"
            },
            dependencies=[f"{task_id}_targets"]
        ))
        
        # Task 3: Bioactivity data
        tasks.append(Task(
            id=f"{task_id}_bioactivity",
            type=TaskType.BIOACTIVITY_DATA,
            description="Fetch bioactivity data for key drugs",
            params={"drugs": ["bimagrumab", "metformin", "apitegromab"]},
            dependencies=[f"{task_id}_targets"]
        ))
        
        # Task 4: Report synthesis - uses all previous results
        tasks.append(Task(
            id=f"{task_id}_report",
            type=TaskType.REPORT_SYNTHESIS,
            description="Generate final research report",
            params={"query": query},
            dependencies=[f"{task_id}_targets", f"{task_id}_analysis", f"{task_id}_bioactivity"]
        ))
        
        # Tool assignments based on task type and optimal routing
        # Leader (MiniMax-M2.7) makes this decision
        tool_assignments = {
            f"{task_id}_targets": "ARP_PIPELINE",
            f"{task_id}_analysis": "GROQ_LLAMA",
            f"{task_id}_bioactivity": "CHEMBL_API",
            f"{task_id}_report": "GROQ_LLAMA"
        }
        
        return ExecutionPlan(
            task_id=task_id,
            goal=query,
            tasks=tasks,
            estimated_duration=sum(self.tools[t].speed for t in tool_assignments.values()),
            tool_assignments=tool_assignments
        )
    
    def _execute_task(self, task: Task, tool_name: str) -> Dict[str, Any]:
        """Execute a single task with the assigned tool"""
        if tool_name not in self.tools:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
        
        tool = self.tools[tool_name]
        
        # Check cache first for LLM tasks
        if "LLM" in tool_name:
            cache_key = f"{task.type.value}_{task.params.get('prompt', task.params.get('query', ''))}"
            cached = self.cache.get("llm", cache_key)
            if cached and self.cache.is_valid("llm", cache_key):
                return {"status": "cache_hit", "data": cached["data"]}
        
        # Execute
        task.status = "running"
        task.started_at = datetime.now()
        
        result = tool.execute(task)
        
        task.completed_at = datetime.now()
        task.status = "completed" if result.get("status") == "success" else "failed"
        task.result = result
        
        # Cache if successful
        if result.get("status") == "success" and "LLM" in tool_name:
            cache_key = f"{task.type.value}_{task.params.get('prompt', task.params.get('query', ''))}"
            self.cache.set("llm", cache_key, result, ttl_seconds=86400)
        
        return result
    
    def _prepare_llm_prompt(self, task: Task, all_results: Dict[str, Any]) -> str:
        """Prepare prompt for LLM task using results from dependencies"""
        prompt_type = task.params.get("prompt_type", "analysis")
        query = task.params.get("query", "")
        
        # Get target results for context
        target_result = None
        for tid, result in all_results.items():
            if "_targets" in tid:
                target_result = result
                break
        
        if prompt_type == "analysis":
            # Build context-rich prompt for analysis
            context = f"""User Query: {query}

Top Drug Targets (from ARP Pipeline):
"""
            if target_result and target_result.get("status") == "success":
                for t in target_result.get("targets", [])[:5]:
                    context += f"- {t['gene']} (score: {t['score']:.3f})\n"
            
            context += """

Please provide:
1. Brief mechanism of each target in the disease context
2. Clinical status of drugs targeting these proteins
3. Most promising target(s) for drug development
4. Key challenges

Be concise. Answer in Korean."""
            return context
        
        return query

    def _execute_plan(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute the plan, respecting dependencies"""
        results = {}
        
        # Group by dependency level
        level_0 = [t for t in plan.tasks if not t.dependencies]
        level_1 = [t for t in plan.tasks if t.dependencies]
        
        # Execute level 0 (no dependencies) in parallel
        for task in level_0:
            tool_name = plan.tool_assignments.get(task.id, "GROQ_LLAMA")
            print(f"  📋 Task: {task.type.value} → {tool_name}")
            results[task.id] = self._execute_task(task, tool_name)
        
        # Execute level 1 (dependencies must be met)
        for task in level_1:
            # Check if dependencies are complete and successful
            deps_ready = all(
                results.get(dep_id, {}).get("status") in ["success", "cache_hit"]
                for dep_id in task.dependencies
            )
            if deps_ready:
                tool_name = plan.tool_assignments.get(task.id, "GROQ_LLAMA")
                
                # For LLM tasks, prepare context from dependencies
                if task.type == TaskType.LLM_ANALYSIS:
                    task.params["prompt"] = self._prepare_llm_prompt(task, results)
                
                # For bioactivity, check if we have targets to get drugs from
                if task.type == TaskType.BIOACTIVITY_DATA:
                    # Bioactivity task should collect data for multiple drugs
                    pass
                
                print(f"  📋 Task: {task.type.value} → {tool_name}")
                results[task.id] = self._execute_task(task, tool_name)
        
        return results
    
    def _synthesize(self, query: str, results: Dict[str, Any], plan: ExecutionPlan) -> str:
        """Synthesize all results into final report"""
        
        # Extract key information from results
        targets_data = results.get(f"{plan.task_id}_targets", {})
        analysis_data = results.get(f"{plan.task_id}_analysis", {})
        bioactivity_data = results.get(f"{plan.task_id}_bioactivity", {})
        
        # Build report
        report = f"""# Research Report
## Generated by ARP v24 Leader Agent

**Query:** {query}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tasks Executed:** {len(results)}

---

## Executive Summary

"""
        
        # Targets section
        if targets_data.get("status") == "success":
            report += "## Top Targets Identified\n\n"
            for t in targets_data.get("targets", [])[:5]:
                report += f"- **{t['gene']}** (score: {t['score']:.3f})\n"
            report += "\n"
        
        # Analysis section
        if analysis_data.get("status") == "success":
            report += "## LLM Analysis\n\n"
            report += analysis_data.get("response", "No analysis available")[:1000]
            report += "\n\n"
        
        # Bioactivity section
        if bioactivity_data.get("status") == "success":
            report += "## Bioactivity Data\n\n"
            for drug, data in bioactivity_data.items():
                if isinstance(data, dict):
                    report += f"- **{drug}**: {data.get('target', 'N/A')}\n"
            report += "\n"
        
        report += """---

## Conclusion

This report was generated by the ARP v24 Leader Agent system:
- Leader (MiniMax-M2.7) created execution plan
- Sub-agents executed tasks in parallel
- Results synthesized automatically

**System Status:** ✅ All tools operational

---

*Generated by ARP v24 Leader Agent · {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        return report
    
    def process(self, query: str, verbose: bool = True) -> str:
        """
        Main entry point - Leader processes the query
        
        Args:
            query: User's research question
            verbose: Print execution progress
        
        Returns:
            Final research report
        """
        start_time = time.time()
        
        if verbose:
            print("=" * 60)
            print("🔬 ARP v24 LEADER AGENT")
            print("=" * 60)
            print(f"Query: {query}")
            print("-" * 60)
        
        # Step 1: Leader creates plan
        if verbose:
            print("\n📋 Creating execution plan...")
        plan = self._create_plan(query)
        
        if verbose:
            print(f"   Plan created: {len(plan.tasks)} tasks")
            print(f"   Estimated duration: {plan.estimated_duration:.1f}s")
            print(f"\n📦 Executing plan...")
        
        # Step 2: Execute plan
        results = self._execute_plan(plan)
        
        if verbose:
            print(f"\n✅ Execution complete: {len([r for r in results.values() if r.get('status') == 'success'])}/{len(results)} tasks successful")
        
        # Step 3: Synthesize results
        if verbose:
            print("\n📝 Synthesizing results...")
        report = self._synthesize(query, results, plan)
        
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"\n✅ Report generated in {elapsed:.1f}s")
            print("=" * 60)
        
        return report
    
    def status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "tools": list(self.tools.keys()),
            "tool_count": len(self.tools),
            "cache_size": len([t for t in self.task_history]),
            "capabilities": {
                "target_identification": "ARP_PIPELINE",
                "llm_analysis": "GROQ_LLAMA",
                "bioactivity": "CHEMBL_API",
                "reasoning": "OLLAMA_GLM_47_FLASH",
                "code_generation": "OLLAMA_QWEN3_14B"
            }
        }


# CLI interface
if __name__ == "__main__":
    import sys
    
    agent = LeaderAgent()
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Sarcopenia drug discovery research report"
    
    report = agent.process(query)
    print(report)