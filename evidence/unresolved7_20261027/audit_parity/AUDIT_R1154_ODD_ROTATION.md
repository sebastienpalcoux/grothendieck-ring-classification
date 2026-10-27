# Independent audit of the R8_3_1154 odd-rotation restriction

**Verdict: the new necessary restriction passes. R8_3_1154 remains unresolved.**
The restriction forces third Frobenius–Schur indicator 2 for every one of
the six noninvertible source simples. It excludes neither the ring nor
any of its three surviving center multiplicity patterns.

## 1. Scope and categorical prerequisites

The source tensor is bound to SHA256
`c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25`.
The inherited inputs are the positive spherical/Galois existence gate,
the forced nontrivial pointed C2 associator, the exhaustive three center
patterns 6971, 8766, 8772, and the packet twist/duality theorem. This note
does not claim a new independent proof of those earlier center theorems.

I checked the new argument against the categorical construction in
`evidence/unresolved10_20261027/r8_quartic/R1154_NOTES.md`.
Anomaly cancellation by a semion gives an actual regular pointed algebra
in C tensor Semion. Its dual is the equivariantization B=C^{C2} for the
coherent inner action, not merely an action on labels. Its canonical
forgetful tensor functor F has a pivotal structure compatible with the
positive spherical structures. The inherited unique necessary rank-ten
ring has a central sign object u with F(u)=1 and

    x*=ux,       F(x)=X4,       (vx)*=u(vx),       F(vx)=X5.

The hypothesis x*=ux is essential. A central order-two object alone
would not establish the doubling rule.

## 2. The odd-rotation argument is valid

For odd n, the two equivariance eigenspaces in Hom_C(1,F(x)^n) are
Hom_B(1,x^n) and Hom_B(1,(ux)^n). Tensoring the equivariance structure
by the sign character multiplies its n-fold tensor structure by -1.
Since F is pivotal, its maps on these morphism spaces intertwine the
pivotal rotation. Therefore

    nu_n(F(x)) = nu_n(x) + nu_n(ux) = 2 nu_n(x).

The second equality uses spherical duality and x*=ux. It is equality,
not complex conjugacy: Ng–Schauenburg, *Frobenius-Schur Indicators and
Exponents of Spherical Categories*, arXiv:math/0601012, Remark 4.2,
explicitly states nu_n(V*)=nu_n(V). Their Theorem 4.1 also proves it
from the center twist formula. The primary paper was checked directly:
https://arxiv.org/pdf/math/0601012.

For n=3, each of the two equivariant morphism spaces has dimension one
by the rank-ten fusion rules. The rotation has cube equal to identity.
Consequently nu_3(X4),nu_3(X5) belong to 2 times the set of cube roots of
unity. Their normalized traces to Q(sqrt(5)) belong to {-1,2}. The same
argument applies to vx and uvx. No unitarity assumption or unsupported
indicator preservation under an arbitrary tensor functor is used.

## 3. Exact arithmetic audit and exhaustive discrete coverage

I first rebuilt the height-three systems from the source tensor and
frozen center domain without invoking a solver. The 127 by 390 system
has nine exact separating certificates for the three value pairs
(-1,-1),(-1,2),(2,-1), across the three center patterns. Each satisfies

    A^T y >= 0,       b^T y < 0.

The retained value pair (2,2) has exact nonnegative rational witnesses
with support sizes 28, 28, 27. The first independent receipt is
`r1154_odd_rotation_independent_receipt.json`.

I then independently replayed the extended stage imposing the possible
third-rotation trace values {-1,1/2,2} on X1 and X6 while fixing the
values on X4 and X5 to 2. Duality handles X2, and the actual inner tensor
autoequivalence Ad(g) handles X7. The latter preserves the canonical
positive pivotal structure by uniqueness, so it preserves indicators.
I independently checked the tensor: duality is (1 2), conjugation by g
is (1 2)(6 7), and all six third vacuum multiplicities are two.
This second stage has 24 separating certificates and three rational
primal witnesses. The complete two-stage arithmetic therefore checks
33 infeasible discrete branches and six surviving necessary-system
witnesses. Exact completeness checks cover every listed value assignment
in every one of the three patterns. No tolerance is used to certify a
sign, equation, or infeasible branch.

The reproducible independent checker is
`verify_r1154_odd_rotation_independent.py`; its complete receipt is
`r1154_odd_rotation_full_independent_receipt.json`. It shares the exact
system builder, and independently checks the certificates and branch
coverage. The old exhaustive center domain and exponent prime-support
theorem remain explicit inherited inputs, rather than being inferred
from successful certificate arithmetic. I also inspected the finite
trace-type implementation: at height three over Q(sqrt(5)) with prime
support {2,3,5}, orders dividing 180 and the all-zero moment type cover
all possible normalized moment triples. Higher prime powers give zero
for all three rational Ramanujan and quadratic Gauss-sum terms. This
does not bound actual twist orders or require twists to lie in Q(sqrt(5)).

Each noninvertible source object has a two-dimensional third-rotation
space. For a two-dimensional representation of C3, normalized trace 2
forces both eigenvalues to be 1. Thus the actual third indicators are
2 and the third rotations are identities. This last implication uses
finite-order diagonalizability, not numerical closeness to 2.

## 4. Classification limit

Every surviving center pattern still has a nonnegative rational witness
for these necessary equations. Such a witness is neither a fusion
category nor proof that all pentagons or center data exist. The result
is a stronger necessary theorem for a hypothetical categorification;
the case remains unresolved.
