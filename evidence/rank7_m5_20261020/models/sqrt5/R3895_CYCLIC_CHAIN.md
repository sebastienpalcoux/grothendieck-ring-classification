# The finite cyclic-rotation proof for R7_5_3895

**Complete finite certificate set, 20 October 2026.** All fifteen final
conditional systems have complete exact exclusion certificates, with 2,126
exact leaves in total. This note records their mathematical premises and
exhaustive coverage. The strict whole-chain replay described in Section 7
is the acceptance gate; its result is recorded separately so that this
proof note can be frozen before that replay. Partial probing checkpoints
and numerical solver outcomes are not premises.

The canonical tensor is `R7_5_3895`, with SHA-256
`590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0`.
In its fixed source basis the Frobenius–Perron dimensions are

\[
(1,\;5+2\sqrt5,\;5+2\sqrt5,\;10+4\sqrt5,\;
 8+4\sqrt5,\;8+4\sqrt5,\;9+4\sqrt5),
\qquad D=720+320\sqrt5.
\]

Its formal codegrees are the roots of

\[
(t-4)(t-16)^2(t-5)^2(t^2-1440t+6400).
\]

The conclusion certified by the complete chain is that no fusion category over the complex numbers
has this based ring. The argument concerns arbitrary categorifications:
pivotality, sphericality, pseudo-unitarity and a braiding on the original
category are not assumed. The passage to a pseudo-unitary Galois conjugate
is proved first; the modular data used subsequently belong to its center.

## 1. Reduction of every categorification to the positive dimension case

The complete oriented sphericalization enumeration has precisely two signed
quotients, and both are gauge equivalent to the original unsigned tensor.
Changing the chosen simple lifts by the corresponding gauge makes every
opposite-lift multiplicity zero. The chosen lifts therefore form a tensor
subcategory of the sphericalization that is tensor equivalent to the
original category. The spherical structure restricts to that subcategory.

Every source character outside the Frobenius–Perron Galois orbit either
vanishes on a simple object or takes different values on dual objects.
Neither can be a spherical dimension character. A field automorphism thus
takes the spherical dimensions of any hypothetical categorification to the
positive Frobenius–Perron dimensions displayed above. Its Galois conjugate
is pseudo-unitary, with the same based ring. It consequently suffices to
exclude the positive dimension case.

The exact enumeration, gauges and complete character calculation are
replayed by [verify_reduction.py](../../sqrt5_reduction/verify_reduction.py);
the categorical argument is [PROOF.md](../../sqrt5_reduction/PROOF.md).
The center used from this point onward is the center of the rank-seven
category, not the center of its sphericalization.

## 2. Complete restriction rows, induced-unit frames and second indicators

Let \(F:Z(\mathcal C)\to\mathcal C\) be forgetful and \(I\) its adjoint.
For a central simple \(Y\), write
\(v_Y=([F(Y):X_i])_i\), \(z_Y=v_Y\cdot d\), and let \(M\) have rows
\(v_Y\). The induction identity gives the source-derived Gram matrix

\[
M^{\mathsf T}M=B,
\qquad B_{ih}=\sum_{k,j}N_{ki}^{j}N_{kh}^{j}.
\]

The commutative source ring has seven one-dimensional irreducible
characters. Accordingly \(I(1)\) has seven distinct simple constituents,
one for each formal codegree \(f_E\), with central dimensions \(D/f_E\).
Their restriction rows are the known or **low** rows. The remaining central
simples have unit coordinate zero and give the **high** rows.

Exact enumeration from the tensor gives 15 low frames and 163,766 candidate
high rows before the subsequent compatibility filters. Character reciprocity
leaves precisely the zero-based low-frame indices 6 and 8. The domain
reconstruction includes categorical duality and the actual positive Galois
row action. If raw transport sends a row to a negative vector, its sign is
corrected; no argument assumes that the raw transport matrix is nonnegative.

All second-indicator alternatives are retained. The four negative-indicator
labellings in each of the two surviving frames are excluded by exact
covectors, for eight negative cases in total. The positive-indicator cases
have indices \(0,2,4,6\) in each frame. Every remaining finite system is
reconstructed from these complete domains by
[verify_source_domains.py](../../integral_gram/verify_source_domains.py).

For frame 6, the saturated conductor-five budget has 20,508 raw integral
allocations. Exact residual-Gram checks leave 126; inactive-column lattice
membership leaves 32 per positive labelling. Across the four labellings,
112 of these 128 branches have exact rational Farkas contradictions. The
other 16 have complete integer trees with 775 leaves. Thus frame 6 is
entirely excluded. The entry point
[verify_frame6.py](../../integral_gram/verify_frame6.py) checks the domain,
all eight negative-indicator cases, and this complete positive frame-6
cover. In particular, the negative cases of frame 8 are covered here too.

## 3. The four surviving conductor-five allocations in frame 8

The difference of the two formal-codegree-five induced-unit constituents
has quadratic torus character \(\chi_5\). Its known modular compression
attains the norm bound \(1/\sqrt5\). Equality forces the generated
representation to descend to level five, and the modular relation fixes
the primitive fifth-root residue class. Thus every high row with
\(v_4\ne v_5\) has the one primitive-five relative phase selected by its
low labelling. The complete high support in this direction has the small
integer budget

\[
\sum_{Y\text{ high}}(v_{Y4}-v_{Y5})^2=8.
\]

This is an all-level compression argument, proved in
[Q5_SATURATION_INDEPENDENT_AUDIT.md](../../modules/Q5_SATURATION_INDEPENDENT_AUDIT.md).
The frame-8 enumeration again has 20,508 raw allocations. Exact Gram
conditions leave 166. The inactive lattice leaves 32 for each of the four
positive labellings, and 112 exact Farkas exclusions among those 128
alternatives leave precisely the allocation indices

\[
\phi\in\{0,19,160,165\}.
\]

These numbers are indices in the complete enumeration, not conjectural
choices of center support. The two labelling classes are exactly
\(\{0,4\}\) and \(\{2,6\}\), by equality of the character attached to
each restriction row. Representatives 0 and 2 are both retained; their
opposite conductor-five residue choices are not identified. Thus eight
frame/label/allocation systems remain before the cyclic-four split.

## 4. A complete finite twist inventory and coupled cyclic characters

Since \(D=80(9+4\sqrt5)\) and \(9+4\sqrt5\) is an algebraic unit,
categorical Cauchy restricts the prime divisors of the Frobenius–Schur
exponent to 2 and 5. Take the relative trace field
\(K=\mathbb Q(\sqrt5,\zeta_8)\). For a twist of order \(2^a5^b\),
the relative trace of its \(2^j\)-th power vanishes on the two-primary
factor if \(a>j+3\), and on the five-primary factor if \(b\ge2\).
Consequently the relative moment tuple

\[
(\mu_1,\mu_2,\mu_4,\mu_8)
=\bigl(t_K(\theta),t_K(\theta^2),t_K(\theta^4),t_K(\theta^8)\bigr)
\]

has exactly 61 possible values: 24 with first moment nonzero, 12 whose
first nonzero moment is the second, 12 whose first is the fourth, 12 whose
first is the eighth, and the all-zero tuple. The 60 visible tuples are
realized by roots of order dividing 320. The zero tuple represents all
orders with \(a\ge7\) or \(b\ge2\); no bound of 320 on actual twists
is imposed.

The source-fixing square-action packets have size
\(2^{\max(a-3,0)}5^{\max(b-1,0)}\). The genuine-zero counts therefore
lie in the additive monoid \(16\mathbb N+5\mathbb N\). Where actual
positive Galois transport fixes a row up to duality, the refined zero
packet divisors are 16, 32 and 10 for exact five-primary parts 1, 5 and
at least 25. The row-fixing field
\(L=\mathbb Q(\sqrt5,\sqrt{-2})\) contains the source-character field
\(\mathbb Q(\sqrt5)\), so fixing \(L\) gives valid, possibly weaker,
packet conditions. It is distinct from the relative trace field \(K\).
The all-order proof and independent 320-root verification are in
[POWER_MOMENT_PHASES_PROOF.md](POWER_MOMENT_PHASES_PROOF.md).

Pivotal rotation on \(\operatorname{Hom}(1,X^n)\) has order dividing
\(n\). The block-rotation identities give

\[
\begin{aligned}
\operatorname{Tr}R_4&=\nu_4(X),&
\operatorname{Tr}R_4^2&=\nu_2(X^2),\\
\operatorname{Tr}R_8&=\nu_8(X),&
\operatorname{Tr}R_8^2&=\nu_4(X^2),&
\operatorname{Tr}R_8^4&=\nu_2(X^4).
\end{aligned}
\]

Their eigenspace multiplicities are nonnegative integers. Indicators of
\(X_i^2\) and \(X_i^4\) are obtained by fusion-linearity from the same
simple-object indicators, including the unit contribution. The center
formula connects these cyclic characters to the twist moments:

\[
D\nu_n(X_i)=\sum_Yv_{Yi}z_Y\theta_Y^n.
\]

For \(n=4,8\), \(K\) contains the indicator field, so the relative-trace
equations determine the full indicators. Using the actual eight
eigenspace multiplicities retains the correct lattice
\(\mathbb Z[\zeta_8]\); it does not incorrectly require the separate
\(\sqrt2\) and \(i\sqrt2\) coefficients to be integers. The universal
theorem and references are in
[CYCLIC_ROTATION_OBSTRUCTION.md](CYCLIC_ROTATION_OBSTRUCTION.md).

## 5. Exact integer systems and the norm-slack parity check

For each of the two label representatives, the source reconstruction
produces a C8 system with 3,925 nonnegative integer variables and 665
equations. It includes restriction Gram equations, relative center traces,
low modular relations, joint central fusion-eigenvalue integrality,
conductor-five restrictions, all 56 nonunit low Verlinde triples, finite
all-word unit-coefficient congruences, a fixed integral fusion-norm
inequality, and the coupled C4/C8 characters. The independently verified
all-word calculation closes an integral order on the complete candidate
spectral domain; it does not assume a maximum word degree. Signed
congruence slacks are represented without imposing nonnegativity on the
corresponding integer word functional.

Before rebuilding either C8 system, the final verifier recomputes all 56
low-Verlinde triple coefficients on the filtered domain of 145 high orbits
with caching disabled. It compares the entire coefficient payload with
the recorded cache and uses the freshly regenerated data. The source
verification therefore does not rely on a cache hash alone.

The norm inequality follows from integral fusion coefficients, not from a
proposed categorical model. For a specified positive product \(P=AB\),
put \(n_Y=[P:Y]\), \(a=F(P)\), and \(q=\sum_Yn_Y^2\). For rational
\(x\), define \(g^*(t)=\max_{k\in\mathbb Z_{\ge0}}(tk-k^2)\).
Choosing integer chord parameters \(b_G\) on the known low constituents
gives

\[
q\ge x\cdot a+
\sum_{G\text{ low}}(2b_G+1-x\cdot v_G)n_G
-\sum_{G\text{ low}}b_G(b_G+1)
-\sum_{Y\text{ high}}g^*(x\cdot v_Y).
\]

The low coefficients are triple Verlinde expressions and \(q\) is a
quartic expression; hence this inequality is linear in the unknown row
multiplicities. Its exact parameters and coefficients are regenerated from
the raw character table. See
[INTEGRAL_FUSION_NORM_PROOF.md](INTEGRAL_FUSION_NORM_PROOF.md).

The frozen R3895 norm row has half-integral high-orbit costs, so declaring
its unscaled slack integral needs an additional argument. In both label
classes, the doubled high-cost parity vector is exactly the mod-2 sum of
the all-word equations with zero-based indices
\(346,347,359,362,373,382,385,390\). Their right-hand sides have even sum.
The norm equation, row 345, is not used in this identity. Therefore the
total high cost, and the norm slack, are necessarily integral. This parity
identity is independently checked column by column; omitting it would
leave a gap in the integer-system argument. The proof is
[R3895_NORM_SLACK_PARITY.md](../../criteria/R3895_NORM_SLACK_PARITY.md).
The later exploratory pools of scalar, virtual-product and joint norm
cuts are not needed for the final probing certificates described here.

## 6. Exhaustive C4 split and the final exact chains

After fixing each conductor-five allocation, the residual Gram must be
entrywise nonnegative and positive semidefinite. A packet whose single
copy violates either condition has multiplicity zero. The same tests give
finite integer upper bounds for every remaining orbit multiplicity; each
bound is recomputed by exact rational arithmetic and encoded with an
integer slack. No numerical PSD tolerance is used in the proof.

For the first nonunit source object, the C4 eigenspace multiplicities in
eigenvalue order \(1,-1,i,-i\) are

\[
(r,9-r,s,2-s),\qquad 0\le r\le9,\quad0\le s\le2,
\]

and \(\nu_4(X_1)=2r-9+i(2s-2)\). There are exactly 30 integer choices
for each of the eight label/allocation pairs. Exact Farkas covectors
exclude 225 of the 240 choices. For case 0, each allocation retains
\((r,s)=(5,1),(6,1)\). For case 2, allocation 0 retains only \((6,1)\),
and the other three retain both. These are precisely the fifteen final
systems, listed below. A leaf count includes the terminal contradiction.

| Label case | Allocation | \(r\) | Forced integer splits | Exact leaves | Status |
|---|---:|---:|---:|---:|---|
| 0 | 0 | 5 | 113 | 114 | Complete |
| 0 | 0 | 6 | 178 | 179 | Complete |
| 0 | 19 | 5 | 110 | 111 | Complete |
| 0 | 19 | 6 | 210 | 211 | Complete |
| 0 | 160 | 5 | 38 | 39 | Complete |
| 0 | 160 | 6 | 231 | 232 | Complete |
| 0 | 165 | 5 | 38 | 39 | Complete |
| 0 | 165 | 6 | 145 | 146 | Complete |
| 2 | 0 | 6 | 144 | 145 | Complete |
| 2 | 19 | 5 | 107 | 108 | Complete |
| 2 | 19 | 6 | 120 | 121 | Complete |
| 2 | 160 | 5 | 89 | 90 | Complete |
| 2 | 160 | 6 | 235 | 236 | Complete |
| 2 | 165 | 5 | 146 | 147 | Complete |
| 2 | 165 | 6 | 207 | 208 | Complete |

The fifteen chains contain 2,111 forced splits and fifteen terminal
contradictions, hence 2,126 exact leaves. Each final chain is replayed
independently under both normal and optimized Python; aggregate acceptance
additionally requires the source and complete-coverage gate below.

For each system \(Ax=b\), every variable is a nonnegative integer.
An integer split is the exhaustive alternative
\(x_j\le k\) or \(x_j\ge k+1\). A certificate step supplies an exact
integer Farkas covector on one side. After representing its retained bounds
by nonnegative slack variables, the verifier checks nonnegative pairing
with every column and strictly negative pairing with the right-hand side.
That side is impossible; the other side remains necessary. A final
covector excludes the last retained side. Thus a chain of \(m\) forced
splits and one terminal covector is a complete integer tree with \(m+1\)
leaves. Floating-point optimization only suggested these splits and rays;
no numerical optimizer result is a premise.

The independent standard-library verifier
[verify_r3895_probing.py](../../criteria/verify_r3895_probing.py) reconstructs
the source Gram, actual restriction-row identities, fixed packet counts,
C4 coordinates, one-packet removals and orbit capacities. It compares the
entire reconstructed matrix with its hash and checks every exact leaf.
It does not import the numerical search or its branch-matrix builder.
Its account of the finite proof is
[R3895_PROBING_INDEPENDENT_AUDIT.md](../../criteria/R3895_PROBING_INDEPENDENT_AUDIT.md).

## 7. Whole-chain replay and the conclusion gate

The strict entry point is
[verify_r3895_cyclic_chain.py](verify_r3895_cyclic_chain.py). From the
repository root, its intended final gates are:

```bash
python evidence/rank7_m5_20261020/models/sqrt5/verify_r3895_cyclic_chain.py --block-scipy --repeat 2
python -O evidence/rank7_m5_20261020/models/sqrt5/verify_r3895_cyclic_chain.py --block-scipy
```

It re-enumerates the signed quotients; regenerates the complete source row,
frame and character domains; excludes every negative-indicator and frame-6
case; replays the frame-8 allocation cover and both label classes;
independently checks all 61 phase records; regenerates the complete C8
matrices, filtered-domain Verlinde coefficients, all-word congruences,
norm inequality and norm-slack parity; verifies all 240 C4 alternatives;
and calls the independent probing verifier on exactly the fifteen
remaining branches. Missing branches, partial chains, absent terminal
covectors or changed proof inputs fail the strict gate. Generated PASS
receipts and discovery logs are not premises. The manifest binds the
actual tensor, proof data, verifier modules and mathematical notes, and
the replay is read-only.

A successful strict replay establishes that all fifteen final systems
are impossible and that they cover every remaining pseudo-unitary case.
Section 1 then excludes every complex fusion categorification. A replay
of an individual conditional branch alone has only that branch's scope;
the general conclusion requires the entire frozen chain.
