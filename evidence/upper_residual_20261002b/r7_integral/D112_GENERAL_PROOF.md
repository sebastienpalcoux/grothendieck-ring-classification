# R7_3_386 and R7_3_966: a Singer-cycle obstruction

Both source tensors have dimension 112 and type (1^2,2^3,7^2), with
trivial universal grading. Their nontrivial invertible fixes the three
dimension-two objects and exchanges the two dimension-seven objects.

Suppose 
\(\mathcal C\) categorifies one of them. Solvability and trivial
universal grading force

\(\mathcal C=\mathcal D^{C_2}\).
The cyclic orbit formula gives

\[
\operatorname{FPdim}\mathcal D=56,\qquad \mathcal D:1^7,7.
\]

The seven invertibles form 
\(C_7\) and fix the remaining simple 
\(X\), which is self-dual because it is the only noninvertible.
Dimension and reciprocity give

\[
X^2=\sum_{g\in C_7}g+6X.
\]

In particular 
\(\mathcal D_{\rm ad}=\mathcal D\). The next solvable step is
therefore a 
\(C_7\)-equivariantization of a dimension-eight category

\(\mathcal E\). The canonical seven characters already account for
every invertible of 
\(\mathcal D\). Its unique dimension-seven simple must come from
a free orbit of seven invertibles: a fixed dimension-seven object
would contribute seven such objects and exceed dimension eight
in 
\(\mathcal E\). Thus 
\(\mathcal E=\mathrm{Vec}_A^\omega\), 
\(|A|=8\), with an order-seven automorphism free on every nonidentity
element of 
\(A\).

This forces 
\(A=C_2^3\). All seven nonidentity elements lie in one orbit and
have the same order. A group of order eight has an involution, so all
these elements have order two; a group of exponent two is abelian.
The induced order-seven element in 
\(\operatorname{GL}_3(2)\) is a Singer cycle.

The central 
\(\operatorname{Rep}(C_7)\) has unique lifts of its underlying
invertibles, because 
\(U(\mathcal D)=1\). Combining it with the outer action gives

\[
\mathcal C=(\mathrm{Vec}_{C_2^3}^{\omega})^H,
\qquad 1\to C_7\to H\to C_2\to1.
\]

The central 
\(\operatorname{Rep}(H)\) embeds fully faithfully in

\(\mathcal C\). The cyclic group 
\(C_{14}\) would have fourteen invertibles, so 
\(H=D_{14}\). A reflection must therefore conjugate the Singer
cycle to its inverse in 
\(\operatorname{GL}_3(2)\). This is impossible: the normalizer of
a Singer subgroup is 
\(C_7\rtimes C_3\), so its conjugation exponents are

\(1,2,4\) modulo seven, and never 
\(-1=6\).

The verifier independently enumerates all 168 invertible binary

\(3\times3\) matrices, constructs a Singer cycle, obtains its
normalizer of size 21 and checks every conjugation exponent. This
finite calculation and the abstract normalizer argument give the
same contradiction. No assumptions on 
\(\omega\), braiding or pivotality enter.

Structural references and their scope are recorded in
`STRUCTURAL_INPUTS.md`.
