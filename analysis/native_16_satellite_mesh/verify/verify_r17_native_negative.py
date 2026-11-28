"""Two actual integral, primitive, noncritical carrier chords at one target n.
Usage: python3 -I -B verify_r17_native_negative.py [directory]
"""
import hashlib,json,sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent
w=json.loads((p/'r17_native_negative.json').read_text())
raw=(p/w['source']).read_bytes();c=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()==w['source_sha256']=='77d913c4ea3dd0dd69ee136d801f846efd492d2b67bbe43172ad50c209380638'
L=c['L'];assert L==w['L']==128
A,B=9**L,25**L;D,E=12*B-3*A,A+10*B;h=D-5;H=3*A+25*B;C=5+3*h-E
y=w['y'];assert y>0 and y%10==0
assert hashlib.sha256(str(y).encode()).hexdigest()=='5c55b483da5a366032e5f092bc2869f892dc2f8d94bfea2fcd28921da48de9f5'
t,rem=divmod(5*y*y-h*y+C,10);assert rem==0
P=(h-3*t,t);S=P[0]**2+P[1]**2;n=S+H;K=S.bit_length()-1
assert n==w['n'] and K==w['actual_K']==11906
assert (25*B)**16<=n<=A**32
assert w['anchor_label']==[2*L+1,2*L+2]
assert w['edge_labels']==[[2*L+2,2*L],[2*L,2*L+1]]
assert S+3**w['anchor_label'][0]+5**w['anchor_label'][1]==n
Qs=((P[0]+1,P[1]+3),(P[0]+3-y,P[1]-1-3*y))
native_qs=[]
for edge,pack in enumerate(c['packs']):
 x,z=Qs[edge];gap=(D,E)[edge];lab=w['edge_labels'][edge]
 assert x*x+z*z==S+2*gap
 assert x*x+z*z+3**lab[0]+5**lab[1]==n
 assert all(a!=b for a,b in zip(lab,w['anchor_label']))
 for m,b,root,norm in pack:
  assert norm==m*m+b*b
  assert (m*x-b*z)%norm==(b*x+m*z)%norm==0
 m,b,root,norm=pack[0];cw=w['carriers'][edge]
 assert (m,b,norm)==(cw['m'],cw['b'],cw['norm'])
 u,v=(m*x-b*z)//norm,(b*x+m*z)//norm
 R=(m*u-b*v,b*u+m*v);dx,dz=R[0]-P[0],R[1]-P[1]
 assert R[0]**2+R[1]**2==x*x+z*z
 assert dx%2==dz%2==1 and gcd(dx,dz)==cw['chord_gcd']==1
 q=(dx*dx+dz*dz)//2;det=dx*P[1]-dz*P[0]
 assert q==cw['q'] and det%2==0
 native_qs.append(q)
 assert 2*q*S==(gap-q)**2+det*det
 assert 64*K*K*q>S
 assert F(1068,1000)<F(64*K*K*q,S)<F(1069,1000)
 print('edge',edge+1,'gcd=1; actual 64*K^2*q/S=',float(F(64*K*K*q,S)))
assert len(set(native_qs))==2
print('PASS same n; both axes change; all 36 factors load; ordinary height; two native primitive noncritical chords')
print('K_actual=',K,'n bits=',n.bit_length(),'n decimal digits=',len(str(n)))
