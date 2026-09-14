import json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class ScopeTests(unittest.TestCase):
    def test_no_failed_producer_promoted(self):
        self.assertTrue(all(r['producer_replay']=='PASS' for r in json.loads((P/'SOURCE_RECEIPTS.json').read_text())))
    def test_strategic_quantifiers(self):
        text=(P/'ML_D2_GATE.md').read_text();self.assertIn('OUTSIDE bulk D=4',text);self.assertIn('does NOT disprove',text)
        text=(P/'MISSING_LEMMA.md').read_text();self.assertIn('ML-K2 is NOT proved',text);self.assertIn('IF ML-K2 held',text)
    def test_no_large_transport_or_binary(self):
        for path in P.rglob('*'):
            if path.is_file():
                self.assertLess(path.stat().st_size,10*1024*1024)
                self.assertNotIn(path.suffix.lower(),['.zip','.npz','.bin','.o','.exe'])
    def test_independent_pr_b_scope(self):
        readme=(P/'README.md').read_text();self.assertNotIn('reference/producer',readme)
        status=(P.parents[1]/'STATUS.md').read_text()
        for s in ['PROJECT: PAUSED','ACTIVE PROMOTED ROUTE: NONE','DIRECT ORIGINAL-n PROGRAM: PAUSED','A303656: UNRESOLVED','LARGE-SCALE COMPUTATION: NOT AUTHORIZED']:self.assertIn(s,status)
    def test_duplicates_not_new_authority(self):
        text=(P/'NOVELTY_MATRIX.md').read_text()
        for line in text.splitlines():
            if '| J witness reformulation |' in line or '| J large-pair result |' in line:self.assertNotIn('NEW AUTHORITY',line)
if __name__=='__main__':unittest.main()
