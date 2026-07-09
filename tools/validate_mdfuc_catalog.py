#!/usr/bin/env python3
"""Validate the MDFUC catalog and repo-family registry.

Standard-library only so it can run in clean GitHub Actions, local terminals,
and agent workspaces without setup.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "mdfuc.catalog.json"
REPO_FAMILY_PATH = ROOT / "registry" / "repo-family.json"
ARTIFACT_PATH = ROOT / "registry" / "artifacts-v0.3.8.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def require_repo(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or "/" not in value or value.startswith("/"):
        errors.append(f"{label} must be an owner/repo string")


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not catalog.get("schema"):
        errors.append("catalog.schema is required")
    repos = catalog.get("active_repositories")
    if not isinstance(repos, list) or not repos:
        errors.append("catalog.active_repositories must be non-empty")
        return errors
    seen: set[str] = set()
    for index, entry in enumerate(repos):
        label = f"active_repositories[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        repo = entry.get("repo")
        require_repo(repo, f"{label}.repo", errors)
        if isinstance(repo, str) and repo in seen:
            errors.append(f"duplicate active repo: {repo}")
        if isinstance(repo, str):
            seen.add(repo)
        for field in ("role", "status", "next_gate"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{label}.{field} must be a non-empty string")
    return errors


def validate_repo_family(repo_family: dict[str, Any], catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    members = repo_family.get("members")
    if not isinstance(members, list) or not members:
        return ["repo-family.members must be non-empty"]
    catalog_members = {entry.get("repo") for entry in catalog.get("active_repositories", []) if isinstance(entry, dict)}
    for repo in members:
        require_repo(repo, "repo-family member", errors)
        if repo not in catalog_members:
            errors.append(f"repo-family member missing from catalog.active_repositories: {repo}")
    return errors


def validate_artifacts(artifact_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    artifacts = artifact_map.get("release_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return ["artifact map release_artifacts must be non-empty"]
    for index, artifact in enumerate(artifacts):
        label = f"release_artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("name", "repository", "target_path", "sha256", "upload_status"):
            if not isinstance(artifact.get(field), str) or not artifact[field].strip():
                errors.append(f"{label}.{field} must be a non-empty string")
        sha = artifact.get("sha256", "")
        if isinstance(sha, str) and len(sha) != 64:
            errors.append(f"{label}.sha256 must be a 64-character SHA-256 hex string")
    return errors


def main() -> int:
    catalog = load_json(CATALOG_PATH)
    repo_family = load_json(REPO_FAMILY_PATH)
    artifact_map = load_json(ARTIFACT_PATH)
    errors = validate_catalog(catalog) + validate_repo_family(repo_family, catalog) + validate_artifacts(artifact_map)
    if errors:
        print("MDFUC validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"MDFUC validation passed: {len(catalog.get('active_repositories', []))} active repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
