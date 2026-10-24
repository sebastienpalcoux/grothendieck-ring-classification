# Algebraic isotropic orbifolds of the Radchenko–Wheeler realization

This note proves an algebraic version of the fusion-rule construction in
Izumi, arXiv:1512.04288, Theorem 12.5, for the **specific Leavitt-algebra
realizations constructed by Radchenko–Wheeler (RW)**, arXiv:2609.21892v1,
section 5.3. It does not classify arbitrary spherical near-group categories,
assert their unitarity, or extend an analytic reconstruction theorem by fiat.
No census ring is promoted by this note alone.

## 1. Inputs and conventions

Let G be a finite abelian group of order N, with nondegenerate symmetric
bicharacter B and even quadratic refinement q:

    q(g+h)=q(g)q(h)B(g,h),  q(-g)=q(g),  q(0)=1.

These are RW's pairing and Gaussian. Izumi's pairing is B inverse; RW
footnote 7 states this convention change explicitly. Assume a finite quantum
dilogarithm for these data, so RW Theorem 10 supplies the following actual
endomorphisms of the Leavitt algebra L=L_(2N), not merely scalar equations.
The algebra has generators S_g,T_g,S'_g,T'_g with

    S'_g S_k=T'_g T_k=delta_(g,k),
    S'_g T_k=T'_g S_k=0,
    sum_g(S_g S'_g+T_g T'_g)=1.

RW supplies alpha_g, rho and U_g in L, satisfying

    alpha_g(S_k)=S_(g+k),   alpha_g(T_k)=B(g,k)^(-1)T_k,
    U_g=sum_k B(g,k)^(-1)S_k S'_k + sum_k T_(k-g)T'_k,
    U_g U_k=U_(g+k),        alpha_g(U_k)=B(g,k)U_k,
    alpha_g rho=rho,        rho alpha_g=Ad(U_g)rho,
    rho^2(x)=sum_g S_g alpha_g(x)S'_g + sum_g T_g rho(x)T'_g.

The primed generators transform with inverse factors. The complete basic
intertwiner spaces, proved in RW section 5.3, are

    Hom_L(alpha_g,alpha_k)=C if g=k, otherwise 0;
    End_L(rho)=C;  Hom_L(alpha_g,rho)=Hom_L(rho,alpha_g)=0.

RW Lemma 4, equation (60), additionally gives

    rho(U_h)=sum_g S_(g-h)S'_g
             +sum_g q(g+h)/q(g) T_(g+h)U_h T'_g.                 (1)

There is a nonzero d with d^2=N(d+1). The self-duality maps for rho are
b=S_0 and e=d S'_0, and the two snake identities hold in L.
These assertions, including the complete Hom calculations, are the precise
external reconstruction dependencies used here.

Let H be a subgroup isotropic for B, meaning B(h,k)=1 for h,k in H.
Write m=|H|. Its orthogonal complement has order N/m and contains H;
in particular m^2 divides N. The restriction q|H is a character with values
in {1,-1}. Choose g_a in G such that

    q(h)=B(h,g_a)^(-1) for h in H.                             (2)

Such a choice exists by nondegeneracy. Only its class modulo H-perp matters;
we need 2g_a in H-perp, not a lift of order two in G.

## 2. The crossed-product endomorphisms

Form the ordinary algebraic crossed product

    R=L rtimes_alpha H = direct_sum_(h in H) L lambda_h,
    lambda_h x=alpha_h(x)lambda_h,  lambda_h lambda_k=lambda_(h+k).

The displayed vector-space direct sum is part of the construction. Thus all
intertwiner calculations below can be compared coefficient by coefficient.
Define unital endomorphisms of R by

    beta_g|L=alpha_g,     beta_g(lambda_h)=B(g,h)^(-1)lambda_h,
    tau|L=rho,           tau(lambda_h)=q(h)U_h lambda_h.         (3)

For tau, the product of the images of lambda_h and lambda_k is
q(h)q(k)B(h,k)U_(h+k)lambda_(h+k), as required. Covariance follows from
alpha_h rho=rho and rho alpha_h=Ad(U_h)rho. The same check for beta is
immediate from the bicharacter identities. These checks prove existence
as algebra homomorphisms; no analytic completion or involution is used.

Direct substitution gives

    beta_g beta_k=beta_(g+k),  beta_g tau=tau,
    tau beta_g=Ad(U_g)tau.                                   (4)

The crucial fusion decomposition holds on **all of R**:

    tau^2(x)=sum_g S_g beta_g(x)S'_g + sum_g T_g tau(x)T'_g.    (5)

It holds on L by RW. For lambda_h, the left side is
q(h)^2 rho(U_h)U_h lambda_h. By (1), q(h)^2=1, and the Leavitt relations,
its S block is

    sum_g B(g,h)^(-1) S_g S'_(g+h) lambda_h,

and its T block is

    sum_g q(h)B(g,h) T_g U_h T'_g lambda_h.

These are exactly the two blocks of the right side of (5), after moving
lambda_h across S'_g and T'_g. Checking L and the lambda_h proves (5),
because both sides define unital homomorphisms. In particular S_g,S'_g
and T_g,T'_g are splitting intertwiners in End(R).

## 3. Complete basic Hom spaces and fusion-category existence

Use the endomorphism category with
Hom(a,b)={x in R: x a(y)=b(y)x for all y in R}.

For x=sum_h x_h lambda_h in Hom(beta_g,beta_k), comparing on L gives
x_h in Hom_L(alpha_(g+h),alpha_k). Therefore x is zero unless k-g lies
in H; in that case it is a scalar multiple of lambda_(k-g). Checking on
lambda_l introduces B(k-g,l), which is one by isotropy. Hence

    Hom_R(beta_g,beta_k)=C lambda_(k-g) if k-g in H, else 0.   (6)

The beta's are simple invertibles, with distinct classes G/H. In particular
the tensor unit has endomorphism algebra C.

For x in End_R(tau), comparison on L and alpha_h rho=rho forces every
x_h to be scalar. Every lambda_h commutes with tau(lambda_k), because
alpha_h(U_k)=B(h,k)U_k=U_k. Consequently

    End_R(tau)=C[H].                                        (7)

The mixed Hom spaces between beta_g and tau are zero: their coefficients
would lie in one of the vanishing mixed Hom_L spaces listed above.

For eta in the character group H-hat set

    p_eta=(1/m) sum_h eta(h)^(-1)lambda_h,
    sigma_eta=(p_eta,tau)

in the Karoubi completion. These are precisely the m distinct simple
summands of tau, by (7). No isometry with range p_eta is needed.

Take the full monoidal subcategory generated by beta_g and tau, then its
additive Karoubi completion. Equations (4) and (5) decompose every tensor
word into copies of beta's and tau. Equations (6), (7), and the mixed-space
calculation then prove finite-dimensional Hom spaces and semisimplicity,
with exactly N/m+m simple objects. This direct argument does not apply a
Leavitt-specific semisimplicity proposition to the different algebra R.

The beta's have strict inverses. For tau, (5) makes S_0 and d S'_0
intertwiners 1 to tau^2 and tau^2 to 1. Their snake identities hold because
tau agrees with rho on L. Thus the generating category is rigid; finite
direct sums and idempotent summands of rigid objects remain rigid in its
additive Karoubi completion. We have therefore constructed an actual
complex fusion category D, independently of unitarity.

The action is transitive on its noninvertible simples. Thus D is a quadratic
(generalized near-group) category. The general sphericality theorem for
quadratic categories applies: Thornton, dissertation, Theorem IV.3.6,
as stated and applied in Liu–Palcoux–Ren, arXiv:2010.10264v5, Theorem 2.15.
This is a separate sphericality dependency, not an inference that rigidity
alone is sphericality. The construction of D as a fusion category above
does not need it.

## 4. Fusion rules from finite Fourier projections

Write B_g for the character h -> B(g,h). Applying beta_g to p_eta gives
p_(eta B_g), and transporting by U_g gives
U_g^(-1)p_eta U_g=p_(eta B_g^(-1)). Therefore

    beta_g sigma_eta=sigma_(eta B_g),
    sigma_eta beta_g=sigma_(eta B_g^(-1)).                    (8)

Let sigma=sigma_1. Its square is the summand of tau^2 cut out by

    P=p_1 tau(p_1).

The two factors commute: p_1 lies in End(tau), so it commutes with tau(R).
Both are idempotents; hence P is an idempotent.

For a fixed class r in G/H, Hom(beta_r,tau^2) has basis

    v_k=S_(r+k)lambda_k,  k in H.

Here (5) and (6) prove completeness of the basis. Left multiplication by
p_1 averages the shifts k -> k+t. Left multiplication by tau(p_1) averages
the same shifts with weights q(t)B(t,r)^(-1). The product P therefore has
rank one precisely when B(t,r)=q(t) for every t in H, and zero otherwise.
By (2), the rank-one classes are r in (H-perp-g_a)/H.

For a fixed eta, Hom(sigma_eta,tau^2) has the complete basis

    w_g=T_g p_eta,  g in G.

The coefficient calculation gives

    P w_g=0                              if B_g != eta,
    P w_g=(1/m)sum_(h in H) q(h)w_(g-h)   if B_g=eta.         (9)

Indeed lambda_h T_g=B(h,g)^(-1)T_g lambda_h and U_h T_g=T_(g-h).
The p_1 factor selects B_g=eta; on that subspace the eta(h) from lambda_h
cancels B(h,g)^(-1). The selected indices form a coset of H-perp, of size
N/m. Each H-orbit in it supports one copy of the q-weighted averaging
idempotent, of rank one. Hence (9) has rank N/m^2 for every eta.

Combining these two block calculations proves exactly

    sigma^2 = sum_(k in H-perp/H) beta_(k-g_a)
               + (N/m^2) sum_(g in G/H-perp) beta_g sigma,
    beta_g sigma=sigma beta_(-g).                            (10)

These are Izumi's Theorem 12.5 fusion rules in RW conventions. They are
proved here for the algebraic realization rather than imported from the
unitary theorem. Every simple noninvertible has FP dimension delta/m,
where delta is the positive root of delta^2=N(delta+1). In particular

    FPdim(D)=(N+delta^2)/m.

The dual of sigma_eta is sigma_(eta q|H); consequently the noninvertibles
are all self-dual if q|H=1, and none is self-dual if q|H is nontrivial.

## 5. A concrete order-32 source and its limited application

RW Proposition 10 applies to gamma=[[1,4],[8,33]], determinant one and
trace 34. Its row-lattice quotient is C8 x C4. The formulas of RW section
4.3 reduce, with coordinates (x,y) modulo (8,4), to

    B((x,y),(z,w))=exp(2 pi i(-xz/8+yw/4)),
    q(x,y)=(-1)^(x+y) exp(pi i(-x^2/8+y^2/4)).

For example omega((x,y)gamma,(x,y))/32 is
-x^2/8-xy+y^2/4; the (-1)^(xy) factor in RW's q cancels the middle term.
Thus Proposition 10 supplies the required quantum dilogarithm for this
specific metric datum, not just some metric on the abstract group.

Take H=<(4,0),(0,2)>, with H-perp the pairs with both coordinates even.
Then G/H=C4 x C2, H-hat=V4, N/m^2=2, and q|H is nontrivial on (0,2).
We can choose g_a=(0,1). Formula (10) constructs a rank-twelve category
with eight invertibles C4 x C2 and four non-self-dual noninvertibles of
dimension 4+3 sqrt(2). This is a genuine model for its displayed tensor.

It is **not** one of the D8-invertible rank-twelve candidates forced by the
remaining rank-nine Morita reductions. In particular this construction
does not solve R9_2_1975 or any of the three remaining commutative quadratic
rank-nine cases. It neither excludes them nor proves that other models do
not exist. The companion verifier checks the finite metric and Fourier
calculations and all fusion-tensor axioms for this concrete example; it does
not replace RW's quantum-dilogarithm or Leavitt reconstruction proofs.

## 6. The canonical nonintegral-algebra proposal

The object A=1+sum_eta sigma_eta has the dimension of the canonical
orbifold subfactor algebra in Izumi Theorem 12.3. That theorem uses a
unitary Q-system and a crossed-product subfactor. Its Remark 12.4 explicitly
says the resulting subfactor is self-dual. Thus, in that established
setting, this particular algebra returns an equivalent even part rather
than producing a new D8-invertible model.

The present proof establishes the algebraic orbifold category and its
fusion rules, **not** a separable algebra structure on A, a categorical
extension of Theorem 12.3, or a formula for its Morita dual outside the
unitary setting. Those require their own algebra and module data. Nor does
a nonnegative induction Gram factorization by itself establish an algebra.
The peer calculation in ../quadratic_noncomm/order32_canonical_algebra_probe.json
finds rank twelve for that conditional module problem, not a rank-nine
model. It remains useful as a constraint, not a categorification.

Other nonintegral algebras or other source metrics are not ruled out.
Failure of this particular route is not a general exclusion criterion.

## Sources

* D. Radchenko and C. Wheeler, *Real quadratic fields and finite quantum
  dilogarithms I*, arXiv:2609.21892v1: Proposition 10; section 5.3, Theorem 10;
  Appendix B, Lemma 4. https://arxiv.org/pdf/2609.21892v1
* M. Izumi, *A Cuntz algebra approach to the classification of near-group
  categories*, arXiv:1512.04288v2: section 12.1, Theorems 12.3, 12.5 and
  Remarks 12.4, 12.6. https://arxiv.org/pdf/1512.04288v2
* Z. Liu, S. Palcoux and Y. Ren, *Classification of Grothendieck rings of
  complex fusion categories of multiplicity one up to rank six*,
  arXiv:2010.10264v5, Theorem 2.15 (quadratic-category sphericality, citing
  Thornton Theorem IV.3.6). https://arxiv.org/pdf/2010.10264v5
* H. He, Z. Liu, S. Lu, S. Palcoux and Y. Ren, arXiv:2610.11652v1:
  Theorem 5.4 and Corollary 6.6 separately provide spherical and
  pseudo-unitary cyclic near-group constructions. They do not assert
  general unitarity and are not needed for the crossed-product proof.
  https://arxiv.org/pdf/2610.11652v1

