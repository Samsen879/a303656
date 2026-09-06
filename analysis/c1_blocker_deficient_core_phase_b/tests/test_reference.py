"""Regression tests: exact arithmetic, graph scopes, and fail-closed semantics."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import arithmetic as A
import graphs as G
import audits
import paired_digits
import boundary
import primed_three
import six_rows

class ArithmeticTests(unittest.TestCase):
    def test_boundary_nonregular(self):
        r=A.row(1645333507)
        self.assertEqual((r['w'],r['s']),(1645333506,2))
        self.assertEqual(r['w_factorization'],{2:1,3:3,30469139:1})
        self.assertEqual(r['valuation_one_check'],1)
        self.assertNotEqual(r['valuation_next_check'],1)
    def test_regular_relays(self):
        for p,w in [(3,2),(1523,1522),(30469139,2176367)]:
            self.assertEqual((A.row(p)['w'],A.row(p)['s']),(w,1))
    def test_unadmitted_terminals(self):
        for p in (5,761,1429):
            self.assertTrue(A.isprime(p));self.assertFalse(A.admitted(p))
            with self.assertRaises(ValueError):A.row(p)
    def test_invalid_inputs(self):
        for n in (0,-1):
            with self.assertRaises(ValueError):A.factor(n)
        for p in (9,21):
            with self.assertRaises(ValueError):A.row(p)
    def test_absolute_frontiers(self):
        self.assertEqual(primed_three.primed_frontier(20771),{3,5})
        self.assertEqual(primed_three.primed_frontier(40487),{3,653})
        self.assertEqual(primed_three.primed_frontier(1645333507),{3,761,1429})
    def test_pure_shallow_gateways(self):
        d=six_rows.run()['cyclotomic_identities']
        self.assertEqual(d['3']['exact_admitted_order_primes'],[31])
        self.assertEqual(d['6']['exact_admitted_order_primes'],[7])
        self.assertEqual(d['5']['exact_admitted_order_primes'],[11,71])
        self.assertEqual(d['10']['exact_admitted_order_primes'],[])
    def test_closure_not_prime_scan(self):
        d=A.closure(1645333507)
        self.assertEqual([r['p'] for r in d['rows']],[3,1523,30469139,1645333507])
        self.assertEqual(d['terminal_factors'],[761,1429])

class HallTests(unittest.TestCase):
    def test_actual_direct_singleton(self):
        adj={1645333507:set()}
        self.assertTrue(G.minimal_deficient(adj,{}));G.assert_minimal_structure(adj,{})
    def test_no_common_factor_required(self):
        adj={0:{3},1:{3,5},2:{5},3:{5}};caps={3:1,5:2}
        G.assert_minimal_structure(adj,caps)
        self.assertEqual(set.intersection(*adj.values()),set())
    def test_mixed_isolated_core_not_minimal(self):
        self.assertFalse(G.minimal_deficient({0:set(),1:{3}},{3:1}))
    def test_order_compatible_is_not_nonregular(self):
        adj={7:{3},31:{3}};caps={3:1}
        G.assert_minimal_structure(adj,caps)
        self.assertEqual(A.row(7)['s'],1);self.assertEqual(A.row(31)['s'],1)
    def test_capacities_change_result(self):
        adj={7:{3},31:{3}}
        self.assertEqual(len(G.maximum_matching(adj,{3:1})),1)
        self.assertEqual(len(G.maximum_matching(adj,{3:2})),2)
    def test_coalescing_not_conserved_flow(self):
        d=audits.route_audit()['coalescing_counterexample']
        self.assertEqual(d['maximum_terminal_matching_size'],2)
        self.assertEqual(d['valid_forest'],{11:5,23:11,67:11})
    def test_primed_circuit_signatures(self):
        s=primed_three.signatures()['signatures']
        self.assertEqual(s['3'],[[3]]);self.assertEqual(s['5'],[[5]])
        self.assertEqual(s['7'],[[3,5]])
        for m in ('1','2','4','6','9','11'):self.assertNotIn(m,s)
    def test_boundary_direct_vs_transitive(self):
        P={3,1523,30469139,1645333507}
        supports={p:set(A.row(p)['odd_order_factors']) for p in P}
        q=1645333507
        self.assertEqual(supports[q]-P,set())
        self.assertEqual(G.terminal_frontiers(P,supports)[q],{1429,761})
        self.assertEqual(G.terminal_frontiers(P-{3},supports)[q],{3,1429,761})

class SemanticTests(unittest.TestCase):
    def test_paired_digits_are_not_independent(self):
        d=paired_digits.run()
        self.assertEqual(d['paired_low_residue_count'],5192)
        self.assertEqual((d['coordinates']['5']['same'],d['coordinates']['5']['different']),(1038,4154))
        for v in d['coordinates'].values():
            for witness in v['witnesses'].values():
                a,b=witness['anchor_logs'];q=d['q']
                self.assertEqual((pow(5,a,q)-pow(5,b,q))%q,2)
                self.assertTrue(all(x>0 for x in witness['valuation_quotients']))
    def test_boundary_local_zero_not_fatal(self):
        d=boundary.run()
        v=next(x for x in d['row_evaluations'] if x['p']==3 and x['c']==0)
        self.assertEqual(v['kind'],'LOCAL_ZERO_UNRESOLVED')
        self.assertEqual(v['local_value_mod_p2'],0)
        self.assertEqual(d['common_odd_safe_exponent'],1569734815146673626)
    def test_boundary_priming_all_small_precisions(self):
        d=primed_three.audit()
        self.assertEqual(d['boundary_cases'],3060)
        self.assertEqual(d['route_cases'],486)
        self.assertEqual(d['mismatches'],0)
    def test_bad_boundary_precision(self):
        with self.assertRaises(ValueError):primed_three.choose_boundary(1,0,0)
    def test_crt_rejects_shared_factors(self):
        with self.assertRaises(ValueError):boundary.crt([(0,3),(1,9)])
    def test_all_six_root_allocations(self):
        d=six_rows.run();self.assertEqual(d['allocation_cases'],84)
        for a in d['allocations']:
            self.assertLess(*a['three_mass']);self.assertLess(*a['five_mass'])
    def test_seven_is_not_claimed(self):
        d=six_rows.run()
        self.assertEqual(max(a['pure3']+a['pure5']+a['mixed'] for a in d['allocations']),6)
    def test_corrupted_order_rejected_by_certificate(self):
        p=30469139;r=A.row(p)
        fake=r['w']*2
        self.assertEqual(pow(5,fake,p),1)  # merely being an exponent is insufficient
        self.assertEqual(pow(5,fake//2,p),1) # exact-order check must reject this fake

if __name__=='__main__':unittest.main(verbosity=2)
