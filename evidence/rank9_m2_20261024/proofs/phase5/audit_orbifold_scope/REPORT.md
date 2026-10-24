# Independent audit: algebraic isotropic orbifold theorem

**Verdict: PASS within the stated scope.** The proof in
`../orbifold_scope/ALGEBRAIC_ORBIFOLD.md` establishes the claimed fusion
category for the specific Radchenko--Wheeler (RW) Leavitt realizations.
Its semisimplicity and rigidity arguments do not assume unitarity, a factor
completion, or existence of isometries splitting the Fourier idempotents.
The concrete order-32 example is a rank-12 auxiliary model with invertible
group C4 x C2. It does not promote any unresolved rank-9 census ring.

## External inputs inspected

RW, arXiv:2609.21892v1, Section 5.3 and Theorem 10 supply actual
endomorphisms, all basic intertwiner spaces, splitting intertwiners for
rho squared, and evaluation/coevaluation maps. Appendix B, Lemma 4,
equation (60) supplies rho(U_h). Proposition 10 supplies the particular
metric datum associated to the chosen SL(2,Z) matrix. These inputs are
stated as proved constructions, not numerical approximations. Their proofs
were inspected at the level needed to identify exactly which assertions
the new argument imports. This audit does not independently reprove the
quantum-dilogarithm existence theorem.

Izumi, arXiv:1512.04288v2, Section 12.1 and Theorem 12.5 provide the
comparison formula. The new argument genuinely proves its algebraic
analogue; it does not silently apply the C*-theorem outside its hypotheses.
RW footnote 7 confirms that RW's bicharacter B is the inverse of Izumi's.

## Crossed-product endomorphisms and the square decomposition

I independently checked the definitions

    R = direct_sum_(h in H) L lambda_h,
    tau(lambda_h) = q(h) U_h lambda_h,
    beta_g(lambda_h) = B(g,h)^(-1) lambda_h.

The multiplication and covariance relations hold. The identities
beta_g tau=tau and tau beta_g=Ad(U_g)tau hold on both L and every lambda_h.
For isotropic H, q restricted to H is a character of order at most two.
Substituting RW equation (60) into

    tau^2(lambda_h) = q(h)^2 rho(U_h) U_h lambda_h

gives exactly the S and T blocks displayed in the author's equation (5).
The S block coefficient is B(g,h)^(-1); the T block coefficient is
q(h)B(g,h). Moving lambda_h past the primed generators gives those same
coefficients on the proposed direct sum. Thus the splitting maps are
intertwiners for all of R, not merely its subalgebra L.

## Complete Hom spaces and semisimplicity

For x=sum_h x_h lambda_h intertwining beta_g and beta_k, the restriction
to L requires x_h in Hom_L(alpha_(g+h),alpha_k). The complete RW Hom
calculation leaves precisely a scalar multiple of lambda_(k-g), and only
when k-g is in H. The remaining lambda_l constraint is satisfied by
isotropy. In particular End_R(id)=C: simplicity of the tensor unit is proved
without asserting that R is a factor or a simple algebra.

For End_R(tau), restriction to L makes every x_h scalar. Each lambda_h
then commutes with tau(lambda_k), again by isotropy, so End_R(tau)=C[H].
The same coefficient argument gives both mixed Hom spaces equal to zero.
These are full Hom calculations in R, not selected spaces of candidate
intertwiners.

The exact square decomposition and the beta/tau relations split every
tensor word into beta objects and tau. Their complete basic Hom spaces
therefore imply that all endomorphism algebras are finite sums of matrix
algebras. The additive Karoubi completion is consequently semisimple with
exactly |G/H|+|H| simple objects. No semisimplicity assertion about the
crossed-product algebra itself is needed, and RW's Leavitt-specific
Proposition 11 is not improperly reapplied to R.

## Rigidity and coherent associators

The beta objects have strict inverses. For tau, equation (5) places S_0
and d S'_0 in the required evaluation and coevaluation Hom spaces over R.
The two snake equations are the existing identities in L because tau|L=rho.
Finite direct sums preserve duals, and the dual idempotent splits in the
Karoubi completion. This proves rigidity of every resulting simple.

Composition in End(R) supplies the strict tensor structure; additive and
Karoubi completion inherit its coherent associator. The proof is therefore
a categorical construction, not an inference from associativity of the
resulting fusion tensor.

## Independent Fourier calculation

Let p_eta=(1/|H|)sum_h eta(h)^(-1)lambda_h and P=p_1 tau(p_1).
Because p_1 commutes with tau(R), P is an idempotent. I recomputed its
action directly, rather than assuming Izumi's projection calculation.

On Hom(beta_r,tau^2), the complete basis is

    v_k = S_(r+k) lambda_k, k in H.

The first Fourier factor averages shifts of k; the second weights those
shifts by q(h)B(h,r)^(-1). The resulting rank is one precisely when
B(-,r)|H=q|H, and zero otherwise. Thus the invertible summands form
(H-perp-g_a)/H with the sign of g_a as in the proposed theorem.

On Hom(sigma_eta,tau^2), the complete basis is w_g=T_g p_eta. Direct
expansion of both Fourier factors gives

    P w_g = 0 unless B(-,g)|H=eta,
    P w_g = (1/|H|)sum_h q(h) w_(g-h) when that equality holds.

The selected indices form an H-perp coset. Each H orbit supports one
rank-one character projector, giving rank |G|/|H|^2 for each eta. This
proves the multiplicity in the claimed square formula without positivity.
The action formulas on sigma_eta agree with the author's signs.

The stated dual is also correct: sigma_eta^*=sigma_(eta q|H), with no
additional inverse on eta. Indeed sigma^*=beta_(-g_a)sigma, and the right
action on the noninvertible orbit reverses the beta index. This directly
gives the displayed character formula. It is particularly relevant when
q|H is nontrivial and the noninvertibles are not self-dual.

## Concrete rank-12 verification

`verify_independent.py` imports no author code. It reduces RW's gamma
formulas independently for gamma=[[1,4],[8,33]], verifies the quadratic and
bicharacter equations, nondegeneracy, isotropy, H-perp and the g_a shift.
It then builds the unsimplified double Fourier projectors with exact
rational arithmetic, checks idempotency, and computes their ranks.

For H=<(4,0),(0,2)> in C8 x C4, the eight invertible block ranks are

    [0,1,0,0,0,1,0,0]

in lexicographic C4 x C2 order. The four noninvertible ranks are [2,2,2,2].
An independently built complete 12x12x12 tensor passes every associativity
equation, both Frobenius reciprocity identities, unit and duality checks,
and FP-dimension equations in Q(sqrt(2)). The noninvertible FP dimension is
4+3sqrt(2), and their duality consists of two transpositions.

The receipt is `independent_verification.json`; its independent tensor
SHA256 is `99a8e9fbf485f046506e7c260012deda9d92b226bb76c364b779fb97fa4bb1f1`.
This equals the author's final tensor hash in `orbifold_verification.json`;
the author's separate standard-library verifier was also replayed and passed.
These finite checks support the new calculation; RW's actual construction
and the preceding categorical proof supply existence and coherence.

## Scope retained

The optional sphericality assertion uses the separate general theorem
for quadratic categories, Liu--Palcoux--Ren arXiv:2010.10264v5 Theorem 2.15,
which cites Thornton IV.3.6. I checked that its stated scope applies to
arbitrary complex quadratic categorifications. Rigidity alone is not used
to infer sphericality. No claim of unitarity follows or is needed here.

The note appropriately leaves unproved any separable algebra structure on
1+sum_eta sigma_eta, any nonunitary analogue of Izumi's Theorem 12.3, and
any claimed Morita dual for that proposed algebra. The auxiliary example
has abelian invertibles, so it does not establish the D8-invertible models
needed by the remaining rank-9 reductions. No census status changes are
justified by this theorem alone.

## Primary sources

- https://arxiv.org/html/2609.21892v1
- https://arxiv.org/pdf/1512.04288v2
- https://arxiv.org/pdf/2010.10264v5

No author proof or code was edited. The author's verifier regenerated its
existing receipt on replay; all independently authored files are in this
audit directory.
