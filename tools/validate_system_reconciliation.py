#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECON = ROOT / "registry" / "system-reconciliation.json"
REGISTRY = ROOT / "registry" / "ecosystem-alpha.json"

VALID_CLASSES = {
    "canonical",
    "feeder",
    "product_surface",
    "research_authority",
    "historical",
    "incubation",
    "duplicate_candidate",
    "exposure_review",
}


def fail(message: str) -> None:
    raise SystemExit(f"system-reconciliation-validation: FAIL: {message}")


def as_classes(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []


def main() -> int:
    data = json.loads(RECON.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    if data.get("schema") != "nexus.system-reconciliation.v1":
        fail("wrong schema")
    if data.get("authority") != "ItsNotAILABS/nexus":
        fail("NEXUS must remain reconciliation authority")

    planes = data.get("canonical_planes") or []
    if len(planes) < 10:
        fail("canonical plane map is unexpectedly small")
    plane_names = [p.get("plane") for p in planes]
    if len(plane_names) != len(set(plane_names)):
        fail("duplicate canonical plane")

    decisions = data.get("repository_decisions") or []
    repos = [d.get("repo") for d in decisions]
    if len(repos) != len(set(repos)):
        fail("duplicate repository decision")

    for decision in decisions:
        repo = decision.get("repo")
        classes = as_classes(decision.get("classification"))
        if not repo or not classes:
            fail("repository decision missing repo or classification")
        invalid = set(classes) - VALID_CLASSES
        if invalid:
            fail(f"invalid classification for {repo}: {sorted(invalid)}")
        if not decision.get("action"):
            fail(f"missing reconciliation action for {repo}")

    canonical_authorities = {}
    for plane in planes:
        authority = plane.get("authority")
        if not authority:
            fail(f"missing authority for plane {plane.get('plane')}")
        canonical_authorities.setdefault(authority, []).append(plane.get("plane"))

    if canonical_authorities.get("ItsNotAILABS/nexus") != ["federation"]:
        fail("NEXUS federation authority was diluted or duplicated")

    internals = data.get("named_internal_architecture") or {}
    for required in ["ORIGO", "SENSUS", "CORPUS", "MEMORIA", "MATHESIS", "NEXUS"]:
        if required not in internals:
            fail(f"missing named architecture mapping: {required}")
        if not internals[required].get("canonical_home"):
            fail(f"missing canonical home for {required}")

    rules = data.get("integration_rules") or []
    if len(rules) < 5:
        fail("integration rules are incomplete")
    if not any("implemented once" in rule.lower() for rule in rules):
        fail("missing single-canonical-implementation rule")
    if not any("visibility" in rule.lower() for rule in rules):
        fail("missing visibility/exposure rule")

    priorities = data.get("priority_actions") or []
    numbers = [p.get("priority") for p in priorities]
    if numbers != sorted(numbers) or len(numbers) != len(set(numbers)):
        fail("priority actions must have unique ascending priority numbers")

    ecosystem_repos = {c.get("repo") for c in registry.get("components") or []}
    if "ItsNotAILABS/nexus" not in ecosystem_repos:
        fail("canonical ecosystem registry lost NEXUS")

    print(
        "system-reconciliation-validation: PASS "
        f"({len(planes)} planes, {len(decisions)} repository decisions, "
        f"{len(internals)} named architecture mappings)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
