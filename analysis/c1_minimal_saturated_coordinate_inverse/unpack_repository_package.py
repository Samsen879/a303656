#!/usr/bin/env python3
"""Reconstruct and safely unpack the authenticated coordinate-inverse package."""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path
import sys
import tarfile

EXPECTED_SHA256 = "1aba57b1b27f9564e840f2271b50a3090598e18266c300142d77bde0f3276efc"
EXPECTED_PARTS = 10


def safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.getmembers():
        if member.issym() or member.islnk() or member.isdev():
            raise SystemExit(f"unsafe archive member type: {member.name}")
        target = (destination / member.name).resolve()
        if target != destination and destination not in target.parents:
            raise SystemExit(f"unsafe archive path: {member.name}")
    archive.extractall(destination)


def main() -> int:
    root = Path(__file__).resolve().parent
    parts = sorted(
        (root / "package_parts").glob("repository_package.tar.xz.b64.part*")
    )
    if len(parts) != EXPECTED_PARTS:
        raise SystemExit(f"expected {EXPECTED_PARTS} parts, found {len(parts)}")

    encoded = b"".join(path.read_bytes() for path in parts)
    archive_bytes = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(archive_bytes).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"SHA-256 mismatch: {digest}")

    output_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else root / "_expanded_package"
    )
    package_dir = output_root / "package"
    output_root.mkdir(parents=True, exist_ok=True)
    archive_path = output_root / "repository_package.tar.xz"
    archive_path.write_bytes(archive_bytes)
    package_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path, mode="r:xz") as archive:
        safe_extract(archive, package_dir)

    print(package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
