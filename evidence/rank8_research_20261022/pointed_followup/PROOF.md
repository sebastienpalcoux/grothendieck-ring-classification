# Order-two pointed induction: exact Fourier fibre packing

This new order-two pointed-induction criterion excludes all complex fusion
categorifications of R8_3_1795. It also forces a nontrivial pointed C2
associator for any categorification of R8_3_1768, which remains unresolved.
It imports the previously verified complete real S/STS central-induction
cones and the separately certified general-to-Galois-pseudo-unitary gates.
No feasible relaxation is identified with a category or model. Exact result
files record every tested branch, including the R1768 odd assignments left
untested after one exact feasible witness.

Let C be a hypothetical pseudo-unitary categorification, g its nontrivial
invertible simple, I central induction, and D=FPdim(C). The tensor verifies
g^2=1, B[0,g]=0, and B[g,g]=8. Write I(g)=sum_Z m_Z Z, z_Z=FPdim(Z).
The pointed second indicator epsilon=nu_2(g) is +1 or -1. The positive
central-induction trace formula gives

    sum m_Z z_Z theta_Z^2 = epsilon D,   sum m_Z z_Z = D.

Equality in the triangle inequality forces theta_Z^2=epsilon whenever
m_Z>0. Since nu_1(g)=0, the two twist fibres have equal mass D/2. This is
the order-two case of the uniform lemma proved in `../r65/PROOF.md`, using
Ng--Schauenburg, Theorem 4.1, arXiv:math/0601012.

If epsilon=+1, the twists in I(g) are +1 and -1, whose first four relative
trace powers are (1,1,1,1) and (-1,1,-1,1). If epsilon=-1 they are +i and
-i, both giving (0,-1,0,1) over the real FP field. These exact per-column
phase filters leave all columns not containing g and all rotation-domain
auxiliary columns unchanged.

## Finite integer packing

Use the basis (1,sqrt(q)) for the FP field, in which all source dimensions
have nonnegative integral coefficients in both cases. A central simple with
forgetful vector v and multiplicity m=v_g contributes

    (m^2, m z_0, m z_1)

to its twist fibre. Its first coordinate contributes to the Gram entry,
and its last two coordinates to dimension mass. Therefore each fibre is a
nonnegative integer packing of these triples with mass D/2. If one fibre
uses Gram value a, the other uses 8-a. Multiplicities of distinct central
simples with equal restriction vectors are allowed without a distinctness
bound, which weakens the condition and preserves necessity.

For each available triple (c,x,y), define exact reachable sets

    S_0={(0,0)},
    S_a = union_(c<=a) [(x,y)+S_(a-c)] intersect [0,T_0]x[0,T_1],

where T=D/2. All sets are finite; c=m^2>=1. A Gram value a can occur in
one fibre only if T belongs to both S_a and S_(8-a). A candidate triple
is retained only if, for some such a, T-(x,y) belongs to S_(a-c).
Candidates failing this condition cannot occur in any actual category.
The process repeats after removal until the finite candidate set stabilizes.
At each step an actual category's complete pair of fibres remains a
witness, so iteration is sound.

This packing test deliberately omits the other full Gram rows and the
requirement that all chosen columns coexist in one integral center matrix.
Its survival is only a necessary-condition result. The remaining columns
are then tested in the complete inherited linear S/STS and indicator cone.

## Exact data

| Ring | FP dimensions, in source order | D/2 | Pointed high columns before/after packing |
|---|---|---|---:|
| R8_3_1768 | 1,1,5+r,6+r,7+r,7+r,6+r,5+r; r=sqrt(37) | 222+36r | 255 / 243 |
| R8_3_1795 | 1,1,6+3r,7+3r,7+3r,7+3r,7+3r,6+3r; r=sqrt(5) | 270+120r | 1476 / 1187 |

The removed counts are 12 and 289. Their complete high-vector indices,
every dynamic-programming round, and the exact domain hashes are recorded
in the result metadata. No twist-order cutoff is introduced: the existing
all-order trace compression and Cauchy prime-support arguments are retained.

## Implementation and replay

`c2_fibres.py` reconstructs each frozen `AtomicRealSTS` cone. The only
performance change is a local evaluator for the existing low-column RREF
equations: row denominators are cleared once and the same finite rectangle
is traversed with exact integer arithmetic. The full resulting metadata,
including domain and modular-feature hashes, must equal the frozen metadata.
The script does not modify the old source modules.

Discovery uses a numerical LP only to propose candidates. A feasible result
is accepted after its full rational weighted column sum equals the exact
right hand side. A separator is accepted after its scalar product with
every permitted column is nonnegative and its right-hand-side pairing is
negative. Old full-cone rays may be reused on the smaller column domain,
but are rechecked exactly. The verifier checks complete branch coverage
before accepting any all-branch exclusion label.

```sh
python evidence/rank8_research_20261022/pointed_followup/c2_fibres.py --ring 1768 --verify
python evidence/rank8_research_20261022/pointed_followup/c2_fibres.py --ring 1795 --verify
```

Add `--write-receipt` to save a source-hashed exact replay receipt. The
verifier also checks the source dimension character and the free order-two
action directly. Its mathematical checks use explicit exceptions rather
than Python `assert`, so optimization does not disable them.

These are initially pseudo-unitary conditions. Their application to general
complex categorifications uses the independently verified gates in
`../pivotality/general_spherical_gates.json`, `../pivotality/PROOF.md`, and
`../pivotality/verify_general_spherical_gates.py`. Those gates imply that any
complex categorification of either ring has a pseudo-unitary Galois
conjugate. They are external inputs to the general conclusions here.

The complete terminal outcomes are:

| Ring | nu_2(g) | Allowed cone columns | Terminal result | Branches checked |
|---|---:|---:|---|---:|
| R8_3_1768 | -1 | 10468 | Exact feasible necessary relaxation | 1 of 8 |
| R8_3_1768 | +1 | 10711 | Every branch exactly excluded | 8 of 8 |
| R8_3_1795 | -1 | 58074 | Every branch exactly excluded | 8 of 8 |
| R8_3_1795 | +1 | 59261 | Every branch exactly excluded | 8 of 8 |

## R1768: the pointed associator must be nontrivial

The terminal `R8_3_1768.json` records exact separators for all eight
admissible indicator assignments with nu_2(g)=+1. Thus this pointed
associator class is excluded. For nu_2(g)=-1, the assignment
`(-1,1,1,1,1,1,1)` has an exact nonnegative rational solution to the
relaxation. The seven other odd assignments were not searched in this
refinement, since one surviving assignment already prevents a complete
exclusion by this cone.

Accordingly any pseudo-unitary R1768 categorification must have the
nontrivial associator on its pointed C2 subcategory. By the independently
certified general-to-Galois-pseudo-unitary gate, the same is necessary for
an arbitrary complex categorification: both classes in H^3(C2,C*)=C2 are
fixed by Galois conjugation. In particular, the subgroup-object sum 1+g
cannot carry the usual connected separable subgroup-algebra structure.
This does not exclude R1768 or construct any category; the exact feasible
point is a witness only for the stated linear relaxation.

## R1795: both pointed associator classes are excluded

The terminal `R8_3_1795.json` records exact full-domain separators for all
sixteen admissible indicator assignments, eight for each possible value of
nu_2(g). Every separator pairs nonnegatively with every permitted column
and negatively with the exact right-hand side. Since these assignments
exhaust both pointed associator classes and all admissible remaining
second indicators, no pseudo-unitary R1795 categorification exists.

If a general complex R1795 categorification existed, the independently
verified gate just cited would supply a pseudo-unitary Galois conjugate
with the same integer fusion rules. This contradicts the sixteen exact
separators. Therefore **R8_3_1795 has no complex fusion categorification**.

The earlier odd-parity snapshot is retained as an independently auditable
intermediate result; the no-argument verifier confirms that it equals the
corresponding record in the complete terminal certificate.

The stable snapshot `R1795_pointed_associator_obstruction.json` records eight
exact separators covering **every** admissible second-indicator assignment
with nu_2(g)=-1. Seven were already separators for the frozen larger cone;
the new Fourier packing filter excludes the previously surviving assignment
`(-1,1,1,1,1,1,1)`. All eight are rechecked on the complete new domain.

The odd-parity result by itself would force a hypothetical pseudo-unitary
R1795 categorification to have trivial pointed associator. Its nonzero class in
H^3(C2,C*)=C2 has canonical second indicator -1 on g, while the zero class
has +1. This statement transfers to arbitrary complex categorifications
using the independently certified R1795 general-to-Galois-pseudo-unitary
gate: the unique nonzero C2 cohomology class is fixed under Galois
conjugation. It motivated the additional `r1795_morita/` investigation of
the subgroup algebra 1+g. That investigation is not required by the complete
exclusion above, whose even-parity separators now eliminate the remaining
pointed class directly.

## A stronger finite refinement left for later work

The current packing test keeps a candidate if it occurs in at least one
possible pair of integer dimension-mass fibres. It then forgets correlations
between the numbers of the different dimension types. A future refinement
could enumerate whole integer dimension-type packings, use their convex
hull, and impose that the two fibre Gram values are complementary. Another
step would retain the entire pointed Gram row, rather than only its diagonal
entry and the dimension projection. Neither stronger hull is computed or
used in the certificates here.
