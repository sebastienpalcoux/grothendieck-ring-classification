# Exact finite-group compression audit for R6_8_1660

This is a necessary-condition calculation. It does not construct modular
data or a fusion category, and does not exclude any of the three retained
low branches.

The preceding all-primary-index Minkowski tests concern the original fusion
tensor and do not imply the finite modular representation cone. The older
`m8_actual48/exploration_summary.json` separately records a complete
532-irreducible / 504-signed-spectrum cone search, with no new exact
exclusions. Its finite-group tables are in `m8_modrep`.

## Complete character data

`finite_spectra48.py` reconstructs SL(2,Z/16) and SL(2,Z/3), their conjugacy
classes and class algebras. Its exact replay verifies class-algebra
homomorphisms, character orthogonality, positive integral degrees, the
degree-square sum, T spectra and central signs. The CRT T exponent is
`3*x + 16*y (mod 48)`, giving 532 tensor-product irreducibles. The cone's
central-sign inequalities correctly bound the trace of duality on each
twist eigenspace. The Ising-complement code correctly subtracts the known
nine-dimensional subrepresentation from both ordinary and signed spectra.

## Additional constraint from the exact twist-one theorem

The new theorem identifies the entire T-fixed space with the six simple
constituents of I(1). Consequently the compression `P S P` is the known
six-by-six low S block, not just an unspecified matrix on a space of
dimension six.

For an irreducible representation of SL(2,Z/m), let
`P = (1/m) sum_j rho(T)^j`. Its compressed operator has

`trace(P S P) = (1/m) sum_j character(T^j S)`

and

`trace((P S P)^2) = (1/m^2) sum_{j,k} character(T^j S T^k S)`.

All nonzero U-fixed dimensions in the local tables are one or two for
modulus 16, and one for modulus 3. The displayed traces therefore determine
their characteristic polynomials exactly. CRT tensors the compressions.
The full twist-one space is self-dual, so only central-sign-plus summands
with nonzero U-fixed space can contribute.

`compressed_spectra.py` performs these calculations over Q(zeta_48),
constructs each six-by-six low S block from the source fusion characters
and induction columns, and compares exact characteristic polynomials. All
three branches have exactly one decomposition into permitted spectrum
types. Their spectra are:

- low branch 0: `1, 1, -1/2, 0, -sqrt(3)/6, -sqrt(6)/12`;
- either low branch 1: `1, -1/2, 0, 0, -sqrt(3)/6, -sqrt(6)/12`.

The scalar 1 comes only from irreducible pair `(3,2)`; scalar -1/2 only
from `(9,2)`; scalar -sqrt(3)/6 from `(33,4)` or `(36,5)`; scalar
-sqrt(6)/12 from `(54,4)` or `(61,5)`. Pair indices use the frozen ordered
local tables. Zero has 24 eligible pairs. No two-dimensional compression
block is eligible. The JSON records every exact coefficient and pair.

## Independent torus audit

On I(1), the diagonal torus acts by the unsigned Galois permutation of
fusion characters: the normalized row is `psi_E/f_E`, and its Galois
conjugate is exactly the row of the conjugate character. The four
dimension characters form the regular biquadratic orbit. The two
formal-codegree-4 characters are rational:

`[1,-1,1,-1,0,0]`, `[1,-1,-1,1,0,0]`.

Thus the T-fixed torus multiplicities for discriminants `1,8,12,24` are
`[3,1,1,1]`. The independently prepared `../modrep/torus_spectra.py` uses
the correct trace `(1/m) sum_j character(h_b T^j)` and torus Fourier
normalization. These constraints and the compression multiplicities can
be added to the full cone. They must be attached to individual irreducible
pairs, or a refined merge key: equal signed T spectra alone need not
imply equal torus/compression data.

No publication or classification status is changed by this audit.

## Exact integer witness for the strengthened system

The subsequent integer witness in `../modrep/exact_integer_witness.json`
uses low branch 0, labelling `[0,5,4,1,3,2]`, and profile 10. This profile
belongs to the retained packet-Gram survivor list. Independent replay
checked every one of its 1,536 integer equations, all 1,447 variable
bounds, the zero high-twist-one multiplicities, the torus weights,
compressed-spectrum multiplicities, and the forced Ising subrepresentation.
The witness has center rank 37. Its active finite-group irreducibles are

`(0,1), (2,1), (2,2), 2(3,2), (9,2), (22,2), (26,2), (36,5), (57,2), (61,5)`.

The audit receipt is `witness_audit.json`. This is an exact passing witness
for the strengthened necessary system. It shows that these constraints
cannot exclude R6_8_1660. It does not supply a full S matrix, modular data,
associator, or fusion category.
