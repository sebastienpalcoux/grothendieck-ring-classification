# Complete finite parameter table for generalized near-group source dimensions

This extends the proof and six-case computation in
`../quadratic/RESIDUAL_QUADRATIC_SEARCH.md` and `rank_two_and_models.py` to
all34 original rank-eight frontier rings. It does not identify a fusion
category from a dimension match.

Let a generalized near-group source have an invertible group of order
G=ls, one orbit of l noninvertible simples, stabilizer order s, and total
noninvertible coefficient K. Their common FP dimension d obeys
d^2=s+Kd. The source global dimension is l(s+d^2). After an arbitrary
positive integer dimension multiplier k, a quadratic target D must obey

    Trace(D) = kl(4s+K^2),
    Norm(D)  = k^2 l^2 s(4s+K^2),
    Norm(D)/Trace(D) = kG.

Consequently G_D=Norm(D)/Trace(D) must be a positive integer. Every
possible k divides G_D, every possible s divides G_D/k, l=G_D/(ks), and
K^2=Trace(D)/(kl)-4s is uniquely determined. Exhausting these divisors and
testing nonnegative integral squares is complete, without a parameter or
rank cutoff. The source polynomial is checked against both target
coefficients. The six earlier quadratic outputs are reproduced exactly
as a regression check against that independent implementation.

The source dimension has degree at most two, so target degrees above two
are excluded immediately. Integral targets need a different parameter
argument and are explicitly marked outside this quadratic exhaustion.

The family allows a single generalized near-group source followed by
finite-group extensions, equivariantizations, pointed/integer-dimension
products, and Morita equivalences, because the resulting dimension is an
integer multiple of the source. It does not cover dimension-decreasing
operations or products of distinct nonintegral sources.

All34 source tensors are hash-bound and their global dimension polynomial
is independently recovered from the positive regular Casimir matrix.
The outcome is 20 dimension-family exclusions, 12 finite parameter lists,
and 2 integral targets outside the quadratic parameter test.

| Outcome | Baseline ring indices |
|---|---|
| Quadratic dimension mismatch | 1154,1203,1795,2842,3258,3413 |
| Degree greater than two | 901,903,925,926,928,941,982,985,1463,1615,1617,1660,1661,1739 |
| Complete finite parameter lists, not models | 65,436,439,455,567,721,921,1055,1350,1768,2885,3472 |
| Integral target outside this test | 731,3344 |

Rank-two source rows with K>1 are explicitly impossible by rank-two
categorification, but other rows are retained until a separate
source-specific obstruction or construction is supplied. In particular,
the R721 generalized near-group list has four dimension possibilities;
the narrower ordinary near-group family has only (G,K,k)=(4,16,1) and
(1,8,4). Eliminating those two narrower possibilities does not eliminate
all generalized near-group sources.

```
python evidence/rank8_frontier_20261021/noncommutative_followup/generalized_near_group_all_frontier.py
python -O evidence/rank8_frontier_20261021/noncommutative_followup/generalized_near_group_all_frontier.py
```
