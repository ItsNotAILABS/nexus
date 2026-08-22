# NEXUS Ecosystem Intelligence Protocols

This document defines the practical interoperability spine for the ItsNotAI Labs repo ecosystem. It is intentionally narrower than a monolithic OS: each repository keeps a clear responsibility and exchanges only bounded, typed state.

## Core rule

A repository may be intelligent without becoming sovereign over the whole system. Cross-repo intelligence is expressed through **capabilities, tasks, policy decisions, context packs, memory events, artifacts, receipts, health, telemetry, compatibility and handoffs**.

## Intelligence loop

```text
Discover -> Route -> Decide -> Budget -> Execute -> Observe -> Receipt -> Learn -> Handoff
```

1. `nexus.capability.v1` describes what a component can actually do.
2. `nexus.task.v1` submits bounded work.
3. `nexus.policy-decision.v1` gates privileged action.
4. `nexus.budget.v1` constrains resource use.
5. `nexus.context-pack.v1` carries curated working context.
6. The component executes inside its own responsibility boundary.
7. `nexus.telemetry.v1` and `nexus.health.v1` expose operational state.
8. `nexus.execution-receipt.v1` and `nexus.artifact.v1` prove outcomes.
9. `nexus.memory-event.v1` records durable lessons/outcomes when appropriate.
10. `nexus.handoff.v1` transfers the next responsibility explicitly.

## Practical feature families

### Capability discovery
Every service or CLI should expose a stable capability descriptor. Minimum useful fields:

- component/repository identity
- role/plane
- actions
- input/output schemas
- risk tier per action
- limits and quotas
- dependencies
- produced/consumed protocol versions
- proof state (`source`, `tested`, `preview`, `hosted`)

### Budgets
Long-running agents and external workers should receive explicit limits instead of vague autonomy:

- wall-clock seconds
- model tokens
- monetary budget (when measurable)
- file count and changed-byte budget
- subprocess count
- external network calls
- recursive child-agent count
- artifact bytes

Exceeding a budget returns a receipt with `status=budget_exhausted`; it does not silently continue.

### Context packs
Context is curated, scoped and provenance-bearing. A context item should identify:

- type: file, code selection, note, memory, artifact, URL reference, telemetry snapshot
- locator/name
- content or digest reference
- sensitivity/retention class
- provenance
- relevance reason

Do not serialize hidden model reasoning as context.

### Memory events
Memory is event-driven, not an unbounded dump. Useful kinds include:

- decision
- outcome
- correction
- preference (non-sensitive only)
- benchmark result
- incident lesson
- compatibility finding
- release evidence

Each event has provenance, scope and retention class so consumers can decide whether to persist it.

### Policy decisions
Privileged actions must produce one of:

- `allow`
- `deny`
- `confirm`

A decision includes policy ID, reasons, actor/scope correlation and expiration when relevant. Denials produce `nexus.denial.v1` so UIs and agents can explain the boundary without scraping logs.

### Receipts
Receipts prove operational events without exposing private reasoning. Recommended fields:

- request ID / trace ID
- component
- action
- status
- start/finish/runtime
- policy decision reference
- budget consumed
- artifact IDs/hashes
- sanitized error code
- digest

### Health and degradation
`nexus.health.v1` distinguishes:

- `healthy`
- `degraded`
- `not_ready`
- `unavailable`

Dependencies are reported individually. A service should not report healthy because the HTTP process is alive while its required storage/provider is unavailable.

### Compatibility
Every component publishes protocols produced and consumed. Breaking changes require a new protocol version rather than silent payload drift.

## Repository role map

| Repository | Primary role | Protocol emphasis |
|---|---|---|
| `nexus` | federation registry / protocol authority | all registry + compatibility |
| `pocket` | user/org identity, routing, policy, product host | task, policy, capability, health, audit |
| `pocket-agent` | long-running execution | task, budget, receipt, artifact, memory-event |
| `pocket-voice-to-text` | conversational/voice control | context-pack, telemetry, health, handoff |
| `nova-intelligence` | intelligence contracts / research proof | capability, compatibility, release-evidence |
| `PhantomSDK` | external SDK packaging | capability, compatibility, schema clients |
| `x-mcp-skills` | connector control plane | capability, policy, handoff, denial |
| `organism-bots-mcp-server` | governed workflow organisms | task, policy, receipt, handoff |
| `MatDaemon` | bounded compute | capability, task, budget, telemetry, receipt |
| `CAPSULA` | isolated runtime/deploy capsules | task, policy, budget, artifact, receipt |
| `MedinaMemorySystems` / Loom memory | durable memory plane | memory-event, context-pack, artifact |
| `AURO` / `Auro14B` | model runtime lanes | capability, telemetry, release-evidence |

## Intelligence features to implement across products

The following are deliberately practical rather than speculative:

1. **Intent router with confidence and fallback** — chooses component/action from capability registry; low confidence returns alternatives rather than guessing.
2. **Plan compiler** — converts a high-level request into typed tasks with dependencies, budgets and proof gates.
3. **Execution governor** — enforces risk tier, tenant scope, budget and confirmation requirements.
4. **Context assembler** — selects the smallest relevant context pack using provenance and recency.
5. **Outcome evaluator** — checks artifacts/tests/receipts against the requested acceptance criteria.
6. **Drift detector** — compares protocol versions, declared capabilities and actual receipts to find stale claims.
7. **Recovery planner** — turns failures into retry/fallback/handoff recommendations without retry storms.
8. **Cost/latency planner** — selects local/remote/model/compute path based on budgets and readiness.
9. **Human checkpoint generator** — asks for approval only at irreversible/high-risk boundaries.
10. **Release truth classifier** — source/test/preview/hosted status derived from evidence rather than README adjectives.

## Enterprise requirements

- Tenant/user/device/session scope survives every hop.
- Secrets are references or server-side bindings, never protocol payloads.
- PII and sensitive content require explicit retention classes.
- Every externally reachable mutating action has auth, rate limit and denial behavior.
- Every privileged execution path has a receipt.
- Cross-repo failures are isolated; one unavailable component should degrade a plan rather than corrupt state.
- Protocol validators run in CI.

## Alpha success criterion

The ecosystem reaches integrated Alpha when at least one end-to-end flow can be reproduced:

```text
POCKET request
  -> capability discovery
  -> policy decision
  -> Pocket Voice context or POCKET Agent task
  -> optional MatDaemon/CAPSULA subtask
  -> artifact + receipt
  -> memory/outcome event
  -> POCKET result
```

with the same request/tenant/session correlation and machine-valid protocol objects at each boundary.
