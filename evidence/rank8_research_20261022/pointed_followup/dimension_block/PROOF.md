# Dimension-block screening and saturated twist-one restrictions

**Conclusion.** All seven rings unresolved immediately after the R65 exclusion
pass the scalar dimension-block
bound. Four attain equality and acquire necessary restrictions on additional
twist-one simples of their centers. All forced summands of `I(1)` satisfy
these restrictions. R1795 is subsequently excluded by the separate C2
Fourier-fibre criterion; that conclusion does not follow from this screen.
No ring is excluded and no model is constructed by the present argument.

## Primary theorem and the equality argument

Reference: Andrew Schopieray, [*The dimension block of a spherical fusion
category*, arXiv:2609.35287v1](https://arxiv.org/html/2609.35287v1),
28 September 2026, Lemmas 2.1 and 4.1, Theorem 5.1; compare Section 6,
equation (30).

Write `K=Q(d_X)` and `D=sum d_X^2` in a pseudo-unitary form. Here
`K=Q(D)`, so the dimensional grading order is one. For each character
`chi` of `Gal(K/Q)` put `h_chi=sum_sigma chi(sigma)/sigma(D)`.
The cited theorem gives `conductor(chi)*|h_chi|^2 <= 1`.

For completeness, the following equality deduction applies the operator
bound used in that theorem. Let `w_chi` be the signed sum of the center
simples indexed by the dimension orbit, and let `P` project onto twist-one
coordinates. Its dimension-orbit coordinates already contribute
`|Gal(K/Q)|*|h_chi|^2` to `||P S_normalized w_chi||^2`. When the scalar
bound is saturated, this is the entire allowed norm. Every coordinate
outside that orbit must therefore vanish. The center row formula yields

    theta_Z=1, Z outside the dimension orbit
       => sum_sigma chi(sigma) sigma(d_Z/D)=0

for each saturated character. This is an exact necessary condition; it
does not assert that the remaining columns are realized by a category.

## Exact arithmetic for the seven rings

For the quartic field use the basis `(1,sqrt(2),sqrt(3),sqrt(6))`.
Its three nontrivial characters have conductors `8,12,24`, respectively.
For a real quadratic field the nontrivial conductor is its fundamental
discriminant.

| Rings | D | h_trivial | Nontrivial conductor-weighted squared sums |
|---|---|---|---|
| R8_3_928, R8_3_941, R8_3_982 | 144+96sqrt(2)+80sqrt(3)+56sqrt(6) | 1/2 | 0, 1, 1 for conductors 8,12,24 |
| R8_3_1154, R8_3_1795 | 540+240sqrt(5) | 3/10 | 4/9 for conductor 5 |
| R8_3_1768 | 444+72sqrt(37) | 1/6 | 1 for conductor 37 |
| R8_3_3472 | 700+490sqrt(2) | 1/7 | 4/25 for conductor 8 |

The trivial-character squares also lie below one. In the quartic case,

    1/D = 1/8 - sqrt(3)/24 - sqrt(6)/48,

so the two saturated Fourier coefficients imply

    d_Z/D in Q(sqrt(2)).

Writing `d_Z=a+b sqrt(2)+c sqrt(3)+d sqrt(6)`, this is equivalent to

    a+b=3c,       a+2b=6d.

For R8_3_1768 the nontrivial sum is `-1/sqrt(37)`. Thus an extra
twist-one simple must have `d_Z/D in Q`; for `d_Z=a+b sqrt(37)` the
equation is

    6a=37b.

These equations apply **only outside the dimension orbit**, not to its
distinguished center simples. They can refine future twist-column searches;
this stage does not run such a refined cone search.

## Forced I(1) summands

The exact Casimir matrices recover every relevant formal codegree outside
the dimension orbit. Since `dim(A_E)/D=1/f_E`, the checks reduce to:

| Rings | Remaining formal codegrees | Irreducible representation dimensions | Required field |
|---|---|---|---|
| R8_3_928, R8_3_941 | 4 | one representation of dimension 2 | Q(sqrt(2)) |
| R8_3_982 | 16-8sqrt(2), 16+8sqrt(2), each twice | all dimension 1 | Q(sqrt(2)) |
| R8_3_1768 | 6 four times, 12 twice | all dimension 1 | Q |

Every reciprocal belongs to the required field. The two noncommutative
quartic rings have four scalar representations from the dimension orbit;
the remaining four-dimensional semisimple algebra must be a single
two-by-two matrix block. Its Casimir eigenvalue is 8, hence formal codegree
4. For the commutative rings the Casimir eigenvalues directly give the
formal codegrees. Thus this is a complete check of forced `I(1)` objects
for all four saturated cases.

## Scope and replay

The prior accepted general-to-spherical/Galois-pseudo-unitary gates allow
these restrictions to be imposed on a pseudo-unitary Galois form of any
general categorification. The scalar arithmetic alone does not prove those
gates, original-unitarity, a model, or general noncategorification.

`verify.py` reconstructs the positive dimension vector from each canonical
tensor's Casimir eigenspace using rational multiquadratic arithmetic. It
checks every dimension multiplication, global dimension, field degree,
character conductor and Fourier sum; derives the displayed linear masks;
and rechecks the complete relevant Casimir factors. Checks remain active
under optimized Python. The saved receipt is read-only unless `--write`
is explicitly selected.

```sh
python evidence/rank8_research_20261022/pointed_followup/dimension_block/verify.py
python -O evidence/rank8_research_20261022/pointed_followup/dimension_block/verify.py
```
