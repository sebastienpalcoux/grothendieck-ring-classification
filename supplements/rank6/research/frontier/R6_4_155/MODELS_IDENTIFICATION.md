# R155: exact comparisons with known center constructions

Research note, 30 September 2026. No known category was identified. The input is
the necessary dimension/twist spectrum of profile 296, **not full modular data**.
The S matrix, the remaining fusion coefficients, associators, and existence are
unknown. No conclusion here changes the unresolved status of R155.

Put d=4+3√2, D=72+48√2, and b=2+4d=D/4. The hypothetical center has rank 52,
dimension D², and exponent 24. Its semion centralizer B has rank 26 and dimension
D²/2. The source of the input is
`forced_twists.md`.

## 1. All five Grossman–Izumi formulas fail direct identification

Primary source: P. Grossman and M. Izumi,
[Infinite families of potential modular data related to quadratic categories,
arXiv:1906.07397v2](https://arxiv.org/pdf/1906.07397), Definitions 3.1, 4.1,
5.1, 6.1, 7.1 and Theorems 3.6, 4.4, 5.6, 6.4, 7.4.
The paper concerns potential data; its formulas do not themselves establish
categorification in general.

Their positive vacuum magnitude is

    S00 = |1/√|G| − 1/√|Γ|| / 2.

Consequently direct agreement forces unordered sizes {16,18} for Z(C), or {8,9}
for B. These are exact, unique possibilities:

    2/D = 1/4 − √2/6;
    2√2/D = √2/4 − 1/3.

For uniqueness, if x=1/√m, y=1/√n and x−y is the prescribed element of Q(√2),
then x+y=(1/m−1/n)/(x−y) also belongs to Q(√2). A positive element of Q(√2)
whose square is rational is rational or a rational multiple of √2. Comparing
the two nonzero coefficients fixes m,n.

| Formula | Direct Z(C), sizes 16 and 18 | Direct B, sizes 8 and 9 |
|---|---|---|
| Section 3 | Size difference 2 forces fixed subgroup U of order 1; an involution of an even group cannot have exactly one fixed point | Difference 1 violates the size conditions |
| Section 4 | Permitted sizes give rank 21, not 52 | Difference must be 2 |
| Section 5 | Difference must be 4 | Difference must be 4 |
| Section 6 | Difference must be 1 | Permitted sizes give rank 14, not 26 |
| Section 7 | Difference must be −1 | Ordering would force G of order 9, incompatible with G[2]≅C2² |

The Section 3 size conditions are |Γ|−|G|=4|U|, or 2|U| with |G|/|U|
even. The rank calculations use the explicit index sets:

    Section 4: 2+2+(16−2)/2+2+(18−2)/2 = 21;
    Section 6: 2+6+(8−4)/2+(9−1)/2 = 14.

The latter really has the target global dimension, so dimension matching would
have produced a false identification. Its dimension multiset is

    1¹, (1+4d)¹, (1+2d)⁶, b², (4d)⁴,

whereas B has

    1², d⁶, (2d)⁸, (3d)², (1+2d)⁴, (1+4d)², b².

These exclusions concern direct membership in the five displayed formulas in
positive-vacuum normalization. They do not exclude further condensation,
gauging, or other constructions applied to categories with those data.

## 2. Nearby realized near-group centers have different fields

Primary sources:

- Z. Yu and Q. Zhang, [Realizing modular data from centers of near-group
  categories, arXiv:2412.20763v2](https://arxiv.org/html/2412.20763v2), Theorems
  1 and 2. They use near-group (C4×C4)+16 and C8+8 for their constructions.
- E. C. Rowell, H. Solomon, and Q. Zhang, [On near-group centers and
  super-modular categories, arXiv:2305.09108v2](https://arxiv.org/pdf/2305.09108),
  abstract and the worked C6+6 and (C2×C4)+8 cases. Table 8 mixes constructions
  with conjectural descriptions; it must not be treated as an existence theorem.

For a near-group ring of order n and multiplicity m, the noninvertible dimension
is ρ=(m+√(m²+4n))/2 and the global dimension is n+ρ². Thus:

| Near-group type | Global dimension | Field |
|---|---|---|
| (C4×C4)+16 | 160+64√5 | Q(√5) |
| C8+8 or (C2×C4)+8 | 48+16√6 | Q(√6) |
| C6+6 | 30+6√15 | Q(√15) |

Their centers square these dimensions. Condensation by a finite Tannakian group
and removal of pointed tensor factors divide global dimension by rational
integers, preserving these nontrivial quadratic fields. Therefore those
specific constructions cannot give Z(C) or B. This does not address arbitrary
products or nonintegral algebra condensations.

## 3. September 2026 Haagerup–Izumi construction also fails the field test

The recent primary preprint by T. Gannon, A. Schopieray and H. Yadav,
[On Haagerup–Izumi fusion categories, arXiv:2609.25185v1](https://arxiv.org/abs/2609.25185),
submitted 21 September 2026, announces cyclic HI categories for all odd N,
near-group ((Z/N)²,N²) equivariantizations, and center formulas.

For these HI rings the noninvertible dimension solves x²=1+Nx, so the global
dimension field is Q(√(N²+4)); the indicated near-group ring has the same field.
It cannot equal Q(√2): such equality would imply N²+4=2t² for an integer t,
but for odd N the two sides are 5 and either 0 or 2 modulo 8. This excludes
their direct centers, finite-group condensations, and pointed-factor removals.

In fact there is a stronger all-orders exclusion. For any standard generalized
Haagerup ring of group order N, let x²=1+Nx and δ=N(1+x²). Then

    Tr(δ)=N(N²+4),     Norm(δ)=N²(N²+4),
    Tr(δ²)/sqrt(Norm(δ²))=N²+2.

The last expression is unchanged on multiplying δ² by a positive rational.
For D² it is 34, so rational-scaled agreement with the target center, or with
B, would force N²=32. No integer N works. This includes even-order HI rings
and their Morita duals, and excludes all constructions that only scale their
center dimension rationally. It does not exclude nonintegral algebra
condensation. The defining fusion rules are displayed in the cited 2026
paper's introduction; no construction theorem is needed for this calculation.

## 4. Only two near-group dimension types survive

For an irrational near-group ring of order n and multiplicity m, let
ρ²=n+mρ and δ=n+ρ². Then

    Tr(δ)=m²+4n,     Norm(δ)=n(m²+4n),
    Tr(δ²)/sqrt(Norm(δ²))=m²/n+2.

Thus rational-scaled agreement of its center dimension with D² requires
m²=32n, equivalently n=2k², m=8k. Its noninvertible dimension is k d and
its global dimension is (k²/2)D.

Schopieray's [Categorification of integral group rings extended by one
dimension, arXiv:2208.07319](https://arxiv.org/pdf/2208.07319), Proposition 3.3,
imposes n|m, hence k|4. The three arithmetic possibilities are (2,8), (8,16),
and (32,32). Theorem 1.1 excludes (2,8), leaving only **(8,16) and (32,32)**.
Neither type is thereby constructed.

The divisibility argument needs no unitarity. To avoid the overstrong literal
pseudo-unitarity assertion in that preprint's Lemma 3.1, first pass to the
pseudo-unitary Galois representative supplied by the two-dimension argument.
The formal-codegree object then has dimension 1+(m/n)ρ, and forgetting to the
original category forces its coefficient of the irrational ρ to be an integer.
This is precisely the proof needed for n|m.

The near-group ring with |G|=m=32 has

    ρ=16+12√2=4d,       FPdim=576+384√2=8D.

An order-8 central Tannakian condensation of such a category's center would
have dimension D². This is only an arithmetic lead: no suitable categorification,
central subgroup, resulting rank, or resulting twists were found. Even existence
of the near-group category would not establish the required condensation.

One group is rigorously ruled out: G=C2⁵. Schopieray's Theorem 1.1 permits
positive multiplicity for elementary abelian 2-groups only at orders 2 and 4.
It does not exclude all groups of order 32. The previously checked conditional
(C4×C2)+16 route likewise remains conditional on a coherent action.

## 5. Structural filters supplied and independently checked during this pass

The root investigation proves B is prime as a modular category. A nontrivial
Deligne factorization of rank 26 would have a rank-2 factor. Its nonunit simple
has dimension x with x²=1+nx. Every irrational such x in Q(√2) has field norm
−1. The available norms, in order 1,d,2d,3d,1+2d,1+4d,b, are

    1, −2, −8, −18, 9, 1, 36.

The only remaining rank-2 factor would be pointed; B's unique nontrivial
invertible is a fermion, so that factor is not nondegenerate.

Also the fermion centralizer of rank 16 cannot be sVec⊠A: this would embed a
modular rank-8 A into B, whose Müger decomposition would require 8 to divide 26.
Thus the required supermodular category is nonsplit. Neither proof needs a
classification of rank-2 or rank-8 categories.

## Reproducible arithmetic and remaining gap

Run `python -O models_exact_comparisons.py` in this directory. The standalone
standard-library check takes under a second and writes
`models_exact_comparisons.json`. It checks dimensions, the two vacuum matches,
the misleading rank-14 dimension match, all norms, and the 32+32 arithmetic.
It uses exact rational pairs, not floating-point tolerances or an enumeration.

There is no full modular-data match or categorical construction here. The
remaining identification problem genuinely includes a prime rank-26 modular
factor and a nonsplit rank-16 supermodular centralizer; the published examples
and formula families tested above do not supply them.
