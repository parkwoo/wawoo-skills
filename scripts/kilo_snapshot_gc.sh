#!/usr/bin/env bash
# kilo snapshot の stale な git index.lock を掃除し、auto GC する。
# 既定は dry-run。--apply で実際に削除・GC する。
#
#   scripts/kilo_snapshot_gc.sh                 # dry-run（対象の表示のみ）
#   scripts/kilo_snapshot_gc.sh --apply         # 除去 + git gc --auto
#   scripts/kilo_snapshot_gc.sh --dir DIR --min-age 60
#
# 背景: kilo の snapshot は <KILO_SNAPSHOT_DIR>/<projectID>/<dir> を git ディレクトリとして持つ。
# 前回プロセス異常終了などで index.lock が残ると "failed to add snapshot files" (exitCode=128)
# が発生する（run c956c7f2 の WARN 2 件）。
set -euo pipefail

SNAP_DIR="${KILO_SNAPSHOT_DIR:-$HOME/.local/share/kilo/snapshot}"
APPLY=0
MIN_AGE=60

usage() { echo "usage: $0 [--apply] [--dir DIR] [--min-age SEC]"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --dir) SNAP_DIR="${2:?--dir requires a value}"; shift ;;
    --min-age) MIN_AGE="${2:?--min-age requires a value}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

[ -d "$SNAP_DIR" ] || { echo "no snapshot dir: $SNAP_DIR"; exit 0; }

now=$(date +%s)
removed=0; skipped=0; gced=0
mode=DRY-RUN; [ "$APPLY" -eq 1 ] && mode=APPLY

# 1) stale index.lock の走査
while IFS= read -r lock; do
  [ -n "$lock" ] || continue
  mtime=$(stat -c %Y "$lock" 2>/dev/null || echo "$now")
  age=$(( now - mtime ))
  if [ "$age" -lt "$MIN_AGE" ]; then
    echo "SKIP (fresh ${age}s): $lock"
    skipped=$((skipped + 1))
    continue
  fi
  if [ "$APPLY" -eq 1 ]; then
    rm -f "$lock"
    echo "REMOVED (${age}s): $lock"
  else
    echo "WOULD REMOVE (${age}s): $lock"
  fi
  removed=$((removed + 1))
done < <(find "$SNAP_DIR" -name index.lock -type f 2>/dev/null)

# 2) git ディレクトリ（HEAD と objects を持つ）で auto GC
if [ "$APPLY" -eq 1 ]; then
  while IFS= read -r head; do
    [ -n "$head" ] || continue
    gitdir=$(dirname "$head")
    [ -d "$gitdir/objects" ] || continue
    if git --git-dir="$gitdir" gc --auto --quiet 2>/dev/null; then
      gced=$((gced + 1))
    fi
  done < <(find "$SNAP_DIR" -maxdepth 3 -name HEAD -type f 2>/dev/null)
fi

echo "== kilo_snapshot_gc ($mode): locks=$removed skipped=$skipped gced=$gced dir=$SNAP_DIR"
