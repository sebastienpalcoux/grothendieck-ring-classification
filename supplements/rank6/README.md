# Rank-six categorification through multiplicity nine

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

**25,421 rings: 25,362 exclusions, 57 realizations and two open cases.**
Classification is complete through multiplicity three and at exact
multiplicities 5, 6, 7 and 9. Multiplicities 4 and 8 are partial.

[Current manuscript](../../manuscripts/rank6/papers/manuscript.pdf) ·
[Verification guide](../../manuscripts/rank6/papers/verification_guide.pdf) ·
[Decision ledger](data/decisions.json) · [Models](data/model_catalog.csv)

| Exact multiplicity | Rings | General exclusions | Models | Open |
|---:|---:|---:|---:|---:|
| 1 | 39 | 18 | 21 | 0 |
| 2 | 154 | 132 | 22 | 0 |
| 3 | 384 | 381 | 3 | 0 |
| 4 | 872 | 866 | 5 | 1 |
| 5 | 1,582 | 1,581 | 1 | 0 |
| 6 | 2,768 | 2,765 | 3 | 0 |
| 7 | 3,814 | 3,812 | 2 | 0 |
| 8 | 6,999 | 6,998 | 0 | 1 |
| 9 | 8,809 | 8,809 | 0 | 0 |
| **Total** | **25,421** | **25,362** | **57** | **2** |

The models comprise 56 unitary realizations and one spherical realization
whose ring has no pseudo-unitary categorification. General exclusions apply
to complex fusion categories without an initial pivotality or unitarity
assumption. A model proves existence of at least one categorification; it
does not assert that all categorifications of that ring are unitary.

## Open cases

- `R6_4_155`: A unique rank-26 semion-centralizer modular candidate satisfies
  the recorded finite Verlinde, Vafa and indicator checks. A rank-22 based
  module passes 234,256 fermion Azumaya linking identities. Odd cyclic Clifford
  constraints pass on all 1,144 tested blocks. The all-order path-Clifford
  divisibility condition for the family R′(m) holds exactly when m is even,
  including m=4. These necessary data supply neither a coherent module
  category nor associators for a categorification.
- `R6_8_1660`: A unique relative-center based ring, three possible Morita-dual
  rings and a bounded domain of restriction profiles remain. In the positive
  spherical representative, saturated modular representations determine all
  indicator sequences and central phase masses. Eight spin objects form four
  dual pairs, all restricting to `2X+2gX+σ+3T`. Exact phase Gram constraints
  leave **640 labelled restriction-data profiles**, in branches **68, 286, 286**.
  A rank-37 candidate fails an exact Verlinde integrality test. This does not
  exclude every possible profile.

The [current research status](../../docs/RESEARCH_STATUS.md) states the complete
two-case frontier, both at rank six. The [necessary-condition package](../../evidence/rigidity_20261017/rank6/README.md)
gives the Clifford, indicator and phase-mass proofs and exact replays. The model
catalogue includes all tensor identifications for the three conformal-embedding
constructions.

## Complete verification

From the repository root, restore the checksummed data, install the rank-six
requirements and choose a new output directory:

```bash
python3 tools/restore_data.py
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/correctness_20261025/replay_rank6.py \
  --output-dir /tmp/rank6-current-complete --jobs 2
```

The [current correction guide](../../evidence/correctness_20261025/README.md)
records all 25,362 original raw exclusion verdicts, seven complete
reference-backend worker retries, the eleven immutable-source multiplicity-nine
completion proofs and the exact original post-loop checks. Historical source
hash checks are preserved; the current tensors and certificates are matched
exactly. This combined campaign is distinct from a single successful full run.
The earlier audit's partly log-derived coverage and initial failures remain
preserved in the original audit archive.

Positive model arguments have their separate proof and tensor checks. The
[repository verification guide](../../docs/VERIFY.md) explains each route and
its scope. A timeout proves no exclusion; checking saved receipts does not
re-execute the mathematics.

## Source identity

The census is pinned to [revision 2a340871242879665fa7ba2b01fa15b8bdeaada3](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3).
Its completeness comes from the census source; the import separately checks
tensor validity, distinctness and exact correspondence. `data/decisions.json`
is the authoritative classification ledger. The
[current document manifest](../../data/current_document_revision.json) binds
the current manuscripts, supplement copies and website PDFs. Source-bound
replay programs run with the compatible snapshots specified by the aggregate
wrapper. The [provenance guide](../../docs/PROVENANCE.md) gives all ledger hashes.
