# R901: the full complex character field

All eight characters of R8_3_901 split over
`L = Q(sqrt(3), sqrt(5), i)`, a degree-eight field. A primitive element
`u = sqrt(3)+sqrt(5)+i` satisfies

\[
 u^8-28u^6+238u^4+372u^2+441=0.
\]

`octic_complex_character_table.py` provides `OcticTable(R,a)` with the
same arithmetic interface as the previously reviewed quartic and sextic
adapters: `K`, `degree`, `characters`, `ds`, `D`, `beta`, `codegrees`,
`coordinates`, `conjugate`, `integral`, `failure`, and inherited
`prepare`/`assignments`. The input `a` uses the FP coordinate order
`[1,sqrt(3),sqrt(5),sqrt(15)]`, as does `generic_data.setup(R,3,5)`.

The three radicals are explicitly recovered in the rational power basis.
The executable verifies their squares and sum, irreducibility, the full
complex conjugation involution, all eight source characters, all 512
multiplication identities, duality, orthogonality, and the positive FP
embedding. Algebraic integrality is checked by the degree-eight rational
multiplication characteristic polynomial. A separate direct construction
of the operator verifies 74 samples; all 64 source character values are
integral. The negative control 1/2 is rejected. The genuinely nonreal
known model `Fib tensor Vec(C4)` retains all 12 actual center-restriction
types in this same degree-eight field.

The read-only source-bound replay is
`python octic_complex_character_table.py`, with receipt
`octic_complex_character_table_results.json`. This is an arithmetic
adapter, not a categorification or an exclusion. When used in the atomic
S system, all eight rational coordinates of S symmetry must be retained,
while the old FP relative twist-moment field remains unchanged. No STS
identity over this larger field is asserted.
