# Countermodels — exact finite certificates

**Every square-hit fixture in this file has variable base b != 5. None is an actual base-5 B31^odd member.** All terminal prime labels are certified. A base is claimed prime only where explicitly marked and accompanied by its own complete Lucas certificate.

Rows list all admitted vertices >3, not a chosen favorable path. Terminal3 is checked separately and is excluded from the all-odd quantifier. Orders are factored completely; all order factors are expanded. See `verify.py` for actual modular equalities and inequality checks.

## CM1: odd_antichain_prime_base_same_first_order_as_5

Base: `171647557511869913`.
Base primality: CERTIFIED PRIME.
Root q: `878851` (CERTIFIED PRIME).
Proper state R: `31`.
Maximal generators: `31`; symbol product = `-1`.

| x | exact order ord_x(b) | exact s_x(b) | (b^order−1)/x^s modx |
|---|---|---:|---|
|31|3|1|4|
|878851|93|2|688101|

All rows have odd squarefree orders and labels 11 or19 mod20. All proper valuations are1; root valuation is exactly2. Basal gateway is31 and absolute terminal set is{3}.

### Construction receipt

```json
{
  "preserved_modulus": "34596",
  "original_base": "5",
  "q_order_at_base5": 93,
  "q_valuation_at_base5": 1,
  "base5_first_lift": 482192,
  "hensel_digit_in_Mq_parameter": 372317,
  "least_lifted_base": "11320197560067137",
  "progression_modulus": "26721226658633796",
  "progression_step": 6
}
```

### Complete admitted edge signs

|upper x|lower p|(p/x)|(x/p)|
|---|---|---:|---:|
|878851|31|-1|1|

Terminal3 sanity: order `2`, valuation `1`. This is not an all-odd basin row.

## CM2: odd_antichain_prime_base_also_preserves_mod8

Base: `679350864025912037`.
Base primality: CERTIFIED PRIME.
Root q: `878851` (CERTIFIED PRIME).
Proper state R: `31`.
Maximal generators: `31`; symbol product = `-1`.

| x | exact order ord_x(b) | exact s_x(b) | (b^order−1)/x^s modx |
|---|---|---:|---|
|31|3|1|4|
|878851|93|2|258873|

All rows have odd squarefree orders and labels 11 or19 mod20. All proper valuations are1; root valuation is exactly2. Basal gateway is31 and absolute terminal set is{3}.

### Construction receipt

```json
{
  "preserved_modulus": "69192",
  "original_base": "5",
  "q_order_at_base5": 93,
  "q_valuation_at_base5": 1,
  "root_first_order_equals_base5": true,
  "progression_modulus": "26721226658633796",
  "progression_step": 25,
  "least_lifted_base": "11320197560067137"
}
```

### Complete admitted edge signs

|upper x|lower p|(p/x)|(x/p)|
|---|---|---:|---:|
|878851|31|-1|1|

Terminal3 sanity: order `2`, valuation `1`. This is not an all-odd basin row.

## CM3: even_antichain_preserves_actual_base5_proper_fork

Base: `1350023785140158092883340475528516436875931205172071528190123096670135643660145755075064632416931265897037`.
Base primality: NOT CLAIMED.
Root q: `269386049336015633650142291` (CERTIFIED PRIME).
Proper state R: `31, 878851, 625552508473588471`.
Maximal generators: `878851, 625552508473588471`; symbol product = `1`.

| x | exact order ord_x(b) | exact s_x(b) | (b^order−1)/x^s modx |
|---|---|---:|---|
|31|3|1|4|
|878851|93|1|482192|
|625552508473588471|31|1|7444|
|269386049336015633650142291|549767447624521701326821|2|130222063101795507307343065|

All rows have odd squarefree orders and labels 11 or19 mod20. All proper valuations are1; root valuation is exactly2. Basal gateway is31 and absolute terminal set is{3}.

### Construction receipt

```json
{
  "preserved_modulus": "20912883901584879224794156591848213255477959618308872",
  "k": 245,
  "primitive_generator_mod_q": 2,
  "u_mod_q": "36235251261554175769160502",
  "teichmuller_mod_q2": "36168597231657426563646041866203695179643536039458102",
  "regular_comparator_base": "1350023785140158092883340481162155611346642593324455357896588605349747778813287453669295613265722853602789",
  "root_base5_full_order_residue": "253604702715415814708233056",
  "terminal_first_order_equals_base5": false
}
```

### Complete admitted edge signs

|upper x|lower p|(p/x)|(x/p)|
|---|---|---:|---:|
|878851|31|-1|1|
|625552508473588471|31|-1|1|
|269386049336015633650142291|878851|-1|1|
|269386049336015633650142291|625552508473588471|-1|1|

Terminal3 sanity: order `2`, valuation `1`. This is not an all-odd basin row.

**Scope warning:** the proper fork is genuinely base-5 arithmetic and is preserved modulo each proper p². The root first-order residue is NOT base5: the stored base5 full-order test is non1. Thus this is not even a claim that this q is a base-5 terminal of the displayed order.

## CM4: three_generator_fork_variable_base

Base: `218558218469020391329099872509045738369759259821`.
Base primality: NOT CLAIMED.
Root q: `603442975211` (CERTIFIED PRIME).
Proper state R: `31, 311, 2791, 3659`.
Maximal generators: `311, 2791, 3659`; symbol product = `-1`.

| x | exact order ord_x(b) | exact s_x(b) | (b^order−1)/x^s modx |
|---|---|---:|---|
|31|3|1|4|
|311|31|1|84|
|2791|31|1|1975|
|3659|31|1|659|
|603442975211|3176015659|2|378406989957|

All rows have odd squarefree orders and labels 11 or19 mod20. All proper valuations are1; root valuation is exactly2. Basal gateway is31 and absolute terminal set is{3}.

### Construction receipt

```json
{
  "crt_congruences": [
    [
      "5",
      "72"
    ],
    [
      "5",
      "961"
    ],
    [
      "260",
      "96721"
    ],
    [
      "1627",
      "7789681"
    ],
    [
      "994",
      "13388281"
    ],
    [
      "250071273181958004816727",
      "364143424331503560494521"
    ]
  ],
  "period": "254152055223982380150537905186158168830878593992",
  "k": 95
}
```

### Complete admitted edge signs

|upper x|lower p|(p/x)|(x/p)|
|---|---|---:|---:|
|311|31|-1|1|
|2791|31|-1|1|
|3659|31|-1|1|
|603442975211|311|-1|1|
|603442975211|2791|-1|1|
|603442975211|3659|-1|1|

Terminal3 sanity: order `2`, valuation `1`. This is not an all-odd basin row.

**Scope warning:** relays311,2791,3659 have order31 at this variable base, NOT as new members of the base-5 first-relay list.

## CM5: transitive_edge_same_first_order_as_5

Base: `5275760879018030027320257731708765`.
Base primality: NOT CLAIMED.
Root q: `490398859` (CERTIFIED PRIME).
Proper state R: `31, 878851`.
Maximal generators: `878851`; symbol product = `-1`.

| x | exact order ord_x(b) | exact s_x(b) | (b^order−1)/x^s modx |
|---|---|---:|---|
|31|3|1|4|
|878851|93|1|482192|
|490398859|81733143|2|312378920|

All rows have odd squarefree orders and labels 11 or19 mod20. All proper valuations are1; root valuation is exactly2. Basal gateway is31 and absolute terminal set is{3}.

### Construction receipt

```json
{
  "preserved_modulus": "53442453317267592",
  "base5_first_lift": "183120337",
  "hensel_digit_in_Mq_parameter": "201302545"
}
```

### Complete admitted edge signs

|upper x|lower p|(p/x)|(x/p)|
|---|---|---:|---:|
|878851|31|-1|1|
|490398859|31|-1|1|
|490398859|878851|-1|1|

Terminal3 sanity: order `2`, valuation `1`. This is not an all-odd basin row.

## Regular comparators and tame tests

For each model, a comparator base is supplied or formed as b+Mq, with M=8*9*product(p² for p in R). It has the same proper modulo-p² data and root modulo-q data, but the verifier proves its root valuation is1. All tested prime-to-q power predicates agree; the q-th-power predicate moduloq² distinguishes them. G2 proves the prime-to-q statement for every allowed index and precision, beyond the finite tests.

## Actual base-5 regular first-order countermodel

The inherited closure `{31,878851,490398859}` has three admitted edges and total lower-over-upper Legendre product−1. All vertices are regular. This refutes an acyclic-implies-positive-edge-product statement, not a theorem restricted to actual base-5 nonregular roots.

## No original problem counterexample

Changing b changes the arithmetic problem. No fixture disproves F1, F2, F4, B31^odd emptiness, exactly-seven, or the original additive representability statement.
