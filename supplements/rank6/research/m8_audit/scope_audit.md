# Scope audit of the multiplicity-eight extension

The audit reviewed the proof interfaces in `proofs.py`, `signed.py`,
`oriented_signed.py`, `commutative_descent.py`, `weighted_induction.py`,
`signed_spherical_traces.py`, `spectral_induction.py`,
`character_induction.py`, `higher_traces.py`, `dimension_order.py`, and
the corresponding manuscript statements. It did not enumerate fusion rings.

## Necessary distinctions

* General categorifiability means existence of a complex fusion category,
  without a prescribed pivotal structure.
* The central-induction inequalities using positive simple dimensions are
  pseudo-unitary obstructions. They become general obstructions only after
  a proved reduction: weak integrality, two Frobenius--Perron dimension
  values, or complete sphericalization/character coverage.
* The two-dimension reduction gives a pseudo-unitary **Galois conjugate**.
  It does not say that the originally chosen categorical structure is
  pseudo-unitary. This is the formulation in Schopieray's published
  Lemma 3.1, DOI `10.1112/jlms.12789`. The first arXiv version states the
  stronger conclusion; use the published formulation.
* Lower-rank subring descent uses the stated classification range of its
  imported theorem. A larger counting census alone does not extend the
  classification range. Here those imported ranges are rank four through
  multiplicity 128 and rank five through multiplicity 17. This widens
  the cited theorem's range, while every subring actually tested in the
  rank-six source range has multiplicity at most eight. The change in
  the imported theorem bound therefore creates no new rank-six
  exclusion in the present ledger.

## Reusable criteria

The rank-two subring obstruction, formal-codegree d-number obstruction,
commutative cyclotomicity test, subcategory-dimension divisibility,
zero-spectrum witness, involution-module representation, and stated
small-dimension Morita obstructions have general scope under their
checked hypotheses. The commutative codegree routines must not be applied
to the regular Casimir spectrum of a noncommutative ring as though every
representation were one-dimensional. The weighted noncommutative routine
explicitly reconstructs the two one-dimensional blocks and the matrix
block and checks the Wedderburn characteristic-polynomial identity.

Complete signed enumeration is a necessary-condition search, not a
construction of a category. Its coverage depends on the normalization and
parity theorem imported from the preceding manuscripts. The oriented
routine uses cyclic symmetry and dual reflection, rather than imposing
commutativity on every signed quotient. The commutative routine is guarded
by a checked descent witness.

The dimension-order criterion is stronger than maximal-order algebraic
integrality and uses an exact lattice in the actual span of the simple
dimensions. On a single character component it excludes that component
only; every possible component and signed branch must be covered before
declaring general nonexistence.

The signed central-trace implementation uses actual signed dimensions,
integer restriction multiplicities, finite cyclic-operator bounds, and
both second-indicator signs. It does not reuse the positive low-mass
inequalities or the absolute-value dimension-orbit rule. Its Galois balance
separated by relative twist-trace type relies on the stated rational or
real-quadratic trace-field hypothesis.

## Construction scope

The mixed central-boson quotient supplies categorical existence before
matching tensors. The equal-phase fixed-point construction is conditional
on specified coherent local fermion data; associativity of its parameterized
integer tensor is not itself an existence proof. The registered parameters
are the cited Ising and half-E6 inputs only.

The relative-Fibonacci-center construction similarly begins with an
existing unitary parent category. A diagonal-one Gram pivot forces one
restriction column; reaching zero then exhausts the restriction matrix.
Uniqueness of the exact linear fusion equations identifies the ring of
that already-existing category. Failure of a pivot or uniqueness check is
inconclusive, not an exclusion.

## Literature cautions for new work

Schopieray's published Proposition 3.8 and Corollary 3.10 are printed for
spherical categories, but their displayed proof uses positivity of induced
simple dimensions and dimension one for the invertible input. Any new
automation based on those triangle-inequality arguments should be restricted
to the positive spherical structure unless a separate signed proof is
provided. These statements should not be imported mechanically into a
non-positive sphericalization branch.

The primary sources inspected for scope were:

* https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789
  (published Lemma 3.1 and the proofs in Section 3.2);
* https://arxiv.org/pdf/1309.4822 (Ostrik, Theorem 2.13,
  Corollary 2.14, and sphericalization in Section 5.1);
* https://arxiv.org/pdf/0809.3031 (Etingof--Nikshych--Ostrik,
  weakly group-theoretical and solvable categories, including dimension 60).

No counterexample to the audited, guarded proof interfaces was identified.
This is a scope review, not a replacement for their exact certificate
checks or a claim of a complete audit of every imported theorem.
