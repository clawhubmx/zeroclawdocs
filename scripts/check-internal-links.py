#!/usr/bin/env python3
"""
Fail if any Markdown link uses an absolute site path (/foo) that does not exist.

Excludes http(s) and // URLs. Complements verify-docs-json.py (sidebar slugs).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent

    valid: set[str] = set()
    for p in root.rglob("*"):
        if p.suffix.lower() not in (".md", ".mdx"):
            continue
        if "node_modules" in p.parts or ".git" in p.parts:
            continue
        rel = p.relative_to(root)
        if rel.name in ("index.md", "index.mdx"):
            s = str(rel.parent.as_posix())
        else:
            s = str(rel.with_suffix("")).replace("\\", "/")
        valid.add("/" + s)

    link_re = re.compile(r"\]\((/[^)\s#\"]+)")
    broken: list[tuple[str, str]] = []
    for p in root.rglob("*"):
        if p.suffix.lower() not in (".md", ".mdx"):
            continue
        if "node_modules" in p.parts or ".git" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in link_re.finditer(text):
            href = m.group(1).rstrip("/")
            if href.startswith("//"):
                continue
            if href not in valid:
                broken.append((str(p.relative_to(root)), href))

    if broken:
        print("Broken internal links (no matching page):", file=sys.stderr)
        for path, href in sorted(set(broken)):
            print(f"  {path}: {href}", file=sys.stderr)
        return 1

    print(f"OK: internal / links resolve ({len(valid)} routes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
