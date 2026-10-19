#!/bin/bash
# Daily DSH memory backup: export to text, commit, push to GitHub.
# Safe to run while dsh web is live (read-only DB access).
set -euo pipefail

REPO="/Users/huangyingfeng/dsh-memory-backup"
cd "$REPO"

export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# 1. Export memories + skills into the repo tree.
/usr/bin/python3 "$REPO/export.py"

# 2. Stage everything.
git add -A

# 3. Commit only if there is a change.
if git diff --cached --quiet; then
    echo "no changes to back up"
    exit 0
fi

STAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
git commit -m "backup: dsh memories + skills @ $STAMP" >/dev/null

# 4. Push (non-fatal if remote not reachable yet).
if git remote get-url origin >/dev/null 2>&1; then
    if git push origin HEAD >/dev/null 2>&1; then
        echo "pushed to origin"
    else
        echo "push failed (will retry next run)" >&2
    fi
else
    echo "no origin remote configured" >&2
fi
