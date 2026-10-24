# Dimension48: complete split-involution Morita obstruction

The two dimension48 rank9 multiplicity2 rings R9_2_396 and R9_2_1265 are not Grothendieck rings of complex fusion categories. The obstruction is the existing project split-involution Morita criterion, with its previously restricted finite enumeration extended from at most two fixed simples to three. There is no new pivotality assumption and no restriction to unitary categorifications.

Choose g=b1 for396 and g=b5 for1265 (zero-based census basis indices). In each ring g is an invertible involution fixing exactly three simples. Existence of a fixed simple trivializes the associator on the subgroup <g>, so A=1⊕g is a connected separable algebra. The simple right A-modules consist of one object per free g-orbit and two objects X+,X− per fixed X.

If f is the number of fixed simples, write T_i for the anti-invariant f×f block of the action of the basis object b_i on these two structures. Its entries obey the exact finite bounds and parity conditions

−N_(i,X)^Y ≤ (T_i)_(X,Y) ≤ N_(i,X)^Y,
(T_i)_(X,Y) ≡ N_(i,X)^Y modulo2,

as well as T_0=I, T_(i*)=T_i^t, and T_i T_j=Σ_k N_(ij)^k T_k. Swapping X+ and X− conjugates every T_i by one diagonal sign matrix. These equations and their proof have no dependence on f≤2.

The new enumerator `general_anti.py` encodes precisely these finite domains for multiplicity at most2, checks each returned solution with integer matrix arithmetic, and excludes its entire diagonal-sign orbit. It reports completion only when the finite solver proves that no solution remains. Both rings have exactly18 branches modulo this gauge. The older project enumerator's f≤2 bound was an implementation bound, not a hypothesis of the categorical criterion.

Each branch determines the entire nonnegative integral module action by the standard split-module formulas in `sources/module_dual_gram.py`. The tensor category of A-bimodules must then have nonnegative integral Gram decompositions compatible with its forced FP dimensions. In both rings all18 branches fail: seven have rational Gram rank greater than the forced dual rank; ten violate a partial internal-end Gram constraint; one violates the full simultaneous Gram constraint.

For every Gram failure the exact rational Farkas vector is saved. `morita_replay.py` enumerates the complete finite anti-module domain afresh, reconstructs each complete Gram-column domain, and verifies each saved rational separator. It never invokes an LP optimizer. The rank obstructions are also recomputed exactly. The two summary certificates are in `morita48_exclusions.json`.

Only Frobenius–Perron dimensions and their positivity enter this argument. It is therefore an all-complex exclusion without a pseudo-unitarity gate. The categorical Morita and module-Gram arguments are the existing project's arguments in `sources/module_dual_gram.py` and `sources/full_morita_gram.py`; this continuation removes the finite enumerator's small-block restriction.

The same extended test has a surviving branch for the independently realized ring389, and also for1025,1254,1709,1759 and1988. Those outcomes are explicitly recorded as inconclusive, not as exclusions.
