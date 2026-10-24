# Independent audit of the signed criteria and folded SO(3) obstruction

Audit date: 2026-10-23. This review re-read the primary arguments and inspected
the discovery and verification code. It does not use the previous audit's
approval as a premise. Fresh exhaustive solver replays are owned by the root
agent and are separate from this categorical audit.

## Conclusion

The nine signed exclusions and twenty signed Galois-to-pseudo-unitary gates
have valid categorical foundations and use the correct full signed domains.
The folded SO(3) argument for R9_2_920 is valid after explicitly adding the
odd-boundary presentation argument below. This is an omitted proof step that
has a short repair, not a counterexample to the claimed obstruction. No
phase-two source file was changed by this audit.

The audit also checked that the signed `original_gauge` branches use the
direct arithmetic/induction spherical report from `sphere.analyse`, rather
than the incomplete lower-positive registry. Consequently the newly found
half-E6 registry omission does not invalidate these signed certificates.

## Signed sphericalization: hypotheses and scope

For an arbitrary complex fusion category, canonical sphericalization supplies
two lifts of each simple and a central object epsilon with dimension -1.
Their dimensions are opposite and nonzero. The latter fact follows from the
nonvanishing squared norm of a simple; it is not a positivity assumption.
Dual-compatible choices exist: in a spherical category a simple and its dual
have equal dimension, whereas the other lift has its negative. In particular
a selfdual original simple has selfdual lifts.

In the epsilon=-1 quotient the coefficient of a lifted product is the
difference of the two nonnegative multiplicities whose sum is the original
multiplicity N. Its domain is exactly {-N,-N+2,...,N}. The implementation keeps
all three values -2,0,2 when N=2. Choosing the unit lift and dual-compatible
lifts gives unit coefficient delta(i,j*), dual reversal, and cyclic Frobenius
reciprocity. No commutativity or Frobenius-Schur indicator hypothesis enters.

Dimension is a scalar character of this signed quotient. Since every basis
dimension is nonzero, every basis-word product is nonzero. Thus the added
degree-two nonzero-product disjunction is necessary. It does not delete a
possible categorical branch.

For any admissible signed table the real regular algebra is a finite
dimensional star algebra: transpose of left multiplication by x_i is left
multiplication by x_i*. The coefficient-of-unit pairing is the positive
Euclidean pairing on the chosen basis. Hence the algebra is semisimple even
though some structure constants are negative. The scalar-character routines
are therefore entitled to use its semisimple decomposition.

## Formal codegrees, fields, norms, and integral dimension lattices

The complexified Grothendieck algebra of sphericalization splits into its
epsilon=+1 and epsilon=-1 summands. The formal codegrees of each quotient,
unsigned or signed, are multiplied by 2 in the doubled based algebra.
The squared global dimension calculation similarly gives
dim(sphericalization)=2 Delta, where Delta=sum_i d_i d_(i*) is the intrinsic
global dimension of the original category. These factors cancel.

Ostrik's induction theorem for a spherical category gives a central simple
A_E with dimension dim(C)/f_E and multiplicity dim(E) in I(1). It does NOT
insert another factor dim(E) into the dimension quotient. Thus, for either
signed or unsigned quotient here, the necessary central dimension is
Delta/f_E. Forgetting to sphericalization places it in the integer span of
the chosen dimensions and their negatives, namely the same Z-span of d_i.
This proves the field and dimension-order tests used in the code. It also
explains why both unsigned and signed formal-codegree factors are tested.

The Casimir eigenvalue on an irreducible representation E is dim(E)*f_E.
The noncommutative rank-nine implementation correctly divides the eigenvalue
of a matrix block of size two by two. Its scalar rank possibilities 0,1,5,9
are the possible Wedderburn decompositions in dimension nine.

The norm test is also necessary: if Delta/f is an algebraic integer, then
for every rational prime p,

  v_p(Norm(Delta))/[Q(Delta):Q] >= v_p(Norm(f))/[Q(f):Q].

This follows by taking the norm in a common overfield. It requires neither
equality of the two fields nor integrality of each individual conjugate ratio
over a smaller field. The exact code cross-multiplies this inequality.

For the field test, inclusion Q(f) in the scalar-character field implies the
degree divisibility test. At a prime where a monic defining polynomial of the
larger field splits into distinct linear factors, the prime is unramified and
completely split in that field and hence in each subfield. A nonlinear factor
of the minimal polynomial of f at this prime contradicts inclusion. The
squarefree requirement prevents a bad-prime shortcut.

The d-number condition on a signed formal codegree follows from the genuine
sphericalization codegree 2f: invariance of the generated ideal under Galois
conjugation is unchanged by rational scaling. All tested codegrees are
algebraic integers in the rationally based algebra. No unitarity assumption
is hidden in this step.

## Exhaustiveness and gauge checks

`signed_problem_data.py` imposes precisely cyclic Frobenius and dual-reversal
orbits. Dual-compatible signs act by epsilon_i epsilon_j epsilon_k on a
coefficient. The independent sign characters selected for gauge fixing can
simultaneously be made nonnegative; zero coordinates cause no obstruction.
Only source permutations checked against every structure constant are used
as based automorphisms.

The bit-vector verifier retains all parity-allowed values. Each uncontracted
associativity difference contains at most two sums of nine products, each
product of absolute value at most four. Its absolute value is therefore at
most 72. Equality modulo 256 is equivalent to integer equality here. The
`tensor` reconstruction additionally checks all integer associativity
equations independently by integer array contraction. Each discovered orbit
is blocked using exactly verified basis signs and based automorphisms; final
UNSAT is a completeness statement after those reductions.

The common-kernel construction used for scalar characters extracts all and
only one-dimensional simple blocks of the semisimple algebra. A polynomial
separating element is chosen from enough integer parameters: two distinct
characters collide at at most seven values, and at most C(9,2)*7=252 values
are bad. The trial allowance exceeds this bound.

If a signed tensor is a sign gauge of the unsigned tensor, choose the
corresponding lifts. Saturation with the correct signs means every summand
of each product is a chosen lift; it does not merely mean absolute values
match. These lifts form a spherical tensor-closed section of the forgetful
functor. The original ring then has a spherical categorification, justifying
the original spherical obstruction. This does not assume pivotality of an
arbitrary categorification.

## Galois pseudo-unitarity

Davidovich-Hagge-Wang Proposition 4.3 applies to fusion categories, not only
modular ones: a fusion category admits a model over a number field. Intrinsic
squared norms and their sum are algebraic and transform under scalar
extension. If every possible signed dimension character has global dimension
with the same irreducible minimal polynomial as FPdim(R), extend an embedding
of that number field sending Delta to the positive FP root to an automorphism
of the algebraic closure. Twisting all structural constants preserves the
based fusion ring, and its intrinsic global dimension becomes FPdim(R).
ENO Proposition 8.23 then supplies the canonical positive spherical structure.

Thus the result is a justified Galois reduction to a pseudo-unitary
categorification, not an assertion that the initial category itself is
pseudo-unitary. The code compares exact irreducible minimal polynomials, not
floating-point dimensions. Dimensions are not confused with squared norms.

## Folded SO(3): the needed presentation repair

The local MPS determinant arguments require only the actual invariant-space
dimensions through degree four and the nondegenerate spherical pairing. They
do not require that the trivalent vertex generate every ambient morphism.
The symmetry and rotation arguments are local for the same reason. For the
folded ring, d=1+2 cos(pi/(2n))>2 and the explicit three-tree Gram determinant
d^3(d^2-d-1) is nonzero. The local relation therefore holds as an actual
morphism identity in the hypothetical category, not only modulo a trace
radical of a smaller diagram space.

Fendley-Krushkal's chromatic algebra C_m has 2m boundary points. Its injective
map into the p_2 corner, combined with the Riordan dimension calculation,
gives the full even-total-boundary spaces. Bending alone does not prove the
corresponding claim for odd-total-boundary spaces. The sentence making that
claim in phase two should be replaced by the following argument.

Let W=p_2 in the unsemisimplified Temperley-Lieb Karoubi category. The
normalized trivalent maps s:W->W tensor W and r:W tensor W->W satisfy r s=id_W;
their bigon scalar is nonzero since d-1 is nonzero. For odd k>=1, splitting
one boundary gives an injection

  Hom(1,W^k) -> Hom(1,W^(k+1))

with retraction given by collapsing the same split. The even-total-boundary
space on the right is spanned by trivalent diagrams by the chromatic-corner
argument. Composing those diagrams with the trivalent retraction spans the
space on the left. This also includes the zero space for k=1. Bending then
covers every Hom(W^a,W^b). The same split/retract argument transfers any
relation to the even-boundary presentation, so no additional odd-boundary
relations are omitted. This completes the required full presentation and
the pivotal functor before semisimplification.

At the root q=exp(pi*i/(4n)), the Jones-Wenzl idempotent p_(4n-1) exists and has
trace zero. Tensoring it with one fundamental strand gives an even object P
of dimension zero. A pivotal functor into the canonical positive spherical
category kills this object. Goodman-Wenzl's generator theorem and parity
show that every even negligible morphism factors through P tensored with an
even object, using domain braiding only. This does not assert that arbitrary
trace-zero morphisms vanish, nor use an odd-root variant of the ideal theorem.

After descent, the dominant functor from PSU(2)_(4n-2) has right-adjoint algebra
1+f. Bruguières-Natale's central-algebra result applies to a dominant tensor
functor without requiring it to be braided or normal. The even SU(2) category
has trivial universal grading, so an invertible's possible central lifts form
a trivial torsor. The sole lift of f is the transparent fermion supplied by
the standard braiding. Commutativity makes f*f->1 zero. The resulting
square-zero ideal gives a nonsplit right-module sequence, contradicting
semisimplicity. Separability is therefore used correctly, and the central
lift is not arbitrarily assumed to be the standard one.

Together with the independently complete signed gate for R9_2_920 and its
exact full-tensor identification, this proves the general complex exclusion.

## Primary references checked

- Etingof-Nikshych-Ostrik, On fusion categories, squared norms,
  sphericalization, and Proposition 8.23: https://arxiv.org/abs/math/0203060
- Ostrik, On formal codegrees of fusion categories, Theorem 1.2 and the
  Casimir formula: https://arxiv.org/abs/0810.3242
- Ostrik, Pivotal fusion categories of rank 3, Theorem 2.13 and Corollaries
  2.14-2.15: https://arxiv.org/abs/1309.4822
- Davidovich-Hagge-Wang, On Arithmetic Modular Categories, Proposition 4.3
  and scalar-extension discussion: https://arxiv.org/abs/1305.2229
- Morrison-Peters-Snyder, Categories generated by a trivalent vertex,
  Lemma 2.2, Propositions 4.1 and 7.1, Lemma 4.11:
  https://arxiv.org/abs/1501.06869
- Fendley-Krushkal, Link invariants, the chromatic polynomial and the Potts
  model, Theorem 4.3 and Lemmas 4.4,7.1: https://arxiv.org/abs/0806.3484
- Goodman-Wenzl, Ideals in the Temperley Lieb Category, Proposition 2.1:
  https://arxiv.org/abs/math/0206301
- Bruguières-Natale, Exact sequences of tensor categories, Proposition 5.1
  and Corollary 5.6: https://arxiv.org/abs/1006.0569
