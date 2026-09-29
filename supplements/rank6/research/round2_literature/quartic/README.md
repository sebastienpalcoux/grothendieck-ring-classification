# Quartic ambient-field continuation

The release theorem is `papers/chapters/cyclotomic_stabilizer.tex`; the tensor-only engine is `software/cyclotomic_stabilizer_trace.py`. The general certificate kind is `general_cyclotomic_stabilizer_trace` and its checker is `verify_general(R, certificate)`. Its pseudo-unitary component has kind `cyclotomic_stabilizer_trace`.

The engine reconstructs the complete involution-module domain, the exact positive dimension-field embedding, low induction frames, native bounded Gram vectors, dimension-quotient integrality, central d-number divisibility, finite joint relative trace vectors, and second-indicator cases. Checking only uses exact arithmetic and does not call the optimizer. A finite integer-range guard precedes the native Gram enumerator.

The four release certificates are stored as `certificates/cyclotomic_stabilizer_<ID>.json` for R6_4_258, R6_4_325, R6_8_570 and R6_8_2203. The copies one directory above this file ending `_general.json` are for campaign discovery. Their local exact rays number 12, 8, 7 and 28 respectively. The general components also verify the sphericalization and Galois pseudo-unitary reductions.

The exploratory files `cyclotomic_trace.py`, `modular_cyclotomic_trace.py` and `fourth_modular_probe.py` are discovery programs, not release verifiers. In particular, the first prototype reads a prior stabilizer-pattern file; the canonical engine instead recomputes all branches directly from the tensor. No conclusion depends on that lookup.

The height-four modular probes for R6_4_22 and R6_4_91 remain feasible on both surviving low-character labellings; see `fourth_modular_probe.json`. These are necessary relaxations only. They neither prove categorifiability nor supply a fusion category. Their global Galois multiplicity equations do not assume that Galois squares fix relative trace types in a quartic field.

Exact replays and mutation controls for the release checker are recorded in `optimized_replay.json` and the independent audit reports in `research/round2_center/`. An additional optimizer-disabled optimized-Python replay for R6_8_570 is recorded in `optimized_R6_8_570_replay.json`; independent multiplicity-eight replays are recorded by the center audit in `research/round2_center/`.
