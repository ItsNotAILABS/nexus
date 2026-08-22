#!/usr/bin/env python3
"""NEXUS ecosystem operator CLI.

Dependency-free, deterministic tooling for inspecting the federation registry,
routing intents, surfacing activation gaps, and compiling bounded Alpha plans.
It does not execute tasks; it produces reviewable protocol objects for governed
runtimes such as POCKET Agent, MatDaemon, CAPSULA, and connector workers.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "ecosystem-alpha.json"
PROTOCOL_PATH = ROOT / "protocols" / "ecosystem.protocols.json"

STOPWORDS = {
    "a", "an", "and", "the", "to", "of", "for", "in", "on", "with", "from",
    "me", "my", "our", "this", "that", "please", "make", "create", "build",
}

PLANE_TERMS = {
    "federation": {"protocol", "registry", "compatibility", "federation", "route"},
    "user-team-policy": {"tenant", "user", "team", "policy", "rbac", "device", "account", "identity", "audit"},
    "execution": {"agent", "execute", "run", "task", "autonomous", "schedule", "capsule", "code"},
    "voice-conversation": {"voice", "audio", "speech", "talk", "conversation", "transcript", "vad", "stt"},
    "intelligence-contract": {"intelligence", "contract", "research", "compatibility", "evidence", "review"},
    "sdk": {"sdk", "client", "package", "schema", "integration"},
    "connector": {"connector", "mcp", "claude", "grok", "cursor", "caffeine", "external"},
    "workflow": {"workflow", "bot", "organism", "orchestrate", "route"},
    "compute": {"compute", "matrix", "matmul", "embedding", "benchmark", "train", "similarity"},
    "execution-capsule": {"sandbox", "capsule", "preview", "wasm", "isolate", "runtime"},
    "memory": {"memory", "recall", "retention", "vault", "context", "continuity"},
    "model": {"model", "inference", "checkpoint", "auro", "mesie", "embedding"},
    "deployment": {"deploy", "container", "image", "preview", "hosting"},
    "device-control": {"phone", "mobile", "device", "approval", "notification"},
    "research": {"research", "paper", "figure", "chart", "study", "publication"},
    "security": {"security", "cyber", "incident", "iam", "zero-trust", "grc", "threat"},
    "synthetic-cognition": {"chimeria", "entity", "state", "cognition", "simulation"},
    "market-execution": {"market", "trade", "risk", "portfolio", "signal", "order", "parralax"},
    "clearing": {"clearing", "netting", "settlement", "margin", "ledger"},
    "builder": {"forge", "builder", "build", "package", "release"},
}

HIGH_IMPACT_TERMS = {
    "deploy", "publish", "production", "live", "trade", "settle", "transfer",
    "delete", "revoke", "write", "execute", "shell", "network_scan", "weapon",
}

DEFAULT_BUDGET = {
    "wall_seconds": 300,
    "max_tokens": 120000,
    "max_cost_usd": 10.0,
    "max_files_changed": 25,
    "max_changed_bytes": 250000,
    "max_subprocesses": 20,
    "max_external_calls": 20,
    "max_children": 8,
    "artifact_bytes": 20000000,
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}") from exc


def registry() -> dict[str, Any]:
    return load_json(REGISTRY_PATH)


def protocols() -> dict[str, Any]:
    return load_json(PROTOCOL_PATH)


def components(data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    data = data or registry()
    return [x for x in data.get("components", []) if isinstance(x, dict)]


def tokenize(text: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9][a-z0-9_.-]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    }


def route(intent: str, items: Iterable[dict[str, Any]]) -> dict[str, Any]:
    tokens = tokenize(intent)
    ranked: list[dict[str, Any]] = []
    for item in items:
        plane = str(item.get("plane") or "")
        authority = [str(x) for x in item.get("authority") or []]
        component = str(item.get("component") or "")
        repo = str(item.get("repo") or "")
        searchable = tokenize(" ".join([component, repo, plane, *authority]))
        direct_hits = len(tokens & searchable)
        plane_hits = len(tokens & PLANE_TERMS.get(plane, set()))
        exact_component = 2 if component.lower() in intent.lower() else 0
        status = str(item.get("status") or "activation-candidate")
        status_weight = {"active": 1.0, "protocol-ready": 0.88, "activation-candidate": 0.68}.get(status, 0.6)
        raw = direct_hits * 2.0 + plane_hits * 1.5 + exact_component
        denominator = max(2.0, len(tokens) * 2.0)
        score = min(1.0, (raw / denominator) * status_weight)
        ranked.append({
            "component": component,
            "repo": repo,
            "plane": plane,
            "status": status,
            "score": round(score, 3),
            "authority": authority,
        })
    ranked.sort(key=lambda x: (-x["score"], x["component"]))
    best = ranked[0] if ranked else None
    confidence = float(best["score"]) if best else 0.0
    return {
        "intent": intent,
        "selected": best,
        "confidence": confidence,
        "needs_review": best is None or confidence < 0.28,
        "alternatives": ranked[:5],
    }


def promotion_gaps(item: dict[str, Any], data: dict[str, Any]) -> list[str]:
    status = item.get("status")
    rules = data.get("promotion_rules") or {}
    if status == "activation-candidate":
        return list(rules.get("activation-candidate_to_protocol-ready") or [])
    if status == "protocol-ready":
        return list(rules.get("protocol-ready_to_active") or [])
    return []


def risk_for_intent(intent: str, requested: str | None = None) -> str:
    if requested:
        return requested
    tokens = tokenize(intent)
    if tokens & {"weapon", "settle", "transfer", "production", "live"}:
        return "high"
    if tokens & HIGH_IMPACT_TERMS:
        return "medium"
    return "low"


def compile_plan(
    intent: str,
    *,
    tenant: str,
    principal: str,
    project: str,
    session: str | None = None,
    risk: str | None = None,
) -> dict[str, Any]:
    data = registry()
    routing = route(intent, components(data))
    selected = routing.get("selected")
    if not selected:
        raise SystemExit("no ecosystem component available")

    risk_tier = risk_for_intent(intent, risk)
    review = routing["needs_review"] or selected["status"] == "activation-candidate"
    confirmation = risk_tier in {"medium", "high"} or review
    request_seed = "|".join([intent, tenant, principal, project, session or ""])
    request_id = stable_id("req", request_seed)
    plan_id = stable_id("plan", request_seed + "|" + str(selected["component"]))

    policy = {
        "schema": "nexus.policy-decision.v1",
        "request_id": request_id,
        "decision": "confirm" if confirmation else "allow",
        "policy_id": "nexus.alpha.plan-compiler.v1",
        "reasons": (
            ["ambiguous_or_candidate_route"] if review else []
        ) + (["high_impact_or_mutating_intent"] if risk_tier in {"medium", "high"} else ["bounded_low_risk_intent"]),
        "decided_at": now(),
    }
    budget = {"schema": "nexus.budget.v1", "limits": dict(DEFAULT_BUDGET)}
    if risk_tier == "high":
        budget["limits"].update({"max_cost_usd": 5.0, "max_external_calls": 5, "max_files_changed": 10})

    steps: list[dict[str, Any]] = [
        {
            "id": "discover",
            "component": "nexus",
            "action": "ecosystem.route",
            "depends_on": [],
            "output": "capability route",
        },
        {
            "id": "policy",
            "component": "pocket" if any(c.get("component") == "pocket" for c in components(data)) else "nexus",
            "action": "host.policy.decide",
            "depends_on": ["discover"],
            "output": "policy decision",
        },
    ]
    if confirmation:
        steps.append({
            "id": "approval",
            "component": "pocket",
            "action": "host.approval.request",
            "depends_on": ["policy"],
            "output": "nexus.approval.v1",
        })
    execution_dep = "approval" if confirmation else "policy"
    steps.extend([
        {
            "id": "execute",
            "component": selected["component"],
            "action": "component-selected-action",
            "depends_on": [execution_dep],
            "output": "artifact + execution receipt",
        },
        {
            "id": "evaluate",
            "component": "pocket-agent" if selected["component"] != "pocket-agent" else "nexus",
            "action": "agent.evaluate_outcome" if selected["component"] != "pocket-agent" else "ecosystem.evaluate",
            "depends_on": ["execute"],
            "output": "acceptance result",
        },
        {
            "id": "handoff",
            "component": "nexus",
            "action": "ecosystem.handoff",
            "depends_on": ["evaluate"],
            "output": "nexus.handoff.v1",
        },
    ])

    acceptance = {
        "require_receipt": True,
        "require_artifact_hashes_for_outputs": True,
        "require_tenant_correlation": True,
        "require_request_correlation": True,
        "allow_private_reasoning_export": False,
        "require_operator_approval": confirmation,
    }

    return {
        "schema": "nexus.plan.v1",
        "plan_id": plan_id,
        "request_id": request_id,
        "intent": intent,
        "principal": {
            "schema": "nexus.identity-ref.v1",
            "principal_id": principal,
            "principal_type": "user",
            "tenant_id": tenant,
            "auth_context": "operator-supplied-reference",
        },
        "scope": {
            "tenant_id": tenant,
            "project_id": project,
            "session_id": session,
        },
        "route": routing,
        "risk_tier": risk_tier,
        "policy": policy,
        "budget": budget,
        "steps": steps,
        "acceptance": acceptance,
        "created_at": now(),
    }


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=False))


def command_list(args: argparse.Namespace) -> int:
    rows = components()
    if args.status:
        rows = [r for r in rows if r.get("status") == args.status]
    if args.plane:
        rows = [r for r in rows if r.get("plane") == args.plane]
    print_json(rows)
    return 0


def command_describe(args: argparse.Namespace) -> int:
    matches = [c for c in components() if args.component in {c.get("component"), c.get("repo")}]
    if not matches:
        raise SystemExit(f"unknown component: {args.component}")
    item = dict(matches[0])
    item["promotion_gaps"] = promotion_gaps(item, registry())
    print_json(item)
    return 0


def command_protocols(_: argparse.Namespace) -> int:
    print_json(protocols())
    return 0


def command_route(args: argparse.Namespace) -> int:
    print_json(route(args.intent, components()))
    return 0


def command_gaps(args: argparse.Namespace) -> int:
    data = registry()
    rows = []
    for item in components(data):
        gaps = promotion_gaps(item, data)
        if gaps:
            rows.append({
                "component": item.get("component"),
                "repo": item.get("repo"),
                "status": item.get("status"),
                "next_gate": gaps,
            })
    if args.status:
        rows = [r for r in rows if r["status"] == args.status]
    print_json(rows)
    return 0


def command_plan(args: argparse.Namespace) -> int:
    plan = compile_plan(
        args.intent,
        tenant=args.tenant,
        principal=args.principal,
        project=args.project,
        session=args.session,
        risk=args.risk,
    )
    if args.output:
        path = Path(args.output)
        path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        print(path)
    else:
        print_json(plan)
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ecosystemctl", description="Inspect and plan against the NEXUS ecosystem registry")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("list", help="list registered ecosystem components")
    sp.add_argument("--status", choices=["active", "protocol-ready", "activation-candidate"])
    sp.add_argument("--plane")
    sp.set_defaults(func=command_list)

    sp = sub.add_parser("describe", help="describe a component and its promotion gaps")
    sp.add_argument("component")
    sp.set_defaults(func=command_describe)

    sp = sub.add_parser("protocols", help="print the canonical protocol registry")
    sp.set_defaults(func=command_protocols)

    sp = sub.add_parser("route", help="rank components for a natural-language intent")
    sp.add_argument("intent")
    sp.set_defaults(func=command_route)

    sp = sub.add_parser("gaps", help="show promotion requirements for non-active components")
    sp.add_argument("--status", choices=["protocol-ready", "activation-candidate"])
    sp.set_defaults(func=command_gaps)

    sp = sub.add_parser("plan", help="compile a bounded nexus.plan.v1")
    sp.add_argument("intent")
    sp.add_argument("--tenant", required=True)
    sp.add_argument("--principal", required=True)
    sp.add_argument("--project", required=True)
    sp.add_argument("--session")
    sp.add_argument("--risk", choices=["low", "medium", "high"])
    sp.add_argument("--output")
    sp.set_defaults(func=command_plan)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
