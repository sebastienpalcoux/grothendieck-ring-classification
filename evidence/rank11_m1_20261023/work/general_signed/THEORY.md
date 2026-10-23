# Oriented signed sphericalization audit

The computation is an exact necessary-condition argument, not a numerical
pentagon search. It applies to multiplicity-one fusion rings. No commutativity
of a signed quotient is assumed.

## Necessary signed tables

Sphericalize a hypothetical complex fusion category and choose a lift of each
simple, with the unit fixed and dual lifts compatible. The quotient of its
Grothendieck ring by the central sign object plus one has structure constants
T[i,j,k] in {-N[i,j,k],N[i,j,k]}. Its unit coefficients are delta(j,i*).
The signed constants obey associativity, cyclic trace symmetry and dual
reversal. These identities identify the trace triple (i,j,k*) only under
cyclic rotation and (a,b,c) -> (c*,b*,a*). In particular, arbitrary permutation
of indices is never imposed.

Changing lifts multiplies T[i,j,k] by s_i s_j s_k, where s_0=1 and s_i=s_i*.
The audit fixes an independent set of gauge coordinates; the recorded gauge
matrix proves this normalization reaches every orbit.

Each nonzero signed coefficient is (-1)^x for a binary variable x. Every
associativity identity becomes a Laurent sign polynomial sum c_m (-1)^(m.x)=0.
If one coefficient has absolute value equal to the sum of the absolute values
of all other coefficients, and the original positive assignment satisfies
the identity, equality in the triangle inequality forces all involved sign
monomials to agree. This yields exact linear equations over F_2. The verifier
reconstructs each full associativity equation and checks every deduction.
After gauge fixing, at most two binary variables remain for these 69 rings;
every remaining assignment is enumerated and directly checked.

## Complete scalar-character checks

For a signed associative table with oriented reciprocity, the regular matrices
satisfy N_i^*=N_{i*}; the finite-dimensional complex algebra is semisimple.
The common kernel of all commutators is precisely the direct sum of its
one-dimensional representations. The discovery code restricts multiplication
to this subspace and finds a separating element. The independent checker does
not trust that construction: it verifies every proposed character directly
as a ring homomorphism, checks its separating generator and irreducible
field polynomial, and proves completeness by counting degrees against the
commutator-kernel dimension.

A spherical dimension character must be nonzero on every simple and equal
on dual pairs. Let delta=sum d_i d_i* and K=Q(d_i). For every simple algebra
representation E, delta/f_E must be an algebraic integer and f_E must lie in
K. The former gives the necessary normalized norm-valuation inequalities;
the latter gives degree and exact finite-prime splitting obstructions. In a
sphericalization, the formal codegrees are doubled and its dimension is 2delta,
so the same constraints apply to the original and signed summands.

A regular Casimir eigenvalue is dim(E) f_E, not always f_E. Field tests may
use either because the multiplier is rational. Norm tests in the original
character audit use actual f_E: the one-dimensional portion is extracted
first; the remaining Wedderburn blocks have size 2 (deficit 4 or 8) or size 3
(deficit 9). Their eigenvalues are divided by that exact block size.

## Categorical implication

If every signed table arising from a sphericalization is a sign gauge of N,
choose those lifts. Their products contain only chosen lifts, so they span a
fusion subcategory of the sphericalization. Forgetting the lifts is a tensor
equivalence onto the original category. Consequently, the original category
admits a spherical structure.

For each remaining original spherical dimension character, the audit finds a
Galois embedding and a tensor sign character s_i such that s_i d_i is strictly
positive. Twisting the spherical pivotal structure by these signs makes the
dimension vector positive, hence equal to FPdim. Thus a Galois conjugate of
the hypothetical category is pseudo-unitary. This reduction is not an
existence result.

## Recorded scope and results

- 69 nonselfdual input rings: every categorically admissible oriented signed
  quotient is gauge-original. 52 are already gauge-original as associative
  signed tables. All alternative categorical branches for the other 17 are
  excluded.
- 77 original-ring dimension inventories (the same 69 plus eight selfdual
  targets): every surviving spherical character admits the certified
  pseudo-unitary reduction.
- All spherical dimension characters are excluded for R9_1_41, R9_1_133,
  R10_1_20, R10_1_59, R10_1_70, R10_1_88, R10_1_99, R10_1_102, R10_1_119,
  R10_1_123, R10_1_149, R10_1_151, R10_1_156, R10_1_181, R10_1_190.
  Thirteen of these are covered by this nonselfdual signed audit; R9_1_41 and
  R10_1_20 require the separate selfdual signed audit.

## Files and replay

- oriented.py: exact oriented sign problem and GF(2) discovery.
- branches.py: complete normalized enumeration and signed character checks.
- ledger.json: complete 69-ring signed receipts.
- verify.py: independent deduction and finite-domain replay.
- original_characters.py / original_characters.json: all 77 original scalar
  character inventories and exact reductions.
- verify_characters.py: independent direct homomorphism, completeness,
  codegree, norm, field and positive-sign verification.

Run from the workspace root:

    python -O work/general_signed/verify.py
    python -O work/general_signed/verify_characters.py

The code imports exact.py and arithmetic.py from work/obstructions. The source
input files are the two uploaded gzipped multiplication tables, retained under
inputs/. The stored JSON identities bind every result to its complete tensor.
