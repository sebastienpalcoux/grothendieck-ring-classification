# Independent audit of the two remaining R9 Morita alternatives

Status: PASS as a necessary-condition reduction. R8_1_9 remains unresolved.
Auditor: rank6_center, 2026-10-16.

I independently read R9_MORITA_FRONTIER.md and the entire portable
verify_r9_morita_frontier.py, then replayed the verifier normally and with
Python -O. Both runs passed and produced identical receipts, saved as
r9_independent_normal.json and r9_independent_optimized.json.

The source digest is
1718ab13b6969ed751b621f7303b9e2bb29bb8280f692315499b130a420538f6.

## Categorical module and bimodule arguments

The published two-dimension Galois pseudo-unitarity lemma makes the
pivotal parity argument applicable to an arbitrary categorification.
The two self-dual noninvertibles each have unit multiplicity one in
their cubes, forcing positive second indicator. The same cubes contain
the pointed involution once, forcing its indicator to be positive.
For a positive pivotal pointed C2 category this trivializes its
associator class, so A=1+g is an actual separable algebra.

Each H-by-H orbit has two objects and stabilizer C2. Its projective
stabilizer representations are both one-dimensional, since
H^2(C2,C*)=0. Thus each orbit contributes two simple A-bimodules.
Their categorical dimensions are the dimensions of their underlying
objects divided by dim(A)=2, giving four invertibles and four objects
of dimension d.

The nontrivial dual character beta is an invertible A-bimodule of
order two. Tensoring by it interchanges the two stabilizer characters
over each support orbit. An invertible over the other pointed orbit
interchanges the two noninvertible support orbits. Together these
actions are transitive on all four noninvertibles; an order-four group
acting transitively on four elements acts freely. This proves the
quadratic-ring hypothesis without assuming it from the census.

The four-object right-module representation is the regular 2D2 based
module. Its first column is cyclic, so the commuting action of an
A-bimodule is determined by the support of its underlying right
A-module. The two objects above each support have the same matrix.
This gives exactly the beta-quotient restrictions on tau, g0, and the
two coset sums of m used in the verifier. The enumeration exhausts
both order-four groups, all their automorphisms, all g0, and all
compositions of four; it does not impose an unproved multiplicity bound.
The finite full-axiom check returns 22 abstract tensors and the stated
nine module-compatible tensors.

## Total second indicators

For the canonical positive pivotal structures, summing the
Ng--Schauenburg center formula with weights dim(X) gives

    sum_X dim(X) nu_2(X)
      = (1/D) sum_Z theta_Z^2 dim(Z)^2.

The canonical braided Morita equivalence preserves all data on the
right, so this total is Morita invariant. The source total is 2+2d.
The exact cube and duality checks in the verifier correctly eliminate
R15/R69 (coefficient4 of d) and R12/R53 (coefficient0 of d).
After the separately established exclusions of R25, R478 and R49,
the only tensor possibilities are R9 and R477. In R477 the coefficient2
forces three positive and one negative noninvertible indicators.

I also checked the pointed class separation. For original C4 class0,
the subgroup dual has the explicitly verified mixed V4 cocycle with
one negative pointed indicator. For class2 its FS exponent is8,
which no pointed V4 category can have; hence its dual pointed group
is C4, again class2. The proof appropriately retains both resulting
categorical possibilities rather than interpreting them as constructions.

Finally, Grossman's actual factor involution phi is the dual action
of the original C4 Haagerup--Izumi orbifold. Its R477 crossed extension
is Morita equivalent to that original R15 category and has total
2+4d. It therefore cannot realize the required R9 indicator pattern.
The note correctly distinguishes this concrete failure from an
exclusion of every possible R477 associator.

This audit relies on the existing source-bound exclusions of R25,
R478 and R49; it does not re-prove those independent results. No
classification count changes follow from this frontier reduction.
