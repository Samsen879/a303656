# Component-wise release of shared order digits and an actual lock

**A shared-order component can be eliminated when its exact safe digits cover every permitted boundary phase.** Opening one digit works on the pinned depth-four circuit with one active neighbouring reader. A second actual reader can close the only escape, even when the anchor is chosen adaptively. The replay checks both cases on the same \(3,5\) orders. [Pinned circuit](https://github.com/Samsen879/a303656/commit/15d8441dd555d8e5ddd517bfc790b435b00c8280) · [Known order inventory](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md#3-exact-selected-cyclotomic-arithmetic)

### Component rule

Assign each row a control digit it reads. Draw \(j\to i\) when row \(j\) reads the digit assigned to row \(i\). Delete strongly connected components in topological order and restore them in reverse. At restoration, a component’s control digits are invisible to the rows already restored. The required local certificate is that **for every permitted boundary phase, some joint assignment of the component’s digits passes all its exact tests**. If a neighbouring row reads a proposed free digit and its phase may change, include its acceptance test in the joint assignment.

For one base-\(\ell\) digit, fix the other digits and write the candidate exponents as \(d_j=d_*+Lj\), \(0\le j<\ell\), using a CRT step that changes only that digit. At an odd reader \(q\ne\ell\), either the residual is constant at the tested depth or there is at most one prime-level collision. In the varying case \(5^L\bmod q\) has order a positive power of \(\ell\), so the \(\ell\) candidate values are distinct. Count that collision as forbidden only if its valuation is odd below the tested depth. Thus, if the constant rows pass and fewer than \(\ell\) distinct digits are forbidden, the component lifts. Testing the union of actual forbidden digits gives the exact one-digit criterion.

At \(q=\ell\), a principal digit can instead **force** a choice. If the first motion has depth \(k\) and the residual is zero modulo \(q^k\), the coefficient at depth \(k\) varies linearly. All digits except the unique deeper cancellation have exact valuation \(k\). For odd \(k\) only that cancellation can pass, and its parity must be checked at the actual precision.

### Same circuit, two boundary outcomes

Use the original rows \(q_0=1783,\ q_1=5023,\ q_2=11419697846380955982026777206637491\). The neighbouring readers \(271,4159\) both have order 27. With \(P\) the product of these primes and \(19\), write
\[
d=18P(u+3v),\qquad u,v\in\{0,1,2\}.
\]
Opening \(u\) releases one lower ternary digit of the old \(d\equiv0\bmod54P\) anchor. The exact phase at \(19\) stays fixed.

| Digit \(u\) | First target | Countercontrol |
|---:|---|---|
| 0 | One circuit row rejects at exact valuation one, determined by \(v\) | Same |
| 1 | \(271\) rejects at exact valuation one | Same |
| 2 | All rows pass | \(4159\) rejects at exact valuation one |

The targets differ only modulo \(4159^2\). At the first target, choosing \(u=2\) works for every upper digit \(v\). At the countercontrol, the neighbours only admit \(u=0\), where the circuit rejects every \(v\). Releasing just the \(1783\)-primary exponent digit then gives exact valuation two at \(1783\) while preserving the other rows modulo their squares. The countercontrol is an obstruction on the frozen anchor, with no whole finite-modulus obstruction established.

```python
from math import gcd, isqrt, lcm, prod

q0,q1,q2 = 1783,5023,11419697846380955982026777206637491
r,s,h = 271,4159,19
Q,R = (q0,q1,q2),(r,s)
chain = (1838773,871578403,1770336106919153,584210915283320491,
         143715885159696840787,q2)
for q in (q0,q1,r,s,h,chain[0]):
    assert all(q%i for i in range(2,isqrt(q)+1))
for p,q in zip(chain,chain[1:]):
    assert p*p>q and (q-1)%p==0 and pow(2,q-1,q)==1
    assert gcd(pow(2,(q-1)//p,q)-1,q)==1

for q,b in zip(Q+R,(162,162,81,27,27)):
    assert q%4==3 and pow(5,b,q)==1
    assert all(pow(5,b//ell,q)!=1 for ell in (2,3) if b%ell==0)

P = prod(Q+R+(h,))
c = 27*lcm(11,31,70491962014697259148313439547145)*P
A = 18*P
assert c%2 and all(pow(5,9*A,q*q)==1 for q in Q+R)
assert all(pow(5,3*A,q*q)==1 for q in R)
assert pow(5,A,h*h)==1

def target(block_second):
    pairs = [(9,24),(pow(3,c,h*h),h*h)] + [(q,q*q) for q in Q]
    for t,q in enumerate(R,1):
        m = q*q
        a = pow(3,c,m)
        if t==1 or block_second:
            a = (a+pow(5,A*t,m)+q)%m
        pairs.append((a,m))
    M = prod(m for _,m in pairs)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M

def rem(n,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

good,bad = target(False),target(True)
assert all(good%m==bad%m for m in (24,*(q*q for q in Q+(r,h))))
assert all(bad%q for q in R)
for n in (good,bad):
    for u in range(3):
        for v in range(3):
            d = A*(u+3*v)
            expected = [(q0,q2,q1)[v]] if u==0 else (
                [R[u-1]] if u==1 or n==bad else [])
            assert [q for q in Q+R if rem(n,d,q)==0]==expected
            assert all(rem(n,d,q*q)==q for q in expected)
            assert rem(n,d,h*h)==h*h-1 and rem(n,d,4)==1 and rem(n,d,3)

# Same countercontrol target. Release only the 1783-primary digit.
L = 162*(P//q0)
assert all(pow(5,L,q*q)==1 for q in (q1,q2,r,s,h))
a = (pow(5,L,q0*q0)-1)//q0
assert rem(bad,0,q0*q0)==q0 and a%q0
d = L*pow(a,-1,q0)
assert rem(bad,d,q0*q0)==0
if rem(bad,d,q0**3)==0:
    d += L*q0
assert rem(bad,d,q0**3) in range(q0*q0,q0**3,q0*q0)
assert all(rem(bad,d,q) for q in (q1,q2,r,s,h))
print('OK')
```

The period checks extend the nine-cell replay to every lift of the frozen anchor at the stated finite depth. The released-primary result certifies the listed norm tests only.

If several rows are assigned the same physical digit, each reads the common digit and they are in the same dependency component. A valid one-digit step here is a true CRT variation, keeping the residue periods on the other primary coordinates fixed, not merely an arithmetic progression chosen with no regard to those periods. The row-1783 release after the frozen failure makes it explicit that the nine-cell lock is not a whole-panel norm obstruction.
