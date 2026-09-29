# Audit of the two imported general exclusions

Both supplied archives were unpacked without replacing project files. Their original sources, proofs, input tensors, and reports are retained in `sources/`. The checks below were carried out against the full tensors, not the archive titles or ring labels.

## Identity and exact replay

`import_tensor_matches.json` records a comparison with all 40 residual tensors, allowing all unit-preserving simultaneous basis permutations. The tensor in `R3582_General_Exclusion.zip` is exactly `R6_7_3582` in the same order. The tensor in `B13_General_Exclusion.zip` has multiplicity 13 and matches no tensor in the multiplicity-at-most-eight census.

The original R3582 verifier passed and its actual report is `r3582_replay.json`. The original B13 verifier passed under `python -O`; its actual report is `b13_replay_optimized.json`. These scripts certify the finite arithmetic and enumerations. The categorical and local-field inputs require the mathematical arguments in the source proofs; successful execution alone was not treated as certification of those inputs.

## R3582 mathematical audit

The proof's signed sphericalization is valid without assuming pivotality of the original category. Every lift of an original self-dual simple is self-dual, because the two lifts have opposite nonzero categorical dimensions and taking dual preserves dimension in the sphericalization. Duality is therefore the identity on its basis, so the ring is commutative. Its sign quotient has integral symmetric regular matrices with the asserted entry bounds and parity.

The dimension field contains all original formal codegrees: apply the central-induction theorem to characters pulled back from the original ring, whose sphericalization codegrees are twice the originals. The corresponding central dimensions are the original global dimension divided by the original formal codegree and belong to the signed dimension field. In this example the field therefore contains the ramified quadratic field Q(sqrt(226)). The checked mod-two algebra has two finite-field factors of rank two and one nonreduced factor of rank two. Idempotent lifting at 2 makes the finite-field factors unramified, so only the remaining quadratic factor can contain the required ramification. This forces the dimension field to be Q(sqrt(226)).

The coefficient-lattice argument then gives S divisible by 5, where S is the sum of squares of the sqrt(226) coefficients in the five nontrivial dimensions. The original Casimir trace 4540 gives S=5. Any reduction of an absolute structure coefficient by 2 loses at least 16 in that trace; the dimension contribution 4520 and four other codegrees greater than one leave less than 16. Thus all absolute coefficients are saturated. The signed associativity and orthogonality arguments in the source then force the FP dimension character or its Galois conjugate, up to permissible signs of the lifts. This establishes the claimed Galois-pseudounitary reduction.

The independent pseudounitary part uses complete bounded central-induction column searches, with bounds displayed in the source proof and checked in the replay. Its remaining twist-trace value is -18-6 sqrt(226), represented as 434 roots of unity. The all-orders Gauss-sum estimate is valid for the fundamental discriminant 904: the sqrt(226) coefficient of a normalized individual root-of-unity trace has absolute value at most 1/224. Taking traces in a common cyclotomic extension preserves this bound for roots of arbitrary order, so at least 1344 roots are necessary. There is no hidden cutoff on their orders.

For the revised project, the standalone imported arithmetic is retained as a provenance and regression check. The canonical release uses the new tensor-based ramified signed criterion and the existing generic pseudounitary induction criterion; no ring-label-specific exclusion dispatcher is needed.

## B13 mathematical audit and uniform extension

All categorical steps above apply again. The original codegree fields force the signed dimension field to be Q(sqrt(5),sqrt(149)): it contains that degree-four field and has degree at most six. The product integral basis is valid since the quadratic discriminants 5 and 149 are coprime. Orthogonality of the four conjugate dimension characters gives the exact trace lattice; formal-codegree divisibility supplies the integral element theta. Total positivity and the trace bound give the finite box printed in the proof. The d-number norm–trace test is a necessary condition, and the remaining pair of signed formal codegrees violates the quadratic d-number test.

The uniform implementation is `software/new_biquadratic_trace.py`. It derives its hypotheses and all search data directly from a rank-six tensor. It allows either sqrt(q) or sqrt(pq) in the FP codegree factor and includes the case of an even second quadratic discriminant. It also uses the necessary congruence of the entire signed Casimir characteristic polynomial modulo two. The full proof and the four new applications are in `biquadratic_trace_theorem.tex`.

The four resulting residual exclusions are R6_7_3813, R6_8_6940, R6_8_6973, and R6_8_6998. Canonical certificates are in `certificates/biquadratic_exclusions.json`. The optimized audit in `biquadratic_trace_audit.json` records all 40 initial residuals, 54 admitted model controls, simultaneous basis permutation controls, rejection of altered certificates and tensors, and exact reproduction of B13's 1129 totally positive candidates. An independent mathematical audit is also recorded in `research/round2_literature/biquadratic_trace_audit.md`.

The input label B13 is not itself counted as a census exclusion. The new counts use only the four exact tensors certified by the uniform criterion.
