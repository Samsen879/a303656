# A303656 prime-scan extension and seven-prime proof review

Read REPORT.md first; REVIEW.md records the scoped review verdict. The fresh
proof is SEVEN_PRIME_INDEPENDENT_PROOF.md. The bounded inventory also has a
separate selected-anchor blocker proof in EXPANDED_PANEL_BLOCKER_PROOF.md.

No GitHub writes. No route promotion. No claim to resolve A303656.

## Verify / reproduce

Python 3 standard library suffices for integrity and mathematical review.
The two enlarged scan implementations require g++ with unsigned __int128.

```sh
python tools/verify_package.py
python tools/verify_package.py --replay-small
python tools/verify_package.py --replay-scan
```

The small replay reruns the fresh mathematical checks, the independent Python
10^7 baseline, the 15 new tests, and the included original source's full
reference replay and 15 tests. The scan replay rebuilds both native scanners,
rechecks all admitted primes through 2e9, and reruns the all-odd auxiliary
scan through 1e8. All replay output goes into a disposable temporary copy;
frozen files are not overwritten. Do not run verification under python -O.

SHA256SUMS.txt binds every payload file; mathematical hashes canonicalize JSON
by removing only keys exactly named `seconds`. The scan JSONL records are
compared byte-for-byte in the full replay. Stream fingerprints are regression
checks, not substitutes for the prime-sieve and modular-arithmetic algorithms.

The original research bundle is preserved, unmodified, under evidence/ with
its own checksums. Producer tests and the newly written review checks are
reported separately. “Independent” denotes different derivation/code cores,
not a different author/model or formal proof-assistant verification.
