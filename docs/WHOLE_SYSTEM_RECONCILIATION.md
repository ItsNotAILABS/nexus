# Whole-System Reconciliation

## Purpose

The ItsNotAI Labs codebase is a constellation, not a monolith. Multiple repositories contain valid work created at different points in the architecture's evolution. The failure mode is not lack of capability; it is duplicated ownership, forgotten implementations, conflicting names, and product surfaces re-implementing systems that already exist elsewhere.

NEXUS is therefore the **canonical reconciliation authority** for the whole system.

The reconciliation contract answers five questions for every major capability:

1. Where is the canonical implementation or protocol home?
2. Which repositories are feeders or adapters?
3. Which repositories are historical, experimental, or duplicate candidates?
4. Which product surfaces consume the capability?
5. What evidence is required before authority moves from one home to another?

The machine-readable source is [`registry/system-reconciliation.json`](../registry/system-reconciliation.json).

## Governing law

> **Implement once. Federate through contracts. Compose at product surfaces. Preserve evidence. Never inherit authority implicitly.**

This extends the existing product law:

> **Agents propose. Policy evaluates. Owners approve. Wallets sign. Receipts remember.**

## Canonical system picture

```text
                         NEXUS
          federation · protocols · compatibility
                   · plans · receipts · handoffs
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
  PRODUCT / OPERATOR                  INTERNAL INTELLIGENCE
  MonadBuilder+                       NOVA model family
  THESIS Agent Desktop                ORIGO · SENSUS · CORPUS
  MCP Spine                           MATHESIS · model registry
          |                                 |
          +---------------+-----------------+
                          |
            +-------------+-------------+
            |             |             |
            v             v             v
          MEMORY        EXECUTION      MODELS
   MedinaMemorySystems   CAPSULA      AURO / MESIE
                        MatDaemon      Auro14B
            |             |             |
            +-------------+-------------+
                          |
                CONNECTORS / WORKFLOWS
       nova-connector-control-plane · x-mcp-skills
               organism-bots-mcp-server
                          |
             +------------+------------+
             |                         |
             v                         v
        MARKET / CLEARING         RESEARCH / PROOF
        PARRALAX                  ResearchersHub
        PARALLAX Clearing         PRODUCTION-
                                  CyberSecurity-AI
```

POCKET Host, POCKET Agent, Pocket Voice, PhoneAI, Chimeria, NATIVE NOVA, sovereign-forge-os and other specialized systems remain distinct feeder or authority planes and connect through NEXUS contracts rather than by copying implementations.

## Reconciliation decisions

### NEXUS

`ItsNotAILABS/nexus` is the sole machine-readable federation and cross-repository protocol authority. Existing NEXUS references in other repositories are consumers, adapters, or historical copies. They do not create a second registry.

### MonadBuilder+ and THESIS

`ItsNotAILABS/CapsulaBuilder` is a product and operator surface, not the canonical home for every subsystem it exposes. It should consume:

- memory from MedinaMemorySystems;
- model/runtime capabilities from NOVA, AURO and Auro14B;
- isolated execution from CAPSULA;
- bounded compute from MatDaemon;
- connectors through the connector control plane and x-mcp-skills;
- market and clearing capabilities from the PARRALAX systems;
- research evidence from ResearchersHub / PRODUCTION-;
- federation contracts from NEXUS.

The product repository owns browser UX, local THESIS control, approval UX, MCP integration, receipt presentation, and product-specific orchestration.

### NOVA / ORIGO / SENSUS / CORPUS

The internal NOVA model-family work already contains concrete ORIGO and SENSUS assets and a release registry. Search evidence also shows older or alternate implementations in `cloudcolony`, Auro14B, and product documentation. Those are not automatically independent authorities.

Canonical rule:

- NOVA owns model-family semantics and internal intelligence contracts.
- Runtime-specific adapters may exist elsewhere.
- A secondary implementation is promoted only when it has a unique responsibility and a declared NEXUS compatibility contract.

### Memory

`MedinaMemorySystems` is the runtime authority for durable memory, bounded context packs, retention, provenance, temporal memory, knowledge graphs, and team vault semantics.

`LOOM-Memoria-De-Intelligencia-` contains important historical doctrine and prior implementations. It remains preserved as historical evidence. Unique runtime mechanisms should be extracted into MedinaMemorySystems before LOOM is treated as an active runtime dependency.

### Research

`PRODUCTION-` is the public research/provenance authority. `ResearchersHub` is the research workbench and evidence-pack lane. Papers should cite and hash runtime evidence rather than duplicate production implementations.

### Market systems

PARRALAX AIHFT owns market research, wallet-ledger, risk, reconciliation and governed execution planning. PARALLAX Exchange Clearinghouse owns netting, clearing and settlement-planning evidence. Product surfaces may invoke these capabilities but may not inherit unrestricted signing or settlement authority.

## Duplicate-resolution protocol

When two repositories appear to own the same capability, do not choose by age, naming, or size alone.

1. Identify the actual source paths and runnable interfaces.
2. Compare contracts, tests, deployment evidence, receipts and current consumers.
3. Identify unique behavior in each implementation.
4. Choose one canonical authority based on responsibility boundaries, not branding.
5. Import unique behavior into the canonical home or expose it through an adapter.
6. Add compatibility tests.
7. Mark the former implementation as `historical`, `feeder`, or `incubation`.
8. Preserve commit and release history.
9. Never delete evidence merely to make the graph look clean.

## Authority promotion

Authority does not move because a README says a system is newer.

A candidate authority must provide:

- a machine-readable capability surface;
- an explicit responsibility boundary;
- compatibility with NEXUS contracts;
- validation commands;
- failure and denial behavior;
- operator documentation;
- release evidence or receipts;
- a migration or adapter plan for existing consumers.

Only after those gates pass should `registry/system-reconciliation.json` change the canonical home.

## Public/private boundary finding

At the time of this reconciliation pass, GitHub reports `ItsNotAILABS/NOVA-private-root` as **public**, while its README explicitly states that it is intended for family-authorized/internal AI builders and is not intended for public onboarding.

That mismatch is not a documentation detail. It is an **exposure-review item**. The operator must decide whether:

- the repository should be private;
- the internal-only statement is obsolete and the public surface has been intentionally sanitized; or
- a separate public release/showcase repository should contain only the intended public subset.

NEXUS records the mismatch but does not silently change repository visibility.

## Stale repository policy

Repositories matching `mesie-career-*.stale.*` are currently empty public repositories and should not appear as active architecture nodes. Before archival or visibility changes, confirm they contain no unique commits, releases, issues, or references. Then archive/hide them rather than deleting provenance.

## Operator commands

```bash
python tools/validate_system_reconciliation.py
python tools/reconcile_ecosystem.py summary
python tools/reconcile_ecosystem.py priorities
python tools/reconcile_ecosystem.py internals
python tools/reconcile_ecosystem.py repos --class duplicate_candidate
python tools/reconcile_ecosystem.py describe ORIGO
python tools/reconcile_ecosystem.py describe CapsulaBuilder
```

## Definition of done

The system is reconciled when:

- every active capability has one canonical authority;
- every product surface references that authority through a contract or adapter;
- duplicate candidates have explicit import/bridge/retire decisions;
- historical work remains discoverable but is not mistaken for current production authority;
- public/private boundaries match actual repository visibility;
- CI rejects conflicting canonical authority claims;
- releases include a reconciliation receipt alongside normal protocol and production evidence.

Reconciliation is continuous. A new repository may be created, but it cannot become architectural authority merely by existing.
