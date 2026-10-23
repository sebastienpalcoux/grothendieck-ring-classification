# Simple multiplicity-one Grothendieck rings through rank 11

There are **15 nontrivial rings** in the current classification. Simplicity means that the distinguished basis has no proper nontrivial subset, containing the unit, closed under products and duality. Rings are counted up to based-ring isomorphism, rather than counting their different categorifications.

| Rank | Census identifier | Ring |
|---:|---|---|
| 2 | `R2_1_1` | K0(Vec(C2)) = Z[C2] |
| 2 | `R2_1_2` | K0(PSU(2)_3) = Fibonacci |
| 3 | `R3_1_1` | K0(Vec(C3)) = Z[C3] |
| 3 | `R3_1_4` | K0(PSU(2)_5) |
| 4 | `F_{1,6}` | K0(PSU(2)_7) |
| 5 | `R5_1_10` | K0(PSU(2)_9) |
| 5 | `R5_1_16` | K0(Vec(C5)) = Z[C5] |
| 6 | `R6_1_34` | K0(PSU(2)_11) |
| 7 | `R7_1_17` | K0(PSU(2)_13) |
| 7 | `R7_1_43` | K0(Vec(C7)) = Z[C7] |
| 8 | `R8_1_92` | K0(PSU(2)_15) |
| 9 | `R9_1_44` | K0(PSU(2)_17) |
| 10 | `R10_1_52` | K0(PSU(2)_19) |
| 11 | `R11_1_182` | K0(Vec(C11)) = Z[C11] |
| 11 | `R11_1_46` | K0(PSU(2)_21) |

Here PSU(2)_k is the even-label fusion subcategory of SU(2)_k; k = 2r − 1 gives rank r. The rank-one ring K0(Vec) = Z may be added if the trivial ring is included.

Every nonunit basis generator was closed under products and duality. Independent enumeration of all unit-containing subsets gives the same simplicity decisions. The cyclic and quantum-group identifications above were verified against every integer fusion coefficient after the recorded basis permutations. Numerical dimensions only select a candidate permutation; the final identification is exact.

The six unresolved multiplicity-one rings are all nonsimple. Proper fusion subrings are witnessed by the following zero-based basis indices:

| Ring | Proper subring indices |
|---|---|
| `R10_1_114` | [0, 9] |
| `R10_1_115` | [0, 9] |
| `R10_1_152` | [0, 9] |
| `R10_1_153` | [0, 9] |
| `R10_1_179` | [0, 7] |
| `R10_1_189` | [0, 1, 2, 7, 8] |

Replay from the repository root:

```bash
python tools/list_simple_multiplicity_one.py --check
```

The exact input hashes and basis permutations are recorded in [the audit data](../data/simple_multiplicity_one_through_rank11.json). As elsewhere in this project, the completeness statement uses the current census and categorification decisions; independent human verification remains pending.
