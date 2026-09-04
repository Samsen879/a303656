#!/usr/bin/env python3
"""Regenerate results, manifest, internal hashes, and deterministic ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
EXCLUDED_NAMES = {"manifest.json", "SHA256SUMS.txt"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def payload_files(root: Path, exclude_internal: bool = False) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(root).as_posix()
        if exclude_internal and rel in EXCLUDED_NAMES:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def clean_bytecode(root: Path) -> None:
    for path in sorted(root.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path)
    for path in root.rglob("*.pyc"):
        path.unlink()


def run_generation(root: Path) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    subprocess.run(
        [sys.executable, str(root / "tools" / "run_reference.py"), "--output-dir", str(root / "results")],
        check=True,
        cwd=root,
        env=env,
    )
    subprocess.run(
        [sys.executable, str(root / "tools" / "run_tests.py"), "--output", str(root / "results" / "test_results.json")],
        check=True,
        cwd=root,
        env=env,
    )
    clean_bytecode(root)


def write_manifest(root: Path) -> None:
    entries = []
    for path in payload_files(root, exclude_internal=True):
        rel = path.relative_to(root).as_posix()
        entries.append({
            "path": rel,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    manifest = {
        "schema": "a303656-deterministic-artifact-manifest-v1",
        "package": root.name,
        "authority": {
            "repository": "Samsen879/a303656",
            "repository_id": 1333945235,
            "main_sha": "29fee0317b268d2b2747f9564efc445fdd6da7f9",
            "main_tree": "0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55",
        },
        "generation": {
            "archive_method": "ZIP_STORED",
            "entry_order": "lexicographic POSIX path",
            "timestamp": "1980-01-01T00:00:00",
            "permissions": "0644 files; 0755 tools/*.py",
            "python_hash_seed": "0",
            "bytecode": "disabled",
        },
        "file_count": len(entries),
        "files": entries,
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_internal_sums(root: Path) -> None:
    lines = []
    for path in payload_files(root, exclude_internal=False):
        rel = path.relative_to(root).as_posix()
        if rel == "SHA256SUMS.txt":
            continue
        lines.append(f"{sha256_file(path)}  {rel}")
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_zip(root: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    prefix = root.name
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED, strict_timestamps=True) as zf:
        for path in payload_files(root, exclude_internal=False):
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{rel}", date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            mode = 0o755 if rel.startswith("tools/") and rel.endswith(".py") else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_STORED
            info.flag_bits = 0
            zf.writestr(info, path.read_bytes())
    digest = sha256_file(zip_path)
    sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    zip_path = args.zip_path.resolve()
    run_generation(root)
    write_manifest(root)
    write_internal_sums(root)
    build_zip(root, zip_path)
    print(f"ZIP_SHA256={sha256_file(zip_path)}")
    print(f"ZIP={zip_path}")
    print(f"SIDECAR={zip_path.with_suffix(zip_path.suffix + '.sha256')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
