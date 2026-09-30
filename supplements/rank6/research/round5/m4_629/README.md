# R6_4_629: one necessary central modular datum

The inherited complete reduction left three induction profiles, with central ranks 30, 35 and 38. This continuation excludes ranks 30 and 38 and determines one full rank-35 central modular/fusion datum, up to complex conjugation and permutations of identical restriction--twist pairs. **The ring remains unresolved: no associator or categorification is constructed.**

The manuscript proof is `papers/chapters/frontier_629.tex`. The generic modular-word closure and finite representation argument is in `papers/chapters/unified_gram.tex`.

## Authoritative proof and replay

`modular_reduction_certificate.json` records the exact result. Rebuild it with:

```sh
python -O research/round5/m4_629/replay_inherited.py
python -O research/round5/m4_629/replay_modular_chain.py
```

The first command freshly verifies the general sphericalization/Galois reduction, all seven low frames, all 784 integral profiles, both low-character labellings and the seven inherited twist obstructions. It checks the canonical and exploratory profile lists by their complete 85-coordinate count vectors and records source/input hashes in `inherited_replay_O.json`. Historical inputs and receipts remain read only.

The replay disables `scipy.optimize.linprog` and `milp`, reconstructs the proof chain in a temporary directory, compares every exact output, and removes that directory. `modular_chain_replay_O.json` records the result and source/input/output SHA-256 hashes. Every acceptance check uses explicit exceptions rather than Python `assert`, so optimization does not remove checks. SymPy provides exact cyclotomic arithmetic; python-flint is an optional acceleration.

The input profile reduction is the inherited, separately replayed `research/round4/m4_629` proof. It covers all seven low frames, both compatible character labellings on the sole surviving frame, and all 784 integral column profiles. The full 85-coordinate count vectors, rather than traversal indices, identify profiles across inherited files. Earlier stages exclude every alternative labelling and leave ranks 30, 35 and 38 for the labelling used here.

## Complete bounded integer searches

The helper `software/round5_629.py:enumerate_with_large_bounds_first` permutes integer variables in decreasing upper-bound order before exact rational elimination. This preserves the integer solution set while preferentially eliminating rotation coordinates with large bounds. It then uses the complete inherited affine enumerator.

| Central rank | Moment height | Equations | Variables | Linear rank | Search nodes | Integer solutions |
|---|---:|---:|---:|---:|---:|---:|
| 30 | 6 | 4,323 | 405 | 350 | 203 | 0 |
| 35 | 10 | 2,476 | 587 | 523 | 4,157 | 2 |
| 38 | 10 | 1,942 | 527 | 470 | 2,408 | 2 |

The complete results are `rank30_certificate.json`, `exact_rank35_h10.json` and `exact_rank38_h10.json`. The last two each have one complex-conjugate pair. Every occupied orbit has degree one and all roots have order dividing 15. The presence of primitive fifteenth roots makes the twist exponent exactly 15. `decode_twists.py` reconstructs actual root representatives without numerical logarithms. `decoded_twists.json` stores every restriction column, multiplicity and root.

## Modular closure and the rank-38 obstruction

`modular_closure.py` uses the six known low S rows, the forced T matrix, the exact Galois signed permutations and the finite-level modular identities. The low simples are self-dual and exactly exhaust the twist-one simples. Charge conjugation fixes the generated subspace; no self-duality assumption is imposed on the unknown high simples. Exact closure increases the known rank from 29 to 30 for each profile.

For rank 38, the S row of the individual object numbered 6 is forced. `known_verlinde.py` computes the nonintegral triple multiplicity `[A1 A1 Z6 : 1] = 1/3`. The independent `independent_fraction.py` repeats this calculation with Python rational fractions modulo Phi_15, without SymPy, FLINT, optimizers or floating point. `equivalences.py` verifies that the second twist list is the exact conjugate, so both branches are excluded. Aggregate rows in `known_verlinde.json` denote sums of simples, for which the same trilinear integrality test remains necessary.

## Exhaustive rank-35 completion

The five-dimensional unknown complement has distinct T eigenvalue exponents `{2,3,8,10,12}` modulo 15. `finite_modular_reps.py` enumerates SL2(F3) and SL2(F5), their complete class algebras, and every irreducible character and T spectrum. Exactly two representation decompositions have the required spectrum: `1+4` and `1+2+2`. The latter would have a four-dimensional negative charge-conjugation eigenspace. Only two interchangeable restriction--twist pairs exist, so that decomposition is impossible.

`complete_rank35.py` constructs the remaining four-dimensional representation as a tensor product of exact two-dimensional finite Weil representations and checks every generator edge in the two finite groups. Distinct T eigenvalues reduce all possible intertwiners to diagonal ones. Symmetry fixes their relative squares, leaving exactly eight sign choices. Four fail Verlinde integrality; four satisfy all 7,140 unordered nonunit triple tests, symmetry, S squared equal to the identity, and the STS relation. `equivalences.py` checks that the four valid matrices are related by the independent interchanges `(21,22)` and `(23,24)`.

`rank35_modular_completions.json` stores all eight candidate matrices, including the failed coefficient for each rejected choice. `rank35_fusion_data.json` stores the complete retained 35-cubed fusion tensor. Every nonunit basis object generates the whole ring. `full_restriction_check.py` verifies all 3,780 coordinates of the forgetful based-ring homomorphism. Passing these tests proves no existence assertion.

## Further necessary tests

The retained datum also passes the checks in `center_indicators.json` (all second indicators are +1), `indicator_integrality.json` (ordinary original indicators through order 30), `vafa_check.json` (73,815 Vafa congruences), `generalized_rotation_spectra.json` (all 21,420 charged-object cases for each prime 2, 3, 5, 7, 11 and 13), and `relative_rotation.json` (forgetful rotation-spectrum differences for primes 3 and 5). These are additional necessary checks, not exclusions or categorifications, and are separate from the authoritative modular reduction replay. Their scripts and exact outputs are retained for continuation. The separate command `python -O research/round5/m4_629/replay_additional_tests.py` reconstructs all of them with numerical optimizers disabled; its receipt is `additional_tests_replay_O.json`.

The common modular-check engine additionally verifies generalized rotations for every composite order 4, 6, 8, 9, 10, 12, 14, 15 and 16, completing coverage of every order from 2 through 16. It also verifies signed Galois covariance and positive higher Gauss sums at every exponent coprime to 15. `composite_rotations.json` stores these exact checks and `composite_rotations_replay_O.json` records their optimizer-free replay. Rebuild the check with:

```sh
python -O software/round5_629_composite_rotations.py --verify --output research/round5/m4_629/composite_rotations.json
```

Superseded dense elimination caches, preliminary modular closure attempts, numerical solver reports and redundant logs have been removed. In particular, numerical infeasibility reports never enter any proof: a numerical solver incorrectly rejected the height-10 profiles for which the exact enumerator found the two explicit solutions.
