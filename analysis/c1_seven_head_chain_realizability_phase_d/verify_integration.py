#!/usr/bin/env python3
"""Fail-closed custody and isolated replay verifier for a Phase D package."""
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
MANIFEST_PATH = ROOT / "INTEGRATION_MANIFEST.json"
TRANSPORT_SUFFIXES = (
    ".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2",
    ".tar.xz", ".txz", ".7z", ".rar",
)
BINARY_SUFFIXES = (
    ".pyc", ".pyo", ".o", ".obj", ".a", ".so", ".dll", ".dylib", ".exe",
)
FORBIDDEN_PARTS = {"__pycache__", ".venv", "venv", "virtualenv"}


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
    if target.stat().st_size != entry["size"]:
        raise RuntimeError(f"size mismatch: {relative}")
    if sha256(target) != entry["sha256"]:
        raise RuntimeError(f"SHA256 mismatch: {relative}")


def verify_inventory(manifest: dict[str, object]) -> list[dict[str, object]]:
    payload = manifest["source_payload"]
    native = manifest["repository_native_files"]
    for entry in [*payload, *native]:
        verify_entry(entry)

    expected = {str(entry["path"]) for entry in [*payload, *native]}
    expected.add(MANIFEST_PATH.name)
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != expected:
        raise RuntimeError(f"integration inventory mismatch: {sorted(actual ^ expected)}")

    for relative in actual:
        path = Path(relative)
        lowered = relative.lower()
        if any(part.lower() in FORBIDDEN_PARTS for part in path.parts):
            raise RuntimeError(f"virtualenv/cache committed: {relative}")
        if lowered.endswith(TRANSPORT_SUFFIXES):
            raise RuntimeError(f"transport archive committed: {relative}")
        if lowered.endswith(BINARY_SUFFIXES):
            raise RuntimeError(f"generated binary committed: {relative}")
        target = ROOT / relative
        if target.is_symlink():
            raise RuntimeError(f"symlink committed: {relative}")
        if target.read_bytes()[:4] in (b"\x7fELF", b"MZ\x90\x00"):
            raise RuntimeError(f"executable binary committed: {relative}")
    return payload


def run(argv: list[str], cwd: Path, environment: dict[str, str]) -> None:
    result = subprocess.run(
        argv, cwd=cwd, env=environment, check=False, capture_output=True, text=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode:
        raise RuntimeError(f"source replay failed ({result.returncode}): {argv}")


def replay_source(manifest: dict[str, object], payload: list[dict[str, object]]) -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_d_integration_") as tmp_name:
        temporary = Path(tmp_name)
        source_root = temporary / "source"
        source_root.mkdir()
        for entry in payload:
            relative = Path(str(entry["path"]))
            destination = source_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

        def expand(value: str) -> str:
            return value.replace("{python}", sys.executable).replace("{tmp}", str(temporary))

        replay = manifest["source_replay"]
        for command in replay["commands"]:
            run([expand(str(argument)) for argument in command], source_root, environment)
        for comparison in replay.get("json_semantic_comparisons", []):
            frozen = json.loads((source_root / str(comparison["frozen"])).read_text(encoding="utf-8"))
            fresh = json.loads(Path(expand(str(comparison["fresh"]))).read_text(encoding="utf-8"))
            if frozen != fresh:
                raise RuntimeError(f"JSON semantic replay mismatch: {comparison}")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    archive = manifest["source_archive"]
    if archive["committed"] is not False:
        raise RuntimeError("source archive policy is not fail-closed")
    if manifest["transport_archives_committed"] is not False:
        raise RuntimeError("transport archive policy is not fail-closed")
    if manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated binary policy is not fail-closed")
    if manifest["manifest_self_hash"] is not None:
        raise RuntimeError("manifest self hash must remain null")
    payload = verify_inventory(manifest)
    replay_source(manifest, payload)
    print(json.dumps({
        "status": "PASS",
        "source_payload_files": len(payload),
        "repository_native_files": len(manifest["repository_native_files"]),
        "isolated_source_replay": "PASS",
        "committed_source_tree_mutated": False,
    }, indent=2))


if __name__ == "__main__":
    main()
