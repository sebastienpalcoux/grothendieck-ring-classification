# Independent audit: symmetric canonical algebra excludes R9_2_1607 and R9_2_1976

Date: 2026-10-27.

**Accepted**, retaining the archived exhaustive spherical/Galois and
TY/Morita-completion reductions as explicit dependencies. This is a different
argument from the unsuccessful quadratic-refinement proposal in
`FS2_AUDIT.md`. It does not use those exploratory module-duality sign tables.

## 1. A symmetric-form lemma

Let F:D -> C be a pivotal strong tensor functor between semisimple pivotal
categories over C. Suppose A in D has a nondegenerate pivotal-symmetric
pairing, B is a self-dual simple constituent of A with multiplicity one,
and

    F(B) = 1 + X_1 + ... + X_k

with the displayed X_i distinct self-dual simple objects. Then

    nu_2(B)=1 and nu_2(X_i)=1 for every i.              (1)

Proof. Let phi_A:A -> A* be the isomorphism obtained by currying the pairing.
Pivotal symmetry means phi_A=phi_A* j_A. Because B=B* and B occurs only
once, the B-isotypic block of phi_A is a nonzero isomorphism B -> B*;
there can be no pairing with another isotypic block. Pulling the pairing
back along B -> A gives a nondegenerate symmetric pairing on B.

Applying F preserves its nondegeneracy and pivotal symmetry. Each self-dual
simple X_i occurs once in F(B), so the same block argument applies again.
The transpose on Hom(X_i,X_i*) is f |-> f* j_Xi. Its nonzero fixed vector
forces its eigenvalue, hence the second FS indicator, to be +1.

This is a statement about preserving pairings. It is **not** the generally
false claim that tensor functors preserve the numerical indicators of
arbitrary objects.

## 2. Why the canonical algebra supplies the pairing

For a pseudo-unitary fusion category E, its center Z(E) has the canonical
ribbon structure induced by E's positive pivotal structure. The algebra
A=I_E(1) is connected commutative separable, hence Frobenius, and

    theta_A=id_A.

The last assertion is Ostrik, *Pivotal fusion categories of rank 3*,
Theorem 2.5 (arXiv:1309.4822). A Frobenius algebra's pairing epsilon m is
nondegenerate: its inverse copairing is Delta eta, by the Frobenius and
unit/counit identities.

The precise additional theorem needed for symmetry is:

J. Froehlich, J. Fuchs, I. Runkel and C. Schweigert,
*Correspondences of ribbon categories*, arXiv:math/0309465,
Proposition 2.25(ii): a commutative Frobenius algebra with trivial twist
is symmetric. Definition 2.22 defines symmetry by equality of the two
currying maps A -> A*, using the sovereign/pivotal left and right
dualities. This equality is exactly phi_A=phi_A* j_A.

This source was checked directly at
https://www.math.uni-hamburg.de/home/runkel/PDF/corr.pdf . Its hypotheses
require ribbon dualities, not a positive Hilbert-space structure. Braided
commutativity by itself would not suffice; the trivial twist is essential.

The forgetful functor Z(E) -> E preserves the specified pivotal structure
by its definition, so it is a valid F for the lemma.

## 3. The distinguished summand B in a zero-shift D8 completion

After the independently established reflection-shift obstruction, each
commutative source under consideration has only its zero-shift D8 Morita
completion remaining. Its four large simples X_q, q in V4, are all
self-dual and have dimension d=4+3 sqrt(2). The based algebra has eight
scalar irreducibles and one irreducible of degree two. Its formal
codegrees are

    D, D', 16 (six times), 4,
    D=144+96 sqrt(2), D'=144-96 sqrt(2).

Let B=A_{sigma(FP)} be the distinguished summand of I_E(1). Ostrik's
Theorem 2.13 gives multiplicity one and dimension D/D'=17+12 sqrt(2).
The central-character/S-symmetry argument audited in
`R1975_INDEPENDENT_AUDIT.md`, Sections 1--2, works unchanged for zero
duality shift, and forces

    F(B) = 1 + sum_{q in V4} X_q.                    (2)

It is important to establish that B is self-dual rather than assume it
from its dimension. Here uniqueness supplies the proof: the Frobenius
pairing makes I_E(1) self-dual. Among its distinguished simple summands,
only B has dimension D/D', since only the sigma(FP) representation has
formal codegree D'. Taking duals preserves dimension in the spherical
category and permutes the summands of I_E(1). Therefore B*=B.

Apply the lemma to (2). It gives the categorical conclusion

    nu_2(X_q)=+1 for all four q.                     (3)

No classification of the unknown noninvertible associators or numerical
duality-cochain convention enters this deduction.

## 4. Morita-invariant weighted indicator gives the contradictions

For a pseudo-unitary fusion category C, put

    W_2(C)=sum_{Y simple} FPdim(Y) nu_2(Y).

The center-induction formula gives

    W_2(C) = (1/FPdim(C))
             sum_{Z simple in Z(C)} FPdim(Z)^2 theta_Z^2.

It is therefore invariant under categorical Morita equivalence: the
canonical positive ribbon centers are equivalent and the global dimensions
agree. This uses the positive spherical structures, not a unitary structure.

For the D8 completion, the contribution of its eight invertibles is an
integer b. Equation (3) then implies

    W_2(E)=b+4d.

For either original rank-nine source, all simples outside the four large
dimension-d objects have integral dimension. Their weighted indicator
contribution is consequently an integer a. Non-self-dual large simples
have second indicator zero; self-dual ones have indicator +1 or -1. Hence

    W_2(C)=a+s d,

where s is the sum over the self-dual large objects.

- For R9_2_1607, exactly two large objects are self-dual, so |s|<=2.
- For R9_2_1976, the four large objects are two nontrivial dual pairs,
  so s=0.

Morita invariance would give a-b=(4-s)d. Since a-b and 4-s are integers
and d is irrational, this forces s=4. Both source cases contradict it.

This form of the proof does not even need the precise sign of the
dimension-two TY indicator: its contribution is absorbed in the integer
a. The companion calculation's more explicit equality of the pointed/TY
terms is consistent but unnecessary.

## 5. Scope and remaining case

The two new exclusions are general complex once the archived gates and
exhaustive Morita reduction are retained. The new ingredients proved here
only assume their hypothetical pseudo-unitary representatives and the
specified surviving zero-shift completion.

R9_2_137 has four self-dual large objects. The equation s=4 is compatible
with all four indicators being +1. This argument therefore does not
exclude R9_2_137 and supplies no model for it.

The earlier FS2_AUDIT.md correctly rejected the proposed universal
nondegenerate-quadratic sign inference. The present symmetric-algebra
argument is independent of that unsuccessful approach and supersedes its
then-current conclusion that no R1976 exclusion had yet been established.

## Primary references

- V. Ostrik, arXiv:1309.4822, Theorems 2.5 and 2.13,
  https://arxiv.org/pdf/1309.4822.
- J. Froehlich, J. Fuchs, I. Runkel, C. Schweigert,
  arXiv:math/0309465, Definition 2.22 and Proposition 2.25(ii),
  https://www.math.uni-hamburg.de/home/runkel/PDF/corr.pdf.
- K. Shimizu, arXiv:1208.2433v2, equation (2.7), Definition 2.8 and
  Remark 2.13, for transpose and the ordinary second indicator,
  https://arxiv.org/pdf/1208.2433.
- S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and exponents
  of spherical categories*, Adv. Math. 211 (2007), 34--71, for the
  center-induction indicator formula.
