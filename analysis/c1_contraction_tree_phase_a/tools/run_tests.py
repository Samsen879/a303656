#!/usr/bin/env python3
"""Run the deterministic unittest suite and write machine-readable results."""
from __future__ import annotations

import argparse
import io
import json
import sys
import unittest
from pathlib import Path


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")
    test_ids = sorted(test.id() for test in flatten(suite))
    # Rediscover because flattening consumes nested iterators in some Python versions.
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    data = {
        "PASS": result.wasSuccessful(),
        "tests_run": result.testsRun,
        "test_ids": test_ids,
        "failures": [{"test": test.id(), "message": message} for test, message in result.failures],
        "errors": [{"test": test.id(), "message": message} for test, message in result.errors],
        "skipped": [{"test": test.id(), "reason": reason} for test, reason in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
