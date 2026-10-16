# R489: sphericality, Galois pseudo-unitarity, and an actual C2 algebra

This is a necessary structural reduction, not a categorification or exclusion.
Every complex fusion categorification of R8_2_489 admits a spherical structure, is Galois conjugate to a pseudo-unitary category, and has trivial associator on its pointed C2 subcategory. Consequently 1+g is a connected separable algebra.

## Ring and exact finite sign calculation

Use generators g, tau, x with

    g^2=1, tau^2=1+tau, x^2=1+tau(x+gx).

The eight basis objects are 1,g,tau,g tau,x,gx,tau x,g tau x; all are self-dual. In census order (g,tau,x)=(1,7,3), with gx=6, tau x=4, g tau x=5, g tau=2. The portable replay reads and hashes the full census tensor and checks the fusion axioms and these relations.

In the canonical sphericalization choose the positive-second-indicator lift of every self-dual simple, as in the existing signed-sphericalization certificates. In the signed quotient epsilon=-1, coefficients T satisfy full triple symmetry, associativity, and

    N_jj^i - T_jj^i = 0 mod4.

All coefficients are at most two, and every multiplicity-two channel has a repeated label. Hence all signed coefficients have absolute value equal to the unsigned coefficient. Repeated multiplicity-one channels are positive; all remaining channels have a Boolean sign. There are sixteen such signs.

The standard-library verifier generates every associativity equation, deduplicates to 100 integer equations, and exhaustively traverses both values of every sign. It visits 59 nodes and finds exactly four solutions. Each is a coboundary

    T_ij^k = s_i s_j s_k N_ij^k,

where the only possibly negative s_i are s_g and s_(g tau). All four choices occur. Changing to the lifts s_i X_i^+ therefore gives a closed spherical section in every case. This alone establishes sphericality.

One can additionally discard the three non-original sign solutions by the odd-power homogeneous-form argument below. The exact unsigned congruences are

    x^3 = x+tau+g tau (mod2),
    (g tau)^3 = g (mod2).

Work inside the already obtained closed section with simples s_i X_i^+. Its simple indicators are s_i, and tau and x both have indicator +1. Hence x^3 has a positive homogeneous form. The first identity forces s_(g tau)=+1. The same argument applied to (g tau)^3 then forces s_g=+1. Thus the original positive lifts themselves form the spherical section, and its simple second indicators are all +1.

## Dimension character and formal-codegree integrality

Let h=d(g) in {1,-1}, t=d(tau), z=d(x). Then t^2=t+1 and

    z^2=1+t(1+h)z.

If h=1, then z satisfies

    f(z)=z^4-2z^3-6z^2+2z+1=0,
    t=(z^2-1)/(2z).

The polynomial f is irreducible modulo three (the verifier checks all linear and monic quadratic possible factors). Its four roots correspond to exactly the four dimension characters with h=1. The positive root d=phi+sqrt(phi^2+1) gives the Frobenius--Perron dimensions. Therefore these four characters constitute one Galois orbit.

If h=-1, then z=+1 or -1 and the global spherical dimension is

    delta=4(t+2).

Because the source ring is commutative, every ring character has formal codegree equal to the sum of its squared basis values. Choose either h=1 character with the same t and write its x-value as d. Its formal codegree is

    f_E=2(t+2)(1+d^2).

Thus delta/f_E=2/(1+d^2). For a spherical fusion category this ratio must be an algebraic integer, by induction to the Drinfeld center and formal-codegree divisibility (Ostrik, Pivotal fusion categories of rank 3, arXiv:1309.4822, Theorem 2.13).

But y=2/(1+d^2) has primitive polynomial

    5y^4-20y^3+25y^2-10y+1.

This is its minimal polynomial: f(d)=0 gives

    d=((d^2)^2-6d^2+1)/(2(d^2-1)),

so Q(d)=Q(d^2)=Q(y), of degree four. The leading coefficient five and constant coefficient one show y is not an algebraic integer. The verifier checks the elimination identity exactly. This rules out h=-1.

Consequently every possible spherical dimension character belongs to the FP Galois orbit. Apply a field automorphism to the category and its spherical structure taking that character to the positive one. The resulting spherical category is pseudo-unitary.

## The pointed associator

For clarity, the homogeneous-form fact used above is this: in a pivotal category a self-dual object V with symmetric (respectively skew-symmetric) nondegenerate pairing has a canonical pairing on V^n of sign nu_2(V)^n. It uses the reversal in the monoidal duality and the same pairing on every tensor factor. A self-dual simple of opposite indicator must occur with even multiplicity in such an object, since its multiplicity-space pairing is alternating. This is also the palindromic tensor-power argument used in the independent R49 certificate.

In the pseudo-unitary Galois conjugate, the above section has nu_2(g)=+1 and d(g)=1. For the pointed rank-two category Vec_(C2)^omega with positive spherical dimensions, the nontrivial cohomology class has nu_2(g)=-1. Therefore omega is trivial. The algebra 1+g is the usual regular C2 algebra and is connected separable. Galois conjugation preserves existence of this algebra, so it exists also in the original category.

No half-braiding on g or tau is inferred. In particular, this result does not itself provide a de-equivariantization or a Deligne factorization.

## Replay

    python verify_fib_r489_galois_pu.py --repo /absolute/path/to/repository
    python -O verify_fib_r489_galois_pu.py --repo /absolute/path/to/repository

Both runs use only the Python standard library. The checked sign list, gauges, tensor identities, and exact elimination agree in both receipts.
