#!/usr/bin/env python3
"""Verify Phase C source custody and replay it from an isolated temporary copy."""
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
GENERATED_BINARY_SUFFIXES = (".pyc", ".pyo", ".o", ".obj", ".so", ".dll", ".exe")


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
        lowered = relative.lower()
        if lowered.endswith(TRANSPORT_SUFFIXES):
            raise RuntimeError(f"transport archive committed: {relative}")
        if lowered.endswith(GENERATED_BINARY_SUFFIXES) or "__pycache__" in Path(relative).parts:
            raise RuntimeError(f"generated binary/cache committed: {relative}")
    return payload


def replay_source(manifest: dict[str, object], payload: list[dict[str, object]]) -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_c_integration_") as tmp_name:
        temporary = Path(tmp_name)
        source_root = temporary / "source"
        source_root.mkdir()
        for entry in payload:
            relative = Path(str(entry["path"]))
            destination = source_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

        replacements = {
            "{python}": sys.executable,
            "{tmp}": str(temporary),
        }
        for command in manifest["source_replay"]["commands"]:
            argv = [replacements.get(argument, argument) for argument in command]
            result = subprocess.run(
                argv,
                cwd=source_root,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )
            if result.stdout:
                print(result.stdout.rstrip())
            if result.stderr:
                print(result.stderr.rstrip(), file=sys.stderr)
            if result.returncode:
                raise RuntimeError(f"source replay failed ({result.returncode}): {argv}")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["source_archive"]["committed"] is not False:
        raise RuntimeError("source archive policy is not fail-closed")
    if manifest["transport_archives_committed"] is not False:
        raise RuntimeError("transport archive policy is not fail-closed")
    if manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated binary policy is not fail-closed")
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
