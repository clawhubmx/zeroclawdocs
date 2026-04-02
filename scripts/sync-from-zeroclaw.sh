#!/usr/bin/env bash
# Sync English canonical documentation from the zeroclaw repo into this site.
# Preserves the zeroclaw/docs/ directory layout under ./docs/
#
# Usage:
#   bash scripts/sync-from-zeroclaw.sh [PATH_TO_ZEROCLAW_REPO]
# Default: ../zeroclaw (sibling of zeroclawdocs)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ZEROCLAW="${1:-${SITE_ROOT}/../zeroclaw}"
SRC_DOCS="${ZEROCLAW}/docs"
DEST="${SITE_ROOT}/docs"

if [[ ! -d "${SRC_DOCS}" ]]; then
  echo "error: missing docs directory: ${SRC_DOCS}" >&2
  echo "Clone https://github.com/zeroclaw/zeroclaw next to this repo or pass its path." >&2
  exit 1
fi

mkdir -p "${DEST}"
rsync -a --delete \
  --exclude-from="${SCRIPT_DIR}/sync-excludes.txt" \
  "${SRC_DOCS}/" "${DEST}/"

# Mintlify ignores root README.md; avoid name clash with repo README copy.
if [[ -f "${DEST}/README.md" ]]; then
  mv "${DEST}/README.md" "${DEST}/hub.md"
fi

# Section indexes: README.md -> index.md so routes are /docs/foo not /docs/foo/README
python3 "${SCRIPT_DIR}/rename_readme_to_index.py" "${DEST}"

# Main repository README (install, quick start) — not the docs hub.
cp "${ZEROCLAW}/README.md" "${SITE_ROOT}/zeroclaw-readme.md"

python3 "${SCRIPT_DIR}/rewrite_doc_links.py" "${SITE_ROOT}"
python3 "${SCRIPT_DIR}/patch_after_sync.py" "${SITE_ROOT}"

echo "Synced from ${SRC_DOCS} -> ${DEST}"
echo "Added ${SITE_ROOT}/zeroclaw-readme.md from ${ZEROCLAW}/README.md"
