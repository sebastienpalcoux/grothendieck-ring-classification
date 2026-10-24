# Independent categorical audit of the model for R9_2_2029

**Verdict: PASS.** The construction in
`phase2/models/d4_zest_triality.md` gives an actual fusion category with
the stated equivariantization, rather than only an invariant based ring.
This audit concerns categorical existence as well as the exact tensor
identification.

## Existence of the associative zest

In the seed modular category `Spin(8)_2`, the currents have highest weights
`0, 2ω1, 2ω3, 2ω4`. Their twists are all one. Their pointed subcategory
is therefore Tannakian, and is contained in the neutral component of the
universal `V4` grading. The order-three diagram automorphism preserves this
symmetric subcategory and cycles its nonidentity simples.

The applicable published result is Galindo–Mora–Rowell,
[arXiv:2311.17255](https://arxiv.org/abs/2311.17255),
Proposition 4.2(1), together with Remark 3.4 identifying the premetric
zesting data with associative zesting of the modular category. In the
Tannakian case the current braiding and associator admit a trivial gauge;
the associative obstruction vanishes. Thus any normalized current-valued
two-cocycle and scalar three-cocycle provide an associative zest.
The stronger restrictions on *braided* zesting in Proposition 4.4 are not
needed: only a fusion category and its tensor action are claimed here.

For the additive group of `F4`, the proposed cocycle

    λκ(a,b) = κ(ab)²,   κ ∈ {t,t+1},   t²+t+1=0,

is normalized and additive in each argument. Its two-cocycle identity
follows directly by expansion. The scalar correction is the constant
three-cocycle one. The actual new product is

    X_a ⊗λ Y_b = X_a ⊗ Y_b ⊗ J(λκ(a,b)).

## Coherent triality, including its action constraints

An ordinary trivialization of the current subcategory alone would not
justify the proposed action. The proof supplies the stronger equivariant
trivialization as follows. The equivariantized current category is
symmetric Tannakian of dimension 12. Its canonical `Rep(C3)` subcategory
gives a group extension

    1 → V4 → E → C3 → 1.

Schur–Zassenhaus splits the extension. Under the equivalence between
equivariantization and de-equivariantization, a choice of complement
identifies the original coherent symmetric action with the ordinary
permutation action on `Rep(V4)`, and hence on the character model
`Vec_A`. Consequently the inclusion `J: Vec_A → Spin(8)_2` has coherent
equivariance, compatible with multiplication of currents.

Both the grading group and the current group are identified with `F4`
so that triality acts by multiplication by `t`. The equality

    λκ(ta,tb) = t⁴ λκ(a,b) = t λκ(a,b)

is an equality of the chosen cocycle data. The original braided tensorator
and the equivariance of `J` therefore define the tensorator of triality
for `⊗λ`. The zested associator is composed from the original associator,
braiding past currents, and the tensor structure of `J`. Each is preserved
by those same maps. This verifies preservation of the new associator;
the original group-composition constraints remain compatible because
`J` has coherent equivariance. Thus this is a genuine `C3` tensor action,
not merely a permutation preserving fusion coefficients.

The construction may be made unitary using the unitary seed, the
equivariant symmetric gauge, and scalar correction one. There is also
an independent existence-level fallback for unitarizability: the resulting
equivariantization has dimension `96=2⁵·3`, so ENO solvability and the
complete unitarity of weakly group-theoretical categories apply.

## Tensor identification

The fixed simples are exactly the unit and `f=ω2`. Both are neutral, and
`f²` is the sum of the four currents. Zesting therefore leaves their
fixed fusion spaces and their triality trace calculation unchanged.
The complete equivariantization tensor follows from the usual character
average, as in the already audited seed model for `R9_2_1857`.

The independent replay reconstructs both cocycles `κ=t,t+1`, checks the
zested fusion axioms and triality invariance, and verifies all 729 source
coefficients for each witness using the source-to-model permutation

    [0,8,7,3,5,2,1,6,4].

Both witnesses realize the same census ring `R9_2_2029`. The canonical
duplicate-free record is
`phase2/models/d4_zest_triality_new_models.json`.

No additional unresolved action-lifting condition is being deferred.
