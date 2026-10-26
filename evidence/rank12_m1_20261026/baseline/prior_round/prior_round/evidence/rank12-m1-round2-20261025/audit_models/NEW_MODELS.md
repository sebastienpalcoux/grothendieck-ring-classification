# Additional rank-twelve models from the positive audit

## R12_1_541 is an ordinary representation ring

Let

\[
G=\langle a,b\mid a^3=b^8=1,\;bab^{-1}=a^{-1}\rangle
  =C_3\rtimes C_8.
\]

This is a group of order 24. Its unitary representation category has eight
one-dimensional simples \(r_k\), \(k\in\mathbb Z/8\), with
\(r_k(a)=1\) and \(r_k(b)=\zeta_8^k\). There are four two-dimensional
simples \(X_j\), \(j\in\mathbb Z/4\), induced from the nontrivial
\(C_3\)-character and the stabilizer \(\langle b^2\rangle=C_4\)-character
\(b^2\mapsto i^j\). Clifford theory exhausts the irreducibles; alternatively,
their squared dimensions sum to \(8+4\cdot4=24\).

The exact fusion rules are

\[
r_kr_l=r_{k+l},\qquad r_kX_j=X_{j+k},\qquad
X_iX_j=r_{i+j}+r_{i+j+4}+X_{i+j}.
\]

The subscripts on \(r\) are modulo eight and those on \(X\) modulo four.
For the last identity, restriction to \(C_3\) has two trivial characters and
the two nontrivial characters. On the trivial part, \(b^2\) acts by
\(i^{i+j}\), so \(b\) has the eigenvalues \(\pm\zeta_8^{i+j}\).
The remaining orbit is the displayed two-dimensional irreducible.

In the ordered basis
\((r_0,\ldots,r_7,X_0,\ldots,X_3)\), the source-to-model permutation is

```
[0, 2, 6, 1, 7, 9, 11, 5, 3, 8, 10, 4]
```

All 1728 coefficients have been compared exactly. This supplies an ordinary
classical model; no assertion of categorical novelty is intended.

## General neutral-current associative C2 zesting

Let a unitary fusion category \(\mathcal C=\mathcal C_0\oplus\mathcal C_1\)
be faithfully \(C_2\)-graded. Let \(\widetilde h\in Z(\mathcal C)\) be a
unitary central invertible whose underlying object \(h\) lies in
\(\mathcal C_0\). There is a unitary fusion category on the same simple
objects with tensor product

\[
X_a\otimes_hY_b=(X_a\otimes Y_b)\otimes h^{ab}.
\]

No order-two assumption on \(h\) is needed. Indeed, define the normalized
object-valued two-cocycle by \(\lambda(1,1)=\widetilde h\) and unit values
otherwise. The only nontrivial object-level cocycle identity compares
\(\widetilde h\) with itself. The associativity maps exist: in a strict
unitary realization every preliminary comparison is an identity on either
the unit or \(\widetilde h\). Their pentagon defect is a scalar normalized
four-cocycle on \(C_2\). It is therefore supported only on \((1,1,1,1)\),
where it has a value \(\epsilon\in U(1)\). A normalized three-cochain
supported at \((1,1,1)\) has coboundary equal to its squared value at that
quadruple. A unit-modulus square root of the inverse defect removes it.
All modified coherence maps remain unitary. Rigidity follows from the
associative-zesting construction.

This is an application of Delaney–Galindo–Plavnik–Rowell–Zhang,
*Braided zesting and its applications*, arXiv:2005.05544, Definition 3.2,
Proposition 3.4 and Section 3.4. Equivalently, the final obstruction is in
\(H^4(C_2,U(1))=0\). A semionic central lift is permitted; its actual
pentagon defect must be used instead of the special boson/fermion formula.
Centrality in the based ring alone is insufficient.

The first-round sampler's order-two restriction was therefore an unnecessary
limitation of its discovery search. It did not invalidate its accepted
models. The expanded, categorically licensed search produced the above
classical ring R12_1_541 and no other new ring among 278 distinct candidates.

## Additional licensed central lifts used in that search

Every invertible of an orthogonal \(C_2\)-equivariantization of a TY category
has a central lift. Gelaki–Naidu–Nikshych, *Centers of graded fusion
categories*, arXiv:0905.3117, Proposition 4.1 gives central invertibles
\(X_{a,\varepsilon}\) over every \(a\in A\), with
\(\varepsilon^2=\chi(a,a)^{-1}\). A strict orthogonal involution fixing
\(a\) preserves both its bicharacter half-braiding and \(\varepsilon\).
Thus it fixes this central object. Its two equivariant structures give the
two invertibles over \(a\) in the equivariantization. The action's optional
odd TY coherence is trivial on the underlying invertible \(a\). The
canonical braided functor \(Z(\mathrm{TY})^{C_2}\to Z(\mathrm{TY}^{C_2})\)
supplies the required lifts. They are unitary.

The existing pseudo-PSU(2)6 factors also have their published and explicitly
checked semionic central lift. It is used only as a positive construction
premise, never as a classification assertion about arbitrary categories.
