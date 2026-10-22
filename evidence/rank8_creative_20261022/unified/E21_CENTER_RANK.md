# Center of the neutral E21 category

Let E=C_A and D=E_0 be the actual unitary fusion categories in
`E21_MODEL_AUDIT.md`, with C=SU(3)_21. Then

    Z(D) = (C_0)_{Reg(Z/3)} tensor Rep(E7_1)^rev,             (1)

as braided fusion categories. Here C_0 is the triality-zero subcategory
of C, and Reg(Z/3) is the regular algebra of its central Tannakian
simple-current subcategory. In particular the center has rank62.

DMNO, Corollary3.30, gives `Z(E)=C tensor Rep(E7_1)^rev`. The order-three
simple currents J=(21,0), J²=(0,21) are summands of the conformal algebra
A. Adjunction shows

    Hom_E(A,J tensor A)=Hom_C(1,J tensor A)=C.

Since the free module J tensor A has FP dimension one, it is the unit A.
The central free functor from C is fully faithful, so J gives three
distinct central lifts of the unit. Their twists are one, since h(J)=7.

It is important to identify these lifts with the specified triality
grading, rather than merely observe that their underlying objects are
units. Their monodromy with the free image of (a,b) is
`exp(+/-2pi i(a-b)/3)`, the simple-current monodromy in SU(3)_21. Once
the underlying image of J is identified with the unit, the half-braiding
of the other central object with it is the unit constraint, by naturality.
Thus this monodromy is the half-braiding of J itself. Free induction
dominates every homogeneous component of E. Consequently these central
lifts are exactly the grading characters of the faithful Z/3 grading.

Gelaki--Naidu--Nikshych, *Centers of graded fusion categories*,
<https://arxiv.org/abs/0905.3117>, Corollary3.7, says that the
de-equivariantization of their centralizer is braided equivalent to Z(D).
The centralizer in the C factor is C_0; the second product factor
centralizes them automatically. This proves (1).

There are85 triality-zero weights (a,b) with a+b<=21. The action

    J(a,b)=(21-a-b,a)

has28 free orbits and one fixed point (7,7). A free orbit gives one
simple module over Reg(Z/3). The fixed point gives three: its stabilizer
is cyclic of order3 and its projective-representation cocycle is trivial,
because `H²(Z/3,C*)=0`. Equivalently, a twisted group algebra of a cyclic
group has a generator whose cube is a nonzero scalar; over C it can be
rescaled to cube one and has three one-dimensional representations.
Hence the de-equivariantization has rank31. The pointed E7_1 factor has
rank2, giving rank62 in (1).

This determines the center of the constructed E21 neutral model. It does
not assert that every category with ring R982 has the same center. In
particular, a comparison with complete possible center ranks for another
ring can exclude Morita equivalence to this model, not categorification
of that other ring.

The orbit count is independently verified in `verify_e21_model.py` and
`e21_model_verification.json`.
