# Correlated relative traces in a biquadratic field

This is an additive finite-height necessary-condition method. A feasible
relaxation is not a categorification, and an exhausted height does not exhaust
all possible categorical obstructions. General-category exclusions require
the separate full sphericalization lift described below.

Let K=Q(sqrt(q),sqrt(r)), where q,r>1 are coprime squarefree positive integers.
For s in {q,r,qr}, put F_s=s if s=1 modulo4, and F_s=4s otherwise, and let
chi_s be the quadratic character of fundamental discriminant F_s. Coordinates
are in the basis (1,sqrt(q),sqrt(r),sqrt(qr)). For a primitive n-th root, the
normalized relative trace to K (equivalently to the intersection with its
cyclotomic field) has rational coordinate mu(n)/phi(n). Its sqrt(s) coordinate
is

    epsilon_s * mu(n/F_s) * chi_s(n/F_s) * sqrt(F_s/s) / phi(n)

when F_s divides n and gcd(n/F_s,F_s)=1, and is zero otherwise. There are four
linked choices: epsilon_q,epsilon_r in {+1,-1}, and
**epsilon_qr=epsilon_q epsilon_r**. These are the four field automorphisms;
the third sign cannot be chosen independently.

For the k-th power of a primitive N-th root set g=gcd(N,k), n=N/g. Apply the
same formula with n and multiply the sqrt(s) coordinate by chi_s(k/g).
Use one fixed pair of signs for all powers. This retains correlations which
separate independent one-power relaxations would lose.

## Derivation and complete finite order box

The rational projection is the Ramanujan sum mu(n). The quadratic projections
are the primitive quadratic Gauss sums, followed by the coprime-part Ramanujan
sum: tau(chi_s)=sqrt(F_s) and the coefficient is
mu(n/F_s) chi_s(n/F_s) tau(chi_s)/phi(n). Division by sqrt(s) gives the displayed
formula. The primitive character vanishes on conductor primes, which gives
the divisibility and coprimality conditions. The embeddings of K multiply the
three quadratic Gauss sums by the linked signs. The power rule follows by
reducing the root order and applying the corresponding cyclotomic automorphism.

Let P contain the prime divisors of the norm of the pseudo-unitary global
dimension D. The spherical Cauchy theorem bounds the prime support of twist
orders by P (Bruillard–Ng–Rowell–Wang, *Rank-finiteness for modular categories*,
arXiv:1310.7050). For height h define

    B = product over p in P of p^(max(1,v_p(F_q),v_p(F_r),v_p(F_qr))
                                  + floor(log_p(h))).

Every joint trace of powers 1 through h is either represented by an order
dividing B or is the joint zero vector. Indeed, if v_p(N) exceeds the displayed
bound, then after division by gcd(N,k), for every k<=h the p-valuation exceeds
all three conductor valuations and exceeds1. Its rational Mobius term is zero;
each quadratic term is zero either because the remaining quotient is not
coprime to the conductor or because its Mobius value is zero. Other coordinates
cannot rescue the joint trace. Thus enumeration of all divisors of B, all four
linked signs, and one zero joint type is complete for this height. The code
checks the conductor support and norm integrality before using this bound.

At height4 the fields (q,r)=(3,7),(3,5),(3,13) and prime supports respectively
{2,3,7},{2,3,5},{2,3,13} give bounds1008,720,1872. These are trace bounds,
not upper bounds on the exponent of a categorification.

## Exact induction and rotation relaxation

Use the full induction Gram matrix B_ij=[F I(X_i):X_j]. For every simple
Grothendieck-algebra representation E, the distinguished central simple A_E
has dimension D/f_E and multiplicity dim(E) in I(1). Its restriction column
therefore starts with dim(E), and contributes its column square once to B.
All compatible low columns are enumerated, including this weighted first-row
identity. The remaining nonnegative columns satisfy the full residual Gram
bounds. Their central dimensions z are required to have integral D/z and the
necessary d-number property. Dropping other conditions only enlarges the
feasible set and cannot create a false exclusion.

For each high column and each linked joint trace type introduce a nonnegative
weight. Impose all Gram equalities, first and second indicator identities,
and the cyclic-rotation trace identities on Hom(1,X^m), for 3<=m<=h and every
proper divisor of m. Rotation spectra use the same exact relative traces of
roots whose orders divide m. The variables are a relaxation of multiplicities;
a hypothetical pseudo-unitary category supplies a feasible point. Each negative
certificate consists of exact rational Farkas multipliers checked after clearing
denominators. The numerical solver only proposes those multipliers.

## Scope and independent verification

A rotation certificate alone has **pseudo-unitary scope**. The lifted proof
also checks every original spherical dimension character: it is eliminated
by an exact formal-codegree obstruction or reduced by a checked Galois/sign
argument to the FP character. It then exhausts every oriented signed quotient
in the sphericalization enumeration, eliminating it by the adjoint parity
criterion, a verified gauge equivalence, or exact character obstructions using
both original and signed formal codegrees. Only this full certificate receives
general complex fusion-category scope. No pivotality conjecture is assumed.

`verify_general_biquadratic_traces.py` independently constructs the cyclotomic
quotient Q[x]/Phi_L with L=lcm(B,1,2,...,h), constructs the quadratic Gauss
sums there, checks their
squares and correlated product, enumerates the exact fixed subgroup, and
compares all coefficients of every bounded-order joint trace with the formula,
including the rotation orders dividing each m<=h.
It covers the three generalized fields above and Q(sqrt2,sqrt3) at height6.
Its receipt is deterministic and normal replay is read-only. This is an
independent check of the trace formulas; the analytic argument above supplies
the completeness beyond the finite box.
