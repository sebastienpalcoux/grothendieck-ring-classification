# Eight unitary models for the rank-nine multiplicity-two census

Every tensor below is reconstructed from a categorical construction or a
published categorical fusion table and compared in all 729 coefficients.
The displayed permutations send the source census basis to the model basis.
No dimension-profile or numerical match is promoted to a model.

| Census ID | Category | Source-to-model permutation |
|---|---|---|
| R9_2_515 | (Ising ⊠ PSU(2)_10)/(1+ψ⊠V10) | 0,5,4,3,2,1,6,8,7 |
| R9_2_748 | TY(C3)^S3, inversion action, trivial parity coherence | 0,1,6,7,2,4,5,8,3 |
| R9_2_1211 | TY(C3)^S3, inversion action, modified parity coherence | 0,6,7,2,4,5,8,1,3 |
| R9_2_1372 | Asaeda--Haagerup AH3 | 0,3,4,1,2,8,5,7,6 |
| R9_2_1373 | (Fib ⊠ Fib)^S3, action through factor swap | 0,4,5,1,3,8,7,6,2 |
| R9_2_1857 | Spin(8)_2 equivariantized by Dynkin triality C3 | 0,8,7,2,1,3,5,6,4 |
| R9_2_1983 | Ordinary-swap equivariantization of the equal half-E6 diagonal-fermion product | 0,1,3,5,8,7,6,4,2 |
| R9_2_2029 | Triality equivariantization of a Tannakian zest of Spin(8)_2 | 0,8,7,3,5,2,1,6,4 |

## Permutation and orthogonal equivariantization

Write S3=C3⋊C2. Its sign quotient acts on Fib⊠Fib by the canonical factor
permutation. Both fixed simple pairs (1,1) and (φ,φ) have three equivariant
lifts, indexed by the three irreducible S3 representations. The orbit
{(1,φ),(φ,1)} has stabilizer C3 and hence three lifts. This produces rank nine.
The fusion calculation in fib_s3.py is the finite-group character average
on each invariant Hom-space, over the exact field Q(ζ3). The canonical
permutation tensorator permutes the two multiplicity-one factor lines.

For TY(C3,χ,τ), take χ(a,b)=exp(2πiab/3) and τ=1/√3. Inversion preserves χ
and acts by actual unitary tensor functors. Gelaki--Naidu--Nikshych,
*Centers of graded fusion categories*,
[arXiv:0905.3117](https://arxiv.org/abs/0905.3117), Proposition 4.8, supplies
the entire orthogonal-group action, with identity tensor structures in the
standard skeleton. Pull it back along S3→C2. The base simples 1 and m are
fixed and each have three equivariant lifts; {a,a²} has three lifts, again
giving rank nine.

There is also a monoidal natural automorphism η of the identity, equal to
−1 on m and +1 on the pointed objects. Modify the composition constraint
for g,h∈S3 by η^{ε(g)ε(h)}, where ε is parity. This is a genuine coherent
action because ε(g)ε(h) is a normalized C2-valued two-cocycle and η is
invariant under inversion. The two choices produce R9_2_748 and R9_2_1211.
For the modified action the projective stabilizer representations at m
are linearized by the cochain i^{ε(g)}. The resulting factor on a fusion
line a⊗b→c is (−1)^{(p(a)+p(b)−p(c))/2} when g is odd. The exact character
average in ty_s3.py implements this formula on every line; no coherence is
inferred from associativity of the final tensor.

General simple-orbit/stabilizer and fusion formulas for equivariantization
are also given by Burciu--Natale, *Fusion rules of equivariantizations of
fusion categories*, [arXiv:1206.6625](https://arxiv.org/abs/1206.6625).

## A free diagonal fermion quotient

Use the standard unitary Ising category with fermion ψ and SU(2)_10 WZW
category, restricting the latter to its even labels V0,V2,…,V10. The
invertible V10 has twist −1 and centralizes every even label: its monodromy
with Vj is (−1)^j. Therefore ψ⊠V10 has a specified central bosonic lift,
and 1+ψ⊠V10 is a central connected separable algebra. Its action on the
18 simple objects is free, since Vj↦V(10−j) has no fixed even label. The
module category consequently has nine simple orbits and the tensor is the
ordinary orbit-sum quotient. ising_psu10.py applies the previously verified
project free-involution constructor and matches R9_2_515 exactly.

## Asaeda--Haagerup

Grossman--Snyder, *The Brauer-Picard group of the Asaeda-Haagerup fusion
categories*, [arXiv:1202.4396v2](https://arxiv.org/abs/1202.4396v2), Section
4.3, Table 3, identify the unitary AH3 category, the principal even part of
AH+1. The ancillary file
[AH3Modules](https://arxiv.org/src/1202.4396v2/anc/AH3Modules) supplies its
full nonunit multiplication table. ah3_source_data.json records only the
512 numerical nonunit coefficients, their output-first indexing, duality,
and the source digest. ah_model.py reconstructs the unit coefficients and
compares the complete tensor, giving R9_2_1372.

## Ordinary swap after fermion condensation

The detailed proof for R9_2_1983 is ordinary_swap.md, independently reviewed
in ../signed/ordinary_swap_audit.md. Its categorical input is the unitary
half-E6 category with its specified central fermion, using the local data
of Aasen--Lake--Walker, *Fermion condensation and super pivotal categories*,
[arXiv:1709.01941v2](https://arxiv.org/abs/1709.01941v2), Sections 7.1--7.2
and Appendix D.1. The established project equal-rotation diagonal-fermion
product theorem first gives a rank-six category Q. Ordinary factor swap,
with the identity equivariance of the diagonal algebra, acts coherently on
Q. Four objects are fixed and the other two are exchanged, so Q^{C2} has
rank nine. An explicit balanced multiplication shows that an equivariant
lift t of the residual fermion has t²=ε, the sign representation. Thus the
four invertibles form C4. Their centrality and the forgetful functor force
every remaining coefficient, up to a harmless choice of one orbit
representative. ordinary_swap.py replays the local certificate, the four
scalar checks, and all 486 forgetful tensor identities as well as the full
census comparison.

## Dynkin triality

The additional model R9_2_1857 is the C3-equivariantization of the standard
unitary WZW category Spin(8)_2. An actual order-three Hopf automorphism
permutes the three outer D4 nodes and descends to the fusion category.
Its only fixed simple objects are1 and the dimension-two object f=ω2;
f² is the sum of all four invertibles. These rules uniquely normalize the
fixed-channel traces, allowing the complete equivariant tensor to be
computed without unknown multiplicity-space actions. d4_triality.py
reconstructs the seed tensor from exact Weyl alternants in Q(ζ32) and the
Verlinde formula, then computes the equivariant tensor by character
averaging. The complete existence and trace proof is d4_triality.md.

A second model R9_2_2029 follows from an actual associative zest of the
same WZW seed. Both its grading group and its Tannakian current group
identify with additive F4, with triality acting by multiplication by t.
The cocycle λ(a,b)=t(ab)² and scalar associator correction1 give an
associative zest by Galindo--Mora--Rowell, arXiv:2311.17255, Proposition4.2.
The pointed subcategory admits an equivariant symmetric trivialization:
its C3 equivariantization is Rep(E) for an extension of C3 by V4, which
splits by Schur--Zassenhaus. Since λ is strictly triality-equivariant, the
actual tensor action descends through the zesting formulas. This changes
the two dimension-six objects into a dual pair. The categorical existence
and action proof is d4_zest_triality.md; the constructor and canonical
single-model record are d4_zest_triality.py and
d4_zest_triality_new_models.json. Both cocycle variants are retained in
d4_zest_triality_models.json without double counting the ring.

## Replay and scope

Run `python phase2/models/verify_models.py` from the research root. It reruns
each constructor, compares all recorded permutations in all coefficients,
checks fusion axioms, and writes replay_manifest.json. The known seven
phase-one models remain separate. Model files from the other phase-two
agents are not merged into this eight-model manifest.

folded_so3_diagnostic.json is explicitly not a model: it identifies
R9_2_920 with the formal fermionic fold of PSU(2)_34, which does not itself
give an ordinary fusion category. classical_dimension_leads.json is a
heuristic negative-search record. Neither file contributes a realization.
