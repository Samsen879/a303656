import sympy as s,time, math, json
from pathlib import Path
T=s.symbols('T')
out=[]
for h in (3,5,7):
 vals=[]
 for Y in (0,1,2):
  t=time.perf_counter();A=5**(Y*h)
  v=int(s.resultant(T**h-A,(T-2)**h-A,T)); dt=time.perf_counter()-t
  vals.append(v);out.append({'h':h,'Y':Y,'value':str(v),'seconds':dt,'bits':abs(v).bit_length()})
 print(h,'gcd',math.gcd(*vals),'times',[x['seconds'] for x in out if x['h']==h],flush=True)
Path(__file__).with_name('resultant_benchmark.json').write_text(json.dumps(out,indent=2)+'\n')
h=67;Z=s.symbols('Z')
E=sum(s.binomial(h,2*k)*Z**k for k in range((h-1)//2+1))
O=sum(s.binomial(h,2*k+1)*Z**k for k in range((h-1)//2+1))
# Use half-degree symmetry; exact rational remainder then clear denominators.
t=time.perf_counter(); base=s.Poly(Z*O**2,Z,domain=s.QQ).rem(s.Poly(E,Z,domain=s.QQ))
print('half-degree remainder',time.perf_counter()-t,flush=True)
for Y in (7,8):
 t=time.perf_counter(); A=5**(Y*h)
 vv=s.resultant(E,s.Poly(A*A,Z,domain=s.QQ)-base,Z)
 # Degree dropped from h to <=(h-3)/2, so restore power of leading E=h.
 degree=s.degree(s.Poly(A*A,Z,domain=s.QQ)-base,Z)
 v=(-2)**h*vv*h**(h-int(degree))
 assert v.q==1
 v=int(v);print('h67 Y',Y,'seconds',time.perf_counter()-t,'bits',abs(v).bit_length(),flush=True)
 Path(__file__).with_name(f'R67_{Y}.hex').write_text(('-' if v<0 else '')+hex(abs(v))+'\n')
vals=[int(Path(__file__).with_name(f'R67_{Y}.hex').read_text().strip(),16) for Y in (7,8)]
g=math.gcd(*vals);print('h67 gcd bits',g.bit_length(),'gcd',g,flush=True)
Path(__file__).with_name('R67_7_8_gcd.txt').write_text(str(g)+'\n')
