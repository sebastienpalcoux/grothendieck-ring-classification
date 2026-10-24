# Independent audit of the twisted GH(C6,2) precursor

## Verdict

The construction in `../quadratic8/TWISTED_GH6_CONSTRUCTION.md` gives an actual complex fusion category with rules

    g^6=1,   g sigma=sigma g^(-1),
    sigma^2=1+2 sum_(j=0)^5 g^j sigma,

and pointed associator class 3 in H^3(C6,C*)=Z/6. Its existence does not require unitarity. The input is the specific Leavitt-algebra realization of Radchenko--Wheeler, rather than a presumed parameterization of every spherical category.

The connected separable algebra 1+sigma is still not constructed. Accordingly this is not a categorification of R8_3_1768.

## Checks of the input and crossed product

For gamma=[[145,12],[12,1]], determinant is one and trace is 146. The row lattice of gamma−1 has Smith invariants 12,12. RW's formulas give

    B((x,y),(a,b))=exp(2pi i(yb−xa)/12),
    q(x,y)=(-1)^(x+y)exp(2pi i(y²−x²)/24).

The mixed xy factor in RW's Gaussian cancels its sign factor. Thus the required metric datum is established, not just the abstract group C12².

On H={h(x,t)=(x,x+6t)}, omega(h(x,t),h(a,s))=(-1)^(ta) is a normalized cocycle. Its commutator is B|H=(-1)^(xs+at); this bicharacter has radical K={h(2z,0)}. Also q(h(x,t))=(-1)^(xt+t), so q(h)^2=1 on all H and q|K=1.

These identities justify all three categorical points which would fail for an arbitrary twisted subgroup:

1. The extension tau(lambda_h)=q(h)U_h lambda_h respects the twisted product, because q(h+k)=q(h)q(k)B(h,k).
2. beta_h=Ad(lambda_h) and every lambda_h belongs to End(tau), because B|H is real and equals the commutator of omega.
3. The original S_g,T_g splitting of tau² remains valid on the extra generators lambda_h, because q(h)^2=1. The proof on the Leavitt subalgebra alone would not have sufficed.

Comparison in the direct sum R=⊕_h A lambda_h gives the complete basic Hom spaces claimed in the construction. End(tau)=C^omega[H] is a direct sum of six M2 blocks. The primitive projectors in that note select all six simple noninvertibles, and the direct rank computations give the stated product, including multiplicity two. The original evaluation maps remain valid on R, proving rigidity before taking idempotent summands.

Finally beta=beta_(1,0) has beta^6=Ad(lambda_(6,0)) and beta(lambda_(6,0))=−lambda_(6,0). This is exactly cyclic class 3, independent of replacing the generator by its inverse.

## An independent tensor-quotient check

Let L={h(x,0)} be the diagonal order-twelve subgroup and let R0=A⋊L. It is isotropic, L=L-perp, and q|L=1. The previous algebraic orbifold theorem therefore constructs GH(C12,1) on R0.

The inclusion R0→R induces a tensor functor on the generated categories. This is not automatic for arbitrary endomorphisms of an algebra inclusion: here all the old splitting intertwiners S_g,T_g and all lambda_l (l in L) remain intertwiners for the extended endomorphisms. The complete old basic Hom lists and the decompositions of tensor words then show the same for every old morphism. Composition and tensor products agree under the algebra inclusion. Idempotent completion extends the functor.

The old primitive projector p=(1/12)Σ_l lambda_(l,l) stays primitive in C^omega[H], so its simple noninvertible maps to the simple sigma. Its old square rule is

    sigma_old²=1+sum_(j in C12) beta_j sigma_old.

The quotient identifies beta_(j+6) with beta_j and pairs the noninvertible translates. Applying the tensor functor proves sigma²=1+2Σ_(j in C6) beta_j sigma, and preserves self-duality. This independently verifies the most important fusion-rule claim.

## Why the canonical near-group algebra gives no shortcut

There is an algebraic construction of the canonical algebra 1+rho in the original near-group category. Let A_G=⊕_g alpha_g be the regular pointed algebra and regard rho as a left A_G-module using the strict identities alpha_g rho=rho. Its internal end is a connected separable algebra of dimension dim(rho)²/|G|=1+dim(rho). Since rho is the unique noninvertible and its dimension is irrational, the underlying object is 1+rho.

Let F be the twisted orbifold tensor functor. It preserves this internal-end construction, relative tensor products, and separability. The image has underlying object

    F(1+rho)=1+2Σ_j sigma_j=sigma².

In this particular construction it is the matrix algebra End(sigma) **as an algebra**, not merely an object of the same dimension. Here is the categorical reason. The unit component of F(A_G) is C^omega[H]. Choose its primitive idempotent p given by the diagonal average. The action of each nontrivial quotient invertible beta_r moves the central K-character of p to a different character. Therefore the corner p F(A_G) p has no nontrivial homogeneous component; its unit component is pC^omega[H]p=C. Hence this corner algebra is the tensor unit. The idempotent is full: the quotient invertibles move its central block transitively, and the twisted group algebra supplies both matrix entries within each block.

Full-corner Morita equivalence sends F(rho)=tau to p tau=sigma. It therefore sends its internal end F(1+rho) to the ordinary internal end of sigma, proving the asserted algebra identification. Its Morita dual is the GH(C6,2) category itself.

This agrees with the independent comparison of the two old rank-eight based-module completions: their small-object internal ends are 1+beta_(2j)sigma; their large-object internal ends contain three pointed summands and noninvertible total multiplicity 33. Neither equals 1+2Σ sigma_j. That comparison is a check on the old module candidates, not the basis of the full-corner proof.

## The remaining algebra equation is explicit and finite

Write Z=lambda_(0,6), p=(1/12)Σ_l lambda_(l,l), and use primed Leavitt generators as algebraic duals; no adjoint or complex conjugation is implied below. Put

    r=(1/sqrt(12)) sum_l S_(l,l) lambda_(l,l),
    s=(1/sqrt(12)) sum_l lambda_(-l,-l) S'_(l,l),
    t0=(1/sqrt(12)) sum_l T_(l,l) p,
    t1=(1/sqrt(12)) sum_l T_(l,l+6) Z p,
    t0'=(1/sqrt(12)) sum_l p T'_(l,l),
    t1'=(1/sqrt(12)) sum_l p Z T'_(l,l+6).

All indices are modulo twelve. The direct projector calculation gives r∈Hom(1,sigma²), s∈Hom(sigma²,1), and ti∈Hom(sigma,sigma²), ti'∈Hom(sigma²,sigma). Leavitt cancellation gives sr=1 and ti'tj=delta_ij p. Thus t0',t1' form a basis of the two-dimensional multiplication space.

For a connected separable algebra 1+sigma, the product sigma²→1 is nonzero. Rescaling the sigma summand lets us normalize it to s. Write its other product component as

    t=b0 t0'+b1 t1'.

The unit equations fix every other product. Associativity is now exactly the following two morphism equations:

    s (t tensor 1_sigma) = s (1_sigma tensor t),
    (s tensor 1_sigma)+t(t tensor 1_sigma)
      = (1_sigma tensor s)+t(1_sigma tensor t).

The first is an equality in Hom(sigma³,1), of dimension two; the second is in Hom(sigma³,sigma), of dimension twenty-five. Thus the last existence problem is a finite linear/quadratic system in b0,b1, with coefficients obtained from the displayed finite averages and RW's explicit rho(S_g),rho(T_g),rho(S'_g),rho(T'_g) formulas. Associative solutions must additionally be checked for separability; no positivity assumption supplies it here.

In the strict endomorphism realization, with P3=p tau(p) tau²(p), these can also be evaluated as

    s t tau²(p)=s tau(t),
    p s+t² tau²(p)=p tau(s)+t tau(t),

with the displayed source and target corners understood. This gives a direct algebraic verification target, rather than a search over arbitrary associators. Its coefficients depend on the actual RW finite quantum dilogarithm; the bicharacter and Gaussian alone do not determine all of them. No evaluation or identity proving a solution to this system is claimed in this audit.

Conjugation by g moves sigma_j to sigma_(j+2). Consequently the six possible objects 1+sigma_j fall into at most two inner-equivalence classes. If the p0 equation fails, p1 must still be tested before excluding this entire construction route.

The special matrix gamma is [[12,1],[1,0]]², with determinant-minus-one square root. This may supply extra identities for the actual RW solution, but no implication from this observation to the multiplication equations has been proved.

## Primary references

* Radchenko--Wheeler, *Real quadratic fields and finite quantum dilogarithms I*, arXiv:2609.21892v1, Proposition 10 and §5.3, Theorem 10; https://arxiv.org/pdf/2609.21892v1.
* Izumi, *A Cuntz algebra approach to the classification of near-group categories*, arXiv:1512.04288v2, §12.2, Lemma 12.16 and Theorem 12.17; https://arxiv.org/pdf/1512.04288v2. Those statements concern the unitary nondegenerate special case; the actual degenerate algebraic construction is proved above and in the companion note.
* Grossman--Izumi, *Drinfeld centers of fusion categories arising from generalized Haagerup subfactors*, equation (2.21), https://arxiv.org/pdf/1501.07679. The explicit extra Q-system condition is a useful scope check; it is not imported as an existence theorem for the present category.
