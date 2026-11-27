# Moving square-modulus control: actual integer versus half integer

In the [marked square-modulus slice](SQUARE_MODULUS_DIRECTION_SIEVE.md), two explicit direction sets at the same height satisfy the necessary square-modulus direction test. Both reconstructed coordinates can even pass the test of divisibility by the determinant without the factor two. One set yields a true norm triple; the other fails exactly at integrality. No infinitely growing family is asserted.

Take \(X=2^{66}\), \(C=227/200\), \(q=1\), \(p=17\), and \(m=p^2\). With \(w=C/(\log X)^2,\ B=\sqrt Xw,\ H=Bw\), the bounds \(0.69314718<\log2<0.69314719\) give \(4658508<B<4658510\) and \(2526.41<H<2526.42\). Both of the following pass \(H/16\le h\le H/15\), \(B/8\le k\le B/7\), \(H/10\le m\le H\), and the middle-width test:
\[
 \alpha=j/h\in[1/8,1/4],\quad
 \beta=\ell/k\in[7/50,7/25],\quad
 \beta-\alpha\in[1/100,1/20].
\]

~~~python
m = 17**2
cases = [
    ((163,634621,37,159193), ((11,0),(13,2),(11,2)), (19465754364,4365082)),
    ((163,665019,37,167680), ((11,0),(12,2),(12,0)), (20343178339,4321211)),
]
for directions, labels, quotients in cases:
    h,k,j,l = directions
    S = [3**c+5**e for c,e in labels]
    delta,gamma = S[0]-S[1],S[0]-S[2]
    P,D = h*h+k*k,k*j-h*l
    assert D and (2*h*k)%17
    assert (j-2*h)%m == (l-2*k)%m == (2*P-gamma+2*delta)%m == 0
    Na = l*(delta-P)-k*(gamma-j*j-l*l)
    Nb = j*(delta-P)-h*(gamma-j*j-l*l)
    assert (Na,Nb) == tuple(D*z for z in quotients)
    if all(z%2 == 0 for z in quotients):
        a,b = (z//2 for z in quotients)
        Z = [(a,b),(a-h,b+k),(a-j,b+l)]
        n = 94728903003381654953
        assert 2**66 < n < 2**67
        assert all(x*x+y*y+s == n for (x,y),s in zip(Z,S))
    else:
        assert all(z%2 == 1 for z in quotients)
~~~

The second determinant is nonzero, so the uniquely reconstructed coordinates at these prescribed directions are both half-integers. This does not exclude a different set of directions or a different representation of any integer.
