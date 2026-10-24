# Independent audit: the folded SO(3) exclusion of R9_2_920

**Verdict: APPROVED**, with the explicit presentation and negligible-idempotent arguments below retained. The argument excludes pseudo-unitary categorifications of the entire folded family at levels `4n-2`, `n>=3`. Combined with the independently replayed Galois-pseudo-unitary gate, it excludes every complex fusion-category categorification of R9_2_920.

The draft reviewed is `../quadratic_theory/R920_PROOF.md`. Its central strategy is sound. This audit supplies the details that are essential to avoid invoking a morphism-generation hypothesis or confusing pseudo-unitarity with a C*-structure.

## 1. Ring hypotheses and the local relation

`audit_R920.py` independently constructs the parent fusion coefficients from the elementary SU(2) formula, checks all 729 source coefficients against the fold, and checks all 324 parent products under the quotient map. It checks the low invariant dimensions `[1,0,1,1,3]`, the generator path, and the two parent simples mapping to the unit. The previously completed signed-gate replay is checked as a dependency, not rerun here.

Write `d=1+2 cos(pi/18)`, `delta=2 cos(pi/36)`, so `d=delta^2-1>2`. For a hypothetical pseudo-unitary categorification use its positive spherical structure. MPS Lemma 2.2 proves symmetric self-duality directly from the one-dimensional second and third invariant spaces and nondegeneracy; that proof does not use generation. This is a precise reference for the self-duality assertion, preferable to an unsupported general assertion about odd fusion multiplicities and indicators.

MPS Proposition 7.1 is a local Gram-determinant computation. Its determinant `d^5(d-2)` excludes either nontrivial cubic rotation eigenvalue in the ambient four-point space of dimension three. After normalizing the bigon to one, Proposition 4.1 similarly forces `t=(d-2)/(d-1)` using local determinants only.

The upper-left three-by-three block of the displayed four-tree Gram matrix is

```
[[d^2,d,d],
 [d,d^2,0],
 [d,0,d]].
```

Its determinant is `d^3(d^2-d-1)`, nonzero for `d>2`. These three diagrams therefore span the full ambient four-point space. Nondegeneracy of its spherical pairing makes the kernel relation of MPS Lemma 4.11 an actual morphism identity. No assertion about the span of higher invariant spaces is needed.

## 2. Normalization and a presentation before semisimplification

The normalization can be checked directly in the diagrams in MPS Lemma 4.11 and Fendley–Krushkal Figure 9. Let `tau` be the bigon-one MPS vertex. Set

`v=sqrt(d-1)*tau`, and `Q=d+1=delta^2`.

Using `H` and `I` for the two connected four-point trees, and `P` and `E` for the two disconnected pairings, the MPS relation is

`H_tau-I_tau+(P-E)/(d-1)=0`.

It becomes `I_v+E=H_v+P`, exactly the chromatic relation. The loop is `Q-1`, the bigon is `Q-2`, and the triangle coefficient is `Q-3`. The tadpole is zero since the first invariant space vanishes. The MPS doubled-strand vertex coefficient `sqrt(delta/(delta^2-2))` becomes `sqrt(delta)` after this rescaling, agreeing with the chromatic-to-TL map.

Fendley–Krushkal Theorem 4.3 presents the chromatic algebra by these trivalent local relations; Lemma 4.4 gives its basis indexed by noncrossing partitions without singleton blocks, and Lemma 7.1 proves that the doubled-strand map into TL is injective for nonzero `delta`. Their proofs extend unchanged from endomorphisms with an even number of boundary points to arbitrary rectangular Hom spaces: the forest reduction and the unique leading doubled diagram depend only on the boundary partition. This observation is needed because a trivalent category also has Hom spaces with an odd total number of boundary points.

Here is an explicit proof that the image is the **full** corner on powers of the second Jones–Wenzl idempotent, rather than an unspecified subcategory. In the additive Karoubi envelope of TL let `V` be one strand and `Y=(V^2,p_2)`. Since `delta!=0`, the complementary cup-cap projector splits off the tensor unit:

`V^2 = 1 direct-sum Y`.

Let `r_N=dim Hom(1,Y^N)`. The planar TL basis and the direct-sum decomposition imply, at every such parameter,

`Catalan(N) = sum_{j=0}^N binom(N,j) r_j`.

The identical formula counts noncrossing partitions of N points by deleting singleton blocks. Hence `r_N` is exactly the number of noncrossing partitions without singletons. Bending strands gives the same conclusion for `Hom(Y^a,Y^b)`, with `N=a+b`. The injective chromatic map thus has equal-dimensional domain and codomain and is onto every Hom space. This elementary dimension argument avoids a generic-parameter specialization assumption.

Consequently the local relations in the hypothetical category define a pivotal functor from the full category on powers of `p_2`. Extending over sums and split idempotents yields a pivotal functor from the full even Karoubi envelope of unsemisimplified TL to the hypothetical category. This extension is legitimate because the target is semisimple and idempotent complete. It is not assumed full.

## 3. Why the functor kills all negligibles

Goodman–Wenzl Proposition 2.1 states that the TL negligible tensor ideal at the present parameter is generated by the Jones–Wenzl idempotent `p_35`. It is defined because the recursion denominators through `[35]` are nonzero. Its categorical trace is `[36]=0`.

The even category contains the idempotent object

`P=(V^36,p_35 tensor id_V)`.

It has dimension zero. A pivotal functor preserves that dimension, and a nonzero object of a pseudo-unitary fusion category in its canonical spherical structure has positive dimension. Thus the image of P is zero; equivalently the image of its identity idempotent is zero.

To check that this suffices for the **even** negligible ideal, expand any element of that ideal using the TL tensor-ideal generator. Each term factors through an object consisting of `p_35` tensored with extra strands. Morphisms preserve parity. For even source and target, the number of extra strands is therefore odd. The TL braiding, which exists at this nonzero parameter, moves strands past the block carrying `p_35`, so each such intermediate object is isomorphic to `P tensor V^(2s)` for some `s>=0`. Every term consequently factors through an object killed by the functor. Passing to sums and retracts preserves this conclusion.

The functor therefore descends through the negligible quotient and its Karoubi completion to

`F: PSU(2)_34 -> C`.

Since the image of `V_2` is the based generator of C, this functor is dominant. This argument uses positive dimensions of **objects** only. It neither assumes that the target is unitary nor claims that arbitrary trace-zero morphisms vanish.

## 4. Audit of the central-algebra contradiction

The even SU(2) fusion ring is generated as a ring by `V_2`, by its three-term recurrence. Accordingly the Grothendieck-ring map induced by F is the previously checked fold. Exactly `1` and `f=V_34` map to the unit, each with multiplicity one. Adjunction gives `R(1)=1 direct-sum f`.

Bruguières–Natale Proposition 5.1 and Corollary 5.6 (arXiv v1 numbering) give the induced commutative central algebra A and the equivalence between its module category and the fusion target. The latter is semisimple. One does not need to assume that F preserves the standard braiding or invoke a separate normality theorem.

The unit is a central subobject of A. Since the center of a fusion category is semisimple in characteristic zero, its complement is a central object with underlying object f. The universal grading of `PSU(2)_34` is trivial: `V_2` generates and occurs in its own square, forcing its grading degree to be neutral. Tensor automorphisms of the identity are therefore trivial. For an invertible object, the ratio of two half-braidings gives such a tensor automorphism; this proves uniqueness of the central lift of f.

The standard braiding supplies that unique lift. With `q=exp(pi*i/36)` its self-braiding is

`c_(f,f)=(-1)^34 q^(-34*36/2)=-1`.

The inverse convention for the braiding gives the same scalar. Commutativity in the center therefore forces the multiplication component `f tensor f -> 1` to vanish. There is no component to f, since `f^2=1` and `f!=1`. Thus f would be a square-zero ideal of A.

For clarity, the resulting contradiction does not need an unexplained Frobenius-pairing claim. The sequence of right A-modules

`0 -> f -> A -> 1 -> 0`

would be nonsplit: any underlying map `1 -> A` is a scalar multiple of the unit, and a nonzero such map cannot be A-linear from the quotient module, because multiplication of the unit by f is nonzero whereas f acts as zero on that quotient. This contradicts semisimplicity of the A-module category. Hence the proposed categorification cannot exist.

## Conclusion and references

All steps hold without morphism generation, a unitary hypothesis, weak group-theoretical assumptions, or an unproved positivity condition on morphism pairings. The verified signed gate promotes the pseudo-unitary exclusion to a general exclusion for R9_2_920. The same categorical proof applies to every folded `PSU(2)_(4n-2)` ring with `n>=3`; the gate for general categorifications must be checked separately when applying this family outside the present ring.

Primary references, inspected directly:

- Morrison–Peters–Snyder, [Categories generated by a trivalent vertex](https://arxiv.org/abs/1501.06869), Lemma 2.2, Proposition 4.1, Lemma 4.11, Proposition 7.1, and the doubled-TL realization. The introduction explicitly warns about morphism generation; this audit does not apply its classification theorem directly.
- Fendley–Krushkal, [Link invariants, the chromatic polynomial and the Potts model](https://arxiv.org/abs/0806.3484), Theorem 4.3, Lemmas 4.4 and 7.1.
- Goodman–Wenzl, [Ideals in the Temperley Lieb Category](https://arxiv.org/abs/math/0206301), Proposition 2.1.
- Bruguières–Natale, [Exact sequences of tensor categories](https://arxiv.org/abs/1006.0569), Proposition 5.1 and Corollary 5.6 in the inspected arXiv v1. Later versions may renumber these results.

Finite-hypothesis replay: `python phase2/signed/audit_R920.py`; output: `R920_audit.json`.
