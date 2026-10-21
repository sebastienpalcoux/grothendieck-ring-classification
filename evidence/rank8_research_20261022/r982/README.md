# R8_3_982 research continuation

The new substantive result is the complete module restriction in
[MODULE_TYPES.md](MODULE_TYPES.md): every indecomposable module category
has rank eight, with exactly three necessary based-module types (regular
and two mutually dual nonregular types). The preceding complete list of
31 possible algebra objects shrinks to eight. Every nonregular Morita
construction must realize the possible algebra `1+X5`; its existence is
not proved. The result applies to general categorification using the
independent Galois-to-pseudo-unitary theorem in `../pivotality/`.

`module_types.py` and `module_types.json` give a complete exact replay.
There is no numerical rejection or arbitrary module-rank cutoff. The
proof uses the forced nontrivial pointed C2 associator, paired induction
Gram matrices, determinant-one and determinant-four integral lattices,
parity, and the full source action. It does not assume a source braiding.

Two additional arithmetic attempts were completed over all 2,636
restriction vectors in the complete surviving center frame. These vectors
have 188 distinct dimensions in `Q(sqrt(2),sqrt(3))`:

* `dnumber_probe.py`: every possible central simple dimension passes the
  d-number test. For a monic minimal polynomial
  `x^n+a1*x^(n-1)+...+an`, the exact test is
  `an^i divides ai^n` for every i. The categorical input is the
  d-number theorem for simple dimensions in modular categories; see
  Ostrik, *On formal codegrees of fusion categories*,
  [arXiv:0810.3242](https://arxiv.org/abs/0810.3242).
* `semion_divisibility_probe.py`: every possible central simple dimension
  d passes both `D/d` algebraic integrality and
  `D^2/(2*d^2)` algebraic integrality, where
  `D=144+96*sqrt(2)+80*sqrt(3)+56*sqrt(6)` is the source global dimension.
  The first follows from integral modular formal codegrees
  `D^2/d^2`. The forced central semion splits the modular center as
  semion times its nondegenerate centralizer; the latter has dimension
  `D^2/2`, and every simple of the center has the same dimension as its
  centralizer factor. Its formal codegree gives the second condition.
  This factorization is a statement about the braided Drinfeld center,
  not about the unbraided source category. The decomposition theorem is
  in Drinfeld--Gelaki--Nikshych--Ostrik, *On braided fusion categories I*,
  [arXiv:0906.0620](https://arxiv.org/abs/0906.0620).

Neither arithmetic attempt deletes any vector. Their receipts record
that negative result, with exact minimal-polynomial arithmetic, bound
source/profile hashes, and positive and negative controls. They therefore
do not strengthen the categorical exclusion status.

All three scripts default to read-only verification against their JSON
receipts and support `--write` only for explicit regeneration. Normal and
`python -O` replay give identical conclusions. R8_3_982 remains unresolved
for unbraided general categorification; none of these files constructs
fusion or module associators.
