# Testing the 2D2 route for R7_5_3895 and R7_5_5039

Both rings have global FP dimension `D=720+320sqrt(5)`, equal to
`(20+8sqrt(5))^2`. The latter is the dimension of the center of a
2D2 even part. This equality suggests a model search, but it does not
produce a model.

In fact neither ring is Morita equivalent to `2D2 boxtimes 2D2^op`,
or to `Z(2D2)`. This rules out products of any of the Morita-equivalent
even parts as well. It is not an exclusion of general categorification.

For the precise comparison, Grossman and Izumi, *Drinfeld centers of
fusion categories arising from generalized Haagerup subfactors*,
<https://arxiv.org/abs/1501.07679>, Figure 6 and Example 6.9, give
the center of 2D2. At `m=1` the first S-matrix row gives the simple
dimensions

```
1, e=9+4sqrt(5), a=5+2sqrt(5) (six copies),
b=8+4sqrt(5) (two copies).
```

Their squared sum is `D`. Consequently the center of
`2D2 boxtimes 2D2^op` has simple dimensions among pairwise products
of `1,e,a,b`. The same is true of `Z(Z(2D2))`.

Suppose a category with either census ring were Morita equivalent to
one of these known categories. Pseudo-unitarity is Morita invariant,
so it would be pseudo-unitary. For each formal codegree `f`, the
induced-unit theorem then supplies a simple object in its center of
FP dimension `D/f`.

For completeness, the pseudo-unitarity assertion follows from Morita
invariance of the center and the formulas
`dim(Z(C))=dim(C)^2`, `FPdim(Z(C))=FPdim(C)^2`, with positive global
dimension; see Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*,
Theorem 7.16.6 and Proposition 9.3.4,
<https://math.mit.edu/~etingof/egnobookfinal.pdf>.

| Ring | Formal codegree | Required central simple dimension |
|---|---:|---|
| R7_5_3895 | 4 | `180+80sqrt(5)` |
| R7_5_5039 | 8 | `90+40sqrt(5)` |

Neither required dimension occurs in the pairwise product set.
Thus the centers cannot be equivalent and the proposed Morita models
cannot realize either ring. The verifier recomputes the formal-codegree
polynomials from the census and checks the complete 100-object product
profile exactly.

This does not rule out all constructions related to the 2D2 family:
new extensions or condensations can change the Morita class. No such
construction with the required tensor has been established here.

Run `python verify_2d2_comparison.py` and
`python -O verify_2d2_comparison.py`.
