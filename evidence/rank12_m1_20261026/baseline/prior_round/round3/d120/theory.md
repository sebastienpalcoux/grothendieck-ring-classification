# Complete dimension-120 family: three new models and twelve exclusions

This argument concerns arbitrary complex fusion categories. It assumes neither unitarity nor the unproved claim that every dimension-120 category is weakly group-theoretical. Independent human verification remains pending.

The supplied dimension-120 rings have type (1^4,2^4,5^4). Besides the previously modeled R12_1_25, the only categorifiable based rings in this family are R12_1_142, R12_1_361 and R12_1_444. All four models are unitary group-theoretical categories. The other twelve supplied rings are excluded over C.

## 1. Two forced Morita reductions

For each source, its dimension-20 fusion subring has four invertibles and four dimension-two objects. There is a unique involution b fixing all four dimension-two objects on both sides. On the dimension-five objects b acts freely, and its left and right permutations coincide. These are exact tensor facts, checked in verify.py.

Apply the cyclic common-stabilizer Morita lemma proved in the prior continuation (`family_quadratic/cyclic_stabilizer_morita_lemma.md`): the regular algebra A=1+b exists, and the dimension-20 subcategory becomes pointed after A-bimodule duality. Its group of invertibles has order twenty. On each free two-element b-orbit of dimension-five simples, the stabilizer for the left-right C2 action is cyclic of order two. Its projective multiplier is a coboundary, giving two A-bimodule structures of dimension five. Hence the whole Morita dual D has type (1^20,5^4). The reverse algebra is 1+c, for an actual involution c in G(D).

For completeness, the cyclic-stabilizer lemma uses actual right A-modules. A fixed object of dimension two has a right A action because the stabilizer obstruction lies in H^2(C2,C*)=0. Its internal endomorphism algebra has dimension 2 and contains the unit; it therefore consists entirely of invertibles, necessarily 1+b. The left C2 stabilizes the right module, and the same H^2 vanishing supplies commuting left actions. Thus all corresponding A-bimodules have dimension one. No based-ring automorphism is promoted to a tensor action.

Let H be the unique Sylow-five subgroup of G(D): uniqueness follows from Sylow, since its number divides four and is 1 modulo 5. It is cyclic and normal. Its left and right actions on the four noninvertible simples are trivial, since C5 has no nontrivial homomorphism to S4. The regular algebra B=⊕_{h∈H}h exists: the action on a fixed simple trivializes the pointed associator on H.

Take a simple right B-module M whose underlying object is one of the dimension-five simples rho. Such an action exists by H^2(C5,C*)=0. Its internal endomorphism algebra in D has dimension FPdim(rho)^2/FPdim(B)=5 and contains the unit. It cannot contain a noninvertible simple, since these all have dimension five. Each invertible has multiplicity at most one in this internal endomorphism algebra, by simplicity of M. Its support is the subgroup of invertibles fixing M as a right B-module, so this subgroup has order five. By uniqueness of the Sylow-five subgroup of G(D), it is H. Therefore every h in H fixes M as a right module. No claim about the full left stabilizer of rho is needed. H^2(C5,C*)=0 then supplies a left B action on M, making it a simple B-bimodule of dimension 5/5=1. For each rho there are five simple right-module structures and, on each, five left-action character choices. Thus these four rho sectors yield 4·5·5=100 invertible B-bimodules.

The pointed sector also gives only invertible B-bimodules: H is normal and cyclic, every double coset is a single H-coset, and all projective representations of H have dimension one. The pointed sector contributes 4·5=20 invertibles, so the total is 100+20=120. Consequently E={}_B D_B is pointed of dimension 120. Thus every categorification of a source ring is group-theoretical.

The reverse subgroup has order ten, not merely an unspecified order dividing 120. Put R=1+c in D. Since H has odd order, c is outside H. The free B-R-bimodule B⊗R has ten distinct invertible homogeneous summands. The left H and right C2 actions are transitive, so the bimodule is simple. Its normalized module dimension is 10/sqrt(5·2)=sqrt(10); its internal endomorphism algebra in E is therefore connected of dimension ten. A connected separable algebra in a pointed category is a twisted subgroup algebra. Hence the source is C(G,ω,K,ψ), with |G|=120 and |K|=10. This uses an actual algebra furnished by the two Morita equivalences.

## 2. The group and subgroup are forced

If K=C10, the identity double-coset sector already has ten invertibles, impossible. Thus K=D10 (dihedral of order ten). H^2(D10,C*)=0: restriction to either cyclic Sylow subgroup is injective on the corresponding primary part and the cyclic Schur multipliers vanish.

Every normalizer double coset therefore contributes the ordinary D10 character degrees 1,1,2,2. Exactly four invertibles force |N_G(K)|=20. These two cosets account for all four dimension-two objects. Every other double coset has stabilizer C2 and size fifty, accounting for two dimension-five objects. There are precisely two such double cosets. Proper intersections of order five would produce unwanted additional dimension-two objects, while trivial intersections would produce dimension-ten objects.

G cannot be solvable. Otherwise a Hall {2,5}-subgroup L of order forty contains K (the standard containment part of Hall's theorem). Since K≤L, L is a union of K-double cosets. It cannot contain a size-fifty coset, so it would be contained in N_G(K), of order twenty: a contradiction.

The nonsolvable groups of order 120 are A5×C2, S5 and SL(2,5). This follows from their composition factors A5 and C2: either A5 is normal of index two (giving its direct product or the outer extension S5), or C2 is central with quotient A5 (giving the split extension or its Schur double cover). SL(2,5) has a unique involution and contains no D10.

Every D10 in S5 lies inside A5. A D10 in A5×C2 projects injectively to the unique conjugacy class of D10 in A5 and is either the trivial graph or the graph of its reflection-sign character. In S5 and the trivial-graph case, the quotient C2 yields a faithful grading with neutral category of type (1^2,2^2,5^2), regardless of admissible cocycle. A dimension-five object's product with its dual has dimension 25, larger than the sum 2+4+10=16 of all neutral simple dimensions. It cannot be multiplicity-free. These cases are impossible.

Thus the only group-subgroup pair is

  G=A5×C2, K={(h,sgn_D(h)):h∈D10}.

## 3. All admissible cohomology classes

Subgroup cochains introduce no extra parameter because H^2(K,C*)=0. Admissible classes are the kernel of H^3(G,C*)→H^3(K,C*).

Its 5-primary part is zero: the index [G:K]=12 is prime to five, so restriction is injective on 5-primary cohomology.

The 3-primary part is cyclic of order three. Restriction to C3 is injective; H^3(C3,C*)=C3, and conjugation inversion acts trivially in degree three. Transfer supplies the nonzero class. This primary part has no effect on fusion rules, by the coprime-twist lemma below, since 3 does not divide |K|=10.

The 2-primary part of H^3(G,C*) is C2^3. Here is a concrete dimension argument. Restriction to the Sylow group P=V4×C2 is injective, and the image is invariant under the normalizer C3 acting irreducibly on V4 and trivially on the last C2. In H^3(P,C*)=C2^7, this invariant subspace has dimension three: the Kunneth filtration consists of H^3(V4,C*) (dimension3, invariant dimension1), H^3(C2,C*) (dimension1), H^2(V4,Z)⊗H^2(C2,Z) (dimension2, no invariants), and Tor(H^3(V4,Z),H^2(C2,Z)) (dimension1, invariant). Since the C3 order is odd, invariants are exact on these F2 modules.

Three independent global classes attaining this bound are:

* u: the nonzero 2-primary class from A5, obtained by transferring the anisotropic V4 three-cocycle;
* v: the external C2 three-cocycle (-1)^(t1 t2 t3);
* w: the Schur-cover cup product (-1)^(λ(a,b)t3), with λ a C2-valued cocycle of SL(2,5)→A5.

Independence follows by restriction to V4, to the external C2, and by the mixed slant invariant, respectively. The latter is the nonzero Schur multiplier of V4, supplied by the Q8 preimage in SL(2,5). Every class restricts to the nonzero 2-primary class on K: u restricts nontrivially to any involution of A5, v to the reflection-sign graph, and w has λ(s,s)=1 at a reflection lift of order four. Thus the relative 2-primary kernel is C2^2, generated by u+v and w+v.

The exact cocycles are reconstructed in all_graph_twists.py. For u, on V4 written F2^2 use

  f(x,y,z)=x0 y0 z0+x1 y1 z1+x0 y1 z1 mod2.

Its restriction to each nonzero cyclic subgroup is the nontrivial three-cocycle. Corestriction to A5, using fifteen coset representatives, gives u. The restriction back to V4 is the sum of its three normalizer conjugates; all other Mackey intersections are trivial. Thus it retains the anisotropic class. A normalized two-cochain gauge makes u|D10 exactly the cube of the reflection-sign character. The Schur section is separately chosen so λ|D10 is the square of that character. These gauges make u+v and w+v exactly trivial on K, so ψ=1 is an actual subgroup algebra cochain.

## 4. Coprime-twist invariance

Lemma. Let p not divide |K|, and let η be a p-primary group three-cocycle. Multiplying a group-theoretical associator by η, with a compatible p-primary subgroup trivialization, does not change the based fusion ring.

Proof. Choose finite roots of unity for all data and a complete strictly henselian discrete valuation ring O of mixed characteristic (0,p) containing these roots. All p-power roots reduce to 1; roots of order prime to p remain distinct. The twisted category is modeled by G-graded K-bimodules over O. On each double-coset component its algebra is a matrix algebra over a twisted stabilizer group algebra. Every stabilizer has order dividing |K|, a unit in O; these algebras are separable over O and have split semisimple residue fibers. Primitive idempotents and the corresponding simple modules lift, with unchanged multiplicities and ranks. Tensor product over the subgroup algebra is a direct summand of the ordinary tensor product, via the separability idempotent with denominator |K|. Hom spaces likewise arise from averaging idempotents over stabilizers. All these modules are finite free and their ranks are unchanged on reduction. Therefore the fusion coefficients in characteristic zero equal those of the reduced category. The η twist and its subgroup cochain reduce to 1, so the two compared categories have identical reductions and fusion rings. This proves the assertion. The argument does not assume that p is coprime to |G|; pointed G-graded vector spaces remain semisimple, and only stabilizer orders enter the separability argument.

In particular the formerly proposed 3-primary twist on SL(2,5) with Dic5 cannot change its known multiplicity-two fusion rules. More importantly, the lemma removes the entire 3-primary part in the exhaustive graph-subgroup classification above.

## 5. Four exact outputs

The two binary parameters multiply the two relative generators. Using the order [u+v,w+v], the outputs are:

| Parameters | Source ID |
|---|---|
| (0,0) | R12_1_25 (previous positive control) |
| (0,1) | R12_1_142 |
| (1,0) | R12_1_361 |
| (1,1) | R12_1_444 |

These are actual unitary subgroup-bimodule categories, with modulus-twenty monomial actions. The computation checks all module equations, completeness and orthogonality of the projective characters, all balanced quotient identities, and every fusion coefficient. It checks all 1728 coefficients of the basis identifications to the supplied inputs. A separate independent Hom-space reconstruction has passed for all four models in normal and optimized Python; see ../independent/construction_audit.md.

Excluded source IDs: 161, 211, 262, 265, 312, 362, 388, 453, 469, 472, 503, 516 (all with prefix R12_1_).

These exclusions use the categorical converse and exhaustive cohomological coverage. They are not conclusions from a failed bounded search.

## References

The group-theoretical model and subgroup-module classification are standard: Etingof--Gelaki--Nikshych--Ostrik, Tensor Categories, §§7.4 and9.7; Schauenburg, A higher Frobenius--Schur indicator formula for group-theoretical fusion categories, arXiv:1502.02906 (including its erratum for indicator formulas; no indicator formula is used here). The Morita dimension identities are standard internal-end identities. The finite-group arguments use Hall's theorem, the Schur multiplier of A5 and cyclic-group cohomology. Coprime-twist invariance is proved explicitly above and is used only as a fusion-ring statement, not a tensor-equivalence assertion.
