# The four remaining dimension-24 cases are settled

The assigned cases have the following decisions:

| ID | Decision | Reason |
| --- | --- | --- |
| R12_1_428 | Unitarily realized | Explicit relative-cocycle subgroup category over A4×C2. |
| R12_1_445 | Excluded over C | Left/right stabilizers V4 and C4 in an invertible pointed bimodule component. |
| R12_1_493 | Excluded over C | The same stabilizer-duality obstruction. |
| R12_1_513 | Unitarily realized | A second explicit relative-cocycle subgroup category over A4×C2. |

The exclusions allow every possible pointed associator. They do not assume that an arbitrary original pointed category has trivial 3-cocycle, and they do not use completeness of the input census. The models use one fixed group and one fixed subgroup. No online revision was made.

## 1. Pointed-component stabilizer duality

**Criterion.** Let a based ring have a faithful finite-group grading whose neutral part is the pointed ring of a finite group G. For a simple basis element X in a homogeneous component, let

\[
H_L(X)=\{g\in G:gX=X\},\qquad H_R(X)=\{g\in G:Xg=X\}.
\]

If the based ring is the Grothendieck ring of a complex fusion category, then both stabilizers are normal abelian subgroups and are isomorphic. In particular, their exponents and element-order distributions must agree.

**Proof.** A grading of the based ring induces a faithful grading of any categorification by the full semisimple subcategories on its homogeneous simple objects. The neutral category is Vec_G^ω for some normalized 3-cocycle ω, which remains arbitrary. By Etingof–Nikshych–Ostrik, *Fusion categories and homotopy theory*, Theorem 6.1(i), every homogeneous component is an invertible bimodule category over this neutral category. Galindo–Plavnik, *Tensor functors between Morita duals of fusion categories*, Corollary 7.11(1)–(2), applies explicitly to arbitrary pointed associators ω1,ω2 and says that its left and right stabilizers are normal abelian and isomorphic. Equivalently, Theorem 7.9 gives a nondegenerate bicharacter between the two stabilizers. Therefore a V4 stabilizer and a C4 stabilizer are impossible. No pivotal, spherical, pseudo-unitary or unitary assumption is used. ∎

For R12_1_445 take the zero-based basis element X=b3. Its left stabilizer is {0,9,10,11}, with element orders 1,2,2,2, whereas its right stabilizer is {0,1,2,11}, with element orders 1,2,4,4. For R12_1_493 take X=b5. Its left stabilizer is {0,9,10,11}, again V4, whereas its right stabilizer is {0,3,4,11}, again C4.

The exact faithful C3 partitions and all product-grading equations are checked in `verify.py` and stored in `exclusions.json`. They have eight invertibles in degree zero and two dimension-2 simples in each other degree. The contradiction uses only the finite subgroup element orders after the categorical criterion has supplied the missing premise. The two exclusions are independently reviewed by the exclusion-audit agent.

Primary references, inspected in full at the relevant statements:

- P. Etingof, D. Nikshych and V. Ostrik, *Fusion categories and homotopy theory*, Theorem 6.1: https://arxiv.org/abs/0909.3140 .
- C. Galindo and J. Y. Plavnik, *Tensor functors between Morita duals of fusion categories*, arXiv:1407.2783v4, §7.4, Theorem 7.9 and Corollary 7.11, especially item (2): https://arxiv.org/abs/1407.2783 . The arbitrary-ω statement is on printed page 29 (PDF page 29).

## 2. A single subgroup and two relative 3-cocycles

Let V=F2², with coordinates u=(u0,u1), and let

\[
T(u_0,u_1)=(u_1,u_0+u_1),\qquad
B(u,v)=u_0v_0+u_0v_1+u_1v_1.
\]

Then T has order three and B is T-invariant. Define the T-invariant trilinear form

\[
F(u,v,w)=\sum_{j=0}^{2}(T^ju)_0(T^jv)_1(T^jw)_1.
\]

All expressions in these forms take values in F2. Write the group

\[
G=(V\oplus C_2)\rtimes C_3\cong A_4\times C_2
\]

in normal coordinates a=(k,u,z), with product

\[
(k,u,z)(l,v,t)=(k+l,u+T^kv,z+t).
\]

Here C3 acts only on V and fixes the last C2. For a=(k,u,z), b=(l,v,t), c=(m,w,s), define

\[
f_0(a,b,c)=B(u,T^kv)s+zts,
\]
\[
f_1(a,b,c)=F(u,T^kv,T^{k+l}w)+zts.
\]

For ε=(ε0,ε1)∈F2² set

\[
\omega_\varepsilon(a,b,c)=(-1)^{\varepsilon_0f_0(a,b,c)+\varepsilon_1f_1(a,b,c)}.
\]

These are normalized group 3-cocycles. For f0, the bilinear T-invariant form gives the group 2-cocycle B_G(a,b)=B(u,T^kv); its cup product with the central-coordinate homomorphism, together with the ordinary cubic zts, gives f0. For f1, a T-invariant trilinear form on the normal abelian subgroup extends by the displayed semidirect-product formula; expansion of the cocycle identity cancels all terms. Independently, the verifier checks every one of the 24^4 cocycle equations with integers, for each of the four displayed choices.

Fix e0=(1,0)∈V and the involution h=(0,e0,1). Set H={1,h}≅C2. Both B(e0,e0)=1 and F(e0,e0,e0)=1, so

\[
f_0(h,h,h)=f_1(h,h,h)=1+1=0.
\]

All other normalized subgroup triples contain the identity. Thus every ωε restricts *pointwise* to the trivial cocycle on H. The ordinary subgroup algebra A=1⊕h is therefore an actual connected separable unitary algebra in Vec_G^{ωε}. Its bimodule category

\[
\mathcal C_\varepsilon=\operatorname{Bimod}_{\mathrm{Vec}_G^{\omega_\varepsilon}}(A)
\]

is an actual unitary fusion category. There is no conjectural reconstruction, action-lifting assumption or scalar-search nonexistence inference.

The complete tensors identify these four constructions as follows:

| ε0 | ε1 | Input ID | Group of invertible simples |
| --- | --- | --- | --- |
| 0 | 0 | R12_1_351 | C2³ |
| 0 | 1 | R12_1_513 | C4×C2 |
| 1 | 0 | R12_1_428 | D8 |
| 1 | 1 | R12_1_597 | Q8 |

The first case supplies an independent reidentification of an existing first-round model. The last supplies an independent alternative to the parent's separate SL(2,3) construction. The two middle rows settle the newly assigned positive cases. These are standard group-theoretical constructions; no novelty up to tensor equivalence is claimed.

## 3. Exact certificates and independent replay

`models.json` contains each explicit group table, subgroup generator, normal-coordinate list, pair ε, complete simple-bimodule phase data, full model tensor and source-to-model based bijection. No input IDs were relabeled. `models.py` constructs these by the existing exact C2 balanced-bimodule implementation.

`verify.py` independently reconstructs all four categories using the second-round generic subgroup-bimodule engine, with eighth-root phase arithmetic and complete projective-character orthogonality. It verifies all group and cocycle equations, trivial subgroup restrictions, the complete balanced relative tensor products, fusion axioms and all 1728 structure constants against each supplied tensor. It additionally checks the exact C3 grading and stabilizer orders for both exclusions. The normal and optimized-Python replay receipts both pass; no accepted check relies on Python assertions.

This settles all four cases assigned in this follow-up: two general complex exclusions and two unitary models. All calculations are fixed small exact certificate checks and explicit finite-group constructions.
