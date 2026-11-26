# A sharp three-label limit for one common primitive projection

Suppose p is odd and divisible by 41. Require that all the norms \(5p^2+K\), for distinct actual labels \(K=10942-5^e-3^f\), share the same integral projection \(H=v\cdot z\) for a single primitive integer direction \(v=(s,t)\). If \(K=10940,10928\) are included, at most one further distinct K can occur. This is sharp by [the actual three-label Pell family](JOINT_TRIPLE_AND_CROSS_BASE_PELL_ORBITS.md). The bound is across all directions, and does not require \(K\ge0\).

## Reducing to seven slots

Set \(A=s^2+t^2\) and \(w=\det(v,z)\). Any two points with the common projection differ by an integer multiple of \((t,-s)\), since v is primitive, so use \(w_j=w_0-jA\). Reverse the index direction if needed so the prescribed second label is at \(d>0\). Then
\[
 d(2w_0-dA)=12,\quad
 U_j:=10942-K_j=2+(12/d)j+Aj(d-j),\quad
 H^2-5Ap^2=10940A-w_0^2 .
\]
The two prescribed norms differ by 4 modulo 8, so \(4\nmid d\): a shift by a multiple of 4 in both coordinates preserves their sum of squares modulo 8. Thus \(d=1,2,3,6\). A primitive sum of two squares gives \(A\equiv1,2,5\bmod8\). For odd d, \(w_0=(dA+12/d)/2\) requires A even. For even d, \(A\equiv5\bmod8\) gives \(w_0\equiv0\bmod8\) and the Pell equation forces \(H^2\equiv5\bmod8\) since p is odd. Hence only 1 or 2 remain.

Since \(U_j\ge2\), one has \(0\le j\le d+12/(dA)\). Any \(j>d\) requires \(A\le12\), which makes \(A=1,2,10\) the only primitive possibilities left. The finite check below shows that no such j gives a new label and a possible Pell anchor modulo both 25 and 41. The sign condition, parity of \(U_j\), and the congruence \(A\bmod8\) leave only the following interior slots:
* \(d=2\), A even: \(j=1\), \(U_j=8+A\).
* \(d=3\), A even: \(j=1,2\), \(U_j=6+2A,10+2A\).
* \(d=6\), A odd: \(j=2,4\), \(U_j=6+8A,10+8A\).
* \(d=6\), A even: \(j=1,2,3,4\), \(U_j=4+5A,6+8A,8+9A,10+8A\).

In the last case \(j=5\) would give \(12+5A\equiv6\bmod8,\ 2\bmod5\). For \(e=0\) the second congruence forces \(f\equiv0\bmod4\) and gives 2 modulo 8. For \(e>0\) it forces \(f\equiv3\bmod4\) and gives 0 or 4 modulo 8. Thus it is excluded. Counting distinct formulas across the table gives seven, so a specified additional label needs at most seven candidate lengths A, with Pell and integrality still to check.

## A finite modular certificate and the exact last step

The modular certificate below (modulus \(16\cdot3\cdot25\cdot13\cdot41\)) includes every nonnegative power, by closing each residue orbit from exponent zero up to its first repetition. For every feasible A class after the 25 and 41 anchor tests, it leaves no simultaneous pair of interior slots for \(d=3\) or \(d=6\), A odd. For \(d=6\), A even, any remaining pair has exactly slots \(2,4\) and \(5\mid A\).

In that exceptional class the larger cost \(10+8A\) is 0 modulo 5, so it must be \(1+3^f\) with \(f\equiv2\bmod4\). The smaller cost \(6+8A\) is 1 modulo 5, forcing its other label's exponent of 5 to be positive (if zero, the remaining power of 3 would vanish modulo 5). The smaller cost is \(3^f-3\), divisible by 3, so its exponent of 3 must be zero. Consequently \(3^f=5^e+4\) with \(e>0\). The odd factors \(3^{f/2}-2\) and \(3^{f/2}+2\) are coprime (their difference is 4), and their product is \(5^e\). The lower factor must therefore be 1, giving \(f=2,e=1\), which would make \(A=0\). This closes the only remaining pair. No inference is made about a second direction or arbitrary two-square representations at the same point.

~~~python
from math import isqrt
def powers(b,M):
    x,S=1,set()
    while x not in S:
        S.add(x)
        x=x*b%M
    return S
sq25={x*x%25 for x in range(25)}
sq41={x*x%41 for x in range(41)}
def base(A,d):
    return 10940*A-((d*A+12//d)//2)**2
def at25(A,d):
    return any((base(A,d)+5*A*p*p)%25 in sq25 for p in range(25))
def cost(A,d,j):
    return 2+12*j//d+A*j*(d-j)
small={5**e+3**f for e in range(5) for f in range(7)}
for d in (1,2,3,6):
    for A in (1,2,10):
        if (d*A+12//d)%2:
            continue
        for j in range(d+1,d+12//(d*A)+1):
            U=cost(A,d,j)
            assert U<3**7 and U<5**5
            if U in small and U not in (2,14):
                assert not at25(A,d) or base(A,d)%41 not in sq41

M=16*3*25*13*41
S={(x+y)%M for x in powers(3,M) for y in powers(5,M)}
for d,r,slots in [(3,2,(1,2)),(6,1,(2,4)),(6,2,(1,2,3,4))]:
    ok={A for A in range(50) if (d*A+12//d)%2==0 and at25(A,d)}
    for A in range(r,M,8):
        if A%50 not in ok or base(A,d)%41 not in sq41:
            continue
        js=[j for j in slots if cost(A,d,j)%M in S]
        if len(js)>=2:
            assert (d,r,js,A%5)==(6,2,[2,4],0)
~~~
