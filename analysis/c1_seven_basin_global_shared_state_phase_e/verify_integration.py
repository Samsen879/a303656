#!/usr/bin/env python3
"""Verify immutable producer payload and replay it in an isolated temporary tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "INTEGRATION_MANIFEST.json"
TRANSPORT_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz", ".7z", ".rar")
BINARY_SUFFIXES = (".pyc", ".pyo", ".o", ".obj", ".so", ".dll", ".exe", ".a")
FORBIDDEN_DIRS = {"__pycache__", ".local-bin", ".venv", "venv"}

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def verify_entry(entry: dict[str, object]) -> None:
    relative = str(entry["path"])
    target = (ROOT / relative).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file() or target.is_symlink():
        raise RuntimeError(f"invalid or missing manifest path: {relative}")
    if target.stat().st_size != entry["size"] or sha256(target) != entry["sha256"]:
        raise RuntimeError(f"size/SHA256 mismatch: {relative}")

def clean_json(value, ignored: set[str]):
    if isinstance(value, dict):
        return {key: clean_json(item, ignored) for key, item in value.items() if key not in ignored}
    if isinstance(value, list):
        return [clean_json(item, ignored) for item in value]
    return value

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["source_archive"]["committed"] is not False:
        raise RuntimeError("source archive policy is not fail-closed")
    if manifest["transport_archives_committed"] is not False or manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated artifact policy is not fail-closed")
    entries = [*manifest["source_payload"], *manifest["repository_native_files"]]
    for entry in entries:
        verify_entry(entry)
    expected = {str(entry["path"]) for entry in entries} | {MANIFEST_PATH.name}
    actual = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() or path.is_symlink()}
    if actual != expected:
        raise RuntimeError(f"integration inventory mismatch: {sorted(actual ^ expected)}")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_DIRS for part in relative.parts):
            raise RuntimeError(f"forbidden generated directory: {relative}")
        if path.is_file():
            lowered = relative.as_posix().lower()
            if lowered.endswith(TRANSPORT_SUFFIXES) or lowered.endswith(BINARY_SUFFIXES):
                raise RuntimeError(f"forbidden generated artifact: {relative}")
            if path.read_bytes()[:4] == b"\x7fELF":
                raise RuntimeError(f"compiled executable committed: {relative}")
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_ef_integration_") as tmp_name:
        temporary = Path(tmp_name)
        source_root = temporary / "source"
        source_root.mkdir()
        for entry in manifest["source_payload"]:
            relative = Path(str(entry["path"]))
            destination = source_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        replacements = {"{python}": sys.executable, "{tmp}": str(temporary)}
        for command in manifest["source_replay"]["commands"]:
            argv = [replacements.get(argument, argument.replace("{tmp}", str(temporary))) for argument in command]
            result = subprocess.run(argv, cwd=source_root, env=environment, check=False, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout.rstrip())
            if result.stderr:
                print(result.stderr.rstrip(), file=sys.stderr)
            if result.returncode:
                raise RuntimeError(f"source replay failed ({result.returncode}): {argv}")
        for comparison in manifest["source_replay"].get("json_comparisons", []):
            expected_path = source_root / comparison["expected"]
            actual_path = Path(comparison["actual"].replace("{tmp}", str(temporary)))
            ignored = set(comparison.get("ignore_keys", []))
            expected_json = clean_json(json.loads(expected_path.read_text()), ignored)
            actual_json = clean_json(json.loads(actual_path.read_text()), ignored)
            if expected_json != actual_json:
                raise RuntimeError(f"JSON replay mismatch: {comparison['expected']}")
    print(json.dumps({"status": "PASS", "source_payload_files": len(manifest["source_payload"]), "repository_native_files": len(manifest["repository_native_files"]), "isolated_source_replay": "PASS", "committed_source_tree_mutated": False}, indent=2))

if __name__ == "__main__":
    main()
