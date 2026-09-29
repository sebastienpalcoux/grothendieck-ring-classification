# Proposed OEIS exports

These are local **draft data files**, not OEIS submissions or assigned
sequence numbers. A term counts the rank-`r` based fusion rings of **exact**
multiplicity `m` with at least one fusion-category realization over ℂ.

| Draft | Complete classification range | Terms |
|---|---:|---:|
| [Rank four realized](draft_rank4_realized.txt) | 1–128 | 128 |
| [Rank five realized](draft_rank5_realized.txt) | 1–20 | 20 |

Generate from the exact status partitions with
`python3 tools/export_oeis_drafts.py`. Every exported band has zero unresolved
and zero unassessed rings; rank-five multiplicities 18–20 are now included after general exclusion certificates closed the former residuals.
Rank-six general classification is complete at multiplicities **1–3** and,
separately, at **exact multiplicity 7**. Multiplicities 4–6 and 8 remain
partial. The isolated completed seventh band does not extend the contiguous
initial classification range and must not be used to fill its intervening
gaps. Rank seven and eight have unresolved cases even in their first analyzed
bands. The exporter currently emits only the rank-four and rank-five drafts
listed above; no rank-six, rank-seven or rank-eight sequence file is proposed
in this directory.
No zero beyond a proven finite
classification bound is inferred from the conjectured unrestricted
classification.

Before proposing any entry, search the live OEIS for duplicates and check
its indexing, references and submission rules. Link both the mathematical
manuscripts and their pinned census source. Publication and editorial
acceptance are separate from the calculations stored here.
