# Nexus

![Status](https://img.shields.io/badge/status-production%20hardening-blue)
![MDFUC](https://img.shields.io/badge/MDFUC-registry%20authority-0b7285)
![Repos](https://img.shields.io/badge/active%20repos-5-6f42c1)
![Candidates](https://img.shields.io/badge/activation%20candidates-5-orange)
![Release](https://img.shields.io/badge/release-v0.3.8-2f9e44)
![Validator](https://img.shields.io/badge/validator-stdlib%20python-success)

Nexus is the registry and coordination authority for the NOVA repo family. It owns the **MDFUC** layer: Medina Development Federation Unified Catalog.

MDFUC tracks the repo family as one coordinated development organism, not scattered repositories.

## Search Keywords

NOVA registry, AI infrastructure registry, MCP repo family, agent platform registry, artifact lineage, runtime catalog, SDK coordination, workflow automation registry, sovereign AI development catalog.

## Active Repository Family

| Repository | Role |
| --- | --- |
| `ItsNotAILABS/nexus` | Registry, artifact lineage, repo-family coordination, MDFUC authority |
| `ItsNotAILABS/nova-intelligence` | Runtime contracts, engine doctrine, proof-bearing research papers |
| `ItsNotAILABS/PhantomSDK` | SDK packaging, release manifests, checksums, install contracts |
| `ItsNotAILABS/x-mcp-skills` | External AI connector control plane and MCP skill catalog |
| `ItsNotAILABS/organism-bots-mcp-server` | Organism Bots MCP server, bot registry, task receipts, runnable bot-control surface |

## Activation Candidates

| Repository | Intended Role |
| --- | --- |
| `ItsNotAILABS/nova-connector-control-plane` | Dedicated production home for connector routing, `connectorctl`, live MCP discovery, and artifact import dashboards |
| `ItsNotAILABS/mercatus-launch-studio` | Launch studio for product pages, pricing advisors, onboarding flows, creator profiles, and outreach guardrails |
| `ItsNotAILABS/specforge-launch-studio` | Click-only app specification builder and 10-section export studio |
| `ItsNotAILABS/MatDaemon` | AI-native matrix compute daemon, SDK, CLI, REST API, MCP server, benchmarks, and CUDA backend |
| `ItsNotAILABS/containers-nova-APPS` | Containerized NOVA app/runtime deployment surface |

## Quick Start

Validate the catalog locally:

```bash
python tools/validate_mdfuc_catalog.py
```

Inspect the core registry files:

```bash
cat mdfuc.catalog.json
cat registry/repo-family.json
cat registry/artifacts-v0.3.8.json
```

## Current Files

- `mdfuc.catalog.json` — machine-readable family catalog.
- `registry/repo-family.json` — active, watch, and ignored repo registry.
- `registry/artifacts-v0.3.8.json` — release artifact map and checksum ledger.
- `docs/MDFUC.md` — operator explanation of the coordination layer.
- `docs/PRODUCTION_READINESS.md` — production gates, launch levels, and discoverability guidance.
- `tools/validate_mdfuc_catalog.py` — dependency-free catalog validator.

## Operating Law

No repo is isolated. Every repo has a role, proof gate, handoff contract, and next gate. Nexus prevents repo-family fragmentation.

## Release Truth Line

The v0.3.8 zip artifacts are registered with checksums, but binary upload is still pending in PhantomSDK until a Git-capable lane or GitHub Release upload is used. Do not claim the binaries are committed until their upload status changes.

## GitHub Discoverability

Recommended repository topics:

`nova`, `ai-infrastructure`, `ai-agents`, `mcp`, `model-context-protocol`, `developer-tools`, `sdk`, `runtime-registry`, `artifact-registry`, `workflow-automation`, `sovereign-ai`.

## Next Gate

Add CI for `python tools/validate_mdfuc_catalog.py`, then seed activation candidates with role manifests and production READMEs before promoting them to active.
