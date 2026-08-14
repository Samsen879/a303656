#!/usr/bin/env python3
"""Build the corrected immutable 13-mask holdout manifest from certified inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


class ManifestError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ManifestError(f"{path} is not a JSON object")
    return value


def build(root: Path) -> dict:
    original_path = root / "analysis/p4_weighted_transferability/results/candidate_manifest.json"
    maxima_path = root / "analysis/p4_weighted_transferability/results/weighted_maxima.json"
    original = load(original_path)
    maxima = load(maxima_path)
    candidates = original.get("candidates")
    if original.get("candidate_count") != 12 or not isinstance(candidates, list) or len(candidates) != 12:
        raise ManifestError("original manifest is not the certified 12-candidate manifest")
    old_masks = [item.get("coverage_mask_hex") for item in candidates if isinstance(item, dict)]
    if len(old_masks) != 12 or len(set(old_masks)) != 12 or any(not isinstance(mask, str) or len(mask) != 102 for mask in old_masks):
        raise ManifestError("original manifest masks are malformed or non-distinct")

    try:
        optimum = maxima["maxima"]["t3eq2"]["pool"]
    except (KeyError, TypeError) as exc:
        raise ManifestError("weighted maxima lacks the t3eq2 pooled optimum") from exc
    required = {
        "scope": "t3eq2",
        "weights": "pool",
        "G": 222,
        "lexicographically_first_argmax": [2, 13, 32, 13],
    }
    for key, expected in required.items():
        if optimum.get(key) != expected:
            raise ManifestError(f"certified t3eq2 optimum mismatch for {key}")
    new_mask = optimum.get("coverage_mask_hex")
    if not isinstance(new_mask, str) or len(new_mask) != 102:
        raise ManifestError("certified t3eq2 optimum mask is malformed")
    if new_mask in old_masks:
        raise ManifestError("certified t3eq2 optimum unexpectedly already exists in the old manifest")

    added = {
        "G": optimum["G"],
        "coverage_mask_hex": new_mask,
        "lexicographically_first_t3eq2_representative": optimum["lexicographically_first_argmax"],
        "selected_by": ["T3EQ2-WEIGHTED-OPT"],
        "certified_source": {
            "artifact": "analysis/p4_weighted_transferability/results/weighted_maxima.json",
            "scope": optimum["scope"],
            "weights": optimum["weights"],
            "maximum_score": optimum["maximum_score"],
            "argmax_digest": optimum["argmax_digest"],
        },
    }
    result = {
        "schema": "a303656-holdout-candidate-manifest-v2",
        "candidate_count": 13,
        "distinct_coverage_mask_count": 13,
        "original_manifest": "analysis/p4_weighted_transferability/results/candidate_manifest.json",
        "original_manifest_sha256": sha256_file(original_path),
        "weighted_maxima": "analysis/p4_weighted_transferability/results/weighted_maxima.json",
        "weighted_maxima_sha256": sha256_file(maxima_path),
        "construction_rule": "the original 12 candidate objects byte-semantically unchanged and in original order, followed by the certified t3eq2 pooled weighted optimum",
        "candidates": candidates + [added],
    }
    if result["candidates"][:12] != candidates or len({item["coverage_mask_hex"] for item in result["candidates"]}) != 13:
        raise ManifestError("internal corrected-manifest construction failure")
    return result


def write_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        write_atomic(args.output, build(args.root.resolve()))
        print("CORRECTED_FROZEN_MANIFEST_BUILT")
        return 0
    except (ManifestError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"build_manifest: ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
