# Independent categorical review of the R11_1_179 model

The proposed C3-equivariantization is valid. This review concerns existence and
coherence; the independent Hom-character tensor replay remains a separate check.

Izumi, arXiv:1512.04288v2, Definition 4.8, Theorem 4.9 and Lemma 6.13 give the
Q8 admissible tuples `(π,π,j,-ζj,χ,0)`. A unitary quaternionic matrix W intertwining
π with a group automorphism φ and commuting with j preserves the tuple, including
j2=-ζj. The accepted lower-rank `NG_ACTIONS.tex` spells out the converse
reconstruction on generators S_g and T(v). Its argument supplies actual tensor
functors and does not depend on φ having order two.

For the proposed W=-(1+I+J+K)/2, W³=1 and φ³=1. Consequently the reconstructed
functor cubes to the identity on all generating morphisms and hence on the
category. The identity compositors satisfy the C3 action coherence. This is a
categorical action, not just an action on the based ring.

For fixed pointed outputs 1,-1 in ρ², the generators S_1,S_-1 are fixed, so their
equivariant phases are trivial. Right absorption introduces no extra phase:
π(±1) is scalar and commutes with W. The action on Hom(ρ,ρ²) has the two
nontrivial C3 eigencharacters, since W³=1 and tr(W)=-1. A convention replacing W
by W^-1 exchanges these eigencharacters and leaves the fusion rule unchanged.
Thus the two noninvertible outputs in P_a P_b are precisely P_(a+b+1) and
P_(a+b+2). Fixed/free pointed-fibre counting then gives all other coefficients.
The unit occurrence forces P_a*=P_-a, as stated.

The three Izumi choices ζ produce the same displayed fusion tensor. No claim of
exhausting all associators for R11_1_179 follows or is needed.
