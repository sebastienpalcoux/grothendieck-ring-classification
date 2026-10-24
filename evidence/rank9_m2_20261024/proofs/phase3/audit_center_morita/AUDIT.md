# Independent adversarial audit: center and Morita exclusions

## Verdict

**PASS for all 21 exclusions audited here.** No incorrect exclusion, omitted
candidate domain, unjustified positivity assumption, or weakly-group-theoretical
hypothesis was found. This conclusion concerns the 19 center exclusions and two
Morita exclusions listed below; it is not an endorsement of the separate baseline
lower-subring registry. In particular, none of these proofs depends on that
registry or on its erroneous omission of the half-E6 ring.

One exposition clarification is required when citing the d-number restriction:
Ostrik's theorem is about **squared norms**, not arbitrary FP dimensions of
braided simples. The additional pseudo-unitarity and integral-closure argument
given below makes the restriction used here valid. No numerical result changes.

| Family | IDs | Fresh verification |
|---|---|---|
| Integral joint center | 301,352,385,725,727,1028,1134,1238,1448,1465,1501,1712,1778,1989 | Complete Python raw domains and integer rays |
| Integral center with modular filter | 366 | Same, plus independent SymPy characteristic polynomials |
| Quadratic joint center | 1569,1886 | Complete Python raw domains, independent arithmetic filters, integer rays |
| Quadratic neutral block | 500,1235 | Complete neutral domains, independent arithmetic filters, integer rays |
| Split-involution Morita | 396,1265 | Independent bounded-bitvector anti-module enumeration and rebuilt Gram certificates |

All source tensors were read afresh. Discovery LP output was never accepted as
proof. Phase-2 files were left unchanged.

## 1. Scope and pseudo-unitarity

For the integral cases the FP global dimension is an integer, so ENO,
*On fusion categories*, Proposition 8.24 makes every hypothetical
categorification pseudo-unitary; Proposition 8.23 supplies the canonical positive
spherical structure. This uses no group-theoretical classification. Integrality
of every source dimension then implies integrality of the dimensions of central
simples because the forgetful functor preserves FP dimensions.

For 1569,1886,500,1235 the center argument is explicitly pseudo-unitary. The
separate exhaustive signed Galois-pseudo-unitarity gates are essential to extend
it to all complex categorifications. They are not inferred merely from quadratic
FP dimensions. The independent signed-foundation audit is in
`../audit_signed_so3/AUDIT.md`.

The Morita argument uses only FP dimensions and semisimple module categories. It
needs neither pivotality nor pseudo-unitarity.

## 2. Induction Gram data and low columns

Every audited center tensor is commutative. With regular matrices N_i and
forgetful multiplicities v_Z,i, adjunction and the explicit underlying object
of induction give

    B = sum_i N_i N_i^t = sum_Z v_Z v_Z^t.

The source unit contributes N_0=I, so B is positive definite. Therefore every
nonzero nonnegative integer column obeys both entrywise inequalities
v_i v_j <= B_ij and v^t B^-1 v <= 1. These imply finite coordinate bounds
v_i <= floor(sqrt(B_ii)). No cutoff on dimensions or unknown central rank is
silently imposed.

Ostrik, *Pivotal fusion categories of rank 3*, Theorems 2.5 and 2.13, apply to
arbitrary spherical fusion categories despite the paper's title. Since the
source ring is commutative, all scalar irreducible characters have degree one:
the simples in I(1) have v_0=1, twist one, and dimensions D/f_h. There are no
other v_0>0 columns. Repeated formal codegrees supply repeated counts; they are
not collapsed into a single occurrence. The programs impose exactly these
dimension counts. Characteristic-factor computations independently confirm the
quadratic multiplicities.

## 3. Arithmetic filters

For a central simple of dimension z, modularity gives the algebraic integer
D^2/z^2. Hence D/z is an algebraic integer: it is integral over the ring of
algebraic integers by its monic quadratic equation, and that ring is integrally
closed. In the integral cases it is rational, hence an integer; thus z divides
D and z<=D. This is not the unproved general assertion that every simple FP
dimension divides the dimension of its source category.

Ostrik, *On formal codegrees of fusion categories*, Theorem 1.8 proves that the
squared norm of a braided simple is a d-number. His Remark 1.9 cautions against
the stronger unrestricted FP-dimension assertion. In the present pseudo-unitary
center the squared norm is z^2. For every Galois automorphism sigma,
(z/sigma(z))^2 is a unit in the ring of algebraic integers. Integral closure
then makes both z/sigma(z) and its inverse algebraic integers. Thus z itself is
a d-number. In a quadratic field, writing z=a+b sqrt(q), the nonrational
d-number test is precisely that 4a^2/(a^2-q b^2) is an integer. The program's
trace-and-norm integrality test is also exact in every quadratic field; no
incorrect Z[sqrt(q)] assumption is made when q=1 mod 4.

For the modular operator test, the eigenvalues of

    (D/z) B^-1 N_v

are the S-ratios S_(A_h,Z)/z (up to an immaterial dual permutation of h).
Deshpande's Corollary 2.18, specialized to the identity bimodule, and character
orthogonality give S_(A_h,Z)=(D/f_h) chi_h(FZ). By symmetry of S these ratios
are fusion-character values on A_h, so are algebraic integers. Therefore the
characteristic polynomial has integral coefficients over Q, or algebraic
integer coefficients in the quadratic field. This argument requires neither a
braiding on the source nor a splitting field for its characters.

For 366, all 3474 pre-filter columns were independently tested using SymPy
instead of FLINT; exactly the same 299 survive. For 1569/1886 the quadratic
arithmetic and characteristic-polynomial tests were independently recalculated
as symbolic expressions, recovering 151 columns before the modular test and
120 final columns. For 500/1235 the modular filter removes no column at all;
their contradictions already use the full arithmetic-admissible column set.

## 4. Galois dimension pairing

In a pseudo-unitary modular center the normalized S matrix is S/D. Its Galois
symmetry permutes columns with signs. For the nontrivial quadratic automorphism,
central dimensions are therefore permuted by

    z -> abs((D/sigma(D))*sigma(z)).

The absolute value is justified by positive dimensions, and it is evaluated
exactly. Thus missing partners exclude a dimension and the multiplicities of
distinct paired dimensions agree. The map on positive dimensions is an
involution. The ordinary quadratic system correctly imposes these restrictions.
The neutral-block system correctly omits them, because a Galois permutation
could leave the retained block.

## 5. Indicator identities, signs and complete trace packets

Ng--Schauenburg, *Frobenius--Schur indicators and exponents of spherical
categories*, Theorem 4.1, gives

    sum_Z z_Z v_Z,i theta_Z^n = D nu_n(X_i).

The first indicator vanishes on nonunit simples. The second is zero on
nonselfdual simples and +/-1 on selfdual simples. The extra +1 rule for an odd
occurrence in Y tensor Y* is sound in a pivotal category: Y tensor Y* has its
canonical symmetric self-duality, and a skew self-dual simple can occur in a
symmetric object only with even multiplicity. This argument uses duality and
the pivotal structure, not Hilbert-space unitarity. Unknown second-indicator
signs are relaxed to [-1,1], which can only enlarge the feasible set.

The Cauchy theorem of Bruillard--Ng--Rowell--Wang, Theorem 3.9, bounds prime
support of the FS exponent by the prime divisors of the norm of D. It does
not bound the exponent itself. The implementation handles all exponents: after
normalized trace to K=Q or Q(sqrt(q)), all nonzero joint packets through height
H occur among divisors of

    product_p p^(max(v_p(conductor(K)),1)+floor(log_p H)).

An order beyond any such valuation has zero relative trace for every power
1,...,H; this follows by averaging over the kernel at that prime-power level.
The all-zero packet is explicitly included. Thus this is an exhaustive finite
trace list, not an empirical conductor cutoff. One common phase sign is kept
across the whole packet, preserving correlations between its powers.

An independent script averages actual cyclotomic monomials over the exact
automorphisms fixing K, reducing modulo the cyclotomic polynomial. It agrees
with every packet used here: rational prime supports {2,3} and {2,3,7} give
11 and 21 packets at height 4; q=2 gives 8 and q=6 gives 15 at height 3.
The first layer beyond each prime-power bound also directly gives zero.
Third-rotation packets agree independently as well.

For integral systems, normalized traces of n-th roots lie between
-1/(p_min(n)-1) and 1, giving the implemented bounds using the exact dimension
of Hom(1,X_i^n). For the quadratic systems the actual joint rotation packets
are used. At accepted height 3 there is only the ordinary third indicator,
so no higher tensor-power identity is needed for these exclusions. Unknown
rotation eigenvalue multiplicities are relaxed to nonnegative real weights.

## 6. Neutral-block relaxation

For 500/1235 the source FP field is quartic, while global D and the retained
six simple dimensions are quadratic. Exact arithmetic verifies membership in
the quadratic subfield, closure under products and duals, and zero cross-block
entries of the **ambient** B. Since v_i v_j<=B_ij with nonnegative v, each
central restriction vector is supported in just one block. Consequently all
discarded columns have zero coefficient in the retained Gram equations and
every retained tensor-power indicator equation. Every I(1) column lies in the
retained block because the unit lies there.

The code uses ambient D, all ambient codegrees, and ambient modular operators.
It never replaces these by the data of the rank-six subcategory. All D/f_h
are verified to lie in the quadratic subfield. Relative averaging to that
field is legitimate for all retained terms. Discarding the other equations
is a necessary relaxation, not a sufficiency claim.

Each complete neutral box has 5600 vectors, 432 passing Gram tests and 102
passing arithmetic tests. Both exact rays give b^t y=-896 and A^t y>=0.
The known model 515 supplies an independently rebuilt exact nonnegative
rational feasible vector for the same generic construction: 61 equations,
2207 variables, 50 nonzero coordinates.

## 7. Morita foundations and complete domain

For 396 and 1265, the chosen invertible involution g fixes three simples.
The one-simple orbit is a rank-one module category over Vec_(Z/2)^omega,
forcing omega to be a coboundary. Therefore A=1+g exists as a connected
separable algebra. This conclusion does not assume g is central or bosonic.

Right A-modules consist of one module for each free orbit and two structures
on each fixed simple. The algebra automorphism g->-g gives an involution on
this module category commuting with the left source action. Its anti-invariant
blocks T_i obey the stated finite parity and magnitude bounds, the full fusion
relations, T_0=I and T_(i*)=T_i^t. Swapping the two structures on fixed simples
is precisely diagonal-sign gauge. There is no requirement that these blocks
be positive or that multiplicity-two entries be +/-2; zero is included.

A fresh independent 8-bit encoding, with no discovery-variable identifications,
exhaustively enumerated the equations. Integer matrix-product entries have
absolute value <=12 and fusion-linear entries <=36, so differences cannot
wrap modulo 256. Each ring has exactly 18 diagonal-sign orbits, identical to
the saved full domain, with a fresh UNSAT conclusion after blocking all orbits.

The reconstructed nonnegative action matrices L_i have their full fusion and
duality relations checked. In the Morita bicategory, associativity and rigidity
give the Gram identity for the unknown right action matrices R_j:

    sum_j R_j(a,d) R_j(b,c) = sum_i L_i(b,a) L_i(c,d).

This supplies the full positive semidefinite integer Gram matrix and its
partial slices. At the distinguished module A its first-column Gram is
I+L_g. Since L_g is an involutive permutation, its nonnegative integer Gram
decomposition is forced: two singleton columns per fixed point, and one
two-entry column per transposition. No simple right-action column at A can
vanish, because its underlying A-bimodule is nonzero. This determines the
dual rank and FP dimensions. No categorical-dimension integrality or Morita
invariance of pivotal structures is used.

The full-vector candidate algorithm restricts to the rational image of the
Gram matrix, fixes allowed first rows and columns, enumerates independent
integer coordinate boxes bounded by the diagonal, and checks every resulting
entry. The partial algorithm similarly exhausts the relevant affine dimension
equations. Repeated right action matrices are allowed through multiplicities.
Thus neither faithfulness of the fusion-ring action nor independence of the
right action matrices is assumed.

Every rebuilt branch fails: seven by rank, ten by partial Gram separation,
one by full Gram separation. All separating inequalities were checked exactly.

## 8. Reproducibility and limits

Fresh receipts are `center_fresh.json`, `morita_fresh.json`,
`trace_packets_fresh.json`, `controls_modular_fresh.json`, and
`quadratic_filters_fresh.json`. The accompanying Python scripts reproduce
them without modifying phase 2. Native enumerators were compared with
independent Python integer domains; characteristic-polynomial filters were
cross-checked using a second exact implementation. Floating-point optimization
was not used by this audit.

The source hypotheses and code loops were reviewed separately from their
numeric replays. An exact replay alone cannot certify a theorem's applicability;
the arguments above supply that part. A feasible relaxation does not provide a
categorical model, and no unresolved case was promoted merely for surviving it.

Separate new artifacts `gate_R9_2_{96,97,98,1266,1489}.json` and their verification
files establish Galois-pseudo-unitarity for five restored cases. These are gates,
not exclusion or model conclusions. Their subsequent classification is owned
by the other project branches.

## Primary references inspected

- Etingof--Nikshych--Ostrik, *On fusion categories*, propositions 8.23--8.24:
  https://arxiv.org/pdf/math/0203060
- Ostrik, *Pivotal fusion categories of rank 3*, section 2, especially theorems
  2.5 and 2.13: https://arxiv.org/pdf/1309.4822
- Ostrik, *On formal codegrees of fusion categories*, theorem 1.8, remark 1.9,
  lemma 2.7: https://arxiv.org/pdf/0810.3242
- Ng--Schauenburg, *Frobenius--Schur indicators and exponents of spherical
  categories*, theorem 4.1: https://arxiv.org/pdf/math/0601012
- Bruillard--Ng--Rowell--Wang, *Rank-finiteness for modular categories*,
  theorem 3.9: https://arxiv.org/pdf/1310.7050
- Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, section 2.7, corollary 2.18, section 4.3:
  https://arxiv.org/pdf/1611.04486
- Ostrik, *Module categories, weak Hopf algebras and modular invariants*:
  https://arxiv.org/pdf/math/0111139

The Morita Gram formula is derived explicitly above from the usual module
category bicategory; it is not attributed to a literature theorem with a
stronger or different hypothesis.
