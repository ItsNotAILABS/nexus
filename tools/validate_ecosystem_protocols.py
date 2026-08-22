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
    "nexus.identity-ref.v1",
    "nexus.task.v1",
    "nexus.plan.v1",
    "nexus.job.v1",
    "nexus.policy-decision.v1",
    "nexus.approval.v1",
    "nexus.denial.v1",
    "nexus.budget.v1",
    "nexus.quota.v1",
    "nexus.idempotency.v1",
    "nexus.lease.v1",
    "nexus.retry-policy.v1",
    "nexus.circuit-breaker.v1",
    "nexus.event.v1",
    "nexus.feature-flag.v1",
    "nexus.incident.v1",
    "nexus.secret-ref.v1",
    "nexus.retention-policy.v1",
    "nexus.context-pack.v1",
    "nexus.memory-event.v1",
    "nexus.artifact.v1",
    "nexus.execution-receipt.v1",
    "nexus.audit-event.v1",
    "nexus.health.v1",
    "nexus.telemetry.v1",
    "nexus.compatibility.v1",
    "nexus.handoff.v1",
    "nexus.release-evidence.v1",
}
REQUIRED_PRINCIPLES = {
    "tenant-aware",
    "receipt-backed",
    "bounded-execution",
    "capability-discovered",
    "secret-values-never-on-wire",
    "human-approval-for-irreversible-actions",
    "idempotent-mutations",
    "failure-isolated-by-default",
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
    if not str(data.get("version") or "").endswith("alpha.1"):
        fail("registry must expose an explicit alpha version")

    protocols = data.get("protocols")
    if not isinstance(protocols, list) or not protocols:
        fail("protocols must be a non-empty list")
    ids = [p.get("id") for p in protocols]
    if len(ids) != len(set(ids)):
        fail("duplicate protocol id")
    missing = sorted(REQUIRED_IDS - set(ids))
    if missing:
        fail("missing required ids: " + ", ".join(missing))
    unknown = sorted(set(ids) - REQUIRED_IDS)
    if unknown:
        fail("unreviewed protocol ids: " + ", ".join(unknown))

    for p in protocols:
        pid = p.get("id")
        if not isinstance(pid, str) or not pid.startswith("nexus.") or not pid.endswith(".v1"):
            fail(f"invalid protocol id {pid!r}")
        if not isinstance(p.get("purpose"), str) or len(p["purpose"]) < 12:
            fail(f"weak purpose for {pid}")
        required = p.get("required")
        if not isinstance(required, list) or "schema" not in required:
            fail(f"invalid required fields for {pid}")
        if len(required) != len(set(required)):
            fail(f"duplicate required fields for {pid}")

    principles = set(data.get("principles") or [])
    missing_principles = sorted(REQUIRED_PRINCIPLES - principles)
    if missing_principles:
        fail("missing operating principles: " + ", ".join(missing_principles))

    print(f"ecosystem-protocol-validation: PASS ({len(protocols)} protocols, {len(principles)} principles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
