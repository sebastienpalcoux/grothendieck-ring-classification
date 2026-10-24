# General exclusion of R9_2_1965

**Theorem.** The based ring `R9_2_1965` is not the Grothendieck ring of a fusion category over the complex numbers.

This is a general exclusion, not merely a braided, unitary, solvable, weakly group-theoretical, or group-theoretical exclusion. The new argument forces a hypothetical categorification to be group-theoretical and then applies the independently audited phase-4 exclusion of that class. In particular, it does not assert that every integral category of dimension 168 is group-theoretical.

## 1. Input and categorical tools

Use source labels 0 through 8. The positive dimension vector is

`(1,6,6,6,6,1,2,3,3)`,

the dual permutation is `(0,2,1,4,3,5,6,7,8)`, and the global dimension is 168. Put `g=b5` and `u=b6`. The invertible group is `{1,g}=C2`. The based adjoint subring is the entire ring, so the universal grading group is trivial. These statements, all fusion axioms, and every finite identity below are checked by `verify_general_exclusion.py` against `source_tensor.json`. The tensor's canonical compact-JSON SHA256 is

`07dac58d848bd451d8a3d9231bfd1c23c1b0117541e6de5055fa0ab90314c4f9`.

Suppose that C categorifies this ring. Since its dimension is integral, C has its canonical positive spherical structure. Write F: Z(C) → C and I for its right adjoint. For any irreducible representation E of the complexified fusion ring, there is a distinguished simple A_E in I(1) satisfying

\[
[I(1):A_E]=\dim E,\qquad \dim A_E=\frac{\dim C}{f_E},\qquad\theta_{A_E}=1.
\]

For a scalar ring character χ, the associated central simple satisfies

\[
\frac{S_{A_\chi,Z}}{\dim A_\chi}=\chi(F(Z)). \tag{1}
\]

The induction matrix is a Gram matrix:

\[
B_{ij}=[FI(b_j):b_i]=\sum_Z [F(Z):b_i][F(Z):b_j],
\qquad FI(b_j)=\sum_t b_t b_j b_t^* . \tag{2}
\]

The order of multiplication in (2) matters because the source ring is noncommutative. Removing any specified central-simple summands from this Gram decomposition leaves a positive semidefinite matrix.

Primary references for these tools are [Ostrik, arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Proposition 2.4, Theorems 2.5 and 2.13, and Example 2.9 with the discussion preceding Theorem 2.13; also [Deshpande, arXiv:1611.04486](https://arxiv.org/abs/1611.04486), Proposition 2.8 and Section 2.7. None requires the fusion ring to be commutative. Pseudo-unitarity and its canonical structure are [EGNO, *Tensor Categories*](https://math.mit.edu/~etingof/egnobookfinal.pdf), Proposition 9.6.5 and Corollary 9.6.6.

## 2. A central Tannakian lift of g is impossible

Assume there is a central Tannakian `Rep(C2)` whose nontrivial character forgets to g. The forgetful restriction to this subcategory is fully faithful. De-equivariantization by its regular algebra `1+g` gives a fusion category D of dimension 84 and a dominant free-module tensor functor Q: C → D (EGNO Theorem 8.23.3).

Tensoring with g has orbits

`{0,5}, {1,3}, {2,4}, {6}, {7,8}`.

By free-module adjunction, Q of each simple in a two-element orbit is simple, with the same dimension as the source. The fixed dimension-two simple u has `dim End(Q(u))=2`. Hence it splits into two distinct simples. Their dimensions sum to two and each is at least one, so both are invertible. Thus D has precisely three invertibles `1,a,a²`, and its remaining simples are `Y,X,Z`, of dimensions `3,6,6`, respectively. Dominance ensures that this list is exhaustive. The source images are

| Source | Q-image |
|---|---|
| b0,b5 | 1 |
| b1,b3 | X |
| b2,b4 | Z |
| b6 | a+a² |
| b7,b8 | Y |

The order-three group of invertibles fixes Y, X and Z under both left and right multiplication: it acts on a one-element set of dimension-three simples and a two-element set of dimension-six simples. Applying Q to the source products now forces all of the following:

\[
\begin{aligned}
&a^3=1,\quad aY=Ya=Y,\quad aX=Xa=X,\quad aZ=Za=Z,\\
&Y^2=1+a+a^2+2Y,\quad YX=XY=3X,\quad YZ=ZY=3Z,\\
&X^2=2X+4Z,\quad Z^2=4X+2Z,\\
&XZ=ZX=1+a+a^2+3Y+2X+2Z.
\end{aligned} \tag{3}
\]

In particular D is integral. We next give a short theoretical obstruction to (3).

### The dimension-84 induction-Gram obstruction

In basis `(1,a,a²,Y,X,Z)`, (2) gives

\[
B=\begin{pmatrix}
6&3&3&8&4&4\\
3&6&3&8&4&4\\
3&3&6&8&4&4\\
8&8&8&28&12&12\\
4&4&4&12&52&24\\
4&4&4&12&24&52
\end{pmatrix}.
\]

Since (3) is commutative, all six irreducible ring representations are scalar. Its formal codegrees are `3,3,4,28,28,84`, as verified by the characteristic polynomial of the Casimir/induction matrix:

\[
\det(fI-B)=(f-3)^2(f-4)(f-28)^2(f-84).
\]

Consequently I_D(1) has six distinct simple constituents, of dimensions `1,3,3,21,28,28`, each with multiplicity one. The dimension-one constituent is the central tensor unit. Let v range over the restriction vectors of the five other constituents. Each has `v_0=1`, and

\[
\sum v=(5,3,3,8,4,4). \tag{4}
\]

The two dimension-three constituents each have `v_a+v_{a²}=2`, with no Y, X or Z coordinates. Thus only two of the total six a/a² coordinates in (4) remain. For each dimension-28 constituent, its dimension equation modulo three says `v_a+v_{a²}≡0 (mod 3)` after subtracting its unit coordinate. The remaining budget is at most two, so both dimension-28 constituents have zero a and a² coordinates. The dimension-21 constituent therefore has `v_a+v_{a²}=2`.

Consider the three pairs of a/a² coordinates belonging to dimensions 3,3,21. Each pair sums to two and the three pairs have total `(3,3)`. Either all are `(1,1)`, or they are a permutation of `(2,0),(1,1),(0,2)`. In the latter case, subtracting their outer products from B gives value `6−8=−2` on the vector supported as `(1,−1)` in the a,a² positions. This violates positive semidefiniteness. Thus all three pairs are `(1,1)`.

Let t be the Y-coordinate of the dimension-21 constituent, and let y₁,y₂ be those of the two dimension-28 constituents. Equation (4) gives `t+y₁+y₂=8`. Remove from B the outer products of all six distinguished restriction vectors, and call the residual matrix M. Its a,Y principal entries satisfy

\[
M_{aa}=3,\quad M_{aY}=8-t,\quad
M_{YY}=28-t^2-y_1^2-y_2^2\le28-t^2-\frac{(8-t)^2}{2}.
\]

Therefore

\[
\begin{aligned}
\det M_{\{a,Y\}}
&\le84-3t^2-\frac52(8-t)^2\\
&=-\frac{(11t-40)^2}{22}-\frac{36}{11}<0.
\end{aligned}
\]

This contradicts (2). Hence (3) has no fusion categorification, and the proposed central Tannakian lift of g cannot exist.

For reference only, the full tensor (3) matches the already excluded lower-census ring `R6_4_38`, under permutation `(0,1,2,5,3,4)`. The preceding proof is independent of its existing exclusion certificate.

## 3. Scalar codegrees force a nontrivial Tannakian subcategory

Set z=−1+√(−7) and z̄=−1−√(−7). Direct substitution in all 81 multiplication equations gives two scalar ring characters

\[
\chi_+=(1,z,\bar z,z,\bar z,1,2,3,3),\qquad
\chi_-=(1,\bar z,z,\bar z,z,1,2,3,3).
\]

Their formal codegrees are both 56. Thus there are two distinct distinguished central simples A₊,A₋ of dimension three, each occurring once in I(1), and each having twist one.

Their restrictions contain the unit once. The remaining dimension two can only be either `2g` or `u`: no additional tensor unit is allowed, because its multiplicity is exactly one. The source induction matrix has `B_{0,5}=1`. A restriction `1+2g` would contribute two to this entry and is impossible. Therefore

\[
F(A_+)=F(A_-)=1+u. \tag{5}
\]

Using (1) and (5), for every σ,τ∈{+,-} we obtain

\[
S_{A_\sigma,A_\tau}=3\chi_\sigma(1+u)=9
=\dim A_\sigma\dim A_\tau. \tag{6}
\]

We spell out why (6) gives actual centralization without any assumption of unitarity. The balancing formula, together with the trivial twists of Aσ and Aτ, says

\[
9=\sum_W N_{A_\sigma,A_\tau}^{W}\theta_W\dim W,
\qquad
9=\sum_W N_{A_\sigma,A_\tau}^{W}\dim W.
\]

All dimensions are positive, and twists are roots of unity. Equality in the triangle inequality forces θ_W=1 for every constituent W. The balancing identity for the double braiding consequently says that the double braiding is the identity. Thus A₊ and A₋ centralize one another and themselves. The fusion subcategory E that they generate is symmetric. Its twist is identically one: this follows on all tensor words from balancing and then on their summands and duals. A positive spherical symmetric fusion category with trivial twist is Tannakian. Thus

`E ≃ Rep(G)`

for a nontrivial finite group G. Here one can use EGNO's symmetric-category classification in Section 9.9; the nontrivial super case has a nontrivial canonical parity twist, which is absent here.

## 4. The Tannakian subcategory must be Lagrangian

The kernel of `Inv Z(C) → Inv C` consists of half-braidings on the tensor unit, equivalently tensor automorphisms of the identity functor. These are the characters of the universal grading group. The source adjoint closure is all of C, so this kernel is trivial.

It follows that `Inv E` injects into `{1,g}`. If it were nontrivial, E would contain a Tannakian `Rep(C2)` whose nontrivial character forgets to g. Section 2 excluded precisely this situation. Therefore `Inv E` is trivial: G has no nontrivial one-dimensional representations and is perfect.

Let E′ be its centralizer in Z(C). The centralizer dimension theorem and de-equivariantization give a fusion category `(E′)_G` of dimension

\[
\operatorname{FPdim}((E')_G)=\frac{168^2}{|G|^2}.
\]

This rational number is an algebraic integer, so it is an integer. A rational number whose square is an integer is itself an integer; hence `|G|` divides 168.

Every group of proper-divisor order of 168 is solvable. Indeed, the orders involving at most two primes are covered by Burnside's theorem. The only proper divisors involving all three primes 2,3,7 are 42 and 84; in either order the Sylow-seven number divides 6 or 12 and is congruent to one modulo seven, so it is one. The quotient by this normal C7 has order 6 or 12 and is solvable. Since a nontrivial perfect group is not solvable, necessarily `|G|=168`.

Therefore `FPdim E=168` and `FPdim Z(C)=168²`. Since E is symmetric, the centralizer dimension formula now yields `E=E′`: it is a Lagrangian subcategory. EGNO Corollary 9.13.6 implies that C is group-theoretical.

## 5. Contradiction with the complete group-theoretical obstruction

Phase 4 already excluded every group-theoretical categorification of `R9_2_1965`. The proof is Section 5 of `phase4/integral/GROUP_THEORETICAL_OBSTRUCTIONS.md`, with independent replay in `phase4/audit_integral_gt/AUDIT.md`.

Briefly, the all-twists projective-character reduction exhausts all 57 groups of order 168 and all 1,751 subgroup conjugacy classes. Only `(PSL(2,7),S4)`, for the two S4 conjugacy classes, survives. Restriction on third cohomology is injective: its kernel is seven-primary, whereas the Sylow-seven normalizer acts without fixed points on `H⁴(C7,Z)`. Thus every admissible associator is globally trivializable. Both classes in `H²(S4,C*)` extend from `H²(PSL(2,7),C*)` and can be removed by a global tensor autoequivalence. The resulting untwisted tensors are `R9_2_1557`, not `R9_2_1965`. Their duality types already differ (seven versus five self-dual simples).

The group-theoretical exclusion is incompatible with Section 4. This proves the theorem.

## 6. Exact replay and scope

From the workspace root, run:

```sh
python rank9_m2_research/phase5/integral168/verify_general_exclusion.py
```

The verifier checks all fusion axioms for both tensors, the universal adjoint closure, the exact two scalar characters over Q(√−7), their formal codegrees, the source induction entry used in (5), every coefficient of the forced quotient ring map, its full induction Gram matrix and formal-codegree polynomial, and the polynomial identity giving the strictly negative minor. It also checks every coefficient of the optional lower-rank identification and records SHA256 bindings to the previously audited group-theoretical proof.

The certificate establishes finite algebraic premises; the categorical deductions are the proof above. No search cutoff, numerical optimization failure, assumption of unitarity, or assumed classification of all integral dimension-168 categories is used. No repositories or published material were changed by this research.
