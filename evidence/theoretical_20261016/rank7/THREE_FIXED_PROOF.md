# Seven general exclusions from three fixed simples

No pivotal, spherical, braided, or positivity assumption on categorical dimensions is used.

## The anti-invariant module representation

Let a complex fusion category have a commutative Grothendieck ring, an invertible simple `g` of order two, and precisely three simples `F1,F2,F3` fixed by tensoring with `g`. The rank-one module category afforded by any fixed simple over the pointed subcategory trivializes its associator. Thus `A=1⊕g` is a connected separable algebra. Every fixed simple has two right A-module structures, because `H²(C2,C×)=0`. A free two-element orbit has one simple right A-module, whose underlying object is the sum of the orbit.

Twisting an A-module by the algebra automorphism that is `+1` on 1 and `−1` on g exchanges the two structures over each fixed simple and fixes the free-orbit modules. It commutes with the left action of the entire category. Its minus eigenspace has basis `Fi,+ − Fi,−` and dimension three. The action of a simple X on this space is an integer matrix `T_X` with

* `|T_X[a,b]| ≤ N_{X,Fa}^{Fb}` and `T_X[a,b] ≡ N_{X,Fa}^{Fb} (mod2)`;
* `T_1=I`, `T_{X*}=T_X^t`, and all source multiplication relations;
* normality `T_X T_X^t=T_X^t T_X`, since the source ring is commutative;
* every eigenvalue belongs to the spectrum of the source fusion matrix `N_X`.

The last statement follows by applying the ring representation to the squarefree part of the source characteristic polynomial, which annihilates X in the complexified semisimple fusion ring. There is no use of a categorification's dimension character here.

## Integral pair R7_2_116 and R7_2_261

In the source ordering, take `(g,X,F)=(1,2,(4,5,6))` and `(3,1,(4,5,6))`, respectively. The bound matrix for `T_X` is

```
B = [[0,1,1],[1,0,1],[1,1,2]].
```

The source spectra are contained in `{0,1,−1,5}` and `{0,1,−1,i,−i,5}`, respectively. The maximum absolute row sum of `T_X` is at most four, excluding eigenvalue five. Normality then implies operator norm at most one. But its first row contains two entries of absolute value one, so its Euclidean norm is square root two. Contradiction.

## Quadratic pair R7_3_364 and R7_3_938

Take `(g,X,F)=(1,4,(4,5,6))` and `(3,4,(4,5,6))`. The simple X is self-dual, so

```
T = [[a,b,c],[b,d,e],[c,e,f]],
B = [[3,1,2],[1,1,2],[2,2,2]],
```

where `a,d,b` are odd and `c,e,f` are even. The squarefree source polynomial is

`x(x²−8x−8)(x²−2x−2)`.

Because T has integral characteristic polynomial of degree three, its eigenvalue multiset is either three zeros, `{0,4±2√6}`, or `{0,1±√3}`. All-zero spectrum forces the symmetric matrix T to vanish, contrary to parity. The large pair has trace-square eighty, whereas `tr(T²)≤32`. For the small pair, `tr(T)=2`, `tr(T²)=8`, and `det(T)=0`. The parity constraints imply `c=e=0`, `|a|=|d|=|b|=1`, and `|f|=2`: any nonzero c or e already contributes eight in addition to the required four, and `|a|=3` also exceeds eight. The determinant condition then forces `ad=b²=1`, so a=d. But `a+d+f` is one of `−4,0,4`, contradicting trace two.

## R7_3_970

Take g=X3 and fixed ordering `(X4,X5,X6)`. The bounds on T1 are `[[0,0,0],[0,1,2],[0,2,1]]`. Its source spectrum is contained in `{0,1,−1,i,−i,9}`. The row-sum bound three excludes nine; normality gives norm at most one. Parity forces

`T1=T2=D=diag(0,ε,η)`, where ε,η are ±1.

The bounds on T5 and T6 are `[[0,2,0],[2,2,0],[0,0,0]]` and `[[0,0,2],[0,0,0],[2,0,2]]`. Commuting with D forces their indicated off-diagonal entries to vanish. Their remaining diagonal supports are disjoint, hence `T5 T6=0`. The source product `X5 X6=2X1+2X2` instead gives `T5 T6=4D≠0`.

## R7_4_2644

Take g=X3, fixed ordering `(X4,X5,X6)`, and X=X1. Its bound matrix is `[[1,2,2],[2,1,2],[2,2,3]]`, with maximum row sum seven. Its source squarefree polynomial is

`(x−1)(x+1)(x²+1)(x²−14x+1)`.

The root `7+4√3>7` is excluded by the row-sum bound. Since the characteristic polynomial of T1 is rational, its quadratic conjugate is also excluded. The remaining eigenvalues have modulus one; normality and parity imply `T1=T2=D`, a diagonal matrix with entries ±1. The first column of T5 is zero by the source bounds. Hence `(T4 T5)[0,0]=0`. But the source product `X4 X5=2X1+2X2` requires this entry to be `4D[0,0]=±4`.

## R7_4_2683

Take g=X5 and fixed ordering `(X1,X2,X6)`. The same unit-spectrum argument, now applied to X3, gives `T3=T4=D`, diagonal with entries ±1. The first row of T1 is zero by the source bounds. Thus `(T1²)[0,0]=0`. The source product `X1²=2X3+2X4` instead gives the nonzero entry `4D[0,0]`.

## Source convention and verification

Indices start at zero with the unit X0. IDs are positions among rows of exact multiplicity in the pinned census `supplements/rank7/data/rank7_tables.txt.gz`, base commit `1592905dc573227ad03659a6370a9459d40db26c`. The verifier reconstructs source IDs, duality, involution action, all bound matrices, all displayed source products, and all spectral polynomials. Its small integer checks are receipts for the elementary inequalities in the proofs; no list of candidate categorifications or signed lifts is assumed exhaustive.
