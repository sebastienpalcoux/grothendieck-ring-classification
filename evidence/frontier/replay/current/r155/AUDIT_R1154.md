# Independent audit of the conditional R1154 rank-seven route

29 October 2026. This audit concerns the conditional route in
`../r1154/CONDITIONAL_RANK7_ROUTE.md`, not the existence of its proposed algebra.
R8_3_1154 remains unresolved.

## Categorical premise: verified, with a precise primary reference

The needed statement is explicitly in V. Ostrik, *Pivotal fusion categories
of rank 3*, arXiv:1309.4822v1, Remark 2.19, pp. 7–8, following Corollary 2.16:

https://arxiv.org/pdf/1309.4822

The remark treats an indecomposable multifusion category with unit components
1_i and identifies the complexified corner Grothendieck algebras with
End(I(1_i)), and the corner bimodules with Hom(I(1_i),I(1_j)). The identification
respects the unit idempotents. It then gives the formulation for module
categories and their Lagrangian algebras. Its hypotheses include spherical
center and trivial twists on the two Lagrangian algebras. The last paragraph
of that remark explicitly proves these hypotheses automatic when the center
has positive dimensions. This is exactly the scope needed after the source's
positive-existence gate.

Here is the resulting finite-dimensional argument, making clear why a numerical
based module alone would not suffice. Suppose C is the positive category and
M is an actual indecomposable C-module category. Put D=C*_M and identify centers.
Let L_C=I_C(1), and let L_M be the image of I_D(1) in Z(C). Write

    L_C = sum_E (dim E) A_E,
    L_M = sum_E m_E A_E + sum_{Z not in support(L_C)} n_Z Z.

Apply Remark 2.19 to the linking multifusion category of C and M. On each common
simple central summand A_E, the cross-corner Hom space is the tensor product of
the defining dim(E)-dimensional module and an m_E-dimensional multiplicity
space. Therefore m_E is exactly the multiplicity of E in K0(M)_C. Orientation
may exchange a module with its contragredient; in this case all the relevant
source characters are self-dual, so this does not change the labels or numbers.

The dual algebra is a direct sum of matrix blocks of sizes m_E and n_Z. Thus

    rank(D) = sum_E m_E^2 + sum_Z n_Z^2.

Its action on K0(M)_C has kernel exactly the blocks with n_Z>0. If there are
no such summands, the action is faithful and identifies K0(D)_C with the full
commutant of K0(C)_C acting on K0(M)_C. This proves the faithfulness assertion;
it is not an inference from a coincidental equality of dimensions.

## Application to the first module branch

For the chi_4 branch, the multiplicities are (1,1,2,0,1). The corresponding
central dimensions are

    1, 161+72 sqrt(5), 135+60 sqrt(5), 27+12 sqrt(5), 108+48 sqrt(5).

Their weighted sum is

    1+(161+72 sqrt(5))+2(135+60 sqrt(5))+(108+48 sqrt(5))
      =540+240 sqrt(5)=FPdim(C).

Since L_M has exactly that dimension, positivity forces every n_Z=0.
Consequently the rank of D is 1+1+4+1=7, and its action is the full
seven-dimensional commutant, as claimed.

The dual block formal codegrees are D,D',4,5. One should distinguish the last
formal codegree 5 from the number 10 in the replay trace formula. The remaining
one-dimensional dual block acts on a two-dimensional source representation, so
its trace on K0(M) is twice its scalar; dividing that matrix trace by 10 gives
the required scalar divided by 5. The script's normalization is correct.

## Other proof checks

The six-vertex Gram derivation, the free action of g, the two missing-line
characters, and the finite commutant enumeration are consistent with the stated
conditional setup. The exclusion of g from a connected algebra uses an actual
simple regular module fixed by g, hence a rank-one module for the nontrivially
associated pointed C2 category; this is a valid contradiction.

The third-indicator coefficient comparison also uses a legitimate field
separation: the indicators lie in Q(zeta_3), whereas delta is in Q(sqrt(5)),
and the two fields have intersection Q. The saturation of the triangle
inequality forces t_1=t_2=1 and t_5=2. Reducing t_3+2t_6=9 in Z[zeta_3]/2,
which is F_4, indeed forces t_3=1 and then t_6=4.

The verifier `../r1154/verify_conditional_rank7.py` was read and replayed
independently in an ordinary Python process. It passed the source hash, Gram
matrix, all module products, duality transposes, complete commutant dimension,
trace and norm formulas, bounded norm-one enumeration, the two orthonormal
bases, and the sole integral nonnegative rank-seven tensor. It uses explicit
exceptions rather than assertions. No associator or algebra structure is
constructed by these tests.

## Scope

The conditional theorem is valid for an actual connected separable algebra
1+X4 whose module category realizes the chi_4 branch. Neither the existence of
that algebra nor the choice of branch has been proved. The second branch also
survives. The rank-seven ring is therefore a necessary conditional Morita
partner, not a model or a new exclusion of R1154.

Additional primary cross-check: G. Schaumann, *Traces on module categories over
fusion categories*, arXiv:1206.5716v3, Proposition 5.8, states that all module
categories over a pseudo-unitary fusion category have the positive module trace.
K. Shimizu, arXiv:1801.02493v2, Theorem 5.12 and Corollary 5.13, independently
identify the dual character/Grothendieck algebra with End of the corresponding
central adjoint algebra. Ostrik Remark 2.19 is the direct reference for the
specific cross-corner and multiplicity statements used here.
