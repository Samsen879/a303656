import copy
import json
import unittest
from pathlib import Path
from fractions import Fraction
import reference as r

DATA=json.loads((Path(__file__).parent/'arithmetic_inputs.json').read_text())

class ReferenceTests(unittest.TestCase):
    def test_recursive_lucas_certificates(self):
        a=r.Arithmetic(DATA)
        for n in DATA['primality_certificates']:
            a.prime(int(n))
        self.assertEqual(len(a.proven),93)

    def test_bad_generator_rejected(self):
        data=copy.deepcopy(DATA)
        data['primality_certificates']['4861']['base']=1
        with self.assertRaises(ValueError):r.Arithmetic(data).prime(4861)

    def test_incomplete_factorization_rejected(self):
        data=copy.deepcopy(DATA)
        data['primality_certificates']['31']['n_minus_1_factors'].pop('5')
        with self.assertRaises(ValueError):r.Arithmetic(data).prime(31)

    def test_twenty_cyclotomic_products(self):
        rows=r.Arithmetic(DATA).cyclotomics()
        self.assertEqual(len(rows),20)
        self.assertTrue(all(x['squarefree'] for x in rows))
        for row in rows:
            if row['n'] in (15,30):
                self.assertTrue(all(not x['admitted'] for x in row['factors']))

    def test_mixed_depth_two_gateways(self):
        rows=r.Arithmetic(DATA).cyclotomics()
        qs=[int(f['q']) for x in rows if x['n'] in (45,90)
            for f in x['factors'] if f['admitted'] and f['primitive_at_index']]
        self.assertEqual(sorted(qs),[1171,169831])

    def test_three_source_roots(self):
        d=r.Arithmetic(DATA).dags()
        self.assertEqual(d['roots']['20771']['terminals'],[3,5])
        self.assertFalse(d['inventory_range_replayed'])

    def test_seven_frontier(self):
        v=[x for x in r.frontier_profiles(3,7) if any(x[3:])]
        self.assertEqual(v,[(0,2,2,3)])
        self.assertEqual(sum(Fraction(n,3**i) for i,n in enumerate(v[0])),1)

    def test_small_circuit_inside_seven(self):
        circuits=r.minimal_deficient((1,)*7)
        self.assertEqual(len(circuits),35)
        self.assertTrue(all(len(s)==3 for s in circuits))
        self.assertEqual(r.minimal_deficient((3,)*7),[tuple(range(7))])

    def test_no_depth_two_five_frontier_with_seven_leaves(self):
        self.assertEqual(r.frontier_profiles(5,7),[(0,5)])
        self.assertIn((0,4,5),r.frontier_profiles(5,9))

    def test_fixture_not_arithmetic_root_realization(self):
        fixture=r.conditional_fixture(r.Arithmetic(DATA))
        self.assertFalse(fixture['actual_nonregular_roots_instantiated'])
        self.assertFalse(fixture['actual_complete_certificate_constructed'])
        self.assertEqual(fixture['actual_regular_row_comparisons'],1051299)

if __name__=='__main__':unittest.main(verbosity=2)
