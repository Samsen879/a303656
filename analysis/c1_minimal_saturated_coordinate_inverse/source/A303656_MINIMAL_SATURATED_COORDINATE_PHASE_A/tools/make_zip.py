#!/usr/bin/env python3
"""Create a byte-deterministic uncompressed ZIP after verification."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path
import stat
import zipfile

from common import sha256_file
from verify_package import verify_root


def create_deterministic_zip(root: Path, output: Path) -> str:
    root = root.resolve()
    output = output.resolve()
    if output == root or root in output.parents:
        raise ValueError("ZIP output must be outside the package root")
    verify_root(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    prefix = root.name
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as zf:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{rel}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = 0o755 if path.suffix == ".py" else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, path.read_bytes())
    return sha256_file(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(create_deterministic_zip(args.root, args.output))


if __name__ == "__main__":
    main()
