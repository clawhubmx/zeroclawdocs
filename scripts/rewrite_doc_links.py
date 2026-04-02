#!/usr/bin/env python3
"""
Rewrite relative Markdown links for Mintlify after sync-from-zeroclaw.sh.

Section indexes use index.md (renamed from README.md) so routes are /docs/foo not /docs/foo/README.

Expected layout:
  SITE_ROOT/docs/              — mirror of zeroclaw/docs (hub = docs/hub.md)
  SITE_ROOT/zeroclaw-readme.md — copy of zeroclaw/README.md
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

DEFAULT_README_URL = "https://github.com/morpheum-labs/zeroclaw/blob/master/README.md"


def normalize_absolute_href(href: str) -> str:
    """Strip trailing /README from Mintlify paths (not structure-README)."""
    if "structure-README" in href:
        return href
    anchor = ""
    path = href
    if "#" in href:
        path, _, rest = href.partition("#")
        anchor = "#" + rest
    while path.endswith("/README"):
        path = path[: -len("/README")]
    return path + anchor


def to_mint(rel_site: Path) -> str:
    """Path under site root -> Mintlify slug."""
    name = rel_site.name
    if name in ("index.md", "index.mdx"):
        return "/" + rel_site.parent.as_posix()
    if name == "README.md":
        return "/" + rel_site.parent.as_posix()
    suf = rel_site.suffix.lower()
    if suf in (".md", ".mdx"):
        return "/" + rel_site.with_suffix("").as_posix()
    return "/" + rel_site.as_posix()


def href_to_readme_or_index(base_dir: Path, href: str) -> str:
    """Point README.md links at index.md after rename."""
    if href.endswith("README.md"):
        return href[: -len("README.md")] + "index.md"
    return href


def main() -> int:
    site_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent.parent
    )
    docs_dir = site_root / "docs"
    hub_path = docs_dir / "hub.md"
    repo_readme = site_root / "zeroclaw-readme.md"
    fallback_url = os.environ.get("ZEROCLAW_GITHUB_README_URL", DEFAULT_README_URL)

    link_re = re.compile(r"\]\(([^)]+)\)")

    def rewrite_file(path: Path) -> None:
        text = path.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            inner = m.group(1).strip()
            if inner.startswith(("#", "http://", "https://", "mailto:")):
                return m.group(0)

            # Absolute site paths: normalize .../README -> section root (not // URLs)
            if inner.startswith("/") and not inner.startswith("//"):
                return f"]({normalize_absolute_href(inner)})"

            anchor = ""
            href = inner
            if "#" in href and not href.startswith("#"):
                i = href.index("#")
                href, anchor = href[:i], href[i:]

            if not href or href.startswith("#"):
                return m.group(0)

            href = href_to_readme_or_index(path.parent, href)
            base_dir = path.parent
            resolved = (base_dir / href).resolve()

            try:
                rel_site = resolved.relative_to(site_root)
            except ValueError:
                return f"]({fallback_url}{anchor})"

            # docs/README.md (hub) — file renamed to hub.md
            if rel_site == Path("docs/README.md") or (
                hub_path.exists() and resolved == hub_path.resolve()
            ):
                return f"]({to_mint(Path('docs/hub.md'))}{anchor})"

            # Repository root README (physical copy)
            if rel_site == Path("README.md"):
                if repo_readme.exists():
                    return f"]({to_mint(Path('zeroclaw-readme.md'))}{anchor})"
                return f"]({fallback_url}{anchor})"

            if rel_site.suffix.lower() not in (".md", ".mdx"):
                return m.group(0)
            if rel_site.parts and rel_site.parts[0] == "scripts":
                return m.group(0)

            return f"]({to_mint(rel_site)}{anchor})"

        new_text = link_re.sub(repl, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")

    for p in site_root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".mdx"}:
            continue
        if "scripts" in p.parts or p.name.startswith("."):
            continue
        rewrite_file(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
