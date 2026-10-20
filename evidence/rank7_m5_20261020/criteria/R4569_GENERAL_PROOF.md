# General exclusion of R7_5_4569

This proof combines the full induced-unit compression bound with a complete
canonical signed quotient calculation. It excludes **arbitrary complex
fusion categories**, without assuming a pivotal structure.

1. The source Casimir has characteristic polynomial

   `(x-14)(x-3)(x-7)^3 (x²-2940x+17640)`.

   The quadratic field is Q(sqrt(15)), of fundamental discriminant 60.
   Thus the exact quadratic compression quantity is

   `60 (2940² - 4*17640) / 17640² = 81/49 > 1`.

   By `cor:quadratic-Casimir` of
   `manuscripts/rank7/papers/full_I1_compression.tex`, the ring has no
   spherical categorification. This step alone does not exclude a general
   fusion category.

2. Suppose a general categorification exists and take its canonical
   sphericalization. Every source simple is self-dual. Its two lifts have
   opposite nonzero spherical dimensions and are each self-dual. Choose
   for each source simple the lift of second Frobenius–Schur indicator +1,
   choosing the actual unit for the unit. In the signed quotient at the
   central sign object epsilon=-1, a coefficient T has the same parity
   as the source coefficient N and satisfies `-N <= T <= N`.

   Spherical trace and dual reversal identify precisely the oriented
   cyclic coefficient orbits implemented by `oriented_signed.problem`.
   The odd-square-channel theorem forces the opposite lift's multiplicity
   in every `X tensor X*` to be even; equivalently, `T = N mod 4` in
   every such channel. This is the proven indicator constraint of
   Liu–Palcoux–Ren–Vercleyen, arXiv:2203.06522v5, Theorem 3.9, not a
   pivotality conjecture concerning the original category.

3. Imposing all associativity identities on those finite integer domains
   has **exactly one solution**: the source tensor itself. The complete
   enumeration visits 2,285,932,869 nodes and finds one solution; both
   search completion and the solution are independently regenerated in
   replay. No assumption of commutativity is imposed by the enumerator.

4. Since the signed difference equals the unsigned source multiplicity
   in every channel, the opposite-lift multiplicity is zero in every
   product. The selected lifts therefore form a tensor subcategory, and
   forgetting gives a tensor equivalence with the original category.
   Its spherical structure transfers along that equivalence. This
   contradicts step 1.

The canonical sphericalization and tensor-section passage are as in
Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822, Section 5.1.
The signed quotient constraints and their implementation are inherited
from the repository's existing general-complex verifier.

## Exact verification

`signed_compression.py` recomputes the source Casimir and spherical
compression inequality, regenerates the full oriented signed enumeration,
validates the resulting signed table, and verifies its gauge equivalence
to the source. Its checks use explicit exceptions and run under `python -O`.

From the repository root:

```
python evidence/rank7_m5_20261020/criteria/signed_compression.py --replay
python -O evidence/rank7_m5_20261020/criteria/signed_compression.py --replay
```

The certificate is `R7_5_4569_signed_compression.json`; separate normal
and optimized replay receipts bind their result to its SHA-256 digest and
to the source tensor's digest. The stand-alone quadratic scanner still
correctly refuses to classify R4569 as a general exclusion: the complete
signed quotient step is essential.
