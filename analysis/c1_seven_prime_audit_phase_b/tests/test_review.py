"""Named regressions for the separately implemented review laboratory."""
from pathlib import Path
import sys,json,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import audit_independent as a
import verify_scan as s
class ReviewTests(unittest.TestCase):
    def test_01_scan_full_inventory(self):
        z=json.loads((a.ROOT/'results/scan_summary.json').read_text())
        self.assertEqual(z['candidate_count'],49112626)
        self.assertEqual(z['hits'],[20771,40487,1645333507])
    def test_02_scan_all_blocks(self):
        x=[json.loads(t) for t in (a.ROOT/'results/scan_a.jsonl').read_text().splitlines()]
        y=[json.loads(t) for t in (a.ROOT/'results/scan_b.jsonl').read_text().splitlines()]
        self.assertEqual(x,y);self.assertEqual(len(x),201)
        self.assertEqual(x[0]['lo'],0);self.assertEqual(x[-1]['hi'],2000000000)
        self.assertTrue(all(u['hi']+1==v['lo'] for u,v in zip(x,x[1:])))
    def test_03_hit_exact_orders(self):
        for q,w in [(20771,10385),(40487,40486),(1645333507,1645333506)]:
            z=s.certify(q);self.assertEqual(z['order'],w);self.assertEqual(z['s'],2)
    def test_04_nonadmitted_prime_not_resource(self):
        self.assertFalse(s.certify(53471161)['admitted'])
    def test_05_complete_helper_inventories(self):
        z=a.arithmetic();self.assertEqual(z['rank3_heads'],{'1':[7,31],'2':[19,5167]})
        self.assertEqual(z['rank5_3free_depth1_heads'],[11,71])
    def test_06_boundary_same_anchor(self):
        self.assertEqual(a.boundary(8)['mismatches'],0)
    def test_07_dynamic_center_excluded(self):
        self.assertFalse(a.dmask(3,3,0,(0,2))&1)
    def test_08_simple_pair_full(self):
        for p in [3,5,7]:
            self.assertEqual(a.dmask(p,2,0,(0,))|a.cmask(p,2,1,0),(1<<(p*p))-1)
    def test_09_parity_essential_negative_control(self):
        self.assertEqual(a.dmask(3,2,0,(0,1))|a.cmask(3,2,2,0),(1<<9)-1)
        self.assertNotEqual(a.dmask(3,2,0,(0,))|a.cmask(3,2,2,0),(1<<9)-1)
    def test_10_three_shallow_head_union(self):
        z=a.shallow_three();self.assertEqual(z['max_union'],'8/9');self.assertEqual(z['min_leaves_at_depth3'],7)
    def test_11_five_all_witnesses(self):
        z=a.five_witnesses();self.assertEqual([t['max_minimal_witnesses'] for t in z['cases']],[1,2])
    def test_12_guard_intersection_never_forgets(self):
        self.assertEqual(a.join({3:(1,1)},{3:(2,4)}),{3:(2,4)})
        self.assertIsNone(a.join({3:(1,1)},{3:(2,2)}))
    def test_13_sparse_exact_elimination(self):
        self.assertEqual(a.abstract_linear()['mismatches'],0)
    def test_14_row_normal_form_and_forall(self):
        self.assertEqual(a.row_normal_forms()['mismatches'],0)
    def test_15_pair_arithmetic_overflow_bound(self):
        q=2_000_000_000
        self.assertLess(2*q*q-3*q,1<<64)
        self.assertLess(q*q,1<<64)
if __name__=='__main__':unittest.main()
