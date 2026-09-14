#!/usr/bin/env python3
"""Replay the empty certified ledger and OPEN mass result; never run searches."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
EXPECTED = "647310534648447373054716179652933499827507406084233396665155828948791617392664703265092784874951801626592881977085113283203001"
TARGET_HASH = "2754f9618901c35bbf9c9ba15f9f29c7c7f3c72facff3a1aab13ab03f97c36f2"
def require(ok, message):
    if not ok:
        raise ValueError(message)
def main():
    raw = (ROOT / "C279.txt").read_bytes()
    require(raw == (EXPECTED + "\n").encode(), "target bytes")
    require(hashlib.sha256(raw).hexdigest() == TARGET_HASH, "target SHA256")
    C = int(EXPECTED)
    num = (5**279-1)*(5**3-1)
    den = (5**93-1)*(5**9-1)
    reconstructed, remainder = divmod(num, den)
    require(remainder == 0 and reconstructed == C, "independent formula")
    require(len(str(C)) == 126 and C.bit_length() == 418, "target dimensions")
    require(pow(2, C-1, C) != 1, "compositeness witness")
    data = json.loads((ROOT / "factors_279.json").read_text())
    require(data["target"]["value"] == EXPECTED, "ledger target")
    require(data["certified_factors"] == [], "nonempty ledger requires actual prime proof support")
    require(data["qualifying_distinct_square_hits"] == [], "unsupported square hit")
    R = int(data["remaining_cofactor"])
    require(R == C, "exact cofactor identity")
    require(data["remaining_cofactor_digits"] == len(str(R)), "R digits")
    require(data["remaining_cofactor_bits"] == R.bit_length(), "R bits")
    B = 970453984500000
    require(int(data["external_bound"]["B"]) == B, "external bound value")
    # External exhaustive-search truth is an explicitly pinned merged dependency.
    threshold = (B+1)**6
    mass = data["mass_bound"]
    require(mass["k"] == 0 and mass["remaining_hits_required"] == 3, "mass count")
    require(mass["exponent"] == 6 and int(mass["threshold"]) == threshold, "mass threshold")
    require(R >= threshold and mass["R_less_than_threshold"] is False, "mass comparison")
    require(mass["status"] == "NOT ENOUGH" and data["outcome"] == "OPEN", "unsupported outcome")
    require(data["search"]["search_wall_seconds"] is None, "invented runtime")
    print(json.dumps({"arithmetic_replay":"PASS","outcome":"OPEN","certified_hits":0,
                      "cofactor_mass_gate":"NOT ENOUGH","composite_base_2_residue":str(pow(2,C-1,C)),
                      "search_completion":"NOT_ESTABLISHED"}, indent=2))
if __name__ == "__main__":
    main()
