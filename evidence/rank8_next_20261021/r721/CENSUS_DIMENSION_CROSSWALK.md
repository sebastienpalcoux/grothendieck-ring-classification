# Exact rank-eight census identification

Among the complete accepted census of **4,500 rank-eight fusion rings of multiplicity at most three**, exactly one has the FP-dimension multiset

\[
\{1,a,a,a+1,a+1,2a+1,2a,2a+2\},\qquad a=(3+\sqrt{17})/2.
\]

It is **R8_3_721**, source tensor SHA-256

`76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5`.

This statement is an exact finite census comparison. Combined with an independently constructed fusion category of rank eight having these dimensions and all fusion coefficients at most three, it identifies that category's Grothendieck ring. This file does not supply that independent categorical construction.

## Exhaustive domain

The cumulative source is `supplements/rank8/data/rank8_m3_tables.txt.gz`, with uncompressed SHA-256

`7baaa0a2018e11a0464c3f19da9030195421f04a73806c22363cf9d5eeb92a84`.

The verifier binds this to the frozen M3 source manifest, checks that all 973 earlier records survive in order, and checks exact raw-byte equality with the public census repository's cumulative source and its previous-M2 archive whenever that checkout is present. Every tensor hash is mapped bijectively to its historical identifier.

| Exact multiplicity | Records scanned |
|---:|---:|
| 1 | 96 |
| 2 | 877 |
| 3 | 3,527 |
| **Total** | **4,500** |

All four duality shards are included: 2,621 selfdual tensors, 1,278 with one dual pair, 516 with two dual pairs, and 85 with three dual pairs.

## Exact exclusion filter

For each tensor let `M[j,k]=sum_i N[i,j,k]`. Any positive dimension homomorphism `d` satisfies

\[
Md=\left(\sum_i d_i\right)d.
\]

For the required multiset, the sum is `21+5 sqrt(17)`, whose minimal polynomial is `x^2-42x+16`. Therefore that polynomial must divide the characteristic polynomial of M. The verifier calculates this divisibility over the integers for **every** source tensor; there is no floating-point tolerance or heuristic shortlist.

Only two records pass this necessary filter:

| Record | Cumulative source line | Exact normalized eigenvector |
|---|---:|---|
| R8_3_2906 | 2,003 | `1,1,(1+r)/2,3+r,3+r,5+r,5+r,(5+r)/2` |
| R8_3_721 | 3,222 | `1,(3+r)/2,(3+r)/2,4+r,(5+r)/2,3+r,(5+r)/2,5+r` |

Here `r=sqrt(17)`. The normalized eigenvectors are solved by exact Gaussian elimination in `Q(sqrt(17))`. The first has the wrong multiset. The second has the requested multiset; all 64 dimension-homomorphism identities and positivity are checked exactly. Its global dimension is `136+32 sqrt(17)`.

The source's ordering corresponds to the constructed dual's dimension ordering by

`[1,a,a',b,b',d,c,e] -> [0,1,2,4,6,3,5,7]`.

This last displayed permutation only matches dimension labels; identification up to based-ring isomorphism follows from census uniqueness, not from asserting that dimensions alone determine every tensor outside this bounded census.

## Reproduction

```sh
python evidence/rank8_next_20261021/r721/census_dimension_crosswalk.py
```

The full receipt is `census_dimension_crosswalk.json`, including input checksums, all spectral-filter survivors, the unique tensor, and its exact FP dimensions. The verifier uses explicit exceptions, so the checks also remain active under `python -O`.
