#!/usr/bin/env python3
import json,time,math
from pathlib import Path

if not __debug__:
    raise RuntimeError("Assertions are required; run Python without -O.")


def powers(p,n):
    d={};v=1
    for j in range(n):
        assert v not in d;d[v]=j;v=v*5%p
    assert v==1
    return d

def replay():
    t=time.perf_counter();dp=powers(67**2,1474);qp=powers(20771,10385)
    dyn=[(b,dp[(a-2)%4489]) for a,b in dp.items() if (a-2)%4489 in dp]
    rig=[(b,qp[(a-2)%20771]) for a,b in qp.items() if (a-2)%20771 in qp]
    bins={}
    for b0,b1 in rig:bins.setdefault((b0%67,b1%67),[]).append((b0,b1))
    joint=[]
    def crt(a,b):return (a+22*((b-a)*pow(22,-1,155)%155))%3410
    for a0,a1 in dyn:
        for b0,b1 in bins.get((a0%67,a1%67),[]):joint.append((crt(a0%22,b0%155),crt(a1%22,b1%155)))
    examples=[]
    for rp,rq in [(2,13471),(0,4494)]:
        dc=[[0]*3410 for _ in range(2)];rc=[[0]*3410 for _ in range(2)];uc=[[0]*3410 for _ in range(2)];ov=[[0]*3410 for _ in range(2)]
        vp=vq=1
        for d in range(228470):
            y=d%3410
            for c in range(2):
                a=1+2*c;fp=(rp-a-vp)%4489;fq=(rq-a-vq)%(20771**2)
                dpv=(fp!=0 and fp%67==0);rpv=(fq!=0 and fq%20771==0)
                dc[c][y]+=dpv;rc[c][y]+=rpv;uc[c][y]+=(dpv or rpv);ov[c][y]+=(dpv and rpv)
            vp=vp*5%4489;vq=vq*5%(20771**2)
        sat=[[y for y in range(3410) if uc[c][y]==67] for c in range(2)]
        examples.append({'r67':rp,'r20771':rq,'saturation_sets':sat,'same_lower':sorted(set(sat[0])&set(sat[1])),'minimum_joint_holes':min(134-uc[0][y]-uc[1][y] for y in range(3410)),'saturated_fiber_counts':[{'c':c,'y':y,'dynamic':dc[c][y],'rigid':rc[c][y],'overlap':ov[c][y]} for c in range(2) for y in sat[c]]})
    return {'dynamic_pairs':len(dyn),'rigid_pairs':len(rig),'pointwise_joins':len(joint),'distinct_lower_pairs':len(set(joint)),'same_lower_joins':sum(a==b for a,b in joint),'examples':examples,'seconds':time.perf_counter()-t}
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'results/existing_pair_replay.json');args=ap.parse_args()
    r=replay();assert (r['dynamic_pairs'],r['rigid_pairs'],r['pointwise_joins'],r['distinct_lower_pairs'],r['same_lower_joins'])==(603,5192,693,692,0)
    args.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
