# Rank-four revision record (23 September 2026)

## Scope

Three deliverables were revised: the bounded finite manuscript, unrestricted companion, and exact verification guide. The numbered results used by the rank-five and rank-six manuscripts were preserved: finite Theorem 1.1; Proposition 2.1 and its item (5); Lemmas 2.2–2.4; Theorem 3.1; Propositions 3.2–3.3 and 5.1; Lemma 7.1; Corollary 7.2; Sections 2, 3, 6, 7; and Appendix B. The exact finite-paper title is *Rank-four Grothendieck rings through multiplicity 128*. In the companion bibliography it is cited without a manuscript author list.

## Changes

1. Removed author input, affiliations, title-page author metadata, date, and the acknowledgment. Each manuscript now has the short disclosure, “GPT-6 Astra assisted with research, computation, and manuscript preparation,” immediately before References. The support guide has the same disclosure at its end. External literature keeps its real author attributions.
2. Replaced the duplicate independent-census appendix with an appendix on tensor reconstruction, retaining the ten-parameter and six-parameter matrices, associativity equations, and the Diophantine identity needed by signed certificates. The pinned [`fusion-ring-census`](https://github.com/sebastienpalcoux/fusion-ring-census) source at commit `7f1b36e74df53a8a1cf8597db45d261e408d61b2` supplies exhaustive input and counts through multiplicity 128. Historical labels continue to use the stored explicit mappings. The optional duplicate unsigned census programs and workflow were removed from this release. The remaining local tensor audit checks the pinned records, without claiming to rederive census completeness.
3. Generated the exclusion table in the actual dispatch sequence and added the first exact multiplicity for each disjoint top-level certificate type. The 12 exclusion rows total 889,515; the fifteen models complete the 889,530-ring input. The largest first use among grouped mathematical criterion families is 18, so the current allocation applies no new family from multiplicity 19 to 128. Later first appearances of nested implementations, such as signed cyclotomicity at 95, reuse established criteria. The table is explicitly labeled an archived allocation: no new full run is implied.
4. Removed the sole one-tensor recognition shortcut for the residual-involution case. Both generation paths now identify it from a general, fully enumerated low-induction certificate on a weakly integral input; its checker reconstructs and checks the general obstruction for every low branch. The historical certificate-kind string is retained to read existing records. The one-ring corollary stays as an illustration of the general proposition, without being a special-case proof rule.
5. Removed unneeded OEIS/Vercleyen references from the finite bibliography after moving census provenance to the current repository. Cross-paper citation numbers and labels remain stable.

## Verification and limits

- Pinned `results/rank4/counts.csv` at the stated commit has 128 terms summing to 889,530. The local compressed parameter file matches its manifest digest.
- `render_report.py` regenerates the table from the archived certificate summary and first-use statistics; the displayed disjoint counts sum to 889,515.
- `test_applications.py` passed 24 permutation checks and rejected eight deliberately corrupted witnesses, including the residual-involution certificate. The revised dispatcher returned the same certificate kind for `F_{5,33}` and the previous `weak_integral` type for `F_{2,3}`.
- `build_pdfs.py` compiled all three PDFs in three passes with no unresolved references or overfull boxes: finite 28 pages; companion 25 pages; guide 7 pages. Their PDF Author metadata is empty. Source and rendered PDF both place the disclosure before References.
- The archived full certificate stream is 75,825,461 bytes with SHA-256 `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`. It is omitted here to keep the revision compact. Restore it from the original attachment before full replay, as described in README. A full post-revision replay was not run because `python-flint` is unavailable in this environment; the previous archived full-run summary is retained as the source of the displayed allocation.

No statement in this revision proves that the criterion suite is minimal or classifies categorifiability beyond multiplicity 128. The companion isolates the remaining unrestricted cases.
