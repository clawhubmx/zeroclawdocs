# Operations & Deployment Docs

For operators running ZeroClaw in persistent or production-like environments.

## Core Operations

- Day-2 runbook: [./operations-runbook.md](/docs/ops/operations-runbook)
- Release runbook: [../contributing/release-process.md](/docs/contributing/release-process)
- Troubleshooting matrix: [./troubleshooting.md](/docs/ops/troubleshooting)
- Safe network/gateway deployment: [./network-deployment.md](/docs/ops/network-deployment)
- Mattermost setup (channel-specific): [../setup-guides/mattermost-setup.md](/docs/setup-guides/mattermost-setup)

## Common Flow

1. Validate runtime (`status`, `doctor`, `channel doctor`)
2. Apply one config change at a time
3. Restart service/daemon
4. Verify channel and gateway health
5. Roll back quickly if behavior regresses

## Related

- Config reference: [../reference/api/config-reference.md](/docs/reference/api/config-reference)
- Security collection: [../security/README.md](/docs/security/README)
