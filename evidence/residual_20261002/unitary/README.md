# Exact analytic obstructions for the remaining fusion rings

This package certifies **28 unitary nonexistence results**: 15 rank-seven and
13 rank-eight rings. Two of these, `R7_3_900` and `R7_3_991`, are upgraded here
to **general complex nonexistence** by an independent dimension theorem.
All ten integral rings in the package also admit no braided complex
categorification, by a separately recorded theorem below. Other records
retain the unitary-only scope. The presence
of an obstruction record does not assert that other general arguments are
unavailable.

Run `python verify.py` (Python 3 and SymPy). The verifier has no numerical,
SciPy, NumPy, network, repository-path, or discovery dependency. It does not
solve new equations: it replays explicit certificates using arbitrary-size
integers and exact number fields with rational root isolation. The callable
`verify_record(record, expected_tensor=None)` can additionally bind a record
to a caller-supplied census tensor; `get_certificate(ring_id)` retrieves one.

## Primary 3 criterion

For fusion matrices `N_i[j,k] = N_ij^k` and positive Frobenius–Perron dimensions
`d_i`, unitary categorifiability requires

\[
 Q_3=\sum_i d_i^{-1}N_i\otimes N_i\otimes N_i\succeq0.
\]

This is Huang–Liu–Palcoux–Wu, *Complete Positivity of Comultiplication and
Primary Criteria for Unitary Categorification*, IMRN 2024(1), 817–860,
[arXiv:2210.00792](https://arxiv.org/abs/2210.00792), Theorem 3.12 (primary 3 criterion).
Transposing every fusion matrix only transposes `Q_3`, so the displayed
row convention does not affect its positivity.

For each of 22 records, the package supplies an explicit integer vector `v`
and the exact integer contractions `c_i = v^T N_i^{tensor 3} v`. The verifier
recomputes all contractions using Python integers and proves
`sum_i c_i/d_i < 0`. It also checks the fusion tensor's unit, duality,
associativity, and positive dimension character, and verifies the recorded
field polynomial and root-isolating interval.

Floating-point eigenvectors were used only to discover integer vectors.
No classification verdict uses floating point. Even the old discovery
contractions were safely below signed 64-bit range: the absolute bound
`max|v|^2 max_i(sum_jk N_ij^k)^3` is at most **5,927,040,000** over the package.
The portable replay uses unbounded Python integers regardless.

## Support consequence of the Minkowski criterion

Junhwi Lim, *Noncommutative Minkowski integral inequality and a unitary
categorification criterion for fusion rings*,
[arXiv:2601.13490v1](https://arxiv.org/html/2601.13490v1), Corollary 3.4,
Equation (15), gives a necessary inequality for every spherical unitary
(multi-)tensor category, every triple of simple objects, every `p >= 1`, and
every vector of nonnegative real numbers. A unitary fusion category has
its canonical positive spherical structure, whose dimensions are `d_i`.

Set that vector equal to the indicator of a subset `S` of simple labels,
and send `p` to infinity. Finite weighted `p`-norms tend to the maximum over
strictly positive weights. A nonzero nonnegative constant to the power
`1/p` tends to 1, while a zero remains zero. Thus, for every `i,j,k,l` with
`N_ij^l > 0`, the following necessary inequality holds:

\[
 \boxed{\frac{1}{d_l}\sum_{n\in S}N_{lk}^{n}d_n
 \ \leq\ \frac{1}{d_j}
 \sum_{\substack{m:\,N_{jk}^{m}>0\\
                    \exists n\in S:\,N_{im}^{n}>0}}
 N_{jk}^{m}d_m.}
\]

This is a direct consequence of Lim's theorem, rather than an assumption
about continuity of category data. There are only finitely many terms; the
limit is elementary. A strict reverse inequality supplies a finite
algebraic certificate. Nine records violate it. All labels in this table
are **zero-based census labels**, and `T` is the right-hand support set.

| Ring | `(i,j,k;l)` | `S` | `T` | Left side | Right side |
|---|---|---|---|---|---|
| R7_2_116 | (4,4,4;6) | {2,3,5} | {6} | 7/3 | 3/2 |
| R7_2_261 | (5,5,5;6) | {1,2,4} | {6} | 7/3 | 3/2 |
| R7_3_387 | (5,2,5;5) | {0,1,4} | {5} | 1 | 2/3 |
| R7_3_970 | (5,1,5;5) | {0,3,4} | {5} | 1 | 2/3 |
| R7_3_900 | (1,1,2;1) | {0,3,4,5,6} | {2} | 2 | 1 |
| R7_3_991 | (3,4,4;3) | {0,1,2,5,6} | {4} | 2 | 1 |
| R7_4_2727 | (3,4,6;3) | {4} | {6} | 4 | 2 |
| R7_3_1036 | (1,1,1;2) | {0,4} | {2} | sqrt(5) | 1 |
| R8_2_209 | (4,4,4;5) | {3,6,7} | {5} | (9+3 sqrt(29))/10 | (2+sqrt(29))/5 |

## Why two exclusions apply to every complex fusion category

The positive dimension characters of `R7_3_900` and `R7_3_991` are,
respectively,

- `(1,4,4,1,1,1,2)`;
- `(1,1,1,4,4,2,1)`.

Both give `FPdim = 40 = 2^3 * 5`. Etingof–Nikshych–Ostrik,
*Weakly group-theoretical and solvable fusion categories*,
[arXiv:0809.3031](https://arxiv.org/pdf/0809.3031), Theorem 1.6, proves that
**every** fusion category of dimension `p^r q^s` is solvable, hence weakly
group-theoretical. Galindo–Hong–Rowell, *Generalized and quasi-localizations
of braid group representations*,
[arXiv:1105.5048](https://arxiv.org/pdf/1105.5048), Theorem 5.20, proves that
every weakly group-theoretical fusion category is completely unitary; in
particular it admits a unitary structure. The strict support violation
`2 > 1` contradicts this. No pivotality, sphericality, pseudo-unitarity,
or unitarity assumption is imposed on a hypothetical original category.

`general_upgrades.json` records precisely these two upgrades and their
sources. The verifier recomputes the dimension and its prime factorization.
All 28 rings equal their adjoint based subrings, so an adjoint-grading
reduction does not add further upgrades here.

## Excluding braidings in the integral cases

Dong, *Classification of certain weakly integral fusion categories*,
[arXiv:2103.04553](https://arxiv.org/pdf/2103.04553), Corollary 3.5, proves
that every weakly integral braided fusion category of FP dimension less
than 1800 is weakly group-theoretical. Combined with GHR Theorem 5.20 and
any of the unitary obstructions above, this excludes **every braided
complex categorification** of each integral ring listed below. No
nondegeneracy assumption on the braiding is required.

| Dimension | Rings |
|---|---|
| 40 | R7_3_900, R7_3_991 |
| 120 | R7_2_116, R7_2_261, R7_4_2727 |
| 140 | R7_3_905 |
| 210 | R7_3_635 |
| 240 | R7_3_387, R7_3_970 |
| 360 | R7_3_601 |

The verifier computes these dimensions exactly and compares them with
`braided_upgrades.json`. This additional conclusion excludes braidings;
it does not, on its own, exclude unbraided categorifications.

## Inventory and controls

Primary-3 obstructions occur at:

- Rank 7: R7_4_1212, R7_4_1213, R7_4_1438, R7_3_601, R7_3_635,
  R7_3_905, R7_4_2510, R7_4_2727, R7_3_1036.
- Rank 8: R8_2_190, R8_2_209, R8_2_260, R8_2_318, R8_2_319,
  R8_2_320, R8_2_368, R8_2_370, R8_2_489, R8_2_630, R8_2_735,
  R8_2_758, R8_2_760.

The initial screen considered all 188 residuals (2 rank-six, 75 rank-seven,
111 rank-eight) and all 57 currently realized unitary rank-seven/eight
rings. The positive controls all survived. Rank-eight tensors were bound
to ledger identifiers by their complete tensor hashes; source-file order
is not ledger order. A second verifier independently rebound every stored
certificate to those census tensors and recomputed the full contractions
with Python integers.

Neither rank-six residual was excluded. Additional bounded Minkowski
optimization on them found no violation. The forced rank-26 modular fusion
candidate for `R6_4_155` also survived a bounded screen: 882 subsets,
all simple triples, `p = 1.5,2,4,16`, and the support limit. These search
outcomes are **not** proofs that all Minkowski inequalities hold and are
**not** model constructions.
