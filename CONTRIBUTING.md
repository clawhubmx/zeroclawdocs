# Contributing to this documentation site

Most prose **lives in the [zeroclaw](https://github.com/zeroclaw/zeroclaw) repository** under `docs/`. Edit there first, then refresh this site with the sync script (or open a PR that runs the sync after upstream merges).

## Change content

1. Clone [zeroclaw/zeroclaw](https://github.com/zeroclaw/zeroclaw) and edit files under `docs/` following that repo’s guidelines.
2. In this repo, run `bash scripts/sync-from-zeroclaw.sh /path/to/zeroclaw` and commit the updated `./docs/` tree and `zeroclaw-readme.md`.
3. If you add new sections or filenames, update `docs.json` navigation.

## Change site chrome only (Mintlify)

Navigation, branding, and landing copy live here (`docs.json`, `index.mdx`, logos). Use `mint dev` from this repository root to preview.
