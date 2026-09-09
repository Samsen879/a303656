# Discovery is not verification

Only `../verify.py` and the root certificate files establish certified claims.
`ecpp_discover.py` uses SymPy/mpmath and CM hints. It does not supply trusted
primality facts until the separate exact verifier accepts its certificates.
The generator is a Linux-oriented research implementation (SIGALRM), not a
production ECPP implementation or the Morain/Primo/PARI package.

Portable path adaptation only: archived scripts now write beside themselves,
not to the original scratch directory. The original generated prime proof DAG
is preserved in `../primality_certificates.json`. The final verifier does not
import any discovery script. `class_polys.json` contains hints; none is used
by the verifier. The optional generator can create fresh proof paths different
from the frozen ones, so exact discovery-run reproduction is not claimed.

`all48_probe.py`: fixed48 orders, candidates q=k*n+1, 1<=k<=10000, odd q not5.
Primality screening there is discovery only; every factor retained in the
arithmetic evidence is proved by root-level certificates. Negative bounded
probe output is NOT used to close an index. No general Wieferich prime scan.

ECM receipts record successful/unsuccessful finite discovery experiments.
Only extracted factors, independently certified and checked, are evidence.
Elapsed seconds and no-factor outcomes prove no squarefree/absence statement.
