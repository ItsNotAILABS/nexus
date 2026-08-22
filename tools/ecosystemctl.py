#!/usr/bin/env python3
"""NEXUS ecosystem operator CLI.

Dependency-free registry inspection, deterministic routing, promotion-gap review,
and bounded nexus.plan.v1 compilation. This tool plans work but never executes it.
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

STOPWORDS = {"a", "an", "and", "the", "to", "of", "for", "in", "on", "with", "from", "me", "my", "our", "this", "that", "please", "make", "create"}

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

DEFAULT_ACTION = {
    "nexus": "ecosystem.route",
    "pocket": "host.route",
    "pocket-agent": "agent.run",
    "pocket-voice": "voice.turn.decide",
    "nova-intelligence": "intelligence.plan.review",
    "phantom-sdk": "sdk.compatibility.check",
    "x-mcp-skills": "connector.plan_run",
    "organism-bots": "organism.route_plan",
    "matdaemon": "compute.validate_matrices",
    "capsula": "capsula.session.run",
    "medina-memory-systems": "memory.context.query",
    "auro-mesie-runtime": "model.capabilities",
    "auro14b": "model.family.describe",
    "nova-connector-control-plane": "connector.route_plan",
    "nova-app-containers": "container.build.plan",
    "phone-ai": "phone.command.plan",
    "researchers-hub": "research.construct",
    "cybersecurity-ai": "security.policy.check",
    "chimeria": "chimeria.simulation.plan",
    "parralax": "market.order.plan",
    "parallax-clearinghouse": "clearing.settlement.plan",
    "sovereign-forge-os": "forge.plan.compile",
}

INTENT_ACTION_HINTS = [
    ({"matrix", "matmul", "similarity"}, "matdaemon", "compute.validate_matrices"),
    ({"benchmark", "compute"}, "matdaemon", "compute.benchmark_smoke"),
    ({"capsule", "sandbox", "wasm"}, "capsula", "capsula.session.run"),
    ({"voice", "speech", "audio"}, "pocket-voice", "voice.turn.decide"),
    ({"memory", "recall", "context"}, "medina-memory-systems", "memory.context.query"),
    ({"trade", "order", "market"}, "parralax", "market.order.plan"),
    ({"netting", "clearing", "settlement"}, "parallax-clearinghouse", "clearing.netting.compute"),
    ({"security", "incident", "iam"}, "cybersecurity-ai", "security.policy.check"),
    ({"research", "paper", "figure"}, "researchers-hub", "research.construct"),
    ({"deploy", "container", "image"}, "nova-app-containers", "container.build.plan"),
    ({"phone", "mobile", "device"}, "phone-ai", "phone.command.plan"),
    ({"connector", "mcp", "claude", "grok"}, "nova-connector-control-plane", "connector.route_plan"),
    ({"checkpoint", "auro"}, "auro14b", "model.checkpoint.inventory"),
]

HIGH_RISK = {"production", "live", "weapon", "settle", "transfer"}
MEDIUM_RISK = {"deploy", "publish", "trade", "delete", "revoke", "write", "execute", "shell", "network_scan"}
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
    return f"{prefix}_{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]}"


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
    return [x for x in (data or registry()).get("components", []) if isinstance(x, dict)]


def tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9][a-z0-9_.-]+", text.lower()) if t not in STOPWORDS and len(t) > 1}


def route(intent: str, items: Iterable[dict[str, Any]]) -> dict[str, Any]:
    tokens = tokenize(intent)
    ranked = []
    for item in items:
        plane = str(item.get("plane") or "")
        component = str(item.get("component") or "")
        authority = [str(x) for x in item.get("authority") or []]
        searchable = tokenize(" ".join([component, str(item.get("repo") or ""), plane, *authority]))
        direct = len(tokens & searchable)
        plane_hits = len(tokens & PLANE_TERMS.get(plane, set()))
        exact = 2 if component.lower() in intent.lower() else 0
        status = str(item.get("status") or "activation-candidate")
        weight = {"active": 1.0, "protocol-ready": 0.88, "activation-candidate": 0.68}.get(status, 0.6)
        score = min(1.0, ((direct * 2.0 + plane_hits * 1.5 + exact) / max(2.0, len(tokens) * 2.0)) * weight)
        ranked.append({**item, "score": round(score, 3)})
    ranked.sort(key=lambda x: (-x["score"], str(x.get("component"))))
    best = ranked[0] if ranked else None
    confidence = float(best["score"]) if best else 0.0
    return {"intent": intent, "selected": best, "confidence": confidence, "needs_review": best is None or confidence < 0.28, "alternatives": ranked[:5]}


def select_action(intent: str, component: str) -> str:
    tokens = tokenize(intent)
    for hints, target, action in INTENT_ACTION_HINTS:
        if target == component and tokens & hints:
            return action
    return DEFAULT_ACTION.get(component, "component.describe")


def promotion_gaps(item: dict[str, Any], data: dict[str, Any]) -> list[str]:
    rules = data.get("promotion_rules") or {}
    if item.get("status") == "activation-candidate":
        return list(rules.get("activation-candidate_to_protocol-ready") or [])
    if item.get("status") == "protocol-ready":
        return list(rules.get("protocol-ready_to_active") or [])
    return []


def risk_for_intent(intent: str, requested: str | None = None) -> str:
    if requested:
        return requested
    tokens = tokenize(intent)
    if tokens & HIGH_RISK:
        return "high"
    if tokens & MEDIUM_RISK:
        return "medium"
    return "low"


def compile_plan(intent: str, *, tenant: str, principal: str, project: str, session: str | None = None, risk: str | None = None) -> dict[str, Any]:
    data = registry()
    routing = route(intent, components(data))
    selected = routing.get("selected")
    if not selected:
        raise SystemExit("no ecosystem component available")
    component = str(selected["component"])
    action = select_action(intent, component)
    risk_tier = risk_for_intent(intent, risk)
    candidate = selected.get("status") == "activation-candidate"
    confirmation = risk_tier in {"medium", "high"} or routing["needs_review"] or candidate
    seed = "|".join([intent, tenant, principal, project, session or ""])
    request_id = stable_id("req", seed)
    plan_id = stable_id("plan", seed + "|" + component + "|" + action)

    policy_reasons = []
    if routing["needs_review"]:
        policy_reasons.append("low_route_confidence")
    if candidate:
        policy_reasons.append("activation_candidate_requires_review")
    if risk_tier in {"medium", "high"}:
        policy_reasons.append("high_impact_or_mutating_intent")
    if not policy_reasons:
        policy_reasons.append("bounded_low_risk_intent")

    budget_limits = dict(DEFAULT_BUDGET)
    if risk_tier == "high":
        budget_limits.update({"max_cost_usd": 5.0, "max_external_calls": 5, "max_files_changed": 10})

    steps = [
        {"id": "discover", "component": "nexus", "action": "ecosystem.route", "depends_on": [], "output": "capability route"},
        {"id": "policy", "component": "pocket", "action": "host.policy.decide", "depends_on": ["discover"], "output": "nexus.policy-decision.v1"},
    ]
    if confirmation:
        steps.append({"id": "approval", "component": "pocket", "action": "host.approval.request", "depends_on": ["policy"], "output": "nexus.approval.v1"})
    steps.extend([
        {"id": "execute", "component": component, "action": action, "depends_on": ["approval" if confirmation else "policy"], "output": "artifact + nexus.execution-receipt.v1"},
        {"id": "evaluate", "component": "pocket-agent" if component != "pocket-agent" else "nexus", "action": "agent.evaluate_outcome" if component != "pocket-agent" else "ecosystem.evaluate", "depends_on": ["execute"], "output": "acceptance result"},
        {"id": "handoff", "component": "nexus", "action": "ecosystem.handoff", "depends_on": ["evaluate"], "output": "nexus.handoff.v1"},
    ])

    return {
        "schema": "nexus.plan.v1",
        "plan_id": plan_id,
        "request_id": request_id,
        "intent": intent,
        "principal": {"schema": "nexus.identity-ref.v1", "principal_id": principal, "principal_type": "user", "tenant_id": tenant, "auth_context": "operator-supplied-reference"},
        "scope": {"tenant_id": tenant, "project_id": project, "session_id": session},
        "route": routing,
        "risk_tier": risk_tier,
        "policy": {"schema": "nexus.policy-decision.v1", "request_id": request_id, "decision": "confirm" if confirmation else "allow", "policy_id": "nexus.alpha.plan-compiler.v1", "reasons": policy_reasons, "decided_at": now()},
        "budget": {"schema": "nexus.budget.v1", "limits": budget_limits},
        "steps": steps,
        "acceptance": {"require_receipt": True, "require_artifact_hashes_for_outputs": True, "require_tenant_correlation": True, "require_request_correlation": True, "allow_private_reasoning_export": False, "require_operator_approval": confirmation},
        "created_at": now(),
    }


def emit(value: Any) -> None:
    print(json.dumps(value, indent=2))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ecosystemctl")
    sub = p.add_subparsers(dest="command", required=True)
    lp = sub.add_parser("list"); lp.add_argument("--status"); lp.add_argument("--plane")
    dp = sub.add_parser("describe"); dp.add_argument("component")
    sub.add_parser("protocols")
    rp = sub.add_parser("route"); rp.add_argument("intent")
    gp = sub.add_parser("gaps"); gp.add_argument("--status")
    pp = sub.add_parser("plan"); pp.add_argument("intent"); pp.add_argument("--tenant", required=True); pp.add_argument("--principal", required=True); pp.add_argument("--project", required=True); pp.add_argument("--session"); pp.add_argument("--risk", choices=["low", "medium", "high"]); pp.add_argument("--output")
    args = p.parse_args(argv)

    if args.command == "list":
        rows = components()
        if args.status: rows = [x for x in rows if x.get("status") == args.status]
        if args.plane: rows = [x for x in rows if x.get("plane") == args.plane]
        emit(rows)
    elif args.command == "describe":
        matches = [x for x in components() if args.component in {x.get("component"), x.get("repo")}]
        if not matches: raise SystemExit(f"unknown component: {args.component}")
        item = dict(matches[0]); item["promotion_gaps"] = promotion_gaps(item, registry()); emit(item)
    elif args.command == "protocols":
        emit(protocols())
    elif args.command == "route":
        emit(route(args.intent, components()))
    elif args.command == "gaps":
        data = registry(); rows = [{"component": x.get("component"), "repo": x.get("repo"), "status": x.get("status"), "next_gate": promotion_gaps(x, data)} for x in components(data) if promotion_gaps(x, data)]
        if args.status: rows = [x for x in rows if x["status"] == args.status]
        emit(rows)
    elif args.command == "plan":
        plan = compile_plan(args.intent, tenant=args.tenant, principal=args.principal, project=args.project, session=args.session, risk=args.risk)
        if args.output:
            Path(args.output).write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8"); print(args.output)
        else: emit(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
