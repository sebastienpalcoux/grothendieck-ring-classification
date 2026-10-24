# A finite eighth-root spectrum forced by the TY subcategory

This is a necessary condition, not a full source-ring exclusion or a construction. Work in a pseudo-unitary representative of a hypothetical source categorification. The previously accepted general reduction obtains such a representative by first passing to the D8 Morita dual, which has two FP dimensions, and then using the Galois-pseudo-unitarity theorem and Morita invariance of pseudo-unitarity. The categorical TY parameter tau is rational, ±1/2, and chi takes values ±1. Galois conjugation therefore preserves the TY sign; an exclusion of either sign in the positive representative excludes that same categorical sign in general complex scope.

Let Y be the dimension-two simple in the integral TY(V4,chi,tau) subcategory, with nonalternating chi, and put epsilon=sgn(tau). Shimizu's Theorem 3.4 gives

    nu_1(Y),...,nu_8(Y) = 0, epsilon, 0, 0, 0, epsilon, 0, 2.

These indicators are unchanged when Y is viewed in the full category: their defining invariant spaces and rotation operators lie entirely in the full tensor subcategory. The TY category carries the positive spherical structure obtained by restriction from the ambient positive structure.

Let I denote induction to the center and D=FPdim(C)=16+32d, d=4+3sqrt(2). The center indicator formula is

    D nu_n(Y) = sum_Z [I(Y):Z] FPdim(Z) theta_Z^n.

At n=8 the right-hand side has total positive weight FPdim(I(Y))=2D and equals 2D. Therefore every constituent has theta_Z^8=1. Finite Fourier inversion now determines the total positive weight in each twist fiber. Writing zeta=exp(pi i/4), the weight mu_j at theta=zeta^j is

    mu_j = (D/8) (2+2 epsilon cos(pi j/2)).

Thus each primitive-eighth-root fiber has weight D/4. For epsilon=+1 the theta=1 and theta=-1 fibers each have weight D/2 and the theta=±i fibers are absent. For epsilon=-1 the theta=±i fibers each have weight D/2 and the theta=±1 fibers are absent.

The exact induction Gram matrix says that F(I(Y)) has no invertible constituent, has Y with multiplicity 16, and has each of the four large simples with multiplicity 16. Consequently a simple constituent Z of I(Y), with multiplicity a, has

    FPdim(Z)=2a+b d,   a≥1, b≥0.

For a primitive-eighth-root fiber, comparing the constant and d coefficients in its weight D/4=4+8d yields

    sum_Z a_Z²=2,   sum_Z a_Z b_Z=8.

There are therefore exactly two constituents in that fiber, both of multiplicity one; their b values add to 8. Modular formal-codegree integrality requires D²/(2+b d)² to be an algebraic integer. For b=0,...,8 it holds only at b=0,1,4,7,8. Equivalently the other cases have denominator 49 or 289 in the integral basis 1,sqrt(2). The newly proved integral-center theorem rules out b=0; b=8 is then ruled out because its partner would have b=0. Each primitive-eighth-root fiber therefore has exactly one of these two dimension pairs:

    (2+d, 2+7d),   or   (2+4d, 2+4d).

For each of the two other nonempty twist fibers, the same comparison gives sum a_Z²=4. Thus either it contains four multiplicity-one constituents or a single multiplicity-two constituent. In the latter case that simple has dimension 4+8d. In particular I(Y) has 10, 13, or 16 distinct simple constituents.

The finite restriction can be imposed already in a height-four relative-trace system. The only primitive-eighth-root relative-trace types over Q(sqrt(2)) are

    ( sqrt(2)/2, 0, -sqrt(2)/2, -1 ),
    (-sqrt(2)/2, 0,  sqrt(2)/2, -1 ).

For epsilon=+1 add the types for theta=±1; for epsilon=-1 add the type (0,-1,0,1) for theta=±i. Impose the exact second and fourth moments D epsilon and zero. This is substantially smaller than permitting arbitrary roots with the allowed prime support; no truncation of possible root orders is being assumed for constituents of I(Y).

`verify_ty_spectrum.py` checks the finite TY indicator sums, all three induction restrictions, the Fourier weights, and the nine exact algebraic-integer tests. `screen_integral_center.py` applies the resulting necessary constraints to the existing labelled-S center system. An infeasible **separator** optimization is only failure to find a contradiction and is never reported as categorical nonexistence.

## Completed conditional exclusion

The sign +1 is excluded for R9_2_1607 and R9_2_1976 by exact Farkas certificates for the strengthened height-four necessary systems. Their products b^T y are respectively -1,253,376 and -17,466,624, and both have minimum entry of A^T y equal to zero. Thus any categorification of either ring must have tau=-1/2. The negative-sign systems supplied no exclusion. Neither source ring is thereby settled. The corresponding positive-sign screen for R9_2_137 supplied no separator; its negative-sign screen reached its explicit 180-second optimization limit and supplies no conclusion.

The positive-sign rays are preserved in the `R9_2_*_integral_center_h4_tau1.json` records. The `_replay.json` records are fresh exact replays without optimizer calls. `export_replay_system.py` creates compressed integer matrices and rays; `check_exported_ray.py` checks their Farkas inequalities using only the Python standard library. Matrix arithmetic verification and the independent audit of the categorical reconstruction are separate obligations.

Primary references: Shimizu, *Frobenius–Schur indicators in Tambara–Yamagami categories*, Theorem 3.4, https://arxiv.org/pdf/1005.4500; Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, center indicator formula, https://arxiv.org/abs/math/0601012; Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13 and the modular formal-codegree discussion, https://arxiv.org/pdf/1309.4822.
