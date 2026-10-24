# A triality descent theorem in dimension 96

The first lemma excludes `R9_2_1356` and `R9_2_1933` in general complex fusion-category scope. The subsequent descent theorem gives a necessary structural description for `R9_2_1857` and `R9_2_2029`; it does not exclude them. The quantum-group category of type `D4` at level two gives an actual example of the remaining dimension-32 structure.

## A central-invertible consequence of solvability

**Lemma.** A nontrivial solvable fusion category with trivial universal grading has a central subgroup of invertible objects of prime order.

Indeed, by the cyclic-prime extension/equivariantization characterization of solvability, its final nontrivial construction step cannot be an extension. It is an actual `Cp` equivariantization. Its canonical `Rep(Cp)` embeds into its Drinfeld center and its forgetful image embeds in the category. All underlying invertibles in this image therefore commute with every simple object.

In each of `R9_2_1356` and `R9_2_1933`, the dimension is 96, the adjoint ring is the whole ring, and the invertible group is `C3`. Thus solvability would force the entire invertible group to be central. It is not: with zero-based labels, generator 1 has the following actions on the dimension-two simples:

| Ring | Left generator action | Right generator action |
|---|---|---|
| `R9_2_1356` | `(3,8,7)` | `(3,7,8)` |
| `R9_2_1933` | `(5,8,7)` | `(5,7,8)` |

These distinct cycles are an immediate contradiction. The companion generator is also noncentral, as follows either by taking its inverse or directly from the tensor. This criterion requires neither pivotality nor commutativity.

## The residual descent theorem

**Theorem.** Suppose a complex fusion category `C` has dimension 96, trivial universal grading, and simple dimensions `(1^3,2^3,3,6^2)`. Assume its invertible group is `C3`, whose generator cycles the three two-dimensional objects and fixes the three- and six-dimensional objects. Then

\[
\mathcal C\simeq\mathcal B^{C_3},\qquad \operatorname{FPdim}(\mathcal B)=32.
\]

The category `B` has type `(1^4,2^7)`, its adjoint category is tensor equivalent to `Rep(D8)`, and its universal grading group is `V4`. Each nontrivial component of this grading has two simple objects of dimension two. The outer `C3` action cycles the three nontrivial invertibles of `B`, the three nontrivial grading components, and their three distinct order-two invertible stabilizers.

No commutativity of the source ring or braiding on `C` is assumed.

## Descent and the invertible action

Dimension 96 has only the prime divisors two and three, so ENO's solvability theorem applies. The last step in a cyclic-prime extension/equivariantization construction cannot be an extension, because `C_ad=C`. Since the character group of the last equivariantizing group embeds into `G(C)=C3`, the last step is an actual `C3` equivariantization.

The orbit/stabilizer description gives three invertibles downstairs from the dimension-three source simple, the unit from the three source invertibles, one fixed dimension-two simple from the source two-dimensional orbit, and two free three-element orbits of dimension-two simples from the two six-dimensional source objects. Thus `B` has dimension 32 and type `(1^4,2^7)`. Its actual `C3` action is transitive on the three nonunit invertibles and has orbit structure `1+3+3` on the dimension-two simples. Consequently `G(B)=V4`.

For a two-dimensional simple `X`, the invertible part of `XX*` has cardinality `|G_X|`. The remaining dimensions are even, so `4-|G_X|` is even. Since `|G_X|` divides four, it is two or four. Hence every left `V4` orbit on the seven two-dimensional simples has size two or one. The outer `C3` permutes the three order-two stabilizer subgroups transitively. Therefore the size-two orbits occur in triples. There are just two possibilities:

1. all seven two-dimensional objects are fixed by `V4`;
2. there are three size-two orbits and one fixed object `T`.

## The all-fixed branch is impossible

In the first branch every `XX*` is the sum of all four invertibles, so `B_ad=Vec_{V4}^omega`. The universal grading group `U` has order eight. Each nontrivial grading component has dimension four and exactly one simple of dimension two, while the neutral component has four invertible simples.

A rank-one module category over `Vec_{V4}^omega` requires the associator class to vanish: the pointed-module description has stabilizer all of `V4`, with a two-cochain trivializing `omega` on that stabilizer. Thus the neutral category is `Vec_{V4}`.

The extension homomorphism

\[
U\longrightarrow\operatorname{BrPic}(\operatorname{Vec}_{V_4})
\]

is injective. A kernel component would be equivalent as a bimodule category to the regular neutral component and would therefore have rank four, whereas all seven nontrivial components have rank one.

The Brauer–Picard group is the split orthogonal group of `V4+V4hat` with evaluation quadratic form. It has order 72 and a dihedral Sylow subgroup of order eight. The accompanying checker verifies this finite group description directly by enumerating all linear isometries over `F2` and displaying a dihedral Sylow subgroup. Thus `U` is isomorphic to `D8`.

The outer `C3` acts nontrivially on the seven nontrivial grading components, with two three-cycles and one fixed component. It would induce an automorphism of order three of `D8`. But `Aut(D8)` has order eight. This is impossible.

## The remaining branch has an eight-dimensional adjoint category

Now assume there are three size-two orbits and one fixed object `T`. Right multiplication by invertibles commutes with the left action and preserves its unique fixed object, so `T` is fixed on both sides. Its dual is also fixed on both sides and hence equals `T`. Therefore `T^2` is the sum of all four invertibles.

The adjoint category contains all four invertibles: the stabilizer lines of the six nonfixed simples run through all three lines of `V4`. If it contained any of those six simples, closure under `V4` and the outer `C3` would force it to contain all six. Its dimension would be at least `4+6*4=28`.

The adjoint category is proper. This uses an actual prime-power grading theorem, not Morita-nilpotence: ENO, *On fusion categories*, Theorem 8.28(i), says every nontrivial category of prime-power dimension has a faithful cyclic-prime grading. Therefore `B_ad` is contained in a proper neutral component. Also its dimension divides 32, because `32/FPdim(B_ad)=|U(B)|`. A proper divisor of 32 cannot be at least 28. Hence none of those six simples belongs to `B_ad`.

For any of these six simples, dimension counting now gives

\[
XX^*=1+g_X+T
\]

where `g_X` is the nontrivial element of its order-two stabilizer. Thus

\[
\mathcal B_{ad}=\operatorname{TY}(V_4,\chi,\tau),\qquad
\operatorname{FPdim}(\mathcal B_{ad})=8.
\]

The outer `C3` preserves this category and permutes the three nonzero invertibles. In the Tambara–Yamagami classification it therefore preserves the nondegenerate symmetric bicharacter `chi`. Over `F2^2`, the nonalternating form has automorphism group of order two, whereas the alternating form has automorphism group `GL(2,2)=S3`. Thus `chi` must be the alternating form. Its two signs give `Rep(D8)` and `Rep(Q8)`.

The universal grading group has order four. Its three nontrivial components each have dimension eight and contain two of the six remaining two-dimensional simples. The outer `C3` cannot fix any one of these components: its permutation on the six simples has no fixed object, and a stable set of two elements could only carry the trivial `C3` action. Thus it permutes the three components transitively, so the grading group is `V4`.

## The quaternion choice is impossible

The extension homomorphism `V4 -> BrPic(B_ad)` is injective: a nonidentity kernel component would have the rank of the regular adjoint category, namely five, but all such components have rank two. Nikshych–Riepel Section 9 computes

\[
\operatorname{BrPic}(\operatorname{Rep}(Q_8))\cong S_3,\qquad
\operatorname{BrPic}(\operatorname{Rep}(D_8))\cong S_4.
\]

There is no embedding of `V4` into `S3`, excluding the quaternion choice. This leaves `B_ad=Rep(D8)` as asserted. The group `S4` does contain a normal `V4` with an order-three normalizer action, so this group-level argument does not exclude the dihedral branch or resolve its extension coherence.

## Exact application and status

`verify_dimension96_reduction.py` reads the original source tensors and checks the full dimension character, order-three generator, required character orbits, adjoint generation, and centrality or its failure for:

- `R9_2_1356`;
- `R9_2_1857`;
- `R9_2_1933`;
- `R9_2_2029`.

It also checks the finite orthogonal group used in the all-fixed branch. The source hashes and results are in `dimension96_reduction.json`. The two general exclusions are additionally isolated in `central_invertible_exclusions.json`. The other two entries are explicitly marked as structural reductions and must not be counted as exclusions on this argument alone.

## Primary references

- ENO, *Weakly group-theoretical and solvable fusion categories*, Theorem 1.6 and Proposition 4.4: <https://arxiv.org/pdf/0809.3031>.
- ENO, *On fusion categories*, Theorem 8.28(i): <https://arxiv.org/pdf/math/0203060>.
- D. Tambara, S. Yamagami, *Tensor Categories with Fusion Rules of Self-Duality for Finite Abelian Groups*, Journal of Algebra 209 (1998), 692–707, classification theorem: <https://doi.org/10.1006/jabr.1998.7558>.
- D. Nikshych, B. Riepel, *Categorical Lagrangian Grassmannians and Brauer-Picard groups of pointed fusion categories*, Section 1, Section 4, and Section 9 equations (40),(41): <https://arxiv.org/pdf/1309.5026>.
- The two alternating Tambara–Yamagami signs are also displayed explicitly in *Notes on gauging noninvertible symmetries, part 1*, Section 3.2.1: <https://vtechworks.lib.vt.edu/bitstreams/fff373d1-7563-466c-98c7-da135b671580/download>.
