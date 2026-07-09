# Nexus Production Readiness

Nexus is the registry authority for the NOVA repo family. It should be treated as the coordination surface that prevents the ecosystem from fragmenting into unrelated repositories.

## Production Role

Nexus owns:

- MDFUC catalog authority
- repo-family membership and role map
- release artifact lineage
- active PR lineage
- cross-repo handoff contracts
- proof-gate inventory

## Current Readiness

| Gate | Status | Evidence |
| --- | --- | --- |
| Active repo catalog | Present | `mdfuc.catalog.json` |
| Repo-family registry | Present | `registry/repo-family.json` |
| v0.3.8 artifact map | Present | `registry/artifacts-v0.3.8.json` |
| Validation tool | Present | `tools/validate_mdfuc_catalog.py` |
| Binary artifact upload | Pending | PhantomSDK release zips still need Git-capable upload |
| CI validation | Pending | Add GitHub Actions after validator lands |

## Launch-Level Definition

- **L1 Registered**: repo appears in MDFUC catalog.
- **L2 Contracted**: repo has role, proof gates, handoffs, and next gate.
- **L3 Verifiable**: validator checks pass and artifact checksums exist.
- **L4 Operational**: CI validates catalog and release state on every PR.
- **L5 Marketable**: README, diagrams, docs, and public repo topics make the system easy to discover and understand.

## GitHub Discoverability

Recommended repository topics:

`nova`, `ai-infrastructure`, `ai-agents`, `mcp`, `model-context-protocol`, `developer-tools`, `sdk`, `runtime-registry`, `artifact-registry`, `workflow-automation`, `sovereign-ai`.

## Next Gates

1. Add CI for `python tools/validate_mdfuc_catalog.py`.
2. Update artifact upload status once PhantomSDK receives the binary zips or GitHub Release assets.
3. Add a `registry/status.json` dashboard for active PRs and release readiness.
4. Add repo topic instructions after the GitHub repo settings are available.
