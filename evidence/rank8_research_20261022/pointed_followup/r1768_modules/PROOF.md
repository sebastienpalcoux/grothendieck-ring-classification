# R8_3_1768: free pointed action on every module category

Every complex categorification of `R8_3_1768` has a nontrivial pointed
associator on its unique subgroup `C2={1,g}`, where `g=X1`. Consequently
`g` acts freely on the simple objects of every indecomposable semisimple
module category. Every such module category has even rank, and rank two
is impossible.

Applying these necessary restrictions to the complete previously saved
induction factors leaves **21 factors on 21 possible algebra objects**,
from 61 factors on 49 objects. Their possible module ranks are **4, 6, 8,
or 12**. Among the nine previously fully determined based-module actions,
exactly three survive; their ranks are 8, 6, and 6. Fifteen of the retained
induction factors still have undetermined full actions. These results do
not classify categorical module structures and do not prove a model or
exclude the fusion ring.

## Categorical proof

The complete `C2` Fourier/indicator calculation in the parent directory
rules out all eight trivial-associator branches. The independent general
sphericalization gate in `../../pivotality/` says that every complex
categorification is spherical and has a pseudo-unitary Galois conjugate.
The two classes in `H^3(C2,C*)` have representatives with values `+1,-1`,
so Galois transport preserves whether the class is trivial. The
nontrivial-associator conclusion therefore applies without assuming a
pivotal structure, braiding, or unitarity on the original category.

If `g*m` were isomorphic to a simple module object `m`, its one-object
orbit would give a rank-one module category over `Vec_C2^omega`. The
module pentagon would then express `omega` as the coboundary of the scalar
module-associativity cochain, contrary to its nontrivial class. Thus `g`
has no fixed module simples. This is also the subgroup restriction in
Ostrik, *Module categories over the Drinfeld double of a finite group*,
Example 2.1, [arXiv:math/0202130](https://arxiv.org/abs/math/0202130).
The same argument is written out in `../../r982/MODULE_TYPES.md`.

For rank two, the free action matrix of `g` is the transposition matrix.
The fusion tensor shows that `g` commutes with every basis element.
Every other module-action matrix therefore has the form

`M_X = [[a,b],[b,a]]`, with nonnegative integers `a,b`.

The positive module dimension vector is fixed by the transposition and
is proportional to `(1,1)`. Its `M_X` eigenvalue is `FPdim(X)=a+b`, which
would be an integer for every source simple. This contradicts
`FPdim(X2)=5+sqrt(37)`. Rank two is therefore impossible.

## Exact finite filter and its scope

The previous complete finite necessary domain and its proof are in
`../../../rank8_next_20261021/quadratic/README.md`. Its
`profile_closure.json` contains all 61 surviving induction factors
`B[r,i]=[X_i tensor A:M_r]` for the 49 possible connected separable
algebra objects, after the preceding sound filters. Every row is nonzero,
and the verifier checks `B^t B=N_A` exactly for every recorded factor.

The source action of `g` on basis indices is

`(0 1)(2 7)(3 6)(4 5)`.

If a row `v` occurs with multiplicity `m`, its `g` translate must also
occur with multiplicity `m`. If the row is its own translate, its
multiplicity must be even: identical restriction rows must still be
paired as distinct module simples. These conditions exactly characterize
the existence of a free involution on the row multiset with the required
effect on restriction vectors. They do not supply the other action
matrices or a categorical module associator. The verifier applies these
row-multiset conditions and the rank-two obstruction to every saved
factor; it performs no new Gram search.

| Remaining module rank | Remaining induction factors |
| --- | ---: |
| 4 | 4 |
| 6 | 6 |
| 8 | 9 |
| 12 | 2 |
| Total | 21 |

For the nine fully determined action classes, the verifier checks the
unit, transpose duality, and all 64 source fusion products, and reads the
number of `g`-fixed module simples directly from the permutation matrix.

| Recorded class index | Rank | `g`-fixed simples | Free-action test |
| ---: | ---: | ---: | --- |
| 0 | 8 | 0 | Survives |
| 1 | 6 | 0 | Survives |
| 2 | 4 | 2 | Excluded |
| 3 | 6 | 0 | Survives |
| 4 | 4 | 2 | Excluded |
| 5 | 4 | 4 | Excluded |
| 6 | 3 | 3 | Excluded |
| 7 | 3 | 3 | Excluded |
| 8 | 2 | 2 | Excluded |

The three surviving complete actions account for six retained induction
factors. The other fifteen factors have no previously determined full
action, so they cannot be omitted from the necessary domain. In
particular, this calculation does not assert that all modules have rank
six or eight, or that any surviving nonregular module exists.

## Reproduction

`verify.py` binds the source tensor, complete preceding factor and action
files, the pointed-associator result, and the general sphericalization
gate by SHA-256. It also verifies the exact positive dimension character
in `Q(sqrt(37))` against all fusion products. Run read-only from the
repository root:

```sh
python evidence/rank8_research_20261022/pointed_followup/r1768_modules/verify.py
python -O evidence/rank8_research_20261022/pointed_followup/r1768_modules/verify.py
```

Both invocations compare the full result with `verification.json`; all
checks use explicit exceptions and remain active under optimization.
