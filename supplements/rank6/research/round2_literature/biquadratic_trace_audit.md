# Independent audit of the biquadratic trace extension

Audited `../round2_external/new_biquadratic_trace.py` against the supplied
B13 proof in `../round2_external/sources/B13_General_Exclusion/proof.tex`.
The extension gives a general complex categorification obstruction; it
does not assume sphericality of the original category.

The general scope is justified as follows. The finite sphericalization
of a hypothetical categorification of a self-dual ring is again
self-dual: a dual lift cannot be the opposite lift, since spherical
simple dimensions are nonzero and equal on duals. Its Grothendieck ring
is therefore commutative. The epsilon=-1 quotient has six commuting
symmetric integral multiplication matrices, a real dimension character,
and character field K of degree at most six.

Central induction in the sphericalization places every original formal
codegree in K and makes Delta/f integral. The program requires their
quadratic fields to generate a biquadratic field E. Hence E is contained
in K, and divisibility of field degrees forces K=E. The same induction
argument applied to the signed characters places every signed formal
codegree in E as well. It applies to genuine characters of the
sphericalization, whose formal codegrees are twice the signed ones.
Their d-number property therefore follows from the ordinary theorem
without assuming nonnegative signed multiplication.

For E=Q(sqrt(p),sqrt(q)), the program requires p=1 mod4 and coprime
quadratic discriminants. The product basis of the two quadratic integer
rings is consequently a maximal integral basis. Direct expansion in
1,phi,eta,phi*eta verifies all four congruences in `integral()` for both
q=1 mod4 and q=2,3 mod4. The four dimension-character conjugates are
distinct even when their formal codegrees coincide. Orthogonality gives

    Tr_E/Q(Delta)=p*q*sum_i w_i^2.

The remaining two codegrees exceed one. Thus their trace uses at least
three units of the integer Casimir trace bound. The program's m bound
and trace lattice follow.

The Perron polynomial tested by the code gives
D=5*k*sqrt(ell)*u, with u^2-s*u-1=0. Thus u is an algebraic unit and
central divisibility implies theta=Delta/(5*k*sqrt(ell)) integral.
Both finite boxes (ell=q and ell=p*q) follow by adding positive
embedding inequalities and retaining strict inequalities before taking
integer square roots. The implemented total-positivity and norm formulas
agree with the two successive quadratic relative norms.

The norm--trace d-number test gives Norm(theta) dividing ell^2*m^4.
For every survivor, the remaining two codegrees have a Galois-invariant
unordered pair. Their sum S and product P are positive integers with
S/P=1-Tr(1/Delta), and the trace bound gives the complete k range in
`complementary_pairs()`. Its real-root and >1 tests are necessary; its
irreducible case additionally tests P|S^2 and membership of the quadratic
root field in E. These are all valid necessary conditions.

Independent optimized replay on the original census tensors returned:

| Tensor | Trace | Trace parameters | Norm survivors | Final result |
|---|---:|---|---:|---|
| R6_7_3813 | 4925 | 1 | 0 | excluded |
| R6_8_6940 | 3580 | 1,2 | 2 | both have no complementary pair |
| R6_8_6973 | 5480 | none | 0 | excluded |

For R6_8_6940 the two surviving dimensions are
(3400 +/- 680*sqrt(5))/4, each with trace 3400. The complete complementary
pair enumeration is empty in both cases. All three certificates replay
under Python -O by recomputing the finite domain and comparing the
entire certificate. No gap was found in the field-containment,
positivity-box, or complementary-codegree scope of this extension.

This is an independent mathematical/code audit, not a proof-assistant
formalization or an independent reproduction of the cited categorical
theorems.

## Casimir parity extension

The later parity filter was also independently checked. Every signed
fusion matrix M_i is congruent to its original fusion matrix N_i modulo
two. Thus the signed Casimir sum_i M_i^2 has the same characteristic
polynomial modulo two as the original Casimir sum_i N_i^2. Its six
codegrees consist of the four embedding-indexed dimensions and the two
complementary codegrees. The function `conjugate_polynomial()` is exactly
the product over all four embeddings, retaining repetitions if Delta
lies in a proper subfield. This proves necessity of the added filter.

Optimized replay also excludes R6_8_6998. Four conjugate dimension
candidates survive the complementary-pair conditions, each with

    P(t)=t^4-1950t^3+650000t^2-63375000t+1056250000,
    Q(t)=t^2-2350t+2500.

Their product reduces to t^6 modulo two. The original Casimir polynomial
reduces to t^6+t^2, giving the contradiction. Other norm survivors have
no complementary pair. The program regenerates all of them, rather than
assuming that these four are the only norm survivors.
