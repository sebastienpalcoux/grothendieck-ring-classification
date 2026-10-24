# Independent audit of the relative-cocycle model for R9_2_1246

Verdict: **PASS** for existence as a unitary fusion category and equality of all
729 source structure constants. The audited record is mask 20, trivialization
parity 0 in `phase3/integral_theory/d48_exotic_relative_twists.json`.

The group G=S4×C2 and subgroup H=⟨((12),1),((34),0)⟩≅C2² are the same as for
R9_2_392. Let s denote permutation sign and e the external bit. The new
associator is

\[
\omega(a,b,c)=\Omega(a_0,b_0,c_0)
 (-1)^{e(a)\alpha(b,c)+s(a)e(b)e(c)},
\]

where a0 is the S4 coordinate and Ω is the explicit eighth-root-valued S4
associator used in the earlier R9_1_92 construction. The cup-product factor is
a three-cocycle. The audit checks α directly on all 48³ triples and ω directly
on all 48⁴ quadruples, so no extrapolation from a previous model status is used.

The imported Ω was also independently checked against its earlier source:

- Source file: `research/prior/rank9_rank10_m1_20261023/work/resolve_small_models/s4_twisted_models.json`.
- Source record: R9_1_92, first model's parameters, modulus 8.
- Source-file SHA-256: `a5718e5471648b5b3fcb6df425dbe3f547701584afa95558413d3102e2281a2c`.
- All 576 products of the old-to-permutation group isomorphism agree.
- All 13,824 transported Ω entries agree.
- Normalization and all 331,776 S4 three-cocycle equations hold independently.

In the ordered subgroup basis (1,y,x,xy), the explicit trivialization is
ψ(a,b)=ζ8^q(a,b), with

\[
q=\begin{pmatrix}
0&0&0&0\\
0&1&2&7\\
0&4&0&0\\
0&1&6&7
\end{pmatrix}.
\]

All 64 relative algebra equations δψ=ω|H⁻¹ hold. Hence A=⊕h∈H h with
multiplication ψ is an actual algebra object in the unitary pointed category
Vec_G^ω, and its bimodule category is the desired unitary group-theoretical
category. The general bimodule character formulas reviewed in
`D48_RELATIVE_TWIST_AUDIT.md` apply unchanged; the required square roots now lie
in μ16. The audit performs the trace sums and inner products exactly in Z[ζ16]
and verifies all nonconstant cyclotomic coefficients cancel.

The complete projective-character list has the same double-coset skeleton as
R9_2_392, giving dimensions (1,1,1,1,2,4,4,2,2) and total dimension 48. Its tensor
is different. The map from original source indices to model indices is

`[0,8,7,5,6,3,1,2,4]`.

All 729 coefficients match physical line 1308 of the original compressed census,
independently counted as exact-multiplicity-two ring 1246. Unit, nonnegativity,
and all associativity identities also hold. The tensor SHA-256 is
`eca2cd1507105573f8393947b68bdb1423cab85f39b2022e6f51897e4d6ed847`.

Replay: `python phase3/audit_models/audit_d48_relative_twist.py --exotic`.
Machine record: `phase3/audit_models/d48_exotic_relative_twist_audit.json`.

This is a positive existence certificate. It does not assert that the tested
relative-cocycle family exhausts all categories with this group and subgroup.
