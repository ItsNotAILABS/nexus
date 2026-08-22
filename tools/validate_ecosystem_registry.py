#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "registry" / "ecosystem-alpha.json"
VALID_STATUS = {"active", "protocol-ready", "activation-candidate"}


def fail(msg: str) -> None:
    raise SystemExit(f"ecosystem-registry-validation: FAIL: {msg}")


def main() -> int:
    data = json.loads(REG.read_text(encoding="utf-8"))
    if data.get("schema") != "nexus.ecosystem-registry.v1":
        fail("wrong schema")
    components = data.get("components") or []
    if len(components) < 10:
        fail("registry unexpectedly small")
    repos = [c.get("repo") for c in components]
    names = [c.get("component") for c in components]
    if len(repos) != len(set(repos)):
        fail("duplicate repository")
    if len(names) != len(set(names)):
        fail("duplicate component name")
    for c in components:
        if c.get("status") not in VALID_STATUS:
            fail(f"invalid status for {c.get('component')}")
        if not c.get("plane"):
            fail(f"missing plane for {c.get('component')}")
        if not isinstance(c.get("authority"), list) or not c["authority"]:
            fail(f"missing authority for {c.get('component')}")
    required = {"nexus", "pocket", "pocket-agent", "pocket-voice", "matdaemon", "capsula", "medina-memory-systems"}
    missing = required - set(names)
    if missing:
        fail("missing core components: " + ", ".join(sorted(missing)))
    rules = data.get("promotion_rules") or {}
    if not rules.get("protocol-ready_to_active"):
        fail("missing activation gate")
    print(f"ecosystem-registry-validation: PASS ({len(components)} components)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
