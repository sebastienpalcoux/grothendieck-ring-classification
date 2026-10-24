# Independent direct exclusion of R9_2_1959

**Accepted, with general complex scope through the audited signed Galois-PU
gate.** The same real-character/dual-dimension obstruction as in `AUDIT1487.md`
applies, with source data verified separately.

In source order the dimensions are

    1, 2+2sqrt(3), 2+2sqrt(3), 4+2sqrt(3), 4+2sqrt(3), 1, 1, 1, 2.

Duality exchanges b1,b2 and b3,b4. The scalar character

    χ=(1,2,2,−2,−2,1,1,1,2)

is dual-invariant and has formal codegree 24. Thus its distinguished central
simple A is selfdual, has dimension 4+2sqrt(3), and restricts with unit
multiplicity one. The large simples b3,b4 cannot occur in F(A), because either
already has its full dimension. Its sqrt(3) coefficient forces exactly one of
b1,b2, contradicting selfduality. This is independent of the duality of b3,b4.

The argument proving A selfdual is given in `AUDIT1487.md` using the
central-character formula and S-matrix duality. It does not presume categorical
unitarity. The complete character/dimension identities, codegree and all six
dimension-compatible restriction columns were independently checked by

    python phase3/audit_quadratic_symmetry/replay1487.py 1959

The output is `replay1959.json`; no developing-agent constructor or sieve is
imported. The separately audited gate is
`phase2/signed/gate_R9_2_1959.json`. No LP, Gram bound or trace enumeration is
needed for this exclusion.
