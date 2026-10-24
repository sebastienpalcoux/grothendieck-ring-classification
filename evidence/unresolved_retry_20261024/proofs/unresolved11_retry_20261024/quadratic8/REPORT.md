# Fresh quadratic rank-eight retry

## R8_3_1768

There is substantial new categorical progress: an actual complex fusion
category with the required twisted `GH(C6,m=2)` precursor has now been
constructed from Radchenko--Wheeler's specific near-group realization on
`C12 x C12`. Its pointed associator is exactly class3 in `H^3(C6,C*)`.

The earlier cyclic-C144 carry anomaly and the unsuccessful search for a
nondegenerate elementary-C2^2 subgroup do not obstruct this construction.
The new subgroup has order24, type `C12 x C2`, and a six-element radical;
its twisted group algebra is six copies of `M2(C)`. The proof explicitly
constructs the crossed-product endomorphisms, primitive projectors,
fusion rules, rigidity, and associator invariant.

See `TWISTED_GH6_CONSTRUCTION.md`, `verify_twisted_gh6.py`, and
`twisted_gh6_verified.json`. The verifier passed all finite metric,
cocycle, projector-rank and fusion-tensor checks. The actual categorical
existence additionally uses RW's proved reconstruction, as stated in the
proof; numerical data are not substituted for that premise.

The missing step is now concrete: construct a connected separable algebra
on `1+sigma` in a suitable realized precursor and identify its Morita dual
with the rank-eight ring. Neither a primitive projector on the image of
the near-group rho nor the existing nonnegative based module completions
automatically supply such an algebra. Therefore R8_3_1768 remains
unresolved at the time of this note.

## R8_3_1154

The fresh quantum-group/conformal-embedding comparisons did not yet yield
an actual model or a categorical obstruction. In particular the new
SU4_6 construction relevant to R10_1_189 has a different global dimension;
its existence alone gives no R1154 algebra. The previously excluded
index-five SU3_7 x Fib route must not be revived without a different
categorical operation.

There are new **uniform route obstructions**: no connected étale full
module construction from any of SU4_6, SU5_5, SU6_4, SU3_7 x Fib, or the
new actual E14, tensored with an arbitrary pointed category, can have
the R1154 global dimension. The proof combines local-module dimension
integrality with positive field coordinates and the bound on rational
connected separable algebras. See
`R1154_POINTED_EXTENSION_OBSTRUCTIONS.md`; the complete exact type-A
dimension sweep and its verifier also accompany this note. This rules
out whole families of fresh quantum routes, not the census ring.

A modular-data convention issue was flagged separately: with positive
double-braiding S and T equal to the positive twist, the packet relation
uses `s T s=T^-1 conjugate(s) T^-1` (central charge one), whereas the old
packet presentation uses the relation without conjugation. Adopting
T=theta^-1, or conjugating the displayed S packet, reconciles the signs.
The integer-real Verlinde matrices are unchanged under simultaneous
complex conjugation of the packet columns. This is a presentation audit
flag, not an exclusion and not a reason to promote the ring.

## Literature refinement checked

Schopieray, *The dimension block of a spherical fusion category*,
arXiv:2609.35287v1, Theorem5.1, applies to spherical categories without a
unitarity assumption. For these quadratic dimension fields e=1. Its
quadratic-character inequality reads
`|1/D-1/D'| <= 1/sqrt(discriminant)`.

R1154 satisfies it strictly: the left side is `2sqrt(5)/15`.
R1768 attains equality: the left side is `1/sqrt(37)`.
The latter agrees with the already established saturated prime37 sector;
it is not a new exclusion.

Sources:
https://arxiv.org/html/2609.21892v1
https://arxiv.org/pdf/1512.04288
https://ems.press/content/serial-article-files/36923
https://arxiv.org/html/2609.35287

No online files were edited by this retry.
