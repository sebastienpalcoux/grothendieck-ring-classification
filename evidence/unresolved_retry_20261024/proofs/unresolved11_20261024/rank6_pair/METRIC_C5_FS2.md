# Independent second-indicator audit of the rank-14 metric-C5 candidate

For the candidate `build(1,2,1)` in `rank10_case189/metric_modular_completion.py`, the exact second Frobenius–Schur indicator vector is

    [1,1,0,0,0,0,0,0,0,0,-1,1,1,-1]

in basis `(1,U,B1,B2,B3,B4,C1,C2,C3,C4,Y,P1,P2,X)`. It has the required zeros on nonselfdual simples and signs on selfdual simples. Thus this check supplies no obstruction.

The replayer `verify_metric_c5_fs2.py` executes only the construction prefix before `results=[]`. It evaluates the indicator formula by factorization through the normalized S-matrix and, independently, by the direct double sum over the exported full fusion tensor. Both exact computations agree in Q(zeta5); no floating-point arithmetic is used. The global dimension is100(2+sqrt(5))², and the actual ribbon twists are used.

The primary categorical justification is Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical Categories*, Theorem7.5 and Remark7.6:

https://arxiv.org/html/math/0601012v3

Section7 assumes a modular tensor category with its underlying spherical structure. Its formula is

    nu_n(X_k) = sum_ij N_ij^k d_i d_j (theta_i/theta_j)^n / Dim(C).

It imposes no unitarity hypothesis, and therefore applies to the pseudo-unitary modular representative used here. Taking n=2 gives the test above.

A passing necessary indicator test does not establish categorification, associators, or a model of the original rank-ten ring.

## Bounded higher-indicator extension

The subsequent exact check computes all indicator vectors for orders1 through10 and all140 ordinary cyclic rotation spectra (14simples times10orders). Every spectrum has nonnegative integral multiplicities. The order-one vector is the unit delta, and the order-ten vector equals the FP dimension vector.

For the kth power of the order-n rotation, put r=gcd(n,k). Grouping r adjacent copies gives the order-(n/r) rotation on X^r. The required trace is the (k/r)-Galois conjugate of nu_(n/r)(X^r). Tensor powers are computed from the exported fusion tensor. For orders5 and10 the Fourier sums are evaluated directly in Q(zeta5); for the other orders all relevant traces are rational and exact Ramanujan sums perform the Fourier inversion. No ambient numerical cyclotomic approximation is used.

The replayer is `verify_metric_c5_higher_indicators.py`, and `metric_c5_higher_indicator_certificate.json` records every indicator and spectrum, plus source hashes. This is a bounded admissibility check, not a proof of all-order admissibility or existence.
