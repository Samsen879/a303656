#!/usr/bin/env python3
"""Replay the retained C21/C22 evidence in a disposable copy (stdlib only)."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_manifest(root):
    for line in (root / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        target = (root / name.lstrip("*")).resolve()
        require(target.is_relative_to(root.resolve()), "unsafe manifest path")
        require(hashlib.sha256(target.read_bytes()).hexdigest() == digest,
                f"manifest mismatch: {name}")


def read(root, name):
    return json.loads((root / name).read_text())


def check_c21(rows, key):
    require(len(rows) == 29, "C21 budget count")
    values = [F(row[key]) for row in rows]
    require(all(v < 1 for v in values), "C21 budget >= 1")
    require(1 - max(values) == F(2465867, 878169600), "C21 worst margin")


def check_c22(rows, key):
    require(len(rows) == 33, "C22 budget count")
    require(all(F(row[key]) < 1 for row in rows), "C22 budget >= 1")
    base = [r for r in rows if (r['M'], r['t']) == (7, 'base')]
    require(len(base) == 1 and F(base[0][key]) == F(155932663, 190512000),
            "C22 base")
    worst = max(rows, key=lambda r: F(r[key]))
    require((worst['M'], worst['t']) == (11, 11), "C22 maximum location")
    require(F(worst[key]) == F(4238011529, 4390848000), "C22 maximum")
    require(1 - F(worst[key]) == F(152836471, 4390848000), "C22 slack")


def main():
    source = PACKAGE / 'source/triage_packet'
    verify_manifest(source)
    with tempfile.TemporaryDirectory(prefix='a303656-triage-') as directory:
        root = Path(directory) / 'packet'
        shutil.copytree(source, root)
        for script in ('checks/root_c22_check.py',
                       'checks/c22_independent_budget.py', 'c21_frozen/verify.py'):
            # Explicitly disable inherited optimization: packet assertions must run.
            subprocess.run([sys.executable, '-E', '-B', str(root / script)],
                           cwd=root, check=True)
        c21 = read(root, 'checks/root_c21_results.json')
        check_c21(c21['budgets'], 'bound')
        require((len(c21['smooth_orders']), len(c21['factors']),
                 len(c21['catalog'])) == (80, 60, 46), 'root catalog counts')
        frozen = read(root, 'c21_frozen/certificate.json')
        check_c21(frozen['inequalities'], 'budget')
        verified = read(root, 'c21_frozen/verification.json')
        require(verified['finite_inequalities'] == 29 and
                F(verified['worst_margin']) == F(2465867, 878169600),
                'frozen C21 summary')
        root22 = read(root, 'checks/root_c22_results.json')
        independent = read(root, 'checks/c22_independent_budget.json')
        check_c22(root22['budgets'], 'bound')
        check_c22(independent['budgets'], 'budget')
        counts = independent['catalog_counts']
        require((counts['h'], counts['factors'], counts['inert']) == (80, 60, 46),
                'independent catalog counts')
        require([(r['M'], r['t'], F(r['bound'])) for r in root22['budgets']] ==
                [(r['M'], r['t'], F(r['budget'])) for r in independent['budgets']],
                'independent C22 budgets disagree')
    verify_manifest(source)
    print('TRIAGE_REPLAY_PASS: C21 29 budgets < 1; worst margin 2465867/878169600')
    print('C22 catalog 80/60/46; 33 budgets < 1; base 155932663/190512000')
    print('C22 max M=11 t=11: 4238011529/4390848000; slack 152836471/4390848000')
    print('A303656: UNRESOLVED')


if __name__ == '__main__':
    main()
