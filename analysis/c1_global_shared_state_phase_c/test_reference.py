import unittest
from fractions import Fraction
import reference as r

class ExactPhaseCTests(unittest.TestCase):
    def test_six_demands_distinct(self):
        self.assertEqual(len(set(r.DEMANDS.values())),6)
    def test_split_is_not_both(self):
        out=r.six_demands();self.assertEqual(out['truth_comparisons'],8160)
        self.assertNotEqual(out['split_residual_tables']['EITHER'],out['split_residual_tables']['BOTH'])
    def test_local_zero_not_fatal(self):
        a,b=r.k2_mask(3,2,6)
        self.assertFalse(a&1);self.assertFalse(b&1)
    def test_period_must_support_row(self):
        with self.assertRaises(AssertionError):r.k2_mask(7,2,6)
    def test_actual_non_TU(self):
        masks=[r.k2_mask(3,x,6) for x in (2,5,8)]
        mat=[[int(((a|b)>>d)&1) for a,b in masks] for d in (0,2,4)]
        self.assertEqual(r.determinant_bareiss(mat),-2)
    def test_actual_three_way_collision(self):
        self.assertEqual(r.sphere_checks()['triple_legal_residues'],[])
    def test_max_radius_mixed_valuations(self):
        for cs in (((0,2),(3,1)),((0,2),(9,2)),((0,2),(9,2),(18,2)),((0,2),(1,1))):
            self.assertEqual(r.sphere_solutions(3,3,cs),r.sphere_formula(3,3,cs))
    def test_real_support_orders(self):
        self.assertEqual(r.order(43),42);self.assertEqual(r.order(1303),62)
        self.assertEqual(r.signature(43)['s'],1);self.assertEqual(r.signature(1303)['s'],1)
    def test_nonregular_rows(self):
        self.assertEqual(r.signature(20771)['s'],2);self.assertEqual(r.signature(40487)['s'],2)
    def test_named_pair_collision(self):
        q=20771
        for a,b,rr in ((2177,9772,16),(1558,10238,17555)):
            self.assertEqual(r.valuation(rr-1-pow(5,a,q*q),q,2),1)
            self.assertEqual(r.valuation(rr-3-pow(5,b,q*q),q,2),1)
        self.assertNotEqual(2177%155,1558%155)
    def test_exact_resultant(self):
        self.assertEqual(r.resultant(3,0),-728)
        self.assertEqual(r.resultant(5,0),-54134432)
    def test_gcd_is_not_state_conjunction(self):
        q=20771
        for Y,a in ((7,2177),(8,1558)):
            x=pow(5,a,q)
            self.assertEqual(pow(x,67,q),pow(5,Y*67,q))
            self.assertEqual(pow(x-2,67,q),pow(5,Y*67,q))
        self.assertNotEqual((8-7)%155,0)
    def test_fractional_capacity_exact(self):
        self.assertEqual(Fraction(2,3)+Fraction(2,7)+Fraction(10,31),Fraction(830,651))

if __name__=='__main__':unittest.main()
