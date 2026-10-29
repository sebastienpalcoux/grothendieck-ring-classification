# The equality case of the bosonic-row mass bound

Let a modular category have symmetric unitary normalized S, actual twists T, and anomaly xi of absolute value one, so STS=xi T^-1 S T^-1. Let J be a set of twist-one labels. Suppose X is not in J and S(X,j) is real for every j in J. Put

    a = sum_(j in J) S(X,j)^2.

The known diagonal STS contribution is exactly a. Outside J the row has squared norm 1-a, and |S(X,X)|<=sqrt(1-a). Taking absolute values in the diagonal modular relation yields

    a <= (1-a)+sqrt(1-a).

Hence a<=3/4. This is a necessary modular condition, not a categorification criterion.

**Equality theorem.** Assume in addition that J is closed under duality and a=3/4. Then X is self-dual, its twist is -1, xi is +1 or -1, and S(X,X)=xi/2. In particular, in the Drinfeld center of a spherical fusion category, with its canonical anomaly-one normalization,

    theta_X=-1,      S(X,X)=1/2.

**Proof.** Equality holds in every inequality above. In particular |S(X,X)|=1/2 exhausts the entire outside-J row norm. Every other outside-J entry of row X vanishes.

If X were distinct from X*, then X* would also lie outside J. The identity S(X*,j)=conjugate(S(X,j)) and the real known J entries would give both rows the same restriction to J, of squared norm 3/4. Their remaining supports could only be their distinct diagonal positions. Their Hermitian inner product would therefore be 3/4 rather than zero, contradicting unitarity. Thus X is self-dual, and its entire S row is real. In particular S(X,X)=+1/2 or -1/2.

The diagonal modular equation is now

    3/4 + theta_X/4 = xi theta_X^-2 S(X,X).

The right-hand side has absolute value 1/2. Since theta_X is on the unit circle, the left-hand side has absolute value 1/2 only for theta_X=-1. The equation then reads 1/2=xi S(X,X), forcing xi=+1 or -1 and S(X,X)=xi/2. QED.

For R137 take J to be all nine distinguished constituents of I(1). Their twists are one, and their known rows chi_E(v)/f_E are real. Indeed each such label is self-dual, so J is duality-closed. An outside-J simple has v0=0. Thus any physical column with

    sum_E (chi_E(v)/f_E)^2 = 3/4

must have exact twist -1. Its first four normalized trace-to-K moments are consequently (-1,+1,-1,+1). This deletes any other trace type, even though the coarser strict-inequality test a>3/4 permits the column.

## For R137 the inequality is strict

In fact equality is impossible for **every nonzero integral restriction vector** of R137 outside I(1), not merely for the finitely listed columns. To avoid overloading the letter a, write m for the known bosonic row mass, a=v1+v2+v7+2v8 for the integral FP-dimension coefficient, and b=v3+v4+v5+v6. Here v0=0.

At equality m=3/4, the row support and diagonal established above give orthogonality with the unit row:

    sum_E chi_E(v)/f_E^2 + (a+b d)/(2D)=0.

Exact substitution of the nine characters gives the left-hand side as

    (31v1-5v2-5v7-2b+44v8)/576
      + (-2v1-2v2-2v7+b-4v8) sqrt(2)/96.

Its vanishing is equivalent to

    b=2a,          v2+v7=3v1+4v8.

Put p=v1 and q=v8. Under these two linear identities the row mass is exactly

    m = [9p^2+24pq+21q^2+(v2-v7)^2
         +(v3-v6)^2+(v4-v5)^2]/16
        +(v3+v6-v4-v5)^2/64.

If q>=1, this exceeds 3/4. If p>=2, it also exceeds 3/4. If p=q=0, both linear identities and nonnegativity force v=0. Thus equality could only occur for p=1,q=0. Now v2+v7=3, so (v2-v7)^2 is 1 or 9; the latter is too large. Equality therefore requires

    (v3-v6)^2+(v4-v5)^2
       +(v3+v6-v4-v5)^2/4 = 2,
    v3+v4+v5+v6 = 8.

Let u=v3+v6 and w=v4+v5. If u,w are even, all three terms on the left are divisible by 4. If u,w are odd, the first two terms are 1 modulo 4, and (u-w)^2/4 is also 1 modulo 4 because u+w=8. The sum is consequently 0 or 3 modulo 4, never 2. This contradiction proves m<3/4.

The argument is theoretical and applies to arbitrary nonnegative integral restriction vectors. It uses no bounded enumeration of vector sizes. In the saved domains, the equality case alone accounts for 636 additional positive-TY variables and 624 negative-TY variables beyond the Galois complement filter. They are disjoint from the strict m>3/4 cuts. This strengthens the necessary system; it does not exclude either whole ring by itself.

The duality-closure assumption is included explicitly in the equality theorem. It is not needed for the basic upper bound, but the proof of self-duality at equality uses it.

The exact linear and quadratic identities, terminal parity calculation, and both domain counts are independently checked by `verify_bosonic_mass_boundary.py`; the receipt is `bosonic_mass_boundary_receipt.json`.
