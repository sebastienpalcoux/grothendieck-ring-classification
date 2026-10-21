# Independent R455 trace-field and categorical-scope review

The complete trace domain and STS normalization used by the R455 exclusion
are valid in the pseudo-unitary Galois conjugate supplied by the previously
reviewed unrestricted signed-sector gate. Together with the independent
`r455_review/verify_direct.py` arithmetic review, this proves general-complex
noncategorifiability. No unitarity hypothesis, pointed strictification,
or exclusion of integral central objects is used.

## Complete root-of-unity domain

The splitting field is K=Q(sqrt(3),sqrt(13)); all five irreducible characters,
including the matrix character, take values in this real field. The positive
global dimension is D=39+9 sqrt(13). Its quadratic norm is 468 and its norm
in K is 468^2. Bruillard--Ng--Rowell--Wang, arXiv:1310.7050v3,
Theorem 3.9, and Ng--Schauenburg, arXiv:math/0601012, Theorem 5.5,
therefore restrict center-twist orders to prime support {2,3,13}.

The three primitive quadratic conductors are 12,13,156. The Ramanujan/Gauss
projection formula in manuscript Proposition `prop:m3-biquadratic-traces`
thus has height-six bound 2^4*3^2*13=1872. This bounds retained joint traces;
it does not bound the categorical exponent. If an order has a larger
p-valuation, reduction by any k<=6 leaves a valuation greater than one and
all three conductor valuations. The rational Möbius term vanishes, and
every quadratic term vanishes by either noncoprimality with its conductor
or a square factor in the Möbius argument. All six moments are then zero.
The sign pair is shared across all powers, and the third sign is its product.

The independent checker builds the exact quotient Q[x]/Phi_9360(x), where
9360=lcm(1872,1,2,3,4,5,6). Its degree is 2304. Explicit quadratic Gauss
sums square to 3 and 13 and multiply to the third basis element. The fixed
subgroup of size 576 gives normalized relative traces directly by averaging
monomial residues. Every bounded central order and every cyclic-rotation
order/power request is checked: 41 requests, all four field automorphisms,
with full polynomial coefficient equality. Their central union, together
with zero, agrees exactly with the producer's 55 correlated trace types.
Integer overflow bounds are explicitly checked for the array operations.

## Noncommutative STS normalization

Put m_E=dim(E), beta_E=D/(f_E*m_E). For a distinguished central object A_E,

    S(A_E,Z)=beta_E*chi_E(FZ).

This is the normalization obtained by inverting Deshpande,
arXiv:1611.04486, equation (39), with full character orthogonality
sum_i chi_E(i)chi_F(i*)=delta_EF*f_E*m_E. The two-dimensional
representation must retain its factor m_E=2. Its distinguished central
object is counted once, although its restriction has unit coefficient two.

Since the center has Gauss sum D and all distinguished twists are one,
STS=D*T^{-1}*S*T^{-1} gives

    sum_Z theta_Z chi_E(FZ)chi_F(FZ)
      = f_F*m_F*chi_E(FA_F).

All coefficients belong to the real field K, so normalized relative trace
of theta factors out directly. No invalid real-part multiplication rule
and no additional unitarity assumption occurs. The two allowable assignments
interchange identical low restriction columns, hence give the same equations.
The reviewer explicitly checks the FP character is the first row, all 25
character orthogonality/S-symmetry pairs, and independently reconstructs all
60 rational-coordinate STS rows from the normalized S matrix. Every entry
of the 715 high-trace columns and every right-hand side agrees with the
producer's normalized operator.

The joint rotation equations use the order-n rotation on Hom(1,X^n): its
nth power is the identity (Ng--Schauenburg, arXiv:math/0503167,
Theorem 5.1). For r|n, its rth power has trace nu_(n/r)(X^r), which follows
by grouping the tensor factors into r-blocks. The center indicator formula
is arXiv:math/0601012, Theorem 4.1. A single nonnegative eigenvalue distribution
for each rotation supplies all its retained divisor moments simultaneously.
The root order 5 needed for these auxiliary rotations is included in the
independent ambient cyclotomic quotient even though 5 is absent from center
twist orders. The producer also checks full STS and all these rotation
identities on the actual center Z(Vec(C2)).

## Scope and replay

The earlier `additional_scope_gates.py/.json` enumeration checks all 32
unrestricted signed tensors of R455; every one is gauge-original. Its
complete scalar/matrix character accounting and ordinary character sieve
force a pseudo-unitary Galois conjugate of any hypothetical complex
categorification. Thus a contradiction to the reviewed PU systems excludes
all complex categorifications.

The independently audited integer-domain chain is 812 complete Gram
patterns, 24 passing all distinguished cubic coefficients, and 12 passing
monodromy parity. All 48 combinations with the four indicator choices have
exact Farkas contradictions. The separate direct reviewer rebuilds every
381-by-792 system and checks every inequality of the common ray. Neither
the extra positive pair-tensor tests nor spectrum filtering is needed in
this minimal exclusion chain.

Canonical no-argument arithmetic replay for the present review:

```
python evidence/rank8_frontier_20261021/review/verify_r455_trace_sts.py
python -O evidence/rank8_frontier_20261021/review/verify_r455_trace_sts.py
```

The source-bound receipt is `r455_trace_sts_review.json`. The arithmetic
checker binds the exact finite identities; the preceding valuation argument
establishes completeness for the unbounded possible root orders.
