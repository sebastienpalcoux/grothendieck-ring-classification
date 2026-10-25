# Exact replacement proof for R8_2_820 and R8_2_869

Exact proof for the 25 October 2026 correction release, integrated into the current manuscript. The original pre-publication audit snapshot is preserved separately; no fusion tensor or classification status changes.

## Statement and scope

**Theorem.** Let N₁ and N₂ be the actual unitary C5+5 near-group categories with Evans–Gannon parameters

\[
(m,\kappa)=(1,-1),\qquad (m,\kappa)=(2,\omega),
\quad \omega=e^{2\pi i/3}.
\]

Inside each unitary Drinfeld center, the five invertible objects generate a nondegenerate pointed category Pᵢ. Their Müger centralizers Bᵢ=Pᵢ′ are unitary modular categories, and

\[
K_0(B_1)\cong R8\_2\_820,
\qquad K_0(B_2)\cong R8\_2\_869.
\]

The proof identifies the **fusion rings** of the actual centralizers. It does not assume, or claim to newly verify, equality of their entire modular data with the proposed data in Evans–Gannon Proposition 7(b). In particular, it does not use the floating-point comparison after their Conjecture 2. The original project verifiers remain useful for exact algebraic character tables and tensor transports; their old assertion that the candidate S matrix was already identified categorically is not a premise here.

The replacement has four parts: derive partial fusion from the rigorously known actual tube blocks; classify all associative completions in a small complete integer domain; compute an actual third-indicator invariant of each seed; and distinguish the two possible rings using exact fusion characters and balancing.

## Published categorical inputs

The following are external theorem dependencies. This audit checked the stated scopes and the formulas used; it does not claim to reconstruct every associator or reprove these papers.

1. D. E. Evans and T. Gannon, *Near-group fusion categories and their doubles*, [arXiv:1208.1500v1](https://arxiv.org/pdf/1208.1500v1), Corollary 5 and Proposition 6/Table 2, printed pp28–33: actual C*-near-group categories with the two parameters above. Section 4.3, especially (4.49)–(4.51) and the **known blocks** of (4.56)–(4.57), printed pp44–45: actual center objects, underlying objects, invertible twists/pairing, and all S blocks except the d–d block. These follow the actual tube-algebra analysis, separately from the candidate identification in §4.4. For the first seed, exact constants are also recorded in Izumi Example 13.8 below. The apparent numerical-dimension typo in that example is not used.
2. M. Müger, *On the Structure of Modular Categories*, [arXiv:math/0201017](https://arxiv.org/pdf/math/0201017), Lemma 3.5, Proposition 4.1 and Theorem 4.2, particularly printed p11: a full nondegenerate modular subcategory of a modular category has a modular centralizer and gives a ribbon tensor-product decomposition. The *-structure is retained in this unitary setting.
3. M. Izumi, *A Cuntz algebra approach to the classification of near-group categories*, [arXiv:1512.04288v2](https://arxiv.org/pdf/1512.04288v2), Remark 3.11, printed pp22–23: the third indicator of the noninvertible object is the trace of the specified rotation j₁∘j₂. The unnumbered formulas at the opening of §9, printed p70 immediately before Theorem 9.1, specify the two anti-linear operators. Their conjugation bars were checked visually in the primary PDF. The parameters agree with the C5 near-group data; see also Example 13.8, printed p124.
4. S.-H. Ng and P. Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical Categories*, [arXiv:math/0601012v3](https://arxiv.org/pdf/math/0601012v3), Theorem 4.1 and (4.2)–(4.3), printed p10: indicators are normalized pivotal traces of twist powers on induction to the center. This applies because the actual seeds are unitary and hence carry their canonical positive spherical structure.

We also use the usual ribbon balancing identity and Verlinde diagonalization for a modular category. EG Definition 2 and (4.11), printed p35, specify the S/Verlinde convention. All objects to which the final square-balancing calculation applies are proved self-dual below. Consistently reversing the ribbon convention conjugates the nonreal indicator/twist expressions and leaves both distinctions unchanged.

## 1. The actual factor and its partial S matrix

Write ζ=e^(2πi/5), and reserve κ for the near-group scalar parameter. Set

\[
a=\frac{5+3\sqrt5}{2},\qquad b=a+1,\qquad c=a+2,
\qquad \mathcal D=45b=9a^2=5c^2.
\]

The identities a²=5+5a and c²=9b fix all normalizations. The seed has five invertible objects and a single object ρ of dimension a, so Dim(N)=5c. Its center has dimension (5c)²=225b.

The actual invertible center objects a_g, g∈C5, have twists ζ^(mg²) and restricted normalized pairing proportional to ζ^(-2mgh). Since 2m is invertible modulo5, their pointed subcategory P is nondegenerate. Müger's theorem gives

\[
Z(N)\simeq P\boxtimes B,\qquad \operatorname{Dim}(B)=\mathcal D.
\]

EG (4.51) gives40 simple center objects: five a's, five b's, ten c's and twenty d's. Since P has5 simples, B has8. Monodromy with the known invertibles identifies four of them as

\[
1=a_0,\quad B=b_0,\quad C_1=c_{1,-1},\quad C_2=c_{2,-2}.
\]

These are self-dual: their underlying objects are self-dual and the relevant half-braiding is unique in the actual tube inventory. The four remaining simples, denoted D₁,…,D₄, are actual d-type objects of dimension a. No group Γ labelling or D self-duality is assumed. Alternatively, the pointed action shifts monodromy characters nondegenerately, placing four of the twenty d objects in each of the five monodromy classes.

In the ordered basis (1,B,C₁,C₂,D₁,…,D₄), the dimensions are

\[
\mathbf d=(1,b,c,c,a,a,a,a).
\]

Let M be the actual unnormalized S matrix of B, so MM*=𝒟I. Its first four columns, directly from the known blocks of EG (4.57), are

\[
\begin{aligned}
\mathbf d&=(1,b,c,c,a,a,a,a)^t,\\
\mathbf s_B&=(b,1,c,c,-a,-a,-a,-a)^t,\\
\mathbf s_k&=(c,c,c(\zeta^{2mk}+\zeta^{-2mk}),
 c(\zeta^{4mk}+\zeta^{-4mk}),0,0,0,0)^t,
 \quad k=1,2.
\end{aligned}
\]

All these entries are real. The entire D–D block is left unknown. The center normalization denominator is5c; passing to its pointed centralizer multiplies normalized S by√5, giving the denominator√𝒟=3a=(5c)/√5 used here.

For X=C_k, Verlinde's sum for N_X uses only those four known columns because M_(C_k,D_j)=0. For X=B, every unknown D column has eigenvalue M_(B,D_j)/d_(D_j)=−1. Eliminate their sum by MM*=𝒟I:

\[
N_B=-I+\frac{(b+1)\mathbf d\mathbf d^t+
 (1+b^{-1})\mathbf s_B\mathbf s_B^t+
 2\mathbf s_1\mathbf s_1^t+2\mathbf s_2\mathbf s_2^t}{\mathcal D}.
\]

Thus no unknown S entry occurs in these three multiplication matrices. Exact evaluation for m=1 and2 gives the same partial fusion. Put E=ΣᵢDᵢ. Besides the unit, commutativity, and C₁↔C₂ symmetry, the complete partial products are

\[
\begin{aligned}
B^2&=1+B+C_1+C_2+E,\\
BC_i&=B+2C_i+C_j+E &&(j\ne i),\\
C_i^2&=1+2B+C_i+2C_j+E &&(j\ne i),\\
C_1C_2&=B+2C_1+2C_2+E,\\
BD_i&=B+C_1+C_2+E-D_i,\\
C_kD_i&=B+C_1+C_2+E.
\end{aligned}
\tag{1}
\]

The verifier `rank8-ng-partial-fusion.py` evaluates these identities exactly and sets every candidate D–D matrix entry to `None` before calculating. It also checks squared-dimension Gauss normalization. That Gauss check uses dimensions **squared**; the induction trace in §3 correctly uses dimensions weighted by forgetful multiplicities.

## 2. Complete finite classification of the remaining products

Let i↦i* be the still-unknown involution on the four D labels. Frobenius reciprocity applied to (1) forces

\[
D_iD_j=\delta_{j,i^*}1+(1-\delta_{j,i^*})B+C_1+C_2+
 \sum_k n_{ij}^kD_k.
\tag{2}
\]

Comparing dimensions with a²=5+5a gives

\[
\sum_k n_{ij}^k=2+\delta_{j,i^*}.
\tag{3}
\]

In lowered notation F_ijk=n_ij^(k*), the coefficients are nonnegative integers, fully symmetric in the three indices, and invariant under simultaneous duality. Equation (3) bounds each by3. These necessary conditions define a complete finite domain; no assumption about a census's completeness is needed.

There are exactly three involution types on four labels. For each, take all20 unordered triples with repetition, merge their simultaneous-duality orbits, and enforce all10 unordered-pair equations (3), counting repeated appearances of a variable with their full multiplicity. The exhaustive nonnegative enumeration gives:

| Duality on D | Variables | Row-sum solutions | Associative labelled tensors | Classes under D relabelling |
|---|---:|---:|---:|---:|
| identity |20|708|9|2|
| one transposition |13|16|0|0|
| two transpositions |10|0|0|0|

Every surviving assignment was reconstructed as a full8×8×8 tensor and checked against every8⁴ associativity identity, as well as unit, commutativity, duality and Frobenius reciprocity. Classification uses all24 permutations of the D labels. The recursion prunes only negative linear residuals, residuals with no remaining variable, or residuals exceeding the sum of exact remaining variable capacities. For a variable v its upper bound is the minimum residual divided by its positive coefficient over all rows containing v; hence all pruning is necessary and all nonnegative solutions are retained. Integer arithmetic is exact and far below its native bounds.

The two classes are the following explicit rings, now necessarily self-dual:

- R_E: the unique labelled completion in which
  \[
  D_i^2=1+C_1+C_2+E-D_i,\qquad
  D_iD_j=B+C_1+C_2+D_i+D_j\quad(i\ne j).
  \]
- R_C: the other class, with eight labelled completions. Label its four D objects by x∈{1,2,3,4}, representing the nonzero elements of C9 modulo sign. Its lowered D–D–D coefficients are
  \[
  F_{xyz}=1-\sum_{s,t\in\{\pm1\}}
   \mathbf1_{x+sy+tz=0\pmod9}.
  \tag{4}
  \]

Together with (1), (2) and self-duality, these specify the entire two tensors. For R_E, the same formula using Γ=C3² and representatives (1,0),(0,1),(1,1),(1,2) gives its displayed rules. These finite groups are **labels for explicit integer rings**, not assumed labels for the actual tube objects.

The exact exhaustive certificate is `rank8-neargroup-associativity-classify.py`. Its use of the pre-existing candidate constructors only identifies the resulting explicit rings; it does not import any categorical realization premise.

## 3. A seed invariant from actual rotation operators

Write A_m(h)=ζ^(2mh²). Izumi's actual anti-linear operators on the five-dimensional space Hom(ρ,ρ²), in its stated orthonormal basis T_h, are

\[
j_1(T_h)=A_m(h)T_{-h},\qquad
j_2(T_h)=\frac{\overline\kappa}{\sqrt5}
 \sum_k\overline{\langle h,k\rangle}T_k,
\quad \langle h,k\rangle=\zeta^{mhk}.
\]

Anti-linearity matters: composing gives

\[
\nu_3(\rho)=\operatorname{Tr}(j_1j_2)
 =\frac\kappa{\sqrt5}\sum_h\langle h,h\rangle^{-1}A_m(h)
 =\frac\kappa{\sqrt5}\sum_h\zeta^{mh^2}
 =\kappa\left(\frac m5\right).
\tag{5}
\]

Consequently the two actual indicators are −1 and −ω. The exact verifier constructs both rotation matrices, checks that their cubes are the identity, and checks these traces; it uses no candidate S or census tensor.

Let t₁,…,t₄ be the unknown actual twists of the factor's four D objects. The other factor twists are1,1,ζ^(-m),ζ^(-4m). The forgetful image of each b, c or d center object contains ρ once; a-type objects contain it zero times. Tensoring a factor simple by a_g multiplies its twist by ζ^(mg²). Define

\[
G_3(m)=\sum_{g=0}^4\zeta^{3mg^2}
 =\left(\frac{3m}{5}\right)\sqrt5,
\qquad
L_3(m)=\zeta^{-3m}+\zeta^{-12m}.
\]

The ten unordered c-label pairs are (u+t,u−t), with u∈C5 and t∈{1,2} modulo sign, so their total cubed-twist sum is G₃(m)L₃(m). Applying Ng–Schauenburg Theorem4.1 to induction ofρ gives exactly

\[
\nu_3(\rho)=\frac{G_3(m)}{5c}
 \left(b+cL_3(m)+a\sum_i t_i^3\right).
\tag{6}
\]

Substitution of (5) into (6) yields

\[
\sum_i t_i^3=4\quad\text{for }N_1,
\qquad
\sum_i t_i^3=1+3\omega^2\ne4\quad\text{for }N_2.
\tag{7}
\]

These are exact identities over Q(ζ₁₅). As the actual factor is unitary, |t_i|=1. Equality in the triangle inequality for the first sum forces every t_i³=1. The second sum precludes that conclusion for all four simultaneously. No individual actual tube twist was guessed or numerically recognized.

The independent certificate is `rank8_neargroup_seed_indicator.py`; its source note records primary formulas and conventions in detail. Consistently conjugating all ribbon conventions conjugates the second expression in (7) and leaves its inequality with4 unchanged.

## 4. Fusion characters and balancing distinguish the completions

The two explicit candidate matrices, now used **only as algebraic character tables of R_E and R_C**, satisfy M²=𝒟I and all multiplicative-character equations. Their eight distinct normalized columns therefore give every irreducible character of each rank-eight commutative ring. This assertion is checked exactly; it is independent of whether the candidate matrices are realized by categories.

For any actual modular category with this ring and positive dimensions, the column M_ij/d_j is a ring character of formal codegree 𝒟/d_j². Exactly four characters in each table have codegree𝒟/a²=9: its four D columns. Thus, after identifying the ring basis, the actual D block is the explicit character block with its columns permuted. Unit-row normalization removes scalar ambiguity; symmetry of actual S restricts the permutation.

Put T_D=Σ_i t_i and T_C=θ_C1+θ_C2. Balancing BD_i in (1), using θ_B=1 and the known actual entry M_(B,D_i)=−a, gives

\[
aT_D=-b-cT_C.
\tag{8}
\]

In either ring, each D_i² contains exactly three D labels once:

\[
D_i^2=1+C_1+C_2+\sum_{j\ne f(i)}D_j.
\]

Balancing this square, then applying (8) and b=a+1, gives

\[
r_i t_i^2=-1-t_{f(i)},
\qquad r_i=M_{D_i,D_i}/a.
\tag{9}
\]

**For R_E:** every entry of its D character block divided by a is1 or−2, and f(i)=i. If r_i=1, (9) is t_i²+t_i+1=0. If r_i=−2, it is (t_i−1)(2t_i+1)=0; its only unit-modulus root is1. Therefore every actual unitary modular realization of R_E with the established partial data and θ_B=1 has

\[
t_i^3=1\quad\text{for all four }i.
\tag{10}
\]

**For R_C:** with labels x,y∈{1,2,3,4}, the D character block divided by a is

\[
Y_{xy}=-2\cos(4\pi xy/9).
\]

Its row3 is1 except for Y₃₃=−2. Every other row has its sole rational entry in column3, equal to1; its other entries are real roots of the irreducible polynomial X³−3X−1. If a column permutation π makes Y symmetric, π must fix3. Otherwise take i=π⁻¹(3)≠3: the (3,i) entry is−2 whereas the (i,3) entry is irrational. Thus three actual diagonal ratios r_i, for i≠3, are real cubic irrationals.

If all four t_i³ were1, (9) would put each r_i in Q(ω). Since r_i is real, it would lie in Q(ω)∩R=Q, contradicting cubic irrationality. Hence R_C cannot satisfy (10).

The verifier `rank8-neargroup-twist-distinction.py` checks character completeness and formal codegrees, all24 D-column permutations, the polynomial/rational alternatives, and every D-square rule. It finds10 symmetric column choices for R_E and3 for R_C, all with the properties just proved. It does not assert any actual individual twist or unknown tube-S identification.

Now (7) finishes the theorem. The first seed has every D twist cubing to1 and therefore realizes R_E. The second cannot realize R_E, so the complete classification forces R_C.

## 5. Exact census identification

In the basis (1,B,C₁,C₂,D₁,D₂,D₃,D₄), use the D representatives stated in §2. The already defined exact tensors identify with the lexicographically ordered exact-multiplicity-two part of `supplements/rank8/data/rank8_tables.txt.gz` as follows. Maps are zero-based and send the displayed model basis to the source basis.

| Explicit ring | Census ID | Model-to-source map | Source-to-model map |
|---|---|---|---|
| R_E | R8_2_820 | (0,2,6,7,1,3,4,5) | (0,4,1,5,6,7,2,3) |
| R_C | R8_2_869 | (0,3,6,7,1,2,5,4) | (0,4,5,1,7,6,2,3) |

The source archive SHA256 is `35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed`. In the compact JSON serialization used by the exact transport verifier, the two source tensor hashes are

- R8_2_820: `88d4e0d03d1f45b727bb5d973ee4c47ef114ff4870f397d9f08342d5db1d0373`;
- R8_2_869: `6fd67687c6a4590e43cf539442042092ebc28973b626127f40d6f27fb66de112`.

`evidence/unified_20261016/rank8/verify_neargroup_centralizer.py` checks all512 entries for each map and all4096 associativity identities, using exact rational field arithmetic. Its independent companion `verify_neargroup_centralizer_independent.py` constructs the integer ring formula directly. For this repair, those programs are used only for ring/character algebra and source transport; their old categorical prose is superseded by §§1–4 above. The full source-bound transports have also been rerun normally and under `python -O` with the new audit replay.

## 6. Reproducibility, validation and remaining external scope

The four new audit certificates are:

1. `rank8-ng-partial-fusion.py` → known actual blocks give the common partial fusion;
2. `rank8-neargroup-associativity-classify.py` → the complete bounded domain has exactly the two ring completions;
3. `rank8_neargroup_seed_indicator.py` → actual seed rotation and induction give the two exact third-twist moments;
4. `rank8-neargroup-twist-distinction.py` → ring character tables and balancing separate those moments.

All correctness guards have been converted to explicit `require` checks, so they remain active under `python -O`. The original scripts and receipts from before this hardening are preserved unchanged in `rank8-ng-pre-hardening/`. These versioned proof scripts accompany the revised manuscript.

Run `python3 evidence/correctness_20261025/replay.py --output-dir /tmp/exact-model-repairs` from the repository root. It runs all four scripts sequentially in normal and optimized modes, preserves separate receipts/logs for both modes, requires equality of their mathematical receipts, verifies that all four contain no optimization-sensitive assertions, and reruns the full candidate-to-census transports in both modes. The combined manifest is `rank8-neargroup-exact-repair-replay.json`; its source hashes bind the four audit scripts, the imported exact field/tensor code, and the census archive. The separate outputs are in `rank8-ng-repair-replays/`.

The proof is new audit work and has been cross-reviewed by the rank-seven, rank-nine and primary-source auditors; this is not an external independent certification or a proof-assistant formalization. The actual seed categories, the exact portion of the published tube analysis, modular factorization, and categorical indicator theorem remain the explicit published dependencies listed above. No floating-point proximity claim or numerical recognition of an unknown S/T entry is used anywhere in the replacement chain.

The justified conclusion is affirmative **unitary modular categorification of both census rings**. The old numerical-identification premise should be replaced explicitly in manuscripts and evidence before describing the current published proof as repaired.
