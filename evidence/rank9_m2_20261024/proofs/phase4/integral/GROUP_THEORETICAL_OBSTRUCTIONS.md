# Exhausting group-theoretical models for the four integral residual rings

**Scope.** This argument excludes group-theoretical categorifications of
`R9_2_12`, `R9_2_959`, and `R9_2_1965`. Together with ENO Proposition 9.11
for the simple exotic ring `R9_2_941`, all four integral residual rings
are outside the group-theoretical class. This does **not** exclude arbitrary
fusion categorifications. In particular, no theorem identifying all
integral categories of dimensions 120 or 168 as group-theoretical is used.

The finite computations below are exact. A separate independent audit
passed: `phase4/audit_integral_gt/AUDIT.md` and `audit_verdict.json`.
The accepted conclusion has group-theoretical scope only.

## 1. An exhaustive projective-character profile reduction

Every group-theoretical category of dimension D has a presentation
`C(G,omega,H,psi)` with `|G|=D`, `d psi=omega|H`. Its simples over a double
coset `HgH` are indexed by projective irreducible representations of
`K_g=H intersect gHg^{-1}`, of dimensions

`[H:K_g] dim(pi)`.

The identity double coset supplies the ordinary category `Rep(H)` as a
fusion subcategory. A projective irreducible degree is at most the square
root of the order of its group, so all simple dimensions are at most |H|.
In particular, |H|<6 cannot supply a dimension-six simple.

`all_twist_skeleton.g` enumerates every group of orders 120 and 168 and
every conjugacy class of subgroups. It first checks that the ordinary
character degrees of H are a submultiset of the target type. For every
remaining double-coset intersection K, it constructs a Schur cover and
partitions the irreducible characters of the cover by their central
character on the kernel. These are precisely all projective degree
profiles, for every class in `H^2(K,C^*)`. It independently chooses any
of these profiles at every double coset, retaining those whose union is
the target type. Independence is a relaxation of global compatibility;
it cannot omit any global three-cocycle or relative two-cochain.

The complete output is:

| D | Groups | Subgroup conjugacy classes | Surviving pairs |
|---:|---:|---:|---|
| 120 | 47 | 1431 | `(S5,S3xC2)` and `(A5xC2,S3xC2)` |
| 168 | 57 | 1751 | the two conjugacy classes `(PSL(2,7),S4)` |

Both dimension-120 pairs have intersections of orders `12,2,4`, with
the order-four intersection V4. Their required projective degree packets
are `(1,1,1,1,2,2)`, `(6,6)`, and `(6)` respectively. Thus the V4
intersection must carry its nontrivial Schur class. Both dimension-168
pairs have intersections S4 and V4; the required packets are
`(1,1,2,3,3)` and `(6,6,6,6)`.

The scan uses GAP 4.12.1 with SmallGrp and the exact character/Schur-cover
algorithms. It is finite group classification plus finite exact arithmetic,
not a restricted three-cocycle ansatz. The saved `.json` normalizes the
GAP output; the original `.jsonl` contains line-wrapped JSON objects.

## 2. Immediate consequence for R9_2_959

For both surviving dimension-120 pairs, H is `S3xC2`, whose representation
category has invertible group V4. It embeds as the identity double-coset
subcategory. But the invertible group of R9_2_959 is C4. A based inclusion
cannot embed V4 into C4. Thus no group-theoretical categorification of
R9_2_959 exists, independently of omega and psi.

## 3. All relative three-cocycles for the S5 pair

Let `G=S5` and `H=S3xC2`. Every admissible class
`a in H^3(G,C^*)` restricts to zero on H. Restriction followed by
corestriction is multiplication by `[G:H]=10`, hence `10a=0`.

The five-primary part of `H^3(S5,C^*) = H^4(S5,Z)` is zero: restriction
to a Sylow C5 is injective on this part, and the image must be fixed by
the normalizer `C5:C4`. An order-four automorphism of C5 acts on H^4 by
the square of a primitive automorphism, namely -1 modulo five, whose
fixed space is zero. Therefore every admissible class has order at most
two.

Every two-torsion class in H^3(G,C^*) lifts to H^3(G,F2), by the long
exact sequence of `1 -> mu2 -> C^* --square--> C^* -> 1`.
Let P be a Sylow D8 of S5. Its index is fifteen, hence odd. If a is a
two-torsion global class and b is any F2 lift of its restriction to P,
then the image of `cor_P^G(b)` in H^3(G,C^*) is
`cor(res(a))=15a=a`. Consequently corestricting **every** F2 third
cohomology class of P exhausts all admissible global associator classes.

The normalized bar complex computes `dim H^3(D8,F2)=4`: 343 normalized
three-cochain variables, cocycle dimension 45, boundary dimension 41.
The program enumerates all sixteen classes. For right coset representatives
`t` of `P\G`, define `h(t,g)` and `t.g` by

`t g = h(t,g) (t.g)`.

The explicit corestricted sign cocycle is

`w(g1,g2,g3) = sum_t b(h(t,g1),h(t.g1,g2),h(t.g1g2,g3)) mod 2`.

This is the usual inhomogeneous cochain transfer, so it takes exact
cocycles to exact cocycles. The program solves `d psi=(-1)^w|H` exactly
in eighth roots of unity. Completeness of this finite primitive test is
explained below.

Eight of the sixteen representatives admit a relative trivialization.
Four yield rank twelve. The other four yield rank nine and match **all
729 coefficients of R9_2_92**, with explicit based isomorphisms; none
matches R9_2_12. Reusing the independently audited twisted bimodule
character formula is legitimate here: only its normalized cocycle and
relative cochain inputs change. Every returned tensor is separately
checked for the unit and every associativity equation: 6,561 at rank nine
and 20,736 at rank twelve.

There is no missing choice of psi. `H^2(H,C^*)=C2`, and the nontrivial
class extends from the Schur cocycle of S5: lifted disjoint transpositions
have nontrivial commutator. Multiplying psi by that class is induced by
an identity-on-objects tensor autoequivalence of `Vec_G^omega`, so it
does not change the based ring. This extension was independently checked
in phase three's `S5_RELATIVE_TWIST.md` and audit.

Thus the entire S5 pair, with all relative cocycles, gives no model for
R9_2_12.

### Exact primitive solver and its bound

Since `H^2(H,C^*)` has exponent two, a sign-valued three-cocycle on H
that is a C^*-coboundary has a fourth-root-valued primitive. Indeed, if
`d psi=w`, then `psi^2` is a two-cocycle. Hence `psi^4=d f` for a
one-cochain f. Choose a fourth root b of f, and replace psi by
`psi/(d b)`; its fourth power is one. Thus eighth roots are more than
sufficient.

The congruence solver lifts successively modulo two, four and eight.
At each lower stage it enumerates all possible H^2(H,F2) classes, whose
basis is `x^2,xy,y^2`, for the two abelianization characters of
`H=S3xC2`. This follows also from the normal odd-order C3 subgroup:
`H^*(H,F2)=H^*(C2xC2,F2)`. Two solutions differing by an F2 two-coboundary
have the same liftability, since that change can be lifted to an integral
one-coboundary adjustment. Exact Gaussian elimination handles the
inhomogeneous linear equations and tests every consistency row. The final
primitive is checked against every normalized triple of H. Thus a failed
test is an exact no-primitive conclusion, not an optimizer timeout.

## 4. The A5xC2 pair, including the odd-primary part

Again the global restriction kernel is killed by ten, so an admissible
class is a sum of a two-torsion and a five-torsion class. We handle the
two-primary part by the same exhaustive transfer construction, using a
Sylow group P=C2^3 of index fifteen. The normalized bar complex has
cocycle dimension 49 and boundary dimension 39, giving ten F2 third
cohomology generators.

For efficiency, let n be an order-three element of the normalizer of P.
Corestriction is unchanged in cohomology by conjugating a seed by n.
Thus corestricting b is cohomologous to corestricting
`b+n*b+n^2*b`, since three is one modulo two. The span of these norm
classes has dimension four. Exact reduction modulo the bar boundaries
therefore gives sixteen representatives covering the image of **all
1,024** original F2 cohomology classes. No global class is discarded.

Only two of these sixteen representatives admit a primitive on H.
For each, both subgroup Schur choices `psi` and `psi*(-1)^{x cup y}`
are explicitly tested. In all four cases the V4 intersection multiplier
is trivial and the resulting category has rank twelve. Thus no
two-primary relative class gives the required rank-nine profile.

The five-primary part cannot change this conclusion. Relative pairs
`(omega,psi)` form relative cohomology, and the multiplier on a
double-coset intersection K is a homomorphism from that relative
cohomology group to `H^2(K,C^*)`. The five-primary part of the relative
group maps isomorphically to the five-primary global restriction kernel,
because `H^2(H,C^*)` has no five-torsion. Its image in the order-two
Schur multiplier of V4 is therefore zero. Equivalently, multiplying
the relative data by any order-five relative class does not change the
V4 projective degree profile. The necessary rank-nine profile requires
that multiplier to be nontrivial. Hence no admissible cocycles for
`(A5xC2,S3xC2)` realize R9_2_12.

Combining Sections 1, 3 and 4 proves the group-theoretical exclusion for
R9_2_12.

## 5. The dimension-168 pair

The all-twist profile reduction leaves only `G=PSL(2,7)`, H=S4, for the
two subgroup conjugacy classes. The following completes the old bounded
argument by showing that these are now the *only* presentations that
need to be considered.

Restriction `H^3(G,C^*) -> H^3(H,C^*)` is injective. Its kernel is killed
by index seven. But G has no seven-primary H^4: restriction to its Sylow
C7 is injective on the seven-primary part, and the normalizer C7:C3
acts on H^4(C7,Z)=C7 by multiplication by 2 and 4, with zero fixed part.
Thus any admissible omega is globally trivializable.

After trivializing omega, `H^2(S4,C^*)=C2`, and both classes extend
from `H^2(PSL(2,7),C^*)=C2`. Nontriviality of restriction is witnessed
by a commuting pair in S4 whose lifts to the Schur double cover fail
to commute. The prior exact checker tests this for both subgroup classes:
`phase3/group_models/psl168_relative_bound.g` and its saved log.
Therefore psi can also be removed by a global two-cocycle autoequivalence.
Both presentations reduce to the untwisted category, whose full tensor
is R9_2_1557, not R9_2_1965. The based nonisomorphism is checked again.

## 6. R9_2_941 and the precise remaining boundary

For the simple exotic dimension-504 ring R9_2_941, ENO Proposition 9.11
excludes the larger class of weakly group-theoretical categorifications;
see `BRAIDED_SCOPE_THEOREMS.md`.

None of these arguments supplies a general exclusion of any of the four
integral residual rings. A non-group-theoretical integral category could
still realize R9_2_12, R9_2_959 or R9_2_1965. A realization of R9_2_941
would additionally be non-weakly-group-theoretical. Models outside the
excluded classes and general categorical obstructions remain open.

## Replay and sources

* `all_twist_skeleton.g`, `.jsonl`, `.json`, `.log`:
  all finite groups/subgroups and all local projective degree profiles.
* `s5_transfer_search.py` (run once normally and once with `--a5c2`):
  exact normalized cohomology, transfer, relative primitives and tensors.
* `a5c2_data.g` and `.json`: explicit A5xC2 group and subgroup data.
* `s5_transfer_search.json` and `a5c2_transfer_search.json`: complete
  finite result records and explicit cocycle/relative-cochain inputs.
  Each model's `psi_exponents_mod8` is its own relative cochain.
  `base_psi_exponents_mod8` is the twist-zero cochain for the top-level
  tensor. The legacy top-level `psi_exponents_mod8` records the final
  subgroup twist, explicitly identified by `psi_record_subgroup_Schur_twist`
  (one for A5xC2, zero for S5); it is preserved for provenance.
* EGNO, *Tensor Categories*, Section 9.7, and ENO,
  <https://arxiv.org/pdf/0809.3031>, Section 2.5: group-theoretical
  presentations and projective double-coset dimensions.
* Kenneth S. Brown, *Cohomology of Groups*, Chapter III: normalized bar
  complex, restriction/corestriction and conjugation invariance. See also
  primary lecture notes on transfer:
  <https://courses.washington.edu/mnotes/groupcoho/notes.pdf>.
* Phase-three `S5_RELATIVE_TWIST.md` and independent model audit:
  exact twisted bimodule character formula, subgroup Schur extension.
* `phase4/audit_integral_gt/AUDIT.md`, `audit_verdict.json`, and independent
  replay certificates: all-group enumeration, all 32 relative classes,
  primitive completeness, stabilizer cocycles, projective characters,
  tensor identifications and categorical scope independently passed.

The new work does not infer nonexistence from an untwisted search failure.
The cohomological reductions above are the reason the tested finite
families cover all relative cocycles for these remaining presentations.
