#!/usr/bin/env python3
"""Verify package hashes; optionally regenerate all canonical math results."""
from pathlib import Path
import argparse
import hashlib
import json
import tempfile
from reference import ROOT, run_all


def verify_manifest() -> int:
    expected = set()
    manifest = ROOT / "SHA256SUMS.txt"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if len(digest) != 64 or any(x not in "0123456789abcdef" for x in digest):
            raise ValueError("invalid digest")
        path = ROOT / relative
        if path.is_symlink() or ROOT not in path.resolve().parents:
            raise ValueError("unsafe manifest path")
        if relative in expected:
            raise ValueError("duplicate manifest path")
        expected.add(relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError("hash mismatch: " + relative)
    actual_files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts and p.name != "SHA256SUMS.txt"}
    if actual_files != expected:
        raise AssertionError("manifest inventory mismatch: " + repr(actual_files ^ expected))
    print(f"MANIFEST: PASS ({len(expected)} files)")
    return len(expected)


def replay() -> None:
    receipt = json.loads((ROOT / "results/replay_receipt.json").read_text())
    with tempfile.TemporaryDirectory(prefix="a303656-pooled-") as d:
        out = Path(d) / "results"
        run_all(out)
        names = [name + ".json" for name in receipt["result_sha256"]] + ["replay_receipt.json"]
        for name in names:
            if (out / name).read_bytes() != (ROOT / "results" / name).read_bytes():
                raise AssertionError("canonical replay mismatch: " + name)
        print(f"CANONICAL REPLAY: PASS ({len(names)} byte-identical JSON files)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    verify_manifest()
    if args.replay:
        replay()
