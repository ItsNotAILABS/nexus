# Corpus Architecture Alignment v2.1

`Corpus de Architectura Intelligentiae Sui Iuris` is the conceptual research program for the ecosystem. This document binds the research language to versioned implementation contracts without converting conceptual proposals into deployment or benchmark claims.

## Authority

- Protocol and registry authority: `ItsNotAILABS/nexus`
- Canonical machine-readable corpus: `research/corpus-architectura-v2.1.json`
- Content SHA-256: `c75ee90a358507652bfcec468649277c348b8bd4d8d28b99a5c5e0fd46905a12`
- Papers: 13 across Volumes I and II

## Core implementation roots

| Repository | Load-bearing responsibility |
|---|---|
| `ItsNotAILABS/nexus` | protocol registry, evidence classes, compatibility, device federation, runtime-cell and handoff contracts |
| `ItsNotAILABS/pocket` | cloud account, Electron desktop, Edge body, users, organizations, devices, product routing and capability marketplace |
| `ItsNotAILABS/Auro14B` | model-family taxonomy, atomic lanes, 500M triad, model councils, checkpoint custody, continuity and model evidence |
| `ItsNotAILABS/AURO` | MESIE-backed spectral compute, embedding, bounded inference, offload and model-runtime evidence |
| `ItsNotAILABS/nova-intelligence` | research index, compatibility review, evidence classification, continuity and emergence review |
| `ItsNotAILABS/pocket-agent` | durable long-running execution, runtime cells, leases, retries and execution receipts |
| `ItsNotAILABS/pocket-voice-to-text` | consent-aware voice state, turn timing, STT/VAD, prosody and voice-session evidence |

## Paper-to-contract map

| No. | Paper | Primary implementation contracts |
|---:|---|---|
| 1 | *Tres Formae, Una Mens* | `pocket.triform-product.v1`, `nexus.identity-ref.v1`, `nexus.device-federation.v1` |
| 2 | *Nubes Perennis, Corpus Intermittens* | `nexus.job.v1`, `nexus.lease.v1`, `nexus.device-federation.v1` |
| 3 | *Computatio Sui Iuris* | `nexus.sovereignty-profile.v1`, `nexus.artifact.v1`, `nexus.release-evidence.v1` |
| 4 | *Identitas, Potestas, et Fines* | `nexus.identity-ref.v1`, `nexus.approval.v1`, `nexus.policy-decision.v1` |
| 5 | *Foedus Machinarum* | `nexus.device-federation.v1`, `nexus.capability.v1`, `nexus.task.v1` |
| 6 | *Agentes Sub Lege* | `nexus.runtime-cell.v1`, `nexus.approval.v1`, `nexus.execution-receipt.v1` |
| 7 | *Consensus ex Minimis* | `auro.model-family.v2`, `nexus.model-council.v1`, `nexus.context-pack.v1` |
| 8 | *Memoria Viva et Continuatio* | `nexus.memory-event.v1`, `nexus.continuity-snapshot.v1`, `nexus.retention-policy.v1` |
| 9 | *Probatio Ante Assertionem* | `nexus.evidence-classification.v1`, `nexus.execution-receipt.v1`, `nexus.release-evidence.v1` |
| 10 | *Mercatus Facultatum Agentium* | `nexus.capability-offer.v1`, `nexus.quota.v1`, `nexus.compatibility.v1` |
| 11 | *Vox, Corpus, Mens* | `pocket.voice-state.v1`, `nexus.identity-ref.v1`, `nexus.telemetry.v1` |
| 12 | *Civitas Intelligentiarum* | `nexus.ecosystem-registry.v1`, `nexus.handoff.v1`, `nexus.audit-event.v1` |
| 13 | *Emergentia Gubernata* | `nexus.emergence-observation.v1`, `nexus.policy-decision.v1`, `nexus.continuity-snapshot.v1` |

## Shared invariants

### Product bodies

POCKET has three coordinated bodies:

1. an independent cloud account and organization plane;
2. an installable Electron desktop runtime with local execution;
3. a Microsoft Edge application surface that reuses the local runtime or opens the cloud account.

These bodies may synchronize identity and task references, but their availability and state ownership remain explicit.

### AURO family

The canonical capacity ladder is:

`Auro-156K -> Auro-250M -> Auro-500M -> Auro-2B -> Auro-4B -> Auro-8B -> Auro-14B -> Auro-100B`

Auro-2B may coordinate the three specialist identities `Auro-500M-SENSUS`, `Auro-500M-PRAXIS`, and `Auro-500M-VERBUM`. A named specialist is not a separately trained model until exact checkpoint or adapter evidence exists.

### Governed execution

Consequential execution follows:

`discover -> classify risk -> plan -> approve -> execute -> validate -> receipt`

The runtime-cell classes are:

- agent sandbox;
- app bottle;
- mini OS.

### Evidence classes

- E0: assertion only
- E1: source present
- E2: execution log
- E3: independently validated output
- E4: signed receipt
- E5: external custody and independent reproduction

A claim must not be promoted above its observed evidence class.

## Claim boundaries

The ecosystem must not conflate:

- architecture configuration with a trained checkpoint;
- accepted context with dense attention;
- named agent identity with separately trained weights;
- source code with deployment evidence;
- a local unkeyed hash chain with external custody;
- same-session recall with persistent memory;
- a successful build with clean-install proof;
- generated output with experimental validation.

## Validation

Run:

```bash
python tools/validate_corpus_architecture.py
```

The validator checks manifest integrity, all thirteen paper IDs, volume membership, contract registration, repository authority mappings, AURO family order, the 500M triad, runtime-cell classes, execution sequence, evidence-class order and claim-boundary presence.
