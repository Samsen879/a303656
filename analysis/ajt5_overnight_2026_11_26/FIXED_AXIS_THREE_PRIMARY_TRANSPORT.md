# Three-primary transport across a fixed-axis phase

Fix \(c=C_*(n)\) at all unit primes and fix the parity of \(d\), as in [exact norm allocation](FIXED_AXIS_NORM_ALLOCATION.md). At an earlier inert \(p>3\), call a test **hard on this parity** when its potential collision class modulo \(\operatorname{ord}_p(5)\) has strict odd valuation below \(w_p=v_p(5^{\operatorname{ord}_p(5)}-1)\). Other tests need not ban any lower exponent class: when a zero ball is encountered, use the prime's own unused coordinate to move into an even valuation shell. This works at arbitrary \(w_p\) by choosing the appropriate lift depth.

For the growing 3-axis, the normalized 3-test is \(n-5^d\). When the chosen parity collides, its allowable \(d_3\) are exactly the finite odd-distance shells around a root \(\alpha\in\mathbb Z_3\), because \(w_3=1\). They meet exactly seven classes modulo 27: the six classes where \(v_3(d_3-\alpha)=1\) and the one class where deeper odd distances are still available. If the chosen parity does not collide, every class is allowed.

Suppose every earlier hard test has order a power of 3 or twice a power of 3. Such a test needs at least three 3-primary digits: at depths one or two the only inert candidate primes are \(7,31,19,5167\), and each base 5 is ordinary there. The list follows by factoring \(5^{18}-1\) and checking the orders; the replay includes this. Each hard row therefore forbids at most one of the seven projected classes. If the terminal \(q>5\) reads \(a=v_3(\operatorname{ord}_q(5))=2\), avoid its first collision by forbidding its one class modulo 9, at most three of the projected classes. Hence at most three hard rows cannot exhaust the options. If \(a\ge3\), its forbidden slice hits at most one such class, so at most five hard rows still cannot exhaust the options. If normalized 3 gives a unit, the same counts work with even more choices. Select a surviving 3-primary phase, then solve all repairable old tests in increasing order, leaving this chosen digit fixed. The terminal remains a unit because that digit differs from its root class; no newly assigned other primary digits can reverse this. At the nonsplit unit primes keep the finite phase of \(c=C_*(n)\) as \(c\) grows. This proves that in the specified cases \(q\) cannot be the first growth-box blocker.

The proof does not treat an arbitrary terminal lacking that 3-depth, nor a mixed-order hard core. In particular, just knowing that every direct 3-reader is ordinary is insufficient to guarantee transport with other variables frozen: repairing one such prime can move a digit read at a later place. The explicit same-\(n\) control below has a route \(3\to31\to20771\). On the frozen route, normalized 3 requires \(d=5\bmod6\), after which the old 31 test forces \(d=28\bmod31\) for any passing phase. Freezing \(d=1\bmod335\) then forces \(d=3686\bmod10385\) and leaves a genuine valuation-one failure at 20771. Releasing the split coordinate at 5 gives a phase passing all the displayed conditions at the same integer. Moreover \(d=1\) gives an actual fixed-axis integer witness. The terminal example is base-5 Wieferich but ordinary in base 3, so this is a countercontrol to frozen transport, not a common Wieferich blocker or an all-exponent obstruction.

~~~python
from math import isqrt
def prime(p):
    return p>=2 and all(p%j for j in range(2,isqrt(p)+1))
x=5**18-1
ls=(2,3,7,19,31,829,5167)
seen=[]
for p in ls:
    if x%p==0: seen.append(p)
    assert prime(p)
    while x%p==0: x//=p
assert x==1 and tuple(seen)==ls
assert all(pow(5,p-1,p*p)!=1 for p in ls if p>3 and p%4==3)
assert {v for v in range(27) if v%3==0 and (v==0 or v%9!=0)}=={0,3,6,12,15,21,24}

N,q=41793953874131,20771
assert N==6+4518506**2+4623533**2 and N%108==11
assert [d for d in range(2,93,3)
        if (N-1-pow(5,d,31**2))%31**2==0]==[59]
assert 34841%6==5 and 34841%10385==3686
assert 3686%31==28 and 3686%335==1
assert pow(5,10385,q*q)==1
assert (N-1-pow(5,3686,q*q))%(q*q)==q
d=508397
assert d%67==1 and d%5==2
assert (N-pow(5,d,27))%27==18
assert (N-1-pow(5,d,31**3))%31**3==6*31**2
assert (N-1-pow(5,d,q))%q==7950
~~~
