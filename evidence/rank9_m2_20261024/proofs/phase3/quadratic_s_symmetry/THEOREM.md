# Distinguished central characters and quadratic S symmetry

Let C be pseudo-unitary with commutative Grothendieck ring R, global dimension
D, and FP dimension field K=Q(sqrt(q)). Let chi_h run over any subset of the
scalar characters of R whose values lie in K. Define the formal codegrees
f_h=sum_i chi_h(b_i) chi_h(b_i*) and d_h=D/f_h.

The distinguished central simple A_h in I(1) associated to chi_h has dimension
d_h and occurs once. Write v_h for the restriction vector of A_h. The central
character formula gives

    S_(A_h,Z) = d_h chi_h(F(Z)).

This follows, for example, by specializing Deshpande, *On centers of bimodule
categories and induction-restriction functors*, Corollary 2.18 to the identity
bimodule and inverting character orthogonality; compare Ostrik, *Pivotal fusion
categories of rank 3*, Theorem 2.13. The S matrix is symmetric. Consequently
every pair of selected characters obeys

    d_h chi_h(v_k) = d_k chi_k(v_h).

These are linear equations in the unknown restriction vectors. Expanding each
side in 1,sqrt(q) gives rational equations without numerical embeddings.

In the pre-existing joint center relaxation every candidate low column v has
v_0=1, twist one, and dimension z=D/f for some formal codegree, but only its
dimension count is retained. Replace its variable by one variable for each
selected character h with d_h=z. If there are more formal codegrees of that
dimension than selected characters, retain one additional anonymous variable
for the remaining low simples. Require the total weight for each selected h
to be exactly one. Keep all original Gram, dimension-count, twist trace,
Galois dimension-balance and rotation equations, then append the displayed
S-symmetry equations.

Every actual category supplies such a solution by assigning each distinguished
simple its character label. The replacement duplicates candidate columns;
it does not assume that a low frame is already known or that anonymous
characters have rational values. Relaxing the labelled choices to nonnegative
real weights remains necessary. Hence a verified Farkas separator for this
system is a valid pseudo-unitary obstruction. A separately verified
Galois-pseudo-unitarity gate extends it to all complex categorifications.

The implementation extracts degree-one and degree-two scalar-character
components. A quadratic component is selected only if its discriminant square
class is exactly q; both embeddings are included. Every selected vector is
checked against every source multiplication equation, and its codegree and
central dimension are recomputed exactly. Characters in other fields remain
anonymous, with their full remaining dimension counts.

## Optional duality refinement

Selected characters are dual-invariant, checked exactly in the code. Therefore
S_(A_h*,Z)=S_(A_h,Z*)=d_h chi_h(FZ*)=S_(A_h,Z). Nondegeneracy then implies
A_h is self-dual. Thus its restriction
vector must satisfy v_i=v_(i*). This allows discarding nonsymmetric candidate
vectors for those labels.

Every other central simple Z has a dual with restriction vector v_(i*) and the
same twist. The latter is equality, not complex conjugation: the ribbon axiom
uses the complex-linear dual of the scalar twist map. Consequently paired
restriction vectors have equal multiplicities at each joint normalized twist
packet. In the LP this can be imposed without adding rows by replacing the
two corresponding columns with their sum. Fixed columns are retained once.
Anonymous low labels are closed under duality because all explicitly selected
labels are self-dual. Unknown indicator and rotation variables are untouched.

This optional refinement is marked `central_duality_orbits=true`. The initial
candidate exclusion for R9_2_516 at height 3 does **not** require it.

## Verification and status

`quadratic_s_symmetry.py` builds the exact systems. Floating-point LP only
proposes a ray, and the saved ray is checked with integer arithmetic against
every column. A result remains
`candidate_exclusion_pending_independent_audit` until separately reviewed.
The known categorical model R9_2_1983 survives both the height-three system and
the height-six duality refinement. Feasibility is recorded as a control, never
as a proof of a new model.

The ten old commutative quadratic residuals are 114,128,137,516,1487,1607,1635,
1636,1959,1976. Noncommutative 1848 and 1975 are outside the theorem's scope.

Primary sources:

- https://arxiv.org/pdf/1611.04486, Corollary 2.18 and section 4.3.
- https://arxiv.org/pdf/1309.4822, Theorem 2.13.
- The detailed audit of the inherited center, arithmetic and trace constraints
  is `../audit_center_morita/AUDIT.md`.
