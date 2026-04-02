# ZeroClaw documentation site

This repository publishes [Mintlify](https://mintlify.com) documentation for [ZeroClaw](https://github.com/morpheum-labs/zeroclaw). Page content is **synced from** `zeroclaw/docs` so the on-disk layout matches the main repository (`docs/setup-guides`, `docs/reference`, `docs/ops`, and so on).

## Prerequisites

- A clone of [`zeroclaw`](https://github.com/morpheum-labs/zeroclaw) (default: `../zeroclaw` next to this repo)
- [Mintlify CLI](https://www.npmjs.com/package/mint) for local preview (`npm i -g mint`)

## Sync documentation from zeroclaw

From the root of this repository:

```bash
bash scripts/sync-from-zeroclaw.sh /path/to/zeroclaw
```

This script:

1. Rsyncs English canonical files from `zeroclaw/docs/` into `./docs/` (excluding `vi/`, `i18n/`, and locale-suffixed files).
2. Renames `docs/README.md` → `docs/hub.md` (Mintlify ignores root `README.md`; the hub needs a stable slug).
3. Renames each `docs/**/README.md` → `docs/**/index.md` so section URLs are `/docs/<section>` (not `/docs/<section>/README`), matching how Mintlify resolves folder indexes.
4. Copies `zeroclaw/README.md` → `zeroclaw-readme.md` for the install / quick start page.
5. Rewrites Markdown links to Mintlify paths and strips legacy `/README` suffixes from internal links.
6. Applies small public-site patches (hub locale line, `docs/SUMMARY.md` stub, `docs/architecture/index.md` stub if needed, frontmatter on `zeroclaw-readme.md`).

Commit the updated `./docs/` and `zeroclaw-readme.md` after review.

## Checks

Confirm every `docs.json` navigation entry exists on disk (CI runs this on every PR):

```bash
python3 scripts/verify-docs-json.py
python3 scripts/find-orphan-pages.py --strict
python3 scripts/check-internal-links.py
```

`find-orphan-pages.py` ensures every `.md`/`.mdx` under `docs/` (plus `index` and `zeroclaw-readme`) appears in `docs.json`, so new upstream files are not left out of the sidebar.

## Local preview

```bash
mint dev
```

Open `http://localhost:3000`.

## Deployment

Connect the repository to the [Mintlify dashboard](https://dashboard.mintlify.com) so pushes to the default branch deploy the site.
