# Revision audit — 23 September 2026

This revision uses the newer rank-six multiplicity-eight release and its pinned
`fusion-ring-census` input, rather than the earlier through-seven publication
bundle. The frozen ledger has 16,612 rings: 16,511 generally excluded,
54 realized (53 unitary and one spherical without a pseudo-unitary
categorification), and 47 unresolved. General categorifiability is completely
classified through multiplicity two only. At multiplicity eight, 6,980 of
6,999 rings have general exclusion certificates and 19 remain unresolved.

The rank-four citation is the authorless *Rank-four Grothendieck rings
through multiplicity 128*. The imported theorem is applied only to rank-four
subrings of multiplicity at most eight in this release. The rank-five citation
is the authorless *Rank-five Grothendieck rings through multiplicity twenty*;
its complete general theorem includes the two resolved multiplicity-eighteen
cases. The cited
Alekseyev–Bruns–Dong–Palcoux paper is marked accepted in *Letters in
Mathematical Physics*. PDF author metadata is empty, no affiliation or
acknowledgment is present, and the AI assistance statement precedes the
references.

The ordered table is the actual executed sieve. It puts inexpensive tests
ahead of finite induction searches and reports incremental exclusions.
Dimension-order and character-induction stages first add a new *top-level*
exclusion at multiplicity eight (one and four rings respectively). These
mechanisms may have been used in nested proof trees earlier; neither a
globally fastest order nor criterion stability beyond eight is asserted.
The companion proof-family table is ordered to correspond to sieve stages;
its retained-certificate counts need not equal a stage's incremental count.

New checks in this revision: `software/build_paper_tables.py` and
`software/release_consistency.py` pass; the latter confirms all 16,612 ledger
rows, 54 model rows, and 47 residual rows. All 144 stored lower-rank-subring
certificates reverify with the updated rank-four theorem bound. Both PDFs
compile without unresolved references or overfull boxes; modified cover,
tables, disclosure and bibliography, plus the modified verification-guide
pages, were rendered and visually checked. The source release includes
records for exact checks of all 16,511 negative certificates. This revision
reran all 26 regression processes in normal and optimized Python modes after
selecting the same SymPy polynomial backend used for certificate generation.
It did not repeat the full 16,511-certificate sweep.
The old `verification/package_check.json` records the original package check;
the current integrity check is `python check_manifest.py` against this
revised package's `SHA256SUMS`.
# Cross-paper update (rank-five complete-through-twenty theorem)

The rank-five paper now proves general classification through multiplicity
twenty, including the two former multiplicity-eighteen residuals. The
rank-six bibliography, lower-rank descent corollary and matching verifier
bound cite the revised title and theorem. This rank-six ledger stops at
multiplicity eight, so its 16,612 status rows and original certificate
allocation are unchanged. Both paper PDFs were rebuilt.

