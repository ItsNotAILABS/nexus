#!/usr/bin/env python3
"""NEXUS ecosystem production gate.

Dependency-free deterministic validation for the protocol and federation spine.
The gate intentionally performs far more than 100 explicit assertions so a
release cannot pass on file-existence checks alone.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS = ROOT / "protocols" / "ecosystem.protocols.json"
REGISTRY = ROOT / "registry" / "ecosystem-alpha.json"
FLOW = ROOT / "examples" / "ecosystem-flow.json"

checks = 0
failures: list[str] = []


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def load(path: Path) -> dict[str, Any]:
    check(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        failures.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        return {}
    check(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> int:
    protocols = load(PROTOCOLS)
    registry = load(REGISTRY)
    flow = load(FLOW)

    # Registry identity.
    check(protocols.get("schema") == "nexus.ecosystem-protocol-registry.v1", "protocol registry schema")
    check(protocols.get("authority") == "ItsNotAILABS/nexus", "protocol registry authority")
    check(text(protocols.get("version")), "protocol registry version")
    check(registry.get("schema") == "nexus.ecosystem-registry.v1", "ecosystem registry schema")
    check(registry.get("authority") == "ItsNotAILABS/nexus", "ecosystem registry authority")
    check(text(registry.get("version")), "ecosystem registry version")

    principles = protocols.get("principles") or []
    check(isinstance(principles, list), "principles list")
    for principle in (
        "provider-neutral",
        "tenant-aware",
        "receipt-backed",
        "bounded-execution",
        "capability-discovered",
        "secret-values-never-on-wire",
        "human-approval-for-irreversible-actions",
        "idempotent-mutations",
        "failure-isolated-by-default",
    ):
        check(principle in principles, f"missing principle: {principle}")

    protocol_rows = protocols.get("protocols") or []
    check(isinstance(protocol_rows, list), "protocols list")
    check(len(protocol_rows) >= 29, "at least 29 shared protocols")
    ids: list[str] = []
    for index, row in enumerate(protocol_rows):
        prefix = f"protocol[{index}]"
        check(isinstance(row, dict), f"{prefix} object")
        pid = row.get("id") if isinstance(row, dict) else None
        ids.append(pid if isinstance(pid, str) else "")
        check(text(pid), f"{prefix}.id")
        check(isinstance(pid, str) and pid.startswith("nexus."), f"{prefix}.id namespace")
        check(isinstance(pid, str) and pid.endswith(".v1"), f"{prefix}.id version")
        check(text(row.get("purpose")), f"{prefix}.purpose")
        check(len(str(row.get("purpose") or "")) >= 20, f"{prefix}.purpose descriptive")
        required = row.get("required")
        check(isinstance(required, list), f"{prefix}.required list")
        if isinstance(required, list):
            check("schema" in required, f"{prefix}.required schema")
            check(len(required) == len(set(required)), f"{prefix}.required unique")
            for field_index, field_name in enumerate(required):
                check(text(field_name), f"{prefix}.required[{field_index}] text")
    check(len(ids) == len(set(ids)), "protocol ids unique")

    must_have_protocols = {
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
    for pid in sorted(must_have_protocols):
        check(pid in ids, f"required protocol present: {pid}")

    components = registry.get("components") or []
    check(isinstance(components, list), "components list")
    check(len(components) >= 22, "at least 22 ecosystem components")
    component_ids: list[str] = []
    repos: list[str] = []
    allowed_statuses = {"active", "protocol-ready", "activation-candidate"}
    for index, row in enumerate(components):
        prefix = f"component[{index}]"
        check(isinstance(row, dict), f"{prefix} object")
        component = row.get("component") if isinstance(row, dict) else None
        repo = row.get("repo") if isinstance(row, dict) else None
        plane = row.get("plane") if isinstance(row, dict) else None
        status = row.get("status") if isinstance(row, dict) else None
        authority = row.get("authority") if isinstance(row, dict) else None
        component_ids.append(component if isinstance(component, str) else "")
        repos.append(repo if isinstance(repo, str) else "")
        check(text(component), f"{prefix}.component")
        check(text(repo) and "/" in str(repo), f"{prefix}.repo")
        check(str(repo).startswith("ItsNotAILABS/"), f"{prefix}.repo organization")
        check(text(plane), f"{prefix}.plane")
        check(status in allowed_statuses, f"{prefix}.status")
        check(isinstance(authority, list) and bool(authority), f"{prefix}.authority")
        if isinstance(authority, list):
            check(len(authority) == len(set(authority)), f"{prefix}.authority unique")
            for authority_index, item in enumerate(authority):
                check(text(item), f"{prefix}.authority[{authority_index}]")
    check(len(component_ids) == len(set(component_ids)), "component ids unique")
    check(len(repos) == len(set(repos)), "repository registrations unique")

    required_components = {
        "nexus",
        "pocket",
        "pocket-agent",
        "pocket-voice",
        "matdaemon",
        "capsula",
        "medina-memory-systems",
        "auro-mesie-runtime",
        "phone-ai",
        "parralax",
        "parallax-clearinghouse",
    }
    for component in sorted(required_components):
        check(component in component_ids, f"required component present: {component}")

    by_component = {row.get("component"): row for row in components if isinstance(row, dict)}
    check(by_component.get("nexus", {}).get("plane") == "federation", "NEXUS plane")
    check(by_component.get("pocket", {}).get("plane") == "user-team-policy", "POCKET plane")
    check(by_component.get("pocket-agent", {}).get("plane") == "execution", "Agent plane")
    check(by_component.get("pocket-voice", {}).get("plane") == "voice-conversation", "Voice plane")
    check(by_component.get("matdaemon", {}).get("plane") == "compute", "MatDaemon plane")
    check(by_component.get("capsula", {}).get("plane") == "execution-capsule", "CAPSULA plane")
    check(by_component.get("medina-memory-systems", {}).get("plane") == "memory", "Memory plane")

    forbidden = registry.get("forbidden_authority_merges") or []
    check(isinstance(forbidden, list), "forbidden authority list")
    check(len(forbidden) >= 5, "forbidden authority coverage")
    for index, pair in enumerate(forbidden):
        check(isinstance(pair, list) and len(pair) == 2, f"forbidden[{index}] pair")
        if isinstance(pair, list) and len(pair) == 2:
            check(text(pair[0]), f"forbidden[{index}][0]")
            check(text(pair[1]), f"forbidden[{index}][1]")

    promotion = registry.get("promotion_rules") or {}
    check(isinstance(promotion, dict), "promotion rules object")
    for key in ("activation-candidate_to_protocol-ready", "protocol-ready_to_active"):
        rules = promotion.get(key)
        check(isinstance(rules, list) and len(rules) >= 4, f"promotion rule {key}")
        if isinstance(rules, list):
            for idx, rule in enumerate(rules):
                check(text(rule), f"promotion {key}[{idx}]")

    # End-to-end fixture checks.
    check(text(flow.get("schema")), "flow schema")
    flow_text = json.dumps(flow, sort_keys=True)
    for component in ("pocket", "pocket-voice", "matdaemon"):
        check(component in flow_text, f"flow references {component}")
    for protocol_id in (
        "nexus.context-pack.v1",
        "nexus.policy-decision.v1",
        "nexus.execution-receipt.v1",
        "nexus.memory-event.v1",
        "nexus.handoff.v1",
    ):
        check(protocol_id in flow_text, f"flow references {protocol_id}")
    check("chain_of_thought" not in flow_text, "flow excludes chain_of_thought")
    check("private_reasoning" not in flow_text, "flow excludes private_reasoning")

    # Required operator/runtime files.
    required_files = [
        "tools/ecosystemctl.py",
        "tools/validate_ecosystem_protocols.py",
        "tools/validate_ecosystem_registry.py",
        "tools/validate_ecosystem_flow.py",
        "tools/validate_protocol_object.py",
        "docs/ECOSYSTEM_INTELLIGENCE_PROTOCOLS.md",
        "README.md",
    ]
    for rel in required_files:
        path = ROOT / rel
        check(path.is_file(), f"required file {rel}")
        if path.is_file():
            check(path.stat().st_size > 100, f"non-empty file {rel}")

    # Stable evidence fingerprint for the gate inputs.
    fingerprint_payload = PROTOCOLS.read_bytes() + REGISTRY.read_bytes() + FLOW.read_bytes()
    fingerprint = hashlib.sha256(fingerprint_payload).hexdigest()
    check(len(fingerprint) == 64, "production input fingerprint")

    if checks < 100:
        failures.append(f"production gate must perform >=100 assertions; got {checks}")

    if failures:
        print(f"NEXUS production gate: FAIL ({checks} assertions, {len(failures)} failures)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"NEXUS production gate: PASS ({checks} assertions)")
    print(f"input fingerprint: {fingerprint}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
