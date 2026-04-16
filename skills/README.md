# ARP v24 Skills

Production-grade research skills for AI-assisted drug discovery.

## Core Development Lifecycle

| Command | Skill | Description |
|---------|-------|-------------|
| `/spec` | [arp-research/SKILL.md](arp-research/SKILL.md) | Research spec before experiments |
| `/plan` | Planning & Task Breakdown | Decompose into verifiable tasks |
| `/build` | Incremental Implementation | Thin vertical slices |
| `/test` | Validation Testing | ADMET → Docking → Synthesis |
| `/review` | Research Review | Five-axis quality review |
| `/ship` | Finalize & Report | Full provenance and documentation |

## Directory Structure

```
skills/
├── README.md                    # This file
├── arp-research/
│   ├── SKILL.md                  # Core research skills
│   └── agents/
│       └── reviewer.md           # Research reviewer agent
```

## Usage

### In OpenClaw
Reference skills in SOUL.md or AGENTS.md:

```markdown
When conducting research:
1. Read skills/arp-research/SKILL.md
2. Follow the development lifecycle
3. Apply the review checklist before conclusions
```

### In Claude Code
```
/project /path/to/skills
```

### In Cursor
Copy SKILL.md into `.cursor/rules/`

---

## Available Skills

| Skill | Purpose | Use When |
|-------|---------|----------|
| arp-research | Research pipeline lifecycle | Any drug discovery research |

---

## Based On

This framework is adapted from [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani, tailored for biomedical research workflows.

---

*Last Updated: 2026-04-16*
