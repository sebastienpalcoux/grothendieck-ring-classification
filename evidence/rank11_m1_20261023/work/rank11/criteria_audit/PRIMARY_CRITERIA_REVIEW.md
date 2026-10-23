# Exact primary and Schur criteria for the two dimension-32 residuals

Both R11_1_104 and R11_1_153 pass the entire primary-n criterion family,
including the noncommutative Schur-product test. This is a necessary-condition
pass and supplies no categorification.

Huang–Liu–Palcoux–Wu, arXiv:2210.00792v1, Theorem 3.9 identifies positivity of
the full primary-3 matrix with positivity of every full primary-n matrix.
Proposition 3.13 then implies the Schur-product criterion. The localized and
reduced twisted matrices in Theorems 4.1 and 5.1 arise by unitary conjugation
and compression of these positive matrices, so those entire families pass too.
These implications apply to noncommutative fusion rings. They avoid an extra
numerical search over irreducible *-representations or twisting unitaries.

For the source tensors here, write

    q = Σ_i (2/d_i) b_i⊗b_i⊗b_i ∈ R⊗R⊗R.

The regular matrix of q is twice the primary-3 matrix. The exact dimension
character takes only values one and two, so all coefficients of q are integers.
Its star invariance makes the regular matrix real symmetric.

The independent verifier `verify_primary3_tensor_algebra.py` multiplies q
directly inside the tensor algebra, using Python integers and the source
structure constants. It does not import the producer, construct Kronecker
matrices, call a numerical eigensolver, or use NumPy/SciPy. For both inputs it
verifies the identity

    q(q−8)(q−16)(q−64)=0.

Thus every eigenvalue belongs to {0,8,16,64}, proving positivity. As an extra
exact check, the traces of q^0,q^1,q^2,q^3 determine the multiplicities:

    0:1147, 8:84, 16:84, 64:16.

This agrees with the producer's independent sparse-matrix polynomial method.
Both ordinary and optimized-Python executions passed. The complete source
hashes and trace values are in `primary3_independent.json`.

The unitarity-based exclusion criteria would have general complex scope for
these inputs: dimension32 implies solvability by ENO arXiv:0809.3031,
Theorem1.6, and weakly group-theoretical categories admit unitary structures
by Galindo–Hong–Rowell arXiv:1105.5048, Theorem5.20. Here the criteria pass,
so that scope upgrade creates no exclusion.
