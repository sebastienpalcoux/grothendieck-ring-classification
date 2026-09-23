# Proposed OEIS exports

These are local **draft data files**, not OEIS submissions or assigned
sequence numbers. A term counts the rank-`r` based fusion rings of **exact**
multiplicity `m` with at least one fusion-category realization over ℂ.

| Draft | Complete classification range | Terms |
|---|---:|---:|
| [Rank four realized](draft_rank4_realized.txt) | 1–128 | 128 |
| [Rank five realized](draft_rank5_realized.txt) | 1–17 | 17 |

Generate from the exact status partitions with
`python3 tools/export_oeis_drafts.py`. Every exported band has zero unresolved
and zero unassessed rings; rank-five multiplicity 18 is deliberately omitted.
Rank-six general classification is complete only at multiplicities 1–2, so
there is no proposed sequence file yet. No zero beyond a proven finite
classification bound is inferred from the conjectured unrestricted
classification.

Before proposing any entry, search the live OEIS for duplicates and check
its indexing, references and submission rules. Link both the mathematical
manuscripts and their pinned census source. Publication and editorial
acceptance are separate from the calculations stored here.
