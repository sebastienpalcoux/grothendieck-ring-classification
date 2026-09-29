# Further higher-multiplicity module and Morita tests

This directory records additional necessary-condition searches. **It adds no
exclusions or categorifications.** The input is frozen by
`verification/continuation/campaign_manifest.json`, so subsequent release
decisions do not change the comparison set.

## Coverage

The original frontier contains 47 rings. The involution profile audit applies
to 21 rings, including `R6_3_215`; 20 applicable rings have multiplicity 4–8.
The two stronger searches were applied to all 46 original multiplicity 4–8
inputs, using 12 seconds per ring and stage, with four workers.

| Stage | Completed | Not applicable | Incomplete timeout |
|---|---:|---:|---:|
| Integral internal-end Gram decomposition | 14 | 26 | 6 |
| Simultaneous commuting dual action | 18 | 26 | 2 |

The recorded run took 55.813 seconds overall. All completed searches retain a
solution. Timeout is explicitly inconclusive. In particular, this audit must
not be interpreted as allocating any additional negative result.

Integral Gram timeouts: `R6_4_146`, `R6_4_416`, `R6_4_427`, `R6_5_100`,
`R6_5_638`, `R6_7_1225`.
Simultaneous-action timeouts: `R6_5_638`, `R6_7_1225`.

Among the 18 completed simultaneous-action cases, 16 have six dual simples
and force the original fusion ring again, up to a based isomorphism. The
remaining two, `R6_5_100` and `R6_5_408`, each retain six nonfaithful action
tuples on a rank-12 dual. Those two rings are excluded by the separate
`new_morita_order6` classification; this weaker module audit does not exclude
them. `R6_4_162` also survives the module audit and is excluded separately by
rank-three subring descent.

## Necessary conditions used

For a categorifiable ring with the split involution algebra `A=1+g`, the
existing exhaustive anti-representation routine supplies all allowed module
actions `M_i`. For each simple module `m`, the internal-end Gram matrix is

`G_m = sum_i (M_i)_{m,m} M_i`.

After subtracting the unit dual object, its nonnegative integral Gram columns
have prescribed Frobenius–Perron dimensions and prescribed counts. The first
search exhausts combinations of columns within every dimension class. It
strengthens the existing rational linear feasibility test to integral
feasibility.

The second search requires every dual simple to act by one simultaneous
nonnegative integral matrix `X`. It imposes `XM_i=M_iX`, fixes the column at
the algebra module using the decomposition of `I+M_g`, and bounds every
entry using the diagonal entries of `G_m-I`. All surviving tuples must
satisfy every internal-end Gram identity. If their action is faithful, its
multiplication tensor is reconstructed exactly. These are necessary
categorical conditions; feasible based actions alone do not construct
associators.

## The E6 subcategory of R6_6_1035

The closed basis `{0,1,4}` has the E6 fusion rules
`g²=1`, `gx=xg=x`, `x²=1+g+2x`.
Hagge and Hong, *Some non-braided fusion categories of rank 3*, Theorem 1,
[arXiv:0704.0208](https://arxiv.org/pdf/0704.0208), classify all four
categorifications as Galois conjugates, without an assumed pivotal or unitary
structure. Consequently the standard E6 connected separable algebra `1+x`
is available in every categorification of this subring: apply the same
Galois automorphism to its algebra and separability morphisms.

For this algebra in `R6_6_1035`, the free-module Gram `I+N_x` has exactly one
nonnegative integral factorization, with an invertible 6-by-6 factor. Hence
the module action is forced. Its dual free-module Gram also has exactly one
invertible 6-by-6 factor. The reconstructed dual ring is isomorphic to
`R6_6_1035` again. Thus this additional condensation is a rigorous surviving
self-Morita possibility, not an existence proof and not an exclusion.

## Reproduction

From the package root:

```sh
python research/higher_continuation/module_saturation.py --seconds 12
python research/higher_continuation/module_saturation.py --profiles
python research/higher_continuation/e6_condensation.py
python -O research/higher_continuation/e6_condensation.py
```

The JSON files retain exact coordinate dimension profiles, column-domain
sizes, completed action tensors and isomorphisms, plus explicit timeout
records. `involution_profiles.json` records the complete frozen 47-ring
profile scan. A single profile can be recomputed with
`module_saturation.py --one R6_6_1035 --stage profile`.
