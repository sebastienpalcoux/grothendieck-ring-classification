# Complete joint integer Gram and cubic domain for R928 and R941

This is a finite necessary-condition calculation, not an associator construction. The separately verified Galois–pseudo-unitary reduction makes the calculation necessary for arbitrary complex categorifications of either source ring.

`source.py` reconstructs each source tensor, its complete distinguished-column domain and all character-compatible symmetric S assignments. There is one surviving low frame and one assignment. All 65 high columns pass the full character eigenvalue algebraic-integrality test. The displayed four-coordinate lifts reproduce every coordinate and every entry of the original seven-coordinate residual Gram matrix. The two rings have the same reduced Gram matrix and the same twenty exact low cubic Verlinde expressions in the basis 1, sqrt(2), sqrt(3), sqrt(6). All distinguished objects and high restriction columns are self-dual; multiplicities of equal restriction columns remain unrestricted nonnegative integers.

For each high column v its multiplicity m_v is a nonnegative integer. The Gram equation is sum m_v vv^t=Q. The unimodular coordinate change recorded in `gram_cubic.json` gives diagonal entries 8,8,13,25. Consequently each m_v is at most the minimum of G_jj/(Tv)_j^2 over nonzero coordinates. These are finite, individually valid bounds, without a rank cutoff. Ten Gram equations and the sixty irrational-coordinate equations of the twenty cubic coefficients are rational linear equations in the 65 multiplicities. Exact rational row reduction, including nonnegative zero-row consequences, expresses all variables in 28 bounded integer free variables. The original multiplicity bounds, nonnegativity, integrality, and nonnegative integrality of all twenty rational cubic values become denominator-cleared linear interval and congruence conditions. All reconstruction formulas and conditions are recorded.

`enumerate.cpp` exhausts that bounded domain with interval propagation and gcd divisibility pruning. Such pruning only rejects boxes whose necessary interval or congruence conditions fail. Every unresolved finite box is partitioned on an integer coordinate until singletons. Python proves a bound for all signed 64-bit intermediates before invoking this engine. The independent Python algorithm in `gram_cubic.py` instead maintains finite sets of allowed values, tests each value against every incident condition, retains holes, and branches in a different order. It uses arbitrary-precision arithmetic. Their complete sorted solutions agree: 1665 native search nodes and 561 independent Python search nodes produce 343 patterns.

Finally every reconstructed pattern is checked directly against all sixteen reduced Gram entries and all four coordinates of all twenty original cubic expressions. The source lift transfers the Gram check to all original entries. All 343 patterns have nonnegative integer cubic coefficients. No rotation or central-invertible orbit assumption is used to obtain this domain. In particular, the common forced multiplicities at canonical indices 40,41,42,43,57 are conclusions of this calculation, available to subsequent structural tests.

Canonical read-only replay (also valid with `python -O`):

```
python evidence/rank8_frontier_20261021/quartic_integer_center/source.py
python evidence/rank8_frontier_20261021/quartic_integer_center/gram_cubic.py
```

The retained 343 patterns are necessary integral center data only. Their existence does not establish a modular category, a categorical center, or a fusion category realizing either source ring.
