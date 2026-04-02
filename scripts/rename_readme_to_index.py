#!/usr/bin/env python3
"""
Rename docs/**/README.md -> docs/**/index.md so Mintlify serves /docs/foo not /docs/foo/README.

Run after moving docs/README.md -> hub.md. Skips files whose path contains structure-README.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    dest = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("docs").resolve()
    if not dest.is_dir():
        print(f"error: not a directory: {dest}", file=sys.stderr)
        return 1

    for path in sorted(dest.rglob("README.md")):
        if "structure-README" in path.name:
            continue
        target = path.with_name("index.md")
        if target.exists() and target != path:
            print(f"skip (exists): {target}", file=sys.stderr)
            continue
        path.rename(target)
        print(f"renamed {path} -> {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
