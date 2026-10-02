# Residual-case update, 2 October 2026

This update resolves **46 previously unresolved based rings**: 29 unitary constructions and 17 exclusions for all complex fusion categories. Neither rank-six residual has been resolved. The complete classification requested remains unfinished.

| Rank | Previously unresolved | New models | New general exclusions | Still unresolved |
|---|---:|---:|---:|---:|
| 6, through multiplicity 9 | 2 | 0 | 0 | 2 |
| 7, through multiplicity 4 | 75 | 7 | 9 | 59 |
| 8, through multiplicity 2 | 111 | 22 | 8 | 81 |

## Constructions

Each entry is a categorical construction together with an exact, source-bound equality of all fusion coefficients after the recorded basis permutation. A feasible modular datum alone is never counted as a model.

| Census ID | Unitary model |
|---|---|
| R7_2_1 | TY(C3)-parity-equivariantization |
| R7_2_195 | TY(C3)-twisted-C4-equivariantization |
| R7_2_218 | Rep(C13rtimesC4) |
| R7_2_313 | Adj(SU(3)_5) |
| R7_3_602 | Rep(A6) |
| R7_4_2 | Vec(Q8)^S3 |
| R7_4_2019 | C(Q8rtimesS3,Chern,S3,1) |
| R8_1_3 | C(C5 semidirect C4, inflated omega_2, C2, 1) |
| R8_1_6 | Bosonic de-equivariantization of PSU(2)_6 x C(C4,q) |
| R8_1_7 | Central square-root extension of pseudo-PSU(2)_6 |
| R8_1_11 | C2 flip extension of pseudo-PSU(2)_6 with central twist |
| R8_1_12 | Isotropic H=4C16 orbifold of Budinski NG(C16,16) |
| R8_1_14 | C2 flip extension of PSU(2)_6 with central twist |
| R8_1_15 | HI(C4) |
| R8_1_19 | (Fib x Fib) crossed C2 (factor swap) |
| R8_1_22 | TY(C3) x Vec(C4), diagonal parity subcategory |
| R8_1_23 | C3-equivariantization of Vec(Q8) |
| R8_1_25 | PSU(2)_6 crossed with its nontrivial C2 tensor action |
| R8_1_30 | TY(C6), inversion equivariantization, odd coherence -1 |
| R8_1_34 | TY(C9) inversion equivariantization with odd coherence -1 |
| R8_1_35 | TY(C3 x C3) inversion equivariantization with odd coherence -1 |
| R8_1_42 | pseudo-PSU(2)_6 crossed with its explicit C2 tensor action |
| R8_1_53 | Isotropic H=2G orbifold of Yu-Zhang NG(C4 x C4,16) |
| R8_1_69 | HI(C2 x C2) |
| R8_1_83 | Integral subcategory of m=0 S3 gauging of the three-fermion category |
| R8_2_39 | Asaeda-Haagerup AH4 |
| R8_2_154 | TY(V4) S3-equivariantization with parity action coherence |
| R8_2_484 | Asaeda-Haagerup AH5 |
| R8_2_611 | TY(V4) S3-equivariantization with strict action |

The full construction formulas, references, permutations, and replay code are in the [rank-seven supplement](../../supplements/rank7/) and [rank-eight supplement](../../supplements/rank8/).

## General exclusions

- **R7_2_75:** solvability and successive de-equivariantization force an equivariantization of a pointed category on C13 by a group of order four. Its invertible group forces that group to be V4, whose action on C13 necessarily produces two-dimensional simples. The census ring has none.
- **R7_2_252, R7_2_315:** successive de-equivariantizations force a pointed category on a group of order sixteen with an S3 action. The required orbit sizes make each transposition fix exactly two elements. The order-three action first restricts the group to C4 x C4 or C2^4, and every involution of either group fixes at least four elements. This is a purely theoretical contradiction.
- **R7_2_185:** the published F210 twisted-pentagon obstruction, Liu–Palcoux–Ren–Vercleyen, Theorem 7.2.
- **R7_3_635:** the same local twisted-pentagon contradiction survives the precisely verified eight-coefficient change. This is a derived application, not an assertion that the paper names this census tensor.
- **R7_3_900, R7_3_991:** the exact necessary inequality is 2 <= 1. Each has FP dimension 40; ENO Theorem 1.6 and Galindo–Hong–Rowell Theorem 5.20 imply any categorification would be unitarizable, making the unitary obstruction unrestricted.
- **R7_3_905:** a new dimension-4pq half-partition criterion forces a Tannakian subcategory in the center and weak group-theoreticity. The resulting Frobenius property contradicts 6 not dividing 140.
- **R7_4_2727:** a dimension-120 Tannakian reduction, using its odd-order invertible group and prime-dimensional induced-unit summand, forces unitarizability and contradicts the exact support inequality 4 <= 2.
- **R8_1_26, R8_2_116, R8_2_189:** their universal gradings cannot map consistently to the Brauer–Picard groups of their pointed neutral components. A rank-one component first forces the neutral associator class to be trivial.
- **R8_2_78, R8_2_168:** a rank-one component would give a fiber functor on the neutral rank-three category. The dimension-six Hopf classification identifies its module dual as Vec(S3), of rank six, contradicting the invertibility of a homogeneous bimodule component over the rank-three neutral category.
- **R8_1_29:** successive cyclic equivariantizations reduce every possible categorification to a pointed category on V4. The two possible residual tensor actions either retain a forbidden multiplicity of two or make the three-dimensional simples nonselfdual, contradicting the census tensor.
- **R8_1_45, R8_1_47:** de-equivariantization would produce a rank-ten category containing a particular dimension-twelve fusion subcategory. Every indecomposable module category over that subcategory has rank four, so an ambient category must have rank divisible by four. This contradicts rank ten.

The proofs are included in the revised rank-seven and rank-eight manuscripts; independent reviews are retained under [audits](audits/).

The last argument gives a useful general necessary criterion: the greatest common divisor of the ranks of all indecomposable module categories over a fusion subcategory divides the rank of any fusion category containing it. The ambient category is a direct sum of such module categories. This test avoids constructing the Drinfeld center explicitly.

## Additional restricted exclusions

The portable [unitary certificate package](unitary/) contains **31 exact witnesses for 28 rings**: 22 primary-three contractions and nine support-limit violations of Lim's Minkowski inequality. Every witness is replayed with arbitrary-size integers and exact algebraic arithmetic. Five of these rings are already among the general exclusions above; the other **23 remain unresolved for general complex fusion categories**, while being excluded in the unitary class.

Ten of the 28 also have no braided complex categorification, by Dong's Corollary 3.5 (weakly integral braided categories of FP dimension less than 1800 are weakly group-theoretical) and unitarizability. Five of those ten remain generally unresolved; the other five were excluded above. These braided conclusions do not assume the original braiding is unitary.

The distinction between unitary, braided, and unrestricted nonexistence is preserved in the data. No restricted obstruction is silently promoted to a general exclusion.

## Rank-six results and limitations

- **R6_4_155:** the additional exact small B3 central-character test passes all 70 nonzero blocks of dimension at most four. This is only a necessary spectral-partition test; it constructs no braid representation or fusion category. See [the research note](rank6/R6_4_155.md).
- **R6_8_1660:** the new [tensor-quotient theorem](rank6/R6_8_1660_tensor_quotients.md) rules out proper dominant pivotal tensor quotients of the positive spherical Galois form, and therefore proper unitary tensor quotients. It does not exclude the category itself or arbitrary nonpivotal tensor functors.

The graded induction-packet identities remove **533** further center profiles for R6_8_1660, leaving **1,136 = 120 + 508 + 508**. The [rank-six addendum](rank6/research_addendum.pdf) proves this reduction and the quotient theorem. Both rings satisfy every primary-n positivity criterion. The new [exact coupling certificates](../rank6_laptop_20261002/all_p_minkowski/) also prove every Lim Corollary 3.4 inequality for all real exponents p >= 1 and all nonnegative vectors on the two six-element bases. These families are exhausted without an exclusion.

Neither ring has gained an unrestricted exclusion or a categorical model. Passing previous induction, indicator, twist, or modular-data tests remains a necessary-condition result only.

The new [structural Morita restrictions](rank6/R6_structural_morita.md) show that neither center contains a nontrivial Tannakian subcategory. Consequently, no Morita representative can be obtained as a nontrivial faithful finite-group extension or equivariantization. The complete retained Morita-ring list also excludes braided Morita representatives for R6_8_1660; the analogous result for R6_4_155 was already established. These restrictions still allow exotic nonbraided models and do not decide categorifiability.

The [local-computation package](../rank6_laptop_20261002/) provides exact Python code for further work. Its R155 program checks 226 additional braid blocks using third generalized indicators and Scott inequalities, with checkpoints and explicit timeout semantics. The full new scan has not been run during preparation and supplies no additional classification decision.

## Reproduction and preservation

From the repository root, run:

```sh
python tools/verify_residual_20261002.py
python evidence/residual_20261002/unitary/verify.py
python evidence/residual_20261002/rank6/verify_braid3.py
python evidence/residual_20261002/rank6/verify_tensor_quotient_obstruction.py
python evidence/residual_20261002/rank6/verify_packet_gram.py
python evidence/residual_20261002/rank6/verify_analytic_exhaustion.py
python evidence/residual_20261002/rank6/verify_morita_structure.py
```

The staged verifier checks the 46 approved transitions and binds every unchanged record to the previous release. The historical AnyonWiki verifier continues to verify its own earlier stage; the new stage is checked separately against the current ledgers. Earlier positive constructions and exclusion records are preserved.
