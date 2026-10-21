# Independent review of joint Galois spectrum constraints

The theorem and `quadratic/joint_galois_balance.py` were reviewed separately
from their author. The necessary condition is accepted in the pseudo-unitary
scope of the distinguished modular character rows.

The central fusion matrices of the distinguished simples are commuting
integer matrices and are simultaneously diagonalized by the modular matrix.
For a central simple Z their complete eigenvalue tuple is
`(beta_E chi_E(FZ)/FPdim(Z))_E`. Keep the distinguished object labels E
fixed while applying a Galois automorphism to every coordinate. An integer
linear combination of the matrices can separate the finite union of all
these tuples and all their conjugates: the forbidden integer coefficient
vectors lie in finitely many proper hyperplanes. The characteristic
polynomial of that integer matrix then forces equal multiplicities on
every complete tuple orbit. This is stronger than coordinatewise orbit
balance and does not permute the labels of the integer matrices.

The implementation checks the complete automorphism group of the splitting
field. It includes all seven non-FP distinguished rows, counts every member
of a high restriction-duality orbit, and includes each fixed constituent
once. Missing simultaneous conjugates delete only nonnegative columns;
the finite iteration records every deleted column and checks that every
distinguished one-hot domain remains nonempty. The row construction counts
complete tuples, including multiplicities when several restrictions have
the same tuple. No numerical spectral approximation is used.

The producer's actual 64-simple center control passed fresh normal and
optimized replay. A second control, `review_joint_control.py`, imports no
producer joint-data, row, or support-filter function. It directly lists the
64 simples of `Z(Fib tensor Vec(C4))`, computes all seven eigenvalues from
the frozen character table, verifies simultaneous Galois multiplicities,
finds a separating integer linear combination, and computes its complete
degree-64 characteristic polynomial exactly. Every coefficient is an
integer. That control also passed normal and optimized replay.

This review establishes the necessary joint-spectrum condition and checks
its shared implementation. A target exclusion additionally requires its
complete restriction domain, exact separator or finite integer proof, and
a separate general-complex scope gate where applicable.
