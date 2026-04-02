#!/usr/bin/env python3
"""
Verify every navigation page in docs.json exists as a .md or .mdx file under the site root.
Exit 1 with details if anything is missing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def iter_pages(nav: dict) -> list[str]:
    out: list[str] = []
    tabs = nav.get("tabs") or []
    for tab in tabs:
        for group in tab.get("groups") or []:
            for p in group.get("pages") or []:
                out.append(p)
    return out


def resolve_page(site_root: Path, slug: str) -> Path | None:
    """Return path if slug exists as a page file or docs/foo/index.md."""
    for ext in (".mdx", ".md"):
        candidate = site_root / f"{slug}{ext}"
        if candidate.is_file():
            return candidate
    for ext in (".mdx", ".md"):
        idx = site_root / slug / f"index{ext}"
        if idx.is_file():
            return idx
    return None


def main() -> int:
    site_root = Path(__file__).resolve().parent.parent
    docs_json = site_root / "docs.json"
    data = json.loads(docs_json.read_text(encoding="utf-8"))
    pages = iter_pages(data.get("navigation") or {})
    missing: list[str] = []
    for slug in pages:
        if resolve_page(site_root, slug) is None:
            missing.append(slug)

    if missing:
        print("Missing pages (expected .md or .mdx next to docs.json):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print(f"OK: {len(pages)} navigation pages found on disk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
