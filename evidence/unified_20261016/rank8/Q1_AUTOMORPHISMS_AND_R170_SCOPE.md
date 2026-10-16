# The automorphism group of the known 2D2 category and R8_2_170

This is a scoped result: it proves a unitary obstruction for R8_2_170,
not a general nonexistence theorem for this fusion ring.

Let Q be the known unitary 2D2 category. In the construction of
`R37_CONSTRUCTION.md`, put T=Ad(b)|_Q. Then T swaps r and gr and
fixes g. Moreover

    T² = Ad(g)

in the group of tensor autoequivalences modulo tensor natural
isomorphism. Grossman, arXiv:1612.07185, Lemma 4.1, proves that
Ad(g) exchanges the two inequivalent Q-systems on 1+r. Therefore
Ad(g) is nontrivial, and T has order exactly four.

Let phi be the automorphism of P fixing M and sending lambda to -lambda,
and put S=Ad(phi)|_Q. Grossman Lemma 4.2 proves S is outer. It fixes
all simple labels, has order two, and is independent of Ad(g).
The factor automorphisms b and phi commute (check M and lambda), hence
T and S commute. They generate C4 x C2: an odd power of T moves r,
whereas S fixes r; S is neither the identity nor T²=Ad(g).
Grossman Theorem 4.19, in its proof on printed p. 44, gives
|Aut_tensor(Q)|=8. Consequently

    Aut_tensor(Q) = <T,S> = C4 x C2,
    Out(Q) = C2 x C2.

The label-fixing subgroup is <T²,S>. Every label-swapping tensor
autoequivalence is T^{2k+1}S^e and has square Ad(g), not the identity.
Thus the label flip has no involutive tensor-autoequivalence lift.

For R8_2_170, the neutral 2D2 subring is on zero-based labels
(0,5,6,7), with g=5 and r=6. An odd invertible, for example u=3,
has u²=1 and conjugates r to gr. In any unitary categorification,
the neutral subcategory is tensor equivalent to Q by the unitary
classification of Edie-Michell–Izumi–Penneys, *Classification of
Z/2Z-quadratic unitary fusion categories*, Quantum Topology 16 (2025),
493–568, Theorem 3.31 (the arXiv numbering is different).
Then Ad(u)|_Q would swap the noninvertibles and square to the identity,
contradicting the preceding calculation.

Therefore R8_2_170 has no unitary categorification. The argument also
excludes a categorification whose neutral 2D2 category is Galois
conjugate to Q: apply the inverse Galois automorphism to the entire
category and use the same algebraic automorphism-group obstruction.

It does not exclude a hypothetical categorification whose neutral
2D2 category is not Galois conjugate to Q. The two-dimension Galois
pseudo-unitarity theorem supplies pseudo-unitarity, not unitarity;
it cannot fill this gap. The published 2D2 classification explicitly
retains a unitary hypothesis and flags its tetrahedral-symmetry step
as an obstacle to treating general fusion categories.

Primary sources:
- https://arxiv.org/pdf/1612.07185, Lemmas 4.1–4.2 and Theorem 4.19.
- https://arxiv.org/pdf/2201.11901, §3 and Theorem 4.1.
- https://ems.press/content/serial-article-files/51094, Theorem 3.31.
