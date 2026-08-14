#!/usr/bin/env python3
"""Source-only authority reconstruction and exact census helpers."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

EXPECTED_R = "1a3b130536245ef8fcd318b591e1dd37c03eef06"
EXPECTED_Q = "4605e09047bc8ca934392c3e26a3ec8f7e8c7370"
DESIGN = "analysis/p5_sparse_panel_feasibility/results/design_C_full_sparse_census.json"
OCCUPIED = "analysis/p5_sparse_panel_feasibility/results/occupied_fresh_class_manifest.jsonl"
REGISTRY = "analysis/p5_sparse_panel_feasibility/results/prior_evaluation_registry.json"
POLICY = "analysis/p5_family_u_census/source_policy.json"
PAIR_FREQUENCIES = "analysis/p4_maximizer_census/pair_frequencies.csv"
P4_HISTOGRAM = "analysis/p4_maximizer_census/global_histogram.csv"
DESIGN_SHA256 = "eda6eaf490dde061f63a82bf99da7833149c6b8b2f1fcc14755cb895775c13d6"
OCCUPIED_SHA256 = "534ca89f5ab80dd1047eded6a84dccaacdc453baa569b8ec8b1b3ffb64884b7a"
REGISTRY_SHA256 = "428f5abee8462d21777326c9fbdf9aa215d722f43d9ceaed75b980e30c4158af"
PAIR_COUNT = 407
MASK_BYTES = 51
CELL_LOW = 183_968_950_234
CELL_HIGH = 246_731_069_451
THRESHOLDS = (0, 10, 12, 14, 15, 16, 18, 20, 24)


class CensusError(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise CensusError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
    temporary.replace(path)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    temporary.replace(path)


def feasibility_module(root: Path):
    path = root / "analysis/p5_sparse_panel_feasibility/tools/common.py"
    spec = importlib.util.spec_from_file_location("p5_feasibility_authority_common", path)
    demand(spec is not None and spec.loader is not None, "cannot load feasibility authority code")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_exact_file(path: Path, digest: str, label: str) -> None:
    demand(path.is_file(), f"{label} missing")
    demand(sha256_file(path) == digest, f"{label} digest mismatch")


def general_coverage(prime: int, residue: int, pairs: list[dict[str, int]]) -> int:
    modulus = prime * prime
    demand(0 <= residue < modulus, "residue outside prime-square modulus")
    result = 0
    for pair in pairs:
        delta = residue - pair["shift"]
        if delta % prime == 0 and delta % modulus != 0:
            result |= 1 << pair["pair_index"]
    return result


def mask_hex(mask: int) -> str:
    demand(mask >= 0 and mask >> PAIR_COUNT == 0, "mask outside 407-bit domain")
    return mask.to_bytes(MASK_BYTES, "little").hex()


def parse_mask_hex(value: str) -> int:
    demand(isinstance(value, str) and len(value) == 2 * MASK_BYTES, "mask width mismatch")
    raw = bytes.fromhex(value)
    demand(raw[-1] & 0x80 == 0, "mask has bits outside 407-pair domain")
    return int.from_bytes(raw, "little")


def reconstruct_panel(root: Path) -> dict[str, Any]:
    """Rebuild every frozen description without trusting its stored integer."""
    root = root.resolve()
    verify_exact_file(root / DESIGN, DESIGN_SHA256, "Design C manifest")
    verify_exact_file(root / OCCUPIED, OCCUPIED_SHA256, "occupied class authority")
    verify_exact_file(root / REGISTRY, REGISTRY_SHA256, "prior-evaluation registry")
    policy = load_json(root / POLICY)
    demand(policy["expected_initial_head"] == EXPECTED_R, "source policy initial HEAD changed")
    demand(policy["authority"]["description_count"] == 457, "source policy count changed")

    fc = feasibility_module(root)
    protected = fc.verify_hashes(root, fc.PROTECTED_HASHES)
    pairs = fc.load_pairs(root)
    demand(len(pairs) == PAIR_COUNT, "pair domain count changed")
    demand([(p["c"], p["d"]) for p in pairs if p["shift"] == 28] == [(1, 2), (3, 0)], "duplicate shift 28 pair merger")
    bases = {row["base_id"]: row for row in fc.load_bases(root)}
    shortlist_value = fc.load_shortlist(root)
    shortlist = shortlist_value["entries"]
    design = load_json(root / DESIGN)
    demand(design.get("schema") == "a303656-p5-provisional-design-C-v1", "Design C schema changed")
    classes = design.get("classes")
    demand(design.get("family") == "U" and design.get("fresh_class_description_count") == 457, "Design C scope/count changed")
    demand(isinstance(classes, list) and len(classes) == 457, "Design C class list count changed")
    demand(list(design.get("per_entry_counts", {})) == [f"ENTRY-{i:03d}" for i in range(1, 21)], "Design C entry order changed")

    occupied = [json.loads(line) for line in (root / OCCUPIED).read_text(encoding="utf-8").splitlines() if line]
    fresh_u = [row for row in occupied if row.get("family") == "U" and row.get("fresh") is True]
    demand(len(fresh_u) == 457 and sum(row.get("description_count", 0) for row in fresh_u) == 457, "fresh Family-U description count changed")
    demand([row["class_id"] for row in fresh_u] == [row["class_id"] for row in classes], "Design C description order changed")
    demand(not any(row.get("family") in ("R", "Q") for row in fresh_u), "Family R/Q injection")

    stored_registry = load_json(root / REGISTRY)
    rebuilt_registry = fc.build_prior_registry(root)
    demand(canonical_bytes(stored_registry) == canonical_bytes(rebuilt_registry), "prior-evaluation registry reconstruction mismatch")
    demand(stored_registry["completeness"]["status"] == "CERTIFIED COMPLETE", "prior registry not certified complete")

    descriptions: list[dict[str, Any]] = []
    for ordinal, (selected, row) in enumerate(zip(classes, fresh_u)):
        demand(row["family"] == "U" and row["fresh"] is True and row["previously_evaluated"] is False, "non-fresh/non-U description")
        demand(row["description_count"] == 1 and len(row["descriptions"]) == 1, "description multiplicity changed")
        demand(selected == {"class_id": row["class_id"], "class_residue": row["class_residue"], "entry_id": row["entry_id"], "modulus": row["modulus"], "n": row["member"]}, "Design C row differs from occupied authority")
        entry_index = int(row["entry_id"].split("-")[1]) - 1
        demand(0 <= entry_index < 20, "description outside frozen shortlist")
        entry = shortlist[entry_index]
        desc = row["descriptions"][0]
        # Family U deliberately ranges over every residue producing the same
        # frozen maximizing union mask; only Family R uses the shortlist's
        # representative t.  Therefore U's t is reconstructed, not equated to
        # the representative t stored on the shortlist entry.
        demand((row["q"], row["q2"], row["base_id"], desc["resulting_union_mask_digest"]) == (entry["q"], entry["q2"], entry["base_id"], entry["resulting_union_mask_digest"]), "description/shortlist identity mismatch")
        base = bases[row["base_id"]]
        base_mask = fc.mask_int(base["coverage_mask_hex"])
        tuple4 = tuple(desc["fixed_P4_tuple"])
        demand(len(tuple4) == 4, "fixed-P4 tuple width changed")
        reconstructed_base = 0
        for prime, residue in zip(fc.P4, tuple4):
            reconstructed_base |= general_coverage(prime, residue, pairs)
        demand(reconstructed_base == base_mask, "base fixed-P4 tuple/mask mismatch")
        fifth = general_coverage(row["q"], desc["t"], pairs)
        union = base_mask | fifth
        demand(fc.mask_digest(union) == entry["resulting_union_mask_digest"], "resulting union-mask reconstruction mismatch")
        demand(union.bit_count() == entry["G5"] and PAIR_COUNT - union.bit_count() == entry["residual_size"], "G5/residual reconstruction mismatch")
        residue, modulus = fc.build_class(tuple4, row["q"], desc["t"])
        members = fc.class_member(residue, modulus)
        demand((residue, modulus, members) == (row["class_residue"], row["modulus"], [row["member"]]), "CRT/activation-cell reconstruction mismatch")
        n = members[0]
        demand(CELL_LOW <= n <= CELL_HIGH and row["member_count"] == 1, "activation-cell member/boundary error")
        demand(not fc.registry_contains(rebuilt_registry, n), "previously evaluated integer injection")
        descriptions.append({
            "description_ordinal": ordinal,
            "description_id": row["class_id"],
            "entry_id": row["entry_id"],
            "base_id": row["base_id"],
            "base_fixed_P4_residue_tuple": list(tuple4),
            "base_mask_hex": mask_hex(base_mask),
            "base_mask_digest": entry["base_mask_digest"],
            "q": row["q"], "q2": row["q2"], "t": desc["t"],
            "fifth_prime_coverage_mask_hex": mask_hex(fifth),
            "resulting_union_mask_hex": mask_hex(union),
            "resulting_union_mask_digest": entry["resulting_union_mask_digest"],
            "newly_covered_pair_indices": [i for i in range(PAIR_COUNT) if (union & ~base_mask) >> i & 1],
            "remaining_exposed_pair_indices": [i for i in range(PAIR_COUNT) if not (union >> i & 1)],
            "G5": entry["G5"], "residual_size": entry["residual_size"],
            "selection_reason": entry["selection_reason"],
            "complete_CRT_congruences": [
                {"modulus": m, "residue": r} for m, r in zip((*fc.P4_SQUARES, row["q2"], 40), (*tuple4, desc["t"], fc.N0_MOD_40))
            ],
            "class_residue": residue, "modulus": modulus, "activation_cell_member": n,
            "prior_evaluation_excluded": True,
        })

    validate_descriptions(descriptions)
    incidence = deduplicate(descriptions)
    return {
        "schema": "a303656-p5-family-u-frozen-panel-v1",
        "status": "FROZEN PANEL READY FOR EVALUATION",
        "integer_evaluation_performed": False,
        "authority": {
            "design_C_manifest": DESIGN, "design_C_manifest_sha256": DESIGN_SHA256,
            "occupied_manifest_sha256": OCCUPIED_SHA256,
            "prior_evaluation_registry_sha256": REGISTRY_SHA256,
            "prior_evaluation_registry_normalized_digest": stored_registry["normalized_registry_digest"],
            "expected_initial_head": EXPECTED_R,
            "protected_hashes": protected,
        },
        "description_count": 457,
        "distinct_CRT_class_count": len({(d["class_residue"], d["modulus"]) for d in descriptions}),
        "distinct_integer_count": len(incidence),
        "descriptions": descriptions,
        "description_authority_canonical_digest": canonical_digest(descriptions),
        "forbidden_evaluator_scope": policy["forbidden_evaluator_scope"],
    }


def validate_descriptions(rows: list[dict[str, Any]]) -> None:
    demand(len(rows) == 457, "missing or extra description")
    demand([row["description_ordinal"] for row in rows] == list(range(457)), "description reordering")
    demand(len({row["description_id"] for row in rows}) == 457, "description ID duplication")
    demand(all(row["description_id"].startswith("U-") for row in rows), "Family R/Q description injection")
    demand(all(CELL_LOW <= row["activation_cell_member"] <= CELL_HIGH for row in rows), "activation-cell boundary error")
    demand(all(row["prior_evaluation_excluded"] is True for row in rows), "previously evaluated integer injection")
    demand(all(parse_mask_hex(row["resulting_union_mask_hex"]).bit_count() == row["G5"] for row in rows), "union mask corruption")


def deduplicate(descriptions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[str]] = defaultdict(list)
    for row in descriptions:
        grouped[row["activation_cell_member"]].append(row["description_id"])
    result = [{"integer_ordinal": i, "n": n, "description_ids": ids, "description_multiplicity": len(ids)} for i, (n, ids) in enumerate(sorted(grouped.items()))]
    demand(sum(row["description_multiplicity"] for row in result) == 457, "collision incidence deletion")
    demand(len({row["n"] for row in result}) == len(result), "duplicate integer retained for evaluation")
    return result


def rational(value: Fraction) -> dict[str, Any]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": format(value.numerator / value.denominator, ".18f")}


def exact_summary(items: list[tuple[int, int]]) -> dict[str, Any]:
    """items are ordered (n,T), with duplicates allowed for secondary views."""
    demand(items, "cannot summarize an empty sample")
    values = [t for _, t in items]
    hist = Counter(values)
    minimum = min(values)
    ordered_values = sorted(values)
    middle = len(ordered_values) // 2
    med_fraction = Fraction(ordered_values[middle]) if len(ordered_values) % 2 else Fraction(ordered_values[middle - 1] + ordered_values[middle], 2)
    counts = {f"T_le_{threshold}": sum(t <= threshold for t in values) for threshold in THRESHOLDS}
    result = {
        "sample_count": len(values), "histogram": {str(k): hist[k] for k in sorted(hist)},
        "minimum": minimum, "argmins": [n for n, t in items if t == minimum], "maximum": max(values),
        "exact_mean": rational(Fraction(sum(values), len(values))), "median": rational(med_fraction),
        "low_tail_counts": counts,
    }
    result["complete_counts_digest"] = canonical_digest({"histogram": result["histogram"], "low_tail_counts": counts})
    return result


def load_pair_frequency_rows(root: Path) -> list[dict[str, Any]]:
    with (root / PAIR_FREQUENCIES).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    demand(len(rows) == PAIR_COUNT and [int(r["pair_index"]) for r in rows] == list(range(PAIR_COUNT)), "P4 frequency authority malformed")
    return rows
