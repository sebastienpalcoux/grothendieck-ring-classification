# A unified relative-cocycle construction in dimension48

The two rings R9_2_392 and R9_2_1246 are realized by unitary
group-theoretical categories on the same group and subgroup. Their
difference is the choice of a pointed associator. The actual cochains,
their coherence identities, and all fusion coefficients are recorded and
replayable. Neither construction requires a categorical classification
of dimension24 categories.

Both models passed independent categorical and exact tensor audits;
the audit receipts are `phase3/audit_models/d48_relative_twist_audit.json`
and `phase3/audit_models/d48_exotic_relative_twist_audit.json`.

## Common group and subgroup

Let `G=S4×C2`. Write an element as `(p,e)`, put `s(p,e)=sign(p)` in F2,
and use e also for the projection to the second factor. Set

`x=((12),1)`, `y=((34),0)`, and `H=<x,y>≅V4`.

Thus `H={1,x,y,xy}`. Write X,Y for its two coordinate homomorphisms.
The subgroup is a complement to the normal A4, so these examples can
also be viewed through a twisted V4 action on a pointed A4 category.
It is the subgroup-algebra construction below that supplies coherence;
an action on the level of simple objects alone is not used as evidence.

Let α be the normalized F2-valued Schur two-cocycle on S4 obtained by
restricting the explicit S5 section cocycle in
`phase3/group_models/s5_schur_data.json` to permutations fixing the
fifth letter. The whole α table is included as `factors_F2[0]` in both
model data files. It is pulled back to G. All 48³ cocycle identities are
checked directly, so the argument does not depend on an undocumented
choice of double-cover convention.

## First associator: R9_2_392

Use

`ω_+(g,h,k)=(-1)^[e(g)(α(h,k)+e(h)e(k))]`.

The exponent is the cup product of a one-cocycle and a two-cocycle;
ω_+ is therefore a normalized three-cocycle. For the stored section,
the explicit cochain

`ψ_+(a,b)=i^[X(a)Y(b)]`, for a,b in H,

satisfies `δψ_+=ω_+^(-1)|H`. This identity is also checked on all64
triples of H. With the convention that the associator is ω, this is
exactly the associativity equation for the algebra
`A=⊕_(h∈H) h`, with multiplication constants ψ.

The category of A-bimodules in Vec_G^(ω_+) realizes R9_2_392. The
source-to-model permutation is

`[0,1,2,8,7,3,5,6,4]`.

Its independent categorical audit is
`phase3/audit_models/D48_RELATIVE_TWIST_AUDIT.md`.

## Second associator: R9_2_1246

Let Ω be the explicit normalized eighth-root-valued cocycle on S4
copied to `s4_exotic_cocycle_seed.json`. Its provenance is the earlier
model of R9_1_92,
`C(F2² ⋊ S3, Ω, C2, 1)`, from the lower-rank project. The seed includes
the old24-element group table, the full24³ associator table, source
filename and SHA256 hash. The old-to-permutation group isomorphism and
every transported cocycle entry are included in
`d48_exotic_relative_twists.json` and checked in the replay.

For clarity, the old symbolic origin was a coherent S3 action on the
even-parity subgroup of F2³. Its crossed-product associator was

`Ω((a,g),(b,h),(c,k)) = w(a,g b,g h c)+J_g(b,h c)-μ_(g,h)(c) mod8`.

No completeness or correctness claim about the earlier census is
required here: all24⁴ three-cocycle identities of the copied finite
table are checked directly. Thus this is an independently valid pointed
associator.

Pull Ω back along G→S4 and set

`ω_-(g,h,k)=Ω(p_g,p_h,p_k)
            (-1)^[e(g)α(h,k)+s(g)e(h)e(k)]`.

Again this is a genuine normalized three-cocycle. In the order
`(1,y,x,xy)` of H, use `ψ_-(a,b)=ζ8^[q(a,b)]`, where

| q | 1 | y | x | xy |
|---|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 |
| y | 0 | 1 | 2 | 7 |
| x | 0 | 4 | 0 | 0 |
| xy | 0 | 1 | 6 | 7 |

Directly, `δψ_-=ω_-^(-1)|H`. The category of the corresponding
subgroup-algebra bimodules realizes R9_2_1246, with source-to-model map

`[0,8,7,5,6,3,1,2,4]`.

Unlike the first associator, ω_- is not assumed to take values ±1.
The code checks the inverse convention explicitly and performs the
character calculation in Q(ζ16).

## Why the common type is (1⁴,2³,4²)

For both cocycles, the five H double cosets have sizes `4,4,16,16,8`
and stabilizer orders `4,4,1,1,2`. Their projective irreducible dimension
lists are respectively

`[1,1,1,1]`, `[2]`, `[1]`, `[1]`, `[1,1]`.

The second V4 stabilizer has nondegenerate commutator pairing; its
twisted group algebra is M2(C). Consequently the simple categorical
dimensions are `1,1,1,1,2,4,4,2,2`, whose squared sum is48. This
explains uniformly how the twist replaces four invertibles in the
untwisted action by a single dimension-two object.

The tensor calculation uses the stabilizer, fiber-transport and balanced
tensor-character formulas derived in
`phase3/group_models/S5_RELATIVE_TWIST.md` and independently audited in
`phase3/audit_models/S5_RELATIVE_TWIST_AUDIT.md`. Only the group, the
subgroup characters and the cocycles change. It verifies exact
cyclotomic integrality, nonnegative multiplicities, associativity, and
all729 source coefficients for each model.

## Scope, replay and bounded search

All associators and algebra constants have unit modulus. The standard
separable subgroup algebra in the pointed unitary category gives a
unitary fusion category of bimodules. Group-theoretical complete
unitarity also follows from Galindo–Hong–Rowell, Theorem5.20:
https://people.tamu.edu/~rowell/GHRarx1.pdf . For the group-theoretical
construction, see ENO §2.5:
https://arxiv.org/pdf/0809.3031 .

The optimizer-free replay is

`python phase3/integral_theory/verify_d48_models.py`.

It needs only the copied cochain data and the project source tensor
corpus; it does not require the previous project directory, GAP, an
external categorical classification or a cochain solver. Its receipt is
`d48_model_verification.json`.

The discovery scripts tested all256 cup-product combinations generated
by `s,e` and the four two-cocycles `α,s²,e²,s⊗e`, first alone and then
after multiplying by Ω. Each pass had32 trivial restrictions to H;
for each such restriction, both subgroup Schur classes were tested.
Each pass yielded32 rank-nine presentations, all with its respective
single fusion tensor. This is a complete check of those explicit
subfamilies, not a claim to enumerate all group-theoretical categories
of dimension48.
