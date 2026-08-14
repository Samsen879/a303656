#!/usr/bin/env python3
"""Authenticated inputs and exact shared contracts for the fifth-prime landscape."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import struct
import zipfile
from pathlib import Path
from typing import Any

START_COMMIT = "02028314ab92d7aa089475f9a6bc96688526f731"
B_ORDER = 5000
P4 = (3, 7, 11, 23)
PAIR_COUNT = 407
MASK_BYTES = 51
L4 = 1_129_118_760
CELL_LOW = 183_968_950_234
CELL_HIGH = 246_731_069_451
CELL_WIDTH = CELL_HIGH - CELL_LOW + 1

AUTHORITY_PATH = "baseline/a303656_p2cover_bundle.zip"
AUTHORITY_MEMBER = "a303656_p2cover/output/primes_B5000_verified.csv"
AUTHORITY_ARCHIVE_SHA256 = "4dadb8ce07cd0ccf56575ef0882d6bb02284a02c61e05cd1424e070d83b22ff3"
AUTHORITY_MEMBER_SHA256 = "88dbfb4122964eab002f1e94433b4376ab93c1940b0535da8c0036e1ab40a68b"
PAIR_ORDER_PATH = "analysis/k4_survivor_incidence/pair_order.csv"
PAIR_ORDER_SHA256 = "5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b"
PAIR_DOMAIN_DIGEST = "cea7cb028f9e9cc05e120b693924e6860e4f6821e23e42366f1122921e36cf39"
BASE_MANIFEST_PATH = "analysis/p4_weighted_transferability/results/candidate_manifest_holdout_v2.json"
BASE_MANIFEST_SHA256 = "728fd5195d91c75b2b93ae02e4ad43aea07afb6fd6a511c54596d0658bc6e1ca"
WEIGHTED_MAXIMA_PATH = "analysis/p4_weighted_transferability/results/weighted_maxima.json"
PAIR_FREQUENCIES_PATH = "analysis/p4_maximizer_census/pair_frequencies.csv"
COMMON_UNCOVERED_PATH = "analysis/p4_maximizer_census/common_uncovered.json"

PROTECTED_HASHES = {
    "README.md": "9c1f11b8ba76e0d0ff70d3d0dc5f8b1b528e1e31405b27be9b047bdcc3916a8b",
    "REPORT_zh.md": "833e66fd88c27412e2522448f17075baf4e85828080c22ca2e87a12f30f77649",
    "output/formal_results_audit.json": "fe87b53734fe9f8978396428769af5db76fb35709276241f36c49c2a9145b533",
    "output/final_packaging_audit.json": "de8f4d351b809b03daac280879eddc69a795fce50f9c8f6b2d786ad2f9d611ca",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt": "510ac25107f8764fbacb3fe10f2c67de1a5cc595b20a23f793ff77dd54d5ec42",
    AUTHORITY_PATH: AUTHORITY_ARCHIVE_SHA256,
    PAIR_ORDER_PATH: PAIR_ORDER_SHA256,
    BASE_MANIFEST_PATH: BASE_MANIFEST_SHA256,
}


class ContractError(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    temporary.replace(path)


def mask_hex(mask: int) -> str:
    demand(mask >= 0 and mask >> PAIR_COUNT == 0, "mask outside 407-pair domain")
    return mask.to_bytes(MASK_BYTES, "little").hex()


def mask_int(value: str) -> int:
    demand(isinstance(value, str) and len(value) == 2 * MASK_BYTES, "mask must be 51 bytes")
    raw = bytes.fromhex(value)
    demand(raw[-1] & 0x80 == 0, "mask has an out-of-domain bit")
    return int.from_bytes(raw, "little")


def verify_protected(root: Path) -> dict[str, str]:
    observed = {}
    for relative, expected in PROTECTED_HASHES.items():
        path = root / relative
        demand(path.is_file(), f"protected file missing: {relative}")
        actual = sha256_file(path)
        demand(actual == expected, f"protected hash mismatch: {relative}")
        observed[relative] = actual
    return observed


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    factor = 3
    while factor <= math.isqrt(n):
        if n % factor == 0:
            return False
        factor += 2
    return True


def load_prime_authority(root: Path) -> tuple[list[int], list[int], dict[str, Any]]:
    archive = root / AUTHORITY_PATH
    demand(sha256_file(archive) == AUTHORITY_ARCHIVE_SHA256, "prime-authority archive mutation")
    with zipfile.ZipFile(archive) as bundle:
        embedded = bundle.read("a303656_p2cover/SHA256SUMS").decode()
        expected_line = f"{AUTHORITY_MEMBER_SHA256}  ./output/primes_B5000_verified.csv"
        demand(expected_line in embedded.splitlines(), "prime-authority member is not authenticated by embedded hashes")
        payload = bundle.read(AUTHORITY_MEMBER)
    demand(sha256_bytes(payload) == AUTHORITY_MEMBER_SHA256, "prime-authority member mutation")
    rows = list(csv.DictReader(io.StringIO(payload.decode())))
    demand(len(rows) == 527, "eligible authority count changed")
    primes = [int(row["p"]) for row in rows]
    demand(len(primes) == len(set(primes)), "duplicate eligible prime")
    demand(all(is_prime(q) and q % 4 == 3 and q % 3 and q % 5 for q in primes), "eligible authority condition corruption")
    demand(all(max(int(row["ord_p_3"]), int(row["ord_p_5"])) <= B_ORDER for row in rows), "unauthorized B expansion")
    excluded = [q for q in primes if q in P4]
    candidates = [q for q in primes if q not in P4]
    demand(all(q % 4 == 3 and 15 % q != 0 and q not in P4 for q in candidates), "fifth-prime condition corruption")
    ordered_payload = "".join(f"{q}\n" for q in candidates).encode()
    report = {
        "authority_path": AUTHORITY_PATH,
        "authority_member": AUTHORITY_MEMBER,
        "authority_archive_sha256": AUTHORITY_ARCHIVE_SHA256,
        "authority_sha256": AUTHORITY_MEMBER_SHA256,
        "B": B_ORDER,
        "eligible_count": len(primes),
        "prime_3_in_authority": 3 in primes,
        "excluded_intersection": excluded,
        "final_fifth_prime_candidate_count": len(candidates),
        "ordered_candidate_list_digest": sha256_bytes(ordered_payload),
        "candidate_definition": "q prime; q == 3 mod 4; q does not divide 15; q not in {3,7,11,23}",
    }
    demand(report["ordered_candidate_list_digest"] == "12a9986fdc0720a878f1e1826daf6a0d5895564747139dd4398320fdddaeee47", "candidate-list digest changed")
    return primes, candidates, report


def load_pairs(root: Path) -> list[dict[str, int]]:
    path = root / PAIR_ORDER_PATH
    demand(sha256_file(path) == PAIR_ORDER_SHA256, "pair-order authority mutation")
    with path.open(newline="", encoding="utf-8") as stream:
        rows = [{"pair_index": int(r["pair_index"]), "c": int(r["c"]), "d": int(r["d"]), "shift": int(r["shift"])} for r in csv.DictReader(stream)]
    demand(len(rows) == PAIR_COUNT and [r["pair_index"] for r in rows] == list(range(PAIR_COUNT)), "pair-domain mutation")
    digest = hashlib.sha256()
    for row in rows:
        digest.update(struct.pack("<HH", row["c"], row["d"]))
        demand(row["shift"] == 3 ** row["c"] + 5 ** row["d"], "inexact shift")
    demand(digest.hexdigest() == PAIR_DOMAIN_DIGEST, "pair-domain digest mismatch")
    duplicate = [(r["c"], r["d"]) for r in rows if r["shift"] == 28]
    demand(duplicate == [(1, 2), (3, 0)], "duplicate shift pair merger")
    return rows


def load_bases(root: Path) -> list[dict[str, Any]]:
    path = root / BASE_MANIFEST_PATH
    demand(sha256_file(path) == BASE_MANIFEST_SHA256, "base-mask mutation")
    with path.open(encoding="utf-8") as stream:
        manifest = json.load(stream)
    with (root / WEIGHTED_MAXIMA_PATH).open(encoding="utf-8") as stream:
        maxima = json.load(stream)
    candidates = manifest.get("candidates")
    demand(manifest.get("candidate_count") == 13 and manifest.get("distinct_coverage_mask_count") == 13 and len(candidates) == 13, "not exactly 13 frozen masks")
    pooled = maxima["maxima"]["full"]["pool"]["coverage_mask_hex"]
    t3 = maxima["maxima"]["t3eq2"]["pool"]["coverage_mask_hex"]
    normalized = []
    for index, item in enumerate(candidates):
        value = mask_int(item["coverage_mask_hex"])
        demand(value.bit_count() == item["G"], "base G mismatch")
        labels = list(item["selected_by"])
        roles = list(labels)
        if item["coverage_mask_hex"] == pooled:
            roles.append("POOLED-GLOBAL-WEIGHTED-OPT")
        if item["coverage_mask_hex"] == t3:
            roles.append("T3EQ2-CONSTRAINED-WEIGHTED-OPT")
        normalized.append({
            "base_index": index,
            "base_id": f"BASE-{index + 1:02d}",
            "G": item["G"],
            "coverage_mask_hex": item["coverage_mask_hex"],
            "base_mask_digest": sha256_bytes(bytes.fromhex(item["coverage_mask_hex"])),
            "roles": roles,
            "representative": item.get("lexicographically_first_t3eq2_representative"),
        })
    demand(len({b["coverage_mask_hex"] for b in normalized}) == 13, "duplicate frozen base mask")
    required = {"G231-COMMON", "POOLED-GLOBAL-WEIGHTED-OPT", "T3EQ2-CONSTRAINED-WEIGHTED-OPT", "CAL-216", "CAL-227", "CAL-230"}
    demand(required <= {r for b in normalized for r in b["roles"]}, "required base roles missing")
    return normalized


def indices(mask: int) -> list[int]:
    return [i for i in range(PAIR_COUNT) if mask >> i & 1]


def coverage_at(q: int, t: int, pairs: list[dict[str, int]]) -> int:
    q2 = q * q
    result = 0
    for row in pairs:
        difference = t - row["shift"]
        if difference % q == 0 and difference % q2 != 0:
            result |= 1 << row["pair_index"]
    return result
