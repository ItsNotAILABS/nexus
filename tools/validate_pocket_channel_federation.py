#!/usr/bin/env python3
"""Deterministic source-level gate for POCKET channel federation v2.

This validates the NEXUS extension contract only. It does not claim that every
runtime transport is deployed or that external integration has been certified.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "protocols" / "pocket-channel-federation.v2.json"


def main() -> int:
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    checks = 0

    def expect(value: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not value:
            raise AssertionError(f"check {checks} failed: {label}")

    expect(doc["schema"] == "nexus.protocol-extension.v1", "extension schema")
    expect(doc["extension_id"] == "pocket.channel-federation.v2", "extension id")
    expect(doc["authority"] == "ItsNotAILABS/nexus", "NEXUS authority")
    expect(len(doc["protocols"]) == 4, "four contracts")
    expect(len(doc["logical_channels"]) == 12, "twelve logical channels")
    expect(len(doc["compatible_transports"]) >= 6, "transport classes")
    expect("claim_boundary" in doc, "claim boundary")

    expected_channels = [
        "user", "heartbeat", "design", "security", "ship", "intel", "model",
        "memory", "proof", "voice", "deploy", "recovery",
    ]
    for index, name in enumerate(expected_channels):
        actual = doc["logical_channels"].get(str(index))
        expect(actual == name, f"channel {index} name")
        expect(isinstance(actual, str), f"channel {index} string")
        expect(bool(actual), f"channel {index} nonempty")
        expect(index >= 0, f"channel {index} nonnegative")
        expect(index <= 11, f"channel {index} bounded")
        expect(expected_channels.count(name) == 1, f"channel {index} unique")
        expect(str(index) in doc["logical_channels"], f"channel {index} addressable")

    required_ids = {
        "pocket.doctrine-laws.v2",
        "pocket.channel-envelope.v2",
        "auro.pocket-channel-contract.v2",
        "auro.execution-receipt.v2",
    }
    seen = set()
    for protocol in doc["protocols"]:
        pid = protocol["id"]
        seen.add(pid)
        expect(pid in required_ids, f"known protocol {pid}")
        expect(bool(protocol["purpose"]), f"purpose {pid}")
        expect(isinstance(protocol["required"], list), f"required list {pid}")
        expect(len(protocol["required"]) >= 5, f"required fields {pid}")
        expect(len(protocol["required"]) == len(set(protocol["required"])), f"required unique {pid}")
        expect("schema" in protocol["required"], f"schema required {pid}")
        expect(all(isinstance(x, str) and x for x in protocol["required"]), f"required strings {pid}")
    expect(seen == required_ids, "exact protocol set")

    for transport in ("in-process", "mesh-disk", "http", "mcp", "websocket", "device-bridge"):
        expect(transport in doc["compatible_transports"], f"transport {transport}")

    rules = " ".join(doc["federation_rules"]).lower()
    for term in ("request identity", "physical rf", "side-effect", "replay", "evidence", "failover", "privacy"):
        expect(term in rules, f"rule term {term}")

    components = doc["components"]
    for component in ("POCKET", "POCKET Agent", "Pocket Voice", "AURO/MESIE", "NEXUS"):
        expect(component in components, f"component {component}")
        expect(bool(components[component]), f"component channels {component}")
        expect(len(components[component]) == len(set(components[component])), f"component channel uniqueness {component}")
        expect(all(ch in expected_channels for ch in components[component]), f"component channels valid {component}")

    expect(checks >= 140, "at least 140 assertions")
    print(json.dumps({"ok": True, "assertions": checks, "contract": doc["extension_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
