# Independent audit of inversion descent for the C16 near-group orbifold

This audit supplies the two descent identities needed in `R12_INVERSION_DESCENT_CANDIDATE.md`. It also corrects the parent center permutation: it is inversion, not the identity. With that correction, the construction of an involutive tensor autoequivalence of the already constructed R8_1_12 category passes the categorical audit. Identification of the final rank-seven tensor is a separate step.

Let C=NG(C16,16) have Izumi data chi(g,h)=exp(2 pi i 3gh/16), and let H=4C16. Write A=sum(h in H) h for the commutative central algebra, D=C_A, and T for the generator of the canonical dual C4 action on D. The unitary existence input and the orbifold rules are unchanged from the existing R8_1_12 construction.

## 1. The parent self-Morita bimodule and its central permutation

Izumi Theorem 11.3 constructs the self-dual near-group category with alpha'_g=Ad U(-g) restricted to M^alpha and rho'=rho restricted to M^alpha. Its equivalence with the original category retains the labels g. The regular-C16 Morita bimodule has one simple a=kappa fixed by C16 and sixteen free-orbit simples b. The uniqueness of its left-module structure follows from internalEnd(a)=sum(g in C16)g and H²(C16,C*)=0. Consequently the argument of Grossman--Jordan--Snyder, Lemma 4.7 and Remark 4.8, applies without a primality assumption: the square is a regular bimodule with a tensor autoequivalence G on the right.

The commutant of rho kappa is spanned by U(h). The sign in its conjugation formula is important. From Ad U(h) composed with rho = rho composed with alpha_h, one gets

    U(h) rho(U(g)) U(h)* = chi(h,g) rho(U(g)),
    Ad rho(U(g))(U(h)) = chi(h,g)^(-1) U(h).

Thus left alpha_g and right alpha'_g induce opposite permutations on the spectral projections that label b. A central object above g acts on the left in the same way as its Morita image on the right. The free orbit forces its image to lie above -g. Izumi Theorem 13.4 gives a central lift of every invertible, and trivial universal grading makes that lift unique. Therefore the central permutation of this Morita equivalence is exactly g -> -g. It preserves H and its regular central algebra A.

In particular the square fixes all central-invertible labels. Since the parent square is represented by G and Izumi Corollary 13.5 identifies tensor autoequivalences with a subgroup of Aut(C16), faithfully on these labels, G is tensor-isomorphic to Id. This avoids any need to determine the numerical b-symmetries or to compare only the quotient modulo four.

## 2. Central-algebra descent and its composition ambiguity

Use the following central base-change lemma. If M is an invertible C--C bimodule and its Morita center equivalence preserves a commutative separable algebra A in Z(C), choose an algebra isomorphism between the transported A and A. The category of left A-module objects in M is then an invertible C_A--C_A bimodule. The commuting right action is balanced using precisely that chosen isomorphism. Central base change commutes with relative tensor product, with the algebra identifications composed in the same order.

One can check this lemma directly from the universal properties: the two sides of the comparison

    (M tensor_C N)_A  =  M_A tensor_(C_A) N_A

classify the same balanced functors with the same compatible A-action. The central structure moves the A-action across the balancing variable; separability splits the relevant coequalizers. The comparison respects left and right actions and their associators. Applying the construction to an inverse bimodule shows invertibility. An equivalence of parent bimodules descends when its A-identifications agree. If they do not, their difference is an algebra automorphism of A, and this twists one descendant action by the corresponding canonical dual autoequivalence.

Here Aut_alg(A)=Hom(H,C*)=C4: each automorphism acts by a scalar on each distinct central summand h, and preservation of multiplication makes the scalars a character. These are exactly the four powers T^j. The central action g -> -g permutes H, but it still preserves A as an algebra. The composite of two chosen identifications is an identification on the parent square; since that square is regular, its discrepancy from the identity is just one such character. Therefore, for the descended bimodule L,

    L tensor_D L = D_(T^j)

for some j modulo four. This statement is in the bimodule category. When L is identified with a tensor autoequivalence F using a chosen regular-module generator, it says

    F² = Inn(v) composed with T^j

for an invertible v of D. Keeping this inner ambiguity is necessary.

## 3. Regularity and the inversion sign

The a object has four distinct A-module structures, since H²(H,C*)=0; denote them a_lambda. The sixteen free b objects give four induced simple A-modules. Each has dimension t=2+sqrt(5), while each a_lambda has normalized dimension one. The left D-invertibles permute the a_lambda freely, and the four noninvertibles take a_lambda bijectively to the four b-modules. For the latter assertion, use rho a=sum(b_g): after descent Q(rho) is the sum of all four D-noninvertibles, and the right side is the sum of the four induced b-modules, once each. All four summands of Q(rho) act nontrivially, so they give precisely that bijection. Thus (-) tensor a_lambda is a left-module equivalence D -> L; L corresponds to an actual tensor autoequivalence F.

The following calculation fixes left-versus-right conventions. Treat lambda_h as the scalar left A-action alpha_h kappa -> kappa. The half-braiding of h with alpha_g is chi(h,g), from the natural isomorphism in Izumi Theorem 13.4. Consequently left alpha_g changes lambda_h to chi(h,g)lambda_h. On the right, kappa alpha'_g=Ad U(-g) kappa is identified with kappa by U(g). Transport of the left A-action gives

    U(g) lambda_h alpha_h(U(g)*) = chi(h,g)^(-1) lambda_h.

The right action on left A-modules is the extension of the original right C-module functor, so this calculation is unaffected by whether the chosen identification of the two H algebras permutes h by inversion. Its balancing only supplies the extension from C to C_A. It follows that F(r)=r^(-1). As a based automorphism it sends rho to r^k rho. Changing the A-identification by a character composes with a power of T; since T fixes r and cycles the four noninvertibles, choose it so that F(rho)=r rho.

For this choice F² fixes every simple label, but that fact alone does not yet make F² tensor-isomorphic to Id.

## 4. Monodromy computes T² and removes the inner ambiguity

For a central invertible p in C, the central crossing p tensor M -> M tensor p descends to A-modules with a possible twist of their A-action. Its defect is the monodromy of p with the summands of A: the two ways of moving h past p differ by c_(p,h)c_(h,p). If this scalar is the character lambda(h), the crossing gives a natural monoidal identification

    Inn(Q(p)) = T_lambda

up to replacing lambda by its inverse according to the left/right-module convention. This identity follows by checking A-linearity on each summand h; the tensor compatibility is the half-braiding axiom. It is therefore stronger than equality on simple labels.

For p=1 in the additive C16 labeling (the generator, not the tensor unit), the defect is chi(1,h)^2. On h=4 this is -1. Hence it is the order-two character, and there is no inverse-convention ambiguity:

    T² = Inn(r).

For p=2 the defect is trivial on H. Its central crossing is A-linear, so Q(p)=r² has a central lift in D and Inn(r²)=Id as a tensor autoequivalence.

Now write v=r^ell. On noninvertible labels Inn(r^ell) shifts by 2ell, whereas T^j shifts by j. Since F² fixes all simple labels, 2ell+j=0 modulo four. In particular j is even. Using T²=Inn(r),

    F² = Inn(r^(ell+j/2)).

The exponent ell+j/2 is even, so this is tensor-isomorphic to Id by the central lift of r².

Finally D has trivial universal grading: rho² contains rho and every r^j rho, which forces all simple degrees to be trivial. Thus Aut_tensor(Id_D)=1. The two coherence composites for an isomorphism F² -> Id differ by a tensor automorphism of F, and therefore agree. This supplies a coherent C2 action, not merely an order-two permutation or outer class. All operations can be made unitary because the parent category, separable algebras, and original Morita equivalence are unitary.

## Sources and scope

The near-group fixed-point formulas, self-duality, inner-triviality, and faithful automorphism action were checked in Izumi, arXiv:1512.04288v2, Theorems 11.3 and 13.4, Corollary 13.5; local text `izumi_near.txt`. Remark 12.4 independently records self-duality of the orbifold subfactor. The parent-square argument was checked in Grossman--Jordan--Snyder, arXiv:1211.6414v2, Lemma 4.7 and Remark 4.8. The extra central compatibility and its behavior under relative tensor products are the structures formalized in *Extension Theory for Braided-Enriched Fusion Categories*, Section 4.1, Definition 4.3; the concrete central-algebra base-change and monodromy proofs are given above.

This audit establishes the unitary crossed product D semidirect_F C2 with F(r)=r^-1 and F(rho)=r rho. The choice of its reflection algebra and identification of its rank-seven Morita-dual tensor still require their own exact calculation. No rank-seven existence entry is asserted by this file alone.
