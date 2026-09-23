# Reproduction

Requirements: Python 3.10+, a C++17 compiler, and the standard library only.
No network access or package installation is needed.

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  analysis/thread4_l53_falsification/verify.py
```

The wrapper performs, in order:

1. integrated and producer-packet hash checks;
2. compilation of the direct-enumeration Engine A in a temporary directory;
3. exhaustive scan from `m=2` through `7,963,079`;
4. arithmetic-criterion Engine B candidate reconstruction;
5. certificate regeneration and byte comparison;
6. producer `m<=5000` historical replay;
7. regression tests.

Expected deterministic hashes:

```text
support_scan.json:
c870ef43f13a033c0b6ae4f863d223b424bc5a5e6c0e6fca2c4c8419351887a3

membership_details.json:
a9a8acc176b74ca8b92fe9514916a55d6f1a18804b93c759e75515ea885c6a0a

l53_falsification_certificate.json:
bab0633619d185314680e5466d70bb0bd4b019bae202507ef3bd56817e1b0022
```
