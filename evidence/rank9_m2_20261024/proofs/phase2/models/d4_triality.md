# Dynkin triality realizes R9_2_1857

Let B=C(D4,2) be the standard unitary WZW/quantum-group fusion category
usually denoted Spin(8)_2 or SO(8)_2. Then

    K0(B^{C3}) ≅ R9_2_1857,

where C3 acts by the order-three diagram automorphism of D4. The model is
unitary and has global dimension96. The exact source-to-model permutation is

    [0,8,7,2,1,3,5,6,4].

The standard quantum-group construction and modular-data formulas are
reviewed in Galindo--Mora--Rowell,
[arXiv:2311.17255](https://arxiv.org/abs/2311.17255), Section5.1.
The specific integral metaplectic category SO(8)_2 is studied in
Deaton et al., *Integral Metaplectic Modular Categories*,
[arXiv:1901.04462](https://arxiv.org/abs/1901.04462).

## Actual action, not a fusion-rule symmetry assumption

Number the D4 nodes so2 is the trivalent node and1,3,4 are its outer nodes.
The cyclic permutation (1,3,4) preserves the Cartan matrix. Therefore
permuting the generators E_i,F_i,K_i of the Drinfeld--Jimbo quantum group by
these indices preserves all defining relations, coproduct, counit and
antipode. It is a Hopf algebra automorphism of order three. The induced
pullback functors on modules form an actual tensor C3 action with identity
composition constraints; this is not inferred solely from the permutation
of simple objects. They preserve tilting modules, the pivotal quantum trace
and its negligible ideal, and hence descend to the semisimplified level-two
fusion category. The standard unitary WZW realization gives the same
unitary action from the compact Lie-algebra diagram automorphism. Thus the
equivariantization B^{C3} exists as a unitary fusion category.

## Seed tensor and the fixed fusion lines

The integrable highest weights are quadruples (a1,a2,a3,a4) of nonnegative
integers satisfying a1+2a2+a3+a4≤2. There are eleven: four simples of dimension
one and seven of dimension two. The weight action is

    (a1,a2,a3,a4) ↦ (a4,a2,a1,a3).

Its fixed simples are precisely1 and f=ω2. The three nontrivial invertibles
form one free orbit, and the six other dimension-two simples form two free
orbits. Moreover

    f⊗f = sum_(g invertible) g.

These assertions are verified from the exact WZW tensor, independently of
the census. The fixed objects therefore have no fixed fusion line except
the unit lines and the single line f⊗f→1. An equivariant structure on f
exists because H²(C3,C×)=0. Its three choices differ by powers of ζ3.
The action on the one-dimensional line f⊗f→1 is a cube root of unity.
Rescaling the equivariant structure by ζ3^r changes this trace by ζ3^(2r),
so it can and will be normalized to1. Unit compatibility gives trace1 on
the remaining unit lines. Thus every required nonidentity-group trace is
determined; no unknown higher-dimensional intertwiner action remains.

Each fixed simple has three equivariant lifts; each free orbit has one.
Consequently the nine dimensions are 1³,2³,3,6². For simple equivariant
objects supported on orbits A,B,C, the identity-group contribution to the
invariant Hom-space is sum_(a∈A,b∈B,c∈C) N_ab^c. For a nonidentity element
of C3, this Hom-space has zero trace unless all three orbits are fixed:
otherwise its summands occur in three-cycles. For three fixed orbits the
remaining character sum is2 when the three character exponents satisfy
r+s=t modulo3 and−1 otherwise, multiplied by N_ab^c. Dividing the complete
character sum by3 gives the full equivariant tensor.

## Exact replay

d4_triality.py builds the Weyl group as the192 even signed permutations of
four coordinates. Using twice the weight coordinates, it evaluates the
Weyl alternants in Q(ζ32), with defining polynomial x^16+1. If U is the
unnormalized alternant matrix then

    U U^T = 4·8^4 I = 16384 I,

because charge conjugation for D4 is trivial. The normalized S is U/128.
The script verifies this equality and computes each of the1331 seed fusion
coefficients by the Verlinde formula using exact algebraic arithmetic.
It checks nonnegativity, integrality, fusion axioms, triality invariance,
fixed-object rules and the four-invertible dimension pattern. It then
computes the equivariant tensor by the preceding character formula and
compares all729 coefficients under the displayed permutation.

All seed simples are self-dual, so the two free dimension-two orbits give
self-dual dimension-six simples in the equivariantization. This distinguishes
the result from R9_2_2029, whose dimension-six objects are dual to one another.
This construction establishes only R9_2_1857. The separate categorical
zesting and equivariant-action proof in d4_zest_triality.md realizes
R9_2_2029.
