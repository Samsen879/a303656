#!/usr/bin/env python3
"""Scan repository files and nested archives without disclosing matched addresses."""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tarfile
import zipfile
from pathlib import Path

EMAIL = re.compile(rb"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}")
SKIP_PARTS = {".git", ".venv", "reproduce_work", "__pycache__"}
MAX_DEPTH = 12
MAX_MEMBER_BYTES = 1024 * 1024 * 1024


def archive_kind(name: str, data: bytes) -> str | None:
    lower = name.lower()
    if data.startswith(b"PK\x03\x04") or lower.endswith(".zip"):
        return "zip"
    if lower.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz")):
        return "tar"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--forbid-env", help="environment variable holding one exact forbidden address")
    parser.add_argument("--reject-domain", action="append", default=[])
    args = parser.parse_args()
    root = args.root.resolve()
    forbidden = None
    if args.forbid_env:
        value = os.environ.get(args.forbid_env)
        if not value:
            print("FAIL: forbidden-address environment variable is absent", file=sys.stderr)
            return 2
        forbidden = value.encode("utf-8").lower()
    rejected = {d.lower().lstrip("@") for d in args.reject_domain}
    stats = {"regular_files": 0, "archive_members": 0, "streams": 0, "bytes_scanned": 0}
    failures: list[dict[str, str]] = []
    archive_errors: list[dict[str, str]] = []

    def inspect(label: str, data: bytes, depth: int) -> None:
        stats["streams"] += 1
        stats["bytes_scanned"] += len(data)
        low = data.lower()
        if forbidden and forbidden in low:
            failures.append({"location": label, "reason": "exact_forbidden_address"})
        for match in EMAIL.finditer(data):
            domain = match.group(0).rsplit(b"@", 1)[1].decode("ascii", "ignore").lower()
            if domain in rejected:
                failures.append({"location": label, "reason": "rejected_email_domain"})
        if depth >= MAX_DEPTH:
            archive_errors.append({"location": label, "reason": "maximum_archive_depth"})
            return
        kind = archive_kind(label, data)
        if kind == "zip":
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as zf:
                    bad = zf.testzip()
                    if bad is not None:
                        archive_errors.append({"location": label, "reason": "zip_crc_failure"})
                    for info in zf.infolist():
                        if info.is_dir():
                            continue
                        if info.file_size > MAX_MEMBER_BYTES:
                            archive_errors.append({"location": f"{label}!/{info.filename}", "reason": "member_too_large"})
                            continue
                        stats["archive_members"] += 1
                        inspect(f"{label}!/{info.filename}", zf.read(info), depth + 1)
            except (OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
                archive_errors.append({"location": label, "reason": type(exc).__name__})
        elif kind == "tar":
            try:
                with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tf:
                    for member in tf:
                        if not member.isfile():
                            continue
                        if member.size > MAX_MEMBER_BYTES:
                            archive_errors.append({"location": f"{label}!/{member.name}", "reason": "member_too_large"})
                            continue
                        handle = tf.extractfile(member)
                        if handle is None:
                            continue
                        stats["archive_members"] += 1
                        inspect(f"{label}!/{member.name}", handle.read(), depth + 1)
            except (OSError, tarfile.TarError, ValueError) as exc:
                archive_errors.append({"location": label, "reason": type(exc).__name__})

    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        low_rel = rel.lower().encode("utf-8")
        if forbidden and forbidden in low_rel:
            failures.append({"location": rel, "reason": "exact_forbidden_address_in_path"})
        stats["regular_files"] += 1
        try:
            inspect(rel, path.read_bytes(), 0)
        except OSError as exc:
            archive_errors.append({"location": rel, "reason": type(exc).__name__})

    result = {
        **stats,
        "archive_errors": len(archive_errors),
        "privacy_findings": len(failures),
        "verdict": "PASS" if not failures and not archive_errors else "FAIL",
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    if failures:
        print(json.dumps({"findings": failures}, sort_keys=True, indent=2), file=sys.stderr)
    if archive_errors:
        print(json.dumps({"archive_errors": archive_errors}, sort_keys=True, indent=2), file=sys.stderr)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
