# Partial modular spectrum and labeled-frame STS constraints

The initial categorical hypothesis in this file is pseudo-unitarity.
The general-complex applications additionally carry a complete oriented
signed/sphericalization certificate. No pivotality conjecture is used.

Let C have commutative Grothendieck ring R, positive global dimension D,
irreducible characters chi_E and formal codegrees f_E. Its distinguished
central simples A_E occurring in I(1) have dimension beta_E=D/f_E and
twist one. If Z has restriction v, then

    S(A_E,Z) = beta_E chi_E(v).

This follows from the character orthogonality and Deshpande, *On centers
of bimodule categories and induction-restriction functors*,
[arXiv:1611.04486](https://arxiv.org/abs/1611.04486), Corollary2.18,
equation(39), specialized to the commutative case. Equivalently use the
central character in Corollary4.5 and the dimension of A_E. The modular
matrix here is unnormalized: its first row consists of object dimensions.

By symmetry, S(A_E,Z)/dim(Z) is a character value of the integral fusion
ring of the center, hence an algebraic integer. Thus every proposed
restriction column must satisfy integrality of

    D chi_E(v) / (f_E dim(v))  for every E.

The implemented field is Q(zeta_24), with exact cyclotomic polynomial
x^8-x^4+1. Its ring of integers is Z[zeta_24]. Consequently membership
is exactly the integrality of all eight rational power-basis
coordinates. This is the standard cyclotomic integer-ring theorem,
e.g. Milne, *Algebraic Number Theory*, section on cyclotomic extensions:
https://www.jmilne.org/math/CourseNotes/ant.html . The implementation
does not infer integrality from an approximate root or a numerical
minimal polynomial.

`partial_s.Table` checks that all eight reconstructed characters are
distinct, satisfy every source tensor multiplication identity, and
satisfy exact character orthogonality. It also checks that the positive
dimension embedding appears. The real coordinates sqrt(2),sqrt(3)
are embedded as zeta^3+zeta^-3 and zeta^2+zeta^-2, respectively; their
squares are explicitly checked. All source tensors are bound by hashes.

For every complete low frame, every bijective labeling by characters
with the required dimension beta_E is tested. An assignment survives
precisely when all distinguished entries satisfy

    beta_E chi_E(v_F) = beta_F chi_F(v_E).

The recursion only removes a partial assignment on this exact equality
or because a character has already been used. It is therefore an
exhaustive search over the permitted labelings. The complete-frame hull
can omit a frame only if it has no surviving assignment. Columns with
the same allowed set are interchangeable before labeling; the labeling
search restores every character assignment after that permutation
quotient.

For R8_3_926 the high integrality filter removes140 of2863 candidates.
The exact symmetric-labeling test retains11 of6891 complete low frames.
The resulting197-row cone has49618 columns and an exact separator for
each of its two admissible indicator assignments. The saved general
certificate also verifies all16 oriented signed branches. Discovery and
optimized read-only replay both pass; independent review is separate.

## Real STS strengthening

This further refinement uses an explicit variable for each surviving
(frame,character-labeling), rather than identifying all labelings of a
frame. The center has Gauss sum D and its distinguished objects have
twist one, so STS = D T^-1 S T^-1 gives

    sum_Z theta_Z chi_E(v_Z) chi_F(v_Z) = f_F chi_E(v_F).

First group high center simples into complete duality orbits. The
twists of Z and Z* agree, while chi_E(v*) is the complex conjugate of
chi_E(v); this character compatibility is checked exactly. Therefore
the sum of the product coefficients on each high duality pair is real;
a duality-fixed restriction already has real character values. Only
after this grouping do we take the normalized relative cyclotomic
trace used by the original cone. In Q(zeta_24), the real subfield is
Q(sqrt(2),sqrt(3)); membership of every coefficient in the actual
relative-trace field is checked exactly. The high term per vector,
summed over its complete duality orbit, is consequently

    Re(chi_E(v) chi_F(v)) Tr(theta).

Low twists are1, so their coefficient and the right hand side project
to their real parts under this relative trace. (If the relative-trace
field is smaller than the real cyclotomic subfield, exact membership
of these real parts is required.) This argument does not replace
Re(theta*c) by theta*Re(c) for an unpaired complex coefficient.

The fixed tensor unit contributes1. Thus the low frame column has
coefficient Re(sum_{nonunit low} chi_E(v)chi_F(v)
- f_F chi_E(v_F)), the high columns have the coefficient above, and the
right hand side is-1. The high duality-pair feature is the sum of its
two distinct restriction features. This derivation does not assume
that an imaginary trace vanishes or multiply a relative trace by a
coefficient outside its fixed field.

All row denominator clearing is positive. The new high-column oracle
uses the exact bilinearity of multiplication in the real field to
evaluate the full finite domain without a dense matrix. The known
unitary R8_3_334 has an exact nonnegative rational feasible certificate
for this stronger system.
