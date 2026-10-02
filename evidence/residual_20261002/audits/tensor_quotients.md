# Independent audit of the R6_8_1660 tensor-quotient obstruction

2026-10-02. **PASS for the stated scope:** every dominant pivotal tensor
functor out of the retained positive spherical form is an equivalence.
The corollary for dominant unitary tensor functors is valid. This does not
exclude the fusion ring, and does not eliminate arbitrary module categories.

No mathematical gap was found in the proof as stated. The established
second-indicator signs and pseudo-unitary Galois reduction remain prior inputs;
this audit does not rerun their substantially larger center certificates.

## Checks

1. **Nimrep foundations.** The Ising restriction argument is sound: its
   symmetric spin matrix satisfies H^2=I+G, GH=H, and has only connected A3
   blocks. For n blocks, M=U+sqrt(2)R is nonnegative irreducible and annihilated
   by the quadratic with roots d and -1/d. Irreducibility of this polynomial
   over Q(sqrt(2)), together with a simple Perron root, forces n=2. This
   argument needs no later full-center saturation or Morita Gram theorem.
   The small-squares equations give precisely the four rows up to block
   exchange, and the integral symmetric involutions V give 2,2,4,4 raw choices.

2. **The target and its unit.** Dominance makes D indecomposable as a
   C-module. FPdim(F(sigma))=sqrt(2) makes this image simple; its self-duality
   rules out F(g)=1. Thus the image of the Ising subcategory is a full Ising
   subcategory. The tensor unit of D must be a leaf. The common positive
   dimension vector is unique up to scale, and every recorded ratio exceeds
   1, so the unit must lie in the smaller block. Either leaf in that block
   gives exactly the same two parity constraints.

3. **Pivotal parity.** A pivotal tensor functor transports nondegenerate
   self-dualities and their transpose signs. On an isotypic component for a
   skew self-dual simple, a symmetric self-duality requires an alternating
   nondegenerate multiplicity-space form, hence even multiplicity. This
   applies to F(X) and F(T), using the negative sign of the simple F(sigma).
   The correct conclusion is parity of multiplicities, not equality of the
   numerical indicators of an object and its possibly nonsimple image.
   The entries are c and a, respectively, excluding rows III and IV.

4. **Dimension gap.** Row II has a target simple of dimension r with
   1<148/125<r<1189/1000<6/5<sqrt(2). A simple of dimension greater than 1
   has its dual product containing the unit and another simple, giving
   dimension at least sqrt(2). The rational root bounds in the verifier prove
   the claimed strict inequalities exactly.

5. **Remaining row.** For row I, either allowed unit leaf has internal end
   precisely 1. Adjunction gives R_F(1)=1; rigidity gives the projection
   formula R_F(F(Z))=Z tensor R_F(1). Thus F is fully faithful, and dominance
   makes it an equivalence.

6. **Unitary corollary.** A unitary tensor functor between fusion C*-categories
   preserves the canonical positive pivotal structures. One can justify this
   directly: images of standard conjugate solutions have the same scalar
   norms, tensor functors preserve FP dimensions, and in a unitary fusion
   category intrinsic dimension equals FP dimension. Hence the image
   solutions attain the minimal intrinsic dimension and remain standard.
   This uses the fusion/simple-unit hypotheses; it should not be generalized
   without qualification to arbitrary multitensor categories.

## Exact independent replay

`audit_tensor_quotient.py` independently enumerates all bounded scalar
small-squares solutions and all V matrices. It verifies the exact Perron
ratios, the six dimension eigenvector identities, both possible first-block
unit leaves, the image multiplicities, and the row-I internal ends. It also
replays the proposed verifier with its output redirected into this audit
directory. Both checks pass. Receipt:
`tensor_quotient_independent_receipt.json`.

The proposed verifier itself hardcodes the four U,R rows; this is not a proof
gap because completeness is supplied by the existing theorem. The independent
enumeration here also checks that interface.

## Sources inspected

- The project's `frontier_1660_morita.tex`, through the complete based-module
  list, and `verify_module_targets.py`.
- The project's `frontier_1660.tex`, uniform second-indicator proposition.
- Bruguières–Natale, *Exact sequences of tensor categories*, Section 5.1,
  https://arxiv.org/html/1006.0569v1, for the induced central algebra and the
  standard dominant-functor/module-category correspondence.
- EGNO, *Tensor Categories*, Sections 4.5, 7.12, and 9.5,
  https://math.mit.edu/~etingof/egnobookfinal.pdf.
- Penneys, *Unitary dual functors for unitary multitensor categories*,
  https://arxiv.org/abs/1808.00323, for the standard unitary dual/pivotal
  framework. The direct dimension-minimality argument above establishes the
  functorial claim needed here.

Keep the pivotal-functor hypothesis explicit in the theorem. The audit makes
no assertion extending it to arbitrary nonpivotal tensor quotients.
