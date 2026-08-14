#!/usr/bin/env python3
"""Generate public authority views from the immutable frozen Master V2 ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

RECEIPT = Path("authority/frozen/FREEZE_RECEIPT.json")


def load_json(zf: zipfile.ZipFile, root: str, name: str):
    return json.loads(zf.read(f"{root}/{name}"))


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    return (
        "| " + " | ".join(headers) + " |\n"
        + "|" + "|".join("---" for _ in headers) + "|\n"
        + "\n".join("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    )


def generated(repo: Path):
    receipt = json.loads((repo / RECEIPT).read_text(encoding="utf-8"))
    artifact = repo / receipt["artifact_path"]
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != receipt["sha256"]:
        raise RuntimeError(f"frozen artifact hash mismatch: {actual}")
    with zipfile.ZipFile(artifact) as zf:
        root = zf.namelist()[0].split("/", 1)[0]
        theorems = load_json(zf, root, "THEOREM_LEDGER.json")["entries"]
        routes = load_json(zf, root, "ROUTE_MATRIX.json")["routes"]
        finite = load_json(zf, root, "FINITE_COMPUTATION_LEDGER.json")["entries"]

    theorem_md = """# Theorem and conditional-authority index

This file is generated from the frozen Master Authority V2 artifact. It is an index, not a replacement for the source packages or proofs. A303656 remains **UNRESOLVED**.

""" + table(
        ["ID", "Classification", "Name", "Statement", "Scope limit", "Sources"],
        [
            (
                item["id"], item["classification"], item["name"], item["statement"],
                item["scope_limit"], ", ".join(item["source_ids"]),
            )
            for item in theorems
        ],
    ) + "\n"

    route_md = """# Route map

This file records research-route status. `STOP` means the audited trigger or formal class is closed at its stated scope; it never means that every conceivable method is impossible.

""" + table(
        ["ID", "Route", "State", "Authority", "Reason", "Exact restart trigger"],
        [
            (
                item["id"], item["route"], item["state"], item["authority"],
                item["reason"], item["exact_restart_trigger"] or "—",
            )
            for item in routes
        ],
    ) + "\n"

    finite_md = """# Certified and exact finite computations

Finite computations establish only their explicit domains. They are not a universal proof and do not establish a counterexample.

""" + table(
        ["ID", "Classification", "Name", "Explicit interval or domain", "Result", "Scope limit", "Sources"],
        [
            (
                item["id"], item["classification"], item["name"], item["explicit_bounds"],
                item["result"], item["scope_limit"], ", ".join(item["source_ids"]),
            )
            for item in finite
        ],
    ) + "\n"
    return {
        Path("docs/THEOREM_INDEX.md"): theorem_md,
        Path("docs/ROUTE_MAP.md"): route_md,
        Path("docs/FINITE_COMPUTATIONS.md"): finite_md,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    failures = []
    for rel, text in generated(repo).items():
        path = repo / rel
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                failures.append(rel.as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if failures:
        print("Generated authority views are stale: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("PUBLIC_AUTHORITY_DOCS=" + ("PASS" if args.check else "GENERATED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
