# Rank-nine retry, 24 October 2026

## Classification outcome

R9_2_137, R9_2_1607, R9_2_1975 and R9_2_1976 remain unresolved. This retry proves new categorical restrictions and completes exact tests of their projected third-indicator consequences. It does not claim a categorification, a complete source-ring exclusion, or exhaustion of all possible approaches.

No repository or website was changed.

## New theoretical progress

1. **Direct source anticommutation.** In each of the three commutative sources, every large object X has an anisotropic stabilizer h for which the actual left and right h actions anticommute. The proof uses the internal-end algebra B=1+h and the Eilenberg--Watts bimodule of right tensor h. Its regular left action would make this functor the identity on the whole left-module component, contradicting the source's nontrivial permutation of the opposite orbit. The only other left action is the sign twist. The argument actually needs no TY-specific hypothesis once its ring-data conditions hold. It was independently audited by the rank6 and quartic-pair agents.
2. **Individual cubic restrictions.** The existing Clifford rotation theorem consequently gives `nu_3(X) in {-1,-zeta_3,-zeta_3^2}` for all twelve large source objects in R137, R1607 and R1976. Each normalized trace to Q(sqrt(2)) lies in `{-1,1/2}`. This is stronger than the prior generic cyclic-rotation constraints.
3. **All-cochain D8 restriction.** For all four sources, including noncommutative R1975, the entire forced pointed associator class is determined by its cyclic restrictions. The explicit rank-four pointed-bimodule cochain has pairing −1 on its left/right central stabilizers. Every other solution differs by an ordinary 2-cocycle, whose commutator with the central right factor is a character; it vanishes on the D8 commutator. Thus the pairing is universally −1. The large-object pointed bimodule is invertible, and each dual large object's third indicator has the same three-element necessary set.
4. **Morita transfer.** Invariance of the weighted total indicator gives a source restriction on all four large-object projected third indicators: their sum belongs to `{-4,-5/2,-1,1/2,2}`. This includes R1975, where the direct source criterion does not apply because the left/right stabilizers differ.

The precise proofs are `SOURCE_LOCAL_CLIFFORD.md` and `POINTED_BIMODULE.md`. The rank9 pointed reduction has **three types in its union**: the commutative sources allow duality shift zero or reflection; R1975 allows reflection or rotation. Only the reflection type overlaps. This correction is retained throughout the new results.

## Exact discrete center tests

The existing source center systems were strengthened by the new categorical constraints. The direct source test used its full discrete projected set, not just the convex inequality. Each of the following surviving source/sign possibilities has an exact nonnegative rational solution to the strengthened height-four necessary system:

| Source | TY sign | Four projected third indicators in exact witness |
|---|---:|---|
| R9_2_137 | − | (−1,−1,−1,−1) |
| R9_2_137 | + | (1/2,1/2,1/2,1/2) |
| R9_2_1607 | − | (−1,−1,−1,−1) |
| R9_2_1976 | − | (1/2,1/2,1/2,1/2) |

The necessary systems allow rational central multiplicities; these solutions are **not** categories or modular data. Their limited purpose is to establish exactly that this strengthened relaxation does not finish the categorification problem. The four portable integer matrices and rational witnesses have a standalone standard-library replay, including exact source/sign/height and system-size coverage checks.

For R137 with positive TY sign, 13 of the other discrete assignments have exact separating vectors and two transport to those by exact based-ring automorphisms. For R1976 with negative TY sign, 12 assignments have exact separating vectors and three transport similarly. Thus each conditional branch has only the all-1/2 projected assignment left. This is a new conditional spectrum restriction, not an exclusion: the corresponding actual third indicators belong to `{-zeta_3,-zeta_3^2}`. Self-duality is not used to assert reality.

The matrix-row semantics and relabelling completion passed a second independent audit. Both saved matrices were reconstructed entrywise from the builders, and the transported permutations fix the distinguished pointed object and TY simple. The arithmetic replays check every separating inequality, all 16 assignments in each of those two cases, and the complete multiplication tensor under each relabelling. A based automorphism is used to relabel a hypothetical categorification; no lift to a tensor autoequivalence is assumed. See `../quartic/AUDIT_DISCRETE_CLIFFORD.md`.

In these two conditional branches, the actual nonreal third indicators also force 9 to divide the Frobenius--Schur exponent. Otherwise cubing every central twist removes its 3-primary part, while the central dimensions lie in Q(sqrt(2)); the indicator formula would then put the third indicators in a cyclotomic field of conductor coprime to 3, which cannot contain a nonrational cube root of unity. This is an exponent restriction, not a ring exclusion.

For R1975, the height-six necessary system with the aggregate Morita bound has an exact rational witness at projected sum 2, which is one of the allowed discrete sums. No separate source-local Clifford condition is claimed for it.

## Reproduction

- `python verify_source_local.py`: generic internal-end/module-permutation criterion; all twelve source applications and the nonapplication to R1975.
- `python verify_pointed_bimodule.py`: exact pointed cocycle, cyclic restrictions, stabilizer cochain and mixed pairing for both TY signs.
- `python verify_discrete_witnesses.py`: all four portable exact nonnegative rational solutions.
- `python verify_discrete_branch_restrictions.py`: 25 direct exact rays and five based-ring relabellings completing the two 15-branch conditional restrictions.
- `screen_morita_third.py`: reconstruction and discovery; requires the restored earlier `rank9_m2_research` center builders, numpy, scipy, sympy and python-flint. The portable replays do not require those packages or invoke an optimizer.

The source-local theorem's independent audit is saved separately under `../quartic/AUDIT_SOURCE_LOCAL_CLIFFORD.md` and `../quartic/source_local_audit_receipt.json`. The earlier central-domain semantics, integral-center theorem and TY-spectrum proof remain inherited dependencies; the new work does not silently replace their hypotheses.

## Remaining gap

The surviving cubic spectra are compatible with the tested center conditions. A full associator construction or an additional categorical contradiction is still missing. The invertible D8 bimodule and its Clifford restrictions are necessary coherence data, not a solution of the pentagons involving three or more noninvertible objects. No central half-braiding or group grading is inferred from based centrality.
