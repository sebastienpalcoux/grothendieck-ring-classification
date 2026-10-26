# Dimension 32 family: second-round theoretical work

All twenty supplied unresolved rings in this family were addressed. None is
newly excluded or modeled by the completed attempts recorded here. Their
unchanged status is **unresolved**, not a claim of nonexistence.

The permanent IDs are 128,144,147,173,237,240,275,285,294,301,318,408,412,
415,419,422,431,524,530,536, with prefix R12_1_. The machine-readable
`d32_summary.json` binds every tensor hash, exact dimension character,
adjoint series and structural hypotheses to its permanent ID.

## Unified categorical structure

Every ring has dimensions 1^8, 2^2, (sqrt8)^2, global dimension32 and the
adjoint series of dimensions 32,16,4,1. Its integral adjoint subcategory is
rank10 and dimension16; it is generalized Tambara–Yamagami (eight
invertibles and two dimension-two simples). The next adjoint category is
pointed of dimension4. Any categorification is therefore nilpotent and
unitarizable. Independently, the general solvability theorem at prime-power
global dimension and GHR Theorem5.20 supply the same unitary bridge.

There are eight noncommutative rings, with invertible group D8 or Q8, and
twelve commutative rings, with invertible group C4×C2 or C2^3. The precise
central involution actions are retained. In particular, several potential
descent patterns occur; the existence of a suitable central boson must not
be inferred from based centrality alone.

## Completed established-criterion attempts

Localized primary-four was screened on all subsets of size two and three,
on all20 cases and the four known positive controls. Localized primary-five
and primary-six were also screened on all subsets of size two. No exact
negative quadratic form was found. The tiny negative floating eigenvalues
are at roundoff scale; they assign no classification status. No exact
positive-semidefinite certificate is claimed. These tests use HLPW,
arXiv:2210.00792, Theorems3.12 and4.1, with the above proved unitary bridge.

The bilateral full-stabilizer squared-dimension quotient was also checked:
for a constituent Z of X⊗Y, use the largest invertible subgroups fixing X
and Z on the left, and Y and Z on the right. Every rational quotient
m² FPdim(Z)²/(|H_L||H_R|) in these rings is integral. This branch gives no
negative witness.

## Actual generalized-Ising actions: completed finite construction attempts

The sixteen first-round positive Liptrap categories of type1^8,(sqrt2)^4
have dimension16. A coherent involution fixing four invertibles and acting
freely on their four odd simples would give a rank12 equivariantization of
the desired dimension pattern. The relevant70 based involutions were
enumerated structurally from group automorphisms and the transitive odd
action. This is only a list of candidate permutations, not categorical
actions by itself.

First, preservation of the entire retained Liptrap data was tested. None
of those70 permutations preserved the saved normal reconstruction on the
nose. This means no strict action was found in that gauge; it is not an
obstruction to a tensorator.

Next, every nonzero associator coefficient was reconstructed from
Liptrap Lemma5.4. The unknowns were only unitary scalar tensorators and
coherent square isomorphisms for the candidate functor. The equations are
linear in root-of-unity exponents:

J(i,j;e)+J(e,k;l)−J(j,k;f)−J(i,f;l)
  = phase(F(pi,pj,pk;pl,pe,pf))−phase(F(i,j,k;l,e,f)),

eta_i+eta_j−eta_k=J(i,j;k)+J(pi,pj;pk),

eta_pi=eta_i.

The first scan solved them modulo128 and varied all invariant tensor
characters of the identity, giving32 distinct constructed tensors. The
second scan prescribed every H²(F,C2) class on the order-four fixed
invertible subgroup F, using exact linear equations modulo256 and batched
right-hand sides. It considered362 action/class systems and produced28
distinct tensors. Successful solutions were checked against all original
equations, and their equivariant fusion tensors were reconstructed by exact
character projections. No new exact match to the twenty target tensors was
obtained. Some output categories can have higher multiplicities, so this
does not classify every output as one of the known multiplicity-one rings.

This is a construction search starting from explicit existing associators,
not a search for solutions of the pentagon. Failed finite-modulus systems
and the use of one saved categorification per based ring are explicit
limitations; no such failure is an exclusion.

## Choi–Lu–Sun extension: a concrete route examined and a remaining gap

The known rank-six category R6_2_69 has dimensions1^4,2,sqrt8 and is a
C2-extension of Rep(H8). Choi–Lu–Sun, arXiv:2310.19867v2, Section7.1 and
Tables3–4, give eight actual categories with these rules. A genuinely soft
tensor involution fixing all object labels, with nontrivial action on the
two-dimensional fusion channels, could in principle split the multiplicity
two and produce a new rank-twelve multiplicity-one category.

The immediate safe inner-action construction does not do so. For g=a,b,ab,
the inner action Ad_g exists, and its equivariantization is the relative
center at Vec_<g>. On Hom(N⊗D,D), its half-braiding transport is

K=F(g,N,D)^(-1) F(N,g,D) F(N,D,g)^(-1).

In Table3 the values for g=a,b,ab are iI,iI,−I. Table4 reverses the two
imaginary signs but leaves these matrices scalar. Hence each corresponding
stabilizer projection retains either zero or two copies; it cannot split
this channel into multiplicity one. An inner action must not be promoted
to the desired model merely because it fixes the object labels.

A non-inner soft action requires its full matrix tensorator and coherent
square, checked against the published multiplicity-two associators. No
such action has been established in this work. This is a remaining
categorical gap, not an accepted construction.

Other possible constructions require either additional generalized-Ising
associator classes, a genuinely forced central-boson descent, or explicit
invertible bimodules over the integral dimension16 neutral category with
their ENO obstruction data. H4(C2,U1)=0 removes only the final obstruction;
it does not establish a missing bimodule or its order-two multiplication.

## Included research code

- `ising_equivariants.py`: strict-data actions and invariant characters.
- `gauge_actions.py`: reconstructed associators and exact scalar action
  equations, including independent action replay.
- `cocycle_actions.py`: all fixed-subgroup extension classes for those
  saved inputs, solved in batches.
- `primary4.py`, `higher_primary.py`: short localized necessary tests.
- JSON receipts and logs: attempted systems and exact/no-conclusion scope.

The downloaded source notebook and PDF page images were for internal
inspection only; they need not be included in a deliverable. The primary
paper remains available at https://arxiv.org/abs/2310.19867.
