#!/usr/bin/env python3
"""Fail-closed verifier for the repository-native inverse-classification integration."""
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
import zipfile


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str], cwd: Path) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    subprocess.run(command, cwd=cwd, env=env, check=True)


def verify_integration_manifest(root: Path) -> int:
    manifest = read_json(root / "INTEGRATION_MANIFEST.json")
    if manifest.get("schema") != "a303656.repository-integration-manifest.v1":
        raise ValueError("integration manifest schema mismatch")
    expected = {entry["path"]: entry for entry in manifest.get("files", [])}
    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and path.name != "INTEGRATION_MANIFEST.json"
    }
    if set(expected) != set(actual):
        raise ValueError(
            f"integration path mismatch missing={sorted(set(expected)-set(actual))} "
            f"extra={sorted(set(actual)-set(expected))}"
        )
    for rel, path in actual.items():
        entry = expected[rel]
        if path.stat().st_size != entry["size"]:
            raise ValueError(f"integration size mismatch: {rel}")
        if sha256_file(path) != entry["sha256"]:
            raise ValueError(f"integration SHA-256 mismatch: {rel}")
    return len(actual)


def verify_source_subset(root: Path) -> tuple[int, int]:
    receipt = read_json(root / "PACKAGE_RECEIPT.json")
    package_manifest = read_json(root / "package_metadata" / "manifest.json")
    manifest_entries = {entry["path"]: entry for entry in package_manifest["files"]}
    source_root = root / receipt["package"]["source_template_path"]

    source_files = [path for path in source_root.rglob("*") if path.is_file()]
    for path in source_files:
        rel = path.relative_to(source_root).as_posix()
        entry = manifest_entries.get(rel)
        if entry is None:
            raise ValueError(f"source file absent from sealed package manifest: {rel}")
        if path.stat().st_size != entry["size"] or sha256_file(path) != entry["sha256"]:
            raise ValueError(f"source file differs from sealed package: {rel}")

    compact_results = [path for path in (root / "results").rglob("*") if path.is_file()]
    for path in compact_results:
        rel = "results/" + path.relative_to(root / "results").as_posix()
        entry = manifest_entries.get(rel)
        if entry is None:
            raise ValueError(f"compact result absent from sealed package manifest: {rel}")
        if path.stat().st_size != entry["size"] or sha256_file(path) != entry["sha256"]:
            raise ValueError(f"compact result differs from sealed package: {rel}")

    sidecar = (root / "package_metadata" / "A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A.zip.sha256").read_text(encoding="utf-8").split()[0]
    if sidecar != receipt["package"]["zip_sha256"]:
        raise ValueError("ZIP sidecar and receipt disagree")
    if sha256_file(root / "package_metadata" / "manifest.json") != receipt["package"]["package_manifest_sha256"]:
        raise ValueError("sealed package manifest hash mismatch")
    if sha256_file(root / "package_metadata" / "SHA256SUMS.txt") != receipt["package"]["package_checksums_sha256"]:
        raise ValueError("sealed package checksum-list hash mismatch")
    return len(source_files), len(compact_results)


def full_replay(root: Path) -> dict:
    receipt = read_json(root / "PACKAGE_RECEIPT.json")
    source = root / receipt["package"]["source_template_path"]
    with tempfile.TemporaryDirectory(prefix="a303656-inverse-replay-") as tmp:
        tmp_path = Path(tmp)
        replay_root = tmp_path / source.name
        shutil.copytree(source, replay_root)
        run([sys.executable, "tools/reproduce.py", "--root", str(replay_root)], replay_root)
        run([sys.executable, "tools/verify_package.py", "--root", str(replay_root)], replay_root)
        output = tmp_path / f"{source.name}.zip"
        run([sys.executable, "tools/make_zip.py", "--root", str(replay_root), "--output", str(output)], replay_root)
        digest = sha256_file(output)
        size = output.stat().st_size
        with zipfile.ZipFile(output) as archive:
            entries = len(archive.namelist())
        package = receipt["package"]
        if digest != package["zip_sha256"]:
            raise ValueError(f"replayed ZIP hash mismatch: {digest}")
        if size != package["zip_size"] or entries != package["zip_entries"]:
            raise ValueError("replayed ZIP size or entry count mismatch")
        return {"zip_sha256": digest, "zip_size": size, "zip_entries": entries}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--full-replay", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    integration_files = verify_integration_manifest(root)
    source_files, compact_results = verify_source_subset(root)
    output = {
        "PASS": True,
        "integration_files_checked": integration_files,
        "source_files_checked": source_files,
        "compact_results_checked": compact_results,
    }
    if args.full_replay:
        output["full_replay"] = full_replay(root)
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
