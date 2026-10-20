# Integral fusion-norm inequalities

Let `A,B` be specified central simples and let `n_Y=[A B:Y]`. With
restriction matrix `M`, source product `a=F(A)F(B)`, and the quartic Verlinde
moment `q=dim Hom(1,A B B* A*)`, necessarily

`sum_Y n_Y M[Y,:] = a`, and `sum_Y n_Y^2 = q`.

For any rational source-coordinate vector `x`, put

`g*(t)=max_(k in Z_{≥0}) (t k-k^2)`.

This is exactly evaluated at `max(0,floor(t/2))` and the next integer. For
each unknown high coefficient, `n_Y^2 >= (x.M_Y)n_Y-g*(x.M_Y)`.
For a known low constituent choose an arbitrary integer `b_G >= 0`; the
integer identity `(n_G-b_G)(n_G-b_G-1) >= 0` gives

`n_G^2 >= (2b_G+1)n_G-b_G(b_G+1)`.

Summing, and using the restriction equation, proves the globally valid cut

`q >= x.a + sum_low (2b_G+1-x.M_G)n_G
          - sum_low b_G(b_G+1) - sum_high g*(x.M_Y)`.

For a fixed labelled induced-unit frame, `a`, `M_G`, and the formal-codegree
labels are fixed. Each `n_G` is a triple Verlinde moment, `q` is a quartic
Verlinde moment, and the last sum is linear in the high restriction-row
multiplicities. The entire cut is therefore linear in the necessary-data
discovery variables. The choices of `x,b` may be suggested by a failed
witness but are fixed rational/integer parameters in the universally valid
inequality. No optimizer result is needed to justify or replay a cut.

## Exact rank55 witness rejection

For the R5039 `c2_fp5` witness, use low object1 (character0, formal codegree8)
and low object6 (character1, the small conjugate global codegree). Their
source product is `(41,381,381,682,682,762,723)`. Choose

`x=(0,1/2,1/2,1,1,1,1)`, `b=(0,6,5,5,8,8,9)`.

The low coefficients in the cut become `(1,3,1,1,1,1,1)` and its constant is
2894. The witness has quartic moment1621, while the necessary lower bound is
1625. It is therefore impossible to extend this displayed restriction
witness to integral fusion products.

There is also a direct equality explanation. After subtracting its seven
low coefficients, the unknown high vector has squared norm1326. Its
restriction equations have a unique minimum-norm real solution with
coordinate

`(v_1+v_2)/4 + (v_3+v_4+v_5+v_6)/2`

at high restriction row `v`. That solution also has squared norm1326, so
equality forces it to be the actual coefficient vector. It contains the
nonintegral values `1/2,17/2,9/4,9/2`, a contradiction.

This rejects the particular rank55 witness. It does not by itself exclude
R5039, since the restriction-row and twist data can vary. The corresponding
linear inequality can be added to the full search without fixing that
witness.

Replay `verify_integral_norm_cut.py` in normal Python and with `-O`. The
verifier reconstructs exact source characters, checks the full restriction
Gram, recomputes the relevant triple and quartic moments, and checks both
contradictions using rational/algebraic arithmetic only.
