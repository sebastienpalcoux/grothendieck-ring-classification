# Research status and verification

> [!IMPORTANT]
> **This is AI-generated research.** The results, proofs, code and data have
> not yet been independently verified by human experts or formalized in
> Lean. Treat all conclusions as provisional and use them with caution.
> Automated checks establish only their stated computational scope.

The [public atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
is a reading and exploration interface to the research record. Publication
on GitHub makes the material accessible; it does not confer mathematical
validation. Read the [prepublication review and dated errata](PREPUBLICATION_REVIEW.md)
alongside the frozen manuscripts and their supporting data.

## How to read the status labels

| Label in the research record | Meaning within this project |
|---|---|
| **Realized** | A categorical model or construction is recorded for the ring. The supporting mathematical argument still requires independent review. |
| **Excluded** | The project records an obstruction intended to exclude categorification under the stated assumptions. |
| **Complete** | Every ring in a specified band has a recorded realization or exclusion; this is a coverage claim within the current research record. |
| **Unresolved** | Neither a general exclusion nor a categorification is established by the project. A necessary-condition witness does not settle the question. |
| **Certified**, **verified**, **PASS** | A specified calculation, consistency check or replay passed the associated program's checks. Read the program and its assumptions to determine what was checked. |

These labels do not assert that a human expert has verified a proof or that
a proof assistant has checked it. Reports described as *independent audits*
within this AI-generated research record are separate AI review passes,
unless an explicitly identified human review says otherwise. They are not
independent human verification.

## What the automated evidence establishes

The repository supplies exact tensors, ledgers, source hashes, derivations
and replay programs. Depending on the program, these check algebraic
identities, finite enumerations, model matches, checksum consistency or
agreement between published counts and individual records. A checksum can
identify an unchanged source; it cannot establish that the source's
mathematics is correct. Likewise, a successfully replayed calculation does
not by itself validate the theoretical reduction that makes the calculation
relevant, or prove that every needed assumption is satisfied.

The [verification guide](VERIFY.md) describes the intended replay paths.
The [provenance record](PROVENANCE.md) identifies data sources and release
boundaries. The [prepublication review](PREPUBLICATION_REVIEW.md) records
the additional checks and limitations found before public release. The
original dated research artifacts remain available so that a later
correction can be compared with the claim it changes.

## The remaining general questions

The [17 October correction](../evidence/review_20261017/README.md) reopens
`R8_2_24`: the original exclusion uses unsupported decorated-phase cancellation;
the proposed repair lacks an established oriented g-cap/crossing sign in its
categorical-to-linear bridge. The conditional repair does not
settle that gap. The latest continuation retains 35 accepted decisions among
38 former residuals: 28 proposed exclusions and 7 unitary constructions.
Three general questions remain open: `R6_4_155`, `R6_8_1660`, and `R8_2_24`.
Necessary-condition computations do not constitute categorifications or
general nonexistence proofs. The frozen 36-decision snapshot and manuscripts
are historical; their R8_2_24 exclusion is superseded by the dated errata.

When relying on any other recorded conclusion, inspect its assumptions,
proof and computation together, and check the dated review for errata.
If you find a gap or error, a [repository issue](https://github.com/sebastienpalcoux/grothendieck-ring-classification/issues)
with the ring ID, file or theorem, and the exact failing step will help
make the correction traceable.
