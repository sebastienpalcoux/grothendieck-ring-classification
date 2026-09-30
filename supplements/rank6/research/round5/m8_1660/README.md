# R6_8_1660: exact restriction-profile frontier

The ring remains unresolved. The general signed reduction proves that every categorification has a pseudo-unitary Galois conjugate. The complete actual-root refinement now leaves **168 profiles in the first low frame and 798 for each of the two labellings of the second frame**; see [the actual-root certificate](../m8_actual48/certificate.json) and [its replay](../m8_actual48/replay_O.json). The files in this directory reconstruct the preceding complete restriction-profile domains on which that refinement operates.

The two saturated dimension-field characters have conductors 24 and 12. Their Fourier coefficients force actual twist support. Combining that support with the Ising subcategory's **individual actual-root mass** eliminates every sigma-supported column except those with sigma multiplicity one. Every actual central twist has order dividing 48; this is a theorem, not an imposed search cutoff.

| Low frame | Admissible high columns | Cubic profiles per labelling | Through degree six and quadratic Gram | Center rank range |
|---|---:|---:|---:|---:|
| 0 | 20 | 371 | 371 | 25–76 |
| 1 | 52 | 2011 | 1999 | 25–82 |

Each frame has two character labellings, with identical retained profile lists. The exact affine searches visit 1009 and 63366 nodes per labelling. No numerical infeasibility report is used as proof.

`low0_profiles.json` and `low1_profiles.json` retain the complete cubic lists in `branches[].cases[].profiles`. **The final domain is indexed by `cases[].gram_filter.survivor_indices`.** In frame one, the twelve excluded raw indices are 754, 755, 769, 778, 787, 793, 799, 800, 814, 823, 832, and 838. Reading only the first 1999 raw profiles would be incorrect.

From the package root, replay the general categorical reduction and both complete enumerations:

```sh
python -O research/round5/m8_1660_conductor/replay_reduction.py
OPENBLAS_NUM_THREADS=1 python -O software/round5_1660.py --verify --output research/round5/m8_1660/low0_profiles.json --receipt research/round5/m8_1660/low0_replay.json
OPENBLAS_NUM_THREADS=1 python -O software/round5_1660.py --verify --output research/round5/m8_1660/low1_profiles.json --receipt research/round5/m8_1660/low1_replay.json
python -O research/round5/m8_1660/verify_sigma_partitions.py --verify
```

The receipts bind the census, certificate, and all loaded in-package Python sources by SHA-256. Verification explicitly disables linear and integer numerical optimizers and works with Python assertions disabled.

The small sigma-partition control checks the displayed Fourier forms, the exact individual sigma dimensions, all retained profiles' sigma multisets, and opposite-root first-trace cancellation. There are only two sigma multisets; both admit cancellation. This control supplies no further exclusion and is not a full twist assignment.

The canonical proofs are in `papers/chapters/frontier_1660.tex`, with the shared saturated-conductor and individual-capacity theorems in `signed_character_fields.tex` and `unified_gram.tex`. The stronger actual-root twist campaign is maintained separately in `research/round5/m8_actual48/`.

Earlier projected-twist and rank-37 word-factorization witnesses were superseded: the individual-root capacity already excludes their entire restriction profile. Their exploratory payloads are omitted from this deliverable.

The full-center projection theorem also forces a nine-dimensional Ising-center modular subrepresentation. [Its exact support check](../m8_modrep/ising_projection_rank_replay.json) covers all 4740 labelled profiles here. The complete finite-group spectrum cone and its Ising complement adapter are documented in [m8_modrep](../m8_modrep/README.md); these representation conditions alone do not establish a category.
