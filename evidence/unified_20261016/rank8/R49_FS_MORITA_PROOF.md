# R8_1_49: a pivotal parity obstruction followed by inverse Morita duality

## Theorem

The source ring `R8_1_49` has no fusion-category categorification over the complex numbers. The proof assumes neither unitarity nor a pivotal structure on an initial hypothetical categorification.

Its compact-JSON tensor SHA-256 is

`a5cefbf544001818e1e5c6e5bde951601eaf35f3d71034a252df1b7de751ea85`.

## 1. A general pivotal parity lemma

Let \(\mathcal C\) be a pivotal fusion category over \(\mathbb C\). Suppose \(X\) is a self-dual simple, and write \(\epsilon=\nu_2(X)\in\{1,-1\}\). If a self-dual simple \(S\) occurs with odd multiplicity in \(X^{\otimes n}\), then

\[
\nu_2(S)=\epsilon^n.
\]

Here no braiding or positivity is required. To prove the statement, use pivotal coherence to suppress associativity and double-dual identifications. If \(f:X\to X^*\) is a nonzero self-duality, its pivotal transpose satisfies \(t(f)=\epsilon f\). The tensor word consisting of \(n\) identical factors is a palindrome, so

\[
F=f^{\otimes n}:X^{\otimes n}\longrightarrow(X^{\otimes n})^*,
\qquad t(F)=\epsilon^nF.
\]

Duality reverses the factors, but all factors and all copies of \(f\) are identical. Thus this construction uses no interchange of different objects and no braiding.

On the \(S\)-isotypic block, write this nondegenerate form as \(f_S\otimes B\), where \(t(f_S)=\nu_2(S)f_S\) and \(B\) is a nondegenerate bilinear form on the ordinary complex multiplicity space. Transposition gives

\[
B^t=\frac{\epsilon^n}{\nu_2(S)}B.
\]

A nondegenerate alternating bilinear form has even dimension. If the multiplicity is odd, the displayed ratio must be \(+1\), proving the assertion. Nondegeneracy on the self-dual isotypic block follows from the isomorphism \(F\) and semisimplicity; non-self-dual blocks pair with their distinct dual blocks and do not enter the argument.

The same proof applies to any palindromic tensor word of self-dual simple objects: its transpose sign is the product of their indicators. In particular, \(X\otimes Y\otimes X\) has sign \(\nu_2(Y)\).

## 2. Obtaining a pivotal category and an actual involution algebra

Use source labels

\[
G=\{0,3,4,5\}\cong C_2\times C_2,\qquad
u=3,\quad g=5,\quad \rho=6.
\]

The remaining source labels \(\{1,2,6,7\}\) all have dimension \(d=2+\sqrt5\), satisfying \(d^2=1+4d\). Hence the ring has exactly two distinct Frobenius–Perron dimensions, 1 and \(d\).

By Schopieray, *Categorification of integral group rings extended by one dimension*, published Lemma 3.1, every complex fusion-category categorification with exactly these two dimension values is Galois conjugate to a pseudo-unitary category. Therefore, if the source ring were categorifiable, it would have a pseudo-unitary categorification \(\mathcal C\) with its canonical positive spherical structure. This supplies the pivotal structure used below. Galois conjugation preserves the source fusion rules; no pivotality conjecture is being assumed.

The object \(\rho\) is self-dual, and the source products give

\[
\rho^2=1+\sum_{h\in G}h\rho,
\qquad
[\rho^3:h]=1\quad(h\in G).
\]

In full source-label order the latter product is

\[
\rho^3=(1,4,4,1,1,1,5,4).
\]

The unit occurs once, so the parity lemma with \(n=3\) first gives

\[
1=\nu_2(1)=\nu_2(\rho)^3,
\qquad \nu_2(\rho)=1.
\]

Every element of \(G\) is self-dual and occurs once in the same cube. Thus

\[
\nu_2(h)=1\quad\text{for all }h\in G.
\]

Only \(\rho\) and its partner \(g\rho\) need be self-dual; the other two noninvertibles are mutually dual. The proof does not assume that every noninvertible is self-dual.

The pointed category on \(\langle u\rangle\cong C_2\) is \(\mathrm{Vec}_{C_2}^{\omega}\). In its positive spherical structure, the second indicator of the nontrivial invertible is the value of the normalized associator class on \((u,u,u)\). The two classes in \(H^3(C_2,\mathbb C^\times)\) have indicators \(+1\) and \(-1\), respectively. Since \(\nu_2(u)=1\), this restriction is trivial. Consequently

\[
A=1\oplus u
\]

is an actual connected separable algebra object of \(\mathcal C\): transport the regular group algebra from \(\mathrm{Vec}_{C_2}\). There is no assumption that \(u\) has a central lift, and no de-equivariantization is used. Triviality of the associator on this single order-two subgroup is sufficient.

## 3. The Morita dual is an impossible order-four near-group category

Let \(\mathcal B={}_A\mathcal C_A\). Since \(A\) is connected and separable, this is a fusion category Morita equivalent to \(\mathcal C\). The source gives

\[
u\rho u=g\rho.
\]

For \(H=\{1,u\}\), the action of \(H\times H\) by left and right multiplication has two pointed double orbits of size 2 and one noninvertible double orbit of size 4. The source-bound verifier checks every orbit and stabilizer.

For a simple \(Y\), the free bimodule \(AYA\) satisfies

\[
\dim\operatorname{End}_{A-A}(AYA)
=\dim\operatorname{Hom}_{\mathcal C}(Y,AYA)
=|\operatorname{Stab}_{H\times H}(Y)|.
\]

Each pointed orbit therefore contributes two simple bimodules. Concretely, the stabilizer is \(C_2\), and every twisted group algebra of this stabilizer splits into two one-dimensional representations because \(H^2(C_2,\mathbb C^\times)=0\). The underlying object of each resulting simple has the two invertibles of its orbit once. Its \(\mathcal B\)-dimension is the underlying \(\mathcal C\)-dimension divided by \(\operatorname{FPdim}(A)=2\), hence is 1.

The noninvertible orbit is free, so \(A\rho A\) has a one-dimensional endomorphism algebra and is itself simple, say \(Z\). Its underlying object is the sum of the four noninvertibles, each once, and

\[
\operatorname{FPdim}_{\mathcal B}(Z)=\frac{4d}{2}=2d=4+2\sqrt5.
\]

Every simple bimodule appears in a free bimodule, and distinct support orbits are disjoint. This gives exactly four invertible simples and the one noninvertible \(Z\). Let their invertible group be \(G'\), of order 4, so \(G'\cong C_4\) or \(C_2\times C_2\). The sole noninvertible is self-dual and is fixed by every invertible. Therefore

\[
Z^2=\sum_{h\in G'}h+\ell Z.
\]

Since \(d^2=1+4d\), the dimension identity is

\[
(2d)^2=4+8(2d),
\]

and \(\ell=8\). Thus \(\mathcal B\) would be a near-group category of type \((G',8)\).

Both possibilities are excluded over \(\mathbb C\). For \(G'=C_2\times C_2\), Schopieray's Theorem 1.1 allows only levels 0 and 4. For \(G'=C_4\), the archived rank-five theorem and its exact level-eight certificate exclude the ring. The source-bound verifier invokes the same immutable terminal package as `R170_INVERSE_MORITA_PROOF.md`: `rank5_cyclic/verify.py` checks all six branches, two with a forced nonintegral coefficient \(1/2\) and four with exact integer separators. Hence the hypothetical \(\mathcal B\), and therefore the original \(\mathcal C\), cannot exist.

## 4. Reproduction and scope controls

```sh
python /absolute/path/to/evidence/unified_20261016/rank8/verify_r49_fs_morita.py --repo /absolute/path/to/repo
```

The verifier checks the original census hash and ledger binding, associativity, duality hypotheses, the exact positive dimension character in \(\mathbb Z[d]/(d^2-4d-1)\), the cube multiplicities, the unique indicator sign assignment, the conjugation relation, and all double orbits. It then replays the exact cyclic terminal certificate. Normal and optimized executions give identical PASS receipts.

The general categorical ingredients are the pivotal parity lemma proved above, the published two-dimension Galois reduction, the pointed \(C_2\) associator/indicator identity, separable-algebra Morita duality, and the cited terminal near-group exclusions. The finite verifier checks their source hypotheses; it does not claim to mechanically certify these categorical arguments.

This proof does not resolve `R8_2_412`: its analogous odd-cube multiplicities are even, so the crucial indicator forcing does not follow.

## References

- A. Schopieray, *Categorification of integral group rings extended by one dimension*, Journal of the London Mathematical Society 108 (2023), 1617–1641, Lemma 3.1 and Theorem 1.1, https://doi.org/10.1112/jlms.12789. Use the published Galois-conjugacy formulation of Lemma 3.1.
- P. Etingof, S. Gelaki, D. Nikshych, V. Ostrik, *Tensor Categories*, AMS (2015), pivotal structures and duality, and algebra objects/module categories and Morita duality, https://math.mit.edu/~etingof/egnobookfinal.pdf.
- S.-H. Ng and P. Schauenburg, *Higher Frobenius–Schur indicators for pivotal categories*, Contemporary Mathematics 441 (2007), 63–90, for the pivotal-transpose interpretation of the second indicator.
- `rank5_cyclic/provenance.json`, `rank5_cyclic/case.json`, and `rank5_cyclic/verify.py` bind and replay the cyclic terminal theorem from the earlier rank-five archive; the package is shared with the already audited R170 argument.
