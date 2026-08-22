#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "examples" / "ecosystem-alpha-flow.json"
REGISTRY = ROOT / "registry" / "ecosystem-alpha.json"


def fail(message: str) -> None:
    raise SystemExit(f"ecosystem-flow-validation: FAIL: {message}")


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key).lower()
            yield from walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_keys(item)


def stable_digest(value: dict[str, Any]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def main() -> int:
    flow = json.loads(FLOW.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if flow.get("schema") != "nexus.integration-flow.v1": fail("flow schema")
    request_id = flow.get("request_id")
    if not request_id: fail("request_id")
    tenant_id = (flow.get("scope") or {}).get("tenant_id")
    if not tenant_id: fail("tenant scope")

    for name in ("policy", "context", "task", "artifact", "receipt", "memory", "handoff"):
        obj = flow.get(name)
        if not isinstance(obj, dict): fail(f"missing {name}")
        if name != "artifact" and name != "memory" and obj.get("request_id") != request_id:
            fail(f"request correlation: {name}")

    if (flow["task"].get("scope") or {}).get("tenant_id") != tenant_id: fail("task tenant")
    if (flow["task"].get("principal") or {}).get("tenant_id") != tenant_id: fail("principal tenant")
    if (flow["context"].get("provenance") or {}).get("tenant_id") != tenant_id: fail("context tenant")
    if (flow["memory"].get("subject") or {}).get("tenant_id") != tenant_id: fail("memory tenant")
    if flow["policy"].get("decision") != "allow": fail("fixture policy must allow")

    limits = ((flow["task"].get("budget") or {}).get("limits") or {})
    if int(limits.get("wall_seconds", 0)) <= 0: fail("wall budget")
    if int(limits.get("artifact_bytes", 0)) <= 0: fail("artifact budget")

    artifact_id = flow["artifact"].get("artifact_id")
    if not artifact_id: fail("artifact id")
    if artifact_id not in (flow["receipt"].get("artifact_ids") or []): fail("receipt artifact link")
    if artifact_id not in ((flow["memory"].get("provenance") or {}).get("artifact_ids") or []): fail("memory artifact link")
    if artifact_id not in (flow["handoff"].get("artifacts") or []): fail("handoff artifact link")

    receipt = dict(flow["receipt"])
    digest = receipt.pop("digest", None)
    if digest != stable_digest(receipt): fail("receipt digest")
    if receipt.get("status") != "succeeded": fail("receipt status")

    registered = {entry.get("component") for entry in registry.get("components", []) if isinstance(entry, dict)}
    for component in (flow["capability_route"].get("component"), flow["receipt"].get("component"), flow["handoff"].get("from"), flow["handoff"].get("to")):
        if component not in registered: fail(f"unregistered component {component}")

    forbidden = {"reasoning", "chain_of_thought", "chain-of-thought", "cot", "hidden_reasoning"}
    leaked = forbidden.intersection(set(walk_keys(flow)))
    if leaked: fail("private reasoning keys present: " + ", ".join(sorted(leaked)))

    expected_schemas = {
        "policy": "nexus.policy-decision.v1",
        "context": "nexus.context-pack.v1",
        "task": "nexus.task.v1",
        "artifact": "nexus.artifact.v1",
        "receipt": "nexus.execution-receipt.v1",
        "memory": "nexus.memory-event.v1",
        "handoff": "nexus.handoff.v1",
    }
    for name, schema in expected_schemas.items():
        if flow[name].get("schema") != schema: fail(f"schema mismatch: {name}")

    print("ecosystem-flow-validation: PASS (Voice/Host/Agent/Compute/Memory/Handoff correlation intact)")
    return 0

if __name__ == "__main__": sys.exit(main())
