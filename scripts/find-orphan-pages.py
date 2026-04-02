#!/usr/bin/env python3
"""
List Markdown/MDX files under the site that are not listed in docs.json navigation.

Use after `sync-from-zeroclaw.sh` so new upstream files are not forgotten in the sidebar.

Examples:
  python3 scripts/find-orphan-pages.py           # print list, exit 0
  python3 scripts/find-orphan-pages.py --strict  # exit 1 if any orphan exists
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def iter_nav_slugs(nav: dict) -> set[str]:
    slugs: set[str] = set()
    for tab in nav.get("tabs") or []:
        for group in tab.get("groups") or []:
            for p in group.get("pages") or []:
                slugs.add(p)
    return slugs


def iter_content_slugs(site_root: Path) -> list[str]:
    """Slugs for discoverable pages (same convention as Mintlify paths in docs.json)."""
    slugs: list[str] = []
    for pattern in ("docs/**/*.md", "docs/**/*.mdx"):
        for path in sorted(site_root.glob(pattern)):
            rel = path.relative_to(site_root)
            slug = str(rel.with_suffix("")).replace("\\", "/")
            slugs.append(slug)
    for name in ("index.mdx", "zeroclaw-readme.md"):
        p = site_root / name
        if p.is_file():
            rel = p.relative_to(site_root)
            slug = str(rel.with_suffix("")).replace("\\", "/")
            slugs.append(slug)
    return slugs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 if any orphan files exist.",
    )
    args = parser.parse_args()

    site_root = Path(__file__).resolve().parent.parent
    data = json.loads((site_root / "docs.json").read_text(encoding="utf-8"))
    nav = iter_nav_slugs(data.get("navigation") or {})

    orphans = sorted(set(iter_content_slugs(site_root)) - nav)

    if not orphans:
        print("No orphan pages: every synced .md/.mdx is listed in docs.json.")
        return 0

    print(
        f"{len(orphans)} file(s) on disk are not in docs.json navigation:",
        file=sys.stderr,
    )
    for o in orphans:
        print(f"  + {o}", file=sys.stderr)

    if args.strict:
        print(
            "\nAdd these slugs to docs.json (or exclude intentionally), then re-run.",
            file=sys.stderr,
        )
        return 1

    print(
        f"\nTip: add them to docs.json or run with --strict in CI once the nav is updated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
