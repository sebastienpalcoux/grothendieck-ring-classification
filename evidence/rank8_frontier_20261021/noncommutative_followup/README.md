# General scope gates for R928 and R941

**Proposition.** Every complex fusion categorification of R8_3_928 or
R8_3_941 admits a spherical structure and has a pseudo-unitary Galois
conjugate. A pseudo-unitary noncategorification obstruction for either
ring therefore excludes every complex categorification. This is a scope
reduction; it neither constructs a category nor asserts unitarity.

The canonical certificate is `scope_gates.json`, replayed by
`verify_scope_gates.py`. It extends the unrestricted signed calculation in
`../review/verify_nc_gate_unrestricted.py` and adds an independent exact
central-idempotent audit in `independent_wedderburn.py`.

## Complete finite domain

For an arbitrary hypothetical category, choose dual-compatible lifts of
its simples in the canonical sphericalization. Quotienting by the sign
object epsilon=-1 gives signed coefficients T satisfying

    -N_ij^k <= T_ij^k <= N_ij^k,
    T_ij^k = N_ij^k modulo 2.

The checker enumerates **all** coefficients in this parity domain subject
to the unit, duality, cyclic trace symmetry, dual reversal, and all ordered
associativity equations. It imposes neither commutativity nor any
positive-indicator/modulo-four normalization. Every returned tensor is
validated exactly. Dual-compatible sign gauges only group equivalent
algebraic tests after the complete enumeration; they do not truncate it.

| Ring | Signed variables | Search nodes | Signed tensors | Gauge-original class | Excluded nongauge class |
|---|---:|---:|---:|---:|---:|
| R8_3_928 | 41 | 30,367 | 32 | 16 | 16 |
| R8_3_941 | 53 | 1,011,903 | 128 | 64 | 64 |

Both nongauge classes have four scalar characters in one irreducible orbit
and one two-dimensional matrix block. Their possible spherical dimension
delta has minimal polynomial

    t^4 - 320 t^3 + 18688 t^2 - 139264 t + 278528.

The ordinary ring has formal codegrees with polynomial

    t^4 - 576 t^3 + 11520 t^2 - 73728 t + 147456,

as well as matrix formal codegree4. The induced-unit theorem applied to
the sphericalization requires delta/f to be an algebraic integer for every
ordinary and signed formal codegree f: the factors of two in sphericalized
dimension and codegrees cancel. Already the displayed ordinary polynomial
contradicts this requirement. In any common field containing delta and f,
the norm of delta/f is a positive integer power of 278528/147456=17/9,
which is not an integer. This is the exact prime3 obstruction stored in
the receipt. Thus every possible signed tensor is gauge-original.

After switching the lifts by its recorded signs, the signed tensor equals
N itself. Positive and negative lift multiplicities sum to N and differ
by N, so every negative multiplicity vanishes. The selected lifts form a
spherical fusion subcategory, and forgetting them is a tensor equivalence
with the hypothetical original category. This proves sphericality.

## Complete noncommutative character accounting

The ordinary scalar algebra for either ring is the single irreducible
quartic orbit with polynomial

    t^4 - 64 t^3 + 320 t^2 - 512 t + 256.

The checker identifies its unique everywhere positive character as the
FP character. Consequently every spherical dimension character is a
Galois conjugate of the FP character. Galois conjugating the category and
its spherical structure to that embedding makes it pseudo-unitary.

The matrix block cannot supply an omitted dimension character: spherical
dimension is a one-dimensional algebra map. Nevertheless that block is
included in every formal-codegree obstruction. The regular Casimir has
eigenvalue2f on its four-dimensional summand, and the code uses f=4.

The independent audit constructs the five central idempotents directly
from all four scalar characters and the matrix trace character. It checks
all products, centrality, their sum1, and regular ranks(1,1,1,1,4). The
center has dimension5, so these idempotents are primitive over C. Thus the
full algebra is C^4 plus M2(C). All scalar multiplication identities and
all full-character orthogonality identities are checked exactly.

For each excluded signed representative, a separate rational audit
constructs the regular projectors onto the complete scalar submodule and
its complement. The scalar algebra is an irreducible separable quartic
field, so its four complex embeddings give all scalar maps. The
complementary algebra has dimension4 and center dimension1; its Casimir
is exactly8 times its identity, verifying matrix formal codegree4. This
argument does not assume the signed quartic field is Galois or positive.

## Sources and replay

The sphericalization and induction inputs are Ostrik, *Pivotal fusion
categories of rank3*, sections2.3 and5.1, Theorem2.13 and Corollary2.14,
https://arxiv.org/abs/1309.4822, together with the canonical construction of
Etingof--Nikshych--Ostrik, *On fusion categories*, Remark3.1,
https://arxiv.org/abs/math/0203060. The general signed argument is also
reviewed in `../review/NC_GALOIS_PU_REVIEW.md`.

```
python evidence/rank8_frontier_20261021/noncommutative_followup/verify_scope_gates.py
python -O evidence/rank8_frontier_20261021/noncommutative_followup/verify_scope_gates.py
```

The earlier normalized calculation in `general_galois_pu_gate.json` and
the initial unrestricted comparison in `gate_unrestricted.json` are
discovery receipts. `scope_gates.json` is the canonical independently
audited unrestricted certificate. The established `noncommutative/`
research package and all frozen baseline evidence remain unchanged.
