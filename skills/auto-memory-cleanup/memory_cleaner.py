#!/usr/bin/env python3
"""
ARP Sleep - Auto Memory Cleanup for ARP Workspace

Inspired by Comad World's sleep module.
Consolidates and cleans memory files across ARP projects.

Usage:
    python memory_cleaner.py [--dry-run]
    python memory_cleaner.py --status
    python memory_cleaner.py --restore <backup_dir>
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

HOME = Path.home()
ARP_WORKSPACE = HOME / ".openclaw" / "workspace"
STATE_FILE = HOME / ".claude" / ".arp-sleep-state.json"
LOCK_FILE = HOME / ".claude" / ".arp-sleep.lock"
MAX_LINES_MEMORY = 200
MAX_HISTORY = 20

# Lock timeout
LOCK_WAIT_SECONDS = 5
LOCK_RETRIES = 3

# ============================================================================
# LOCK PROTOCOL
# ============================================================================

def check_omc_locks() -> bool:
    """Check for OMC consolidation locks"""
    projects_dir = HOME / ".claude" / "projects"
    if not projects_dir.exists():
        return False
    
    for project_dir in projects_dir.iterdir():
        memory_dir = project_dir / "memory"
        lock_file = memory_dir / ".consolidate-lock"
        if lock_file.exists():
            try:
                pid = int(lock_file.read_text().strip())
                if os.kill(pid, 0) == 0:  # Process alive
                    return True
            except (ValueError, ProcessLookupError):
                pass  # Stale lock
    return False

def acquire_lock() -> bool:
    """Acquire our lock file"""
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            os.kill(pid, 0)
            print(f"Another ARP-Sleep is running (PID: {pid}). Skipping.")
            return False
        except (ValueError, ProcessLookupError):
            pass  # Stale lock
    
    LOCK_FILE.write_text(str(os.getpid()))
    return True

def release_lock():
    """Release our lock file"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_state() -> dict:
    """Load state from file"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "lastRun": None,
        "runsTotal": 0,
        "projectStates": {},
        "pendingReviews": [],
        "history": []
    }

def save_state(state: dict):
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def compute_hash(content: str) -> str:
    """Compute hash of content"""
    return hashlib.md5(content.encode()).hexdigest()[:20]

def get_file_signature(path: Path) -> Tuple[int, str]:
    """Get line count and hash of a file"""
    content = path.read_text()
    return len(content.splitlines()), compute_hash(content)

# ============================================================================
# SCANNING
# ============================================================================

def find_memory_files() -> List[Path]:
    """Find all memory files in ARP workspace"""
    files = []
    for arp_dir in ARP_WORKSPACE.glob("arp-v*"):
        memory_dir = arp_dir / "memory"
        if memory_dir.exists():
            for f in memory_dir.glob("*.md"):
                files.append(f)
    return files

def scan_project(project_dir: Path) -> dict:
    """Scan a project directory for memory state"""
    memory_dir = project_dir / "memory"
    if not memory_dir.exists():
        return {"lineCount": 0, "fileCount": 0, "lastHash": ""}
    
    files = list(memory_dir.glob("*.md"))
    total_lines = 0
    all_content = ""
    
    for f in files:
        content = f.read_text()
        total_lines += len(content.splitlines())
        all_content += content
    
    return {
        "lineCount": total_lines,
        "fileCount": len(files),
        "lastHash": compute_hash(all_content)
    }

def detect_duplicates(files: List[Path]) -> List[Tuple[Path, Path, str]]:
    """Find duplicate content across files"""
    hash_to_files: Dict[str, List[Path]] = {}
    
    for f in files:
        content = f.read_text()
        h = compute_hash(content)
        if h not in hash_to_files:
            hash_to_files[h] = []
        hash_to_files[h].append(f)
    
    duplicates = []
    for h, paths in hash_to_files.items():
        if len(paths) > 1:
            # Group by similar content
            for i in range(len(paths)):
                for j in range(i + 1, len(paths)):
                    duplicates.append((paths[i], paths[j], "exact"))
    
    return duplicates

def detect_stale_references(files: List[Path], known_targets: Set[str]) -> List[Tuple[Path, str]]:
    """Detect stale target references"""
    stale = []
    old_target_patterns = [
        "arp-v10", "arp-v11", "arp-v12", "arp-v13",
        "deprecated", "superseded", "old_target"
    ]
    
    for f in files:
        content = f.read_text()
        for pattern in old_target_patterns:
            if pattern.lower() in content.lower():
                stale.append((f, pattern))
    
    return stale

def detect_transient_content(files):
    """Detect transient/session-specific content"""
    transient_patterns = [
        "currently working", "todo:", "fixme:", "temp:",
        "working on", "in progress", "임시", "작업 중",
        "this session", "오늘의", "이번 주"
    ]
    
    results = []
    for f in files:
        content = f.read_text().lower()
        found = []
        for pattern in transient_patterns:
            if pattern in content:
                found.append(pattern)
        if found:
            results.append((f, found))
    
    return results

# ============================================================================
# CONSOLIDATION
# ============================================================================

def merge_duplicate_into_memory(duplicate: Path, memory_md: Path):
    """When duplicate found, keep detail in topic file, one-line + link in MEMORY.md"""
    if not memory_md.exists():
        return
    
    memory_content = memory_md.read_text()
    duplicate_name = duplicate.stem
    
    # Check if link already exists
    if f"[{duplicate_name}]" in memory_content or duplicate.name in memory_content:
        return  # Already linked
    
    # Add link to MEMORY.md
    memory_content += f"\n- [{duplicate_name}]({duplicate.name})"
    memory_md.write_text(memory_content)

def prune_transient_from_file(path: Path, patterns: List[str]):
    """Remove transient content from file"""
    content = path.read_text()
    original = content
    
    for pattern in patterns:
        # Simple line-based removal for common patterns
        lines = content.splitlines()
        cleaned = []
        skip = False
        for line in lines:
            if pattern.lower() in line.lower():
                if "TODO" in line or "FIXME" in line or "temp" in line.lower():
                    continue  # Skip these lines
                skip = True
            if not skip or "\n" in line:
                cleaned.append(line)
                skip = False
        
        content = "\n".join(cleaned)
    
    if content != original:
        path.write_text(content)
        return True
    return False

def tag_uncertain_content(path: Path, reason: str):
    """Tag uncertain content for review"""
    content = path.read_text()
    tag = f"\n\n[REVIEW NEEDED: {reason} — {datetime.now().strftime('%Y-%m-%d')}]"
    
    if "[REVIEW NEEDED" not in content:
        path.write_text(content + tag)

# ============================================================================
# BACKUP
# ============================================================================

def create_backup() -> Optional[Path]:
    """Create timestamped backup with verification"""
    backup_dir = HOME / ".claude" / f"arp-memory-backup-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}"
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup all ARP memory directories
        for arp_dir in ARP_WORKSPACE.glob("arp-v*"):
            memory_dir = arp_dir / "memory"
            if memory_dir.exists():
                dest = backup_dir / arp_dir.name
                shutil.copytree(memory_dir, dest)
        
        # Verify backup
        src_count = sum(1 for arp_dir in ARP_WORKSPACE.glob("arp-v*") 
                       if (arp_dir / "memory").exists()
                       for _ in (arp_dir / "memory").glob("*"))
        backup_count = sum(1 for _ in backup_dir.glob("**/*") if _.is_file())
        
        if src_count != backup_count:
            print(f"Backup verification failed: {src_count} source files vs {backup_count} backup files")
            shutil.rmtree(backup_dir)
            return None
        
        return backup_dir
    
    except Exception as e:
        print(f"Backup failed: {e}")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_cleanup(dry_run: bool = False) -> dict:
    """Run the cleanup process"""
    result = {
        "files_scanned": 0,
        "duplicates_found": 0,
        "stale_references": 0,
        "transient_removed": 0,
        "changes_made": [],
        "backup_path": None
    }
    
    # Phase 1: Scan
    files = find_memory_files()
    result["files_scanned"] = len(files)
    
    # Fast path: check if anything changed
    state = load_state()
    project_hashes = {}
    for arp_dir in ARP_WORKSPACE.glob("arp-v*"):
        h = compute_hash(str(scan_project(arp_dir)))
        project_hashes[arp_dir.name] = h
    
    unchanged = all(
        state.get("projectStates", {}).get(name, {}).get("lastHash") == h
        for name, h in project_hashes.items()
    )
    
    if unchanged and len(files) < 50:
        result["status"] = "CLEAN"
        return result
    
    # Find issues
    duplicates = detect_duplicates(files)
    stale_refs = detect_stale_references(files, set())
    transient = detect_transient_content(files)
    
    result["duplicates_found"] = len(duplicates)
    result["stale_references"] = len(stale_refs)
    
    # Phase 2: Act (unless dry-run)
    if not dry_run:
        # Backup first
        backup = create_backup()
        if backup is None:
            print("Backup verification failed. Aborting cleanup.")
            return result
        result["backup_path"] = str(backup)
        
        # Consolidate duplicates
        for dup, orig, _ in duplicates:
            if orig.stem == "MEMORY":
                merge_duplicate_into_memory(dup, orig)
                result["changes_made"].append(f"Merged {dup.name} into {orig.name}")
        
        # Prune transient
        for path, patterns in transient:
            if prune_transient_from_file(path, patterns):
                result["transient_removed"] += 1
                result["changes_made"].append(f"Pruned transient from {path.name}")
    
    # Record history
    state["history"].append({
        "date": datetime.now().isoformat(),
        "changes": result["changes_made"] if result["changes_made"] else ["No changes needed"]
    })
    if len(state["history"]) > MAX_HISTORY:
        state["history"] = state["history"][-MAX_HISTORY:]
    
    state["lastRun"] = datetime.now().isoformat()
    state["runsTotal"] += 1
    
    # Update project states
    if "projectStates" not in state:
        state["projectStates"] = {}
    for arp_dir in ARP_WORKSPACE.glob("arp-v*"):
        state["projectStates"][arp_dir.name] = scan_project(arp_dir)
    
    save_state(state)
    
    return result

def show_status():
    """Show current memory status"""
    state = load_state()
    print(f"Last run: {state.get('lastRun', 'Never')}")
    print(f"Total runs: {state.get('runsTotal', 0)}")
    print(f"Projects tracked: {len(state.get('projectStates', {}))}")
    print(f"Pending reviews: {len(state.get('pendingReviews', []))}")
    
    if state.get("history"):
        print(f"\nRecent history:")
        for entry in state["history"][-3:]:
            print(f"  {entry['date']}: {entry['changes']}")

def restore_backup(backup_dir: str):
    """Restore from backup"""
    backup_path = Path(backup_dir)
    if not backup_path.exists():
        print(f"Backup not found: {backup_dir}")
        return
    
    for arp_dir in ARP_WORKSPACE.glob("arp-v*"):
        memory_dir = arp_dir / "memory"
        backup_memory = backup_path / arp_dir.name / "memory"
        
        if backup_memory.exists():
            if memory_dir.exists():
                shutil.rmtree(memory_dir)
            shutil.copytree(backup_memory, memory_dir)
            print(f"Restored {arp_dir.name}/memory")

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="ARP Sleep - Auto Memory Cleanup")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--restore", metavar="DIR", help="Restore from backup")
    parser.add_argument("--trigger", metavar="TEXT", help="Trigger text (for compatibility)")
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
        return
    
    if args.restore:
        restore_backup(args.restore)
        return
    
    # Check locks
    if check_omc_locks():
        print("OMC consolidation in progress. Try again later.")
        return
    
    if not acquire_lock():
        return
    
    try:
        result = run_cleanup(dry_run=args.dry_run)
        
        if result.get("status") == "CLEAN":
            print("Memory is clean. No action needed.")
        else:
            print(f"ARP Sleep Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print(f"Scanned: {result['files_scanned']} files")
            print(f"Duplicates: {result['duplicates_found']}")
            print(f"Stale refs: {result['stale_references']}")
            print(f"Transient removed: {result['transient_removed']}")
            if result["changes_made"]:
                print("\nChanges:")
                for change in result["changes_made"]:
                    print(f"  - {change}")
            if result.get("backup_path"):
                print(f"\nBackup: {result['backup_path']}")
    finally:
        release_lock()

if __name__ == "__main__":
    main()