"""Replay the two frozen R1 engines on their already published 10-million-parent domain."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from paths import REPO

def run():
    with tempfile.TemporaryDirectory() as name:
        out=Path(name)
        for tool,src in (("squares","ajt5_scan"),("valuation","ajt5_valuation_replay")):
            subprocess.run(["g++","-std=c++17","-O3",str(REPO/"src"/(src+".cpp")),
                            "-o",str(out/tool)],check=True)
        for cmd in ([out/"squares","10000000",out/"s"],
                    [out/"valuation","10000000",out/"s",out/"v"]):
            subprocess.run(list(map(str,cmd)),check=True)
        reports=[json.loads((out/d/"summary.json").read_bytes()) for d in ("s","v")]
        frozen=json.loads((REPO/"analysis/ajt5_exact_audit/results/summary.json").read_bytes())
        for data in [*reports,frozen]:
            if (data["max_m"],data["max_n"],data["cases"],data["combined_failures"],data["vacuous"])!=(
                10000000,50000004,49999995,[0]*5,[0]*5):
                raise ValueError("finite bridge replay failed")
        print(json.dumps(dict(upper_m=10000000,pairs=49999995,actual_bridge_misses=0,
                              independent_table_entries=50000005,
                              D_sha256=hashlib.sha256((out/"s/masks.u16le").read_bytes()).hexdigest())))
if __name__=="__main__":
    run()
