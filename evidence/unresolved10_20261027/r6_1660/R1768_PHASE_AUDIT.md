# Independent audit of the R1768 diagonal phase

**Verdict: passes.** Together with `R1768_LATTICE_LEMMA.md`, the root
investigator's `../root/DIAGONAL_PHASE.md` establishes
`E(l,l)=1` for every `l=1,...,11` in the actual RW solution.

The audit separately checked the following mathematical normalizations.

- `T gamma T^(-1)` is the displayed HJ monodromy. The two eta multipliers
  both equal one; no eta or square-root phase is dropped.
- At arbitrary nonreal parameter, shifting the parameter by one leaves
  the defining q-Pochhammer quotient exactly unchanged under that
  conjugation. The first integer index remains `l`, while the numerator
  `l tau+l` becomes `l omega`. Thus the new group index is `(l,0)`.
- The argument shift to `z0=(1-l/12) omega` is
  `(l+1)omega-l`. Multiplication by `gamma'^(-1)-I` gives exactly
  `(m,-12m)`, with `m=l-12`. These are nonzero classes: the two index
  lattices are both `12 Z²`.
- In RW Proposition 5's proof the individual factors are
  `Phi_S(t_j-1;omega_j)`. Keeping the displayed Gaussian factor gives
  exactly the phase polynomial used by the root's verifier.
- Independently reconstructing every backward cocycle variable gives
  integral `m_j=x_j-u_j`, `m_12=0`, `m_0=-m`, and
  `z_j+m_j omega_j-m_(j-1)=x_j omega_j+y_j-1` in all 132 instances.
  RW equation (16) then changes `Phi_(0,-m)` to `Phi_(m,0)` exactly.
- The index lists `j=0,...,11` and `j=1,...,12` differ by a cyclic shift.
  All eleven phase sums vanish exactly in `Q(sqrt(37))`.

The positivity of each double-sine factor follows from its real Barnes
definition: `0<t_j<1+omega_j`, since `0<x_j<=1`, `0<=y_j<1` and
`omega_j>1`. Thus no sign is inferred merely from a modulus calculation.

Reproduce the arithmetic audit with `python audit_r1768_phase.py`.
The resulting `r1768_phase_audit.json` records all backward indices.
The script uses explicit checks that remain active under optimized Python.
It imports the root's exact quadratic arithmetic and phase computation,
but independently computes the argument shifts and backward cocycle data.

Primary source checked directly: Radchenko–Wheeler,
<https://arxiv.org/html/2609.21892v2>, definition (2), equation (16),
Proposition 2(ii), Lemma 2, and the proof of Proposition 5.

This audit does not identify the Grothendieck ring of the eventual Morita
dual; that remains a separate categorical calculation.
