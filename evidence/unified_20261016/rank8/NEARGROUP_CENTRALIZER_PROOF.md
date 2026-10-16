# Unitary modular constructions for R8_2_820 and R8_2_869

**Theorem.** Both census rings admit unitary modular categorifications. They are the nonpointed Müger factors of the centers of two different near-group categories with fusion rules `C5+5`.

## Categorical input and its scope

The source is D. E. Evans and T. Gannon, *Near-group fusion categories and their doubles*, Advances in Mathematics 255 (2014), 586–640, [arXiv:1208.1500](https://arxiv.org/abs/1208.1500). Proposition 6 and Table 2 construct three equivalence classes of C*-fusion categories with these near-group rules. Use the first and second entries for `G=C5`:

| Case | Near-group parameter c | Pairing parameter m | Auxiliary group G' | Auxiliary quadratic form Q' |
|---|---|---|---|---|
| R8_2_820 | −1 | 1 | C3×C3 | (x²+y²)/3 |
| R8_2_869 | exp(2πi/3) | 2 | C9 | 2x²/9 |

Proposition 7(b) supplies the center formulas used here. The paragraph immediately following Conjecture 2 establishes their identification with the actual near-group centers for every odd group order at most 13, including these two cases. Thus the argument uses the established finite result at order five; it does not assume the general conjecture. Their categorical existence comes from the C*-categories and their actual centers, rather than from abstract modular data alone. The third Table 2 entry is conjugate to the second and is unnecessary for existence.

## A common centralizer construction

Set

\[
 a=\frac{5+3\sqrt5}{2},\qquad
 b=a+1=\frac{7+3\sqrt5}{2},\qquad
 c=a+2=\frac{9+3\sqrt5}{2}.
\]

The near-group category has dimensions five copies of 1 and one copy of a. Since `a²=5b`, its global dimension is `5c`. Its unitary Drinfeld center therefore has global dimension `25c²=225b`.

Write `h(g,h)=exp(2πi mgh/5)`. The five invertible center objects `a_g` have restricted normalized S pairing `h(g,h)²`. This pairing is nondegenerate because `2m` is invertible modulo 5. They generate a nondegenerate pointed fusion subcategory P of dimension five. The Müger decomposition theorem gives

\[
 Z(\mathcal C_m)\simeq P\boxtimes B_m,
 \qquad B_m=P',\qquad \operatorname{FPdim}(B_m)=45b.
\]

In particular, B_m is an existing unitary modular category.

Its simple objects can be read off directly from monodromy with `a_g`. For objects `a_h,b_h,d_{h,γ}` the monodromy is trivial precisely when `h=0`. For `c_{k,l}` it is trivial precisely when `k+l=0`. Consequently its complete basis is

\[
 a_0,\ b_0,\ c_{1,-1},\ c_{2,-2},\ d_{0,\gamma_1},\ldots,d_{0,\gamma_4},
 \qquad \{\gamma_i\}=(G'\setminus\{0\})/\{\pm1\}.
\]

There are eight objects, all self-dual, of dimensions `(1,b,c,c,a,a,a,a)`. These dimensions sum in squares to `45b`, independently checking that the list exhausts the centralizer.

## Exact tensor identification

Let M be the unnormalized S matrix of B_m, so `S=M/sqrt(45b)`. Its first row is the dimension vector above. With B=`b_0`, C_k=`c_{k,-k}`, and D_γ=`d_{0,γ}`, its other blocks are

\[
\begin{aligned}
 M_{B,B}&=1,& M_{B,C_k}&=c,&M_{B,D_\gamma}&=-a,\\
 M_{C_k,C_l}&=c\bigl(h(k,l)^2+\overline{h(k,l)^2}\bigr),&
 M_{C_k,D_\gamma}&=0,\\
 M_{D_\gamma,D_\eta}&=-a\bigl(h'(\gamma,\eta)+\overline{h'(\gamma,\eta)}\bigr).
\end{aligned}
\]

Here `h'((x,y),(u,v))=exp(2πi(xu+yv)/3)` in the first case, and `h'(x,y)=exp(2πi·2xy/9)` in the second. Choose representatives `((1,0),(0,1),(1,1),(1,2))` in the first case and `(1,2,3,4)` in the second.

The standard-library verifier `verify_neargroup_centralizer.py` evaluates this matrix and every Verlinde coefficient using exact rational arithmetic in

\[
 K=\mathbb Q[q,z]/(q^2-5,\ z^3-3z+1),
 \qquad q=\sqrt5,\quad z=2\cos(2\pi/9).
\]

The fifth-root cosine values are `(-1±q)/2`; the ninth-root values follow the integral recurrence `P_0=2`, `P_1=z`, `P_{r+1}=zP_r-P_{r-1}`. Thus there is no floating-point approximation in the identification. It checks `M²=45b I`, all 512 Verlinde coefficients, the fusion axioms, and the complete source-tensor equality under the following unital maps:

| Ring | Model-to-source basis permutation | Source-to-model basis permutation |
|---|---|---|
| R8_2_820 | (0,2,6,7,1,3,4,5) | (0,4,1,5,6,7,2,3) |
| R8_2_869 | (0,3,6,7,1,2,5,4) | (0,4,5,1,7,6,2,3) |

The source is the lexicographically ordered multiplicity-two portion of `supplements/rank8/data/rank8_tables.txt.gz`. The archive and both selected tensors are bound by SHA-256 checks in the verifier. `model(which)` exposes the reconstructed tensor independently of the census.

The independent audit takes a different algebraic route: `verify_neargroup_centralizer_independent.py` reconstructs the tensor directly from the integer fusion formulas following Proposition 7(b), then checks associativity and all 512 entries. It gives the same two identifications. Its note also separately audits categorical existence and the finite-case scope of the center identification.

## Replay and status

```
python evidence/unified_20261016/rank8/verify_neargroup_centralizer.py --repo .
python -O evidence/unified_20261016/rank8/verify_neargroup_centralizer.py --repo .
python evidence/unified_20261016/rank8/verify_neargroup_centralizer_independent.py --repo .
```

Both normal and optimized exact-field receipts are supplied, as are the independent integer-formula receipts. All checks use the Python standard library and survive disabled assertions.

Both rings therefore have affirmative general, pivotal, spherical, pseudo-unitary, and unitary categorifiability. The separate theorem in `SIMPLE_GALOIS_PU.md` remains an additional statement about *every* categorification; it is no longer needed to settle existence.
