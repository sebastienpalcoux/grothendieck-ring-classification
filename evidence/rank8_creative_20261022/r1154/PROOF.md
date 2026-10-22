# A four-object semionic packet in every remaining R1154 center

## Result and scope

Assume that `R8_3_1154` has a complex categorification. Apply the already
certified spherical/Galois reduction and work with its pseudo-unitary
Galois conjugate C. Write D=540+240√5. The previous complete center-domain
calculation leaves patterns 6971, 8766, and 8772 and 25 pair histograms.

For **every** remaining pattern, the four simple summands of I(g), where g
is the nontrivial invertible of C, necessarily form the following packet:

* all four have dimension D/4;
* after labelling them Z0,Z1,Z2,Z3, their twists are (i,i,−i,−i);
* Z0*=Z1 and Z2*=Z3;
* their normalized S block is uniquely forced to be

\[
 B=\begin{pmatrix}
 -\frac14+\frac i2&-\frac14-\frac i2&\frac14&\frac14\\
 -\frac14-\frac i2&-\frac14+\frac i2&\frac14&\frac14\\
 \frac14&\frac14&-\frac14-\frac i2&-\frac14+\frac i2\\
 \frac14&\frac14&-\frac14+\frac i2&-\frac14-\frac i2
 \end{pmatrix}.
\]

Their full S columns, and hence all four full fusion matrices, are forced
by the existing restriction matrix. The replay reconstructs and checks
these matrices on every one of the 25 surviving pair histograms.

All these matrices are nonnegative integral. Thus **no new whole-pattern
or ring exclusion is obtained**, and no category is constructed. This is a
new necessary structural theorem, reducing the unresolved center problem.
The term packet denotes these four objects, not a fusion subcategory.

## General reconstruction principle

The argument below only uses an anomaly-free normalized modular datum
(s,T), a four-element label set Z of equal vacuum entries 1/4, and the
specified spectral-projector identity. It therefore supplies a reusable
criterion for other center calculations with the same configuration.

We use s=S/D for the center, with s symmetric and unitary, s²=C the duality
permutation, and

    s T s = T⁻¹ s T⁻¹.

These are the standard canonical-center normalization and modular
identities; see Dong–Lin–Ng, *Congruence property in conformal field theory*,
Algebra & Number Theory 9 (2015), equations (1-9)–(1-10), §4, and
[Etingof–Nikshych–Ostrik, *On fusion categories*](https://arxiv.org/abs/math/0203060).
The former primary article is available at
<https://msp.org/ant/2015/9-9/ant-v9-n9-p03-s.pdf>.
No unitarity of the fusion category itself is assumed: the normalized
modular S matrix is unitary in the positive spherical normalization.

## 1. Twists and the spectral projector

The previously proved rank-five Morita obstruction excludes the trivial
pointed C2 associator for R1154. Consequently ν₂(g)=−1 in the positive
spherical normalization. The frozen restriction columns show

    I(g)=Z0+Z1+Z2+Z3,     dim(Zj)=D/4.

The induction indicator identities give

    Σ θj=0,     Σ θj²=−4.

Because every θj has absolute value one, equality in the triangle
inequality forces θj²=−1. The first identity gives precisely two +i and
two −i twists. These standard induction identities are the same ones
used in the accepted pointed-induction exclusions; see Ng–Schauenburg's
higher-indicator formula, and Ostrik,
[*Pivotal fusion categories of rank 3*](https://arxiv.org/abs/1309.4822), §2.

Let A0=1,A1,A2,A3,A4 denote the five existing distinguished central simples,
all of twist 1. In the real coordinate space on center simples, put

    u=(e_Z0+e_Z1+e_Z2+e_Z3)/2,
    v=(e_Z0+e_Z1−e_Z2−e_Z3)/2,
    w=(e_A0+e_A1−e_A2−e_A3)/2.

Let Q be the coordinate projection onto the four Z labels, and W=im(Q)∩u⊥.
The forced A2 fusion matrix N2 has eigenvalue −1 exactly at the four Z
spectral labels. Its spectral projector is

    P = N2(N2−3)(N2+5)(N2²−270N2+225)/7936
      = wwᵀ + Q − uuᵀ.                                 (1)

The exact replay verifies (1) for all 25 current pair histograms, not just
one chosen witness. The preceding spectrum is complete: the other A2
values are 0,3,−5 and the roots of x²−270x+225.

By Verlinde diagonalization, P=sQs*. Since the four vacuum entries are
1/4, Pe_A0=(su)/2. Formula (1) gives Pe_A0=w/2, hence

    su=w,     sW=W.

I(g) is self-dual, so C preserves Z and Cu=u. Consequently sw=s²u=u.
Also Tw=w and Tu=iv, Tv=iu. Applying the STS identity to w gives

    i sv = −i v,     hence sv=−v.                         (2)

## 2. Complete classification of the residual two-dimensional block

Let

    a=(e_Z0−e_Z1)/√2,     b=(e_Z2−e_Z3)/√2,
    E=span(a,b).

Both s and T preserve E; T_E=diag(i,−i). Write the symmetric unitary
restriction of s as A=[[a₀,b₀],[b₀,c₀]]. Duality preserves twists, so it
independently either fixes or exchanges each same-twist pair. Thus
A²=diag(ε₊,ε₋), where ε₊,ε₋ belong to {1,−1}.

The STS relation gives, when b₀≠0,

    a₀−c₀=−i.

Since A commutes with A², unequal ε values force b₀=0. The diagonal case
of STS forces A=diag(i,−i), and therefore A²=−I. If both ε are +1 and
b₀≠0, A²=I gives c₀=−a₀, hence a₀=−i/2 and b₀²=5/4. This violates
unitarity. If both ε are −1, the remaining possibilities are

    A = diag(i,−i),
    A = (i/2) [[−1, √3],[√3,1]],
    A = (i/2) [[−1,−√3],[−√3,1]].                        (3)

This is the complete case split. In particular duality must exchange
both pairs: Z0*=Z1 and Z2*=Z3.

Let E also denote the 4-by-2 matrix with the above a,b columns. The full
packet S block is B=−vvᵀ+EAEᵀ. Outside Z, each packet column equals w/2;
this follows from sW=W and su=w. Hence every entry of the full four-column
matrix V is known for each of the three options (3).

The fusion-matrix difference N_Z0−N_Z1 is consequently known independently
of every other unknown S column:

    V diag(4(B_0j−B_1j)) V*.

For the two mixed options in (3), its entry (Z2,Z3) is respectively √3
and −√3. A difference of fusion matrices has integral entries. Both
mixed options are therefore impossible. The diagonal option yields the
unique block displayed above.

## 3. Reconstructing the four full fusion matrices

Let M be the source-by-center restriction matrix. By adjunction and the
projection formula, the fusion matrix of I(g) is

    J = Mᵀ N_g M.                                       (4)

Here N_g is left multiplication by g on the source ring. Its action is an
involutive permutation; the restrictions of central objects commute with
g, so the equivalent right-multiplication convention gives the same (4).

The three signed combinations of packet fusion matrices are determined
by their full S columns:

    D₊ = V diag(4(B_0j−B_1j)) V*,
    D₋ = V diag(4(B_2j−B_3j)) V*,
    H  = V diag(−4,−4,4,4) V*.

Thus, in the row-input fusion convention,

    N_Z0=(J+H+2D₊)/4,    N_Z1=(J+H−2D₊)/4,
    N_Z2=(J−H+2D₋)/4,    N_Z3=(J−H−2D₋)/4.             (5)

The verifier checks integrality, nonnegativity, the vacuum rows, duality
transpose, pairwise commutativity, commutativity with N2, and the sum
identity (4). The matrices are saved in `semionic_packet.json`.

Passing these checks supplies necessary packet fusion data only. The
remaining center simples, modular data, Lagrangian algebra multiplication,
and source associators are not constructed by (5).

## Inputs and replay

The input identities are SHA-256 bound by the receipt. The mathematical
dependencies are the existing complete three-pattern center domain, the
25-pair Galois refinement, the forced A2 action, and the nontrivial pointed
associator theorem. This small replay does not rerun those earlier large
calculations.

    python3 evidence/rank8_creative_20261022/r1154/verify_semionic_packet.py

The proof and implementation passed a separate automated mathematical
review, including independent projector, spectral-label, and entrywise
projection-formula checks on all 25 domains. See
[the review](../unified/audits/R1154_PACKET_REVIEW.md). This is an automated
review, not independent human verification.
