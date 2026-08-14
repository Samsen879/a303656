#!/usr/bin/env python3
"""Exact description-to-integer bipartite incidence adapter."""
import argparse
import sys
from collections import Counter
from pathlib import Path

from common import CensusError, atomic_json, canonical_digest, deduplicate, load_json, validate_descriptions


def build(panel: dict) -> dict:
    descriptions = panel.get("descriptions")
    if not isinstance(descriptions, list):
        raise CensusError("panel descriptions malformed")
    validate_descriptions(descriptions)
    integers = deduplicate(descriptions)
    multiplicities = Counter(row["description_multiplicity"] for row in integers)
    collisions = [row for row in integers if row["description_multiplicity"] > 1]
    incidence_payload = [{"n": row["n"], "description_ids": row["description_ids"]} for row in integers]
    return {
        "schema": "a303656-p5-family-u-incidence-v1", "raw_description_count": 457,
        "distinct_CRT_class_count": panel["distinct_CRT_class_count"], "distinct_integer_count": len(integers),
        "integers_generated_by_exactly_1_description": multiplicities[1],
        "integers_generated_by_exactly_2_descriptions": multiplicities[2],
        "integers_generated_by_exactly_3_descriptions": multiplicities[3],
        "integers_generated_by_at_least_4_descriptions": sum(v for k, v in multiplicities.items() if k >= 4),
        "maximum_description_multiplicity": max(multiplicities), "collision_groups": collisions,
        "canonical_incidence_digest": canonical_digest(incidence_payload), "integers": integers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(load_json(args.panel))
        atomic_json(args.output, result)
        print(f"DEDUPLICATION_PASS descriptions=457 integers={result['distinct_integer_count']}")
        return 0
    except (CensusError, OSError, ValueError) as exc:
        print(f"deduplicator: ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
