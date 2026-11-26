# A local restriction for positive residue 26 in the plus-sign quartic

Use the real square-difference family $(d,2;d+1,3)$ with $d=8+6j$, $j\ge0$. Write $A=5^d-131770$, $B=A-4$, $H=r+A/r-4$, $m=H/2$, $Z=rt^2+2$, and $w=(Z^2+m^2+B)/H$ for rational parameters with $rH\ne0$. Suppose $w$ is integral and the proposed child $5(w^2-B)$ is a sum of two integer squares. Then the following is necessary for $w\equiv2\bmod3$:
$$
 (v_3(r),H\bmod9,t\bmod3)\in
 \{(0,3,0),(1,3,0),(1,6,1),(1,6,2)\}.
$$
In particular $v_3(H)=1$ in every case. This is a local restriction only, and does not establish sufficiency at the other primes.

Indeed $w^2-B=(w-m)^2+Z^2$. At 3 an integral sum of two rational squares forces each coordinate to be integral at 3, since the valuation of a nonzero sum is twice the smaller coordinate valuation. Hence $m,Z$ are integral at 3. As $A\equiv6\bmod9$, the condition on $H$ forces $v_3(r)$ to be 0 or 1: otherwise one of $r,A/r$ has a unique pole. The condition on $Z$ then forces $t$ to be integral at 3.

If $H$ is a unit, the unit among $r,A/r$ is $2\bmod3$ and $H\equiv1\bmod3$. Then $Z^2\equiv1\bmod3$, $m^2\equiv1\bmod3$ and $B\equiv2\bmod3$, so $w\equiv1\bmod3$. If $3\mid H$ and $r$ is a unit, then $r\equiv1\bmod3$ and $t$ must be zero modulo 3 to make the numerator divisible by 3. Its numerator is then $6\bmod9$. If instead $v_3(r)=1$, the condition $3\mid H$ gives $r/3\equiv2\bmod3$. The numerator is $6\bmod9$ when $t=0\bmod3$ and $3\bmod9$ otherwise. Thus in the exceptional cases the numerator has valuation exactly one, and dividing by $H$ gives precisely the displayed restrictions.

For the factorization-free construction in CYCLOTOMIC_VARIABLE_SLOPE_FAMILY.md, $H=(5^{d-1}-1)/73$ is a 3-adic unit. No choice of its parameter $t$ can produce the positive target residue 26 modulo 30 with these norm conditions. Other denominator profiles are left open.
