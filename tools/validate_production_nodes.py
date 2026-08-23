#!/usr/bin/env python3
"""Validate that every NEXUS ecosystem component has an operational production contract."""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "ecosystem-alpha.json"
NODES = ROOT / "registry" / "production-nodes.json"

checks = 0
failures: list[str] = []


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def load(path: Path) -> dict[str, Any]:
    check(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        failures.append(f"invalid json {path.name}: {exc}")
        return {}
    check(isinstance(value, dict), f"{path.name} must be object")
    return value


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> int:
    registry = load(REGISTRY)
    catalog = load(NODES)

    check(catalog.get("schema") == "nexus.production-nodes.v1", "production node schema")
    check(catalog.get("authority") == "ItsNotAILABS/nexus", "production node authority")
    check(text(catalog.get("version")), "production node version")

    registered = registry.get("components") or []
    nodes = catalog.get("nodes") or []
    check(isinstance(registered, list), "registry components list")
    check(isinstance(nodes, list), "production nodes list")
    check(len(registered) >= 22, "registry has at least 22 nodes")
    check(len(nodes) == len(registered), "every registered node has production row")

    registered_ids = {row.get("component") for row in registered if isinstance(row, dict)}
    node_ids = {row.get("component") for row in nodes if isinstance(row, dict)}
    check(registered_ids == node_ids, "production catalog matches registered component ids")

    required = (
        "component",
        "repo",
        "plane",
        "maturity",
        "runtime",
        "verify",
        "health",
        "protocol_manifest",
        "operator_doc",
        "receipt",
        "deployment",
        "failure_mode",
    )
    maturity_values = {"production-control-plane", "production-mvp", "production-protocol"}
    repo_seen: set[str] = set()

    by_registered = {
        row.get("component"): row for row in registered if isinstance(row, dict) and text(row.get("component"))
    }

    for index, node in enumerate(nodes):
        prefix = f"node[{index}]"
        check(isinstance(node, dict), f"{prefix} object")
        if not isinstance(node, dict):
            continue
        for field in required:
            check(text(node.get(field)), f"{prefix}.{field}")
        component = node.get("component")
        repo = node.get("repo")
        check(node.get("maturity") in maturity_values, f"{prefix}.maturity allowed")
        check(str(repo).startswith("ItsNotAILABS/"), f"{prefix}.repo organization")
        check(repo not in repo_seen, f"{prefix}.repo unique")
        if isinstance(repo, str):
            repo_seen.add(repo)
        registered_row = by_registered.get(component, {})
        check(registered_row.get("repo") == repo, f"{prefix}.repo matches registry")
        check(registered_row.get("plane") == node.get("plane"), f"{prefix}.plane matches registry")

        # Operational quality: entries must describe mechanisms, not placeholders.
        for field in ("runtime", "verify", "health", "receipt", "deployment", "failure_mode"):
            value = str(node.get(field) or "")
            check(len(value) >= 12, f"{prefix}.{field} descriptive")
            check("todo" not in value.lower(), f"{prefix}.{field} no TODO")
            check("tbd" not in value.lower(), f"{prefix}.{field} no TBD")

        check(str(node.get("protocol_manifest")).endswith((".json", ".md")), f"{prefix}.protocol_manifest file-like")
        check(str(node.get("operator_doc")).endswith(".md"), f"{prefix}.operator_doc markdown")

    # Critical planes must be represented independently.
    planes = {node.get("plane") for node in nodes if isinstance(node, dict)}
    for plane in (
        "federation",
        "user-team-policy",
        "execution",
        "voice-conversation",
        "compute",
        "execution-capsule",
        "memory",
        "model",
        "device-control",
        "deployment",
        "security",
        "market-execution",
        "clearing",
        "builder",
    ):
        check(plane in planes, f"required operational plane: {plane}")

    # High-impact nodes must explicitly describe bounded failure behavior.
    for component in ("phone-ai", "parralax", "parallax-clearinghouse", "sovereign-forge-os", "chimeria"):
        node = next((row for row in nodes if isinstance(row, dict) and row.get("component") == component), {})
        failure = str(node.get("failure_mode") or "").lower()
        check(bool(failure), f"{component} failure mode")
        check(any(word in failure for word in ("deny", "reject", "stop", "revoke", "bounded", "unpromoted")), f"{component} bounded failure semantics")

    if checks < 300:
        failures.append(f"node validator must execute >=300 assertions; got {checks}")

    if failures:
        print(f"production node validation: FAIL ({checks} assertions, {len(failures)} failures)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"production node validation: PASS ({checks} assertions, {len(nodes)} nodes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
