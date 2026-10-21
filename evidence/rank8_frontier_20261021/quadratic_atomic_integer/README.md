# Exact integer center campaigns for R1768 and R1795

The canonical final replay is `python final_verify.py` from this directory
(or the corresponding repository-relative path). It reconstructs both source
tensors and every retained restriction domain. Default replay uses exact
arithmetic only; numerical proposals are confined to explicit `--write`
discovery. `python -O final_verify.py` performs the same mathematical checks.

The final system combines complete character-labelled low choices, high
restriction-duality orbit counts, integer Gram equations, full distinguished
S symmetry, all 196 nonunit cubic Verlinde coefficients, individual and
joint Galois spectral multiplicity equalities, exact FP bounds on fusion
coefficients, and source-unit product norm/AM–GM constraints. It first applies
the proved integral-center filter and complete missing-conjugate support
filters. All variables, including fusion coefficients and inequality slacks,
have finite nonnegative integer bounds.

Exact interval/gcd propagation, bounded full-column linear separators,
modulo-two and modulo-three consistency, and signed integer column-lattice
membership are distinct tests. An affirmative numerical proposal is recorded
only after every integer coordinate, original equation and bound passes an
exact check. A failed or interrupted numerical search never supplies an
exclusion. Signed lattice membership does not establish bounded integer
feasibility, and a bounded integer solution of these necessary equations
would still not construct a category. The categorical scope is
pseudo-unitary until a separate general-complex reduction is supplied.

The final receipts are `R8_3_1768_final.json` and `R8_3_1795_final.json`.
Their top-level `status` gives the exact terminal conclusion, with source
hashes, complete domain reports and replayable certificates beneath it.
Earlier individual and joint stages are retained as historical records.
The R1795 historical HNF searches were superseded before a result and make
no lattice claim; only the final route is registered as the campaign replay.
R1768's earlier individual and joint signed-lattice memberships are recorded
separately and are not categorical existence claims.

The final R1795 HNF proposal orders sparse auxiliary generators first and
has a 120-second wall-clock limit and a 256-MiB additional virtual-allocation
limit. A stopped worker records `no_exact_lattice_conclusion`; this is an
explicit limitation, not lattice membership or nonmembership. The bounded
integer proposal has a 180-second solver limit and a 210-second wall-clock
limit. Default exact replay reconstructs all completed mathematical tests
and checks any positive witness; it does not repeat unsuccessful searches.

| Ring | Final exact results | Remaining limitation |
| --- | --- | --- |
| R8_3_1768 | Box and mod-2/mod-3 consistency; signed integer lattice membership of rank 268 | No bounded nonnegative integer witness was found within the stated search cap. |
| R8_3_1795 | Box and mod-2/mod-3 consistency, of modular ranks 629 and 616 | The capped HNF search made no exact lattice determination; the capped bounded search found no exact witness. |

Neither terminal result excludes a categorification or supplies a model.

Independent and positive controls:

* `review_joint_control.py`: a directly enumerated 64-simple center, full
  simultaneous Galois tuple multiplicities, and the exact degree-64 integer
  characteristic polynomial of a separating integer matrix combination.
  It imports no joint-data, row-building or support-filter producer function.
* `unit_pair_constraints.py`: all source-unit product identities, finite
  AM–GM slacks and original integer center equations on the actual center of
  Fibonacci tensor Vec(C4), including complex dual character labels.
* The shared `commutative_integer` controls cover actual integer centers,
  finite-field elimination, Hermite arithmetic, finite-box propagation and
  exact bounded linear separators.

`JOINT_GALOIS_REVIEW.md`, `INTEGRAL_CENTER.md`,
`integral_center_filter.tex`, and `unit_pair_method.tex` give the theorem
scope and manuscript-ready arguments. No assertion of exotic categorification
or of a new categorical construction follows from these campaign records.
