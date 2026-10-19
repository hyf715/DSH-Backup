#!/usr/bin/env python3
"""Export DSH memories + skills into a git-friendly text layout.

Reads the live SQLite DB (safe: read-only connection) and writes:
  memories/<id>-<slug>.md   one file per memory, YAML-ish front matter + body
  memories.jsonl            one JSON object per line (restore-friendly)
  skills/                   verbatim copy of ~/.dsh/skills
"""
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

DSH_HOME = os.path.expanduser("~/.dsh")
DB = os.path.join(DSH_HOME, "memory", "memory.db")
SKILLS = os.path.join(DSH_HOME, "skills")
REPO = os.path.dirname(os.path.abspath(__file__))
MEM_DIR = os.path.join(REPO, "memories")


def slugify(text: str) -> str:
    """Short ASCII slug from a memory's first line, for readable filenames."""
    s = re.sub(r"[^A-Za-z0-9]+", "-", text.strip()[:60]).strip("-").lower()
    return s[:40] or "memory"


def iso(ts: int) -> str:
    # DSH stores epoch in milliseconds; tolerate seconds too.
    if ts > 10_000_000_000:
        ts = ts / 1000.0
    return datetime.fromtimestamp(ts, timezone.utc).isoformat()


def main() -> int:
    if not os.path.exists(DB):
        print(f"no memory db at {DB}", file=sys.stderr)
        return 1

    # Read-only connection so we never disturb the running dsh process.
    uri = f"file:{DB}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    rows = con.execute(
        "SELECT id, text, tags, pinned, created_at, updated_at "
        "FROM memories ORDER BY id"
    ).fetchall()
    con.close()

    os.makedirs(MEM_DIR, exist_ok=True)

    # Clear old exported md so deletions propagate.
    for name in os.listdir(MEM_DIR):
        if name.endswith(".md"):
            os.remove(os.path.join(MEM_DIR, name))

    jsonl_lines = []
    for mid, text, tags, pinned, created, updated in rows:
        slug = slugify(text)
        path = os.path.join(MEM_DIR, f"{mid:04d}-{slug}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"id: {mid}\n")
            f.write(f"tags: {tags}\n")
            f.write(f"pinned: {'true' if pinned else 'false'}\n")
            f.write(f"created_at: {iso(created)}\n")
            f.write(f"updated_at: {iso(updated)}\n")
            f.write("---\n\n")
            f.write(text.rstrip() + "\n")
        jsonl_lines.append(json.dumps(
            {
                "id": mid,
                "text": text,
                "tags": tags,
                "pinned": bool(pinned),
                "created_at": created,
                "updated_at": updated,
            },
            ensure_ascii=False,
        ))

    with open(os.path.join(REPO, "memories.jsonl"), "w", encoding="utf-8") as f:
        f.write("\n".join(jsonl_lines) + ("\n" if jsonl_lines else ""))

    # Copy skills verbatim (they are plain text dirs).
    skills_dst = os.path.join(REPO, "skills")
    if os.path.isdir(skills_dst):
        shutil.rmtree(skills_dst)
    if os.path.isdir(SKILLS):
        shutil.copytree(SKILLS, skills_dst)

    print(f"exported {len(rows)} memories + skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
