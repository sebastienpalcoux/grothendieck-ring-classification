# Research announcement for Hexagon

**Low-rank Grothendieck rings: an AI-assisted classification project, constructions, and open problems**

A five-page overview of the classification scope, seven construction candidates for novelty review, and two unresolved rank-six categorification problems.

**AI-generated research · independent verification pending.** The announcement distinguishes reported mathematical results, exact finite checks, and open problems. Independent verification and Lean formalization remain pending.

- [Read the five-page announcement](Low_rank_Grothendieck_rings_announcement.pdf)
- [Download the TeX source ZIP for Hexagon](Hexagon_Source.zip)
- [Submission text and provenance](submission_metadata.txt)
- [Pinned snapshot and file checksums](snapshot_manifest.json)

## Submit to Hexagon

1. Open https://hexagonmath.org/submit and authenticate with your ORCID account.
2. Use the title and abstract in `submission_metadata.txt`.
3. Upload `Hexagon_Source.zip`. It contains only `main.tex`, including the bibliography. Code and data remain in the linked GitHub repositories.
4. Inspect Hexagon's compiled PDF and confirm that all five pages, formulas, references, and links are present.
5. Select the license and the truthful human-understanding / AI-provenance options in the live form. Review any required attestations personally.
6. Submit after reviewing the complete preview. Once a public identifier exists, add it to this directory and the repository's main README.

This is a submission-ready package, not a claim of publication or acceptance by Hexagon. The public deposit will have its own permanent identifier only after submission.

## Rebuild

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with a standard TeX Live installation. No shell escape, external images, bibliography processor, or custom class is required.

## Snapshot

The announcement cites fixed classification commit `e34396cd95aff1090c10974dd934fe6054ca45eb` and census commit `d4c36cc2ee5eb5f0e5291de18d2bb433ffb7ce8b`. Its 14 research manuscripts / 485 pages count describes that snapshot and excludes this announcement.

[Classification repository](https://github.com/sebastienpalcoux/grothendieck-ring-classification) · [Fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census) · [Interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
