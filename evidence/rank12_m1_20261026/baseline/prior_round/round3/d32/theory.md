# Dimension-32 family: third offline round

## Accepted result

**R12_1_240 and R12_1_408 are categorifiable.** The construction is a subgroup-algebra Morita dual of a graded subcategory of a Deligne product. It uses the ordinary Ising category and a pointed category on the dihedral or semidihedral group of order 16 with an explicit 3-cocycle. It does not assume that an unspecified categorification is unitary, spherical, braided, or group-theoretical.

All other 18 input cases remain unresolved in this directory. No failed search is used as an exclusion.

## A uniform categorical construction

Write
\[
E=D_{16}=\{(a,b):a\in\mathbb Z/8,\ b\in\mathbb Z/2\},\qquad
(a,b)(c,d)=([a+(-1)^bc]_8,b+d).
\]
Here brackets take values from 0 to 7. Put
\[
\beta((a,b),(c,d))=\frac{a+(-1)^bc-[a+(-1)^bc]_8}{8}.
\]
For \(g=(a,b),h=(c,d),k=(e,f)\), define
\[
\omega(g,h,k)=
\exp\!\left(\frac{2\pi i}{8}\,a(-1)^b
\frac{c+(-1)^de-[c+(-1)^de]_8}{8}\right).
\]
The displayed expression is unambiguous, including negative carries.

This is a normalized 3-cocycle for a theoretical reason. Let the integers be the sign module for the character \((a,b)\mapsto(-1)^b\). The coordinate lift \(x(a,b)=a\) satisfies \(\delta x=8\beta\), and \(\delta\beta=0\). Pairing two sign modules into the trivial module gives
\(\delta(x\smile\beta)/8=\beta\smile\beta\), an integer cochain. Consequently \(\exp(2\pi i(x\smile\beta)/8)\) is a cocycle. The replay additionally checks all 65,536 group cocycle identities exactly modulo 8.

Let \(\mathcal I\) be a standard Ising category, with simples \(1,\psi,\sigma\), \(\psi^2=1\), \(\psi\sigma=\sigma\), and \(\sigma^2=1+\psi\). Its grading is \(\deg(1)=\deg(\psi)=0\), \(\deg(\sigma)=1\). Inside
\(\mathcal I\boxtimes\operatorname{Vec}_E^\omega\), take the full fusion subcategory
\[
\mathcal C=\langle (X,(a,b)):\deg(X)=a\pmod2\rangle.
\]
It has 16 invertible simples and eight simples of dimension \(\sqrt2\), hence total dimension 32.

Let \(s=(0,1)\) and \(c=(1,s)\), where the first coordinate is the tensor unit of \(\mathcal I\). Since \(c^2=1\) and \(\omega\) is identically 1 on \(\langle s\rangle^3\), the object \(A=1+c\) is the usual subgroup algebra. It is connected and separable over \(\mathbb C\). Therefore \({}_A\mathcal C_A\) is a fusion category of dimension 32, Morita equivalent to \(\mathcal C\).

The eight even group elements form a copy of \(D_8\). Its reflection \(s\) has centralizer of order four. Consequently the even (A)-bimodules consist of eight invertibles and two dimension-two simples. On the odd simple labels, left and right multiplication by \(s\) generate free four-element orbits, because conjugation by an odd rotation changes the reflection conjugacy class inside \(D_8\). There are two such orbits. Each gives one simple bimodule with dimension \(4\sqrt2/2=\sqrt8\). The resulting type is therefore
\[
(1^8,2^2,(\sqrt8)^2).
\]

## Exact tensor identification

`r240_model.py` gives a standalone replay, with `bimodule.py` as its exact balanced-product engine. Source labels are ordered first by Ising label \(0=1,1=\psi,2=\sigma\), then by the pair \((a,b)\). Only standard scalar Ising associators with at most two \(\sigma\)'s enter the computation. In the usual Tambara–Yamagami convention these are
\[
F_{u,\sigma,v}=(-1)^{uv},\qquad
F_{\sigma,u,\sigma}^{v}=(-1)^{uv}
\]
for \(u,v\in\{0,1\}\), with all remaining relevant scalar blocks equal to one. Each is multiplied by the displayed group cocycle. The three-\(\sigma\) Fourier block is not used by subgroup-bimodule operations, but its existence is provided by the actual Ising category; it is not inferred from a partial pentagon check.

For every pair of source bimodules the replay imposes the balancing relation, checks descent of left and right actions, and computes the exact stabilizer eigenspace dimensions. Arithmetic takes place in \(\mathbb Q(\zeta_8)\), using the polynomial \(t^4+1\), with no floating-point decisions. The resulting tensor passes the fusion-ring validation. The source-to-model basis permutation for the census tensor is

```
[0, 8, 9, 3, 4, 10, 2, 7, 11, 5, 6, 1]
```

All 1,728 coefficients are checked under this permutation. The full source tensor, target tensor, labels, bimodule phases and permutation are saved in `r240_certificate.json`.

A separate implementation in `../independent/audit_ising_dual.py` reconstructs all 1,728 coefficients by grade-preserving Hom-space relation graphs, without using the stabilizer-character projection formula. It independently checks all group cocycle equations, all bimodule axioms, pairwise simplicity, the dimension count, and the full match to R12_1_240. The untwisted R12_1_28 control also passes.

## The semidihedral companion: R12_1_408

The same categorical construction works for
\[
E=SD_{16},\qquad (a,b)(c,d)=([a+3^bc]_8,b+d).
\]
The matching grading is again the parity of the rotation exponent, and the algebra generator is again \(c=(1,(0,1))\). The even subgroup is again dihedral of order eight; the same double-coset argument gives eight invertibles, two dimension-two objects and two dimension-\(\sqrt8\) objects.

Here the cocycle is specified by the exact normalized exponent table `cocycle_SD16_mod16.json`, with values modulo 16. The table is indexed by the lexicographically ordered list \((a,b)\), \(0\leq a<8\), \(0\leq b<2\). It is part of the certificate, not a black-box cohomology assertion. All 65,536 identities are checked directly by both replay implementations, and its restriction to \(\langle(0,1)\rangle\) is zero. Thus it defines an actual pointed category and actual separable subgroup algebra.

For reproducibility, the table was obtained by the following short exact lift. Define
\[
\phi(g,h,k)=a3^b\left(2\left\lfloor\frac{c+3^de}{8}\right\rfloor+5de\right)\pmod {16}.
\]
Its reduction modulo eight is a 3-cocycle. Solve the normalized finite linear system
\(\delta t=\delta\phi/8\pmod2\), and take \(\Omega=\phi+8t\pmod {16}\). `semidihedral_lift.py` records the deterministic elimination; it has 3,375 normalized cochain variables and rank 3,163, and the solve took less than one second. The resulting table is verified independently of this derivation. This is an exact existence certificate for a cocycle, with no classification inference from a failed search.

`r408_model.py` is the portable replay. The basis map is

```
[0, 8, 9, 3, 4, 10, 11, 2, 7, 5, 6, 1]
```

All 1,728 tensor coefficients match R12_1_408. The independent Hom-space implementation verifies both choices \((1,s)\) and \((\psi,s)\) of subgroup generator and obtains the same ring. The complete certificate is `r408_certificate.json`. Both portable replays use the frozen census tensors and local `ring_checks.py`; both pass with Python assertions disabled (`python -O`).

As a bounded follow-up, all mod-two third-cohomology twists of this lift were computed: the quotient has dimension two, and both twists whose subgroup restriction is trivial still give R12_1_408. Odd powers three, five and seven of the accepted cocycle also give the same ring. These checks add coverage but are not asserted to classify all possible dimension-32 categories.

## Other attempts and their limits

1. Matched-grading pullbacks of Ising with the representation categories of the dihedral and quaternion groups of order 16, with admissible elementary zests, recover the known R12_1_28 and R12_1_183. They do not resolve a new case.
2. The eight Choi–Lu–Sun dimension-16 categories have an explicitly verified soft tensor involution. In the notation of `cls_soft.py`, its three multiplicity-two blocks are \(Y,-Y,Y\), and its scalar signs are \((1,-1,-1,1)\). All 4,992 relevant tensor-functor coherence entries pass exactly. Both coherent action-square choices are included. Equivariantization recovers R12_1_28 and R12_1_183. This is a positive construction check, not an exhaustion theorem for arbitrary soft actions.
3. `soft_monomial.py` enlarges that ansatz to all monomial involution blocks with eighth-root phases while fixing the neutral tensorator. It solves the exact coherence congruences. Again the only census matches are R12_1_28 and R12_1_183. `soft_monomial_full.py` also allows neutral scalar tensorators, giving 32 diagonal trace signatures and 16 swapped-block trace signatures per variant; it likewise yields only R12_1_28 and R12_1_183. Neither ansatz is asserted to exhaust all categorical actions.
4. Untwisted Ising–pointed pullbacks for the metacyclic order-16 presentations \(srs^{-1}=r^u\), \(s^2=r^v\), recover R12_1_28 (dihedral) and R12_1_183 (semidihedral). Adding the rotation cocycle above produces R12_1_240. Inflated cubic character cocycles were also considered. The exploratory all-grading script reached a phase-modulus limitation in one branch and is not an exhaustive classification. The accepted R12_1_240 replay is separate, short, deterministic and independently audited.
5. A possible general reduction through an isotropic order-two algebra in the dimension-16 neutral category was explored. There is a plausible compatibility argument for its two stabilizer bicharacters. A complete classification of all resulting generalized-Ising and generalized-Tambara–Yamagami Morita sources has not been established here. In particular one cannot assume that the inverse subgroup generator lies outside the noninvertible stabilizer, or that it acts freely on every odd simple. These branches prevent using the partial reduction as an exclusion theorem.
6. Fermionic zest constructions were considered to generate nonsplit invertible groups in possible Morita sources. No new accepted model or exclusion is based on an unverified zest coherence or an unproved exhaustiveness premise.

The exploratory checks therefore support two new positive results, not eighteen negative ones.
