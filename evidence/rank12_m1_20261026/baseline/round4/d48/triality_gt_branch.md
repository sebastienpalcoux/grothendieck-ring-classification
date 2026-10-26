# The group-theoretical half of the dimension-twelve triality classification

## Lemma

Every group-theoretical complex categorification of R_(3,V4), of type (1^4,2^2), has exactly three Lagrangian subcategories in its Drinfeld center. Consequently every equivariantization of such a category by a finite 2-group is group-theoretical.

Together with `triality_soft_automorphisms.md`, this proves the following branch criterion: if T has R_(3,V4) fusion rules and a group P of order four acts on T, then either T^P is group-theoretical or T^P is not multiplicity-free.

## Exhausting the group-theoretical categories

Jordan–Larson, Theorem 1.4, gives exactly six tensor-equivalence classes categorifying R_(3,V4). Their Theorem 1.1 gives exactly three non-group-theoretical classes of dimension twelve. All three have this ring. Therefore it suffices to exhibit three pairwise inequivalent group-theoretical categories with the ring.

Let H be an order-two subgroup of the normal Klein four subgroup V in A4, let pi:A4->C3=A4/V, and let kappa generate H³(C3,C*). For j=0,1,2 take

    T_j = C(A4, pi*(kappa^j), H, 1).

These are genuine unitary group-theoretical categories. The cocycle is normalized and inflated from C3, so it is identically one whenever any argument lies in V; in particular the subgroup algebra is defined without any adaptation.

The H double cosets in A4 have sizes 2,2,4,4, with stabilizers H,H,1,1. Thus the simple dimensions are 1^4,2^2. The invertibles form V/H times H*=C2 times C2: the neutral V-sector has trivial cocycle and V is abelian. The two outer cosets lie in the two nontrivial C3 grades and supply one simple each. Grading and dimensions then force rho²=2 rhobar, rhobar²=2 rho, and rho rhobar=sum(V4), with all invertibles fixing rho and rhobar. Hence the fusion ring is R_(3,V4).

The three categories are inequivalent, as can be seen directly from the third Frobenius–Schur indicator. For an outer representative g, the stabilizer is trivial and both elements of gH are 3-cycles. Schauenburg's adapted-cocycle formula (Theorem 4.2 in arXiv:1502.02906) gives

    nu_3(rho)=nu_3(rhobar)=2 zeta_3^(-j).

Indeed, the two summands are pi_(-3)(r), and for pi(r)=1 or2 the cyclic cocycle contributes zeta_3^(-j*pi(r)^2)=zeta_3^(-j). These three values are distinct. This use of the indicator is legitimate for tensor equivalence: the categories are pseudo-unitary and their canonical positive spherical structure is unique. The 2017 erratum to Schauenburg concerns passing from adapted to arbitrary cocycles; these cocycles are already adapted, so its corrections do not enter (and their relevant factors would be one here anyway).

This proves that the three T_j exhaust the group-theoretical categorifications of the ring. No model construction is being substituted for a missing classification: the six-category theorem and the three-category non-group-theoretical theorem are explicit premises.

## Three Lagrangians

The center of T_j is braided equivalent to Z(Vec_(A4)^(pi*kappa^j)). The only normal abelian subgroups of A4 are 1 and V. The Naidu–Nikshych classification of Lagrangians applies exactly as in `ng24_lagrangian_lemma.md`: inflation makes every twisting correction on V trivial. There are precisely two alternating bicharacters on V=F2², and both are invariant under the C3 conjugation action. The subgroup V therefore contributes two Lagrangians and the trivial subgroup contributes one, for a total of three.

A finite 2-group acting on a set of three elements has a fixed point: its nontrivial orbit sizes are powers of two. Tensor autoequivalences act on the Lagrangians of the center. The stable-Lagrangian criterion for equivariantizations (Gelaki–Naidu–Nikshych, Corollary 3.11) then proves the assertion for every 2-group action, including actions with nontrivial coherence data.

## Primary references

- Jordan–Larson, *On the classification of certain fusion categories*, Theorems 1.1 and 1.4: https://ems.press/content/serial-article-files/30464 .
- Schauenburg, *A higher Frobenius–Schur indicator formula for group-theoretical fusion categories*, adapted-cocycle Theorem 4.2 and cyclic inflation Proposition 5.2 in the preprint: https://arxiv.org/pdf/1502.02906 .
- Schauenburg, erratum, https://link.springer.com/content/pdf/10.1007/s00220-016-2770-0.pdf .
- Naidu–Nikshych, *Lagrangian subcategories and braided tensor equivalences of twisted quantum doubles of finite groups*, Theorem 4.12: https://arxiv.org/pdf/0705.0665 .
- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, Corollary 3.11: https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf .
