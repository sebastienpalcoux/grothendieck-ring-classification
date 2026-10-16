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
  module passes 234,256 fermion Azumaya linking identities. Neither supplies
  a coherent module category or associators for a categorification.
- `R6_8_1660`: A unique relative-center based ring, three possible Morita-dual
  rings and a bounded domain of center profiles remain. Graded induction
  reduces the profile domain to 1,136. Saturated traces force `nu_3(T)=2`.
  A rank-37 candidate fails an exact Verlinde integrality test. This does not
  exclude every possible profile.

The [current research status](../../docs/RESEARCH_STATUS.md) states the complete
three-case frontier across ranks six to eight. The model catalogue includes
all tensor identifications for the three conformal-embedding constructions.

## Complete verification

Use the [combined replay guide](../../evidence/prepublication_20261017/rank6_backend/README.md)
from a fresh restored checkout. The executed campaign covers all 25,362
exclusion certificates by 25,355 initial passes plus seven complete
Python-backend retries, with the two post-loop checks executed separately.
The initial full process failed and its failed status is retained. This was
not a successful single full run or an all-Python full-census pass.

The portable complete-replay orchestrator has not itself been executed end
to end; its identity, coverage and rejection controls were tested. From the
repository root, in an isolated environment and without native binaries cached
beside the rank-six C++ sources:

```bash
python3 tools/restore_data.py
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \
  --repo . --output-dir NEW_DIR --jobs 2
```

Choose a new output directory outside `supplements/rank6`. The
[repository verification guide](../../docs/VERIFY.md) supplies the individual
model, multiplicity-nine completion and frontier commands and explains their
scope. A receipt audit checks source identities and predicates; it does not
rerun the mathematics. A timeout proves no exclusion. Normal Python is
required when proof checks use `assert`.

## Source identity

The census is pinned to [revision 2a340871242879665fa7ba2b01fa15b8bdeaada3](https://github.com/sebastienpalcoux/fusion-ring-census/tree/2a340871242879665fa7ba2b01fa15b8bdeaada3).
Its completeness comes from the census source; the import separately checks
tensor validity, distinctness and exact correspondence. `data/decisions.json`
is the authoritative classification ledger. The
[current document manifest](../../data/current_document_revision.json) binds
the current manuscripts, supplement copies and website PDFs. Source-bound
replay programs run with the compatible snapshots specified by the aggregate
wrapper. The [provenance guide](../../docs/PROVENANCE.md) gives all ledger hashes.
