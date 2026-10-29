# Independent audit: R1660/R941 continuation

29 October 2026. Reviewer: separate R155 research agent.

## Verdict

The two new arguments in `../pair/REPORT.md` are valid within their stated
hypotheses. They exclude construction routes, not either fusion ring. The
nonreal invariant argument must retain its positive spherical scope when
discussing complex conjugation and real forms. I flagged a sentence whose
construction consequence omitted that scope; the author agreed to correct it.

## Weighted third indicator

Starting with the inherited positive-indicator values, independently expand

\[
1+2d(2+\omega)+2\sqrt2d
=1+(3+2\sqrt2)d+i\sqrt3d.
\]

The other branch is its conjugate. The imaginary part cannot vanish because
d is positive. Ng–Schauenburg, arXiv:math/0601012v3, Theorem 4.1, gives the
source indicator as the normalized twist trace of induction. Summing with
dimension coefficients gives

\[
W_n=\operatorname{FPdim}(C)^{-1}
\sum_{Z\in\operatorname{Irr}Z(C)}\operatorname{FPdim}(Z)^2\theta_Z^n.
\]

Morita equivalence preserves the braided center and, for pseudo-unitary
categories, its unique positive spherical structure. Hence it preserves W_n.
Complex conjugation conjugates W_n, and tensor opposition reverses the
center's braiding and twist, also conjugating it. Thus a positive
categorification cannot be Morita equivalent to its conjugate or tensor
opposite. A real form in this positive Morita class is consequently impossible.

A braided Morita representative is impossible as well: every braided fusion
category is tensor equivalent to its tensor-opposite, using its braiding as
the tensor comparison. This would make the original category Morita
equivalent to its tensor-opposite.

The no-tensor-opposite and no-braided-Morita-representative consequences may
be transported back through an actual positive Galois conjugation: opposite
tensor products, braidings, and module categories all transport. The same
one-line transport does not establish a real-descent obstruction for every
original complex categorification, since arbitrary Galois automorphisms need
not commute with complex conjugation. Retaining positive scope for the latter
claim avoids that unproved extension.

The R941 corollary remains conditional on a categorical Morita equivalence,
not merely equality of FP dimensions.

## The SU(2) level-(6,10) dimension cone

The added direct-modular-source proposition also passes. Given the inherited
strict dominance bounds, any proper nontrivial nondegenerate H in the center
would have a nontrivial nondegenerate centralizer H′. Neither can be pointed,
because the pointed center is sVec. Hence both dimensions would exceed D,
contradicting their product D². The center is prime. DMNO Corollary 3.30 then
forces any presentation C≅B_A with B nondegenerate braided and A connected
étale to have B_A^0=Vec, B≅Z(C), and A Lagrangian. This conclusion is properly
limited to full module categories over connected étale algebras; it does not
exclude arbitrary module duals, nonmodular sources, or local-module
constructions of the center. The inherited dominance hypotheses were checked
against `../pair/prior/REPORT.md`; no new premise is inferred from the common
FP dimension.

I independently checked the complete simple-dimension lists using the
standard sine formula and verified exactly with SymPy that

\[
(16+8\sqrt2)(48+24\sqrt3)
=(24-8\sqrt6)(144+96\sqrt2+80\sqrt3+56\sqrt6).
\]

For K=Q(√2,√3), c=√(2+√2) does not belong to K. Writing c=a+b√3 with
a,b∈Q(√2) forces a=0 or b=0, because c² lies in Q(√2). The two alternatives
require 2+√2 or (2+√2)/3 to be squares in Q(√2), whose norms 2 and 2/9 rule
this out. Thus the eight displayed basis elements are independent. Their
multiplication constants are nonnegative. Every source simple dimension is
in their nonnegative rational cone, whereas the required algebra dimension
24−8√6 is not. The full-module and doubled-source local-module dimension
formulas used in the note therefore exclude the specified constructions.

The argument uses FP dimensions, so these particular route exclusions do
not depend on positivity of a chosen spherical structure or on unitarity.
They also survive Galois forms of the same based source rings.

## Replay and limitations

Read the complete checker `../pair/verify.py`, then ran it under ordinary
Python: PASS. It uses assertions and is therefore an ordinary-Python check;
an optimized-Python run would not be a valid verification. Its arithmetic
input includes the inherited indicator theorem as a hypothesis and does not
purport to prove its categorical completeness afresh.

Primary references inspected:

- Ng–Schauenburg, Theorem 4.1:
  https://arxiv.org/html/math/0601012v3 .
- DMNO, Section 2.1 (unique positive spherical structure), Section 2.2
  (reverse braiding), module-dimension formulas:
  https://arxiv.org/html/1009.2117v2 .

No online changes were made. Neither ring is reclassified by these results.
