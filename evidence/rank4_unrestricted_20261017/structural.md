# Structural audit of the unrestricted rank-four argument

AI-generated research · independent verification pending

## Scope and conclusion

I read the structural arguments in Sections 1–7 and the complete uniform-bound assembly in Section 12, corresponding to `manuscripts/rank4/papers/companion_sections/01_introduction.tex` through `07_dimension_descent.tex` and `12_uniform_bound.tex`. I also read the supplied proof-dependency account and bibliography. I independently checked the induction/character interfaces against Ostrik's primary paper and the sphericalization interface against Bartlett's primary paper, and recomputed the main short polynomial identities from multiplication tensors rather than importing the attachment's checking code.

**Conclusion: no mathematical gap or counterexample was found in the assigned structural arguments.** The unrestricted hypotheses are respected: the category is a finite semisimple rigid complex linear tensor category with simple unit, without an assumed pivotal, spherical, braided, or unitary structure. The arguments establish the structural implications claimed in these sections, conditional only on the explicitly cited standard categorical results. This is an AI audit, not an independent human verification or a formal proof. It does not by itself certify the quadratic, cubic, quartic, pivotal-bound, or exhaustive-census arguments reviewed by other auditors.

The assembly in Section 12 is logically complete provided its four imported theorems are accepted: the spherical bound; the cubic sphericality/classification theorem; the quadratic short-orbit reduction and dimension bound; and the quartic dimension bound. I found no omitted dimension-field case in that assembly.

## Section 2: sphericalization and algebra

- A rank-four complex semisimple algebra with a one-dimensional representation is commutative: the only noncommutative dimension-four semisimple algebra is the single factor `M_2(C)`. The signed quotient really does have a positive coefficient-of-unit Hermitian form, so its regular star representation supplies the required semisimplicity. Its dimension character supplies the one-dimensional representation. It is therefore legitimate to identify the eight characters of the sphericalization with four ordinary and four signed characters.
- Self-dual lifts are justified. The two lifts of a self-dual simple have opposite nonzero spherical dimensions, while duality preserves spherical dimensions; consequently duality cannot exchange the two lifts.
- Spectral domination is valid for signed matrices: their entrywise absolute values are bounded by the nonnegative ordinary fusion matrices, hence every signed character value has modulus at most the corresponding Frobenius–Perron dimension. Equality of the global dimensions forces equality coefficient by coefficient in the dimension equations. The resulting selected lifts form an actual tensor subcategory mapping equivalently to the original category; this supplies a spherical structure on the given categorification, not merely a spherical realization of its ring.
- The integrality and field-containment interface is correct. For a commutative spherical category of dimension `2E`, central induction gives one constituent per character, with multiplicity one and dimension `E/f` or `E/g`. Ostrik Theorem 2.13 and Corollary 2.15 provide exactly the needed statements. No pseudo-unitarity assumption is needed for this interface. All formal codegrees are totally positive, so these eight constituent dimensions are positive at the selected real embedding.
- Galois changes are used algebraically, or by applying a complex-field automorphism to all structure constants when an actual conjugate category is required. Selecting a different signed dimension character alone is not an assertion that the original spherical structure changes. The section criterion at equality is nevertheless valid because it depends only on the signed structure constants and a positive character.
- The trace identity `tau(a) = Tr(a/E)` is applied only when the signed rational algebra is a field, where multiplication by `E` is invertible. The discriminant quotient is a rational square because both orders lie in the same number field; integrality makes its norm an integer square. I found no hidden assumption that one order contains the other.

### Absolute-value and trace rigidity

I independently formed all associativity equations for the symmetric ten-parameter rank-four tensor. Simultaneous associativity with `e` and `-e`, on the locus `e != 0`, yields precisely the three linear relations and four residual relations displayed in the proof. The diagonal-group normalization is legitimate because changing the sign of basis element `k` changes every coefficient `T_iik` by that sign. The five cases `d>f>0`, `d>f=0`, `d=f>0`, `d=f=0`, and `d<f` are exhaustive and establish a zero diagonal group or an impossible integer equation. Thus the final sign flip is valid. The trace-saturation corollary then follows termwise from sums of squares.

### Canonical central sign and indicators

The canonical central sign is the canonical `Rep(C2)` object from the equivariantization realization of sphericalization. Its underlying spherical dimension and ribbon twist are both `-1`. Applying the modular-character formula at this object gives the translate twist `chi(epsilon)`. Thus ordinary constituents translate to twist `+1` and signed constituents to twist `-1`.

The sixteen known objects in the second-moment argument are genuinely distinct: the eight constituents of `I(1)` have positive dimension, and their eight sign translates have negative dimension; tensoring by an invertible object is injective on isomorphism classes. This rules out the possible double-counting concern. The second indicators of the two self-dual lifts have opposite signs, as their pivotal maps differ by a sign. The sign object's odd indicators vanish and its even indicators equal `-1`.

The adjoint-parity lemma has the correct generality. For a skew self-duality `f` on `X`, the displayed self-duality on `Y X Y*` is skew; its induced pairing on `Hom(1,Y X Y*)` is nondegenerate and alternating. Rigidity identifies its dimension with the claimed adjoint multiplicity. This argument uses pivotality of the category in which it is applied; the sphericalization has that structure.

## Section 3: measures and inequalities

- All uses of positive measures in the general sphericalization arguments employ **squares** of real central dimensions, so they remain positive without pseudo-unitarity. The center has squared total dimension `4E^2`. Removing the sixteen known objects removes squared mass `2E^2(u+v)` from both the zeroth and second moments. The resulting nonnegative cosine-square moment gives exactly `E(u+v-1) <= sum |beta_i|`.
- The quartic averaged measure has total mass four. For an individual indicator order `n`, the hypothesis `L intersect Q(zeta_n) = Q` makes the two Galois averages independent because both fields are Galois. The normalized trace identity kills all nonunit basis terms. The resulting moment is `1/2` at odd orders and `1` at even orders, with no missing factor of two from the sign lifts.
- The forced atoms are `2u+v` at `+1` and `v` at `-1`. Subtracting `1/4` at `-1` is justified by `v>=1/4`; the residual measure has mass `15/4` and constant moments `3/4`. The Fejér bound is therefore applied with the stated constants.
- The squared-moment and short-conductor consequences respect the field-degree restrictions. A totally real quartic field has trivial intersections with cyclotomic fields of orders two, four, and six; order eight can contribute only `Q(sqrt(2))`. Among orders at most seven, only `Q(sqrt(5))` can give a nontrivial intersection, since a cubic real field cannot embed in a quartic field.
- For `Q(sqrt(2),sqrt(5))`, averaging orders `40j+n` projects the finite root-of-unity support onto the fortieth roots while retaining the required residue moments. The resulting additive-array form follows from discrete Fourier support in multiples of five or eight. I independently verified the exact additive-array identity and therefore the coefficient `5u+4v<=15/4`.
- The unsquared pivotal Fejér estimate is explicitly confined to a pseudo-unitary category or to a proved Galois conjugate of such a category. In that setting every central dimension is a positive combination of positive simple dimensions. Its three-term polynomial calculation and the weighted sum over nonunit simples are correct.
- In the quadratic comparison lemma, `k=Norm(E/D)` is a positive integer. For `k=1`, the inverse `D/E` is an algebraic integer because `E/D` is a norm-one integral unit. The trace gap is consequently legitimate. For `k>=2`, `D>E>=sqrt(k DD')` gives `D/D'>k`, and the stated strict inequality yields `q<=2P/3`.

## Section 4: non-self-dual sphericality

The duality trace argument correctly yields exactly two real characters. Under a nonspherical hypothesis, rational `D` is excluded by weak integrality, so the Frobenius–Perron character field and `Q(D)` are both the same real quadratic field. The signed dimension field contains it and has degree at most two, hence equals it. The two nonreal character factors are imaginary quadratic; their repeated formal codegrees are rational integers.

The arithmetic reduction to `k in {1,2}` and repeated signed codegree `g in {3,4}` is correct. The identity `g=2+a^2+2t^2`, together with integrality of `(1+a^2+t^2)/2`, excludes `g=5`; I checked its small possibilities independently. Evaluation of the signed table at the remaining characters gives the displayed near-group or `i`-character normal forms without a positivity assumption on the signed structure constants.

I checked the norm and trace formulas, the unit-gap arguments, and the final constant-codegree branch:

- In the `g=4` branch the ratio unit is at least `(3+sqrt(5))/2`, while `E'<5/2`; this forces the forbidden `D'<1`.
- In the `g=3`, positive-parameter branch, integrality of `E/3` forces `3|mu`. The quadratic field is ramified at three, ruling out the two small unit fields needed in the norm-one and norm-two subcases. The displayed bounds on `E'` are sufficient.
- At `mu=0`, the ordinary repeated codegree is `3 mod 8` and divides `2 DD'`; with `DD'` equal to 18 or 36 this forces codegree three, yielding either a rational `D` or negative discriminant.

The resulting sphericality theorem applies to every complex categorification with a dual pair. Its pseudo-unitary-conjugate corollary also follows: both real characters form the irrational Frobenius–Perron orbit, and a spherical dimension character must be one of them.

## Section 5: a nontrivial invertible object

The interchanged action gives the correct quadratic norm ratio `(mu^2+4)/(m^2+4)`. It is an integer at most one; equality forces a signed dimension codegree conjugate equal to `D`, giving the spherical section.

For the fixed action, a positive lift of the invertible object has dimension one and cannot send a positive lift to a negative lift. The rational codegree-two row is therefore present in both quotients. The quadratic case correctly reduces the other rational signed codegree to three or four. I independently verified the mixed-sign codegree-four norm `EE'=8(4b^2+4b+9)`, so integrality of `E/4` indeed fails. In the codegree-three case, norm integrality at denominators two and three forces `6|mu`.

The small trace/discriminant chart in the positive-parameter codegree-three case was independently recomputed: it consists exactly of `(k,T)=(1,4),(1,5),(3,6)`. The first two are eliminated modulo three; the last forces `p>1/2`. The constant-codegree case uses the correct ring of integers `Z[sqrt(6)]`.

The cubic codegree-two contradiction is particularly robust: two distinct induction constituents of dimension `E/2` must each occur at least twice in `I(G+)`. The eight-dimensional endomorphism algebra is then saturated by multiplicities two and two. All twists equal one, contradicting the first-indicator zero identity of the nontrivial simple `G+`. Independence of `1,x,y` follows from the faithful cubic character on the quotient by `G-1`. No positivity of general central dimensions is needed for this contradiction.

## Section 6: Fibonacci normal form

The symmetric two-by-two nonnegative action matrix satisfying `M^2=I+M` has trace one and determinant minus one. Its two possible label orderings do not commute, so left and right actions agree; duality cannot exchange the outside simples. The signed action normalizes by a permitted basis sign change. The stated ordinary and signed multiplication formulas follow.

For `(a,b)=(1,0)`, multiplicity-one sphericality applies. For `(1,1)`, opposite signed parameters give the radicand `6-phi` with norm 29. Its conjugate quadratic extension cannot coincide with the original unless 29 is a square in `Q(sqrt(5))`, which it is not. Thus the resulting quartic character field is nonnormal and cannot be cyclotomic. This is a valid signed-character obstruction.

## Section 7: columns, descent, and the Haagerup model

The simultaneous-column formula has the correct normalization: `S_(Achi,0)=1/(2 fchi)` and `S_(Bsigma,Achi)=1/(2 sigma(fchi))`. Symmetry gives `chi(F(Bsigma))=fchi/sigma(fchi)`. The folded coefficients are nonnegative integers, the signed coefficients are their differences, and their unit coefficients equal one because the sign translates are disjoint from `I(1)`.

For dimension-field descent, a nontrivial automorphism fixing `D` supplies a central simple with folded Frobenius–Perron dimension one and unit multiplicity one. Hence its underlying object in the sphericalization is exactly the positive unit, not the sign object. Its nontrivial half-braiding is a monoidal automorphism of the identity. The modular-character calculation forces its value on the sign to be one, so it descends to the original category. Its finitely many scalar values give a nontrivial faithful cyclic grading. This is the exact place where no injectivity of the character maps is needed.

The rank-four grading lemma covers all neutral ranks. In rank two it invokes the established rank-two categorical classification, not an unjustified classification of abstract rank-two rings. Equality of homogeneous component dimensions then supplies either weak integrality or a nontrivial invertible simple. This proves the dimension-field descent conclusion needed later.

For a quartic rational field algebra, the separate argument excluding lower degree of `D` is valid: a Galois automorphism fixing `D` must attain all individual spectral bounds, giving a sign grading. Neither weak integrality nor a nontrivial invertible can occur in the faithful positive field character. Thus the degree of `D` is four.

The Haagerup proof uses a valid fundamental-unit argument for `Q(sqrt(13))`. An integral totally positive `d`-number `E` has quotient `E/E'` equal to an even power of the fundamental norm-minus-one unit. The even and odd powers lead to the two displayed forms of `E`; divisibility by 117 forces their minimum to be at least `D` or 39, respectively. Both contradict the proper signed quotient.

## Section 12: complete scope of the assembly

Spherical categories are delegated to the independent pivotal bound. A nonspherical category is self-dual by Section 4 and has irrational `D`. The Frobenius–Perron character field has degree at most four, so the degree of `D` is two, three, or four. Degree three is excluded by the cubic theorem. The descent corollary then identifies the signed dimension field with `Q(D)` in degrees two and four. These are precisely the hypotheses required for the quadratic and quartic reductions. Once `D<1000`, the coefficient bound `N<=d_X<sqrt(D)<32` gives integral multiplicity at most 31. No multiplicity assumption is used to obtain the bound.

## Presentation refinements, not blockers

1. When the selected real embedding changes, consistently call the resulting dimension values **embedded spherical dimensions**. This avoids suggesting that an arbitrary Galois-conjugate character is a different pivotal structure on the unchanged category. The proof itself already transports the relevant identities correctly.
2. In the descent proof, “Define `A` and `B_sigma` as in the preceding proof” mentions an unused `A`; defining only `B_sigma` would be clearer.
3. It would help readers to explicitly identify the canonical central sign with the `Rep(C2)` object of sphericalization's equivariantization construction when its twist `-1` is first used.
4. The unrestricted result is a theoretical uniform reduction followed by exact finite certification. It should not be described as a wholly noncomputational classification, even though the preliminary multiplicity bound is purely theoretical.

## Reproducible algebra checks

Run `python evidence/rank4_unrestricted_20261017/structural_algebra.py` from the repository root. Its sibling JSON records the successful checks. The script independently builds the ten-parameter tensor and verifies the exceptional sign-rigidity equations, the forty-root additive-array identity, the fixed-action norm obstruction, the two quadratic norm formulas, the trace/discriminant chart, and the non-self-dual small-codegree rows. These checks do not formalize the categorical arguments.

## Primary sources consulted

- Victor Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822, especially Example 2.9, Theorem 2.13, Corollary 2.15, and Section 5.1: https://arxiv.org/pdf/1309.4822 . These give the induction constituents, modular characters, field containment, and sphericalization section criterion used above.
- Bruce Bartlett, *Fusion categories via string diagrams*, arXiv:1502.02882, Section 5.3 and Corollary 5.15: https://arxiv.org/pdf/1502.02882 . These realize sphericalization as equivariantization and specify its canonical spherical dimensions.
