# General-case classification and exact replay

The full pipeline is `python3 supplementary/check.py`, run from the package root.
No pivotality assumption or pivotal classification is imported.

## Ordinary-census ledger

```sh
python3 supplementary/classification/classify.py
python3 supplementary/classification/verify.py
```

The classifier reads the **local** census in `../census/data`, finds the rank-two
and arithmetic witnesses, and assembles an exact certificate for every input.
Its self-dual witness bank is `data/positive_certificates.jsonl.gz`; no `status`
field is trusted. Basis isomorphisms transport every witness to its input tensor.
The verifier regenerates the signed cover first and then checks all 1,692 ledger
records. Results are `results/certificates.jsonl`, `summary.json`, `survivors.json`,
and `verification.json`. Model recognition verifies full tensors, not names.

The nine mutually exclusive recorded rejection stages leave respectively
1,317, 233, 231, 210, 101, 98, 88, 82, and 15 rings. These counts are regenerated
from the per-input ledger, not copied from the pivotal work. The final 15 models
comprise nine self-dual and six non-self-dual rings.

For non-self-dual inputs, the checker tests exact nonmembership in the seven
candidate tensors justified by the manuscript's automatic-sphericality and
Galois-pseudo-unitary reduction. The additional S(2) candidate is excluded by its
own proved moment obstruction. These are applications of independently stated
theorems; the checker does not formalize their categorical proofs.

## Internal signed-cover proof

```sh
python3 supplementary/classification/verify_compact.py
python3 supplementary/classification/verify_compact.py --engine python
```

Both commands regenerate the global cover. The second uses the Python local
search instead of C++; the global enumeration still requires C++17 and OpenMP.
The bound-31 cover has 92,795 signed orbits; universal arithmetic leaves 2,217,
with 1,182 positive orbits. The bank verifies 1,173 exclusions and nine models.
It deliberately has the broader multiplicity-only scope, not D < 1000.
The existing `generated_criteria.tex` is a detailed supplementary certificate-type
inventory; the main paper instead shows the ordinary-census successive-filter table.

`software/discovery.py` contains optional witness search, separate from replay.
`classify.py` regenerates the complete ledger from the supplied witness bank;
it does not claim to rediscover every algebraic witness from scratch.

## Conditional modes

`verify.py --ledger-only` checks all ledger witnesses but assumes the recorded
signed-cover completeness. `verify_compact.py --trust-cached-global` similarly
uses a cached full-cover report. Both print their assumption explicitly. Neither
is the default and neither is used by `supplementary/check.py`.

The tested dependency is SymPy 1.14.0; see `requirements.txt`. Optional
`python-flint` acceleration is retained but was not used in the delivered runs.
Machine fingerprints and source hashes are integrity checks, not categorical
exclusion criteria. Numerical approximations never decide an exclusion.
