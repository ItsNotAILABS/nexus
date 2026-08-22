#!/usr/bin/env python3
"""Runtime utilities for NEXUS ecosystem wire objects.

This is intentionally dependency-free so it can be copied into SDK generators,
CI gates, and minimal edge services. It validates registry-required fields plus
cross-cutting privacy/correlation invariants; specialized repos may add stricter
validation for their own protocol payloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "protocols" / "ecosystem.protocols.json"

FORBIDDEN_REASONING_KEYS = {
    "chain_of_thought", "chain-of-thought", "cot", "hidden_reasoning",
    "private_reasoning", "scratchpad", "reasoning_trace",
}
SECRET_VALUE_KEYS = {
    "password", "passwd", "api_key", "apikey", "access_token", "refresh_token",
    "private_key", "client_secret", "secret_value",
}
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def protocol_map() -> dict[str, dict[str, Any]]:
    return {str(p["id"]): p for p in registry().get("protocols", []) if isinstance(p, dict) and p.get("id")}


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, str(key), child
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk(child, f"{path}[{idx}]")


def stable_digest(value: Mapping[str, Any], *, exclude: Iterable[str] = ("digest", "receipt_hash")) -> str:
    blocked = set(exclude)

    def clean(node: Any) -> Any:
        if isinstance(node, Mapping):
            return {str(k): clean(v) for k, v in node.items() if str(k) not in blocked}
        if isinstance(node, list):
            return [clean(x) for x in node]
        if isinstance(node, tuple):
            return [clean(x) for x in node]
        return node

    raw = json.dumps(clean(value), sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_wire_object(value: Mapping[str, Any], *, strict_privacy: bool = True) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    schema = value.get("schema")
    protocols = protocol_map()
    spec = protocols.get(str(schema))
    if not schema:
        errors.append("missing_schema")
    elif not spec:
        errors.append(f"unknown_schema:{schema}")
    else:
        for field in spec.get("required") or []:
            if field not in value or value.get(field) is None:
                errors.append(f"missing_required:{field}")

    for path, key, child in walk(value):
        lowered = key.lower()
        if lowered in FORBIDDEN_REASONING_KEYS:
            errors.append(f"private_reasoning_field:{path}")
        if strict_privacy and lowered in SECRET_VALUE_KEYS:
            errors.append(f"secret_value_field:{path}")
        if strict_privacy and isinstance(child, str):
            for pattern in SECRET_PATTERNS:
                if pattern.search(child):
                    errors.append(f"secret_value_pattern:{path}")
                    break

    request_id = value.get("request_id")
    if request_id is not None and (not isinstance(request_id, str) or len(request_id) < 3 or len(request_id) > 200):
        errors.append("invalid_request_id")

    tenant_ids = []
    principal = value.get("principal")
    scope = value.get("scope")
    if isinstance(principal, Mapping) and principal.get("tenant_id"):
        tenant_ids.append(str(principal["tenant_id"]))
    if isinstance(scope, Mapping) and scope.get("tenant_id"):
        tenant_ids.append(str(scope["tenant_id"]))
    if len(set(tenant_ids)) > 1:
        errors.append("tenant_scope_mismatch")

    if schema == "nexus.execution-receipt.v1" and value.get("digest"):
        actual = stable_digest(value)
        if value.get("digest") != actual:
            errors.append("digest_mismatch")
    if schema == "nexus.secret-ref.v1" and "value" in value:
        errors.append("secret_ref_must_not_contain_value")
    if schema == "nexus.policy-decision.v1" and value.get("decision") not in {"allow", "deny", "confirm"}:
        errors.append("invalid_policy_decision")
    if schema == "nexus.health.v1" and value.get("status") not in {"healthy", "degraded", "not_ready", "unavailable"}:
        errors.append("invalid_health_status")

    return {"ok": not errors, "schema": schema, "errors": sorted(set(errors)), "warnings": sorted(set(warnings))}


def validate_correlation(values: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    values = list(values)
    request_ids = {str(v.get("request_id")) for v in values if v.get("request_id")}
    tenant_ids: set[str] = set()
    for value in values:
        for candidate in (value.get("scope"), value.get("principal"), value.get("subject"), value.get("provenance")):
            if isinstance(candidate, Mapping) and candidate.get("tenant_id"):
                tenant_ids.add(str(candidate["tenant_id"]))
    errors = []
    if len(request_ids) > 1:
        errors.append("request_id_mismatch")
    if len(tenant_ids) > 1:
        errors.append("tenant_id_mismatch")
    return {
        "ok": not errors,
        "request_id": next(iter(request_ids)) if len(request_ids) == 1 else None,
        "tenant_id": next(iter(tenant_ids)) if len(tenant_ids) == 1 else None,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="protocol-runtime")
    sub = parser.add_subparsers(dest="command", required=True)
    vp = sub.add_parser("validate")
    vp.add_argument("json_file")
    vp.add_argument("--allow-secret-shaped-fields", action="store_true")
    dp = sub.add_parser("digest")
    dp.add_argument("json_file")
    cp = sub.add_parser("correlate")
    cp.add_argument("json_files", nargs="+")
    args = parser.parse_args(argv)

    if args.command == "validate":
        obj = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        result = validate_wire_object(obj, strict_privacy=not args.allow_secret_shaped_fields)
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    if args.command == "digest":
        obj = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        print(stable_digest(obj))
        return 0
    objects = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.json_files]
    result = validate_correlation(objects)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
