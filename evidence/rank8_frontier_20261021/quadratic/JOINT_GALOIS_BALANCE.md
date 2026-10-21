# Joint Galois constraints for distinguished central fusion matrices

Let the source fusion category be pseudo-unitary. For each distinguished
simple object A_E in its induction of the tensor unit, the fusion matrix
N_(A_E) is an integer matrix. These matrices commute because they belong
to the braided Drinfeld center, and its modular S matrix simultaneously
diagonalizes them. The source category itself need not be braided.

For a central simple with restriction vector v, collect the eigenvalues

    Lambda(v) = (beta_E chi_E(v) / (m_E dim(v)))_(E != FP),

where beta_E is the FP dimension of A_E and m_E is the degree of the
irreducible source-ring representation affording the full matrix
character chi_E. The commutative implementation in
`joint_galois_balance.py` has m_E=1 throughout. Noncommutative applications
must retain the degree factor (or supply the already normalized character).

Every entry lies in the verified Galois character splitting field L. The
multiset of these complete tuples, with central-simple multiplicities,
is invariant under every automorphism of L over Q. To prove this, take
the finite union of all candidate tuples and their conjugates. There
exists an integer linear form separating all distinct tuples in this
union: each forbidden coincidence is a proper rational hyperplane, and
finitely many such hyperplanes cannot cover Z^m. Apply this form to the
commuting integral matrices. The resulting matrix is integral and has
the selected linear forms of the tuples as its eigenvalues. Its integer
characteristic polynomial has equal multiplicities on Galois conjugates.
Separation converts that statement into equality of complete-tuple
multiplicities. The labels E of the matrices remain fixed throughout.

This strengthens separate eigenvalue-multiplicity equations: the same
field automorphism acts simultaneously on every coordinate of a tuple.
For each complete tuple orbit, equate every multiplicity to one reference.
Fixed constituents contribute constants; low choices and high duality
orbits contribute their actual integer simple counts. All conjugates are
included even when they do not occur in any candidate column.

In particular, if a present tuple has a conjugate absent from the entire
remaining support, every nonnegative variable containing that tuple must
vanish. If it occurs in a fixed constituent, there is a necessary-domain
contradiction. Repeating this deletion to closure is exact. It is a
support filter, not a construction of an associator or a central simple.

The isolated `joint_galois_balance.py` implements both the support filter
and additive equations. Its positive control uses the actual 64-simple
center of Fibonacci tensor Vec(C4), checks complete joint-orbit counts,
and verifies that every actual low and high support survives. The full
automorphism enumeration and field arithmetic reuse the independently
controlled exact character adapters. The control passes both normally
and with Python assertions disabled.
