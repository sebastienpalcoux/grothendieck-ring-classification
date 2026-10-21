# Independent audit of the R65 pointed-phase exclusion

**Verdict: accepted.** The uniform pointed-induction/Fourier argument and the
six exact separators cover all four classes in H^3(C4,C*) and exclude
pseudo-unitary categorification of `R8_3_65`. Schopieray's published Lemma 3.1
then excludes general complex categorification. This verdict does not use the
older subgroup-dual obstruction for the trivial pointed class, the rank-four
classification, or the R1453 exclusion.

## Mathematical scope checks

For an invertible object g of order n in a pseudo-unitary category, the
canonical positive spherical structure gives positive weights m_Z FPdim(Z)
in the central-induction formula. The nth indicator has modulus one because
its rotation acts on the one-dimensional space Hom(1,g^n), whereas every
smaller positive indicator vanishes. Equality in the triangle inequality
therefore forces every supported twist to have the same nth power. Fourier
inversion at these n roots gives each individual twist fibre weight D/n.

The directly recomputed pointed induction Gram matrix is 8 times the
identity. Thus a central simple in I(g) contains no other source invertible
in its restriction. Writing its dimension as m+b d, fibrewise coefficient
comparison in D/4=2+11d gives sum m^2=2 and sum mb=11. It follows that m=1
and b<=11 for every constituent in I(g) or I(g^3). These are restrictions on
actual integral multiplicities before any real/rational cone relaxation.
There is no assumption that normalized trace preserves integrality of
individual twist-fibre counts.

The cyclic cocycle product was independently recomputed for each k=0,1,2,3.
The fourth indicators of g and g^3 are i^k; the second indicator of g^2 is
(-1)^k. The three generator trace domains are consequently fourth roots
(k=0), primitive sixteenth roots (k=1 or 3), and primitive eighth roots
(k=2). The involution domains are respectively {+1,-1} or {+i,-i} as stated
in the producer's proof. The source dual-pair restriction does not change
these domains: ribbon duals have equal twists, and g,g^3 have equal fourth
indicators.

Schopieray, *Categorification of integral group rings extended by one
dimension*, published Lemma 3.1 explicitly applies to any fusion ring whose
FP dimensions belong to {1,d}, and concludes that any categorification is
Galois conjugate to a pseudo-unitary one. Its hypotheses hold here. The
Galois-conjugate pointed associator class need not be identified, since every
class has been excluded. Primary source:
https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms.12789.

The central-induction formula is Theorem 4.1 of Ng–Schauenburg,
*Frobenius-Schur indicators and exponents of spherical categories*,
https://arxiv.org/abs/math/0601012. The triangle-equality and Fourier steps
above are direct deductions, not extra hypotheses of that theorem.

## All-order domain check

The inherited Cauchy prime support is {2,5}, since Norm(D)=2000. For moments
1 through 4, all orders dividing 40 are retained. Any supported root order
not dividing 40 has either 2-adic valuation at least 4 or 5-adic valuation at
least 2. After division by gcd(order,j), 1<=j<=4, the former still has
2-adic valuation at least 2, and the latter still has 5-adic valuation at
least 2. In each case both the rational Ramanujan term and the primitive
quadratic-conductor-5 Gauss term vanish. Therefore the whole four-moment
tuple is zero. This proves the extra all-zero type covers the unbounded
tail; 40 is not asserted to bound the twist order.

The audit independently averages powers of zeta_40 over its eight Galois
automorphisms fixing sqrt(5). It recovers exactly the imported thirteen
joint trace types after adjoining the all-zero tuple. This uses direct
cyclotomic polynomial reduction, not the producer's Ramanujan/Gauss formula.

The existing cone remains an outer relaxation: all possible low choices,
all integral high restriction vectors passing necessary Gram/integrality
tests, all complete duality orbits, and all auxiliary rotation columns are
retained. Full-field S symmetry is the distinguished induction-character
identity. In the CM STS rows the complete dual pair makes the character
product coefficient real, so it factors through the trace to Q(sqrt(5));
the field trace of a lone nonreal coefficient is not silently discarded.
The code checks this exact field reconstruction. These imported identities
are independently documented in `quadratic/CM_REAL_STS.md` and
`global_induction/PROOF.md` under the previous research directory.

## Finite replay

`r65_independent_audit.py` independently computes the pointed group,
induction Gram matrix, source FP-dimension equations, cyclic indicator
classes, and thirteen cyclotomic trace types. It reconstructs the allowed
column mask separately and scans every explicit sparse column against every
saved integer separator. It does not call an optimization routine or rely
on the factorized Farkas oracle.

| Associator classes | Certificate | Allowed columns | Indicator branches |
|---|---|---:|---:|
| 0 | `pointed_phase_k0_fourier.json` | 2413 | 2 |
| 1,3 | `pointed_phase_k1_fourier.json` | 1992 | 2 |
| 2 | `pointed_phase_k2.json` | 2222 | 2 |

Every column pairing is nonnegative and every right-hand-side pairing is
strictly negative. The independent receipt records those exact pairings
and certificate file hashes in `r65_independent_audit.json`. The decisive
even-class certificate does not need the additional Fourier restriction;
retaining its larger domain is valid.

Reproduce from the repository root:

```sh
python evidence/rank8_research_20261022/r1768_r3472/r65_independent_audit.py
```

The general exclusion is a mathematical and exact finite-certificate
deduction. A failed model search, solver timeout, or numerical infeasibility
has no role in the conclusion.
