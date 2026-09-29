# Independent audit of the second continuation

The multiplicity-three frontier R6_3_215 is excluded in general scope.
The new categorical ingredient is the adjacent pair-insertion argument in
`stabilizer_rotation.md`; exact rotation naturality connects its
anticommuting local stabilizers to third Frobenius–Schur indicators.

The complete combined certificate was independently replayed with Python
optimization enabled. It covers 1,480 unrestricted signed quotients in 63
sign orbits, 271 nongauge character rejections, all 16 involution-module
branches, all 91 low induction frames and all 200 central trace systems.
The exact third-indicator rows, low modular equations, joint Galois
dimension/eigenvalue conditions, and all ten order-three relative-trace
patterns were also inspected mathematically. No numerical infeasibility
output is used as an exclusion certificate.

The stronger Clifford identities underlying the higher-multiplicity
criterion are checked in `clifford_rotation.py`: U³=1, cyclic conjugation
of the three generators, and trace -1 on each two-dimensional simple.
For cubic multiplicity m the real-field averaged third indicator lies
between -m/2 and m/4. The pair-insertion proof does not require its fixed
simple object to be self-dual.

The resulting general exclusion of R6_4_416 was audited in
`higher_stabilizer.md`. Its complete pseudo-unitary certificate was
independently replayed under `python -O`: both module branches, all 895
low induction frames and all 32 required trace systems pass exact checking.

The earlier fixed-map obstruction for the actual cyclic-eight category was
also strengthened to the whole actual Morita class in
`actual_cyclic8_morita.md`. This is an independent stepping stone; the final
multiplicity-three exclusion does not need to identify a hypothetical
center with that known center.

The four general biquadratic exclusions R6_7_3813, R6_8_6940, R6_8_6973 and
R6_8_6998 were independently regenerated and verified under `python -O`.
Their field-containment, integral-basis, positivity-box, norm, complementary
codegree and parity arguments were checked. The further ramification
argument for R6_7_3812, R6_8_6234 and R6_8_6509 was checked mathematically:
the dimension field is forced to Q(sqrt(226)); the rational codegree 15
then forces a global-dimension trace larger than the original Casimir trace.
All three final simplified certificates also passed independent optimized
replay.

The trace-ideal criterion `software/new_trace_ideal.py` was checked
mathematically and independently replayed under optimization. It excludes
R6_8_6997 because the dimension trace is a positive multiple of 18,435,
larger than the original Casimir trace 6,173. For R6_8_6520 its trace
multiple 6,145 leaves a magnitude deficit of at most 20, smaller than the
first possible deficit 24. The complete saturated signed enumeration
(2,616 nodes, one gauge-original solution) proves a Galois pseudo-unitary
reduction. The subsequent complete Gauss-family obstruction was audited
in `gauss_family.md`: its forced sum of 590 roots requires at least 4,298
roots by an arbitrary-order quadratic Gauss bound. The combined general
exclusion of R6_8_6520 passed independent optimized replay with optimizer
entry points disabled; see `gauss_family_replay.json`.

A separate exploratory relative-center argument was not used: the claim
that a central fermion is impossible merely because the universal grading
is trivial is unjustified. The main proof avoids this issue completely.
