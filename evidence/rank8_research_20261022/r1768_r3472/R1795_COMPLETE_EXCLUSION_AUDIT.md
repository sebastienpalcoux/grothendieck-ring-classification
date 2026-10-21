# Independent audit of the complete R1795 exclusion

The two C2 Fourier-packing branches together exclude every complex fusion
categorification of `R8_3_1795`. The previously recorded pointed-associator
triviality result was an intermediate consequence of the odd branch alone.
The terminal even-branch certificates exclude its remaining possibility.

## Complete hypothesis reduction

The source-bound general sphericalization theorem in
`../pivotality/PROOF.md`, with records
`R8_3_1795_signed.json`, `R8_3_1795_character_sieve.json` and
`general_spherical_gates.json`, implies that any complex categorification
of this fusion ring would have a pseudo-unitary Galois conjugate with the
same fusion rules. The exclusion may therefore be proved for the canonical
pseudo-unitary pivotal structure. This step does not assume an original
pivotal structure and does not claim that an original category would itself
have been pseudo-unitary.

The pointed subgroup has order two, with nonidentity object `g`. Its two
possible associator classes have canonical second indicator
`epsilon=nu_2(g)` equal to `+1` and `-1`. Equivalently, since `g` is
selfdual, the second indicator necessarily takes one of these two values.
No third parity is available. The source tensor has selfdual simples at
all eight indices. The usual odd-multiplicity indicator condition forces
`nu_2(X_i)=+1` precisely at indices `5,6,7`: each of these occurs with odd
multiplicity in some `X_j X_j*`. The other four signs, at indices
`1,2,3,4`, remain unrestricted. Thus the complete necessary sign domain
has sixteen assignments, eight for each value of `epsilon`.

## Common exact finite domain

The proof of the Fourier-fibre lemma and its independent audit are in
`R1795_POINTED_INDEPENDENT_AUDIT.md` and `../pointed_followup/PROOF.md`.
The induction Gram gives `B[0,g]=0` and `B[g,g]=8`. Every hypothetical
center's two twist fibres have mass `D/2=270+120 sqrt(5)`. Their constituents
contribute the nonnegative integer triples `(m^2,m z_0,m z_1)`; the two
Gram totals sum to eight. A finite iterative packing filter retains exactly
1,187 of the 1,476 pointed high restriction columns. A separate
constituent-addition closure gives the identical retained set.

For the odd branch, the supporting twist traces are `(0,-1,0,1)`, leaving
58,074 complete-cone columns. For the even branch, the supporting twist
traces are `(1,1,1,1)` or `(-1,1,-1,1)`, leaving 59,261 columns. Both
domains retain all applicable nonpointed and rotation columns. Their
inherited complete all-order trace compression, low-column choices,
character-labelled S symmetry and STS constraints are unchanged. No
twist-order cutoff or assumed complete fusion-ring model is introduced.

For every one of the sixteen necessary sign assignments, an exact integral
ray pairs nonnegatively with every column of its corresponding domain and
strictly negatively with its required right-hand side. Hence neither
domain contains the required positive center data. No pseudo-unitary
categorification exists, and the general Galois reduction proves the full
complex noncategorification statement.

## Independent replay and source agreement

The odd-branch audit checks the immutable snapshot
`../pointed_followup/R1795_pointed_associator_obstruction.json`:

```sh
python3 evidence/rank8_research_20261022/r1768_r3472/r1795_pointed_independent_audit.py
```

The even audit reads the terminal complete result
`../pointed_followup/R8_3_1795.json` and checks that its odd record is
identical to that already audited snapshot. It independently checks the
complete indicator domain directly from the tensor, the packing domain,
the even-phase column mask and all eight even rays:

```sh
python3 evidence/rank8_research_20261022/r1768_r3472/r1795_even_independent_audit.py
```

Together the audits check every explicit sparse column against every ray
in addition to the inherited factored oracle: 58,074 columns for eight
odd rays and 59,261 columns for eight even rays. Both are read-only,
contain active checks, and require no optimizer. Their mathematical inputs
and the general-to-pseudo-unitary gate must all be retained in any source
manifest supporting this general exclusion.

This conclusion supersedes the earlier open-case designation and the
intermediate trivial-pointed-associator restriction. Conditional module
and Morita computations remain mathematically meaningful necessary data,
but they do not supply categorifications of this excluded ring.
