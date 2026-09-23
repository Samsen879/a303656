# Route-scope matrix

`Killed` means ruled out only when every hypothesis in the theorem sheet is
satisfied.

| Feature | Killed? | Not killed / boundary |
|---|---:|---|
| finite states | Conditional | Killed only with the other Q*/Q-dagger hypotheses. |
| fixed finite multipliers | Yes | Q* uses `K>=2`; Q-dagger allows `K>=1` with strict index increase. |
| rational maps | Conditional | Only a uniformly finite bounded-degree chart catalogue. |
| bounded-degree maps | Yes | Within the finite one-source rational-chart model. |
| polynomial maps | Yes | They are special rational charts when degree is uniformly bounded. |
| piecewise maps | Conditional | Finitely many uniformly bounded charts are covered; unbounded pieces are not. |
| arbitrary guards | Yes | Guards only restrict successful chart images; they cannot add witnesses. |
| n-dependent guards | Yes | Even target-set-encoding guards are harmless if the witness maps remain in scope. |
| growing state count | No | The number of states must be fixed and finite. |
| Boolean witness selection | No | Pure support/existence decoders need not be rational charts. |
| nonlinear min/max selection | No | Not generally rational of uniformly bounded finite-chart complexity. |
| unbounded-degree identities | No | Uniform degree D is essential. |
| representation-dependent choice | Conditional | Guards may inspect the propagated witness; free reselection of an unrelated representation is excluded. |
| infinitely many transition families | No | The edge catalogue must be fixed and finite. |
| fixed rational-linear mixed-dilation counting systems | Yes | M/M+ rule out exact finite systems containing F. |
| nonlinear finite functional systems | No | B15--B17 are an explicit finite nonlinear closure. |
| multi-source witness combination | No | Q/Q*/Q-dagger are single-source transition theorems. |
| nonbinary or nonquadratic states | No | Q* is specific to positive-definite binary rational quadratic states. |
| coordinate-dependent index carries | No | Q-dagger permits exponent-dependent, not square-coordinate-dependent, carries. |

Certified phrasing:

> Finite-state, finite-seed, witness-continuous bounded-degree rational lifting
> systems with fixed finite multipliers and the stated positive-definite binary
> quadratic states cannot reach a positive-density set of original integers.

Forbidden overstatement:

> All finite recursion is impossible.
