#!/usr/bin/env python3
"""Verify Phase G custody, dependency binding, isolated replay, and scope."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[1]
NATIVE = {
    "INTEGRATION.md", "DEPENDENCY_BINDING.json", "INTEGRATION_MANIFEST.json",
    "verify_integration.py", "tests/test_integration_scope.py",
}
FORBIDDEN_DIRS = {"__pycache__", ".venv", "venv"}
FORBIDDEN_SUFFIXES = (".zip", ".7z", ".rar", ".tar", ".tgz", ".pyc", ".pyo", ".o", ".obj", ".so", ".dll", ".exe", ".a")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def producer_entries() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(maxsplit=1)
        relative = relative.lstrip("* ")
        if relative in entries or relative == "SHA256SUMS.txt":
            raise RuntimeError(f"invalid producer manifest entry: {relative}")
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file() or target.is_symlink():
            raise RuntimeError(f"unsafe or missing producer path: {relative}")
        if sha256(target) != digest:
            raise RuntimeError(f"producer SHA256 mismatch: {relative}")
        entries[relative] = digest
    if len(entries) != 13:
        raise RuntimeError("producer manifest entry count changed")
    return entries


def verify_dependencies() -> None:
    binding = json.loads((ROOT / "DEPENDENCY_BINDING.json").read_text(encoding="utf-8"))
    if binding.get("status") != "BOUND_TO_MERGED_REPOSITORY" or binding.get("repository_source_wins") is not True:
        raise RuntimeError("dependency binding is not fail-closed")
    for item in binding["dependencies"]:
        target = (REPOSITORY / item["path"]).resolve()
        if not target.is_relative_to(REPOSITORY.resolve()) or sha256(target) != item["sha256"]:
            raise RuntimeError(f"dependency mismatch: {item['path']}")


def main() -> None:
    manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest["source_archive"]["committed"] is not False:
        raise RuntimeError("transport archive policy changed")
    if manifest["transport_archives_committed"] is not False or manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated artifact policy changed")
    entries = producer_entries()
    expected = set(entries) | {"SHA256SUMS.txt"} | NATIVE
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() or p.is_symlink()}
    if actual != expected:
        raise RuntimeError(f"integration inventory mismatch: {sorted(actual ^ expected)}")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_DIRS for part in relative.parts):
            raise RuntimeError(f"forbidden generated directory: {relative}")
        if path.is_symlink() or (path.is_file() and relative.as_posix().lower().endswith(FORBIDDEN_SUFFIXES)):
            raise RuntimeError(f"forbidden artifact: {relative}")
    verify_dependencies()
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_g_dpr_") as tmp_name:
        temporary = Path(tmp_name)
        source = temporary / "source"
        source.mkdir()
        for relative in set(entries) | {"SHA256SUMS.txt"}:
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        output = temporary / "results.json"
        result = subprocess.run(
            [sys.executable, "-B", "verify.py", "--check-hashes", "--out", str(output)],
            cwd=source, env=environment, check=False, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        replay = json.loads(output.read_text(encoding="utf-8"))
        frozen = json.loads((source / "results.json").read_text(encoding="utf-8"))
        if replay != frozen or replay.get("negative_controls_rejected") != 12:
            raise RuntimeError("isolated replay or mutation-control mismatch")
    print(json.dumps({
        "status": "PASS",
        "producer_files": 14,
        "producer_hash_entries": 13,
        "isolated_replay": "PASS",
        "mutation_controls_rejected": 12,
        "dependency_binding": "PASS",
        "abstract_model_is_actual_certificate": False,
    }, indent=2))


if __name__ == "__main__":
    main()
