#!/usr/bin/env python3
"""Black-box tests for the integer certificate CLI, with injected I/O failures."""
import errno
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "src/ajt5_integer_certificates.py"
sys.path.insert(0, str(CHECKER.parent))
import ajt5_integer_certificates as checker


class CertificateCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "certificate.json"

    def run_cli(self, *args):
        process = subprocess.run([sys.executable, "-O", str(CHECKER), *args],
                                 capture_output=True, check=False)
        self.assertEqual(process.stderr, b"")
        return process.returncode, json.loads(process.stdout)

    def check_cli(self, status, code, *args):
        rc, outcome = self.run_cli(*args)
        self.assertEqual((outcome["status"], rc), (status, code), outcome)
        return outcome

    def record(self, **kwargs):
        self.path.write_text(json.dumps(kwargs), encoding="utf-8")
        return self.path

    def test_bad_source_and_arguments(self):
        for args in [(self.path,), (self.path.parent,), (), ("--wrong-option",)]:
            with self.subTest(args=args):
                self.assertTrue(self.check_cli("INVALID", 2, *args)["reason"])

    def test_failed_reads(self):
        # Inject at read(), after open() succeeds. Both use the real CLI
        # parser, exit mapping and JSON output; no host-wide exhaustion needed.
        for error, status, code in [(MemoryError(), "UNKNOWN_RESOURCE", 4),
                                    (OSError(errno.ENOMEM, "out of memory"), "UNKNOWN_RESOURCE", 4),
                                    (OSError(errno.EIO, "input/output error"), "INVALID", 2)]:
            with self.subTest(error=error):
                stream = io.StringIO()
                with patch.object(Path, "open") as opened, redirect_stdout(stream):
                    opened.return_value.__enter__.return_value.read.side_effect = error
                    rc = checker.main([str(self.path)])
                self.assertEqual((json.loads(stream.getvalue())["status"], rc), (status, code))

    def test_strict_decode_and_limits(self):
        for data, status, code in [(b'\xff', "INVALID", 2), (b'{"n":2,"n":3}', "INVALID", 2),
                                   (b'1.0', "INVALID", 2), (b'NaN', "INVALID", 2),
                                   (b'['*65 + b']'*65, "UNKNOWN_RESOURCE", 4),
                                   (b' '*(8*1024*1024+1), "UNKNOWN_RESOURCE", 4),
                                   (str(1 << 4096).encode(), "UNKNOWN_RESOURCE", 4)]:
            with self.subTest(length=len(data), prefix=data[:8]):
                self.path.write_bytes(data)
                self.check_cli(status, code, self.path)

    def test_largest_parent_and_derived_child(self):
        # Supplied m fits 4096 bits; internally computed 5m+4 has 4099.
        m = (1 << 4096) - 1
        n = 5*m+4
        self.assertEqual(n.bit_length(), 4099)
        path = self.record(kind="NO_BRIDGE", m=m, r=4, positive=[], negative=[])
        self.check_cli("PARTIAL", 3, path)

    def test_five_bridges_at_m_two(self):
        # 2 = 0²+0²+3⁰+5⁰. Each listed child is an independent identity.
        parent = dict(side="parent", d=0, c=0, a=0, b=0)
        children = [(0, 0, 2, 2), (0, 0, 0, 3), (0, 0, 1, 3),
                    (1, 1, 1, 2), (0, 1, 1, 3)]
        for r, (e, c, a, b) in enumerate(children):
            self.assertEqual(10+r, 5**e+3**c+a*a+b*b)
            child = dict(side="child", d=e, c=c, a=a, b=b)
            path = self.record(kind="NO_BRIDGE", m=2, r=r, positive=[parent, child], negative=[])
            self.assertEqual(self.check_cli("REFUTED", 1, path)["bridge"], [0, e])

    def test_unitary_composite_and_prime(self):
        # 62-5^0-3^0 = 60. 15 and 3 are both valid units. Other active
        # c and d still need evidence for a complete EMPTY_D certificate.
        for n, u, status, code in [(62, 15, "PARTIAL", 3), (62, 3, "PARTIAL", 3),
                                   (47, 15, "INVALID", 2), (47, 3, "INVALID", 2)]:
            column = dict(side="target", d=0, units=[dict(c=0, u=u)])
            path = self.record(kind="EMPTY_D", n=n, positive=[], negative=[column])
            self.check_cli(status, code, path)

    def test_not_activated_and_zero(self):
        # At d=1, c=1 the equality point is x=5+3. Below it the row is
        # NOT_ACTIVATED. A fixed-window calculation cannot submit it as evidence.
        zero = dict(side="target", d=1, c=1, a=0, b=0)
        for n, status, code in [(7, "INVALID", 2), (8, "REFUTED", 1)]:
            path = self.record(kind="EMPTY_D", n=n, positive=[zero], negative=[])
            self.check_cli(status, code, path)
        col = dict(side="target", d=1, units=[dict(c=1, u=3)])
        for n in (7, 8):
            path = self.record(kind="EMPTY_D", n=n, positive=[], negative=[col])
            self.check_cli("INVALID", 2, path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
