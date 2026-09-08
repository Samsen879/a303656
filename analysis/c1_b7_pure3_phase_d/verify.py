#!/usr/bin/env python3
"""B7 Phase D sealed arithmetic verifier. Python standard library only.
Usage: python verify.py [--self-test] [--output result.json]
No network, repository imports, discoveries, or GitHub writes.
Primality is proved with recursive complete-(n-1) Lucas certificates.
"""
import argparse
import copy
from functools import lru_cache
import json
import math
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def prime_factors(n):
    require(isinstance(n, int) and n >= 1, "positive integer required")
    ans = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            ans.append(p)
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        ans.append(n)
    return ans

def divisors(n):
    low, high = [], []
    for d in range(1, math.isqrt(n)+1):
        if n % d == 0:
            low.append(d)
            if d*d != n:
                high.append(n//d)
    return low + high[::-1]

@lru_cache(None)
def phi5(n):
    require(n >= 1, "bad cyclotomic index")
    denominator = math.prod(phi5(d) for d in divisors(n) if d < n)
    value, remainder = divmod(5**n - 1, denominator)
    require(remainder == 0, "cyclotomic division was not exact")
    return value

def phi5_mobius(n):
    """Second value construction via squarefree-divisor inclusion-exclusion."""
    ps = prime_factors(n)
    numerator, denominator = 1, 1
    for mask in range(1 << len(ps)):
        d = math.prod(p for i,p in enumerate(ps) if (mask >> i) & 1)
        value = 5**(n//d) - 1
        if mask.bit_count() % 2:
            denominator *= value
        else:
            numerator *= value
    value, remainder = divmod(numerator, denominator)
    require(remainder == 0, "Mobius division was not exact")
    return value

def linear_power(a, exponent, modulus):
    value = 1
    for _ in range(exponent):
        value = value*a % modulus
    return value

def binary_power(a, exponent, modulus):
    value = 1
    while exponent:
        if exponent & 1:
            value = value*a % modulus
        a = a*a % modulus
        exponent >>= 1
    return value

class PrimeChecker:
    def __init__(self, certificates):
        self.certificates = certificates
        self.verified = set()

    def check(self, n):
        n = int(n)
        if n in self.verified:
            return
        require(str(n) in self.certificates, "missing prime certificate")
        rec = self.certificates[str(n)]
        if n == 2:
            require(rec == {"factors": [], "witness": None}, "corrupt base certificate")
            self.verified.add(2)
            return
        require(n > 2 and n % 2, "invalid odd-prime label")
        fs = [(int(p), int(e)) for p,e in rec["factors"]]
        require(len(fs) == len({p for p,e in fs}), "duplicate n-1 factors")
        require(all(2 <= p < n and e >= 1 for p,e in fs), "invalid descent")
        require(math.prod(p**e for p,e in fs) == n-1, "incomplete n-1 product")
        for p,e in fs:
            self.check(p)
        a = rec["witness"]
        require(isinstance(a,int) and 1 < a < n, "invalid Lucas witness")
        require(pow(a,n-1,n) == 1, "Lucas Fermat test failed")
        for p,e in fs:
            require(math.gcd(pow(a,(n-1)//p,n)-1,n) == 1,
                    "Lucas full-order gcd failed")
        self.verified.add(n)

def verify_order(q, w):
    require(q > 2 and w >= 1 and (q-1) % w == 0, "order does not divide q-1")
    require(pow(5,w,q) == 1, "order multiple failed")
    require(all(pow(5,w//p,q) != 1 for p in prime_factors(w)),
            "order not exact")

def find_order_from_multiple(q, multiple):
    w = multiple
    require(pow(5,w,q) == 1, "bad order multiple")
    for p in prime_factors(w):
        while w % p == 0 and pow(5,w//p,q) == 1:
            w //= p
    verify_order(q,w)
    return w

def trial_prime(n):
    if n < 2:
        return False
    return all(n%d for d in range(2,math.isqrt(n)+1))

def regular_skeleton():
    # Actual rows 7 and 43 only. No fictional nonregular root.
    modulus = 6*7*43
    a = next(d for d in range(modulus) if d%6 == 4 and d%7 == 0 and d%43 == 0)
    rows = [(7,6),(43,42)]
    residues = {p:(3+pow(5,a,p*p))%(p*p) for p,w in rows}
    holes, branch_count, covered = [], 0, 0
    comparisons = 0
    for d in range(modulus):
        direct_union = False
        for p,w in rows:
            v = (residues[p]-3-pow(5,d,p*p))%(p*p)
            direct = v != 0 and v%p == 0
            symbolic = (d-a)%w == 0 and (d-a)%p != 0
            require(direct == symbolic, "actual regular-row shell mismatch")
            direct_union |= direct
            comparisons += 1
        if d%6 == 4:
            branch_count += 1
            if direct_union:
                covered += 1
            else:
                holes.append(d)
    require(holes == [a] and branch_count == 301 and covered == 300,
            "regular skeleton holes changed")
    return {"rows":[7,43], "full_period":modulus, "anchor":1,
            "branch":"d=4 mod 6", "branch_size":branch_count,
            "covered_in_branch":covered, "holes":holes,
            "residues":residues, "direct_row_comparisons":comparisons,
            "actual_nonregular_root":False, "complete_certificate":False}

def basin_signature(root, orders):
    D, terminals, gateways = set(), set(), set()
    def visit(p):
        if p == 3 or p % 4 == 1:
            terminals.add(p)
            return
        require(p in orders, "missing certified order")
        if p in D:
            return
        D.add(p)
        ps = {x for x in prime_factors(orders[p]) if x != 2}
        require(bool(ps), "empty admitted odd support")
        if ps == {3}:
            gateways.add(p)
        for x in ps:
            require(x < p, "nondecreasing DAG edge")
            visit(x)
    visit(root)
    return D, terminals, gateways

def run(data):
    require(data["schema"] == "a303656.b7.phase_d.v1", "unknown schema")
    checker = PrimeChecker(data["prime_certificates"])
    for q in data["prime_certificates"]:
        checker.check(int(q))
    recs = {(r["n"],int(r["q"])):r for r in data["arithmetic_records"]}
    require(len(recs) == len(data["arithmetic_records"]), "duplicate records")
    by_index = {}
    all_orders = {3:2}
    factor_total = 0
    for entry in data["cyclotomic_factorizations"]:
        n, fs = entry["n"], list(map(int,entry["factors"]))
        require(n not in by_index, "duplicate index")
        require(len(fs) == len(set(fs)), "repeated factor in squarefree claim")
        require(math.prod(fs) == phi5(n) == phi5_mobius(n), "factor product mismatch")
        by_index[n] = []
        for q in fs:
            checker.check(q)
            w = find_order_from_multiple(q,n)
            r = recs[(n,q)]
            require(w == r["order"], "recorded order mismatch")
            mod2 = pow(5,w,q*q)
            require(mod2 == linear_power(5,w,q*q), "modular core disagreement")
            require(mod2 != 1 and mod2 % q == 1, "regularity not proved")
            require(r["s"] == 1 and int(r["residue_mod_q2"]) == mod2,
                    "bad lifting record")
            require(int(r["lifting_coefficient"]) == (mod2-1)//q, "bad coefficient")
            require(r["admitted"] == (q%4 == 3), "admission error")
            require(r["primitive"] == (w == n), "primitive-factor error")
            require(q not in all_orders or all_orders[q] == w, "inconsistent orders")
            all_orders[q] = w
            if q%4 == 3 and w == n:
                by_index[n].append(q)
            factor_total += 1
    require(factor_total == len(recs), "unused arithmetic record")
    gate = sorted({q for n in (7,14,21,42) for q in by_index[n]})
    require(gate == data["first_relay_gate"] == [43,127,379,7603,19531,519499],
            "first relay gate mismatch")
    require(all(trial_prime(p) for p in gate), "independent trial primality failed")
    for p in gate:
        D,T,G = basin_signature(p,all_orders)
        require(D == {7,p} and T == {3} and G == {7}, "relay closure mismatch")
    indices = sorted({r*m for r in gate for m in (1,2,3,6,7,14,21,42)})
    require(indices == data["three_vertex_orders"] and len(indices)==48, "48-index gate")
    removed = set(data["certified_excluded_three_vertex_orders"])
    require(removed == {43,86,127,129,258} and removed <= set(by_index), "bad exclusions")
    require(sorted(set(indices)-removed) == data["three_vertex_remaining_orders"],
            "bad survivor list")
    r43 = sorted({43*m for m in (1,2,3,6,7,14,21,42)}-removed)
    require(r43 == data["r43_remaining_orders"] == [301,602,903,1806], "r43 gate")
    P = int(data["regular_P89"])
    require(P == (5**127-1)//4 and len(str(P)) == 89, "P89 identity")
    D,T,G = basin_signature(P,all_orders)
    require(D == {P,127,7} and T == {3} and G == {7}, "P89 DAG")
    require(pow(5,127,P*P) == 1+4*P, "P89 regularity")
    # Sealed partial divisor probe of one cyclotomic index, not all primes.
    probe = data["prime_order_19531_probe"]
    zeros, count = [], 0
    for m in range(probe["m_min"],probe["m_max"]+1):
        if m%10 not in probe["m_mod_10"]:
            continue
        q = 1+2*m*19531
        v = pow(5,19531,q)
        require(v == binary_power(5,19531,q), "probe modular disagreement")
        count += 1
        if v == 1:
            zeros.append([m,q])
    require(count == probe["tested_candidates"] == 2000 and zeros == [], "probe changed")
    return {
        "status":"PASS",
        "recursive_Lucas_prime_certificates":len(checker.verified),
        "complete_cyclotomic_products":len(by_index),
        "factor_order_lifting_records":factor_total,
        "first_relay_gate":gate,
        "three_vertex_initial_indices":len(indices),
        "three_vertex_excluded_indices":sorted(removed),
        "three_vertex_remaining_indices":len(set(indices)-removed),
        "r43_remaining_indices":r43,
        "regular_skeleton":regular_skeleton(),
        "P89_regular":True,
        "prime_order_19531_partial_probe_candidates":count,
        "B7_member_found":False,
        "B7_empty_proved":False,
        "total_lower_bound_raised_to_eight":False,
        "GitHub_writes":"NONE"
    }

class Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((HERE/"arithmetic_certificates.json").read_text())
    def test_full_replay(self):
        self.assertEqual(run(self.data)["status"],"PASS")
    def test_corrupt_witness(self):
        c = copy.deepcopy(self.data["prime_certificates"]); c["43"]["witness"]=1
        with self.assertRaises(ValueError): PrimeChecker(c).check(43)
    def test_corrupt_n_minus_one(self):
        c = copy.deepcopy(self.data["prime_certificates"]); c["43"]["factors"][0][1]+=1
        with self.assertRaises(ValueError): PrimeChecker(c).check(43)
    def test_missing_certificate(self):
        c = copy.deepcopy(self.data["prime_certificates"]); del c["7"]
        with self.assertRaises(ValueError): PrimeChecker(c).check(43)
    def test_bad_base(self):
        c = copy.deepcopy(self.data["prime_certificates"]); c["2"]["witness"]=1
        with self.assertRaises(ValueError): PrimeChecker(c).check(43)
    def test_imprimitive_seven(self):
        with self.assertRaises(ValueError): verify_order(7,42)
        verify_order(7,6)
    def test_order_multiple_not_exact(self):
        with self.assertRaises(ValueError): verify_order(43,84)
    def test_wrong_factor_product(self):
        d=copy.deepcopy(self.data); d["cyclotomic_factorizations"][0]["factors"][0]="43"
        with self.assertRaises(ValueError): run(d)
    def test_regular_is_not_nonregular(self):
        p=int(self.data["regular_P89"])
        self.assertNotEqual(pow(5,127,p*p),1)
    def test_gateway_is_not_direct_edge(self):
        D,T,G=basin_signature(43,{7:6,43:42})
        direct_into_3={p for p in D if 3 in prime_factors({7:6,43:42}[p])}
        self.assertEqual(G,{7}); self.assertEqual(direct_into_3,{7,43})
    def test_no_squarefree_q_minus_one_requirement(self):
        self.assertEqual(519498%(7*7),0)
        self.assertEqual(len(prime_factors(21)),2)
        verify_order(519499,21)
    def test_regular_skeleton_retains_hole(self):
        self.assertEqual(regular_skeleton()["holes"],[1204])
    def test_foreign_terminal(self):
        D,T,G=basin_signature(11,{11:5})
        self.assertEqual(T,{5})
    def test_basin_not_prime_order_chain(self):
        self.assertEqual(basin_signature(127,{127:42,7:6})[2],{7})
        self.assertNotEqual(42,7)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
        if not result.wasSuccessful():
            raise SystemExit(1)
    data=json.loads((HERE/"arithmetic_certificates.json").read_text(encoding="utf-8"))
    result=run(data)
    text=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(text,encoding="utf-8")
    print(text,end="")

if __name__=="__main__":
    main()
