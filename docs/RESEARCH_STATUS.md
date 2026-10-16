# Research status and verification

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The [public atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
connects the current manuscripts, fusion rules, classification tables and
reproducible evidence. Publication makes the material accessible; it does not
confer mathematical validation.

## Current classification

The [current research account](../docs/RESEARCH_STATUS.md) records **35 decisions among 38 cases**: 28 proposed general exclusions and 7 unitary constructions. Three general questions remain open: `R6_4_155`, `R6_8_1660` and `R8_2_24`. The combined residual program records 139 decisions (119 exclusions and 20 constructions), all subject to independent mathematical verification.

[All 38 cases and current proof references](CASE_INVENTORY.md).

Rank six records **25,362 exclusions, 57 realizations and
2 open cases** through multiplicity nine. Its complete contiguous
range ends at three; exact bands 1, 2, 3, 5, 6, 7, 9 are complete. Rank seven records
**4,172 exclusions and 29 realizations**,
with no open case through multiplicity four. Rank eight records
**895 exclusions, 77 realizations and
one open case** through multiplicity two: multiplicity one is complete and
multiplicity two is partial.

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 semion-centralizer modular candidate; a rank-22 based module satisfies the fermion Azumaya linking identities. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | One relative-center based ring, three possible Morita-dual rings and a bounded center-profile domain; saturated traces force `nu_3(T)=2`. | A categorification or an obstruction covering every possible profile. |
| `R8_2_24` | A rank-four neutral component and a required tensor autoequivalence whose square is the indicated inner action. | A general categorical obstruction or construction; the mixed transport identities in the proposed local approach are unproved. |

A necessary-condition witness is neither a categorification nor a general
nonexistence proof. Scoped unitary, pseudo-unitary, pivotal or braided
obstructions retain their assumptions and do not change a general open status.

## Reading the labels

| Label | Meaning within this project |
|---|---|
| **Realized** | A categorical construction is recorded, subject to mathematical review. |
| **Excluded** | An obstruction is recorded under its stated assumptions. |
| **Complete** | Each ring in the specified band has a recorded realization or general exclusion. |
| **Unresolved** | Neither a general exclusion nor a categorification is established. |
| **Certified**, **verified**, **PASS** | The stated program checks passed; read their scope and hypotheses. |

Reports described as independent audits are separate AI review passes unless
an explicitly identified human review says otherwise. They are not independent
human verification. Hashes establish source identity; they do not prove the
mathematics. Successful computation does not validate the categorical reduction
making that computation relevant.

Read the [verification scope](PREPUBLICATION_REVIEW.md), [replay guide](VERIFY.md)
and [provenance](PROVENANCE.md) together with the
[manuscripts](../manuscripts/README.md). A [repository issue](https://github.com/sebastienpalcoux/grothendieck-ring-classification/issues)
identifying the ring, theorem and exact failing step makes a reported gap actionable.
