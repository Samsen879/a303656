#!/usr/bin/env python3
"""Canonical utilities for forensic recovery and fail-closed Gate V2 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

STATUSES = ("COMPLETE", "PARTIAL", "MISSING", "NOT_APPLICABLE", "NOT_ESTABLISHED")
LEVELS = (
    "E0_DESIGN_ONLY",
    "E1_BINARY_REPRESENTABILITY_CHECK",
    "E2_EXACT_T_COUNT",
    "E3_COMPLETE_WINNER_MASK",
    "E4_DIRECT_ORACLE_OR_WITNESS_VERIFIED",
)
GATES = (
    "V2.1_CORE_EXACT_RESULT",
    "V2.2_REGISTRY_INTEGRITY",
    "V2.3_ANY_RECORDED_EVALUATION_NON_REUSE",
    "V2.4_EXACT_T_NON_REUSE",
    "V2.5_SELECTION_T_BLIND",
    "V2.6_HIERARCHICAL_BALANCE",
    "V2.7_CONTROLLED_COMPARISON",
    "V2.8_IMMUTABLE_PREREGISTRATION",
    "V2.9_INDEPENDENT_AUTHORIZATION",
)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def close(doc: dict) -> dict:
    doc["canonical_digest"] = digest({k: v for k, v in doc.items() if k != "canonical_digest"})
    return doc


def normalize(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    for low, high in sorted(intervals):
        if low > high:
            raise ValueError("INTERVAL_ENDPOINT_ORDER")
        if out and low <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], high)
        else:
            out.append([low, high])
    return [(a, b) for a, b in out]


def union_length(intervals: list[tuple[int, int]]) -> int:
    return sum(high - low + 1 for low, high in normalize(intervals))
