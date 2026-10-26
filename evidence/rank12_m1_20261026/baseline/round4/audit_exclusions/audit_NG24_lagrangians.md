# Audit of the near-group dimension-24 Lagrangian argument

The proposed lemma is valid: every C2 equivariantization of a complex
fusion category with near-group rules NG(D8,2) or NG(Q8,2) is
group-theoretical. The same reasoning applies to a faithful C2 extension,
using the canonical action on the center and GNN Corollary 3.10.
This is a categorical lemma; binding the rank-12 Morita branches to these
near-group rules is handled separately by the D48 proof.

The general-complex scope requires the following explicit bridge. The
near-group category has FPdim 24=2³*3, hence is solvable by ENO Theorem
1.6, in particular weakly group-theoretical. GHR Theorem 5.20 therefore
provides a unitary realization of every such original category. Only
after this bridge may one invoke Izumi's complete unitary classification.
Izumi–Tucker Theorem 3.2 supplies all six representatives, three for each
of D8 and Q8, distinguished by their canonical positive pivotal
indicators. Each is Morita equivalent to Vec(S4,omega), with omega
cohomologous to inflation of a normalized cocycle on S4/V4=S3.
The construction paper alone would not supply the general-complex premise.

Replace omega by its actual normalized inflated representative, which
does not change the braided equivalence type of the center. Naidu–Nikshych
Theorem 4.12 describes every Lagrangian subcategory of this twisted double
by a normal abelian subgroup H and an invariant alternating
omega-bicharacter on H. The only normal abelian subgroups of S4 are 1
and V4. For h in V4 every term in the formula for beta_h(x,y) contains
h or a conjugate of h as one argument of omega. Inflation and
normalization make all such terms equal to one. Consequently Definition
4.5 reduces to an ordinary alternating bicharacter, and the correction
factor in Definition 4.6, equation (27), is also one for all x,y.

There is one bicharacter for H=1. On V4=F2² there are exactly two
alternating bicharacters: the zero form and the unique nonzero
determinant form. Both are invariant under the full GL2(F2), hence under
S4 conjugation. Thus the center has exactly three Lagrangian
subcategories. This is a complete count, not just three examples; the
twisted classification theorem exhausts all possibilities.

Any categorical C2 action induces a permutation action of C2 on these
three subcategories. An involution acting on an odd set has a fixed
point. GNN Corollary 3.11 says precisely that a C2 equivariantization
is group-theoretical if the center has a stable Lagrangian subcategory.
No choice of coherent pointwise action on that subcategory is needed
beyond stability in that theorem. For extensions, Corollary 3.10 gives
the identical conclusion from the canonical action on the center of
the neutral component. Morita equivalence transports the set of
Lagrangians and its permutation action; the action need not preserve
one preselected pointed presentation.

Primary statements and formulas checked:

- Izumi–Tucker, Theorem 1.2, Section 3.2 and Theorem 3.2:
  <https://arxiv.org/html/1908.01655v1>.
- Naidu–Nikshych, Definitions 4.5–4.6 and Theorem 4.12:
  <https://arxiv.org/pdf/0705.0665>.
- Gelaki–Naidu–Nikshych, Corollaries 3.10–3.11:
  <https://arxiv.org/pdf/0905.3117>.
- ENO, Theorem 1.6: <https://arxiv.org/abs/0809.3031>.
- GHR, Theorem 5.20: <https://people.tamu.edu/~rowell/GHRarx1.pdf>.

This audit finds no categorical gap in this particular odd-Lagrangian
argument. It does not assert group-theoreticity for arbitrary dimension-24
categories: the specific near-group classification and the three-element
Lagrangian set are essential.
