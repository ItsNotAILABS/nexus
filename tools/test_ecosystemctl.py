#!/usr/bin/env python3
"""Dependency-free smoke tests for ecosystemctl."""
from __future__ import annotations

import ecosystemctl as ctl


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main() -> int:
    data = ctl.registry()
    items = ctl.components(data)
    check(len(items) >= 20, "ecosystem registry unexpectedly small")

    agent = ctl.route("run a long agent coding task", items)
    check(agent["selected"]["component"] == "pocket-agent", agent)
    check(agent["needs_review"] is False, agent)

    voice = ctl.route("voice conversation transcript turn", items)
    check(voice["selected"]["component"] == "pocket-voice", voice)

    compute = ctl.route("validate matrix compute shapes", items)
    check(compute["selected"]["component"] == "matdaemon", compute)

    memory = ctl.route("recall project memory context", items)
    check(memory["selected"]["component"] == "medina-memory-systems", memory)

    market = ctl.route("plan market order risk", items)
    check(market["selected"]["component"] == "parralax", market)

    candidate = next(x for x in items if x["component"] == "phone-ai")
    gaps = ctl.promotion_gaps(candidate, data)
    check("ecosystem.surface.json" in gaps, gaps)
    check("validation command" in gaps, gaps)

    low = ctl.compile_plan(
        "run a long agent coding task",
        tenant="tenant-a",
        principal="user-a",
        project="project-a",
        session="session-a",
    )
    check(low["schema"] == "nexus.plan.v1", low)
    check(low["route"]["selected"]["component"] == "pocket-agent", low)
    check(next(x for x in low["steps"] if x["id"] == "execute")["action"] == "agent.run", low)
    check(low["policy"]["decision"] == "allow", low)
    check(low["scope"]["tenant_id"] == "tenant-a", low)
    check(low["principal"]["tenant_id"] == "tenant-a", low)
    check(low["acceptance"]["allow_private_reasoning_export"] is False, low)

    high = ctl.compile_plan(
        "plan a live market trade",
        tenant="tenant-a",
        principal="user-a",
        project="market-a",
    )
    check(high["risk_tier"] == "high", high)
    check(high["policy"]["decision"] == "confirm", high)
    check(high["acceptance"]["require_operator_approval"] is True, high)
    check(any(x["id"] == "approval" for x in high["steps"]), high)
    check(high["budget"]["limits"]["max_external_calls"] == 5, high)

    phone = ctl.compile_plan(
        "send a phone device command",
        tenant="tenant-a",
        principal="user-a",
        project="mobile-a",
    )
    check(phone["route"]["selected"]["component"] == "phone-ai", phone)
    check(phone["policy"]["decision"] == "confirm", phone)
    check("activation_candidate_requires_review" in phone["policy"]["reasons"], phone)

    print("ecosystemctl-smoke: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
