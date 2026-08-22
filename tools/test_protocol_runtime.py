#!/usr/bin/env python3
from protocol_runtime import stable_digest, validate_correlation, validate_wire_object


def main() -> int:
    policy = {
        "schema": "nexus.policy-decision.v1",
        "request_id": "req-1",
        "decision": "allow",
        "policy_id": "p1",
        "reasons": ["scope_match"],
        "decided_at": "2026-08-22T00:00:00Z",
        "principal": {"tenant_id": "t1"},
        "scope": {"tenant_id": "t1"},
    }
    assert validate_wire_object(policy)["ok"] is True
    invalid = dict(policy)
    invalid["decision"] = "unknown"
    assert "invalid_policy_decision" in validate_wire_object(invalid)["errors"]

    receipt = {
        "schema": "nexus.execution-receipt.v1",
        "request_id": "req-1",
        "status": "succeeded",
        "component": "matdaemon",
        "started_at": "2026-08-22T00:00:00Z",
        "finished_at": "2026-08-22T00:00:01Z",
    }
    receipt["digest"] = stable_digest(receipt)
    assert validate_wire_object(receipt)["ok"] is True
    receipt["component"] = "changed"
    assert "digest_mismatch" in validate_wire_object(receipt)["errors"]

    correlated = validate_correlation([
        {"request_id": "req-1", "scope": {"tenant_id": "t1"}},
        {"request_id": "req-1", "provenance": {"tenant_id": "t1"}},
    ])
    assert correlated["ok"] is True
    mismatch = validate_correlation([
        {"request_id": "req-1", "scope": {"tenant_id": "t1"}},
        {"request_id": "req-2", "scope": {"tenant_id": "t2"}},
    ])
    assert set(mismatch["errors"]) == {"request_id_mismatch", "tenant_id_mismatch"}

    print("protocol-runtime-smoke: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
