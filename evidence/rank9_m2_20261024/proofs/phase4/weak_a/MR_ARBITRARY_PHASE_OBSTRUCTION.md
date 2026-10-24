# A five-equation obstruction for every complex tensorator in the mixed lift ansatz

The earlier phase3 tests ruled out16th- and32nd-root tensorators for the
mixed Moore–Read lift(p,r,v)=(2,15,1). That statement was intentionally
bounded. Here we remove the phase bound entirely, uniformly for
p=2,6,10,14 and r=7,15,v=1. This excludes these proposed tensor-functor
lifts preserving the given central condensation algebra; it does not
classify all actions on every generalized Moore–Read category and does
not by itself exclude R9_2_1254.

Use the notation of `phase2/weak_integral/mr_mixed_action.py`: objects of
the parity subcategory of Ising boxtimes Vec(C16,omega_p) are(i,a), with
i=0,1,2 for1,psi,sigma and charge a of the same parity as i==2.
The proposed functor is

    F(i,a)=(i+(a/2 mod2) mod2, r*a), if i<2;
    F(2,a)=(2,r*a).

The central boson is g=(psi,8), with right half-braiding phase
`zeta16^(j a + e_i)`, j=-p/2 modulo8 and(e_0,e_1,e_2)=(0,8,12).
The tensorator J(a,b;c) is an arbitrary nonzero complex scalar on each
multiplicity-one channel a b ->c. It is not restricted to modulus one
or to roots of unity.

Define four ratios of tensorator scalars:

    x=J((psi,6),(sigma,3);(sigma,9)) /
      J((sigma,3),(psi,6);(sigma,9)),
    y=J((sigma,9),(psi,6);(sigma,15)) /
      J((psi,6),(sigma,9);(sigma,15)),
    z=J((sigma,15),(sigma,9);(psi,8)) /
      J((sigma,9),(sigma,15);(psi,8)),
    t=J((psi,8),(sigma,15);(sigma,7)) /
      J((sigma,15),(psi,8);(sigma,7)).

For p=2,r=15, four entries of the tensor-functor associator equation and
one central transport equation give, respectively,

    xy=zeta16^12,  x=zeta16^2,  yz=zeta16^6,
    zt=zeta16^2,   t=zeta16^14.

Multiplying the second, third and fifth and dividing by the first and
fourth gives1=zeta16^8=-1. This is a contradiction in C*.

The four associator channels(a,b,c;d;e,f) are listed verbatim in
`verify_mr_five_equations.py`. That independent verifier imports no
previous equation generator and computes their exponent ratios from the
standard Ising F-symbol signs and the explicit pointed3-cocycle. It checks
the same contradiction for all8 choices of p,r. The exact5-equation
linear combination has coefficient vector(-1,1,1,-1,1); its variable
coefficients vanish over the integers, not merely modulo16.

For reproducibility, `mr_exact_relation.py` discovers the relation from
all19169 equations by integer sparse elimination. The discovered source
row indices and integer coefficients are in `mr_exact_relation.json`.
The small independent direct verification is authoritative for replay;
no solver or large matrix normal form is required.

A full-Hermite-normal-form exploratory run was not completed and is not
used in this proof. The short identity replaces it completely.
