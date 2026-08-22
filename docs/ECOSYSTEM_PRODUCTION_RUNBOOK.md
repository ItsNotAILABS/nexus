# NEXUS Ecosystem Production Runbook

This runbook is the shared operating sequence for the POCKET/NEXUS ecosystem.

## 1. Validate NEXUS first

```bash
python tools/validate_ecosystem_protocols.py
python tools/validate_ecosystem_registry.py
python tools/validate_ecosystem_flow.py
cd tools && python test_ecosystemctl.py
cd .. && python tools/production_gate.py
```

NEXUS is the protocol and federation authority. A runtime should not invent a conflicting task, policy, receipt, health, artifact or handoff shape locally.

## 2. Start the product control plane

POCKET Host owns identity, tenant, policy, routing, approvals and product surfaces.

Operator checks:

```text
GET /health
GET /v1/ready
GET /v1/catalog
```

Confirm that the intended tenant, principal, project, session and device scopes are visible before enabling externally reachable mutations.

## 3. Start execution planes only when needed

### POCKET Agent

```bash
python -m pip install -e ".[dev]"
pytest -q
pocket-agent doctor --fix
```

Use for long-running goals, repository work, schedules, recursive workers and capsule dispatch.

### MatDaemon

```bash
python -m pip install -e ".[dev]"
pytest -q
```

Use for bounded matrix/compute work and compute receipts.

### CAPSULA

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests
```

Use for isolated runtime sessions, previews, bounded builds, WASM planning and deploy plans.

## 4. Start conversational and device planes

### Pocket Voice

```bash
npm install
npm test
npm start
```

Use for patient turn-taking, STT control, Studio context, provider selection, voice telemetry and handoff.

### PhoneAI

```bash
cd backend
python -m pip install -r requirements.txt
export MONGO_URL='mongodb://127.0.0.1:27017'
export DB_NAME='phoneai'
export PHONEAI_WORKSPACE_ROOT='/path/to/workspace'
export PHONEAI_RECEIPT_KEY='replace-with-long-random-secret'
uvicorn production_server:app --host 0.0.0.0 --port 8000
```

Mobile:

```bash
cd frontend
yarn install
export EXPO_PUBLIC_BACKEND_URL='http://WORKSTATION-IP:8000'
yarn start
```

## 5. Use the standard request lifecycle

```text
identity
  -> capability discovery
  -> route
  -> policy
  -> approval when required
  -> quota / idempotency / lease
  -> budget
  -> execute
  -> health / telemetry
  -> artifact
  -> receipt
  -> outcome evaluation
  -> memory event when durable
  -> handoff
```

Every cross-repo request should preserve the same `request_id` and tenant/project/session correlation.

## 6. External worker integrations

Connector runtimes and MCP workers consume NEXUS tasks and policy objects. External systems remain worker surfaces; NEXUS/POCKET retain policy and routing authority.

Primary repos:

```text
x-mcp-skills
nova-connector-control-plane
organism-bots-mcp-server
PhantomSDK
```

Use receipt-backed artifact imports rather than copying unverified worker output directly into a release.

## 7. Models and memory

Model runtimes:

```text
AURO
Auro14B
MESIE lanes
```

Durable continuity:

```text
MedinaMemorySystems
```

Store durable outcomes, decisions, corrections, benchmark evidence, incidents and compatibility findings. Pass bounded context packs into model/execution calls instead of cloning the entire memory state.

## 8. Finance and clearing

PARRALAX and PARALLAX Exchange Clearinghouse use the same policy, approval, idempotency, audit, artifact and receipt primitives as the rest of the ecosystem.

Typical flow:

```text
market input
 -> risk evaluation
 -> execution plan
 -> approval where required
 -> execution/simulation adapter
 -> order/execution receipt
 -> netting/clearing handoff
 -> ledger/audit artifact
```

## 9. Build and deployment

Use Sovereign Forge, CAPSULA and NOVA app containers for build/package/deploy preparation.

```text
source
 -> plan
 -> bounded build
 -> artifact hash
 -> preview
 -> approval
 -> deploy handoff
 -> deployment receipt
```

Keep build evidence separate from runtime health evidence so a successful package does not masquerade as a healthy deployed service.

## 10. Production acceptance packet

A release packet should contain:

```text
component/version
commit SHA
protocol versions consumed/produced
configuration fingerprint
validation results
artifact hashes
health/readiness result
integration fixture result
rollback command or strategy
data recovery strategy
known feature flags
open incidents
release receipt
```

## 11. Failure handling

Standard failure sequence:

```text
classify
 -> retry only if policy permits
 -> bounded backoff
 -> circuit-open failing dependency
 -> alternate route when available
 -> preserve partial artifact/receipt
 -> create incident for repeated/systemic failure
 -> handoff or stop
```

Never let one degraded model/provider/connector cause an unbounded retry storm across the federation.

## 12. Promotion checklist

```text
[ ] protocol validator passes
[ ] repository tests pass
[ ] package/build check passes
[ ] health and readiness endpoints behave correctly
[ ] tenant/request correlation survives one E2E task
[ ] denial path is exercised
[ ] approval path is exercised for privileged actions
[ ] idempotency duplicate is exercised
[ ] dependency failure opens/follows circuit policy
[ ] artifact and receipt hashes are produced
[ ] operator documentation matches actual commands
[ ] rollback/recovery path is documented
```

The production goal is not to make every repository identical. It is to make every specialized runtime interoperable, inspectable, recoverable and operable through the same ecosystem contract.