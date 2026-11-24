"""One-command acceptance at the pinned R5 commit. Emits one JSON receipt on success."""
import json
import subprocess
import sys
from time import monotonic

from paths import HERE, PIN, R5, verify_sources
from replay import verify, need
from check_control import check


def checked_cli(name,args,details=True):
    start=monotonic()
    p=subprocess.run(args,capture_output=True,text=True,check=True)
    record=dict(seconds=round(monotonic()-start,3),exit=p.returncode)
    if details:
        record["result"]=json.loads(p.stdout.splitlines()[-1])
    return name,record


def main():
    verify_sources()
    receipt={"pinned_head":PIN}
    start=monotonic()
    proof=verify(HERE/"proof.jsonl.gz")
    receipt["adaptive_16"]={"result":proof,"seconds":round(monotonic()-start,3)}
    start=monotonic()
    receipt["control"]={"result":check(json.loads((HERE/"control.json").read_bytes())),
                        "seconds":round(monotonic()-start,3)}
    for name,args,details in (
        ("without_3",[sys.executable,"-O",str(R5/"global_verify.py"),"--variant","no3_24"],True),
        ("finite",[sys.executable,"-O",str(HERE/"finite.py")],True),
        ("adversarial",[sys.executable,"-O",str(HERE/"tests.py")],False)):
        key,values=checked_cli(name,args,details)
        receipt[key]=values
    need(receipt["finite"]["result"]["upper_m"]>=proof["first_strict_parent"]-1,
         "gap between finite and strict tail")
    receipt["verdict"]="EXCLUDED_AT_MOST_16_DISTINCT_INERT_PRIMES"
    print(json.dumps(receipt,sort_keys=True,indent=2))
if __name__=="__main__":
    main()
