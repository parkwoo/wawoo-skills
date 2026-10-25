#!/usr/bin/env bash
# internal.example → internal/（git 管理外）に配置
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/internal.example"
DST="${ROOT}/internal"

if [[ ! -d "$SRC" ]]; then
  echo "missing: $SRC" >&2
  exit 1
fi

mkdir -p "$DST"
rsync -a --delete "${SRC}/" "${DST}/"
echo "OK: ${DST}/ を更新（git 管理外）"
