# Proposed OEIS exports

The rank-eight multiplicity-three continuation addresses all 3,527 supplied exact-multiplicity-three rings: 3,504 general exclusions, 14 models and 9 unresolved cases. Every recorded model admits a unitary realization. The remaining rings retain unresolved status for general complex categorification.

The rank-seven multiplicity-five continuation addresses all 5,805 supplied exact-multiplicity-five rings: 5,804 general exclusions, 1 realization and 0 unresolved cases. The classification of the supplied census is complete through multiplicity 5. The new realization R7_5_5678 is Rep(AGL(1,7)).

These are local **draft data files**, not OEIS submissions or assigned
sequence numbers. A term counts the rank-`r` based fusion rings of **exact**
multiplicity `m` with at least one fusion-category realization over ℂ.

| Draft | Complete classification range | Terms |
|---|---:|---:|
| [Rank four realized](draft_rank4_realized.txt) | Unrestricted; file displays 1–128 | 128 |
| [Rank five realized](draft_rank5_realized.txt) | 1–20 | 20 |

Generate from the exact status partitions with
`python3 tools/export_oeis_drafts.py`. Every exported band has zero unresolved
and zero unassessed rings; rank-five multiplicities 18–20 are included with general exclusion certificates.
Rank-six general classification is complete at exact multiplicities
**1, 2, 3, 5, 6, 7, 9**, contiguously through **3**. Two rings remain unresolved through 9.
The rank-six census value a(9)=8809 counts all based rings regardless of
categorifiability. The exporter proposes only the rank-four and rank-five
drafts above; no incomplete band is an exact sequence term.
The unrestricted rank-four theorem gives the sequence
**9, 3, 2, 0, 0, 1, 0, 0, …**, with every term after multiplicity six zero.
Its file retains 128 explicit terms to match the separate census export.
Rank five remains a classification through multiplicity twenty; no assertion
about higher multiplicities is inferred from its finite data.

Before proposing any entry, search the live OEIS for duplicates and check
its indexing, references and submission rules. Link both the mathematical
manuscripts and their pinned census source. Publication and editorial
acceptance are separate from the calculations stored here.
