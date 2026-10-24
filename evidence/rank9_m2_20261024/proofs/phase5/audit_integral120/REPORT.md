# Independent adversarial audit of the dimension-120 exclusions

**Verdict: PASS.** The arguments in `phase5/integral120/THEORY.md` establish general non-categorifiability over C of `R9_2_12` and `R9_2_959`, using the previously audited complete group-theoretical exclusions within their established scope. No missing categorical premise or scope error was found. In particular, the proof does not replace pseudo-unitarity by unitarity.

The author verifier was replayed successfully. A separate implementation, `independent_checks.py`, reads the original compressed census and independently cross-checks it against `work/verification_corpus.json`; it does not import the author verifier. Its result is `independent_checks.json`, also PASS. The author files and previous phases were not revised by this audit.

## 1. Fermion parity and the Tannakian reduction

The induction statement applies to arbitrary spherical fusion categories. Integrality gives the positive spherical structure, and dimensions of central objects equal those of their images under the forgetful functor. Thus the center is integral and nondegenerate, as needed for the prime-power criterion.

The following reasoning is valid and is the essential new step:

1. A dimension-five simple in the center forces a nontrivial symmetric subcategory by ENO Corollary 7.2.
2. A symmetric category of dimension greater than two contains a nontrivial Tannakian subcategory, including the super case: for `Rep(G,z)`, the even part is `Rep(G/<z>)`. Only sVec needs separate treatment.
3. With canonical positive dimensions, its fermion χ has dimension one and twist −1. Since all constituents of A=I(1) have twist +1, χ has coefficient zero in A.
4. The χ coordinate of the exact identity `S[A]=120[A]` is consequently zero. Monodromy with χ on each simple constituent is a scalar ε=±1: the tensor product with an invertible remains simple, and the scalar is multiplicative in the invertible variable, whose order is two.
5. Thus the dimensions of the ε=+1 and ε=−1 constituents each sum to 60. The unit belongs to the positive part. Every other dimension is even except the single dimension-five constituent, which must therefore also belong to that part.
6. The centralizer of sVec in the nondegenerate center has Müger center exactly sVec. It is integral and contains the dimension-five simple. ENO Proposition 7.4 therefore supplies a nontrivial Tannakian subcategory.

No positivity of a Hilbert-space inner product is used. The entire fermion argument uses categorical positivity, the induction S-eigenvector, and scalar monodromy. This direct argument is sufficient; the relative-center derivation is not needed for the conclusion. I also checked that derivation: the relative-center unit-morphism equation and naturality of the fermion's half-braiding combine to the stated scalar monodromy condition. The injectivity on invertibles follows from the trivial universal grading, so the dimension-two subcategory used there is nontrivial.

Dai Lemma 3.1 has exactly the claimed hypothesis: an integral dimension-120 category with a nontrivial Tannakian subcategory in its center is weakly group-theoretical. Its use does not presume a Tannakian subcategory in C itself or a braiding on C. The two-primary branch and the de-equivariantized-center branch are applicable as written.

Primary checks: [ENO, arXiv:0809.3031](https://arxiv.org/abs/0809.3031), Corollary 7.2 and Proposition 7.4; [Ostrik, arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Theorem 2.5, Proposition 2.8 and Theorem 2.13; [Dai, 2025](https://inmabb.criba.edu.ar/revuma/pdf/v68n2/v68n2a03.pdf), Lemma 3.1.

## 2. The dimension-30 obstruction includes all twists

The claim that an integral dimension-30 category has only simple dimensions one and two is proved, not inferred from an untwisted search. ENO Theorem 9.2 first puts it in the group-theoretical class.

I checked the group argument independently. A group of order 30 has a normal cyclic subgroup P of order 15. The stated Sylow-counting argument is valid: six Sylow-five subgroups would account for 24 nonidentity elements; ten Sylow-three subgroups would require 20 additional nonidentity elements. Thus in that case Sylow three is normal. Its quotient of order ten has normal Sylow five, giving a normal subgroup of order 15; such a subgroup is cyclic, so its characteristic Sylow five would be normal in the original group, a contradiction. Normal Sylow five and the normal Sylow-three subgroup in the quotient of order six then give P.

For any subgroup H and double-coset intersection K, the cyclic subgroup Q=H∩P is normal in the whole group (all subgroups of cyclic P are characteristic) and lies in K. Since [H:Q] is at most two, either K=H or K=Q. Every K has square-free order. Its complex Schur multiplier vanishes: restriction to each cyclic Sylow subgroup is injective on the relevant primary part by transfer, and the target is zero. Thus arbitrary associators and relative cochains cannot introduce a projective degree omitted from the ordinary degree calculation.

If K=Q, its projective irreducibles have degree one and [H:K]≤2. If K=H, the cyclic subgroup Q has index at most two, so Clifford theory gives degrees at most two. This covers every group-theoretical simple. The forbidden dimension-three object therefore cannot occur.

## 3. Both dimension-60 nonsolvability arguments are valid

For type `(1^6,3^6)`, the stabilizer G[X] has order dividing 9 and 6; the dimension equation for XX* makes it divisible by three. It is therefore the unique order-three subgroup H of the six-element invertible group. H fixes all six three-dimensional simples, lies in the adjoint category, and XX* has a noninvertible remainder of dimension six. Hence any neutral grading component contains at least three invertibles and one three-dimensional simple.

The grading enumeration can be checked without software. If the grading group has order u>1, each component has dimension 60/u≥12, so u is 2,3,4, or 5. For u=3, a component of dimension 20 must have type `(1^2,3^2)`, impossible for the neutral component. For u=4, each dimension-15 component would need six invertibles; for u=5, each dimension-12 component would need three. Both exceed the total inventory. Only u=2 remains, with both components of type `(1^3,3^3)` and dimension 30, already impossible. Thus the universal grading is trivial.

The last step of a solvable construction is consequently an equivariantization by C2 or C3. The C2 action is free on the three-dimensional simples because their stabilizer has odd order, and the descent has forbidden type `(1^3,3^3)`. For C3, the fixed simple free-module endomorphism algebras are twisted C3 group algebras. Their cocycles are cohomologically trivial, so each three-dimensional simple splits into three invertibles. The de-equivariantization is pointed of dimension 20. A C3 action on its group K fixes its characteristic Sylow C5 pointwise, since Aut(C5) has order four. It therefore has at least five fixed elements. Each fixed invertible gives three invertibles after equivariantization, contradicting the required six. There is no omission of projective stabilizer representations in this count: H²(C3,C*)=0.

For type `(1^2,2,3^2,6)`, the square 36 of the dimension-six object excludes every nontrivial grading, since such a component has dimension at most 30. A final solvable step can only be C2-equivariantization. The involution fixes the unique dimension-two and dimension-six simples and exchanges the dimension-three pair. The free-module decomposition gives type `(1^3,3^3)` below, again impossible.

For the source rings, every potential underlying central involution is included. The independently computed lists and types are:

| Source | Involution labels | Dimension-60 type |
|---|---|---|
| R9_2_12 | 1, 2 | `(1^2,2,3^2,6)` |
| R9_2_12 | 7 | `(1^6,3^6)` |
| R9_2_959 | 8 | `(1^6,3^6)` |

The fixed/free-orbit rules follow from the free-module adjunction and the vanishing cyclic Schur multiplier. They are not merely counts guessed from dimensions.

## 4. Nonsolvable weakly group-theoretical dimension 120 implies group-theoretical

This lemma was checked with attention to both orders of the extension tower.

Weak group-theoreticality provides a Morita-equivalent nilpotent category of the same dimension. Its faithful grading-group orders multiply to 120. If each grading group is solvable, its normal composition series refines that extension into cyclic-prime extensions; the resulting category and its Morita class are solvable. Thus a nonsolvable category requires a nonsolvable grading group.

Among proper divisors of 120, only 60 can be the order of a nonsolvable group; a nonsolvable group of order 60 is A5. A factor of order 120 leaves no other nontrivial factor and gives a pointed category immediately. A factor of order 60 leaves exactly a C2 stage. There are only two orders to examine:

- **A5 then C2.** For P=`Vec_A5^ω`, every extension component is an invertible P-bimodule category, so its underlying left module has pointed dual. Naidu–Nikshych Example 2.2 applies to arbitrary ω and forces the stabilizer to be a normal abelian subgroup of A5, hence trivial. The component has 60 simples, transitively permuted by P, with equal Frobenius–Perron dimensions. Its dimension is 60, so all simples have dimension one.
- **C2 then A5.** For either associator on `Vec_C2`, its center is pointed with four simple objects. Braided automorphisms act faithfully on those objects: in the classification by metric groups, an object-fixing braided autoequivalence is tensor-isomorphic to the identity. Hence BrPic(P) embeds in S3. Every homomorphism from A5 to it is trivial. Every extension component is therefore the regular P-bimodule and has two equal-dimensional simples, whose squared dimensions sum to two. Again they are invertible.

The extension associators and coherence data do not affect these simple-count and dimension conclusions. The nilpotent representative is pointed, proving that the original category is group-theoretical. This does not claim that all dimension-120 fusion categories are group-theoretical.

The arbitrary-associator module premise was checked directly in [Naidu–Nikshych, arXiv:0705.0665](https://arxiv.org/abs/0705.0665), Example 2.2. The Brauer–Picard identification and pointed braided category classification are in [EGNO](https://math.mit.edu/~etingof/egnobookfinal.pdf), Sections 8.27 and 8.4. Solvability's equivalent direct construction and Morita formulation are ENO Definition 1.2 and Proposition 4.4.

## 5. Exact evidence and final implication

The independent replay verifies the full source tensors, associativity, positive dimensions, trivial universal grading, and the full induction formula `FI(X)=ΣY YXY*`. Its characteristic polynomial independently yields the claimed formal codegrees and induction dimensions. All nine fermion sign solutions with zero signed dimension sum put the dimension-five summand in the centralizing part. Every source involution and all grading possibilities were independently enumerated.

Source tensor hashes:

| Ring | Canonical compact-JSON SHA256 |
|---|---|
| R9_2_12 | `da611b1fd91686294deac7afe234e3732658da54718c4669deeffa95c3295cf8` |
| R9_2_959 | `891b9cf737debdc8a1fbd3d2281c2db06ac07778587b500ad4f343d72862a1c4` |

The author verifier additionally revalidates the existing phase-four GT audit status and its recorded source hashes. This audit accepts that independently audited all-cocycle GT theorem as an explicit dependency; it does not replace it by a new untwisted search.

The logical chain is complete: the fermion argument forces weak group-theoreticality; the existing no-GT result and Section 4 force solvability; trivial universal grading forces a final C2-equivariantization; and every resulting dimension-60 type is nonsolvable. Both general exclusions are approved.

Independent replay:

```sh
python rank9_m2_research/phase5/audit_integral120/independent_checks.py
```

Output: `PASS: independent raw/corpus, ring, full-induction, parity, involution and grading checks`.
