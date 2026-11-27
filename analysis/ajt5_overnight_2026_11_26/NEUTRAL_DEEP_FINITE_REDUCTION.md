# Necessary finite reduction for a neutral deep anchor

The [ten-reader unequal-step minimum](https://github.com/Samsen879/a303656/commit/9184510b88d7503367ce0376528be0d1a20f052c) uses a nonneutral anchor at the depth prime. This note narrows the stricter question without deciding it.

In the chart, three shared shallow readers with distinct vertical labels are necessary. Use the five shared patterns \((A\bmod49,u\bmod49)=(31,2),(31,9),(36,17),(36,24),(36,38)\). The stride-31 patterns require the reader 1865431; its base-5 order has 3-part too large for an order-49 step with \(v_3(B)=2\), as the modular check below shows. For the other three, normalize vertical labels by \(v\mapsto BA^{-1}v\bmod343\). This is just a reindexing of the finite phases: the shallow vertical hit classes and the two native residues move together. Deep neutrality forces \(343\mid C\), and the chart also has \(6\mid C\), so the native anchor is neutral modulo \(7^4\).

Lift the normalized \(A,u\) modulo 343. On the native line, the candidates not covered by shallow labels must obey
\[
3^{Au}+5^{Av}=3^{A(u+1)}+5^{Aw}\pmod{2401}.
\]
The check gives 2058 tuples. At a neutral depth reader with primitive step \(z\) of order 343, the vertical step is \(z^k\) for a unit \(k\bmod343\). Dividing the collision equation by \(z^u\) gives
\[
1+z^{kv-u}-z-z^{kw-u}=0.
\]
Every permitted prime therefore divides a resultant between \(\Phi_{343}\) and one of these sparse polynomials. Multiplying by a monomial, scaling the exponents by a unit, and exchanging summands or sides preserve the prime test. There are 9604 raw pairs and 6610 canonical tests. This is a necessary reduction; no exhaustive factoring or sieve conclusion is asserted here.

~~~python
patterns = (
    (17,{33,12,47},{39,11,46}),
    (24,{40,5,26},{46,4,25}),
    (38,{5,40,33},{11,39,32}),
)
assert pow(5,49*9*470,1865431) == 1319802

T = []
for u0,L,R in patterns:
    for a in range(36,343,49):
        A = a+343*((-a)%6)
        g,h = pow(3,A,2401),pow(5,A,2401)
        inv = {pow(h,v,2401):v for v in range(343)}
        assert len(inv) == 343
        for u in range(u0,343,49):
            change = pow(g,u,2401)-pow(g,u+1,2401)
            for v in range((1-u)%7,343,7):
                if v%49 in L:
                    continue
                w = inv[(pow(h,v,2401)+change)%2401]
                if w%49 not in R:
                    T.append((a,u,v,w))
assert len(T) == 2058

def hit(q):
    s = q-1
    while s%7 == 0:
        s //= 7
    z = s
    while z%3 == 0:
        z //= 3
    g,h = pow(3,s,q),pow(5,s,q)
    if (pow(5,343*9*z,q) != 1
            or any(pow(x,343,q) != 1 or pow(x,49,q) == 1 for x in (g,h))):
        return None
    inv = pow(s,-1,343)
    G = [pow(g,inv*i,q) for i in range(343)]
    H = [pow(h,inv*i,q) for i in range(343)]
    return next(((a,u,v,w) for a,u,v,w in T
                 if (G[a*u%343]+H[a*v%343]
                     -G[a*(u+1)%343]-H[a*w%343])%q == 0), None)

assert hit(262739) is None
pairs = {((k*v-u)%343,(k*w-u)%343) for a,u,v,w in T
         for k in range(1,343) if k%7}
assert len(pairs) == 9604

def canonical(a,b):
    P,Q = (0,a),(1,b)
    return min(((p[1-i]-p[i])*t%343,(q[1-j]-p[i])*t%343)
               for p,q in ((P,Q),(Q,P)) for i in (0,1) for j in (0,1)
               if (q[j]-p[i])%7
               for t in (pow((q[j]-p[i])%343,-1,343),))


assert len({canonical(a,b) for a,b in pairs}) == 6610
~~~

## Same-target anchor control

At the known nonneutral attachment the anchor value is 235492 modulo 262739 and has order 383. Replacing it by a neutral anchor while preserving the native and shallow readings opens a local escape in each of the two columns, on the same target. This only rules out the particular neutral attachment and, via the finite check above, neutral use of the same prime in this chart. A different prime remains possible.

~~~python
from math import lcm, prod

Q,d = 3571,262739
P = ((491,33,39),(68699,12,11),(135731,47,46))
L0 = ((6763,5),(119659,26),(190807,40))
L1 = ((430907,18),(434827,25),(472067,32))
base = (Q,*(q for q,v,w in P),*(q for q,v in L0+L1))
D = lcm(18,d*((d-1)//343),
        *(q*((q-1)//(7 if q==Q else 49)) for q in base))
j = 232*pow(D,-1,343)%343
B = D*(j if j%3 else j+343)
A = 4117*B
L = lcm(6*343,*(q*(q-1) for q in base))
C,C0 = 94*d*L,766*d*L

def S(c,u,v,m):
    return (pow(3,c+A*u,m)+pow(5,B*v,m))%m

assert pow(3,C0,d*d) == 1 and pow(3,C,d) == 235492
assert pow(235492,383,d) == 1
assert pow(3,C,7**5) == pow(3,C0,7**5)
assert all(pow(3,C,q*q) == pow(3,C0,q*q) == 1 for q in base)
assert S(C,17,68,2401) == S(C,18,53,2401) == 1479
eq = [(4,3),(243,82),(7**5,S(C,17,1440,7**5)+7**4),
      (Q*Q,S(C,0,1,Q*Q)+Q)]
for q,v,w in (*P,(d,68,53)):
    x,y = S(C,17,v,q*q),S(C,18,w,q*q)
    assert (x-y)%q == 0
    eq.append((q*q,next(x+j*q for j in (1,2) if (x+j*q-y)%(q*q))))
eq += [(q*q,S(C,u,v,q*q)+q)
       for u,T0 in ((17,L0),(18,L1)) for q,v in T0]
M = prod(m for m,_ in eq)
n0 = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq)%M

for u,v,rem in ((17,1440,2710),(18,3483,73248)):
    for c in (C,C0):
        z = (n0-S(c,u,v,243))%243
        w = (n0-S(c,u,v,7**5))%7**5
        assert z and z%81 == 0 and w and w%7**4 == 0
        assert all((n0-S(c,u,v,q))%q for q in base)
    z = (n0-S(C,u,v,d*d))%(d*d)
    assert z and z%d == 0
    assert (n0-S(C0,u,v,d))%d == rem

E = C0+19*A
delta = (n0-4*pow(3,E,M))%M
assert C0-C < A and E > M.bit_length() and 19*4117 >= 2*6173
print(E,delta)  # Common target n = 4*3**E + delta.
~~~
