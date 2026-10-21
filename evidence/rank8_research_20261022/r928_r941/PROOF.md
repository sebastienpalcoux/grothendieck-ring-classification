# Braided Morita obstructions for R8_3_928 and R8_3_941

**Outcome.** Any complex fusion categorification of either ring has no braided
fusion category in its categorical Morita class. This is a restriction on possible
models, not an exclusion of general fusion categorification. No associator or
model is constructed here. Both general categorification problems remain open.

The new ingredient for R8_3_941 is a fermion-centralizer rank-square obstruction.
For R8_3_928 we apply the semionic obstruction, also used previously for the
rank-six case R6_4_155. The two arguments use the entire Morita class, not just
noncommutativity of the original based rings.

The simpler [minimal-image criterion](../braided_morita/PROOF.md), developed
in the same campaign, proves these applications directly and applies to all
eight remaining rings without a pseudo-unitary hypothesis. The independent
center arguments below are retained for their reusable semion and fermion
criteria and their exact audit of the 22-simple fermion centralizer.

## 1. Frozen inputs and scope

The exact verifier `verify.py` binds the existing source tensors and the complete
necessary center audits by SHA-256. It recalculates the positive dimension
character, the global dimension and its norm, the source invertible objects and
adjoint closure, and the relevant center counts. It does not repeat the expensive
center enumeration or the general-to-pseudo-unitary proof. Those dependencies
remain explicit, and their completeness is inherited, not newly asserted by this
short verifier.

The prior general gate
`evidence/rank8_frontier_20261021/noncommutative_followup/general_galois_pu_gate.json`
proves that any complex categorification of either ring has a pseudo-unitary
Galois conjugate. A chosen Galois automorphism extends to the complex numbers and
can be applied to all associativity, module-category, and braiding data of a
putative braided Morita representative simultaneously. Thus a braided Morita
representative in the original realization would give one in the pseudo-unitary
realization. We may work with the latter throughout.

The center inputs are:

* Both source rings have exactly two invertibles, and their adjoint subring is
  the whole ring. The central-orbit audit gives exactly one central lift of the
  nontrivial invertible and no nontrivial central invertible over the unit.
* For R8_3_928 that lift is a semion, with twist `+i` or `-i`. Therefore the
  complete pointed center consists of the unit and this semion.
* For R8_3_941 that lift is a fermion, with twist `-1`. Therefore the complete
  pointed center is `sVec`. The frozen proof of this assertion excludes the
  alternative bosonic lift using the ordinary rank-four quotient bound; no such
  bound is applied to a fermionic quotient.
* Every one of the fourteen remaining R8_3_941 center allocations has 22 simple
  objects centralizing the fermion. These are necessary allocations, not fourteen
  established centers. Some still have unresolved integer feasibility.

The center-orbit input is
`evidence/rank8_frontier_20261021/review/quartic_central_orbits.json`.
The forced-fermion proof is
`evidence/rank8_frontier_20261021/quartic_integer_center/R941_FERMION.md`.
The final allocation list is
`evidence/rank8_frontier_20261021/review/r941_fusion_traces.json`.

## 2. Morita transport and uniqueness of invertible lifts

We use categorical Morita equivalence for fusion categories. If a category `M`
is Morita equivalent to a pseudo-unitary category `C`, it is pseudo-unitary:
both categorical dimension and Frobenius–Perron dimension are Morita invariant
([EGNO], Proposition 9.3.9 and Corollary 7.16.7). Their centers are braided
equivalent. Equip every pseudo-unitary category with its unique positive spherical
structure ([EGNO], Proposition 9.5.1); the center equivalence then preserves twists.

For any pseudo-unitary `M`, a central invertible that forgets to the tensor unit
has twist 1: its self-half-braiding and the pivotal structure on the underlying
unit are identities. Consequently, if `Z(M)` has no nonidentity invertible of
twist 1, the homomorphism

\[
\operatorname{Inv} Z(M)\longrightarrow\operatorname{Inv} M
\]

is injective. If `M` is braided, every invertible `a` of `M` has the two lifts

\[
(a,c_{a,-}),\qquad(a,c_{-,a}^{-1}).
\]

Injectivity forces them to coincide. A scalar isomorphism of lifts over a simple
object makes their half-braidings equal, so `a` centralizes every object of `M`.

## 3. Semionic obstruction: R8_3_928

**Lemma.** Suppose a pseudo-unitary fusion category `C` has no nonidentity
invertible of twist 1 in its center, and its center contains an invertible with
nontrivial self-monodromy. Then `C` has no braided Morita representative.

Indeed, take a putative braided representative `M` and transport that central
invertible to `Z(M)`. Its underlying invertible `a` has a unique central lift,
so the two lifts from Section 2 coincide and `a` is transparent. In particular
its self-monodromy is 1. The transported central object's self-monodromy is the
same scalar, a contradiction.

For R8_3_928 the only nonidentity central invertible is a semion `G` of order 2.
The balancing equation gives self-monodromy
`theta(G^2)/theta(G)^2 = -1`, and there is no nonidentity twist-one invertible.
The lemma applies. Section 1 transfers the conclusion to arbitrary complex
categorifications, not just their pseudo-unitary conjugates.

This does **not** assert that an unbraided category containing a central semion
splits as a tensor product. It also does not exclude arbitrary constructions by
modules or local modules in a larger braided category; those operations need not
keep the output in the braided category's Morita class.

## 4. Fermion-centralizer rank-square obstruction

**Lemma.** Let `M` be a pseudo-unitary braided fusion category whose Müger center
is `sVec`, generated by the transparent fermion `a`. Write `r = rank(M)`.
Then the centralizer of the induced fermion in `Z(M)` has rank `r^2/2`.
In particular, that rank is twice a perfect square.

**Proof.** Since `a` is transparent, balancing gives
`theta(a tensor X) = -theta(X)` for every simple `X`. Twists are nonzero, so
`a tensor X` is never isomorphic to `X`. The action of `a` on simples is free;
in particular `r` is even.

By [DNO], Corollary 4.4, the centralizer is braided equivalent to

\[
Z(M,\mathrm{sVec})\simeq M\boxtimes_{\mathrm{sVec}}M^{\mathrm{rev}}.
\]

By [DNO], Remark 2.11, this relative product is de-equivariantization of
`M boxtimes M^rev` by the diagonal Tannakian category generated by `(a,a)`.
Its regular algebra is `A = 1 direct-sum (a,a)`. The action of `(a,a)` on pairs
of simple objects is free. For a simple pair `V`, adjunction gives

\[
\operatorname{End}_A(V\otimes A)
\cong\operatorname{Hom}(V,V\otimes A)\cong\mathbb C.
\]

Thus its free module is simple. The same adjunction shows that two such modules
are isomorphic exactly when their pairs lie in the same diagonal orbit. Every
simple module is a summand of an induced simple object, by dominance of the free
module functor, so these orbits exhaust the simples. There are exactly `r^2/2`
orbits. Writing `r=2s` gives rank `2s^2`. This also explains why no additional
fixed-point splitting has been omitted. QED.

This lemma is a necessary condition for a **braided Morita representative**. It
does not impose a rank-square requirement on the center centralizer of an
arbitrary unbraided category with a central fermion.

## 5. Forcing a slightly degenerate representative for R8_3_941

Suppose `M` is a braided Morita representative of a pseudo-unitary
categorification of R8_3_941. Its center has exactly the unit and a fermion as
invertibles. By Section 2 the forgetful map on invertibles is injective, and the
braiding makes it surjective. Hence `M` has exactly two invertibles. Its
nontrivial invertible `a` is transparent and has twist `-1`.

Let `E` be the Müger center of `M`. This symmetric fusion category contains `a`
and has exactly two invertibles. Deligne's classification gives
`E = Rep(H,z)` for a finite group `H` and a central involution `z` ([EGNO],
Theorem 9.9.26). Put `m = |H| = FPdim(E)`. Lagrange's theorem for fusion
subcategories ([EGNO], Theorem 7.17.6) says that `D/m` is an algebraic integer,
where the source global Frobenius–Perron dimension is

\[
D=144+96\sqrt2+80\sqrt3+56\sqrt6.
\]

Its minimal polynomial and norm are

\[
p_D(t)=t^4-576t^3+11520t^2-73728t+147456,
\qquad N(D)=147456=2^{14}3^2.
\]

Taking the degree-four field norm of `D/m` shows `m^4` divides `147456`, hence
`m` lies in `{1,2,4,8}`. The fermion excludes `m=1`. Every group of order 4 is
abelian, and every group of order 8 has abelianization of order at least 4.
Those alternatives would give at least four invertibles in `Rep(H,z)`, contrary
to the two invertibles of `E`. Therefore `m=2` and `E=sVec`.

We can now apply Section 4. Under the center equivalence the unique fermion
goes to the unique fermion, so its centralizer must have rank twice a square.
The complete remaining allocation list instead gives rank 22 in all cases:

| Allocation index | Center pattern | Fermion centralizer rank | Other charge rank |
| ---: | ---: | ---: | ---: |
| 8 | 45 | 22 | 21 |
| 19 | 65 | 22 | 21 |
| 21 | 70 | 22 | 18 |
| 31 | 137 | 22 | 21 |
| 34 | 140 | 22 | 18 |
| 43 | 151 | 22 | 18 |
| 45 | 154 | 22 | 15 |
| 56 | 186 | 22 | 18 |
| 60 | 189 | 22 | 15 |
| 72 | 200 | 22 | 15 |
| 73 | 203 | 22 | 12 |
| 77 | 228 | 22 | 15 |
| 79 | 229 | 22 | 12 |
| 85 | 235 | 22 | 12 |

The verifier recalculates these values from the charge allocations, without
using the recorded rank values as input: four positive low simples and their
four fermion translates contribute 8; the remaining seven positive fermion
pairs contribute 14. The two remaining known simples have negative charge.

Thus `r^2 = 44`, impossible for an integer `r`. No braided Morita
representative exists. The simultaneous Galois transport from Section 1 gives
the same conclusion for general complex categorifications of R8_3_941.

## 6. Controls and remaining frontier

The exact control `M=sVec` has rank 2 and center the toric-code category. Its
fermion centralizer has rank 2, agreeing with `2^2/2`. Conversely, the center
of a semion category is the double-semion category: it has a nontrivial boson.
It therefore fails the no-boson hypothesis of Section 3, as it must because a
semion category itself is braided.

These results rule out all realizations as categorical Morita duals of braided
fusion categories, of any rank or dimension compatible with the invariants.
They give no contradiction for the residual unbraided Morita classes, no full
center fusion rules, and no solution of their associator equations. The public
general categorification status of both rings must remain unresolved.

## References

* [EGNO] P. Etingof, S. Gelaki, D. Nikshych, V. Ostrik, *Tensor Categories*,
  AMS, 2015. [Author's final PDF](https://math.mit.edu/~etingof/egnobookfinal.pdf).
* [DNO] A. Davydov, D. Nikshych, V. Ostrik, *On the structure of the Witt group
  of braided fusion categories*, Selecta Math. **19** (2013), 237–269.
  [arXiv:1109.5558](https://arxiv.org/abs/1109.5558), especially Remark 2.11
  and Corollary 4.4.

## Reproduction

From the repository root:

```sh
python evidence/rank8_research_20261022/r928_r941/verify.py
```

The small verifier uses only the Python standard library and compares its
deterministic receipt with `verification.json`.
