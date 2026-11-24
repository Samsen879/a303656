import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = "8122d1d9b9d3f6cdcd2c4829bfa5a2965087d5d4"
REPO = Path(os.environ.get("A303656_REPO", HERE.parents[1])).resolve()
R5 = REPO / "analysis/ajt5_frontier"
sys.path[:0] = [str(R5), str(REPO / "src"), str(REPO / "scripts")]


def verify_sources():
    manifest = json.loads((HERE / "upstream.json").read_bytes())
    if manifest["commit"] != PIN:
        raise ValueError("unexpected repository pin")
    for name, expected in manifest["sha256"].items():
        if hashlib.sha256((REPO / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"pinned input changed: {name}")
