# Noncommutative rank-nine frontier: 1848 and 1975

## Status

Both **R9_2_1848 and R9_2_1975 remain unresolved as fusion rings**. Their
noncommutativity already excludes braided categorifications. No model,
associator, or general exclusion is claimed here. This continuation derives
new exact Morita reductions and checks additional necessary constraints.

The source tensors are taken, unchanged, from
`../../work/verification_corpus.json`. The existing general-to-pseudo-unitary
existence reductions are used only as existence reductions: no claim is made
that every original category is pseudo-unitary or unitary.

## R9_2_1848: a self-returning Morita reduction

Put `g=b1`, `h=b8=g^3`, and `X=b5`. The invertible group is **C6, not S3**:
`g,g^2,g^3,g^4,g^5 = b1,b4,b8,b3,b2`.
The noninvertibles form a single C6/C2 orbit, have dimension
`d=3+sqrt(11)`, and obey `d^2=2+6d`. The stabilizer is the central subgroup
`{1,h}`; the noncommutativity comes from the inversion action on C6/C2,
not from the group of invertibles. Thus the normal-stabilizer condition for
two-orbit fusion rings is satisfied.

Since `hX=X`, the pointed associator on `<h>` is trivializable: the action
on the simple object X gives a rank-one module category over that pointed
subcategory. Hence A=`1+h` is a connected separable algebra in every
hypothetical categorification. The split-module action has one exact branch,
with nine module simples. The full Morita Gram identity has exactly nine
admissible right-action matrices, with all multiplicities forced to one.
They are linearly independent. Their products therefore determine the
entire Grothendieck ring of the Morita dual.

All 729 coefficients identify that forced dual ring with R9_2_1848 again.
The map from the candidate-matrix order to the original tensor basis is
`[5,6,7,3,1,2,4,8,0]`. Therefore this algebra does not provide a reduction
to a smaller-rank category or a previously excluded ring.

Files: `R9_2_1848_morita_candidates.json`, `1848_dual_raw.json`,
`1848_morita_transport.json`; replay `morita_probe.py` and `verify.py`.
The exhaustive candidate-domain derivation is the existing full Morita Gram
argument in `../../phase3/noncomm_morita.md` and
`../../sources/full_morita_gram.py`, with reversed row-action multiplication
retained throughout.

A second possible direction is equivariantization by the inner order-three
symmetry cycling the noninvertibles, which would give near-group parameters
`(|G|,m)=(18,18)` if the coherent action is supplied. No classification of
all such near-group categories, and no contradiction from those parameters,
is established here. In particular, an odd central Tannakian subgroup is
not generally forbidden in near-group categories.

## R9_2_1975: a finite rank-twelve Morita reduction

Let `h=b5`. It is central as a based-ring element and fixes `b8`, of
dimension two. The same rank-one pointed-module argument provides A=`1+h`.
The exact split-module calculation has one branch and six module simples.
The full Morita Gram system has ten candidate action matrices. Their
multiplicities are uniquely

`[1,1,1,1,1,1,2,2,1,1]`.

Thus the dual has twelve simple objects. Eight have distinct permutation
actions and dimension one. Their multiplication is the dihedral group D8
of order eight: element orders `1,2,2,2,2,2,4,4`. The four remaining simples
have dimension `d=4+3sqrt(2)` and two repeated action matrices. Repeated
matrices must not be merged into two simple objects.

Here is a finite necessary completion of these repeated matrices. Let
`G=D8`, `H=Z(G)=C2`, and `Q=G/H=V4`. Because d is irrational and there are
only two FP dimensions in the dual, the invertible action is transitive on
the four noninvertibles (Schopieray, Lemma 2.6). Their stabilizer is a normal
subgroup of order two, necessarily H. Write them `X_q`, q in Q.

The two distinct module actions define a nonzero homomorphism
`pi:Q -> C2`. Left and right actions have the same pi. If `X=X_0`, its
square has invertible part the coset `alpha H`, where `pi(alpha)=1`.
The standard two-orbit automorphism `theta` of Q preserves pi, has order
at most two, and fixes alpha. An automorphism of V4 preserving pi is either
the identity or exchanges the two elements with pi=1. Hence theta is the
identity. Consequently G commutes with each X_q at the level of classes.

The duality is `X_q^*=X_(q alpha)`. Write

`X^2 = sum_(g in alpha H) g + sum_(q in Q) m_q X_q`.

Duality forces `m_q=m_(q alpha)`. Comparing the two repeated module actions
forces the sum of m_q in each pi-fiber to be four. Therefore, for some
integer a with `0<=a<=4`,

- `m_q=a` on `{0,alpha}`;
- `m_q=4-a` on the other two elements of Q.

There are two possible alpha cosets in the recorded labeling, and five
values of a, hence ten candidate based rings. Relabeling X exchanges a and
4-a, leaving six obvious isomorphism types before applying restrictions.
`build_d8_duals.py` constructs all ten and verifies associativity,
Frobenius reciprocity, and every product of their recorded module actions.
These are necessary alternatives, **not constructed fusion categories**.

### Eliminating four candidates by the FP field

For a=1 or 3, the degree-one characters have formal codegrees
`48+16sqrt(6)` and `48-16sqrt(6)`. Neither belongs to `Q(sqrt(2))`.
In any pseudo-unitary categorification, every formal codegree f satisfies
`dim(A_E)=FPdim(C)/f` for a distinguished central simple A_E. Since its
restriction is an integral combination of simples, this dimension belongs
to the FP-dimension field `Q(sqrt(2))`. Hence f belongs to that field too,
a contradiction. This excludes the four candidate dual rings with a=1,3.
The polynomial `t^2-96t+768` is checked as a factor of the regular Casimir
polynomial; it is from scalar blocks, so there is no missing degree factor.

### Extreme branches and the existing rank-six frontier

For a=0 or 4, the adjoint subring has rank six and multiplicity four.
Exact 216-coefficient transports give:

| alpha label | a | rank-six subring | Existing status |
|---|---:|---|---|
| 2 | 0,4 | R6_4_155 | unresolved |
| 3 | 0,4 | R6_4_1 | excluded |

The second row is ruled out by the project's existing general-complex
exclusion for R6_4_1. That entire lower-rank indicator proof is a dependency;
this continuation checks its tensor binding but does not claim a fresh full
replay of the lower-rank proof. The first row cannot be ruled out: R6_4_155
is one of the current open cases.

The two required lower-rank tensors and their source decision records are
bundled in `lower_tensors.json`, so both `verify.py` and `dual_subrings.py`
replay without a sibling GitHub checkout. Their source is classification
commit `111137a3e3ddf93be340b39c8a7c7b6ea94b844c`. The restored census has
SHA256 `9bb71564082688f1c130050bfe42034431c90dd4f48e0e2d31be8e3a224552ff`;
the decision ledger has SHA256
`abb36cb0e7f9196e0a231cb85a601c82a1c8fd398996f77a8961487a7ca692e5`.
Both hashes were checked against the
[commit-pinned payload manifest](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/111137a3e3ddf93be340b39c8a7c7b6ea94b844c/data/large_files_manifest.json).
The local provenance file gives every immutable payload URL and its hash.
The dependent R6_4_1 categorical proof uses the two-FP-values Galois gate and
finite indicator traces; see the
[commit-pinned rank-six replay instructions](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/111137a3e3ddf93be340b39c8a7c7b6ea94b844c/supplements/rank6/README.md).
The copied decision includes its complete stored scalar certificate, but
this continuation does not re-establish its categorical premises.

Thus, up to the stated relabeling, three alternatives survive: the branch
containing R6_4_155, and the two uniform a=2 D8 quadratic rings. Establishing
or excluding coherent associators for these survivors remains necessary.
This is a useful finite structural reduction, not a resolution of 1975.

## Additional center test

The prior labelled-S, weighted-codegree, Galois-dimension and rotation
system for 1975 has 253 equations and 1291 variables. This continuation
required its variables to be nonnegative **integers**, rather than merely
nonnegative reals. Z3 returned `unknown` after 120 seconds. No feasible
integer witness and no unsatisfiability certificate was obtained. File
`1975_integer_center.json` records the exact system hash, time, and outcome;
`integer_center.py` reproduces the test. A timeout has no classification
consequence.

## Primary references checked

- Andrew Schopieray, *Categorification of integral group rings extended by
  one dimension*, JLMS 108 (2023), 1617–1641,
  <https://doi.org/10.1112/jlms.12789>. Lemma 2.6 and the two-orbit
  normal-stabilizer and quotient-automorphism results; the induction/formal
  codegree relation recalled in Section 3. This is not a classification of
  the candidate D8 categories.
- Jingcheng Dong and Hua Sun, *Structure, examples and classification for
  generalized near-group fusion categories*,
  <https://arxiv.org/abs/2004.08735>. The general structural statements apply;
  the classification conclusions requiring braidings do not exclude the
  present nonbraided cases.
- Pinhas Grossman and Masaki Izumi, *Infinite families of potential modular
  data related to quadratic categories*,
  <https://arxiv.org/abs/1906.07397>. Its potential modular data are not
  categorical existence or completeness theorems for these rings.

`verification.json` records the exact replay. No existing ledger or online
repository has been edited by this continuation.
