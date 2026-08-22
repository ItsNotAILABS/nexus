#!/usr/bin/env python3
"""Dependency-free validator for the NEXUS ecosystem protocol registry."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "protocols" / "ecosystem.protocols.json"
REQUIRED_IDS = {
    "nexus.capability.v1",
    "nexus.task.v1",
    "nexus.policy-decision.v1",
    "nexus.budget.v1",
    "nexus.context-pack.v1",
    "nexus.memory-event.v1",
    "nexus.artifact.v1",
    "nexus.execution-receipt.v1",
    "nexus.health.v1",
    "nexus.telemetry.v1",
    "nexus.compatibility.v1",
    "nexus.handoff.v1",
    "nexus.denial.v1",
    "nexus.release-evidence.v1",
}


def fail(message: str) -> None:
    raise SystemExit(f"ecosystem-protocol-validation: FAIL: {message}")


def main() -> int:
    if not REGISTRY.is_file():
        fail(f"missing {REGISTRY.relative_to(ROOT)}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "nexus.ecosystem-protocol-registry.v1":
        fail("wrong registry schema")
    if data.get("authority") != "ItsNotAILABS/nexus":
        fail("nexus must remain registry authority")
    protocols = data.get("protocols")
    if not isinstance(protocols, list) or not protocols:
        fail("protocols must be a non-empty list")
    ids = [p.get("id") for p in protocols]
    if len(ids) != len(set(ids)):
        fail("duplicate protocol id")
    missing = sorted(REQUIRED_IDS - set(ids))
    if missing:
        fail("missing required ids: " + ", ".join(missing))
    for p in protocols:
        if not isinstance(p.get("purpose"), str) or len(p["purpose"]) < 12:
            fail(f"weak purpose for {p.get('id')}")
        required = p.get("required")
        if not isinstance(required, list) or "schema" not in required:
            fail(f"invalid required fields for {p.get('id')}")
    principles = set(data.get("principles") or [])
    for principle in {"tenant-aware", "receipt-backed", "bounded-execution", "capability-discovered"}:
        if principle not in principles:
            fail(f"missing operating principle {principle}")
    print(f"ecosystem-protocol-validation: PASS ({len(protocols)} protocols)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
