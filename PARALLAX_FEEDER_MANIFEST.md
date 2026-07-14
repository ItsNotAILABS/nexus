# PARALLAX Feeder Manifest

This repository feeds the PARALLAX authority repo:

```text
ItsNotAILABS/PARALLAX-Exchange-Clearinghouse
```

## Lane

```text
federation_mcp_control_plane
```

## What this repo may feed

- MCP federation catalog entries,
- tool routing schemas,
- connector capability summaries,
- NEXUS receipt bridge requirements,
- repo catalog records,
- operator routing requirements.

## What this repo must not feed

- API keys,
- connector credentials,
- tool secrets,
- unapproved external automation claims,
- silent mutation pathways,
- uncontrolled tool execution.

## PARALLAX target surfaces

- Cloudflare Edge Gateway,
- Control Tower,
- Federation Registry,
- Proof Room,
- AI Execution.

## Promotion rule

A federation, connector, MCP, or tool-routing artifact from this repo becomes PARALLAX authority only after:

1. source commit or artifact hash is recorded,
2. tool permission boundary is assigned,
3. mutation and read-only behavior is declared,
4. proof or receipt expectation is mapped,
5. explicit integration PR is opened in `PARALLAX-Exchange-Clearinghouse`.

## Current boundary

This feeder may route tools and repo intelligence into PARALLAX, but it must not expose credentials or enable silent external execution.
