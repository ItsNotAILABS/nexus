#!/usr/bin/env python3
"""Validate the Corpus de Architectura contract against NEXUS registries.

This gate checks research-to-code alignment. It does not claim that an
architecture is deployed, that a checkpoint is trained, or that an experiment
has been executed. Those remain separate evidence states.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "research" / "corpus-architectura-v2.1.json"
PROTOCOLS = ROOT / "protocols" / "ecosystem.protocols.json"
ECOSYSTEM = ROOT / "registry" / "ecosystem-alpha.json"

EXPECTED_VOLUME_I = {1, 4, 7, 8, 9}
EXPECTED_VOLUME_II = {2, 3, 5, 6, 10, 11, 12, 13}
EXPECTED_LANES = [
    "Auro-156K",
    "Auro-250M",
    "Auro-500M",
    "Auro-2B",
    "Auro-4B",
    "Auro-8B",
    "Auro-14B",
    "Auro-100B",
]
EXPECTED_TRIAD = [
    "Auro-500M-SENSUS",
    "Auro-500M-PRAXIS",
    "Auro-500M-VERBUM",
]
EXPECTED_EVIDENCE = [
    "E0-assertion",
    "E1-source",
    "E2-execution-log",
    "E3-validated-output",
    "E4-signed-receipt",
    "E5-external-custody-and-reproduction",
]


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def canonical_sha(value: dict[str, Any]) -> str:
    copy = dict(value)
    copy.pop("content_sha256", None)
    raw = json.dumps(copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    corpus = load(CORPUS)
    protocols = load(PROTOCOLS)
    ecosystem = load(ECOSYSTEM)
    errors: list[str] = []

    if corpus.get("schema") != "medina.corpus-architectura.v2":
        errors.append("unexpected corpus schema")
    if corpus.get("version") != "2.1.0":
        errors.append("corpus version must be 2.1.0")
    if corpus.get("authority") != "ItsNotAILABS/nexus":
        errors.append("NEXUS must remain the protocol authority")
    if canonical_sha(corpus) != corpus.get("content_sha256"):
        errors.append("corpus content_sha256 does not match canonical content")

    papers = corpus.get("papers") or []
    numbers = [int(item.get("number", 0)) for item in papers]
    ids = [str(item.get("id", "")) for item in papers]
    if numbers != list(range(1, 14)):
        errors.append(f"paper numbers must be ordered 1..13, got {numbers}")
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        errors.append("paper IDs must be non-empty and unique")
    if int(corpus.get("publication", {}).get("paper_count", 0)) != 13:
        errors.append("publication.paper_count must be 13")

    volume_i = {int(item["number"]) for item in papers if item.get("volume") == "I"}
    volume_ii = {int(item["number"]) for item in papers if item.get("volume") == "II"}
    if volume_i != EXPECTED_VOLUME_I:
        errors.append(f"Volume I mismatch: {sorted(volume_i)}")
    if volume_ii != EXPECTED_VOLUME_II:
        errors.append(f"Volume II mismatch: {sorted(volume_ii)}")

    protocol_ids = {str(item.get("id")) for item in protocols.get("protocols", [])}
    referenced_protocols = {
        str(contract)
        for paper in papers
        for contract in paper.get("primary_contracts", [])
    }
    missing_protocols = sorted(referenced_protocols - protocol_ids)
    if missing_protocols:
        errors.append(f"unregistered paper contracts: {missing_protocols}")

    registered_repos = {
        str(item.get("repo")) for item in ecosystem.get("components", [])
    }
    referenced_repos = {
        str(repo)
        for paper in papers
        for repo in paper.get("authority_repositories", [])
    }
    missing_repos = sorted(referenced_repos - registered_repos)
    if missing_repos:
        errors.append(f"paper authority repositories absent from ecosystem registry: {missing_repos}")

    invariants = corpus.get("system_invariants") or {}
    if invariants.get("auro_family_lanes") != EXPECTED_LANES:
        errors.append("AURO family lane order differs from canonical ladder")
    if invariants.get("auro_2b_specialist_triad") != EXPECTED_TRIAD:
        errors.append("AURO 2B specialist triad differs from canonical identities")
    if invariants.get("evidence_classes") != EXPECTED_EVIDENCE:
        errors.append("evidence classes differ from E0-E5 canonical order")
    if invariants.get("runtime_cells") != ["agent-sandbox", "app-bottle", "mini-os"]:
        errors.append("runtime cell classes must remain agent-sandbox, app-bottle, mini-os")
    if invariants.get("execution_sequence") != [
        "discover", "classify-risk", "plan", "approve", "execute", "validate", "receipt"
    ]:
        errors.append("governed execution sequence mismatch")

    roots = set((corpus.get("implementation_roots") or {}).keys())
    missing_roots = sorted(roots - registered_repos)
    if missing_roots:
        errors.append(f"implementation roots absent from ecosystem registry: {missing_roots}")

    if len(corpus.get("claim_boundaries") or []) < 8:
        errors.append("all eight truth boundaries must remain explicit")

    receipt = {
        "schema": "nexus.corpus-architecture-validation.v1",
        "corpus": corpus.get("corpus_id"),
        "version": corpus.get("version"),
        "paper_count": len(papers),
        "protocol_count": len(protocol_ids),
        "authority_repository_count": len(referenced_repos),
        "content_sha256": corpus.get("content_sha256"),
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }
    receipt["receipt_sha256"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
