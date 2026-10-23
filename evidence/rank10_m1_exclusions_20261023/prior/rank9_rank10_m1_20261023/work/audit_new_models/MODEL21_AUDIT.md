# Independent categorical audit of the model for R10_1_21

**Verdict: accepted as an actual unitary categorification.** The construction
is the central condensation of the canonical permutation equivariantization
of \(\mathrm{PSU}(2)_6\boxtimes\mathrm{PSU}(2)_6\) by
\(A=1\oplus(f,f)_-\). The nontrivial fixed-point calculation gives the
invertible group \(C_2\times C_2\), as required for R10_1_21.

The categorical argument in work/resolve_rank10_quadratic/model21.tex was
checked independently, including the balanced tensor product rather than
only associativity of a proposed fusion tensor. The exact replay is:

    python work/audit_new_models/verify_model21.py

It uses only the standard library and writes model21_audit.json. It checks
the fixed-point calculation with integer matrices, independently reconstructs
all 196 source fusion products of the permutation equivariantization, checks
that the stated free-module map respects every product, and verifies all
1000 coefficients against the original tensor under the stated based map.
It passed.

## The central algebra and the fixed-point square

In the standard unitary even \(\mathrm{SU}(2)_6\) category, \(f\) is the
transparent fermion. The subcategory on \(1,f\) is \(\mathrm{sVec}\), with
trivial associator on the pointed skeleton. Thus \(h=(f,f)_-\) is transparent,
has order two, and has self-braiding \(+1\). It generates a central Tannakian
copy of \(\operatorname{Rep}(C_2)\), so the regular algebra \(A=1\oplus h\)
exists. Its module category is a unitary fusion category. The minus sign in
the equivariant structure does not change the self-braiding of \(h\).

Let \(X=(1,f)\oplus(f,1)\), with basis lines \(e_1,e_2\). The permutation
equivariance is \(P=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\).
Write \(R=iJ\), where
\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]
Then \(R^2=1\) and \(PR=-RP\), exactly the equivariance condition for a
right \(h_-\)-action. Its negative gives the other simple module.

The half-braiding \(c_{h,X}\) is minus the identity on both graded lines.
Therefore the left action used in the balanced tensor product is \(-R\).
The balancing relation is the image of \(R\otimes1+1\otimes R\). Since this
operator is Hermitian, its cokernel identifies with its kernel. Removing the
nonzero scalar \(i\), the kernel is exactly
\[
u=e_1e_1+e_2e_2,\qquad v=e_1e_2-e_2e_1.
\]
The diagonal equivariance \(P\otimes P\) has eigenvalues \(+1,-1\) on
\(u,v\), respectively. Their grades are \(1,(f,f)\), so the underlying
equivariant object is \(1\oplus h_-\).

The remaining right action is \(1\otimes R\), with
\(u\mapsto iv\), \(v\mapsto-iu\). Replacing \(v\) by \(iv\) gives the regular
right \(A\)-module. Thus the corresponding invertible module \(g\) satisfies
\(g^2=1\). The sign object \(s\) exchanges the two module structures, so
the four invertibles are \(1,s,g,sg\), all of order two.

This direct calculation is necessary: identifying the underlying pointed
permutation fusion category with \(\operatorname{Rep}(D_8)\) alone does not
record the central half-braiding used in the module tensor product.

## The remaining fusion rules are forced

There are six free \(h\)-orbits and two fixed simples in the source. The
fixed simples each split into two inequivalent modules; their stabilizer is
cyclic of order two. This gives rank ten and the stated dimension profile.

For \(a=F(p_{1x})\), \(b=F(d_x^+)\), the source products yield
\[
\begin{aligned}
b^2&=1+a+ga+b+sb+gb+sgb,\\
a^2&=1+s+a+ga+b+sb,\\
ab&=a+b+sb+gb+sgb.
\end{aligned}
\]
The source free-module images also give \(sa=a\), identify the two-element
orbit \(\{a,ga\}\), and identify the four distinct objects
\(\{b,sb,gb,sgb\}\). The distinctness follows from their disjoint underlying
source supports, together with the inequivalent two fixed-point modules.
The displayed products, the invertible action, and commutativity determine
every fusion coefficient. The replay verifies this against every source
product and against R10_1_21.

The model-to-input basis map is
\[
(0,9,1,2,3,8,6,7,5,4)
\]
for the model basis \((1,s,g,sg,a,ga,b,sb,gb,sgb)\). All indices are zero
based. This audit makes no assertion about an R10_1_114 model.
