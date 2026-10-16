# A unified character-parity obstruction for the Fibonacci pair

## Theorem

Neither census ring `R8_2_190` nor `R8_2_489` is the Grothendieck ring of a complex fusion category.

This is a theoretical obstruction. The accompanying exact replay binds the two census tensors to the presentation and checks the field identities. No low-column enumeration, numerical feasibility result, or assumed braiding on the hypothetical category is used.

## Categorical input and scope

The independently audited theorem `evidence/unified_20261016/rank8/FIB_PAIR_THEORETICAL_GALOIS_PU.md` proves that any categorification of either ring has a spherical structure and a pseudo-unitary Galois conjugate. Consequently it suffices to exclude pseudo-unitary categorifications. This reduction is essential: positivity below refers to the canonical spherical structure of that Galois conjugate.

For a commutative spherical fusion ring and its one-dimensional character `chi`, write `f_chi` for its formal codegree and `Z_chi` for the associated simple summand of `I(1)` in the Drinfeld center. Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822, Example 2.9, the character-level definition immediately preceding Theorem 2.13, and Theorem 2.13 give

- `dim Z_chi = D/f_chi = beta_chi`;
- `[F Z_chi:1]=[I(1):Z_chi]=1`;
- `S(Z_chi,W)=beta_chi chi(FW)` for the unnormalized modular matrix.

Thus symmetry of the modular matrix gives the character reciprocity identity

`beta_chi chi(F Z_psi) = beta_psi psi(F Z_chi)`.

Primary source: https://arxiv.org/pdf/1309.4822, printed pages 5–6, especially Example 2.9 and Theorem 2.13. This identity holds for the actual character labels, including repeated formal codegrees; no arbitrary identification of equal-dimensional central simples is being made.

## The common ring presentation

Let `epsilon=1` for `R8_2_190` and `epsilon=0` for `R8_2_489`. Both have the commutative presentation

`g^2=1, tau^2=1+tau, x^2=g^epsilon+tau(x+gx)`,

with basis `1,g,tau,g tau,x,gx,y,gy`, where `y=tau x`. The involution is `g*=g`, `tau*=tau`, `x*=g^epsilon x`.

Put `phi=(1+sqrt(5))/2` and `d=phi+sqrt(phi+2)`. The positive dimensions are `1,1,phi,phi,d,d,phi d,phi d`, and

`D=2(phi+2)(1+d^2)`, `d^2=1+2 phi d`.

The four numbers `1,phi,d,phi d` are linearly independent over the rationals. Indeed, the quadratic extension adjoining `d` to `Q(phi)` adjoins `sqrt(phi+2)`. If `phi+2` were a square in `Q(phi)`, its rational norm `5` would be a rational square, which it is not.

The exact monomial-basis order used by the replay is `g^i tau^j x^k`, lexicographically ordered over `(i,j,k) in {0,1}^3`. Its maps to the census basis are:

| Ring | epsilon | Model-to-census map |
|---|---:|---|
| R8_2_190 | 1 | `[0,1,5,3,7,2,6,4]` |
| R8_2_489 | 0 | `[0,3,7,4,1,6,2,5]` |

## Three characters and their central dimensions

Take `omega=1` if `epsilon=0`, and `omega=i` if `epsilon=1`. Define two characters by

`chi_±(g)=-1, chi_±(tau)=phi, chi_±(x)=±omega`.

They have the same formal codegree

`f_±=4(phi+2)`

and therefore the same central dimension

`beta_±=D/f_±=1+phi d`.

For `epsilon=1`, the calculation uses `chi(b)chi(b*)`, rather than `chi(b)^2`: since `x*=gx`, the contribution from `x` is `-omega^2=1`.

Define a third character `psi` by

`psi(g)=1, psi(tau)=1-phi, psi(x)=(phi-1)d-phi`.

The latter value satisfies `z^2=1+2(1-phi)z`. Its formal codegree is `f_psi=2(3-phi)(1+z^2)`, and exact reduction using `phi^2=phi+1` and `d^2=1+2 phi d` yields

`beta_psi=D/f_psi=(1+phi)+(2+3phi)d`.

## The parity contradiction

Write `Z_+,Z_-,B` for the three central simples indexed by `chi_+,chi_-,psi`.

Since each restriction has unit multiplicity one and nonnegative integral multiplicities, rational linear independence of `1,phi,d,phi d` and `beta_±=1+phi d` imply

`FZ_± in {1+y, 1+gy}`.

Because `psi(g)=1`, the value `psi(FZ_±)=1+psi(y)` is independent of either choice. Applying reciprocity to `(B,Z_+)` and `(B,Z_-)` and using `beta_+=beta_-` gives

`chi_+(FB)=chi_-(FB)`.

On the other hand, the dimension `beta_psi` forces the sum of the multiplicities of `x,gx` in `FB` to be `2`, and that of `y,gy` to be `3`. Let their respective multiplicity differences be the integers `Delta_x,Delta_y`. Subtracting the character values gives

`0=chi_+(FB)-chi_-(FB)=2 omega(Delta_x+phi Delta_y)`.

Irrationality of `phi` forces `Delta_x=Delta_y=0`. But two equal integer multiplicities cannot sum to `3`. This contradiction excludes both pseudo-unitary categories, and the previously proved spherical/Galois reduction excludes all complex categorifications.

## Replay scope

`verify_fib_character_parity.py` checks the full 512 tensor entries for each census case, duality, all three character homomorphisms and formal codegrees, both central-dimension identities, and the resulting odd-pair contradiction using integer arithmetic only. The proof above supplies the categorical implications. The proof does not depend on the exploratory list of 178 low induction blocks.
