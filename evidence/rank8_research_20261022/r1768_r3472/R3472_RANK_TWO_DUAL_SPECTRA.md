# Conditional Morita-dual spectra for one rank-two R3472 module

This result restricts possible categorification of one of the two recorded
rank-two based modules. It does **not** assert that either based module lifts to a module
category, construct a fusion category, or exclude general categorification of
`R8_3_3472`. No braiding, pivotal structure, spherical structure, or
pseudo-unitarity is assumed.

## Statement

Let C be a complex fusion category with Grothendieck ring `R8_3_3472`. Suppose the rank-two based module whose source basis-1 matrix is
`[[5,7],[7,7]]` in
`evidence/rank8_next_20261021/quadratic/action_classes.json` is realized by an
indecomposable C-module category M. Then the dual fusion category B has one of
the ten dimension spectra surviving the certificate
`r3472_rank_two_dual_spectra.json`.

The exact arithmetic sieve initially gives eleven spectra. One is impossible
by the action of its seven invertible objects. The retained spectra are
necessary conditions only; no fusion multiplication or coherence is certified.

## Derivation

Write r = sqrt(2), d = 7 + 5r, and D = FPdim(C) = 700 + 490r. On reversing
the two module simples, the covered action of basis object 1 is

```
[[7, 7], [7, 5]].
```

Every action matrix N_Y of a simple Y in B commutes with this matrix. Solving
the four commutator equations over the integers gives

```
N_Y = [[s+t, 7t], [7t, s-t]].
```

Here s and t are integers, t >= 0, and s >= t. The
common positive eigenline is the module FP-dimension line, so

```
FPdim(Y) = s + 5t r.
```

This computation does not require distinct B-simples to act by distinct
matrices, or B to have a commutative Grothendieck ring. All such multiplicities
are allowed in the enumeration.

Morita invariance gives FPdim(B) = D. The regular FP-dimension element of B
acts on the indecomposable module M by a rank-one matrix. Therefore its
eigenvalue on the other eigenline vanishes. These two equations are

```
sum_Y (s_Y + 5 t_Y r)^2 = 700 + 490r,
sum_Y (s_Y + 5 t_Y r)(s_Y - 5 t_Y r) = 0.
```

Consequently

```
sum s_Y^2 = 350,     sum t_Y^2 = 7,     sum s_Y t_Y = 49.
```

Set k_Y = s_Y - 7t_Y. Then

```
sum k_Y^2 = 7,       sum t_Y k_Y = 0.
```

Integral-dimensional simples are precisely those with t = 0. They form a
fusion subcategory: tensoring two such objects cannot produce a summand with
positive radical coefficient. Let its dimension be h. The last square-sum
identity gives 1 <= h <= 7. The quotient D/h is an algebraic integer, so its
trace 1400/h and norm 9800/h^2 are integers. This leaves

```
h in {1, 2, 5, 7}.
```

Each integral subcategory is pointed. For h = 1 or 2 this is immediate. For
h = 5, the only nonpointed alternative has simple dimensions 1 and 2; the
square of the dimension-2 simple would require 4 = 1 + 2n. For h = 7, the only
nonpointed alternative has dimensions 1, 1, 1, 2. Its three invertibles fix the
unique dimension-2 simple X, so XX* contains all three invertibles, each once,
and would require 4 = 3 + 2n. Both equations are impossible.

Thus h = g is the number of invertibles. For nonintegral simples the entire
remaining problem is

```
t in {1, 2},  k in {-2, -1, 0, 1, 2},
sum n_(t,k) t^2 = 7,
sum n_(t,k) k^2 = 7-g,
sum n_(t,k) tk = 0,
n_(t,k) >= 0 integral.
```

These are complete bounds, since each term contributes a nonnegative square.
All resulting matrices are nonnegative in the covered branch. Exact enumeration
gives five spectra for g = 1, two for g = 2, two for g = 5, and two for g = 7.

## The additional orbit obstruction

For g = 7 all k vanish. The two arithmetic spectra are

```
1^7, d^7;             1^7, d^3, (2d)^1.
```

For a d-dimensional simple X, the equation d^2 = 1 + 14d and the absence of
other constant terms imply that XX* has exactly one invertible summand.
By Frobenius reciprocity, this number is the size of the stabilizer of X in
the group of seven invertibles. Hence this group acts freely on all
d-dimensional simples. Their number is therefore divisible by seven. The
second spectrum, with just three, is impossible.

The first spectrum has a free transitive action of the seven invertibles on
the seven noninvertibles. This recovers a necessary generalized-near-group
shape, but neither its full fusion rules nor its categorification follows
from the dimension calculation.

## Reproduction and sources

Run from the repository root:

```sh
python evidence/rank8_research_20261022/r1768_r3472/r3472_rank_two_dual_spectra.py
```

The script checks the two input action matrices, records their source SHA256,
enumerates all bounded integer solutions, verifies the covered nonnegative matrix
cone, and applies the orbit test. Default replay compares the saved receipt without writing; `--write` explicitly
regenerates it. All verification checks remain active with `python -O`.
Expected output: eleven arithmetic
spectra, one excluded by the orbit test, ten remaining.

The categorical inputs are standard results in Etingof–Gelaki–Nikshych–Ostrik,
*Tensor Categories*: Corollary 7.16.7 (Morita invariance of FP dimension),
Exercise 7.16.8 (rank-one action of the regular virtual object), and
Corollary 3.3.16 (algebraic-integrality of the quotient by a fusion
subcategory). Primary author PDF:
https://math.mit.edu/~etingof/egnobookfinal.pdf.

The explicit commutant calculation, simultaneous square-sum reduction,
eleven-spectrum enumeration, and seven-invertible orbit obstruction are the
new necessary-condition calculation recorded here.

## Scope correction recorded during independent review

The other rank-two action has normalized matrix `[[11,5],[5,1]]`. Its full
integral commutant is `[[s+t,t],[t,s-t]]`, with dimension `s+t sqrt(2)`.
An initial draft incorrectly restricted this commutant to off-diagonal
entries divisible by five. Independent review detected the gap. The present
theorem and certificate cover only the first action, for which divisibility
by seven follows from the exact commutator equation. No finite-spectrum
claim is made for the other action in this note.
