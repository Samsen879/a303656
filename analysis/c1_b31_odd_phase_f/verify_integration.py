#!/usr/bin/env python3
"""Verify immutable Phase-F payload, isolated replay, and Phase-E receipts."""
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
REPOSITORY = ROOT.parents[1]
MANIFEST_PATH = ROOT / "INTEGRATION_MANIFEST.json"
BINDING_PATH = ROOT / "DEPENDENCY_BINDING.json"
TRANSPORT_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz", ".7z", ".rar")
BINARY_SUFFIXES = (".pyc", ".pyo", ".o", ".obj", ".so", ".dll", ".exe", ".a")
FORBIDDEN_DIRS = {"__pycache__", ".local-bin", ".venv", "venv"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_file(base: Path, entry: dict[str, object]) -> None:
    relative = str(entry["path"])
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()) or not target.is_file() or target.is_symlink():
        raise RuntimeError(f"invalid or missing manifest path: {relative}")
    if target.stat().st_size != entry["size"] or sha256(target) != entry["sha256"]:
        raise RuntimeError(f"size/SHA256 mismatch: {relative}")


def clean_json(value, ignored: set[str]):
    if isinstance(value, dict):
        return {key: clean_json(item, ignored) for key, item in value.items() if key not in ignored}
    if isinstance(value, list):
        return [clean_json(item, ignored) for item in value]
    return value


def verify_binding(binding: dict[str, object], strict: bool) -> None:
    if binding["producer_source_gap"].get("preserved") is not True:
        raise RuntimeError("producer source gap is not preserved")
    if binding.get("local_dependency_reconciliation") != "PASS":
        raise RuntimeError("local dependency reconciliation is not PASS")
    status = binding.get("repository_dependency_status")
    blocked = binding.get("merge_blocked")
    if (status, blocked) not in {("PENDING_MERGE", True), ("BOUND_TO_MERGED_REPOSITORY", False)}:
        raise RuntimeError("dependency status / merge block is inconsistent")
    dependencies = binding.get("dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise RuntimeError("dependency receipt has no dependencies")
    for dependency in dependencies:
        if not isinstance(dependency.get("phase_e_draft_pr_number"), int):
            raise RuntimeError("dependency PR number missing")
        head = dependency.get("phase_e_draft_pr_head_sha", "")
        if not isinstance(head, str) or len(head) != 40:
            raise RuntimeError("dependency head SHA missing")
        if dependency.get("local_cross_binding_result") != "PASS":
            raise RuntimeError("dependency cross-binding is not PASS")
        for entry in dependency.get("relevant_source_payload_files", []):
            if set(entry) != {"path", "size", "sha256"}:
                raise RuntimeError("malformed dependency source-file receipt")
    receipts = binding.get("reconciliation_receipts", {})
    for key in ("C903", "C1806"):
        if key in receipts:
            receipt = receipts[key]
            own = ROOT / receipt["phase_f_path"]
            if receipt.get("byte_identity") != "PASS" or sha256(own) != receipt["sha256"]:
                raise RuntimeError(f"hard object receipt failed: {key}")
    if not strict:
        return
    if status != "BOUND_TO_MERGED_REPOSITORY" or blocked is not False:
        raise RuntimeError("strict dependency mode requires merged binding and merge_blocked=false")
    for dependency in dependencies:
        dep_root = (REPOSITORY / dependency["phase_e_destination_directory"]).resolve()
        if not dep_root.is_relative_to(REPOSITORY.resolve()) or not dep_root.is_dir():
            raise RuntimeError(f"merged dependency directory missing: {dep_root}")
        dep_manifest_path = dep_root / "INTEGRATION_MANIFEST.json"
        dep_manifest = json.loads(dep_manifest_path.read_text(encoding="utf-8"))
        if dep_manifest["source_archive"]["outer_sha256"] != dependency["phase_e_outer_sha256"]:
            raise RuntimeError(f"dependency archive identity mismatch: {dep_root}")
        payload = {entry["path"]: entry for entry in dep_manifest["source_payload"]}
        for entry in dependency["relevant_source_payload_files"]:
            if payload.get(entry["path"]) != entry:
                raise RuntimeError(f"dependency manifest binding mismatch: {dep_root / entry['path']}")
            verify_file(dep_root, entry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-merged-dependencies", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    if manifest["source_archive"]["committed"] is not False:
        raise RuntimeError("source archive policy is not fail-closed")
    if manifest["transport_archives_committed"] is not False or manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated artifact policy is not fail-closed")
    entries = [*manifest["source_payload"], *manifest["repository_native_files"]]
    for entry in entries:
        verify_file(ROOT, entry)
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
    verify_binding(binding, args.require_merged_dependencies)
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_f_integration_") as tmp_name:
        temporary = Path(tmp_name)
        source_root = temporary / "source"
        source_root.mkdir()
        for entry in manifest["source_payload"]:
            relative = Path(str(entry["path"]))
            destination = source_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        if manifest["source_archive"].get("source_integrity_type") == "MANIFEST.json":
            producer_manifest = json.loads((source_root / "MANIFEST.json").read_text(encoding="utf-8"))
            protected = producer_manifest.get("files")
            if not isinstance(protected, dict):
                raise RuntimeError("producer MANIFEST.json has no files mapping")
            actual_source = {
                path.relative_to(source_root).as_posix()
                for path in source_root.rglob("*")
                if path.is_file() and path.name != "MANIFEST.json"
            }
            if actual_source != set(protected):
                raise RuntimeError(f"producer manifest inventory mismatch: {sorted(actual_source ^ set(protected))}")
            for relative, expected_hash in protected.items():
                if sha256(source_root / relative) != expected_hash:
                    raise RuntimeError(f"producer manifest SHA256 mismatch: {relative}")
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
    print(json.dumps({
        "status": "PASS",
        "source_payload_files": len(manifest["source_payload"]),
        "repository_native_files": len(manifest["repository_native_files"]),
        "isolated_source_replay": "PASS",
        "local_dependency_reconciliation": "PASS",
        "repository_dependency_status": binding["repository_dependency_status"],
        "merge_blocked": binding["merge_blocked"],
        "strict_dependency_mode": args.require_merged_dependencies,
        "committed_source_tree_mutated": False
    }, indent=2))


if __name__ == "__main__":
    main()
