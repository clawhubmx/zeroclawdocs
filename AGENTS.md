# zeroclawdocs — agent notes

- This is a **Mintlify** site. Configuration: `docs.json`. Landing page: `index.mdx`. Section indexes are `docs/**/index.md` (sync renames `README.md` → `index.md` so routes are `/docs/<section>` not `/docs/<section>/README`).
- **Source of truth for prose** is the [`zeroclaw`](https://github.com/morpheum-labs/zeroclaw) repository under `docs/`. This repo mirrors that tree under `./docs/` plus `zeroclaw-readme.md` from the repo root README.
- After changing upstream docs, run `bash scripts/sync-from-zeroclaw.sh [path-to-zeroclaw]` and commit the resulting files. Update `docs.json` navigation if new top-level sections or files are added.
- Run `python3 scripts/verify-docs-json.py` so every sidebar slug matches a real `.md`/`.mdx` file.
- Run `python3 scripts/find-orphan-pages.py --strict` so every synced file is listed in `docs.json` (no orphan pages).
- Run `mint dev` to preview; use `mint broken-links` when the CLI is available.
- For Mintlify product behavior (components, `docs.json` schema), use the official Mintlify docs or `npx skills add https://mintlify.com/docs`.
