# arp-v24 — PRISM Research Pipeline

## What This Does
ARP v24 is Brown Biotech's autonomous research pipeline — ZIP-RC agents, tournament scoring, RAG evidence retrieval, and self-evolution. The core system for decision-ready biotech research briefs.

## Architecture
- `arp_coordinator.py` — mission control, budget tracking, escalation
- `zip_rc_agent.py` — ZIP-RC research heuristic decomposition
- `arp_tournament.py` — pairwise candidate ranking with TrueSkill
- `arp_verifier.py` — QA evidence verification, one-reject escalation
- `arp_mcp_server.py` — MCP instrument server for tool access
- `arp_self_evolution.py` — autonomous pattern improvement from trial logs
- `rag/` — FAISS vector store, PubMed/PMC retrieval
- `eval/` — benchmark harness for agent evaluation

## Commands
```bash
# Run full pipeline on a research brief
python arp_coordinator.py --mission "senolytic candidates 2025-2026"

# Run tournament ranking only
python arp_tournament.py --brief-id <id>

# Run self-evolution cycle
python arp_self_evolution.py --generations 5

# Start MCP server
python arp_mcp_server.py --port 8080

# Safety check before push
./scripts/pre-push-safety-check.sh
```

## Critical Gotchas
- Coordinator tracks `budget_used` per workstream — check before each iteration
- QA returns one reject → escalate, NOT back to worker
- RAG retrieval: check `retrieved` timestamp on all evidence
- Self-evolution: run safety check after each generation
- MCP server: requires auth token in `ARP_MCP_TOKEN` env var

## Memory Scopes
- `agent_repo`: ZIP-RC config, evolution rules (durable)
- `project`: per-brief state, candidate scores (brief lifetime)
- `session`: raw findings, trial drafts (ephemeral)
- `discard`: failed approaches, unsupported speculation

## Loop Guards
- Worker max_attempts: 5 before escalation
- QA max_rejections: 2 before escalate
- Tool retries: 3 before blocked

## Integration Points
- MCP instruments → brown-biotech-platform (via MCP client)
- Tournament results → Notion Research Briefs DB
- Self-evolution logs → arp-v24/evolution/