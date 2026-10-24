# Quartic-family theoretical retry (24 October 2026)

Targets: R8_3_928, R8_3_941, with the shared possible Morita route through R6_8_1660.

## Result

No categorical existence or nonexistence theorem was obtained for these targets in this retry. In particular, no status change is justified. The new work below excludes additional specific model routes and identifies why several plausible stronger arguments do not establish an obstruction.

The authoritative starting point is the restored `unresolved11_20261024` archive and its input profiles. This note does not replace its exact certificates.

## An index lemma excluding an additional exceptional-model route

**Lemma.** If D is a proper full fusion subcategory of a fusion category C, then FPdim(C)/FPdim(D) >= 2.

**Proof.** Regard C as a left D-module category and decompose its simple objects into indecomposable components M. The component containing the unit is D itself. Fix a simple X in a component M. The positive dimension vector on M is the restriction of the FP dimension vector of C. The regular-element identity for an indecomposable based D-module gives

    FPdim(End_D(X)) = FPdim(D) d(X)^2 / sum_{Y in Irr(M)} d(Y)^2.

Here End_D(X) is the internal end for the D-action. By Frobenius reciprocity it is the D-part of X tensor X*, so its FP dimension is at most d(X)^2. Consequently every component has sum of squared FP dimensions at least FPdim(D). A proper inclusion has at least the unit component and one other component. Summing proves the claim. This uses FP dimensions and requires neither unitarity nor a spherical structure.

For the three targets the common dimension is

    d = 144 + 96 sqrt(2) + 80 sqrt(3) + 56 sqrt(6).

The exceptional right-module category associated with the conformal embedding SU(4)_8 into Spin(20)_1 has dimension

    e = 48(9 + 5 sqrt(3)).

The exact ratio is

    e/d = 24 - 15 sqrt(2) + 12 sqrt(3) - 9 sqrt(6),

and lies strictly between 1 and 2. Hence none of the three target categories can be a full fusion subcategory, including a neutral component, of this specific exceptional module category. This route is excluded independently of the E21 Morita-rigidity argument. It does not exclude other algebra objects or other categories associated with SU(4)_8.

Primary source for the exceptional module category and its dimension: R. Coquereaux and G. Schieber, *Quantum Symmetries for Exceptional SU(4) Modular Invariants Associated with Conformal Embeddings*, SIGMA 5 (2009), 044, https://doi.org/10.3842/SIGMA.2009.044 ; open PDF https://www.emis.de/journals/SIGMA/2009/044/sigma09-044.pdf . See the conformal-embedding discussion and the E8 quantum-cardinality computation.

## Other exceptional constructions checked

The quantum-group categories F4 at level 3 and G2 at level 4 have the same dimension

    240 + 96 sqrt(6) = 475.151... < d = 555.499... .

Their nine FP dimensions are, as a multiset,

    1,
    (2 + sqrt(6)) twice,
    (3 + sqrt(6)) twice,
    (4 + 2 sqrt(6)) twice,
    5 + 2 sqrt(6),
    6 + 2 sqrt(6).

These values were checked from the quantum Weyl dimension formula. The categories themselves are therefore too small to contain a target as a full fusion subcategory; their conformal-extension module categories are smaller still. This is a model-screening calculation, not a new universal exclusion.

The already constructed E21 model R8_3_982 comes from the triality-zero component of the chiral SU(3)_21 -> E7_1 module category. The established Morita rigidity of R982 only rules out a Morita transfer from that category. It does not by itself rule out every other neutral-component construction involving a larger quantum-group category. This logical distinction was kept throughout this retry.

## Stronger categorical arguments examined but not proved

1. **R928 and Q-system completeness.** The archived all-ranks module argument says that every indecomposable semisimple module category is regular. In the unitary literature this is called Q-system completeness or torsion-freeness. The cited literature implies Morita rigidity, not that the fusion ring is commutative. Thus it cannot exclude R928. Noncommutative pointed examples also show that a general implication from module rigidity to commutativity would be false.

2. **The central semion.** A nondegenerate semion subcategory of Z(C) splits the center, but does not automatically split C as a Deligne product. The known R982 model is an essential control. No additional argument turning the R928 module rigidity into the required splitting was found.

3. **R941 fermion condensation.** The actual algebra 1+g gives a module category and a fermionic quotient. It does not give an ordinary rank-four fusion category merely because the g-action on simples is free. The quotient is a superfusion category; odd morphism channels remain. Therefore ordinary rank-four classifications and a claimed ordinary dimension character of the signed quotient cannot be used as exclusions.

4. **The signed quotient.** The R941 quotient at g=-1 is a split quaternion algebra, and the analogous R928 quotient is Hamilton quaternionic. The absence of one-dimensional characters in those quotients does not contradict a physical positive dimension function: that dimension function factors through the g=+1 specialization. A pivotal structure with g-dimension -1 has not been established.

5. **Formal-codegree inequalities.** The general spherical inequality of Ostrik,

       sum_E 1/f_E^2 <= (1 + 1/dim(C))/2,

   applies, but does not obstruct the formal-codegree multiset consisting of the four conjugates of d and the additional codegree 4. The left side is 5/32, well below the strongest right side obtained from the largest conjugate d. This adds no cut to the existing exact center domain.

6. **R1660 to R941.** The archived exact possible Morita dual is genuine ring-level information. The required nonpointed separable algebra is still an existence premise, rather than a consequence of the tensor. Its multiplication and associativity cannot be supplied by the dimension match.

Primary references consulted for the logical scope:

- C. Jones and K. Schatz, *Quantum Cellular Automata and Categorical Dualities of Spin Chains*, Proposition 6.1 and the preceding Q-system-complete discussion, https://doi.org/10.1007/s00220-026-05571-y ; https://inspirehep.net/files/6f01b73404987d41b7090a7bf95fd01a .
- V. Ostrik, *Remarks on global dimensions of fusion categories*, Theorem 3.1.1, https://arxiv.org/abs/1804.08761 ; https://arxiv.org/html/1804.08761v1 .
- D. Aasen, E. Lake, K. Walker, *Fermion condensation and super pivotal categories*, https://arxiv.org/abs/1709.01941 , especially the fermion-condensation and superpivotal conventions.

## Remaining categorical gap

A resolution still requires either an actual associator/model construction, an algebra-existence theorem realizing the R1660/R941 Morita route, or a categorical obstruction that goes beyond the presently surviving necessary center data. The narrowed phase allocations and the exact ring computations do not fill that gap.
