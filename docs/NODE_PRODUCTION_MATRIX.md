# NEXUS Production Node Matrix

The ecosystem is operated as one federated runtime. The machine-readable source of record is [`registry/production-nodes.json`](../registry/production-nodes.json); CI validates it with [`tools/validate_production_nodes.py`](../tools/validate_production_nodes.py).

Every registered node must declare a runtime, verification path, health/readiness mechanism, protocol manifest, operator documentation, receipt/evidence mechanism, deployment mode, and bounded failure behavior.

| Node | Plane | Production posture | Primary runtime |
|---|---|---|---|
| NEXUS | federation | control plane | `python tools/ecosystemctl.py` |
| POCKET | user/team/policy | MVP | POCKET host + Electron/Edge/Cloud |
| POCKET Agent | execution | MVP | `pocket-agent` daemon/CLI |
| Pocket Voice | voice/conversation | MVP | Node voice API + Studio |
| NOVA Intelligence | intelligence contracts | protocol | runtime/review contracts |
| PhantomSDK | SDK | protocol | schema/client package |
| x-mcp-skills | connector contracts | protocol | MCP/skill connector layer |
| Organism Bots | workflow | protocol | MCP workflow server |
| MatDaemon | compute | MVP | SDK/CLI/API/MCP/Docker |
| CAPSULA | execution capsule | MVP | API/runtime/preview/WASM lane |
| Medina Memory Systems | memory | protocol | durable memory/context packages |
| AURO/MESIE | model | protocol | local model runtime |
| Auro14B | model | MVP | native runtime + checkpoint custody + browser brain |
| NOVA Connector Control Plane | connector runtime | protocol | connector runtime / `connectorctl` |
| NOVA App Containers | deployment | MVP | app/container lane + durable Nova Chat |
| PhoneAI | device control | MVP | paired substrate + Expo + secure repo bridge |
| ResearchersHub | research | protocol | research/compute/artifact lane |
| CyberSecurity-AI | security | protocol | defensive analysis/control lane |
| CHIMERIA | synthetic cognition | protocol | state/simulation/policy lane |
| PARRALAX | market execution | MVP | Wallet AOS v0.2 + risk/simulation plane |
| PARALLAX Clearinghouse | clearing | protocol | validation/netting/margin/ledger lane |
| Sovereign Forge OS | builder | protocol | bounded build/package/release lane |

## Production invariants

1. **Identity and tenant scope survive handoffs.** POCKET owns the user/team boundary; worker nodes consume scoped references rather than inventing identity.
2. **Mutations are idempotent and bounded.** Budgets, quotas, leases, retries, circuit breakers, and explicit approvals are common runtime concepts.
3. **Every material result can become evidence.** Artifacts carry hashes and lineage; executions produce receipts; durable memory stores typed outcome events rather than raw internal state.
4. **Failure is a first-class protocol result.** A node can deny, degrade, hand off, retry within policy, open a circuit, or stop. It must not silently widen its authority.
5. **Model, memory, execution, deployment, finance, and security remain separate planes.** Federation does not mean one process receives every privilege.
6. **Release promotion is machine-checkable.** Protocol compatibility, node completeness, end-to-end correlation, runtime object validation, and the production gate run together in NEXUS CI.

## Release commands

```bash
python tools/validate_ecosystem_protocols.py
python tools/validate_ecosystem_registry.py
python tools/validate_production_nodes.py
python tools/validate_ecosystem_flow.py
python tools/production_gate.py
```

Operator discovery:

```bash
python tools/ecosystemctl.py list
python tools/ecosystemctl.py describe pocket-agent
python tools/ecosystemctl.py gaps
python tools/ecosystemctl.py route "run a bounded matrix benchmark"
```

## Promotion model

`production-protocol` means the node has a complete governed federation contract and operator boundary. `production-mvp` adds a concrete runnable product/runtime lane. `production-control-plane` is reserved for the federation authority.

The ecosystem registry separately tracks `active` versus `protocol-ready`: `active` requires a reproducible end-to-end task plus execution evidence and a passing CI or equivalent signed validation receipt.
