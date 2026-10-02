# R7_3_398 and R7_3_478: inversion in a pointed Brauer–Picard group

The source tensors have dimension 54 and type

\(1^2,2^4,6\). Their universal grading is trivial, and their
nontrivial invertible fixes every noninvertible simple.

Assuming a categorification, solvability forces an initial

\(C_2\) equivariantization. Its de-equivariantization

\(\mathcal D\) has dimension 27 and type

\(1^9,3^2\). The order-two action fixes only the identity among
the nine invertibles and exchanges the two dimension-three objects.

Let 
\(A\) be the invertible group of 
\(\mathcal D\); it has order nine and is abelian. Its action on
the two remaining objects is trivial, since a group of odd order
has no nontrivial image in 
\(S_2\). For either remaining simple 
\(X\), reciprocity and dimensions give

\[
XX^*=\sum_{a\in A}a.
\]

Thus 
\(\mathcal D_{\rm ad}=\mathrm{Vec}_A^\omega\), and

\(\mathcal D\) is faithfully graded by 
\(C_3\), with two rank-one nonneutral components. Their existence
forces 
\([\omega]=0\), by the scalar module pentagon.

Write 
\(T\) for the outer order-two tensor action. Its automorphism on

\(A\) is fixed-point-free off zero, so it is inversion: for its
endomorphism 
\(\tau\), 
\(\tau-1\) is invertible and

\((\tau+1)(\tau-1)=0\), hence 
\(\tau=-1\).
It also exchanges the two nonneutral components, so it acts by
inversion on the grading 
\(C_3\).

The restriction of 
\(T\) to 
\(\mathrm{Vec}_A\) has a tensorator class

\(\eta\in H^2(A,\mathbb C^\times)\).
Inversion acts trivially on this group, identified with alternating
bicharacters of 
\(A\). Since 
\(T^2\) is tensor-isomorphic to the identity, its restricted
class is 
\(\eta+(-1)^*\eta=2\eta=0\).
For an order-nine group the cohomology group is odd-primary
(trivial for 
\(C_9\), and 
\(C_3\) for 
\(C_3^2\)), so 
\(\eta=0\).

Under

\[
\operatorname{BrPic}(\mathrm{Vec}_A)=O(A\oplus\widehat A),
\]

this restricted action is the scalar isometry 
\(-I\), which is central. It therefore fixes each invertible
bimodule class under conjugation. Let 
\(b\) be the class of one nonneutral component. Graded
multiplication gives 
\(b^3=1\), whereas the outer symmetry sends the component to
the inverse component, giving 
\(b=b^{-1}\). Hence 
\(b=1\).
This is impossible: the identity bimodule has regular left rank
nine, while this component has rank one.

All possible tensorators of the outer action were retained before
the order-two cohomology constraint removed them. The proof therefore
excludes arbitrary complex fusion categorifications, rather than only
ones with a chosen strict action or trivial associator at the outset.
See `STRUCTURAL_INPUTS.md` for the primary structural references.
