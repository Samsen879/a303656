#!/usr/bin/env python3
"""Fail-closed manifest and checksum verifier."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

from common import AuditError, sha256_file


TEXT_SUFFIXES = {".json", ".md", ".py", ".txt"}
FORBIDDEN_CONTROLS = set(range(0x00, 0x09)) | {0x0B, 0x0C} | set(range(0x0E, 0x20)) | {0x7F}


def verify_text_hygiene(root: Path) -> None:
    """Reject malformed UTF-8 and hidden C0/DEL controls in text payloads."""
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES):
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AuditError(f"invalid UTF-8: {path.relative_to(root).as_posix()}") from exc
        bad = sorted({byte for byte in data if byte in FORBIDDEN_CONTROLS})
        if bad:
            raise AuditError(
                f"forbidden control bytes {bad}: {path.relative_to(root).as_posix()}"
            )


def payload_paths(root: Path) -> list[Path]:
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.relative_to(root).as_posix() not in {"manifest.json", "SHA256SUMS.txt"}
    )


def build_manifest(root: Path, metadata: dict | None = None) -> dict:
    files = []
    for path in payload_paths(root):
        files.append({
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return {
        "schema": "a303656.deterministic-package-manifest.v1",
        "metadata": metadata or {},
        "files": files,
    }


def verify_manifest(root: Path, manifest: dict) -> None:
    if manifest.get("schema") != "a303656.deterministic-package-manifest.v1":
        raise AuditError("manifest schema mismatch")
    expected = {entry["path"]: entry for entry in manifest.get("files", [])}
    actual = {p.relative_to(root).as_posix(): p for p in payload_paths(root)}
    if set(expected) != set(actual):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise AuditError(f"manifest path mismatch missing={missing} extra={extra}")
    for rel, path in actual.items():
        entry = expected[rel]
        if path.stat().st_size != entry["size"]:
            raise AuditError(f"size mismatch: {rel}")
        if sha256_file(path) != entry["sha256"]:
            raise AuditError(f"sha256 mismatch: {rel}")


def verify_sha256s(root: Path) -> None:
    checksum_path = root / "SHA256SUMS.txt"
    if not checksum_path.is_file():
        raise AuditError("SHA256SUMS.txt missing")
    expected: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        digest, sep, rel = line.partition("  ")
        if not sep or len(digest) != 64:
            raise AuditError("malformed checksum line")
        expected[rel] = digest
    actual_paths = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.relative_to(root).as_posix() != "SHA256SUMS.txt"
    )
    actual_names = {p.relative_to(root).as_posix() for p in actual_paths}
    if set(expected) != actual_names:
        raise AuditError("SHA256SUMS path set mismatch")
    for path in actual_paths:
        rel = path.relative_to(root).as_posix()
        if sha256_file(path) != expected[rel]:
            raise AuditError(f"SHA256SUMS mismatch: {rel}")


def verify_root(root: Path) -> None:
    verify_text_hygiene(root)
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise AuditError("manifest.json missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verify_manifest(root, manifest)
    verify_sha256s(root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    verify_root(args.root.resolve())
    print("PASS")


if __name__ == "__main__":
    main()
