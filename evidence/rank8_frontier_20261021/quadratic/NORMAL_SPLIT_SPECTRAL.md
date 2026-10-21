# A normal-matrix spectral-support obstruction: R8_3_921

`R8_3_921` has no fusion categorification over the complex numbers. The
proof uses the same separable algebra `A=1+g` and fixed-point difference
module as [the simultaneous criterion](SIMULTANEOUS_SPLIT_MODULE.md).
Here `g=5` and the fixed basis indices are `[3,4,6,7]`. No assertion
`S_g=I` is needed.

Let `B=S_3`. The ring is commutative and index 4 is dual to index 3, so
`B B^T = B^T B`: **B is a real normal matrix**. The fixed-block bounds are

```
1 3 1 1
1 1 1 1
1 1 1 1
1 1 1 1
```

All sixteen entries are odd integers, while each diagonal entry is `±1`.
Consequently `|tr B| ≤ 4` and `||B||_F^2 ≥ 16`. The regular fusion matrix
has the squarefree annihilator

`p(t) = t (t^2-8t+6) (t^2+2t+4)`.

Since `B` is rational and four-dimensional, its characteristic polynomial
is `t^a (t^2-8t+6)^b (t^2+2t+4)^c`, where `a+2b+2c=4` and all exponents
are nonnegative integers. Its trace is `8b-2c`. Real normality implies
that the squared Frobenius norm is the sum of squared absolute values of
its eigenvalues, namely `52b+8c`. These two bounds exhaust the six
possible exponent triples:

| `(a,b,c)` | Trace | Squared Frobenius norm | Conclusion |
| --- | ---: | ---: | --- |
| `(4,0,0)` | 0 | 0 | Norm too small |
| `(2,0,1)` | -2 | 8 | Norm too small |
| `(2,1,0)` | 8 | 52 | Trace too large |
| `(0,0,2)` | -4 | 16 | Only surviving support |
| `(0,1,1)` | 6 | 60 | Trace too large |
| `(0,2,0)` | 16 | 104 | Trace too large |

Thus all eigenvalues are roots of `q(t)=t^2+2t+4`. Normality (or the
squarefree source annihilator) gives `q(B)=0`. The following exact
identity holds in the original regular fusion representation:

`q(N_3) (-7N_1-7N_2-3N_3+30N_6-7N_7) = 148N_6`.

Faithfulness of the regular representation makes this a ring identity,
so it holds on every module representation. Hence `S_6=0`. But the
fixed-block coefficient `N[6,3,3]=1` forces `(S_6)[0,0]` to be odd. This
is a contradiction.

The proof is entirely algebraic and uses no positivity of categorical
dimensions, pivotality, sphericality, braiding, or unitarity. The norm
is the ordinary Euclidean matrix norm in an integral module basis; its
use does not impose a C*-structure on the hypothetical category.

`normal_split_spectral.py` verifies the tensor fingerprint, all source
polynomial identities, all six characteristic possibilities, and the
final parity contradiction. Independently of the trace/norm argument,
it enumerates every one of the **131,072** matrices in the full bounded
parity box, checks normality and the source polynomial, and confirms
that each surviving matrix satisfies `q(B)=0`. It uses unbounded Python
integers and no numerical tolerance, gauge reduction, or search cutoff.
Its default is read-only; `--write` regenerates the JSON evidence.

```sh
python evidence/rank8_frontier_20261021/quadratic/normal_split_spectral.py
python -O evidence/rank8_frontier_20261021/quadratic/normal_split_spectral.py
```

The categorical source is the same module-category argument documented
in the simultaneous criterion, with primary references Ostrik,
[arXiv:math/0111139](https://arxiv.org/abs/math/0111139), and EGNO,
[*Tensor Categories*, Chapter 7](https://math.mit.edu/~etingof/egnobookfinal.pdf).
