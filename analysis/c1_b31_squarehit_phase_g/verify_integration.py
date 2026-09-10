#!/usr/bin/env python3
"""Verify consolidated Phase G B31 square-hit custody, replay, and scope."""
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
REPOSITORY = ROOT.parents[1]
CORE = ROOT / "producer_core"
WRAPPERS = ROOT / "task_wrappers"
NATIVE = {
    "SOURCE_CUSTODY.md", "SOURCE_CONSOLIDATION.json", "INTEGRATION.md",
    "DEPENDENCY_BINDING.json", "INTEGRATION_MANIFEST.json",
    "verify_integration.py", "tests/test_integration_scope.py",
}
CORE_FILES = {
    "AUTHORITY.json", "PROOFS.md", "README.md", "SOURCE_BINDING.json",
    "certificates.json", "evidence.json", "generate_certificates.py", "reference.py",
}
WRAPPER_FILES = {"REPORT.md", "results.json", "verification_log.json"}
FORBIDDEN_DIRS = {"__pycache__", ".venv", "venv"}
FORBIDDEN_SUFFIXES = (".zip", ".7z", ".rar", ".tar", ".tgz", ".pyc", ".pyo", ".o", ".obj", ".so", ".dll", ".exe", ".a")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source_manifest(task: str, manifest_name: str) -> None:
    manifest = ROOT / "source_manifests" / manifest_name
    seen: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(maxsplit=1)
        relative = relative.lstrip("* ")
        if relative in seen or relative == "SHA256SUMS.txt":
            raise RuntimeError(f"invalid producer manifest entry: {relative}")
        seen.add(relative)
        if relative in CORE_FILES:
            target = CORE / relative
        elif relative in WRAPPER_FILES:
            target = WRAPPERS / task / relative
        else:
            raise RuntimeError(f"unmapped producer path: {relative}")
        if not target.is_file() or target.is_symlink() or sha256(target) != digest:
            raise RuntimeError(f"producer SHA256 mismatch for {task}: {relative}")
    if seen != CORE_FILES | WRAPPER_FILES:
        raise RuntimeError(f"producer inventory mismatch for {task}: {sorted(seen ^ (CORE_FILES | WRAPPER_FILES))}")


def verify_dependencies() -> None:
    binding = json.loads((ROOT / "DEPENDENCY_BINDING.json").read_text(encoding="utf-8"))
    if binding.get("status") != "BOUND_TO_MERGED_REPOSITORY" or binding.get("repository_source_wins") is not True:
        raise RuntimeError("dependency binding is not fail-closed")
    for item in binding["dependencies"]:
        target = (REPOSITORY / item["path"]).resolve()
        if not target.is_relative_to(REPOSITORY.resolve()) or sha256(target) != item["sha256"]:
            raise RuntimeError(f"dependency mismatch: {item['path']}")


def run(argv: list[str], cwd: Path, environment: dict[str, str]) -> None:
    result = subprocess.run(argv, cwd=cwd, env=environment, check=False, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main() -> None:
    manifest = json.loads((ROOT / "INTEGRATION_MANIFEST.json").read_text(encoding="utf-8"))
    consolidation = json.loads((ROOT / "SOURCE_CONSOLIDATION.json").read_text(encoding="utf-8"))
    if manifest["transport_archives_committed"] is not False or manifest["generated_binaries_committed"] is not False:
        raise RuntimeError("generated artifact policy changed")
    archives = {item["id"]: item for item in consolidation["archives"]}
    if archives["E-v2"]["sha256"] != archives["E-v2-duplicate"]["sha256"]:
        raise RuntimeError("exact duplicate receipt mismatch")
    if consolidation.get("independent_implementations_claimed") != 0:
        raise RuntimeError("shared producer core mislabeled as independent")
    expected_core = consolidation["shared_cores"][1]["byte_identical_files"]
    if set(expected_core) != CORE_FILES:
        raise RuntimeError("canonical core inventory mismatch")
    for relative, digest in expected_core.items():
        if sha256(CORE / relative) != digest:
            raise RuntimeError(f"canonical core hash mismatch: {relative}")
    verify_source_manifest("n878851", "n878851_SHA256SUMS.txt")
    verify_source_manifest("eight_index", "eight_index_SHA256SUMS.txt")
    expected = (
        {f"producer_core/{name}" for name in CORE_FILES}
        | {f"task_wrappers/{task}/{name}" for task in ("n878851", "eight_index") for name in WRAPPER_FILES}
        | {"source_manifests/n878851_SHA256SUMS.txt", "source_manifests/eight_index_SHA256SUMS.txt"}
        | NATIVE
    )
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() or p.is_symlink()}
    if actual != expected:
        raise RuntimeError(f"integration inventory mismatch: {sorted(actual ^ expected)}")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_DIRS for part in relative.parts):
            raise RuntimeError(f"forbidden generated directory: {relative}")
        if path.is_symlink() or (path.is_file() and relative.as_posix().lower().endswith(FORBIDDEN_SUFFIXES)):
            raise RuntimeError(f"forbidden artifact: {relative}")
    verify_dependencies()
    n_results = json.loads((WRAPPERS / "n878851/results.json").read_text(encoding="utf-8"))
    e_results = json.loads((WRAPPERS / "eight_index/results.json").read_text(encoding="utf-8"))
    if n_results.get("task") != 1 or e_results.get("task") != 2:
        raise RuntimeError("task wrapper identity mismatch")
    n_body, e_body = dict(n_results), dict(e_results)
    n_body.pop("task")
    e_body.pop("task")
    if n_body != e_body:
        raise RuntimeError("results wrappers differ beyond task identity")
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="a303656_phase_g_squarehit_") as tmp_name:
        temporary = Path(tmp_name)
        source = temporary / "source"
        shutil.copytree(CORE, source)
        normal = temporary / "normal.json"
        optimized = temporary / "optimized.json"
        run([sys.executable, "-B", "reference.py", "--self-test", "--output", str(normal)], source, environment)
        run([sys.executable, "-O", "-B", "reference.py", "--self-test", "--output", str(optimized)], source, environment)
        frozen = json.loads((CORE / "evidence.json").read_text(encoding="utf-8"))
        if json.loads(normal.read_text(encoding="utf-8")) != frozen or json.loads(optimized.read_text(encoding="utf-8")) != frozen:
            raise RuntimeError("normal or optimized evidence replay mismatch")
    evidence = json.loads((CORE / "evidence.json").read_text(encoding="utf-8"))
    if evidence.get("prime_certificates_verified") != 57 or len(evidence.get("variable_base_models", [])) != 4:
        raise RuntimeError("finite certificate/model count mismatch")
    if not all(evidence.get("mutation_tests", {}).values()):
        raise RuntimeError("source mutation controls failed")
    expected_indices = [878851, 2636553, 27244381, 81733143, 625552508473588471, 1876657525420765413, 19392127762681242601, 58176383288043727803]
    if evidence.get("indices") != expected_indices:
        raise RuntimeError("exact eight-index specialization changed")
    bound = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 150000
    n = 878851
    raw_k = (bound - 1) // (2 * n) + 1
    admissible_k = raw_k
    while admissible_k % 10 not in (5, 9):
        admissible_k += 1
    candidate = 1 + 2 * admissible_k * n
    published = evidence["published_bound"]
    if (bound, raw_k, admissible_k, candidate) != (970453984500000, 552115197, 552115199, 970453989512699):
        raise RuntimeError("bounded-gate arithmetic mismatch")
    if published["B"] != bound or published["n878851_min_k_after_bound_and_old_congruences"] != admissible_k or published["corresponding_q_not_asserted_prime"] != candidate:
        raise RuntimeError("bounded-gate evidence mismatch")
    print(json.dumps({
        "status": "PASS", "canonical_source_manifests": 2,
        "canonical_shared_core_files": 8, "exact_duplicate_archives": 1,
        "independent_implementations_claimed": 0,
        "normal_replay": "PASS", "optimized_replay": "PASS",
        "prime_certificates_verified": 57, "variable_base_models": 4,
        "mutation_controls": len(evidence["mutation_tests"]),
        "published_bound": bound, "first_admissible_k": admissible_k,
        "corresponding_integer_not_asserted_prime": candidate,
        "dependency_binding": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
