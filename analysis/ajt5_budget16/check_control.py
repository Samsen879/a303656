"""Direct arithmetic over every active column and independent R5 JSON CLI replay."""
import json
import subprocess
import sys
import tempfile
from math import gcd, isqrt, prod
from pathlib import Path
from paths import HERE, REPO


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def valuation(residual,p):
    require(residual>0,"valuation requires a positive integer")
    h=0
    while residual%p==0:
        residual//=p
        h+=1
    return h


def explain(residual,palette):
    if residual==0:
        return None
    for p in palette:
        h=valuation(residual,p)
        if h%2:
            unit=p**h
            require(unit%4==3 and residual%unit==0 and gcd(unit,residual//unit)==1,
                    "nonunitary divisor")
            return p,h,unit
    return None


def check(data):
    m,r,qs=(data[k] for k in ("m","r","palette"))
    require(type(m)==int and m.bit_length()==263 and r==4,"control domain")
    require(len(qs)==len(set(qs))==16 and 3 in qs,"palette cardinality")
    require(all(type(p)==int and p>0 and p%4==3 and
                all(p%i for i in range(2,isqrt(p)+1)) for p in qs),"palette primality")
    ps={}
    finite_rows={("parent",d,c) for d in (1,2,3,4,5,7) for c in range(12 if d==7 else 10)}
    finite_rows.update(("child",e,c) for e in (0,1,6,7) for c in range(11))
    finite_rows.add(("child",0,11))
    require(len(finite_rows)==107,"W1 label count")
    # Use the same prime order as the R5 cover for checking the CRT stride.
    byside={"parent":m,"child":5*m+r}
    for side,j,c in sorted(finite_rows):
        residual=byside[side]-5**j-3**c
        atom=explain(residual,qs)
        require(atom is not None,"uncovered W1 atom")
        p,h,_=atom
        ps[p]=max(ps.get(p,0),h+1)
    require(len(ps)==16,"unused control prime")
    step=prod(p**h for p,h in ps.items())
    require(data["crt_modulus"]%step==0 and m%data["crt_modulus"]==data["crt_residue"],
            "CRT does not preserve all odd valuations")
    negatives=[]
    uncovered={}
    counts={}
    first_template={}
    for side,x in byside.items():
        safe={}
        j=0
        totals=[0,0,0]
        while 5**j+1<=x:
            c=0
            units=[]
            while 5**j+3**c<=x:
                residual=x-5**j-3**c
                atom=explain(residual,qs)
                if atom:
                    units.append({"c":c,"u":atom[2]})
                elif j not in safe:
                    safe[j]=c
                c+=1
            if units:
                negatives.append({"side":side,"d":j,"units":units})
            totals[0]+=1
            totals[1]+=c
            totals[2]+=len(units)
            j+=1
        counts[side]=dict(columns=totals[0],active_atoms=totals[1],covered_atoms=totals[2],
                          completely_negative_columns=totals[0]-len(safe))
        uncovered[side]=safe
        template_j=(1,2,3,4,5,7) if side=="parent" else (0,1,6,7)
        first_template[side]=[(j,safe.get(j)) for j in template_j]
    edges=[(d,e) for d in uncovered["parent"] for e in (d,d+1) if e in uncovered["child"]]
    require(edges[0]==(0,0) and (uncovered["parent"][0],uncovered["child"][0])==(1,12),
            "unexpected first surviving edge")
    positives=[]
    for side,c in (("parent",1),("child",12)):
        a,b=data[side]
        require(all(type(t)==int and t>=0 for t in (a,b)) and a*a+b*b+1+3**c==byside[side],
                "false square identity")
        positives.append({"side":side,"d":0,"c":c,"a":a,"b":b})
    record=dict(kind="NO_BRIDGE",m=m,r=r,positive=positives,negative=negatives)
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"candidate.json"
        for pos,expected in ((positives,(1,"REFUTED")),(positives[:1],(3,"PARTIAL"))):
            path.write_text(json.dumps(dict(record,positive=pos),separators=(",",":")))
            sub=subprocess.run([sys.executable,str(REPO/"src/ajt5_integer_certificates.py"),str(path)],
                               capture_output=True)
            got=json.loads(sub.stdout)
            require((sub.returncode,got["status"])==expected,(sub.returncode,got))
            if len(pos)==2:
                require(got["bridge"]==[0,0],"wrong actual edge")
    return dict(bits=m.bit_length(),palette_size=len(ps),W1_covered=len(finite_rows),counts=counts,
                surviving_edges=len(edges),first_actual_edge=[0,0],first_parent_c=1,first_child_c=12,
                first_uncovered_c_by_template_column=first_template,with_both_witnesses="REFUTED/1",
                with_parent_only="PARTIAL/3")

if __name__=="__main__":
    print(json.dumps(check(json.loads((HERE/"control.json").read_bytes())),sort_keys=True))
