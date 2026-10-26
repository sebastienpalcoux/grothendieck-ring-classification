# Independent audit: all fifteen remaining dimension-120 cases are group-theoretical if categorifiable

This is an implication about every complex categorification. It does not assert existence, and does not use a classification of all dimension-120 fusion categories.

## Prime-dimensional pointed-dual lemma

Let D be a fusion category over C. Assume that its invertibles form a finite group G with a unique subgroup H of prime order p, that every noninvertible simple has FP dimension p, and that there are 0<t<p noninvertible simples. Then D is group-theoretical. In fact D is Morita equivalent to a pointed category by the regular algebra B on H.

**Proof.** Tensoring on the left or on the right gives an action of H on the t noninvertible isomorphism classes. All its orbits have length 1 or p, and t<p. Hence H fixes each of these simples on both sides. In particular the pointed subcategory on H has a rank-one module category, furnished by any one of those objects; its associator restricts cohomologically trivially. The regular connected separable algebra B=direct_sum(h in H)h therefore exists.

The simple right B-modules can be classified orbit by orbit. On invertibles the right H-action is free, so each simple has underlying object the sum over an H-coset, of FP dimension p. On a noninvertible X, the stabilizer is all H. Since H^2(C_p,C^*)=0, the relevant projective representations are one-dimensional; there are p simple module structures, each with underlying object X and FP dimension p. Thus every simple right B-module M has underlying FP dimension p.

The internal endomorphism algebra End_D(M)=M tensor_B M^* has FP dimension p^2/p=p and contains the unit once. It cannot have a noninvertible constituent, because such a constituent would already have dimension p in addition to the unit. Its invertible constituents have multiplicity either 0 or 1: Hom_D(g,End_D(M)) is Hom_B(g tensor M,M), and both modules are simple. Their support is the subgroup of G stabilizing the isomorphism class of M. This subgroup has order p, hence is exactly the unique H.

Consequently every h in H sends M to an isomorphic right B-module. Choose right-B-linear identifications h tensor M -> M. Their associativity defect is a scalar 2-cocycle on H, after fixing the multiplication of B. Since H^2(H,C^*)=0, rescale them to obtain a coherent left B-action commuting with the right action. The p characters of H give the p resulting simple bimodule structures. More generally, all equivariant objects over this fixed right-module isomorphism class are described by projective representations of H, so this exhausts them. All simple B-bimodules therefore have underlying FP dimension p, and bimodule FP dimension p/FPdim(B)=1. Thus D_(B|B) is pointed. QED.

In the application below, |G|=20 and p=5. Sylow's theorem gives a unique subgroup H of order 5, since n_5 divides 4 and n_5=1 mod 5. There are exactly four noninvertibles, so t=4<p=5. No transitivity of the invertible action and no determination of the full stabilizer of a noninvertible is required.

## First Morita step from the supplied rank-twelve tensors

Each of the fifteen supplied rings has an integral based subring E of type (1^4,2^4), FP dimension 20. There is a common left and right stabilizer K={1,h} of every dimension-two basis object, with h of order two. These are full stabilizers among the four invertibles. Therefore the regular algebra A=1+h exists: the fixed simple trivializes the pointed associator on K.

The same right-module/internal-end argument, now inside E with p=2, proves that E_(A|A) is pointed. Every simple right A-module has underlying dimension two. Its internal end has dimension two, contains 1, and has only invertible constituents. The support must be K: every invertible stabilizing a module with underlying noninvertible X stabilizes X, whose full stabilizer is K; for an invertible coset module this also follows directly. Thus the right modules admit coherent left K-actions, and all simple A-bimodules in E have dimension one. The dual contains twenty invertibles.

The remaining four source simples have FP dimension five. On these four labels, left and right multiplication by h are the same free involution in all fifteen tensors. The K-by-K double orbits therefore have size two and diagonal cyclic stabilizer of order two. Twisted stabilizer representations are all one-dimensional, since H^2(C2,C^*)=0. Each of the two orbits gives two simple A-bimodules. Their underlying dimensions are 2*5=10 and their bimodule dimensions are 10/2=5. This accounts for all objects outside E.

Thus the full Morita dual D=C_(A|A) has type (1^20,5^4). Apply the lemma with p=5. It follows that C is Morita equivalent to a pointed fusion category of FP dimension 120, hence is group-theoretical and unitarizable.

## Exact audit and scope

`verify.py` checks all mandatory first-step statements on every one of the fifteen supplied tensors, including their hashes, exact positive integral dimension characters, the dimension-20 based subring, both full dimension-two stabilizers, the order-two relation, equal free left/right actions on the four dimension-five labels, and the full K-by-K orbit/stabilizer counts. The second step is the uniform lemma above; no unknown associator is replaced by a selected model.

The final implication is **general complex categorification => group-theoretical => unitarizable** for these fifteen rings. Their existence remains unresolved unless a separate model or obstruction is supplied. This strengthens the old record, which did not establish unitarizability for this family.

The internal-Hom and bimodule-dimension facts are the standard module-category FP dimension formulas; see Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Chapters 7 and 9. The special cyclic-stabilizer mechanism also occurs in Etingof--Gelaki--Ostrik, arXiv:math/0304194v2, Lemmas 6.1--6.2. Group-theoretical categories are unitarizable; compare Galindo--Hong--Rowell, arXiv:1105.5048, Theorem 5.20.
