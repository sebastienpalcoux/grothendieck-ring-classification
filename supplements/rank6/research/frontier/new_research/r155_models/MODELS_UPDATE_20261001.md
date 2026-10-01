# R155: new near-group existence and a pointed-condensation obstruction

Research date: 1 October 2026. Frozen release was read but not modified.
No construction or nonexistence proof of R155 is obtained here.

**Audited upgrade:** the algebraic scope gap discussed in Section 3 below was subsequently closed by the independent proof in `../r155_categorical/rw_small_algebra_obstruction.md`, audited by this agent. Thus none of the three new order-32 Radchenko-Wheeler centers admits ANY connected etale algebra of FP dimension eight. This excludes all direct condensations of those centers to the required R155 center dimension, without a unitarity assumption.

## 1. A material literature update

D. Radchenko and C. Wheeler, *Real quadratic fields and finite quantum dilogarithms I*, arXiv:2609.21892v2, 29 September 2026, Theorem 12 and Corollary 6, p. 27, constructs complex near-group categories of type `(G,|G|)` for every product of two cyclic groups. This includes `(C32,32)`, `(C2 x C16,32)`, and `(C4 x C8,32)`. These are actual categorification assertions, not potential modular data. Unitarity is not established: Section 6 explicitly lists the relation between real and unitary solutions as an open problem.

Source: https://arxiv.org/pdf/2609.21892
Local PDF and extracted text: `radchenko_wheeler_2609_21892.{pdf,txt}`.

For all three categories the noninvertible FP dimension is `rho=16+12 sqrt(2)=4d` and the global FP dimension is `8D`. Thus the prior statement that no actual near-group construction of the dimension type `(32,32)` was found is now obsolete. This does not construct R155.

Y. Meng and Z. Yu, *Classification of some Z/2Z x Z/2Z-quadratic fusion categories of rank 6*, arXiv:2608.06064v1, Theorem 1.1, lists R'(4) as its last surviving ring. Theorem 4.8 retains parameters 0,2,4. Section 5 constructs R'(0) and R'(2); Corollary 5.8's near-group de-equivariantization is R'(2), with field Q(sqrt(6)), not R'(4). Its conjecture concerns completeness of candidate fusion rules and does not assert categorification of every candidate.

Source: https://arxiv.org/pdf/2608.06064
Local PDF and extracted text: `meng_yu_2608_06064.{pdf,txt}`.

## 2. An exact obstruction covering all three newly constructed groups

Let G be C32, C2 x C16, or C4 x C8. Let chi be ANY nondegenerate symmetric bicharacter on G, and let q(g)=chi(g,g). There are exactly four elements g with q(g)=1. Therefore no subgroup of order eight is isotropic for q.

This statement is purely group-theoretic and does not rely on a categorification, unitarity, or a numerical calculation. Write e(t)=exp(2 pi i t).

* On C32, chi(x,y)=e(a xy/32) with a odd. Thus q(x)=1 iff x is a multiple of eight: four elements.
* On C2 x C16 every symmetric bicharacter has
  `q(x,y)=e(A x^2/2 + B y^2/16 + Cxy)`, with A modulo 2, B modulo 16, C modulo 2. Nondegeneracy forces B odd: otherwise `(0,8)` is radical. It then forces A odd: if A=0, `(1,8C)` is radical. The equation `8 A x^2+B y^2=0 mod 16` has no solution with x=1 (squares mod 16 are 0,1,4,9), and with x=0 it forces y divisible by four. Again there are four bosons.
* On C4 x C8 every symmetric bicharacter has
  `q(x,y)=e(A x^2/4 + B y^2/8 + Cxy/2)`, with A,C modulo 4 and B modulo 8. Nondegeneracy forces B odd (otherwise `(0,4)` is radical). It forces A odd as well: if A is even and C is even, `(2,0)` is radical; if A is even and C is odd, `(2,4)` is radical. For q=1, reduction modulo 2 first forces y even. Write y=2z. Then `2 A x^2+4 B z^2=0 mod 8`. If x is odd the first summand is 2 or 6 mod 8, impossible after adding 0 or 4. Hence x is even, and z must be even. The bosons are exactly `(x,y) in {0,2} x {0,4}=G[2]`.

Replacing chi by its inverse or a Galois conjugate does not change this conclusion.

An independent exact enumeration of all bicharacters is in `verify_order32_bosons.py`, with certificate `bicharacter_order32_certificate.json`. It checks respectively 16,16,32 nondegenerate forms. Every one has exactly four bosons. Runtime is below one second, using integer arithmetic only.

## 3. Application and the scope that still needs care

For standard Izumi near-group centers the invertible objects are `a_g`, g in G, and their twists are `chi(g,g)`. The remaining dimensions are rho, rho+1, rho+2. See E. Rowell, H. Solomon, Q. Zhang, *On near-group centers and super-modular categories*, arXiv:2305.09108v2, Section 2.3, equations (2.9)-(2.10), pp. 6-7.

Source: https://arxiv.org/pdf/2305.09108
Local PDF and extracted text: `rowell_solomon_zhang_2305_09108.{pdf,txt}`.

In that setting, condensation from dimension `(8D)^2` to dimension `D^2` requires a connected etale algebra of FP dimension 8. Since rho>8, all its constituents must be invertible. A connected etale algebra in a pointed braided category is supported, multiplicity one, on an isotropic subgroup. The four-boson result therefore rules out every such direct condensation, not merely de-equivariantization by a preselected H=2G.

However, the standard source is written for C*-Izumi categories, whereas the new Radchenko-Wheeler construction is algebraic and explicitly nonunitary. One should either verify the algebraic extension of the relevant half-braiding formulas or state the conclusion with its structural hypotheses. It is not justified to silently assume unitarity of the new examples.

There is a short algebraic route to the required twist formula. In Radchenko-Wheeler Section 5.4,
`alpha_g rho=rho`, `rho alpha_g=Ad(U_g)rho`, and `alpha_g(U_h)=chi(g,h) U_h`.
Any half-braiding on alpha_g has `c_(g,rho)=lambda_g U_g`. Naturality with `U_h:rho -> rho alpha_h`, together with the hexagon, forces
`c_(g,alpha_h)=chi(g,h)^(-1)`.
Thus its self-braiding is the inverse of the same nondegenerate bicharacter on the diagonal. The scalar lambda_g cancels. What this local calculation does not by itself prove is existence of every central lift alpha_g.

An alternate way to avoid a full center calculation, once all invertibles lift, is the low-dimension argument communicated by the root agent: if a center simple Z of dimension at most 8 forgets to an object containing rho, its dimension is at least rho>8, impossible. Otherwise it forgets to a pointed object. Tensor by a lift of an invertible constituent to obtain a simple appearing in I(1). The formal-codegree constituents of I(1), other than the unit, have dimensions `rho+1` and `rho+2`, again >8. Hence Z is invertible. This gives the needed conclusion without asserting full modular data.

For existing half-braiding literature, M. Izumi, *A Cuntz algebra approach to the classification of near-group categories*, arXiv:1512.04288v2, Section 12.2, p.115, explicitly recalls that every alpha_h has a unique half-braiding, citing [32, Lemma 6.1]. Its stated scope remains C* categories.

## 4. Remaining paths

The `(8,16)` type is not constructed by Radchenko-Wheeler's `m=|G|` theorem. Izumi's Section 10 treats `m=2|G|` via equations, excludes the groups of orders 2 and 4, and explicitly identifies abelian groups of order eight as the first tests for its Case III (p.89). No present source located here resolves the C4 x C2 case.

The four-boson proof only covers the three abelian groups of order 32 generated by at most two elements. Other order-32 groups are not excluded by it. It also does not exclude constructions that first tensor with another category, change the center through a different operation, or use intermediate categories of a different dimension. Nor does it exclude R155 directly.

Useful source reference IDs for retrieval in the parent turn: Radchenko-Wheeler PDF `turn392view1` (Theorem12/Cor6 `turn396view1` or `turn417view0`); Meng-Yu author manuscript mirror `turn404view0`; Rowell-Solomon-Zhang `turn411view0`/`turn415view0`; Izumi `turn424view0`, order-eight open test at `turn427view1`, half-braiding recall `turn429view1`. The arXiv direct Meng-Yu PDF downloaded successfully via urllib despite browser fetch errors.


## 5. Audit of the algebraic upgrade

The proof in `../r155_categorical/rw_small_algebra_obstruction.md` avoids assuming that all group elements lift centrally. Its essential lemma is sound: if a central object has multiplicity-free pointed underlying object, its half-braiding matrix M with rho is monomial. Naturality at U_h forces a nonzero matrix entry in column g of row k to satisfy `a(k,h)=chi(g,h)^(-1)` for every h; bicharacter nondegeneracy gives at most one such column per row. Invertibility gives a permutation pi.

The hexagon makes the half-braiding with rho^2 send tagged group label g to pi^2(g). Naturality at a split inclusion T:rho -> rho^2 instead compares it with a nonzero map into the tagged output label pi(g). Both maps are nonzero (split inclusions composed with isomorphisms), so pi^2(g)=pi(g), hence pi=id. Even though the underlying endomorphism objects for different labels may be isomorphic, the external direct-sum tags and their projections remain distinct; the argument does not rely on nonisomorphism there.

For dimension-eight central etale A, all underlying simples are pointed. The I(1) formal-codegree bound makes F(A) connected. Separability makes F(A) a simple regular right module, so free-module adjunction gives each underlying invertible multiplicity at most one; the support is its stabilizer subgroup, of order eight. The lemma splits it into central invertibles, which must all be bosons by twist-freeness. This contradicts the exact four-boson count.

This closes the conditional paragraph in Section 3: the direct-condensation exclusion is unconditional for the Radchenko-Wheeler examples. It still does not exclude R155 itself or the (8,16) near-group route.
