#!/usr/bin/env python3
"""Zero-context, network-free verification of the curated A303656 repository."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "STATUS.md", "REPRODUCE.md", "LICENSE", "CITATION.cff",
    "docs/THEOREM_INDEX.md", "docs/ROUTE_MAP.md", "docs/FINITE_COMPUTATIONS.md",
    "docs/AUTHORITY_TREE.md", "docs/ARTIFACT_LINEAGE.md",
    "docs/PROVENANCE_BOUNDARY.md",
    "authority/frozen/FREEZE_RECEIPT.json",
    "authority/frozen/PUBLIC_RELEASE_RECEIPT.json",
]


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        fail("missing public surface files: " + ", ".join(missing))
    receipt = json.loads((ROOT / "authority/frozen/FREEZE_RECEIPT.json").read_text())
    if receipt.get("designation") != "MASTER AUTHORITY V2: FROZEN":
        fail("freeze designation")
    if receipt.get("a303656") != "UNRESOLVED":
        fail("A303656 status")
    private_commit = receipt.get("private_forensic_scope_patch_commit", "")
    if len(private_commit) != 40 or any(c not in "0123456789abcdef" for c in private_commit):
        fail("private forensic scope-patch identifier")
    if "scope_patch_commit" in receipt:
        fail("ambiguous public/private scope-patch field")
    if "not expected to resolve" not in receipt.get("private_forensic_commit_note", ""):
        fail("private forensic provenance note")
    release = json.loads((ROOT / "authority/frozen/PUBLIC_RELEASE_RECEIPT.json").read_text())
    if release.get("release_authorization") != "PUBLIC GITHUB RELEASE: AUTHORIZED":
        fail("public release authorization")
    if release.get("a303656") != "UNRESOLVED":
        fail("public release A303656 status")
    if release.get("scientific_authority", {}).get("sha256") != receipt.get("sha256"):
        fail("public release scientific authority binding")
    if release.get("release_root_post_commit_gate") != "MUST PASS BEFORE PUBLIC VISIBILITY":
        fail("public release post-commit gate")
    for section in ("sanitized_history", "privacy_scan", "fresh_clone", "github_actions"):
        if release.get(section, {}).get("status") != "PASS":
            fail(f"public release basis: {section}")
    artifact = ROOT / receipt["artifact_path"]
    if not artifact.is_file():
        fail("frozen artifact absent")
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != receipt["sha256"]:
        fail(f"frozen artifact hash {actual}")
    validator = ROOT / receipt["validator_path"]
    result = subprocess.run(
        [sys.executable, str(validator), str(artifact)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout, file=sys.stderr)
        fail("frozen authority recursive validator")
    generated = subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate_public_docs.py"), "--repo", str(ROOT), "--check"],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if generated.returncode:
        print(generated.stdout, file=sys.stderr)
        fail("generated public authority views")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    for name, text in [("README.md", readme), ("STATUS.md", status)]:
        if "UNRESOLVED" not in text or "no general proof" not in text.lower():
            fail(f"{name} lacks fail-closed project status")
    for rel in ["output/formal_results_audit.json", "output/final_packaging_audit.json"]:
        json.loads((ROOT / rel).read_text(encoding="utf-8"))
    print(json.dumps({
        "a303656": "UNRESOLVED",
        "frozen_authority_sha256": actual,
        "generated_docs": "PASS",
        "recursive_authority_validator": "PASS",
        "repository_surface": "PASS",
        "public_private_provenance_boundary": "PASS",
        "public_release_receipt": "PASS",
        "scope": "network-free metadata, custody, ledger, and stored-evidence validation; no multi-billion search rerun",
        "verdict": "PASS",
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
