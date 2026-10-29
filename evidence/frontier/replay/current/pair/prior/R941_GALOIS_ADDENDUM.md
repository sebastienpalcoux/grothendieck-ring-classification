# Bounded follow-up: a same-restriction triple-orbit condition for R941

29 October 2026. **No further exclusion.** This follow-up proves a necessary
restriction and checks its small finite column domain. It does not modify
the main report or any classification status.

The five irreducible characters of R941 have values in
K=Q(sqrt(2),sqrt(3)): four are the dimension-field conjugates of the FP
character and the degree-two character is (2,0,0,-2,0,0,0,0). Their
evaluations on the center basis

    1, g, X1+X2, X4+X5, X6+X7

have determinant 3072. Thus they separate central elements. Every
forgetful image F(Z) of a central object is central in the source ring.

Apply the full-restriction Galois lemma proved in the parallel R137
investigation, including its noncommutative extension. For completeness,
the normalized central S entries on distinguished rows A_E are rational
degree factors times chi_E(FZ)/f_E and hence belong to K. A modular
Galois automorphism fixing K fixes these entries. The positive unit
row removes its column sign. Consequently every chi_E has the same
value on F(Z) and F(pi_sigma Z); separation on the ring center gives
the equality of the **entire restriction vectors**.

If a twist has order divisible by nine, choose a cyclotomic automorphism
whose exponent is 25 on the 2- and 3-primary part and is a unit on all
remaining prime factors. It fixes K because it is 1 modulo24. The
squared-twist action multiplies the exponent modulo9 by4, of order3.
Thus the twist orbit has size divisible by three. In particular every
such central simple belongs to a set of at least three distinct simples
having exactly the same restriction vector. No assertion that their
whole orbit always has length exactly three is made.

The low simples have twist one, so all these copies belong to the high
column Gram. In the existing four reduced high coordinates, write Q for
that positive definite Gram matrix. Each relevant vector v must satisfy

    3 v v^t <= Q, equivalently 3 v^t Q^(-1) v <= 1.

The exact check finds 22 eligible vectors among the65 available column
types; the other43 cannot carry a twist with order divisible bynine.
All14 retained fermionic allocations nevertheless have eligible
restriction fibers with multiplicity at leastthree. Their eligible
fibers of multiplicity>=3 have indices9,10,12,17 as applicable. Their
Gram capacities are23,11,8,5, respectively.

Therefore this bounded test removes no complete retained allocation.
It does not justify a bound48 on the Frobenius-Schur exponent and does
not supply a modular S matrix or a category. A further decision would
require simultaneous twist, fusion and indicator constraints, rather
than the orbit-capacity condition by itself.

`r941_galois_followup.py` checks the center basis, character determinant,
positive Gram, all65 exact capacities and the14 retained allocations.
The categorical Galois inputs and source references are given in
`../r137/REPORT.md`, Section1; that proof uses normalized S entries and
the canonical anomaly-one center twist normalization.

