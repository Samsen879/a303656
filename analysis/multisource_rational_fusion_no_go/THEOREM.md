# MF-R: full-product multi-source rational fusion no-go

Fix a **fixed finite source number** `k >= 1` and rational constants
`A_1,...,A_k,T`. Let the **full generic independent product** have coordinate
ring

```text
R = Q[X,a_1,b_1,...,a_k,b_k]/(a_j^2+b_j^2-X+A_j : 1<=j<=k),
K = Frac(R).
```

The output coefficient field is the **original Q-function field** `K`:
`U,V in K`. The target is the **monic linear residual** `X-T`.

> **MF-R.** The identity `U^2+V^2=X-T` holds in `K` for some `U,V in K`
> if and only if `T` belongs to `{A_1,...,A_k}`.

Repeated offsets, arbitrary rational degree and poles, and dependence on every
source coordinate are permitted. For `T=A_j`, take `U=a_j,V=b_j`.

The exact proof is [PROOF.md](PROOF.md). The scope and escape examples are in
[SCOPE.md](SCOPE.md). This is a theorem about rational identities on the full
product, not a theorem about integer witness density or arithmetic selection.
