# Galois multiplicity constraints on distinguished central spectra

Let C be pseudo-unitary with commutative Grothendieck ring R. For a
distinguished simple A_E in I(1), write beta_E = D/f_E, and let v_Z be
the restriction vector of a simple object Z in Z(C). Its eigenvalue in
the integral fusion matrix N_(A_E) is

    lambda_E(v_Z) = beta_E chi_E(v_Z) / dim(v_Z).

The characteristic polynomial of N_(A_E) lies in Z[x]. Consequently every
Galois conjugate of an eigenvalue has the same multiplicity. If a normal
number field L contains the complete character table and FP dimensions,
all these eigenvalues lie in L, so the complete finite automorphism group
of L supplies every required conjugate. The object A_E stays fixed when
one forms this rational-spectrum condition.

For each E and each orbit of candidate eigenvalues, choose one reference
lambda. Each other value mu gives an integer linear equation equating
the number of central simples with eigenvalue lambda to the number with
eigenvalue mu. A low variable contributes one chosen distinguished
restriction vector. A high variable counts a complete restriction-duality
orbit and contributes the eigenvalue count for every member of that orbit.
The already fixed central unit contributes to the right-hand side. In a
fixed-frame application, every fixed low restriction contributes there.
Values missing from the candidate domain still occur in the orbit and
give valid equations with zero variable coefficients. Fusion-coefficient
auxiliary variables have zero coefficients in these equations.

These counts are integers because they count actual central simples.
No integrality is imposed on the averaged twist-trace variables used in
the earlier rational cones. No phase-field enlargement is needed.

`atomic_galois_balance.py` checks the full field polynomial splits in its
own degree-d field, verifies every image of the primitive generator and
all basis products, and checks these images permute the complete root set.
It then constructs the exact additive multiplicity rows. The two target
fields are Q(sqrt(5),i) for R65 and Q(sqrt(2),zeta_7+zeta_7^(-1)) for R3472.

The independent positive control uses the actual 64-simple center of
Fib tensor Vec(C4). Its restriction multiplicities are four copies of
1_g, eight of tau_g, and four of (1+tau)_g for each g in C4. All generated
Galois equations hold. Independently multiplying the 64 linear eigenvalue
factors for each of the eight distinguished objects gives an integer
characteristic polynomial; genuinely nonreal eigenvalues occur. The
no-argument replay passes normally and with Python assertions disabled.

The isolated target driver `atomic_integer_cubic.py` appends these rows to
the shared exact integer Gram, full-field S-symmetry, distinguished-duality,
and cubic Verlinde system. Every unknown has a finite necessary
nonnegative bound. A modular covector which annihilates every integer
column but not the right-hand side proves the necessary integer system
impossible. Conversely, consistency modulo 2 and 3 alone is only that
scoped statement: it proves neither integer-lattice membership nor a
nonnegative integer solution, and it does not construct a category.
