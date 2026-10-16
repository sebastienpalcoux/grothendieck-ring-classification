# Publication identities and reproducible checks

The current mathematical record has 35 accepted decisions in its 38-case
continuation, with **R6_4_155, R6_8_1660 and R8_2_24 unresolved**.
The manuscript sources, PDFs and website copies are bound by
[`data/current_document_revision.json`](../../data/current_document_revision.json).

Treat the AI-generated results and data with caution. Independent human
verification and Lean formalization have not been completed.

From the repository root:

```sh
python3 tools/verify_current_publication.py --metadata-only
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The first command verifies the complete current document inventory, PDF
identities, available website copies, decision inventory and preserved replay
source identities. The other commands also run the exact proof-history chain
and the rank-six release's 779-file checksum manifest in isolated workspaces.
They require the full repository and the dependencies stated in
[`docs/VERIFY.md`](../../docs/VERIFY.md).

`replay_files.json` and `replay_files.zip` preserve byte-exact source material
from commit `c1165f6ec2b7ca890e7c5100eb3cda093a9fce70`. Both complete-file hashes
are pinned in `tools/current_publication.py`; every enclosed file also has an
individual size and SHA-256 check. Source recovery was checked against the
commit's Git blob identities or the original restoration manifest. The replay
dispatcher restores those files only into a temporary directory, leaving every
current manuscript in place. Existing proof manifests and their expected hashes
are unchanged. A calculation's successful replay certifies only its stated
computational scope; it does not certify an unproved categorical premise.

The current download includes all manuscripts and guides, their sources, proof
evidence, this replay packet and a complete archive manifest. Its standalone
metadata check is run after extraction before the download is registered for
publication. The archive uses fixed timestamps and sorted paths.

Completed verification receipts are available for [normal Python](verification/normal.json)
and [optimized Python](verification/optimized.json), together with the complete
[normal log](verification/normal.log), [optimized log](verification/optimized.log)
and [three mutation controls](verification/negative_controls.json). Both full-chain
runs passed, including the 779-file rank-six checksum check; all three deliberately
changed inputs were rejected. The final receipt in each log records the current
35 accepted decisions and three unresolved cases. Earlier receipt blocks are the
verbatim output of isolated replay stages. These checks establish publication
identities and the stated calculations, not independent human or Lean verification.
