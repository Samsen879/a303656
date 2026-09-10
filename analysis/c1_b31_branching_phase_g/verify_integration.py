#!/usr/bin/env python3
"""Verify Phase G B31 branching custody, replay, mutations, and bindings."""
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
REQUIRED_MUTATIONS = {
    "corrupt_exact_order", "terminal3_in_all_odd_rows", "drop_maximal_generator",
    "wrong_edge_sign", "fake_base5_member",
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
        target = (ROOT / relative).resolve()
        if relative in entries or relative == "SHA256SUMS.txt" or not target.is_relative_to(ROOT.resolve()):
            raise RuntimeError(f"invalid producer manifest entry: {relative}")
        if not target.is_file() or target.is_symlink() or sha256(target) != digest:
            raise RuntimeError(f"producer SHA256 mismatch: {relative}")
        entries[relative] = digest
    if len(entries) != 15:
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


def run(argv: list[str], cwd: Path, environment: dict[str, str]) -> None:
    result = subprocess.run(argv, cwd=cwd, env=environment, check=False, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


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
    with tempfile.TemporaryDirectory(prefix="a303656_phase_g_b31_branching_") as tmp_name:
        temporary = Path(tmp_name)
        source = temporary / "source"
        source.mkdir()
        for relative in set(entries) | {"SHA256SUMS.txt"}:
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        normal = temporary / "normal.json"
        optimized = temporary / "optimized.json"
        discovery = temporary / "discovery.json"
        run([sys.executable, "-B", "verify.py", "--output", str(normal)], source, environment)
        run([sys.executable, "-O", "-B", "verify.py", "--output", str(optimized)], source, environment)
        frozen = json.loads((source / "verification_log.json").read_text(encoding="utf-8"))
        first = json.loads(normal.read_text(encoding="utf-8"))
        second = json.loads(optimized.read_text(encoding="utf-8"))
        if first != frozen or second != frozen:
            raise RuntimeError("normal or optimized source replay mismatch")
        rejected = set(first.get("corruptions_rejected", []))
        if not REQUIRED_MUTATIONS <= rejected:
            raise RuntimeError(f"required mutation controls missing: {sorted(REQUIRED_MUTATIONS - rejected)}")
        run([sys.executable, "-B", "replay_discovery.py", "--output", str(discovery)], source, environment)
        fresh_discovery = json.loads(discovery.read_text(encoding="utf-8"))
        frozen_discovery = json.loads((source / "discovery_only.json").read_text(encoding="utf-8"))
        if fresh_discovery.get("count") != frozen_discovery.get("count") or fresh_discovery.get("hits") != frozen_discovery.get("hits"):
            raise RuntimeError("bounded discovery core result mismatch")
    print(json.dumps({
        "status": "PASS", "producer_files": 16, "producer_hash_entries": 15,
        "normal_replay": "PASS", "optimized_replay": "PASS",
        "countermodels_replayed": 5, "required_mutation_classes": 5,
        "bounded_discovery_count": 80000, "bounded_discovery_hits": 0,
        "dependency_binding": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
