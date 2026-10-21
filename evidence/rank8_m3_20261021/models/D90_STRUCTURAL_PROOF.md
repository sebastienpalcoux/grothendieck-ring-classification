# A structural obstruction in dimension 90

**Theorem.** Neither R8_3_2904 nor R8_3_3082 admits a complex fusion categorification. More generally, a fusion ring of dimension 90 and type(1,2;2,4;6,2), whose adjoint subring is the whole ring and whose unique nontrivial invertible fixes every noninvertible, is not categorifiable.

The exact verifier `d90_structural.py` checks these hypotheses against all 512 coefficients of each source tensor. Its certificate is independent of the general dimension-order linear-programming exclusions of the same two rings.

The recovered deterministic receipt is `d90_structural.json`. Default execution
is read-only; `--write` is required to replace the receipt. Both
`python d90_structural.py` and `python -O d90_structural.py` rederive the fusion
axioms, all64 positive dimension-character identities, the complete adjoint
closure, both sign actions, all closed based subrings, and the forced
dimension45 type directly from each source tensor. The categorical theorems
and cohomological argument below are explicit mathematical inputs, not claims
that the program independently formalizes those theorems.

Suppose C categorifies such a ring. Dong, *Classification of certain weakly integral fusion categories*, [arXiv:2103.04553v3](https://arxiv.org/pdf/2103.04553), Corollary 4.16, p. 17, states that every fusion category of dimension 90 is solvable. This is the result needed here; dimension 90 has three distinct prime divisors, so the ENO two-prime solvability theorem alone would not suffice.

By Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, [arXiv:0809.3031v2](https://arxiv.org/pdf/0809.3031), Proposition 4.4, its final step in a solvable construction is a prime-order extension or equivariantization. Its trivial universal grading excludes a nontrivial extension. An equivariantization by Cp contains Rep(Cp), so its two invertibles force p=2. Write C=D^C2. The two equivariant lifts of a fixed simple of D are exchanged by the sign representation g. Since g fixes all six noninvertible simples of C, each of those comes instead from a free orbit of size 2. The four simples of dimension 2 therefore give eight invertibles of D, and the two simples of dimension 6 give four simples of dimension 3. Including the unit, D has type(1,9;3,4) and dimension 45.

Every integral fusion category of dimension 45 is group-theoretical by Jordan–Larson, *On the classification of certain fusion categories*, [arXiv:0812.1603v2](https://arxiv.org/pdf/0812.1603), Theorem 1.1: the only possible non-group-theoretical odd case has p dividing q+1, which fails for p=5,q=3. In fact every integral category of dimension 45 is pointed. To see this in the group-theoretical presentation C(G,ω,H,ψ), note that all groups G of order 45 are abelian. If G is cyclic, every H has trivial Schur multiplier. Otherwise G=C3²×C5. Any subgroup with nontrivial Schur multiplier contains the full Sylow 3 subgroup and has index 1 or 5. Restriction to H is injective on the 3-primary part of H³(G,C×), since restriction followed by corestriction multiplies by the index. Hence the condition [ω]|H=0 kills the 3-primary part of [ω]. The stabilizer multiplier contributions of ω are therefore 5-primary, while H²(H,C×) is 3-primary. The ψ contributions cancel because conjugation in G is trivial. Every stabilizer multiplier is trivial, so all simples are one-dimensional. This contradicts the forced four 3D simples of D.

The standard simple-object formula used here is FPdim(g,π)=[H:H∩gHg⁻¹]dimπ, with π a projective representation for the stabilizer multiplier. See Gelaki–Naidu, *Some properties of group-theoretical categories*, [arXiv:0709.4326](https://arxiv.org/pdf/0709.4326), §5.1, for the multiplier and simple-object description.

For clarity, the cancellation of the two ψ contributions is a cohomology
statement, not pointwise equality of cochains. There is also a direct gauge
argument for the primary-component step. Choose a μ5-valued representative
of the remaining 5-primary class [ω]. For a noncyclic H, multiplication by5
on H²(H,C×) is invertible. The coefficient exact sequence therefore makes
H³(H,μ5) inject into H³(H,C×), so this representative admits a μ5-valued
trivialization on H. The displayed stabilizer cocycle is then μ5-valued;
its class vanishes because H²(H,C×) is 3-primary. Changing the trivialization
by a 2-cocycle does not change that class: its conjugation difference is
trivial when G is abelian. Thus the conclusion does not depend on an
unproved compatibility of cochain choices.

This proof concerns all complex fusion categories. It does not assume a braiding, unitarity, or a chosen pivotal structure.

