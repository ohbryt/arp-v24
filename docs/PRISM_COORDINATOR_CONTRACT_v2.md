# PRISM Coordinator Contract v2.0
## Based on: Agentlas PM Soul + Org Chart patterns adapted for biotech research pipeline

## Core Design Principle

> Multi-agent failure in research contexts is an **organization design failure**, not a prompt failure.
> The fix is explicit authority, bounded iteration, typed returns, and scoped memory per role.

---

## Role Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                    MISSION OWNER                        │
│  Dr. OCM — defines goal, global budget, final stop      │
│  Only layer that can extend budget or change scope      │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 STRATEGY OFFICE                         │
│  ZIP-RC Agent — decomposes mission into workstreams     │
│  Cannot execute; only decomposes and routes             │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ DOMAIN A │  │ DOMAIN B │  │ DOMAIN C │
  │ (Literature)│ │(Synthesis│  │(Validation│
  │          │  │         │  │          │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │             │
       ▼             ▼             ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ WORKER   │  │ WORKER   │  │ WORKER   │
  │ specialist│  │ specialist│  │ specialist│
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │             │
       └─────────────┴─────────────┘
                       │
              ┌────────▼────────┐
              │   QA / VERIFIER  │
              │  Evidence Office │
              │  One reject →    │
              │  escalate        │
              └─────────────────┘
```

---

## Worker Return Schema

Every specialist returns a typed manifest, never conversational prose:

```yaml
role: literature-specialist
task_id: lit-2026-05-24-001
status: done | needs_revision | blocked | escalate
output:
  summary: "120-char finding summary"
  detail: "full structured output"
evidence:
  - type: pubmed | pmc | arxiv | internal
    id: "PMID or URL"
    citation: "Author et al. Year"
    retrieved: "2026-05-24"
risks:
  - level: low | medium | high
    note: "what might be wrong or incomplete"
next_action: accept | revise | escalate | stop
budget_used: 3 / 5 worker attempts
```

---

## Loop Guard Rules (prevent infinite recursion)

1. **No lateral handoffs** — workers report UP to manager only
2. **Scoped memory per role** — each domain tracks its own state, not the full pipeline
3. **Counter on every loop edge** — each task has `max_attempts`
4. **One reject → escalate** — QA rejects once, then the issue moves UP, not back to worker
5. **Every manager must choose** — `accept | revise | escalate | stop` with documentation
6. **Unresolved contradiction escalates** — two credible findings disagree → move up
7. **Budget tracking mandatory** — coordinator tracks `budget_used` per workstream

---

## Memory Scopes (4-layer model)

| Scope | Owner | Lifetime | Contents |
|---|---|---|---|
| `agent_repo` | PRISM coordinator | durable | ZIP-RC configuration, evolution rules, MCP instrument definitions |
| `project` | per research brief | brief lifetime | Brief metadata, candidate scores, ranked shortlist, open questions |
| `session` | per workstream run | ephemeral | Raw findings, intermediate drafts, trial scores |
| `discard` | — | never written | Failed approaches, unsupported speculation, duplicate hits |

**Conservative default:** Session scratch → discard unless evidence confirms value.
**Promotion rule:** Session → project requires `still_relevant + evidence + stable owner`.

---

## Coordination Protocol

### Task Decomposition (Strategy Office → Domain Managers)

```
Mission: "Identify top-3 senolytic candidates from 2025-2026 literature"
  ↓
Workstream A: Literature scan (lit-specialist) — arXiv, PubMed, PMC
Workstream B: Synthesis scoring (synthesis-specialist) — IOA + structural filters
Workstream C: Validation evidence (verifier) — cross-ref, confidence check
  ↓
QA reviews all outputs → Coordinator synthesizes → Mission Owner receives ranked shortlist
```

### Escalation Path

```
Worker blocked → Domain Manager reviews → 
  if unresolved → Strategy Office reviews →
    if unresolved → Mission Owner decides
```

### Bounded Iteration

- Each worker: `max_attempts = 5` before escalation
- Each QA review: `max_rejections = 2` before escalate
- Each workstream: `max_tool_retries = 3` before record as blocked

---

## Integration with arp-v24

| Pattern | arp-v24 Implementation |
|---|---|
| Coordinator as Mission Owner | `arp_coordinator.py` receives mission, sets global budget |
| ZIP-RC as Strategy Office | `zip_rc_agent.py` decomposes into literature/synthesis/validation |
| Domain workers | `lit_specialist.py`, `synthesis_specialist.py`, `verifier.py` |
| QA / Evidence Office | `arp_verifier.py` — one reject → escalate to coordinator |
| Typed returns | All specialist outputs use Worker Return Schema YAML |
| Scoped memory | PRISM state JSON per brief — not global memory dump |
| Loop guards | Budget counters in coordinator state, checked before each iteration |
| Public safety check | `brown-biotech-safety-check.sh` pre-push hook |

---

## Self-Evolution Integration

Each PRISM self-evolution run produces:
1. **Trial manifest** — worker return schemas for each run
2. **QA rejection log** — what was rejected and why
3. **Budget consumption report** — did we hit limits, where
4. **Escalation log** — when and why issues moved up the chain

These feeds into the evolution engine to adjust:
- Worker max_attempts (if too many escalations)
- QA rejection threshold (if too many valid items rejected)
- Domain scope boundaries (if lateral handoffs attempted)
- Memory promotion rules (if too much session-level noise)

---

## Adoption Status

- [x] Worker Return Schema defined
- [x] Loop guard rules documented
- [x] 4-scope memory model defined
- [x] Coordination protocol specified
- [x] arp-v24 integration mapping
- [ ] Safety check hook integrated into arp-v24
- [ ] Coordinator state schema updated with budget tracking
- [ ] Self-evolution trial manifest schema implemented
- [ ] QA one-reject escalation path coded