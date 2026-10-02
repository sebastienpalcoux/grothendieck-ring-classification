# R7_2_50 and R7_2_280: the other dimension-96 branch

The verified source premises are dimension 96, type

\(1^2,2,3^2,6^2\), trivial universal grading, and a sign invertible
which fixes the dimension-two simple but exchanges **both** the
dimension-three and dimension-six pairs.

Solvability forces 
\(\mathcal C=\mathcal D^{C_2}\). The orbit formula now gives

\[
\operatorname{FPdim}\mathcal D=48,\qquad \mathcal D:1^3,3,6.
\]

There is no faithful grading of

\(\mathcal D\). A 
\(C_2\) grading would have neutral dimension 24; all three
invertibles are neutral, so this dimension has the form

\(3+9b+36c\), impossible modulo nine. A

\(C_3\) grading would have neutral dimension 16; the number of
neutral invertibles is three or one, giving

\(3+9b+36c\) or

\(1+9b+36c\), again impossible. Any nontrivial group of order
dividing 48 is solvable and has a prime cyclic quotient of order
two or three. Thus 
\(U(\mathcal D)=1\).

The next step is therefore

\(\mathcal D=\mathcal E^{C_3}\), with

\(\operatorname{FPdim}\mathcal E=16\).
The three canonical characters exhaust the invertibles of

\(\mathcal D\). Its single dimension-three object must come
from a free orbit of three invertibles; a fixed dimension-three
object would give three dimension-three equivariants. Its single
dimension-six object must likewise come from an orbit of three
dimension-two objects; a fixed dimension-six object would give
three equivariants and cannot occur in dimension sixteen. Thus

\[
\mathcal E:1^4,2^3,
\]

and the order-three action cycles the three nonidentity invertibles
and the three dimension-two simples. The invertible group is

\(V_4\), since 
\(C_4\) has no order-three automorphism.

The permutation action of these invertibles on the three other
simples is trivial. Its image is either trivial or a subgroup of
order two in 
\(S_3\). The order-three outer action normalizes this image and
cycles the three simples, which is incompatible with a nontrivial
order-two image. Hence all four invertibles fix every dimension-two
simple 
\(X\). Reciprocity and dimensions imply

\[
XX^*=\sum_{g\in V_4}g.
\]

Consequently the adjoint category is precisely

\(\mathrm{Vec}_{V_4}^{\omega}\), the universal grading has order
four, and its three nonneutral components each have rank one and
dimension four. The order-three symmetry permutes them, so the
grading group is 
\(V_4\).

A rank-one left module forces

\(\omega\) to be a coboundary: its scalar module associativity
is a two-cochain 
\(\psi\) with 
\(\delta\psi=\omega\). Rank-one left modules over

\(\mathrm{Vec}_{V_4}\) are classified by

\(H^2(V_4,\mathbb C^\times)=C_2\), so there are just two
equivalence classes.

But the three nonneutral grading components are pairwise
inequivalent as left modules. Indeed, if two invertible bimodules
have the same left module, their relative quotient has the regular
left-module type, of rank four; see the elementary transport-of-
right-action argument in `STRUCTURAL_INPUTS.md`. That quotient is
the third nonneutral grading component, of rank one, a contradiction.
Three different rank-one left modules cannot be chosen from two
classes. This excludes both rings over the complex numbers.

This argument uses no pivotal structure, no classification of
centers, and no assumption that distinct right actions define
distinct left modules: the relative quotient is exactly what
rules out repetition of a left-module class.
