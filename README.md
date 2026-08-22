# NEXUS

![Protocol](https://img.shields.io/badge/protocols-29-2563eb)
![Registry](https://img.shields.io/badge/federation-22%20components-7c3aed)
![Operator](https://img.shields.io/badge/operator-ecosystemctl-059669)
![Runtime](https://img.shields.io/badge/runtime-provider--neutral-0f766e)

**NEXUS is the machine-readable federation and protocol authority for the ItsNotAI Labs runtime ecosystem.**

It discovers components, routes work, compiles bounded multi-repo plans, validates protocol objects, correlates receipts, exposes activation gaps and keeps each runtime inside a clear responsibility plane.

```text
Intent
  │
  ▼
Discover capabilities
  │
  ▼
Route + policy + budget
  │
  ▼
Compile nexus.plan.v1
  │
  ├── POCKET Host       identity / tenant / policy
  ├── Pocket Voice      conversational control
  ├── POCKET Agent      long-running execution
  ├── MatDaemon         bounded compute
  ├── CAPSULA           isolated runtime / build
  ├── Medina Memory     durable continuity
  ├── AURO / MESIE      model runtime
  ├── Connectors        external worker surfaces
  ├── Research          evidence / artifacts
  └── PARRALAX          finance / clearing planes
  │
  ▼
Artifact + receipt + audit + memory + handoff
```

## Operator quick start

Validate the federation:

```bash
python tools/validate_ecosystem_protocols.py
python tools/validate_ecosystem_registry.py
python tools/validate_ecosystem_flow.py
```

Inspect components:

```bash
python tools/ecosystemctl.py list
python tools/ecosystemctl.py describe pocket-agent
python tools/ecosystemctl.py gaps
```

Route an intent:

```bash
python tools/ecosystemctl.py route "run a bounded matrix benchmark"
```

Compile a multi-component plan:

```bash
python tools/ecosystemctl.py plan \
  "audit this repository and produce a release artifact" \
  --tenant acme \
  --principal user-123 \
  --project platform
```

The plan compiler emits a `nexus.plan.v1` object containing deterministic correlation IDs, selected component/action, scope, risk tier, policy decision, approval requirement, execution budget, ordered dependencies and acceptance gates.

## Protocol spine

NEXUS currently defines **29 shared contracts**.

### Discovery and identity

```text
nexus.capability.v1
nexus.identity-ref.v1
nexus.compatibility.v1
```

### Work and orchestration

```text
nexus.task.v1
nexus.plan.v1
nexus.job.v1
nexus.handoff.v1
nexus.event.v1
```

### Policy and control

```text
nexus.policy-decision.v1
nexus.approval.v1
nexus.denial.v1
nexus.budget.v1
nexus.quota.v1
nexus.feature-flag.v1
```

### Resilience

```text
nexus.idempotency.v1
nexus.lease.v1
nexus.retry-policy.v1
nexus.circuit-breaker.v1
nexus.incident.v1
```

### Context and memory

```text
nexus.context-pack.v1
nexus.memory-event.v1
nexus.retention-policy.v1
nexus.secret-ref.v1
```

### Evidence and operations

```text
nexus.artifact.v1
nexus.execution-receipt.v1
nexus.audit-event.v1
nexus.health.v1
nexus.telemetry.v1
nexus.release-evidence.v1
```

The canonical machine-readable registry is [`protocols/ecosystem.protocols.json`](protocols/ecosystem.protocols.json).

## Federation registry

[`registry/ecosystem-alpha.json`](registry/ecosystem-alpha.json) classifies components by plane, authority and maturity instead of assuming every repository is interchangeable.

The integrated graph includes the POCKET family plus model, compute, capsule, memory, connector, workflow, research, security, mobile, finance, clearing, builder and deployment surfaces.

Current core lanes:

| Plane | Component |
|---|---|
| federation | NEXUS |
| user/team/policy | POCKET Host |
| voice/conversation | Pocket Voice |
| execution | POCKET Agent |
| compute | MatDaemon |
| execution capsule | CAPSULA |
| memory | Medina Memory Systems |
| model | AURO / MESIE / Auro model family |
| connector | NOVA Connector Control Plane / x-mcp-skills |
| SDK | PhantomSDK |
| workflow | Organism Bots |
| research | ResearchersHub |
| device control | PhoneAI |
| security | CyberSecurity-AI / CHIMERIA bridge |
| market execution | PARRALAX |
| clearing | PARALLAX Exchange Clearinghouse |
| builder | Sovereign Forge |
| deployment | NOVA app containers |

## Ecosystem control loop

```text
Discover
  -> Route
  -> Decide
  -> Approve when needed
  -> Reserve budget / quota / lease
  -> Execute
  -> Observe health / telemetry
  -> Produce artifact + receipt
  -> Evaluate outcome
  -> Persist durable lesson when useful
  -> Handoff
```

This loop is intentionally component-neutral. A voice interaction, coding job, model benchmark, container build and market simulation can all use the same correlation and evidence semantics without becoming the same application.

## Runtime protocol validation

NEXUS includes generic validation for wire objects before they cross component boundaries.

Validation covers:

- known protocol schema IDs;
- required fields;
- request correlation;
- tenant correlation;
- execution-receipt digests;
- policy object structure;
- health object structure;
- secret-reference semantics;
- prohibited secret-value fields;
- prohibited private-reasoning fields.

This gives SDKs, gateways and workers a shared validation target instead of duplicating protocol assumptions.

## End-to-end fixture

The repository includes a synthetic federation fixture that exercises:

```text
Pocket Voice context
  -> POCKET policy
  -> NEXUS route
  -> bounded execution
  -> MatDaemon artifact
  -> execution receipt
  -> memory event
  -> handoff
```

The validator checks correlation and protocol compatibility across the complete packet.

## Active engineering lanes

NEXUS maps system work into explicit engineering responsibilities:

| Lane | Focus |
|---|---|
| Systems Architect | protocol and ownership coherence |
| Drift Detector | declared vs observed capability drift |
| Correction Engine | CI/release debt and regressions |
| Red Team | tenant, denial and irreversible-action paths |
| MATHESIS | budgets, bounds, latency and cost |
| Resource Hub | registry, discovery and knowledge structure |
| Execution Governor | jobs, leases, idempotency and resilience |
| Data Governance | context, memory, provenance and retention |
| Human Approval | privileged / irreversible checkpoints |
| Model Intelligence | AURO/MESIE capability and evidence |
| Voice / Multimodal | Pocket Voice integration |
| SDK / Connector | external developer and worker ecosystem |
| Device | PhoneAI |
| Finance / Clearing | PARRALAX and settlement protocols |
| Security | public defensive and CHIMERIA bridge surfaces |

See the engineering workstream documents in this repository for the current acceptance gates.

## Production integration pattern

A component joining NEXUS should expose an `ecosystem.surface.json` containing:

```text
schema
component
repo
plane
status
authority
actions
consumes
produces
limits
```

Promotion is based on concrete interoperability:

```text
activation-candidate
  -> protocol-ready
  -> active
```

A protocol-ready component declares its surface and validates its manifest. An active component additionally demonstrates real cross-component request/receipt flow.

## MDFUC

NEXUS also retains the **Medina Development Federation Unified Catalog (MDFUC)** for repository and artifact lineage.

Key files:

```text
mdfuc.catalog.json
registry/repo-family.json
registry/artifacts-v0.3.8.json
docs/MDFUC.md
tools/validate_mdfuc_catalog.py
```

The ecosystem protocol registry is the broader runtime federation layer; MDFUC remains useful for release/artifact lineage.

## Repository map

```text
protocols/
  ecosystem.protocols.json
registry/
  ecosystem-alpha.json
  repo-family.json
examples/
  ecosystem-flow.json
tools/
  ecosystemctl.py
  validate_ecosystem_protocols.py
  validate_ecosystem_registry.py
  validate_ecosystem_flow.py
  validate_protocol_object.py
  validate_mdfuc_catalog.py
docs/
.github/workflows/
```

## CI / release gates

The ecosystem workflow is designed to run:

```bash
python tools/validate_ecosystem_protocols.py
python tools/validate_ecosystem_registry.py
python tools/validate_ecosystem_flow.py
cd tools && python test_ecosystemctl.py
```

Legacy MDFUC validation is kept separate so old catalog debt cannot hide the status of new federation contracts.

## Build products against NEXUS

NEXUS is not a UI product that replaces POCKET. It is the interoperability substrate used by:

- POCKET APIs and enterprise routing;
- POCKET Agent execution clients;
- Pocket Voice context/handoff;
- PhantomSDK clients;
- connector/MCP workers;
- model and compute runtimes;
- receipt/audit dashboards;
- deployment and release tooling.

The core design goal is simple: **every component remains specialized, but work can move between them with the same identity, policy, budget, evidence and recovery semantics.**
