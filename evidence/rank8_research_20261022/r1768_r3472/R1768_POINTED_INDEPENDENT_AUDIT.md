# Independent review of the R1768 pointed-associator restriction

The C2 Fourier-packing argument in `../pointed_followup/PROOF.md` forces
the **nontrivial** class in `H^3(C2,C*)` for the pointed subcategory of any
complex categorification of `R8_3_1768`. This is a necessary restriction,
not a general exclusion of the fusion ring or a categorical construction.
In particular, the connected separable subgroup algebra `1+g` cannot
exist in a hypothetical categorification.

The proof mechanism is the same as in `R1795_POINTED_INDEPENDENT_AUDIT.md`,
with the opposite surviving pointed-associator class. The directly checked
source identities are `g^2=1`, `B[0,g]=0`, and `B[g,g]=8`. In the basis
`(1,sqrt(37))`, the equal twist-fibre mass is `D/2=(222,36)`. Nonnegative
source dimension coordinates make the integer packing domain finite and
complete for the chosen necessary relaxation. The two fibre Gram values
must sum to eight. The iterative filter retains 243 of the 255 pointed
high columns.

For trivial associator the canonical pointed indicator is `nu_2(g)=+1`.
The equality case of the positive induction trace forces every supporting
twist to be `+1` or `-1`; their first four powers have traces `(1,1,1,1)`
and `(-1,1,-1,1)`. After the independent packing filter, this gives 10,711
allowed columns. Eight exact separators cover every admissible assignment
with `nu_2(g)=+1`. The previously accepted general-to-Galois-pseudo-unitary
gate transfers the restriction to every complex categorification, because
both classes of `H^3(C2,C*)=C2` are fixed by Galois conjugation.

The terminal producer result retains an exact feasible necessary-system
witness in the `nu_2(g)=-1` branch. Such a witness supplies no category or
associator. It must not be promoted to a realization.

## Independent executable checks

`r1768_pointed_independent_audit.py` reads the stable terminal producer
file `../pointed_followup/R8_3_1768.json` and performs no optimization or
file mutation. It reconstructs the induction Gram directly from the
tensor, matches the frozen complete cone, independently enumerates the
finite packing domain by repeated constituent addition, reconstructs the
entire allowed phase mask, checks full eight-branch coverage, and pairs
each of the 10,711 explicit sparse columns with all eight exact rays.
It also verifies the factored scoring oracle and every strictly negative
right-hand-side pairing. Active checks remain enabled under optimization.

```sh
python3 evidence/rank8_research_20261022/r1768_r3472/r1768_pointed_independent_audit.py
```

The categorical reduction, phase argument, finite domain and certificate
scopes are independently accepted. Mathematical references and the
inherited all-order trace-domain proof are those in the producer proof;
this audit introduces no pivotality assumption or twist-order cutoff.
