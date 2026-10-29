# Independent audit of the R137 distinguished-Verlinde restriction

**Verdict:** the new restriction is valid, and the old positive-TY rational witness fails it exactly. This rejects that witness as a possible completion to modular fusion data. It does **not** exclude R9_2_137, the other TY sign, or every feasible point of the necessary relaxation.

## Formula and hypotheses

Work in the inherited pseudo-unitary representative. Put d=4+3 sqrt(2), D=144+96 sqrt(2), and r=17+12 sqrt(2). The previously forced central simple B has restriction 1+X3+X4+X5+X6 and dimension r. It is the nontrivial Galois conjugate of the unit label. Write sigma for the automorphism of Q(sqrt(2)). In normalized center notation, the known row is

    s(B,Z)=r sigma(delta_Z)/D,

where delta_Z=FPdim(Z). This row is real, as are the distinguished-character rows. It follows from the ordinary Verlinde formula that

    N(B,B;B)=sum_Z (r sigma(delta_Z))^3/(D^2 delta_Z).

For a restriction vector v, set a=v0+v1+v2+v7+2v8 and b=v3+v4+v5+v6. Then delta=a+b d. Since d^2=8d+2,

    r sigma(delta)=a+(4a-b)d.

Consequently the coefficient of the multiplicity variable belonging to v is the explicit field element

    t(v)=(a+(4a-b)d)^3/(D^2(a+b d)).

No twist or unknown entry of the modular matrix is involved in this row. Nonnegative-integral fusion coefficients impose that the total be an ordinary nonnegative integer, not merely an element of Q(sqrt(2)).

More generally, for a distinguished simple A_E with source character chi_E and formal codegree f_E, the known character row gives

    N(B,B;A_E)=sum_Z (r sigma(delta_Z))^2 chi_E(FZ)/(D delta_Z f_E).

This furnishes nine necessary linear functionals of the existing physical multiplicity variables. The eight nonunit outputs must be nonnegative integers; the unit output is 1. The complete character table is real here, so no omitted complex conjugation changes these expressions.

## Independent exact replay

The audit uses its own rational-pair arithmetic in Q(d), independently of the case researcher's Q(sqrt(2)) implementation. It checks:

- all 264 old equations for the published positive-TY witness;
- its 102 support coefficients, their nonnegativity, and absence of removed columns;
- every one of the 22,179 physical columns has Gram block vv^t, so the witness coefficient really is a multiplicity weight and no orbit normalization is missing;
- multiplicativity of all nine source characters against every product in the exact source tensor and all nine formal codegrees;
- all nine distinguished Verlinde sums by independent field arithmetic.

The result is

    N(B,B;B)=5/6,

and several of the other distinguished coefficients even have a nonzero sqrt(2) component. Thus the old witness does exactly what its original label said—it certifies feasibility of its necessary relaxation—but it cannot be modular fusion data. The original account did not claim that it was a category, so this is a stricter necessary test rather than a retraction of an accepted categorification.

Run `python unified/audit_r137_verlinde.py`; the output is `audit_r137_verlinde.json`. No optimizer is called by this audit.

## Relation to the complete positive-sign obstruction

This audit checks the exact character/Verlinde formula and rejects the earlier saved witness. The full positive-TY branch is now excluded by the separate nine-certificate proof in `audit_r137_positive_certificates.md`. Its exact replay establishes the bounds 1/2 and31/18 and their subsequent integer consequences. The negative sign remains unresolved; its current necessary-data witness has a separate exact audit.
