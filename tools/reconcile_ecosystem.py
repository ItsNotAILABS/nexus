#!/usr/bin/env python3
"""Inspect the whole-system authority map without executing external actions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECON = ROOT / "registry" / "system-reconciliation.json"


def load() -> dict:
    return json.loads(RECON.read_text(encoding="utf-8"))


def emit(value) -> None:
    print(json.dumps(value, indent=2))


def classes(value) -> list[str]:
    return [value] if isinstance(value, str) else list(value or [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reconcile-ecosystem")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("summary")
    sub.add_parser("priorities")
    sub.add_parser("internals")
    sub.add_parser("planes")

    rp = sub.add_parser("repos")
    rp.add_argument("--class", dest="classification")

    dp = sub.add_parser("describe")
    dp.add_argument("name")

    args = parser.parse_args(argv)
    data = load()

    if args.command == "summary":
        decisions = data.get("repository_decisions") or []
        counts: dict[str, int] = {}
        for item in decisions:
            for classification in classes(item.get("classification")):
                counts[classification] = counts.get(classification, 0) + 1
        emit({
            "schema": data.get("schema"),
            "version": data.get("version"),
            "authority": data.get("authority"),
            "canonical_planes": len(data.get("canonical_planes") or []),
            "repository_decisions": len(decisions),
            "named_internal_architecture": sorted((data.get("named_internal_architecture") or {}).keys()),
            "classification_counts": counts,
            "top_priorities": (data.get("priority_actions") or [])[:5],
        })
        return 0

    if args.command == "priorities":
        emit(data.get("priority_actions") or [])
        return 0

    if args.command == "internals":
        emit(data.get("named_internal_architecture") or {})
        return 0

    if args.command == "planes":
        emit(data.get("canonical_planes") or [])
        return 0

    if args.command == "repos":
        rows = data.get("repository_decisions") or []
        if args.classification:
            rows = [row for row in rows if args.classification in classes(row.get("classification"))]
        emit(rows)
        return 0

    if args.command == "describe":
        name = args.name.lower()
        for item in data.get("repository_decisions") or []:
            if name in str(item.get("repo", "")).lower():
                emit(item)
                return 0
        for key, item in (data.get("named_internal_architecture") or {}).items():
            if name == key.lower():
                emit({"name": key, **item})
                return 0
        raise SystemExit(f"no reconciliation record matching: {args.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
