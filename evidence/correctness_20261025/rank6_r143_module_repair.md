# Independent categorical identification of R6_2_143

Exact proof for the 25 October 2026 correction release, integrated into the current manuscript. The original pre-publication audit snapshot is preserved separately; no fusion tensor or classification status changes.

## Why this additional argument is useful

The current manuscript `supplements/rank6/papers/chapters/06.tex:219–241` identifies R6_2_143 using Evans–Gannon, arXiv:1006.1326, Theorem7. The full216 coefficients printed there agree with the local constructor. However, Theorem7 assumes the actual double's fusion data and a specified canonical endomorphism. The earlier finite identification uses the numerical S comparison discussed in that paper's §4.1. Grossman–Snyder §6 explicitly retains those hypotheses. Thus copying the tensor correctly does not independently verify those premises.

The following proof identifies the actual dual category from its canonical module, avoiding all center modular-data identification. The existing model is correct once this independent argument is added; the mathematical tensor does not change.

## Actual category and exact module

Start with the known unitary Haagerup–Izumi C5 category, with simples `α_g,α_gρ`, dimension `d=(5+√29)/2`, and the actual Q-system `1+ρ`. Its unitary dual category `D` therefore exists. Existence of this C5 seed and Q-system is Izumi's original construction; Grossman–Snyder, arXiv:1102.2631v2, §6 opening p32, recalls both independently of the later paragraph imposing center-data conditions.

For the dual object inventory use the exact categorical derivation in [Izumi, *The classification of 3^n subfactors and related fusion categories*, Quantum Topology9 (2018)](https://ems.press/content/serial-article-files/36852), §7, printed pp527–529, equation(7.1) and the dimension identity preceding Proposition7.4. Its hypotheses are the actual Q-system above. Specializing `G=C5` gives six dual simples

\[
1,\ a,\ b_1,b_2,\ c_1,c_2
\]

of dimensions `1,d,d−1,d−1,d+1,d+1`. In the primary notation these are `id,ρhat,σ1,σ2,η1,η2`. The displayed identity `sum_j n_j²=(|G|−|G2|)/2=2` already forces exactly two σ objects with multiplicity1; the more general Theorem7.5 is unnecessary here. The displayed Proposition7.4 inventory has an evident omission of the ρhat-type in its text; the preceding derivation and (7.1) explicitly include it, and those formulas are used here.

The canonical module has simples `i_g=α_gι` for `g∈C5` and `τ`, with relative dimensions `1,1,1,1,1,d−1`. The same primary derivation gives

\[
\iota a=\iota+\tau,\qquad
\iota b_j=\tau,\qquad
\iota c_j=\alpha_j\iota+\alpha_{-j}\iota+\tau.
\]

The left C5 action fixes τ because it is the unique module simple of its dimension. Thus the top-left five-by-five blocks of the six right-action matrices are

\[
I,\quad I,\quad0,\quad0,\quad P+P^{-1},\quad P^2+P^{-2},
\]

where P is the cyclic shift. For each nonunit simple all five entries connecting the i-labels to τ are1. The τ-diagonal entries are respectively4,3,3,5,5, forced by the positive dimension vector and `d²=1+5d`. The unit matrix has τ-diagonal1 and no connecting entries. These exact matrices require no center formula.

## Commutativity and both possible dualities

The six action matrices commute and span a four-dimensional algebra. The six-dimensional complex fusion algebra is semisimple. A noncommutative simple summand has dimension at least4; its homomorphism to a commutative algebra must vanish. It would therefore lie in the two-dimensional kernel, which is impossible. Hence the actual fusion ring is commutative.

The objects a,c1,c2 are self-dual: `1+a=barιι`, and `c_j=barι α_jι=c_{-j}`. Duality either fixes b1,b2 individually or interchanges them; these are all possibilities, since the other dimensions differ.

Write

\[
T(i,j,k)=\dim\operatorname{Hom}(1,X_iX_jX_k)
       =N_{ij}^{k^*}.
\]

Commutativity and Frobenius reciprocity make T symmetric in all three labels, and duality preserves T. For each of the two possible dualities impose the exact module identities

\[
M_iM_j=\sum_k T(i,j,k^*)M_k.
\]

After the unit coefficients are fixed, this is a rational linear system in35 unordered nonunit triples. No multiplicity bound is imposed.

- If b1 and b2 are dual to one another, the unique linear solution has `T(b1,b1,b1)=−1/2`, impossible for a fusion category.
- If both are self-dual, the solution space has one parameter `t=T(b2,b2,b2)`. Its other undetermined coefficients are `T(b1,b1,b1)=2−t`, `T(b1,b1,b2)=t−1`, and `T(b1,b2,b2)=1−t`. The last two must be nonnegative, so `t=1`.

Thus the actual category has a unique possible full fusion tensor. The exact linear equations and their complete affine solution vectors are recorded in the accompanying JSON. This derivation uses no census-completeness assumption and no hypothetical upper bound on structure constants.

## Tensor identification and verification

`rank6_r143_module_repair.py` independently constructs the canonical action matrices, verifies their span dimension and commutativity, solves both duality branches, and forces the unique tensor by the inequalities above. Only after this reconstruction does it import the existing formula constructor and census. All216 tensor coefficients agree, with one model-to-census map

\[
(0,3,1,2,4,5).
\]

It also verifies all1296 associativity equalities. Maximum multiplicity2 is a conclusion. The census tensor hash is `aac7d0adf7fe999392b64a087ab3539cc73ac141c5ea9e6af7a1f192d5cf342f`. Normal and optimized Python runs pass with identical receipts. The existence claim remains a genuine Q-system dual construction; the linear calculation identifies its ring rather than manufacturing a category from integer feasibility.

This supplies a replacement proof for R6_2_143's categorical-identification premise. Publication should add the independent argument and its versioned certificate rather than retrospectively changing historical source-bound receipts.
