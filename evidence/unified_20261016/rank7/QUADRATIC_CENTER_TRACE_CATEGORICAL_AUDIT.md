# Independent categorical audit of the quadratic two-trace relaxation

Status: PASS for the necessary categorical constraints. This audit does not
convert floating-point infeasibility into an exclusion; exact certificates
and exhaustive source-bound replay are separate requirements.

Auditor: rank6_center, 2026-10-16.

## Complete Galois transport

I checked the character identity against the primary source, Ostrik,
*Pivotal fusion categories of rank 3*, arXiv:1309.4822, Section 2.3,
printed pp. 5--6. Immediately before Theorem 2.13, A_E is defined by
the equality chi_E(F(A))=S_(A,A_E)/S_(0,A_E). The theorem gives
S_(0,A_E)=1/f_E in the normalized center matrix. Therefore

    chi_E(F(pi_sigma(A)))
      = epsilon_sigma(A) (f_E/f_(sigma E)) chi_(sigma E)(F(A)).

This determines the entire forgetful row, not only its dimension.
The signed transport matrix has rational entries by cyclotomicity and
commutativity of the cyclotomic Galois group. The I(1) multiplicity
vector m satisfies S m=m, so G_sigma m=m. Thus I(1) is preserved with
positive Galois signs. These arguments require no construction of an
unknown center. The full derivation and explicit matrix formula are
in ../rank6_center/GALOIS_FORGETFUL_ROW_LEMMA.md.

The rank-one specialization in full_row_galois.py needs a further
field check: rational formal codegrees by themselves do not imply
rational character values. I independently recomputed the characteristic
polynomials of M=sum_i w_i N_i directly from the archived source tensors,
with w=(1,3,11,37,101,307,997). They are

    R106: (x-1860)(x+66)(x+494)
          (x^2-16448x-12738752)(x^2-124x-171388),
    R2155: (x-1314)(x-654)(x+1064)
           (x^2-19656x+889872)(x^2+1452x+527204),
    R146: (x-654)(x-184)(x+66)(x+234)(x+1852)
          (x^2-15896x+12501688).

All roots are distinct. The first two rings' two quadratic factors
have fields (Q(sqrt(3)),Q(sqrt(2))) and
(Q(sqrt(3)),Q(sqrt(-2))), respectively. In the third, the sole
quadratic field is Q(sqrt(6)). A one-dimensional common eigenspace
of the rational matrices is defined over its eigenvalue field; the
simultaneous character values therefore lie in that field. Consequently
one can choose a cyclotomic automorphism that flips the dimension
quadratic field while fixing all the other character values. The
disjoint quadratic fields make these requirements compatible.

Write d_i=a_i+b_i sqrt(r), a(v)=sum_i a_i v_i and
b(v)=sum_i b_i v_i. The exact full-row transformations then are

    r=3:  T(v)_i=v_i+b_i (a(v)-7 b(v)/4),
    r=6:  T(v)_i=v_i+b_i (a(v)-5 b(v)/2).

For the other characters, this rank-one correction vanishes by
character orthogonality: the coefficient vector b is proportional
to the difference of the two dimension-character idempotent vectors.
Evaluation on the two dimension characters verifies the required
f_E/f_(sigma E) factors. Thus the specialization used in the code
is valid here, although it is not valid for arbitrary rings having
only rational additional codegrees. The associated integer matrices
are involutions; their signed nonnegative row pairing is consequently
the necessary full Galois transport.

## The unrestricted nine-vertex hull

I independently checked every root-order case in
QUADRATIC_TWO_MOMENT_HULL.md. For K=Q(sqrt(r)), r=3 or6, let f=12 or24.
If f does not divide the order n, the normalized relative trace is the
rational Ramanujan value mu(n)/phi(n), because the intersection with K
is Q. A nonzero irrational first moment requires
n=f*m with m squarefree and coprime to6. The primitive-f pairs are

    (+/-sqrt(3)/2, 1/2), or (+/-sqrt(6)/4, 0),

respectively. The imprimitive Gauss factor is
mu(m) chi_f(m)/phi(m). For f=12 the second moment is
mu(m)/(2 phi(m)); for f=24 it is zero. When m>1,
phi(m)>=4, so the proposed convex combination with the rational
vertical segment supplies the required correction. A nonzero irrational
second moment with zero first moment requires n=2f*m and lies between
the two primitive-2f vertices. The remaining rational cases are
(q,q), (-q,q), or (0,q), and lie in the displayed five-vertex rational
hull. Thus the nine-vertex hull is valid for arbitrary root orders;
it does not secretly impose a conductor bound.

## Saturated rows and equal-phase pairing

I read the conductor-equality lemma and its quadratic-residue refinement
under evidence/unified_20261016/compression. Conditional on the
application's checked torus character and compressed eigenvalue
-1/sqrt(f), a nonzero saturated coordinate has theta^f=1 and every
primitive-f twist has chi_f(k)=-1. These hypotheses reduce the allowed
relative-trace pairs to the five rational vertices and the negative
primitive-f vertex. For f=24 the additional actual proper-divisor
pairs (0,0) and (0,1/2) are already inside the rational hull.

The pairing in quadratic_fullrow_trace_lp.py is also justified:
modular Galois symmetry gives theta_(pi_sigma(A))=theta_A^(a^2).
Every unit a modulo12 or24 has a^2=1 modulo that conductor.
Consequently saturated Galois partners have exactly the same twist,
and hence the same first/second relative-trace pair. Their convex
decompositions can therefore be chosen with the same phase weights.
This uses neither involutivity of the full Galois permutation nor a
tensor-functor interpretation of that permutation. Arbitrary twists
on the unrestricted, row-fixed fibers remain covered by the larger
nine-vertex hull.

## Induction trace right-hand sides

For a nonunit source simple X, the exact identities are

    Tr(theta on I(X))=0,
    Tr(theta^2 on I(X))=D nu_2(X).

Every already enumerated I(1) constituent has twist one. Its contribution
to either identity for X is its multiplicity in I(X) times its dimension.
Thus the builder correctly subtracts the same known vector once from
each target, using zero for the first and D times the indicator for
the second. Relative trace is linear over K, so multiplication by the
known dimensions commutes with taking it. No dimension normalization
factor is missing.

The indicator branches in the builder agree with the previously proved
pivotal odd-isotypic relations. In particular, the additional positive
indicator in R7_4_2155 is justified by the stronger adjoint-word form:
for arbitrary X, the canonical symmetric form on X tensor X* forces
every self-dual odd-multiplicity constituent to have second indicator
+1. Its source coefficient N[1][2][4]=1 applies to label4. The two
non-self-dual source simples have indicator zero.

The general-to-pseudo-unitary bridges, exhaustive low-block generation,
dimension/divisibility filters, and exact saturation coordinates remain
the responsibility of their source-bound verifiers. The present audit
checks the new categorical constraints and their implementation in the
45-row integer matrix builder; it makes no standalone status change.
