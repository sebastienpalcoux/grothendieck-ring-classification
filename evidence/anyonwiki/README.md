# AnyonWiki positive categorification update — 2026-10-01

This update corrects missed positive models in the rank-seven and rank-eight
multiplicity-one ledgers. All 139 census tensors have a unique exact based-ring
match in the pinned AnyonWiki fusion-ring tables. Dimensions and names alone
are never used as identification certificates.

| Rank | Multiplicity-one census | Generally excluded | Realized | Unresolved |
|---:|---:|---:|---:|---:|
| 7 | 43 | 30 | 13 | 0 |
| 8 | 96 | 41 | 30 | 25 |

The previously unresolved rank-seven rings are:

| Census ID | AnyonWiki ring | Exact category code | Cyclotomic conductor | Pentagon equations |
|---|---|---|---:|---:|
| `R7_1_19` | `FR_7_1_2_3` | `(7,1,2,3,1,0,1)` | 8 | 9,856 |
| `R7_1_28` | `FR_7_1_2_12` | `(7,1,2,12,1,0,1)` | 28 | 45,061 |
| `R7_1_36` | `FR_7_1_4_3` | `(7,1,4,3,1,0,1)` | 16 | 9,856 |

Independent exact arithmetic checks all 64,773 pentagon equations, all
2,007 nonempty associator blocks for invertibility, and the unit and rigidity
constraints. The checked coefficients are included under `symbolic/`. These
checks construct general complex fusion categories, without a pivotality
assumption. The external category list additionally supplies unitary-gauge
existence; unitarity of those gauges was not independently reconstructed here.

Five previously unresolved rank-eight rings have sourced unitary constructions:

| Census ID | AnyonWiki ring | Construction |
|---|---|---|
| `R8_1_36` | `FR_8_1_2_2` | `TY(C3)` crossed with `C2` acting by inversion |
| `R8_1_61` | `FR_8_1_0_4` | One-half `SO(12)_2`, a rank-eight fusion subcategory |
| `R8_1_78` | `FR_8_1_0_13` | Standard `SO(9)_2` metaplectic category |
| `R8_1_79` | `FR_8_1_0_14` | `Z(Vec(S3)) = Rep(D(S3))` |
| `R8_1_85` | `FR_8_1_0_29` | Neutral component after full `S3` gauging of `SO(8)_1` |

All five constructions have full tensor matches. The crossed-product tensor
is independently generated from the Tambara–Yamagami rules. Its inversion
action preserves the standard bicharacter and the positive parameter, and
squares strictly to the identity. The four other categorical existence claims
use the cited standard constructions, rather than an independent associator
reconstruction.

A pivotal, spherical or unitary category is also a general fusion category over
the complex field. A valid positive model therefore settles general existence.
It says nothing about whether every categorification has that extra structure.
Failure of a pivotal search alone cannot give a general exclusion. Missing
AnyonWiki flags mean unknown. The fusion-ring summary even leaves the unitary
flag blank for `FR_7_1_2_3`, although its individual category list has eight
unitary entries; the individual witness data takes precedence.

No new negative decision is imported in this update. The paper reports a
general pentagon no-go for `FR_8_1_4_2`, matching `R8_1_26`; this release keeps
that ring unresolved until a replayable negative certificate is included.
Every earlier negative record and every unaffected ledger record is unchanged.

Run from the repository root:

```sh
python tools/verify_anyonwiki_import.py
```

This checks the entire 139-ring crosswalk, all added model permutations,
preservation of the previous negative and unaffected records, and the three
exact associators. It replays supplied data; it does not search for new
associators or repeat costly unchanged negative searches. The archived earlier
full-verification reports remain distinguished from this finite update.

Sources: [AnyonWiki rings](https://anyonwiki.github.io/pages/Lists/losmffr.html),
[AnyonWiki categories](https://anyonwiki.github.io/pages/Lists/losmffc.html),
Vercleyen–Slingerland, *On Low-Rank Multiplicity-Free Complex Fusion Categories*,
CMP **407**, 231 (2026), [DOI](https://doi.org/10.1007/s00220-026-05705-2), and
Cui–Galindo–Plavnik–Wang, *On Gauging Symmetry of Modular Categories*,
[arXiv:1510.03475](https://arxiv.org/abs/1510.03475).
The symbolic data comes from the TensorCategories.jl AnyonWiki artifact with
SHA-256 `4515aecb88748e6a2b56751507fcc50bdfa9a94f39cadcf6dc95584aec101ee2`.
The copied AnyonWiki data is distributed under its MIT license.
