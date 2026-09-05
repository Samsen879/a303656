"""Scope and fail-closed regressions for the independent reference laboratory."""
from pathlib import Path
import sys, unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from contraction import (Clause, antichain, contract_geometry, contract_provenance,
                         multiply, ONE, ZERO, symbolic_roots, evaluate_polynomial)
from direct_check import direct_minimal_covers, direct_csp
from residue_states import direct_mask, power_cycle, trie_quotient
from run_small_models import cyclic_states
from itertools import product

class ReferenceTests(unittest.TestCase):
    def test_three_row_divergent_roots(self):
        rows=[((1,3),(2,3)),((2,1),(1,1)),((2,2),(1,2))]
        for c in (0,1):
            shapes=[row[c] for row in rows]
            a=contract_provenance((2,2),shapes,True)
            self.assertTrue(a['covered'])
            self.assertTrue(contract_geometry((2,2),shapes))
            self.assertEqual(a['minimal_supports'],frozenset([frozenset(range(3))]))
            self.assertEqual(a['minimal_supports'],direct_minimal_covers((2,2),shapes))

    def test_incompatible_state_tokens_fail_closed(self):
        a=frozenset([frozenset([(0,0)])]); b=frozenset([frozenset([(0,1)])])
        self.assertEqual(multiply(a,b),ZERO)
        self.assertEqual(multiply(a,a),a)
        self.assertEqual(multiply(a,ONE),a)

    def test_distinct_resources_do_not_conflict(self):
        a=frozenset([frozenset([(0,1)])]); b=frozenset([frozenset([(1,0)])])
        self.assertEqual(multiply(a,b),frozenset([frozenset([(0,1),(1,0)])]))

    def test_exact_state_coupling_not_marginal_union(self):
        exact=cyclic_states(3,(1,1,2),2)
        relaxed=cyclic_states(3,(1,1,2),2,True)
        self.assertFalse(symbolic_roots((2,3),exact)['joint'])
        self.assertEqual(len(direct_csp(relaxed,6)['solutions']),12)

    def test_branch_local_reuse_is_not_consumption(self):
        # Top shell row is used in two alternative lower branches.
        shapes=[(3,1),(1,2),(2,2)]
        result=contract_provenance((2,2),shapes,True)
        self.assertTrue(result['covered'])
        self.assertEqual(result['minimal_supports'],frozenset([frozenset([0,1,2])]))

    def test_original_zero_is_never_accepted(self):
        p,k,r=3,2,2
        pw=power_cycle(p,k)
        mask=direct_mask(p,k,frozenset([1]),pw,r)
        self.assertFalse(mask&1) # r-1-5^0 ==0 mod9 at anchor0
        states,_=trie_quotient(p,k,frozenset([1]),pw)
        state=next(s for s in states if s.representative==r)
        self.assertFalse(state.mask&1)

    def test_invalid_valuation_sets_rejected(self):
        for accepted in [frozenset(),frozenset([0]),frozenset([2]),frozenset([3])]:
            with self.assertRaises(ValueError):
                trie_quotient(3,3,accepted,power_cycle(3,3))

    def test_symbolic_truth_table_all_rows_assignments(self):
        states=[[(1,2),(2,1)],[(2,1),(1,2)]]
        out=symbolic_roots((2,),states)
        expected=direct_csp(states,2)['solutions']
        for assignment in product(range(2),repeat=2):
            self.assertEqual(evaluate_polynomial(out['joint'],assignment),assignment in expected)

    def test_deeper_accepted_odd_shell(self):
        from collections import Counter
        p,k=3,4; pw=power_cycle(p,k)
        for accepted in [frozenset([3]),frozenset([1,3])]:
            states,stats=trie_quotient(p,k,accepted,pw)
            direct=Counter(direct_mask(p,k,accepted,pw,r) for r in range(p**k))
            self.assertEqual(direct,{s.mask:s.residue_count for s in states})
            self.assertLessEqual(stats['emitted_buckets'],1+k*stats['distinct_centers'])

if __name__=='__main__': unittest.main(verbosity=2)
