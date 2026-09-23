# Reproduce the data

## Fast, offline checks

From this repository root:

```bash
python3 tools/validate_release.py
python3 tools/render_readme.py
git diff --exit-code README.md
```

These commands check every displayed cell, rank bound, exact-multiplicity
sequence, CSV/JSON agreement, and each classification partition. They do not
rerun the mathematical criteria or enumerate the fusion rings. Continuous
integration performs the same checks on every change.

## Rebuild from the pinned census

Check out the source commit and use its manifest:

```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

The exporter requires complete, verified whole-rank bands and verifies that
every count from 1 to the declared bound exists and sums to the published
cumulative total. Rank two follows its symbolic normal form, independent of
the repository enumeration.

## Rebuild classification partitions

Unpack the attached `FusionFrontier.tar.xz`. The rank-four ledger is the
`Rank4/.../certificates/classification.jsonl.gz` file. Rank-five and rank-six
ledgers live as `data/decisions.json` inside their respective release ZIPs.
Then run, substituting the actual extracted paths:

```bash
python3 tools/generate_classification.py \
  --bundle FusionFrontier.tar.xz \
  --census fusion-ring-census/results/census.json \
  --rank4 classification.jsonl.gz \
  --rank5 rank5-decisions.json \
  --rank6 rank6-decisions.json
```

The exporter records source checksums, checks cardinalities and agreement with every
census band. It assigns `unassessed` to entire bands absent from the ledgers.

The rank-five and rank-six source-tensor crosswalks can be rerun:

```bash
python3 tools/check_rank5_crosswalk.py census_independent.json \
  fusion-ring-census/results/rank5/tables.txt.gz \
  --report data/rank5_crosswalk.json
python3 tools/check_rank6_crosswalk.py rank6_through7_tables.txt.gz \
  fusion-ring-census/results/rank6/tables.txt.gz \
  --report data/rank6_crosswalk.json
```

The rank-five check tests exact based-ring isomorphism classes under every
unit-fixing permutation of basis; the rank-six check tests identical labeled
tensor lines in identical order. Their recorded reports alone cannot verify
certificate proofs. For the individual obstruction certificates, positive
models and theoretical coverage arguments, use the `verify.py` programs and
verification guides in the attached rank-specific research releases and the
revised manuscripts.

## Release discipline

When the source census advances, record its new commit and compare every
affected rank/multiplicity band before changing `data/`. If a classification
ledger does not yet cover a newly available census band, keep that band's
classification state as `census_only`; do not infer exclusions or count
unresolved rings from census data alone. Do not treat a search timeout as a
negative categorification result.
