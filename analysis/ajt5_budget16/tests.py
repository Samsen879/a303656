import gzip
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from paths import HERE
import replay
from check_control import check


class AdversarialChecks(unittest.TestCase):
    def test_bound_equality_and_wrong_weights(self):
        for node in ([1,[1,0]], [True,[1,1]], [1,[1]], [1,[1,2]]):
            with self.subTest(node=node), self.assertRaises(ValueError):
                replay.check_tree(node,{0,1},{},1,Counter())

    def test_single_residue_and_default_budget(self):
        roots={0,1,7,8}
        catalogue=replay.catalogue(roots)
        self.assertEqual(catalogue,{7:{0:{0,7},1:{1,8}}})
        default=[None,[1,[1,1,1,1]]]
        a,b=[0,[1,[1,1]]],[1,[1,[1,1]]]
        replay.check_tree([7,[default,a,b]],roots,catalogue,1,Counter())
        for branch in ([a,b],[default,a,a],[default,b],[default,a,b,b]):
            with self.assertRaises(ValueError):
                replay.check_tree([7,branch],roots,catalogue,1,Counter())
        roots={0,11,77}
        self.assertTrue(all((143-k)%11==0 and (143-k)%121 for k in roots))
        forged=[7,[[None,[1,[1,0,0]]],[0,[1,[1]]]]]
        with self.assertRaisesRegex(ValueError,"non-strict"):
            replay.check_tree(forged,roots,replay.catalogue(roots),1,Counter())

    def test_odd_three_is_contained(self):
        for delta in range(-1000,1001):
            if delta==0:
                continue
            t=abs(delta)
            h=0
            while t%3==0:
                h+=1
                t//=3
            if h%2:
                self.assertFalse(delta%3 or (delta%9==0 and delta%27!=0))
        self.assertEqual(9%27,9)  # valuation two stays alive
        self.assertEqual(81%27,0) # valuation four can be conservatively removed

    def test_missing_prefix_or_wrong_direction(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.gz"
            for line,reason in (("[0,1,[]]","direction order"),
                                ('[0,0,[[],[],[]]]',"mod27 children"),
                                ('[0,0,[false,[],[]]]',"mod27 children")):
                with gzip.open(p,"wt") as f:
                    f.write(line+"\n")
                with self.assertRaisesRegex(ValueError,reason):
                    replay.verify(p)

    def test_countercontrol_mutations(self):
        data=json.loads((HERE/"control.json").read_bytes())
        for key,value in (("palette",data["palette"][:-1]+[3]),
                          ("crt_modulus",1),("child",[0,0])):
            with self.subTest(field=key),self.assertRaises(ValueError):
                check(dict(data,**{key:value}))

if __name__=="__main__":
    unittest.main(verbosity=2)
