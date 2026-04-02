#!/usr/bin/env python3
"""Post-sync fixes for the public Mintlify site (broken locale links, SUMMARY stub)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ARCH_README = """# Architecture

This section currently includes ADRs and diagrams mirrored from the repository.

- [ADR 004 — tool shared state ownership](/docs/architecture/adr-004-tool-shared-state-ownership)
- [Architecture diagrams](/docs/assets/architecture-diagrams)
"""

SUMMARY_STUB = """# Summary (table of contents)

The canonical unified TOC (`SUMMARY.md`) lives in the [zeroclaw repository](https://github.com/zeroclaw/zeroclaw/tree/master/docs).

Use this site’s sidebar for navigation, or return to the [documentation hub](/docs/hub).
"""

LOCALE_BLOCK = re.compile(
    r"\nLocalized hubs:\n[^\n]+\n",
    re.MULTILINE,
)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    hub = root / "docs" / "hub.md"
    if hub.is_file():
        text = hub.read_text(encoding="utf-8")
        replacement = (
            "\n**Other languages:** locale hubs ship in the "
            "[zeroclaw `docs/` tree on GitHub](https://github.com/zeroclaw/zeroclaw/tree/master/docs) "
            "(see `README.*.md` files).\n\n"
        )
        text, n = LOCALE_BLOCK.subn(replacement, text, count=1)
        if n:
            hub.write_text(text, encoding="utf-8")
        # i18n tree is not synced; avoid 404 to /docs/i18n
        text = hub.read_text(encoding="utf-8")
        text = text.replace(
            "](/docs/i18n)",
            "](https://github.com/zeroclaw/zeroclaw/tree/master/docs/i18n)",
        )
        hub.write_text(text, encoding="utf-8")

    (root / "docs" / "SUMMARY.md").write_text(SUMMARY_STUB, encoding="utf-8")

    arch_index = root / "docs" / "architecture" / "index.md"
    arch_index.parent.mkdir(parents=True, exist_ok=True)
    if not arch_index.is_file():
        arch_index.write_text(ARCH_README, encoding="utf-8")

    zr = root / "zeroclaw-readme.md"
    if zr.is_file() and not zr.read_text(encoding="utf-8").startswith("---"):
        zr.write_text(
            '---\ntitle: "ZeroClaw — repository README"\ndescription: "Install, quick start, and project overview"\n---\n\n'
            + zr.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
