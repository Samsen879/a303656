# Reproduce Phase 0.5 outputs

```bash
python3 scripts/phase05_reconcile.py --repo . --phase0 /tmp/a303656_evidence_alignment_20260813 --original-repo /home/samsen/code/a303656/repo/a303656_bounded_counterexample
python3 scripts/build_master_authority_v2.py --repo . --stage /tmp/a303656_master_v2_replay --output /tmp/master-v2-replay.zip
python3 scripts/verify_master_authority_v2.py /tmp/master-v2-replay.zip
sha256sum /tmp/master-v2-replay.zip
```

Expected Master V2 candidate SHA256: `f387abf7ccf8aba381977e9e34b0a80d6811a18dd6fd3aadbbaeddb85ab17b8e`. No large-scale finite search is part of this replay.
