# nexus

NEXUS is the registry and coordination authority for the NOVA repo family.

## Role

NEXUS owns the **MDFUC** layer: Medina Development Federation Unified Catalog.

It tracks which repository owns which part of the organism:

- `nexus` — registry and cross-system coordination authority.
- `nova-intelligence` — core intelligence runtime exports and proof-bearing engine contracts.
- `PhantomSDK` — SDK packaging surface for external builders and local AIs.
- `x-mcp-skills` — MCP and external AI connector skills.
- `x-organism-bots-mcp` — held for later organism bot MCP workers.

## Current Files

- `mdfuc.catalog.json` — machine-readable family catalog.
- `registry/repo-family.json` — active, held, and ignored repo registry.
- `docs/MDFUC.md` — operator explanation of the coordination layer.

## Operating Law

No repo is isolated. Every repo has a role, proof gate, handoff contract, and next gate. Nexus prevents repo-family fragmentation.
