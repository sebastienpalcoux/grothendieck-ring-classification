# Actual-root refinement for R6_8_1660

The ring remains unresolved. These are complete necessary-condition reductions, not constructions of a fusion category or modular datum.

Saturated dimension-character support, together with the Ising subcategory projection, proves that every actual central twist has order dividing 48. The calculation therefore uses actual powers of ζ48 rather than projected twist averages. Each of the four primitive-sixteenth-root Ising phases has weighted mass D√2/4. This distinguishes the two opposite roots that were merged in the earlier conductor-24 calculation.

The compact certificate reconstructs both complete induction-profile sources and all 16 low-frame, character-labelling, and second-indicator branches. Thirteen branches have exact Farkas certificates. The remaining three have indicators (1,1,1,−1,1), and the following complete profile reductions:

| Low frame | Character labelling | Input profiles after word constraints | Remaining profiles |
|---|---|---:|---:|
| 0 | (0,5,4,1,3,2) | 371 | 168 |
| 1 | (0,5,4,1,2,3) | 1,999 | 798 |
| 1 | (0,5,4,1,3,2) | 1,999 | 798 |

The low-frame-1 source stores 2,011 cubic profiles; its exact word filter removes 12 specified indices. The replay uses that index set, never a truncation of the list. A six-row congruence modulo 4 excludes every asymmetric Ising restriction pattern (1,6,1), forcing all eight Ising-supported central simples to have the balanced restriction vector. Exact Farkas rays are shared across profiles and checked against every applicable right-hand side.

Run the canonical optimizer-free replay from the package root:

```sh
python -O research/round5/m8_actual48/certificate.py
```

`certificate.json` contains grouped exact witnesses and the exhaustive unresolved index lists. `replay_O.json` records the independently rebuilt systems and source bindings. Discovery shards are unnecessary for replay.

The earlier rank-37 witness is excluded as a particular profile. This does not exclude center rank 37: surviving profiles still have that rank. The remaining center ranks are 28 through 76 for low frame 0 and 28 through 82 for low frame 1, in steps of three.

The additional searches are summarized in `exploration_summary.json`. The complete level-48 representation cone, with exact integer rank and root-capacity bounds, was tested on all 1,764 remaining profile/labelling cases. The forced nine-dimensional Ising-center subrepresentation was also removed in three global complementary-spectrum probes, using the correctly signed trace bounds. Neither search produced an additional exact exclusion. These are inconclusive search results, not feasibility certificates.

Reusable adapters for the saturated-character moments, exact large-prime indicators, finite modular-representation cone, and complete cyclic rotations remain alongside the proof. The cyclic-rotation equations have an independent exact `Rep(S3)` control:

```sh
python -O research/round5/m8_actual48/rotation_control.py
```
