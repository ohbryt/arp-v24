# auto-memory-cleanup skill

Memory consolidation for ARP workspace - removes duplicates, prunes stale references, and cleans transient notes.

## Trigger

- User says "整理して", "clean memory", "organize memory"
- Memory files exceed 200 lines
- Weekly scheduled cleanup

## Features

1. **Duplicate Detection** - Find same info across multiple files, merge intelligently
2. **Stale Pruning** - Remove references to old targets, superseded compounds
3. **Backup First** - Timestamped backup with verification before any changes
4. **Dry-Run Mode** - Preview without writing
5. **Cross-Project Consolidation** - Works across all arp-vXX project directories

## Lock Protocol

Before any work:
1. Check for OMC consolidation locks in `~/.claude/projects/*/memory/.consolidate-lock`
2. Check for own lock at `~/.claude/.arp-sleep.lock`
3. Acquire lock, do work, release lock on completion

## State Tracking

State file: `~/.claude/.arp-sleep-state.json`

```json
{
  "lastRun": "ISO-8601 timestamp",
  "runsTotal": 0,
  "projectStates": {
    "project-id": {
      "lineCount": 0,
      "fileCount": 0,
      "lastHash": "first 100 chars"
    }
  },
  "pendingReviews": [],
  "history": []
}
```

## Execution

### Phase 1: Scan (Fast Path Check)
- Read state file
- Scan all memory files, compute line counts and hashes
- Compare against last run
- If ALL unchanged → return "Memory is clean"

### Phase 2: Act (Backup + Consolidate + Prune)
1. **Backup** with verification
2. **Consolidate** duplicates - keep detail in topic file, one-line + link in MEMORY.md
3. **Prune** transient content, dead links, stale references
4. **Validate** all links point to existing files

## Cleanup Rules

### Remove
- Transient notes ("currently working on", "TODO", "FIXME")
- Dead cross-references (links to non-existent files)
- Duplicate information already in another file
- Stale target references (old ARPs superseded)
- Non-.md artifacts

### Keep
- User-written CLAUDE.md (never touch)
- Project-specific knowledge
- Research findings and insights
- Configuration notes

### Tag for Review
- Uncertain information → `[REVIEW NEEDED: reason — date]`
- Orphans from prior runs

## Dry-Run

If invoked with "dry-run", "preview", "미리보기":
- Execute Phase 1 (Scan) only
- Output action plan WITHOUT making changes
- Skip backup and all writes