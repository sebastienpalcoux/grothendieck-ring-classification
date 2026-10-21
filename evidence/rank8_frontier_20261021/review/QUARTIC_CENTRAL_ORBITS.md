# Forced central involutions for R928 and R941

Work in the pseudo-unitary Galois conjugate provided by the previously
reviewed unrestricted signed-sector gates. All conclusions below are
necessary structure; they construct no category and imply no tensor
factorization of the original category.

The complete source/domain and two independently implemented integer-Gram
and distinguished-Verlinde enumerations are
`quartic_integer_center/source.py/.json` and `gram_cubic.py/.json`.
They leave exactly 343 patterns for each ring. Every pattern has exactly
one central simple with restriction g, where g is the nonunit central
invertible source object (source index 7 for R928 and 3 for R941).

## Kernel and order

Among all distinguished constituents of I(1), only the tensor unit has
restriction supported entirely on the source unit. Any central simple
whose restriction is k*1 occurs in I(1) with multiplicity k, so the complete
low list shows that the forgetful kernel is Vec.

If a central simple Z restricts to k*g, then Z Z* restricts to k^2*1.
Every constituent of Z Z* therefore lies in this kernel, hence is the unit.
Rigidity gives the unit multiplicity one, forcing k=1. Moreover, two distinct
lifts of g would differ by an invertible in the kernel, which is impossible.
Consequently the pure-2g column is forbidden and the pure-g column has
multiplicity at most one. The complete 343-pattern enumeration forces its
multiplicity to be exactly one; denote this central invertible by G.
Since F(G^2)=1, the kernel statement gives G^2=1.

Tensoring by G permutes the central simples and translates restrictions by
the tensor-derived permutation g. Each of the five low columns translates
to canonical high index 40,41,42,43,57, respectively. Each of these high
multiplicities is exactly one, because its inverse image is the single
corresponding low simple. All high indices 0 through 39 are fixed as
restriction vectors. The other twenty high columns have positive-unit
translates absent from the complete low list, so have multiplicity zero.
The reviewer checks this graph directly against all 343 integer patterns.

## Pointed sign and semionic moments

The original complete height-six rotation receipts are replayed rather than
merely read. They force nu_2(g)=-1 for R928 and nu_2(g)=+1 for R941.
The forgetful functor preserves the canonical positive pivotal structure.
On a normalized pointed order-two subcategory,
nu_2(g)=omega(g,g,g); see Schauenburg, arXiv:1502.02906, Definition 2.2
and Proposition 4.1 with H={1} (or the one-dimensional rotation directly).
The order-two hexagon gives c(G,G)^2=omega(G,G,G). Balancing then implies

    theta_G^2 = nu_2(g).

Thus R928 forces theta_G=+i or -i; R941 permits +1 or -1 at this stage.
The R941 boson exclusion requires the separate de-equivariantization/rank-four
argument and is not assumed by this checker.

For any central simple Z, its monodromy charge
M_GZ=S(G,Z)/dim(Z) is an eigenvalue of the involution fusion matrix N_G,
so M_GZ is +1 or -1. Balancing gives

    theta_(GZ) = theta_G*M_GZ*theta_Z.

In the semion case a fixed simple would force 1=theta_G*M_GZ, impossible.
Thus G acts freely on all central simples. For each fixed restriction type
0 through 39, its multiplicity is even. Exactly 15 of the 343 patterns
satisfy this necessary parity condition, at canonical indices

    2,6,40,44,49,58,61,64,186,191,196,199,243,245,248.

Each pair of twists differs by +i or -i. Therefore its second and sixth
power sums vanish exactly, before taking any relative trace. All these
fixed restriction types have zero second and sixth total twist moments.
For a low object A_E, theta_(A_E)=1 and
M_G,A_E=chi_E(g)/dim(E), obtained from the normalized distinguished S row.
The five charges are +1,+1,+1,+1,-1. Consequently all five translated high
objects have twists +i or -i and their normalized traces to the real FP field
at powers 1 through 6 are exactly (0,-1,0,1,0,-1).
These constraints may be added to the subsequent fixed-pattern rotation/STS
systems. They are not by themselves a noncategorifiability result.

The checker verifies the tensor graph, all recorded Gram/cubic patterns,
complete original indicator certificates, charges including the matrix
character factor two, and all finite parity/moment data. Its known control
uses both actual pointed semion quadratic forms with Gaussian-integer
arithmetic. Full pattern completeness remains supplied by the separately
registered two-algorithm enumerator.

```
python evidence/rank8_frontier_20261021/review/verify_quartic_central_orbits.py
python -O evidence/rank8_frontier_20261021/review/verify_quartic_central_orbits.py
```
