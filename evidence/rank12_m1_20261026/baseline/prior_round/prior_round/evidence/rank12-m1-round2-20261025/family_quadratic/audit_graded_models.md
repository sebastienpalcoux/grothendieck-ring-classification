# Independent categorical audit: R12_1_156 and R12_1_449

**Result: PASS for R12_1_156, R12_1_263 and R12_1_449.** The audit covers seven recorded Morita identifications, as well as the direct C4 TY equivariantization of R449. No conclusion is made about failed discovery attempts or unrecorded future variants.

## R12_1_156: Liptrap category and its actual Morita dual

The precursor has serf group F20=C5 semidirect C4, four lords, stabilizer C5, quotient involution inversion and p=0. It is an actual feudal rule: the quotient extension is the dihedral group of order eight, and the kernel of the group homomorphism F20 -> D8 is C5. This is the setting of Liptrap's reconstruction theorem, without a two-lord restriction.

I checked the primary paper arXiv:1002.3166v2, Definition 4.3, Theorem 4 and Lemma 5.4. The positive phase data have fifth-root values, normalized upsilon, nondegenerate symmetric stabilizer bicharacters, and constant tau=1/sqrt(5). The exact phase equations give a genuine fusion system. All scalar recouplings are phases; the remaining recouplings are normalized Fourier blocks, checked exactly. This supplies an actual unitary precursor, rather than merely a consistent fusion tensor.

The algebra A=1+c uses a noncentral involution c in the serf group. Its restricted associator is exactly trivial. It is therefore the ordinary connected separable group algebra of C2 in the unitary pointed subcategory, with its standard Q-system structure. Centrality or a braiding is not needed for its Morita dual. The category of A-bimodules is a unitary fusion category of dimension forty.

The constructor classifies simple bimodules by C2 double orbits. Left multiplication is free. The orbits of size four have trivial stabilizer and one simple; those of size two have cyclic stabilizer of order two and two projective characters. Enumerating square-root phases in tenth roots exhausts these characters after the displayed gauge fixing. The resulting simples have dimensions 1^4,2^4,sqrt(5)^4.

The relative tensor product is the actual coequalizer of the right action on the first factor and the left action on the second, with the relevant associator inserted. I derived the signs from the categorical equations, and checked both action descent and all constituent bimodule axioms. As an additional check beyond the reconstruction equations, the audit evaluates all **480,000 scalar pentagons with at most two lords**, precisely the F-blocks entering these balanced products. All pass.

For an independent decomposition, I replaced the constructor's stabilizer-character trace formula by weighted relation graphs. These compute the balanced quotient and then all monomial intertwiner spaces from every simple bimodule. This gives all **1,728 fusion coefficients** again. The tensor agrees with the recorded model and matches R12_1_156 under the stored exact based bijection.

Receipt counts: 1,600 quasisymmetry equations; 32,000 biderivation equations; 64 exact unitary Fourier blocks; 480,000 scalar pentagons; 144 balanced products; 1,728 independent Hom dimensions.

The bar placement in Liptrap's beta_3 formula was explicitly reviewed against the primary definition with the constructing agent. The exhaustive mixed pentagons pass both for the self-dual F20,p=0 precursor and for the non-self-dual-lord D10xC2,p=2 precursor used in the alternate R449 models. Thus the latter is checked directly, rather than inferred by analogy from self-dual lords.

## R12_1_449: a genuine weak C4 action on TY(C5)

The TY category uses chi(a,b)=exp(2 pi i ab/5) and positive tau. Inversion preserves this bicharacter, so it gives a strict unitary tensor functor F with F^2=Id. The C4 action is weak: its generator is F, and the chosen F^4 coherence is the monoidal natural parity character epsilon, equal to -1 on the TY-odd simple and +1 on pointed simples. This does not assert that inversion has order four as a permutation.

Writing g,h in {0,1,2,3}, the action coherence is epsilon^floor((g+h)/4). The carry identity verifies its group-action associativity; epsilon is F-invariant and monoidal because the TY rule is C2 graded. Consequently the equivariantization is an actual unitary category. The odd simple has projective stabilizer eigenvalues lambda^4=-1, and the pointed nontrivial orbits have cyclic stabilizer of order two.

The audit recomputes the stabilizer multiplicities by exact eighth-root character projection, independently of the shared cyclic-equivariantization routine, then checks all **1,728 coefficients** against R12_1_449. The retained zero-zest representative already gives this ring, so no additional zest hypothesis is required for its existence.

## Normalized grading-cocycle twists: R12_1_263 and alternate models

The audit also checks every retained model in `feudal_twist_results.json` and `feudal_abelian_twist_results.json`. The former includes R263 from a nontrivial dihedral-grading cocycle, together with alternate R156 identifications; the latter supplies alternate R449 models. In each record the grading group and the fusion grading are checked, all normalized cocycle identities are checked exactly (4096 equations), and the twisted associator is formed by multiplying the actual Liptrap associator by the inflated unit-modulus three-cocycle. This operation preserves the pentagon and unitarity.

The order-two subgroup algebra is separately checked *after twisting*: the restriction of the twisted associator to (c,c,c) is one. A nontrivial C2 three-cocycle cannot be removed by a normalized two-cochain, so this gate is necessary and has not been inferred merely from the untwisted fifth-root phases. For each twisted model the audit again reconstructs all balanced quotients and all 1728 intertwiner dimensions, independently of the constructor's cyclotomic trace reduction, allowing tenth-, twentieth- and fortieth-root phases. Every stored tensor and input basis map agrees exactly.

## Reproducibility and limits

`audit_graded_models.py` writes `audit_graded_models.json`; its checks use explicit exceptions and survive optimized Python. The receipt identifies the specific files examined by hashes. The theorem establishing a fusion system from its uberderivation remains a cited categorical premise, not a computer formalization. The independent replay checks its explicit data and all F-blocks required for the new Morita computation. No online or baseline source files were modified.
