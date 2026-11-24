"""Produce only integer checkable coverage bounds. An unsuccessful LP gives no conclusion."""
import argparse
import gzip
import json
import tempfile
from collections import Counter
from pathlib import Path
from time import monotonic

from paths import HERE, R5
import generate_ajt5_palette_proofs as lp
import verify_ajt5_palette as geom


def roots(r, a, level):
    # Level 0 agrees with R5. Further rows are selected only on failed prefixes.
    pc = [12, 12, 13, 14][level]
    qc = [13, 14, 15, 16][level]
    parent = {5*(5**d+3**c) for d in range(8) if not a >> d & 1
              for c in range(pc+1) if level or (d,c) != (7,12)}
    child = {5**e+3**c-r for d in range(8) if a >> d & 1
             for e in (d,d+1) for c in range(qc+1)}
    return parent | child


def live(ks, x, modulus):
    if modulus == 3:
        return {k for k in ks if (x-k)%3}
    return {k for k in ks if (x-k)%3 or (x-k)%27 in (9,18)}


def strict(tree, ks, groups):
    scale, weights = tree
    w = dict(zip(sorted(ks),weights,strict=True))
    penalty = sum(max(0,max(sum(w[k] for k in g) for g in residues.values())-scale)
                  for residues in groups.values())
    return sum(weights)-penalty > 15*scale


def run(out):
    start = monotonic()
    stats = Counter()
    with gzip.open(R5/"global_all15.jsonl.gz","rt") as source, \
            out.open("wb") as raw, gzip.GzipFile(fileobj=raw,filename="",mtime=0,mode="wb") as dest:
        for r in range(5):
            catalogs = {}
            def catalog(level):
                if level not in catalogs:
                    catalogs[level] = geom.catalogue(roots(r,0,level)|roots(r,255,level))
                return catalogs[level]
            for a in range(256):
                digit,mask,trees = json.loads(next(source))
                if (digit,mask)!=(r,a):
                    raise ValueError("pinned record order")
                if a != a | ((a<<1)&(a>>1)&255):
                    continue
                record = []
                for t in range(3):
                    ks = live(roots(r,a,0),t,3)
                    mode,tree = trees[t+1]
                    if mode == "coarse" and strict(tree,ks,geom.restrict(catalog(0),ks)):
                        record.append("reuse")
                        stats["reuse"]+=1
                        continue
                    splits = []
                    for x in range(t,27,3):
                        for level in range(4):
                            ks = live(roots(r,a,level),x,27)
                            groups = geom.restrict(catalog(level),ks)
                            classes = [(p,v,sorted(g)) for p,rs in groups.items() for v,g in rs.items()]
                            leaf = lp.dual(ks,classes,15)
                            if leaf:
                                break
                        else:
                            # Complete finite non-3 branches if a single strict leaf fails.
                            leaf = lp.solve(ks,classes,15)
                        splits.append([level,leaf])
                        stats["level"+str(level)]+=1
                    record.append(splits)
                dest.write((json.dumps([r,a,record],separators=(",",":"))+"\n").encode())
            print(r,dict(stats),round(monotonic()-start,2),flush=True)
        if source.readline():
            raise ValueError("extra original record")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",nargs="?",type=Path,default=HERE/"regenerated.jsonl.gz")
    output=parser.parse_args().output
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        staged=Path(temp)/"proof.gz"
        run(staged)
        staged.replace(output)
