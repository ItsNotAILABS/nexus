# Ecosystem Alpha Engineering Workstreams

The ecosystem is developed as parallel responsibility lanes with one integration gate. These lanes are engineering roles, not independent sovereign agents: every change must land through repository review, protocol compatibility, tests/evidence and the authority boundaries in the NEXUS registry.

## 1. Systems Architect — protocol coherence

Owns:
- protocol versioning and schema compatibility;
- component authority boundaries;
- plan/task/handoff topology;
- prevention of duplicated control-plane responsibility.

Gate:
- no two components silently claim the same load-bearing authority;
- incompatible wire changes create a new protocol version.

## 2. Drift Detector — declared vs observed capability

Owns:
- `ecosystem.surface.json` vs runtime capability comparison;
- README/release claim vs evidence comparison;
- stale endpoint/action detection;
- protocol producer/consumer drift.

Gate:
- observed runtime cannot expose undeclared privileged actions without failing the release gate.

## 3. Correction Engine — failing CI and release debt

Owns:
- isolating baseline failures from new-feature failures;
- reproducible diagnostics;
- migration and compatibility fixes;
- closing red gates rather than disabling them.

Current priority:
- GitHub Actions jobs are failing rapidly across multiple repos while log artifacts return unavailable/BlobNotFound. Repo-local isolated gates remain required; Actions infrastructure must be repaired separately.

## 4. Red-Team Reviewer — tenant, denial and irreversible-action paths

Owns:
- cross-tenant access tests;
- malformed/expired identity and approval tests;
- denial receipts;
- arbitrary-shell/path/network escape tests;
- live financial/deployment/device-action boundaries.

Gate:
- high-impact action requires explicit authority, scope, budget and approval evidence.

## 5. MATHESIS — budget, cost and latency discipline

Owns:
- wall time, tokens, monetary budgets, file/change budgets, subprocesses, external calls and child-agent limits;
- quota math;
- provider/runtime cost and latency comparison;
- benchmark methodology.

Gate:
- no unbounded autonomy; budget exhaustion is a terminal or handoff state with a receipt.

## 6. Resource Hub — registry and discoverability

Owns:
- the 22-component federation registry;
- capability manifests;
- operator documentation;
- protocol catalog and examples;
- SDK consumability.

Gate:
- an operator can answer "what owns this capability?" without searching source code.

## 7. Execution Governor — jobs, leases and resilience

Owns:
- job lifecycle;
- leases;
- idempotency;
- bounded retries;
- circuit breakers;
- cancellation and recovery handoffs.

Gate:
- mutating work is idempotent, retry-bounded and isolated from unhealthy dependencies.

## 8. Data Governance — context, memory and retention

Owns:
- `nexus.context-pack.v1`;
- `nexus.memory-event.v1`;
- sensitivity and retention classes;
- secret references;
- export/delete/legal-hold behavior.

Gate:
- no cross-tenant memory recall; no secret values or private reasoning stored in ecosystem wire objects.

## 9. Human Approval Lane — irreversible checkpoints

Owns:
- `nexus.approval.v1`;
- mobile/desktop approval UX;
- expiry and replay resistance;
- actor/scope correlation.

Gate:
- approval is specific to request, action and scope; a generic prior approval cannot authorize unrelated work.

## 10. Model/Intelligence Lane — provider-neutral cognition

Owns:
- AURO/MESIE/Auro14B capability evidence;
- model routing and fallback;
- checkpoint truth state;
- inference telemetry;
- context and research contracts.

Gate:
- model runtimes do not become policy authorities and do not receive implicit external side-effect permissions.

## 11. Voice/Multimodal Lane — conversational control

Owns:
- turn timing, VAD/STT scaffolding, provider readiness, session budgets, context snap, telemetry and handoff;
- measured browser/device/network performance evidence.

Gate:
- conversational control can hand off long work; it does not absorb long-running execution or identity authority.

## 12. SDK/Connector Lane — external developer value

Owns:
- PhantomSDK;
- connector manifests and discovery;
- schema clients;
- receipt verification;
- examples and stable public APIs.

Gate:
- external AIs/connectors are workers, not trunk/policy authorities; credential values remain operator managed.

## 13. Device Lane — PhoneAI and paired execution

Owns:
- cryptographic device pairing;
- device capability allowlists;
- approval notifications;
- revoke/cancel behavior;
- local runner receipts.

Gate:
- PhoneAI's current simulated substrate must not be described as real laptop execution until a governed local runner is implemented and evidenced.

## 14. Finance/Clearing Lane — PARRALAX

Owns:
- verifiable market research and simulation;
- risk decisions;
- machine-checkable netting;
- execution/clearing receipts;
- broker/counterparty evidence boundaries.

Gate:
- generic ecosystem execution is paper/simulation by default. Live orders, settlement or funds movement require external account/broker/counterparty evidence and explicit operator authority.

## 15. Security/CHIMERIA Lane — public-safe defense boundary

Owns:
- defensive control mapping, incident tabletop, policy checks;
- approved CHIMERIA public-safe capability bridge;
- simulation/evidence boundaries.

Gate:
- no offensive cyber execution, autonomous weapon action, private trunk export or current consciousness claim.

## Single integration gate

A feature is not ecosystem-integrated because its repo has a manifest. The minimum end-to-end Alpha path is:

```text
User/Phone/Voice
  -> POCKET identity + tenant + policy
  -> NEXUS route + bounded plan
  -> POCKET Agent / MatDaemon / CAPSULA / connector worker
  -> artifact + execution receipt
  -> outcome evaluation
  -> Medina Memory event when durable
  -> explicit handoff back to POCKET
```

The same request, tenant, session/project correlation must survive every hop. Failure paths must produce a denial, retry/circuit decision, incident or bounded handoff rather than disappear into logs.
