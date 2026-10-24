# Quadratic neutral-block obstruction inside a quartic dimension field

The general exclusions here are **R9_2_500** and **R9_2_1235**. Their exact certificate replays pass, and the independent theoretical audit is **APPROVED** with no additional assumptions. Both have quadratic global FP dimension `D=32+16sqrt(2)`, although individual dimensions generate a quartic field.

## A general restriction principle

Let C be pseudo-unitary with commutative Grothendieck ring R, global dimension D in a real quadratic field K, and positive dimension character d. Suppose a subset S of the basis, containing the unit and closed under tensor products, has dimensions in K. Assume the ambient induction Gram matrix B has zero entries between S and its complement.

For every central simple Y, its nonnegative restriction vector v satisfies `v_i v_j<=B_ij`. Therefore its support is entirely in S or entirely in the complement. In particular, central simples supported outside S contribute zero to every Gram entry indexed in S, and zero to every induced twist trace of an object in the fusion subcategory on S. The latter remains true for tensor powers of such an object because S is closed under products.

Consequently one may retain only central restriction vectors supported in S and impose only the Gram and indicator/rotation equations for indices in S. One must still use the **ambient** global dimension D, ambient formal codegrees, and ambient modular character operators. Using the center of the rank-six subcategory in place of these ambient data would be a different problem and would not give this obstruction.

The full ambient I(1) lies in the retained block: every restriction vector with v_0=1 has support in S. Hence all its formal-codegree counts must be imposed, with dimensions D/f_h. In the present cases each D/f_h is in K, checked exactly. All retained central dimensions are in K, so the quadratic relative-trace method of `THEOREM.md` applies unchanged to their twists. Averaging over the Galois group fixing K preserves the coefficients of these equations. Discarded central objects have coefficient zero in every retained equation, regardless of their dimensions or twists.

The necessary arithmetic filters remain valid for every retained vector: algebraic integrality of D/z, the central simple d-number condition, and algebraic integrality of every coefficient of

`det(t I - (D/z)*B^-1*N_v)`.

Here B and N_v are full ambient matrices of rank nine. Since the ambient ring is commutative, their character eigenvalues have precisely the modular S-ratio interpretation proved in `THEOREM.md`. No splitting-field approximation or quartic-to-quadratic truncation is used: the dimensions and D/f_h are tested for actual membership in K inside the exact quartic field.

For the two accepted applications below, the modular characteristic-polynomial filter rejects **no** column: the arithmetic filters alone already leave exactly the final 102 columns. The contradictions therefore do not depend on this additional modular filter.

No Galois dimension-pair closure or balance is imposed in this relaxation, because a Galois permutation might exchange retained and discarded central objects. Omitting such constraints is conservative. The discarded Gram and trace equations are also omitted. Thus every categorification produces a feasible solution of the reduced system, and exact infeasibility of the reduced system excludes categorification.

## The two applications

| Ring | Retained source indices S | Global dimension |
|---|---|---|
| R9_2_500 | 0,1,3,4,6,8 | 32+16sqrt(2) |
| R9_2_1235 | 0,3,5,6,7,8 | 32+16sqrt(2) |

In each case S is the rank-six neutral subring identified with the diagonal-fermion quotient of Ising times PSU(2)_6. Its complement has three objects. The code checks subring closure and every zero cross-block Gram entry exactly. The field generator sqrt(2) is recovered as `(D-32)/16` inside the exact quartic character field, and its square is checked to be two.

The exhaustive raw neutral-vector box has 5600 elements. Exactly 432 nonzero vectors pass the entrywise and positive-semidefinite Gram inequalities. The exact arithmetic and full ambient modular filters retain 102 central restriction columns. The joint height-three system has 63 equations and 667 variables. The same 25-term separating functional works for both rings after relabeling their neutral objects. Each stored integral Farkas ray satisfies

`A^T y >= 0`, and `b^T y = -896`.

Hence a nonnegative solution of Ax=b would imply `-896=x^T A^T y>=0`, a contradiction. The signed general-to-Galois-pseudo-unitary gates for both rings, independently replayed in `../signed/`, turn these pseudo-unitary contradictions into general complex-fusion-category exclusions.

The only order-three rotation rows with nonzero coefficients in these rays concern the nontrivial invertible object g (source index 1 or 6). It has order two, so Hom(1,g^3)=0 and its third indicator vanishes. Thus this particular obstruction uses only neutral induction Gram data, arithmetic/formal-codegree restrictions, first and second twist moments, and the elementary third-indicator condition for that invertible object.

## Replay and control

Run from the research root:

```sh
python phase2/quadratic_theory/verify_quadratic_neutral.py
```

This rebuilds the exact integer systems from the original tensors, verifies every Farkas inequality with integers, compares metadata, and independently enumerates the entire neutral bounded box in Python to verify the native enumerator. It calls no LP solver. `neutral_verification.json` records PASS, the separating value -896, and both system SHA-256 hashes.

The known model R9_2_515, the diagonal-fermion quotient of Ising times PSU(2)_10, supplies a quartic-field positive control for this precise restriction principle. Its quadratic global dimension is recovered by the same generic code, its neutral block has six objects, and its height-three system has an exactly verified rational nonnegative solution. That sparse witness is saved in `neutral_positive_control.json`. This control is separate from the exact infeasibility certificates.

Files: `quadratic_neutral.py`, `verify_quadratic_neutral.py`, `R9_2_500_neutral_h3.json`, `R9_2_1235_neutral_h3.json`, and `neutral_verification.json`. The source theorems and references for the center, modular integrality, finite relative trace packets and tensor rotation are listed in `THEOREM.md`; the reduction principle above explains why they apply despite the ambient quartic dimension field.

The independent audit is `../signed/neutral_audit.md` with exact results in `../signed/neutral_audit.json`. It independently enumerates raw vectors, obtains low-column counts from the characteristic factors of B, verifies equality of the arithmetic-filtered column set, hand-lists the eight possible joint twist packets, rechecks both Farkas rays, and provides an independently recovered exact feasible witness for the known R9_2_515 model. Both reconstructed system hashes agree with this implementation.
