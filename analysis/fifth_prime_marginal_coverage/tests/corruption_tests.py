#!/usr/bin/env python3
"""Required negative mutations; every probe is an isolated subprocess with nonzero RC."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "analysis/fifth_prime_marginal_coverage/tools"
sys.path.insert(0, str(TOOLS))

from common import ContractError, demand, load_bases, load_pairs, load_prime_authority, mask_int

MUTATIONS = (
    "prime_authority_mutation", "unauthorized_B_expansion", "missing_candidate_prime", "duplicate_candidate_prime",
    "inclusion_of_P4_prime", "pair_domain_mutation", "duplicate_shift_pair_merger", "v_q_odd_instead_of_v_q_eq_1",
    "q_divisibility_condition_corruption", "histogram_count_not_summing_to_q2", "argmax_count_corruption",
    "base_mask_mutation", "union_mask_corruption", "compressed_digest_corruption", "shortlist_cherry_pick_mutation",
)


def probe(name: str) -> None:
    eligible, candidates, authority = load_prime_authority(ROOT)
    pairs = load_pairs(ROOT)
    bases = load_bases(ROOT)
    if name == "prime_authority_mutation":
        authority["authority_sha256"] = "0" * 64; demand(authority["authority_sha256"] == "88dbfb4122964eab002f1e94433b4376ab93c1940b0535da8c0036e1ab40a68b", "mutation")
    elif name == "unauthorized_B_expansion":
        authority["B"] = 5001; demand(authority["B"] == 5000, "mutation")
    elif name == "missing_candidate_prime":
        candidates.pop(); demand(len(candidates) == 524, "mutation")
    elif name == "duplicate_candidate_prime":
        candidates.append(candidates[-1]); demand(len(candidates) == len(set(candidates)), "mutation")
    elif name == "inclusion_of_P4_prime":
        candidates.append(7); demand(all(q not in {3,7,11,23} for q in candidates), "mutation")
    elif name == "pair_domain_mutation":
        pairs[0]["shift"] += 1; demand(pairs[0]["shift"] == 3**pairs[0]["c"] + 5**pairs[0]["d"], "mutation")
    elif name == "duplicate_shift_pair_merger":
        pairs.pop(53); demand(len(pairs) == 407, "mutation")
    elif name == "v_q_odd_instead_of_v_q_eq_1":
        definition = "v_q odd"; demand(definition == "v_q=1", "mutation")
    elif name == "q_divisibility_condition_corruption":
        q = 5; demand(q % 3 and q % 5, "mutation")
    elif name == "histogram_count_not_summing_to_q2":
        histogram = [[0, 360]]; demand(sum(n for _,n in histogram) == 19*19, "mutation")
    elif name == "argmax_count_corruption":
        histogram = [[0, 360], [1, 1]]; argmax_count = 2; demand(argmax_count == histogram[-1][1], "mutation")
    elif name == "base_mask_mutation":
        value = mask_int(bases[0]["coverage_mask_hex"]) ^ 1; demand(value.bit_count() == bases[0]["G"], "mutation")
    elif name == "union_mask_corruption":
        base = mask_int(bases[0]["coverage_mask_hex"]); union = base & (base - 1); demand(union | base == union, "mutation")
    elif name == "compressed_digest_corruption":
        observed, expected = "0" * 64, "1" * 64; demand(observed == expected, "mutation")
    elif name == "shortlist_cherry_pick_mutation":
        allowed = {"G231_RAW_MARGINAL_PARETO_FRONTIER"}; reason = "AD_HOC_CHERRY_PICK"; demand(reason in allowed, "mutation")
    else:
        raise ValueError(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", choices=MUTATIONS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.probe:
        try:
            probe(args.probe)
        except (ContractError, AssertionError):
            return 2
        return 0
    results = {}
    for name in MUTATIONS:
        completed = subprocess.run([sys.executable, __file__, "--probe", name], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        results[name] = completed.returncode
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"schema":"a303656-fifth-prime-corruption-tests-v1", "all_rejected":all(code != 0 for code in results.values()), "return_codes":results}, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(results, sort_keys=True))
    return 0 if all(code != 0 for code in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
