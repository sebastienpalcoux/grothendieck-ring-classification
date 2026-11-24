# Grothendieck rings of complex fusion categories: rank 5

Publication edition: 24 November 2026. The canonical [PDF](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/manuscripts/rank5.pdf) and [TeX](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/manuscripts/rank5.tex) are also included here as `rank5.pdf` and `rank5.tex`. See the [reading guide](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/manuscripts/rank5/README.md) and [project website](https://sebastienpalcoux.github.io/grothendieck-ring-classification/). AI assisted with the research and preparation; complete human verification remains pending.

The [frozen verification snapshot](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/b479c65c702c6a09a674df7c2f8468b1a48915d3/supplements/rank5/sharp) preserves the fourth-review programs, certificates, model tensors and transcripts. This publication revision changes the title, references, explanatory text and repository links; it retains those computational files byte-for-byte.

Theorem A proves that every complex fusion category of rank five has a pseudo-unitary Galois conjugate and therefore admits a spherical structure. The sharp bounds are fusion multiplicity at most four and global Frobenius–Perron dimension at most 48 + 24√3. Theorem B classifies the seventeen resulting based rings; each has a unitary realization.

The proof has three stages: Galois descent, bounds on the fusion rules, and a finite classification within those bounds. The dimension arguments use the published integral classification and near-group results, together with the structural and arithmetic arguments proved in the manuscript. The computational checks verify finite calculations and certificates. The categorical implications and the justification of the finite search ranges are given in the paper.

## Contents

- `rank5.tex`: the complete manuscript source, including the bibliography, in one file.
- `rank5.pdf`: the current revised manuscript (72 pages, with 51 bibliography entries).
- `Publication_Revision_Letter.pdf` and `Publication_Revision_Letter.tex`: the new publication revision letter, recording the title, reference, model-attribution and GitHub updates.
- `publication_revision.patch`: the exact manuscript-source changes relative to the fourth reviewed version.
- `publication_changes.txt`: the 28 editorial change locations and 22 added bibliography keys.
- `Revision_Letter_Round4.pdf` and `Revision_Letter_Round4.tex`: the detailed fourth audit and revision letter, preserved unchanged.
- `Revision_Letter_Round3.pdf` and `Revision_Letter_Round3.tex`: the third revision letter, preserved unchanged as a historical record.
- `Revision_Letter_Round2.pdf` and `Revision_Letter_Round2.tex`: the second revision letter, preserved unchanged as a historical record.
- `Revision_Letter.pdf` and `Revision_Letter.tex`: the preceding seven-page revision letter, preserved unchanged.
- `Review_Report.pdf` and `Review_Report.tex`: the previous seven-page review, preserved unchanged as a historical document.
- `verify.py` and `checks/`: eighteen exact arithmetic programs for descent and the structural bounds.
- `final_census/`: the bounded ring generator, the 114 witness records, exact exclusion criteria, and the seventeen model tensors.
- `verification.txt`: the complete successful verification run after the fourth-review code changes.
- `final_census/verify_independent_census.py`: the optional additional census and Pieri-model audit.
- `final_census/verify_additional_audits.py`: optional checks of certificate input, the quadratic and sharp-dimension cutoffs, direct cyclotomic averages, Gram columns, and generator-range coverage.
- `independent_verification.txt`: the preceding audit and assertion-mode rejection results, preserved unchanged.
- `audits_round4/`: three additional optional probes of positive models, an explicit dihedral center, and native linear completion.
- `additional_verification_round4.txt`: actual output of both established optional audits and the three new probes in the fourth review.
- `additional_verification_round3.txt`: the preceding optional-audit transcript, preserved unchanged.
- `additional_verification_round2.txt`: the preceding optional-audit transcript, preserved unchanged.
- `revision_round4.patch`: exact edits to existing text files relative to the third revised package; new files are listed in the fourth revision letter.
- `revision_round3.patch`: the third revision's patch, preserved unchanged.
- `revision_round2.patch`: the second revision's patch, preserved unchanged.
- `revision.patch`: the preceding revision's patch, preserved unchanged.
- `SHA256SUMS.txt`: checksums of the final distributed files.

## Reproducing the computations

The complete run was checked with Python 3.12, SymPy 1.14.0 and NumPy 2.3.5. Use Python 3.12 with SymPy and NumPy, and a C++17 `g++` compiler with OpenMP support. Run the following commands from this directory:

```bash
python3 verify.py --bounds-only
python3 verify.py --classification-only
```

The first command runs the eighteen programs listed in `BOUNDS` in `verify.py`. Their finite ranges come from the inequalities in the paper. This stage does not read the `final_census` directory.

The second command regenerates all 269 based rings of multiplicity at most four, applies the exact dimension bound, and verifies a decision for each of the 114 remaining rings: 97 exclusions and seventeen model identifications. The stronger conclusion of Theorem A allows all exclusions to use necessary conditions for a pseudo-unitary realization. See `final_census/README.md` for the detailed counts and certificate sources.

To run both stages in sequence:

```bash
python3 verify.py
```

Run Python with assertions enabled, without `-O`. The main entry points and all assertion-dependent standalone structural scripts now reject optimized Python explicitly. The first stage finishes with `All 18 structural checks passed.` The classification stage finishes by confirming all 97 exclusions and all seventeen based-ring model identifications. A successful model comparison verifies the fusion tensor and its basis permutation; the cited categorical constructions establish existence and unitarity.

All acceptance and exclusion decisions use exact integer, rational, or algebraic-number arithmetic. Replaying the stored separating forms does not require a numerical linear-programming solver or network access. Compiled helpers are placed in temporary directories.

## Additional census and model audit

To reconstruct the symmetry and associativity equations, check every linear-completion equation, compare the optimized census with a replay that bypasses its nonlinear shortcuts, and independently reconstruct the `Ad(SU(3)_4)` model from its Pieri graph, run:

```bash
python3 final_census/verify_independent_census.py
```

This optional check reproduces 220 self-dual rings, 47 rings with one nontrivial dual pair, and two with two dual pairs. The slower replay shares the existing fraction-free linear-completion routine and basis parametrization; it is an additional check, not a wholly independent implementation or a formal proof. The main verifier does not need this optional run.

For the targeted arithmetic and certificate checks, run:

```bash
python3 final_census/verify_additional_audits.py
```

This rejects the malformed subring certificate that previously falsely excluded the realized `Rep(D14)` ring, verifies the corrected lower bound `5/18` in the final subcase of Proposition 6.3, and independently checks the sharp-dimension cutoff by exact root isolation on all 269 generated rings, including the three at equality. It also computes 864 relative-trace moments directly in cyclotomic quotient rings, checks all 14 induction/indicator certificate rings and 11 residual Gram matrices by direct enumeration, and derives complete rational interval ranges for the three quartic generator searches. Every reported Perron upper endpoint is certified. The trace vectors, column lists, and range coverage agree with the existing programs.

These targeted checks share the ring generators, defining field data, certified root intervals, and construction of individual restriction columns. They check the dimension comparison, joins, and range construction separately; they do not prove the categorical hypotheses. Both optional commands leave the stored witnesses and model tensors unchanged. Their current output is in `additional_verification_round4.txt`.

The structural check `checks/verify_exchange.py`, included in the ordinary run, now uses all 600 second/third-indicator tuples in the final conductor-five case. Its third-indicator coordinates are real parts of cubic rotation traces and include half-integers. The same six separating forms exclude every tuple; no reality assumption on the indicators is used.

## Fourth-review audit probes

Three additional programs preserve the new checks made during the fourth review:

```bash
python3 audits_round4/positive_models.py
python3 audits_round4/dihedral_center.py
python3 audits_round4/linear_completion.py
```

The first checks the d-number, central-dimension norm and field, global-moment, and induction criteria on all seventeen positive model tensors. It also checks subcategory dimension divisibility on their twenty-seven proper nontrivial fusion subrings. The second constructs an explicit feasible system from the center of `Rep(D14)`, with five unit-induction and twenty-three further simple objects, and checks the Gram and moment equalities and thirty-two higher-indicator inequalities through order six.

The third runs both optimized generators at multiplicity four with C++ undefined-behavior sanitization, then compares native augmented-matrix elimination with independent exact rational row reduction on 659 inputs: all 269 generated parameter records and 390 fixed-seed boundary/random inputs. This comparison checks the sampled elimination steps; it does not independently enumerate every rejected parameter choice or prove the native algorithm formally. It shares the generator's matrix construction. The positive-model and dihedral checks share the package's model tensors or criterion implementation, so they test consistency and concrete feasible cases rather than replacing the categorical proofs.

All three programs require Python assertions to be enabled and locate package files relative to their own paths. The native probe additionally requires a `g++` installation with the undefined-behavior sanitizer. Its compiled programs are temporary. These probes are optional and are not called by the ordinary verifier. Their outputs are included in `additional_verification_round4.txt`.

## Rebuilding the manuscript

The distributed `rank5.tex` is self-contained apart from standard LaTeX packages. Run:

```bash
pdflatex rank5.tex
pdflatex rank5.tex
pdflatex rank5.tex
```

These commands produce `rank5.pdf` and stabilize the table of contents, theorem references, and citations. No separate bibliography file or BibTeX run is needed. Build `Publication_Revision_Letter.tex` in the same way to reproduce the current publication letter. The earlier letters and report sources remain available under their original names.
