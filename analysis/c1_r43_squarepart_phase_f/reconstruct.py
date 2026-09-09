import sympy as s, json, math, pathlib, time
P=pathlib.Path(__file__).resolve().parent
out={}
x=s.Symbol('x')
for n in [903,1806]:
 t=time.monotonic();num=den=1
 for d in s.divisors(n):
  mu=int(s.mobius(n//d))
  if mu==1:num*=5**d-1
  elif mu==-1:den*=5**d-1
 N,r=divmod(num,den);assert r==0
 N2=int(s.Poly(s.cyclotomic_poly(n,x),x).eval(5));assert N==N2
 C=N;fs={}
 for q in s.primerange(2,1000001):
  if C%q==0:
   e=0
   while C%q==0:C//=q;e+=1
   fs[str(q)]=e
 rec={'n':n,'phi':str(N),'phi_bits':N.bit_length(),'phi_digits':len(str(N)),'trial_limit':1000000,'trial_factors':fs,'cofactor':str(C),'cofactor_bits':C.bit_length(),'cofactor_digits':len(str(C)),'cofactor_isprime_sympy':bool(s.isprime(C)),'cofactor_is_square':math.isqrt(C)**2==C,'elapsed':time.monotonic()-t}
 out[str(n)]=rec
 print(json.dumps(rec,indent=2),flush=True)
 (P/f'N{n}.txt').write_text(str(N)+'\n')
 (P/f'C{n}_trial.txt').write_text(str(C)+'\n')
(P/'reconstruction.json').write_text(json.dumps(out,indent=2)+'\n')
