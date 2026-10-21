# Independent review of the R1154 Galois reciprocal-action test

This is a subsequent necessary-condition refinement. It does not change
the frozen publication, the source-ring ledger, or the unresolved status
of `R8_3_1154`.

## Theory and conventions

Let `S` be the canonical **normalized** matrix of a pseudo-unitary center:
`S[0,i] = d_i/D`, where `D` is the source category's global dimension.
For an extension of the nontrivial automorphism of `Q(sqrt(5))` to the
cyclotomic field of the modular representation, set

```
G = sigma(S) S^-1,     G[i,j] = epsilon_i delta_(pi(i),j).
```

The signed-permutation assertion, with precisely this row convention, is
Dong–Lin–Ng, *Congruence property in conformal field theory*,
Algebra & Number Theory 9(9) (2015), 2121–2166, Theorem II(iii) and
Section 4, equations (4-3)–(4-4), p. 2145. The canonical center normalization
is equation (1-10), p. 2130; Lemma 4.2, p. 2146, explicitly uses it.
Primary source: <https://msp.org/ant/2015/9-9/ant-v9-n9-p03-s.pdf>;
DOI <https://doi.org/10.2140/ant.2015.9.2121>.

For the retained R1154 restriction patterns, every eigenvalue `lambda_i`
of the distinguished selfdual action `N = N_(A1)` belongs to this quadratic
field and satisfies `sigma(lambda_i) lambda_i = 1`. Since `N` is integral,
Verlinde diagonalization gives

```
N = sigma(S) diag(sigma(lambda)) sigma(S)^-1
  = G N^-1 G^-1,
```

and consequently `N G N = G`. No claim that `G^2 = I` is used: an
extension of the quadratic automorphism need not have order two.
Writing `Y = N[:,0:5]` and using symmetry of `N` gives the necessary
finite equation `Y^T G Y = G[0:5,0:5]`.

The normalized vacuum column gives the exact signed target dimension:
`sigma(d_i/D) = epsilon_i d_(pi(i))/D`. All permitted signs and target
dimension classes are computed from the field arithmetic, not hardcoded.
Only these dimension restrictions and the displayed five-column equation
are imposed in this independent verifier. Thus its search is a valid
necessary-condition superset, even before additional modular relations.

## Independent arithmetic and complete finite search

`review.py` imports the frozen source/character setup, not the discovery
Galois test. It recomputes the low entries of `Y` using degree-three
Verlinde moments and independently verifies all 25 entries of `Y^T Y`
against degree-four moments. The high entries come from the previously
accepted complete pair-histogram domain.

For each histogram, rows with identical known data are grouped, while
each of the five low labels remains separate. A signed permutation is
then represented by an integral transportation table with the prescribed
source and target class sizes. Every nonnegative table with these margins
is realizable by a bijection of the individual labels. Conversely, every
allowed labelled permutation produces such a table. All tables are
enumerated exactly; they are compressed only when their entire 25-entry
contribution to `Y^T G Y - G_low` agrees. Complete finite sumsets of these
contributions decide feasibility.

This differs from the discovery enumeration, which lists target-row-type
assignments to individual source labels. For every retained case, the
reviewer expands its transportation solution to an actual labelled signed
permutation and directly checks the 25 scalar equations.

## Result and scope

The complete 36-histogram incoming domain is reduced to 25 histograms:

| Restriction pattern | Incoming histograms | Surviving histogram indices |
|---|---:|---|
| 6971 | 9 | 1, 2, 3, 5, 6, 7, 8 |
| 8766 | 11 | 1, 2, 3, 7, 10 |
| 8772 | 16 | 0, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15 |

The decisions agree with the independent discovery enumeration in every
case. All three restriction patterns remain possible at this level. The
25 signed-permutation witnesses are not center fusion matrices or models.

Run from the repository root:

```sh
python evidence/rank8_postpublication_20261021/r1154_galois_review/review.py
python -O evidence/rank8_postpublication_20261021/r1154_galois_review/review.py
```

The checked-in `review.json` and `review_optimized.json` bind the source
inputs and verifier. They are byte-identical. Checks use explicit
exceptions and remain active under Python optimization.
