# Complete correlated semion-pair traces at height six

The central-orbit proof `QUARTIC_CENTRAL_ORBITS.md` shows that, in the
pseudo-unitary conjugate of a hypothetical R928 categorification, each
central simple in fixed restriction types 0 through 39 belongs to a
free G-orbit with twists theta and +i theta or theta and -i theta.
The unordered minus pair is the plus pair based at -i theta. Therefore
one can enumerate only pairs (theta,i theta).

The center twist prime support is {2,3}. With K=Q(sqrt2,sqrt3), the
complete height-six root trace bound is 288. If the order of theta does
not divide 288, one prime valuation exceeds the bound; multiplying by i
cannot remove such an excess (the only affected prime is 2, and the
excess is already beyond exponent five). All six relative traces of both
theta and i theta are then zero by the conductor/Möbius tail argument.
Otherwise theta=zeta_288^a for some integer a, and i theta=zeta_288^(a+72).

`semion_pair_traces.py` constructs Q[x]/Phi_288, degree96, and embeds K
using its quadratic Gauss sums. It averages every monomial over the
24-element subgroup fixing both positive square-root generators. For
all288 exponents and all powers1 through6 it adds the two exact relative
traces. Full polynomial-coordinate identities, the square/product rules
of the radical basis, and explicit integer overflow bounds are checked.
After adjoining the zero tail, exactly30 pair trace types occur. Both
possible semion signs are verified to give the same complete unordered
pair domain. The actual pair (1,i) gives (1,0,1,2,1,0).

These are sums of two simple-object moments. A cone variable for a pair
therefore contributes twice the restriction outer product, and its
multiplicity equation is sum(pair weights)=m_v/2. Weighted indicator,
rotation and STS coefficients multiply the saved trace sums directly;
they must not divide those sums by two. Each actual orbit gives one
nonnegative integer pair weight, and relaxing to rational weights is
necessary and safe. This is stronger than separately imposing even
multiplicity and zero moments2/6 on independent single-object trace
weights, because the odd moments now come from the same pair of roots.

The five distinct translated low objects retain their fixed trace tuples
(0,-1,0,1,0,-1). They are not among the paired restriction types.
The domains make no categorical existence claim.

```
python evidence/rank8_frontier_20261021/review/semion_pair_traces.py
python -O evidence/rank8_frontier_20261021/review/semion_pair_traces.py
```
