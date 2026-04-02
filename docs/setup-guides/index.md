# Getting Started Docs

For first-time setup and quick orientation.

## Start Path

1. Main overview and quick start: [../../README.md](/zeroclaw-readme)
2. One-click setup and dual bootstrap mode: [one-click-bootstrap.md](/docs/setup-guides/one-click-bootstrap)
3. Update or uninstall on macOS: [macos-update-uninstall.md](/docs/setup-guides/macos-update-uninstall)
4. Find commands by tasks: [../reference/cli/commands-reference.md](/docs/reference/cli/commands-reference)

## Choose Your Path

| Scenario | Command |
|----------|---------|
| I have an API key, want fastest setup | `zeroclaw onboard --api-key sk-... --provider openrouter` |
| I want guided prompts | `zeroclaw onboard` |
| Config exists, just fix channels | `zeroclaw onboard --channels-only` |
| Config exists, I intentionally want full overwrite | `zeroclaw onboard --force` |
| Using subscription auth | See [Subscription Auth](/zeroclaw-readme#subscription-auth-openai-codex--claude-code) |

## Onboarding and Validation

- Quick onboarding: `zeroclaw onboard --api-key "sk-..." --provider openrouter`
- Guided onboarding: `zeroclaw onboard`
- Existing config protection: reruns require explicit confirmation (or `--force` in non-interactive flows)
- Ollama cloud models (`:cloud`) require a remote `api_url` and API key (for example `api_url = "https://ollama.com"`).
- Validate environment: `zeroclaw status` + `zeroclaw doctor`

## Next

- Runtime operations: [../ops/README.md](/docs/ops)
- Reference catalogs: [../reference/README.md](/docs/reference)
- macOS lifecycle tasks: [macos-update-uninstall.md](/docs/setup-guides/macos-update-uninstall)
