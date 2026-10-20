# Prime-conductor partial projection and exact FP-difference weights

## Uniform representation-theoretic identity

Let `ell` be an odd prime and `chi` the primitive quadratic character
of conductor `ell`. In a unitary congruence representation, let `w`
be upper-unipotent-fixed with torus character `chi`. Let `Q_0` project
only onto the trivial `ell`-primary twist component, and let `Q_1`
project only onto `ell`-primary twist order dividing `ell`; both act
as the identity on the other primary factors. Then

`||Q_1 S w||^2 = ell ||Q_0 S w||^2`,

`||Q_0 S w||^2 <= ||w||^2/ell`.

Thus the squared masses at exact `ell`-primary orders one and `ell`
are `b` and `(ell-1)b`, respectively, where
`b=||Q_0 S w||^2`. Higher primary orders can carry the remaining
mass; they are not discarded.

### Proof at every prime power

At modulus `M=ell^a`, use the universal primitive-vector realization of
`Ind_U^{SL_2(Z/M)} 1`. Write coordinates `(x,y)`. The unipotent-fixed,
torus-character subspace splits orthogonally into the big-cell line

`F(x,y)=chi(y)[ell does not divide y]`

and small-cell functions

`f(x,y)=chi(x)g(xy)` on `x` a unit and `ell` dividing `y`.

Here `g` is defined on the multiples of `ell`; its additional
unipotent-invariance conditions are not needed for this calculation.
Use `(S f)(x,y)=f(-y,x)`. Direct averaging over `T` gives

`Q_0 S F(x,y)=chi(x)[ell divides y]`,

`Q_0 S f(x,y)=chi(-y)*(1/M)*sum_{z divisible by ell}g(z)`

on `y` a unit, and zero elsewhere for the second formula. Averaging
instead over `T^ell` gives

`Q_1 S F(x,y)=chi(x)[x a unit]`,

`Q_1 S f(x,y)=chi(-y)*(ell/M)*sum_{z divisible by ell}g(z)`

on `y` a unit and `ell` dividing `x`, and zero elsewhere. In each
case the big-cell and small-cell outputs have disjoint support.

The big-cell squared norm increases by a factor of `ell` between
the two projectors. For the small cell the two exact squared norms
are

`(phi(M)/M)|sum g|^2` and `(ell*phi(M)/M)|sum g|^2`,

respectively. These establish the exact norm ratio on the entire
domain, including all cross terms by orthogonality. Also

`|sum g|^2 <= (M/ell) sum |g|^2`,

and `||f||^2=phi(M)sum|g|^2`, giving the claimed upper bound for
`Q_0`. The complete largest-singular space is spanned by `F` and
`chi(x)[ell divides y]`, both pulled back from level `ell`.

Frobenius reciprocity embeds every irreducible with a unipotent-fixed
vector isometrically into the universal representation. Orthogonal
decomposition therefore transfers the operator identity and bound to
every local representation. At the other prime factors the Weyl
operator is unitary, because the projectors act as the identity there.
Tensor decomposition proves the global statement. No sign assumption
about normalized source-row Galois transport is used.

## Exact source constants for the two remaining rings

For both sources the FP dimensions are `d_i=a_i+b_i sqrt(5)`, with

`b=(0,2,2,4,4,4,4)`,

`a_3895=(1,5,5,10,8,8,9)`,

`a_5039=(1,5,5,8,8,10,9)`.

Their global dimension is `D=720+320 sqrt(5)`, with norm `6400`.
Let `w_FP` be the difference of the induced-unit constituents for the
FP character and its conjugate. It is a twist-fixed torus-character
vector for `chi_5`, of squared norm two. For any restriction row `v`,
define the integer

`u(v)=(2a-(9/2)b) dot v`.

Its coefficient vectors, in the original source order, are

* R7_5_3895: `(2,1,1,2,-2,-2,0)`;
* R7_5_5039: `(2,1,1,-2,-2,2,0)`.

Direct quadratic-field arithmetic gives

`(S w_FP)_Y = d(v_Y)/D - conjugate(d(v_Y))/conjugate(D)`

`= -u(v_Y) sqrt(5)/20 = -u(v_Y)/(4 sqrt(5))`.

Unitarity therefore gives the exact total weight

`sum_Y u(v_Y)^2 = 160`.

In every remaining character-compatible induced-unit frame, the seven
known values of `u` are one `2`, one `-2`, and five zeros. All seven
objects have twist one. Thus their contribution to the primary-order-one
weight is exactly eight.

Apply the prime-projection theorem at `ell=5`. In integral `u^2` units,
write `c` for the weight at exact five-primary twist order one. The
exact weights at five-primary orders one and five are

`c` and `4c`, with `8<=c<=32`.

The weight at five-primary orders at least twenty-five is `160-5c`.
Here `c` is an integer because it counts actual center simples with
integral `u^2` weights. No parity assertion for `c` is needed.

## Safe use with a finite relative-phase inventory

Over `F=Q(sqrt(5),sqrt(2),i)`, nonzero two-moment phase records come
from orders dividing eighty. Let `V_0` and `V_1` be the `u^2` weights
of visible nonzero records whose fifth-primary part is respectively
one and five. Then only the inequalities

`V_0<=c`, `V_1<=4c`, and `8<=c<=32`

follow without additional variables. In particular `V_0<=32`, with
at most twenty-four available beyond the known induced-unit rows,
and `V_1<=128`. One must **not** replace these inequalities by
`V_1=4V_0`: the genuine zero phase can hide high two-primary orders
with either fifth-primary part, as well as higher fifth-primary orders.

For an exact integer refinement, partition zero-phase weights into
`Z_0,Z_1,Z_high` by fifth-primary order one, five, or at least
twenty-five, and impose

`V_0+Z_0=c`, `V_1+Z_1=4c`, `Z_high=160-5c`.

The first two zero-phase classes have two-primary order at least
thirty-two and hence fixed-row multiplicity divisible by four; the
last has fixed-row multiplicity divisible by five. If both large
primary factors occur, the multiplicity is divisible by twenty.
This splitting is a necessary condition only.

## Reproduction

`verify_prime_projection.py` checks exact operator Gram identities at
moduli five, twenty-five, and one hundred twenty-five, using complete
unipotent/torus-character function spaces of dimensions two, six, and
ten. It verifies the squared singular spectrum `{0,1/5}`, the exact
factor-five norm ratio, both source dimension characters against all
products in the raw tensors, the coefficient formula above, source
hashes, and the induced-unit contribution eight in every stored
character-compatible frame. The receipt is
`prime_projection_certificate.json`. Normal and optimized execution
retain every check.
