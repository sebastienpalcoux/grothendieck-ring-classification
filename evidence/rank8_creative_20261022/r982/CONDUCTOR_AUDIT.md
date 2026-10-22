# Independent audit of the saturated-conductor theorem

The argument in `../unified/SATURATED_CONDUCTOR.md` is valid after the
small-cell character convention described below. This audit does not rely
on the case-specific phase enumeration.

The primary input was checked directly against Sections 3–5 of Andrew
Schopieray, *The dimension block of a spherical fusion category*,
[arXiv:2609.35287v1](https://arxiv.org/html/2609.35287v1). Its local proof
supplies the big/small-cell compression and its norm. The equality-space
and conductor-descent arguments are additional deductions.

## Equality-space check

For a nontrivial local character alpha of conductor c, the compression is
off-diagonal relative to the big-cell line and the small-cell space.
The small-to-big map has rank one and norm c^(-1/2). Therefore its entire
maximal singular space is its adjoint range. The full equality space has
exactly two dimensions, spanned by the big-cell function and that adjoint
range. With the point action `(x,y) -> (b^(-1)x,by)` on functions, the
small-cell function is

    conjugate(alpha)(x) [y = 0 modulo c].

Using alpha(x) instead would interchange alpha and its conjugate. This
does not affect the real characters used by the rank-eight applications.
Both correct equality vectors depend only on `(x,y) modulo c`. The space
of functions with this property is invariant under the full group, so
every irreducible constituent supporting an equality vector factors
through reduction modulo c. For the trivial character, equality makes the
vector fixed by both opposite unipotent subgroups; these generate the full
local group. Its generated representation is therefore trivial.

In a tensor product, equality for the product norm forces support in the
tensor product of maximal singular spaces. This remains true for an
entangled vector. Thus the local result passes to every Chinese-remainder
factor, including primes absent from the conductor. The bound on the
generated subrepresentation, and hence `T^c S w = S w`, follows. There is
no missing prime factor or extra projective scalar: the canonical center
representation uses its actual twist matrix and has trivial anomaly.

## Independent exact finite controls

`conductor_local_audit.py` builds the permutation representation on primitive
columns directly, constructs the full unipotent-fixed torus eigenspace,
and averages the S-action explicitly. It does not use the proposed
two-vector formula to construct the equality space. Exact principal minors
check positivity of the norm defect; its full kernel is then computed.
Every kernel vector is checked for descent and the twist-power identity.

The six controls cover conductors 4, 3, 8 and 5 inside moduli 16, 27, 16
and 25; both the quadratic and nonreal order-four character modulo 5;
and the trivial character at modulus 9. All pass. The nonreal control also
checks the conjugation issue above. These finite computations support the
audit; the arbitrary-modulus assertion follows from the proof, not from
testing finitely many moduli.

```sh
python3 evidence/rank8_creative_20261022/r982/conductor_local_audit.py
python3 -O evidence/rank8_creative_20261022/r982/conductor_local_audit.py
```

This result alone is not an exclusion or a construction of R8_3_982.
