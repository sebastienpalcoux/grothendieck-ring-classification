# Grothendieck rings of complex fusion categories: rank 5

Publication edition: **24 November 2026**. The 72-page manuscript joins the uniform rank-two, rank-three and rank-four series. Its bibliography contains 51 references. AI assisted with the research and preparation; complete human verification remains pending.

## Current manuscript and supporting files

| Material | Link |
|---|---|
| Reading copy | [rank5.pdf](../rank5.pdf) |
| Complete manuscript source | [rank5.tex](../rank5.tex) |
| New publication revision letter | [PDF](../hexagon/rank5-publication-letter.pdf) · [TeX](../hexagon/rank5-publication-letter.tex) |
| Hexagon submission source | [One-file ZIP](../hexagon/hexagon-rank-5-source.zip), containing `main.tex` |
| Portable manuscript and verification package | [ZIP](../hexagon/rank5-publication-package.zip) |
| Exact verification and prior review history | [Supplement](../../supplements/rank5/sharp/README.md) |
| Exact manuscript changes | [Patch](../../supplements/rank5/sharp/publication_revision.patch) · [change index](../../supplements/rank5/sharp/publication_changes.txt) |
| File identities | [JSON](../hexagon/rank5-source-identities.json) |

The paper proves that every complex fusion category of rank five has a pseudo-unitary Galois conjugate and admits a spherical structure. It gives the sharp bounds

\[
\mu\leq 4,\qquad \operatorname{FPdim}\leq 48+24\sqrt{3},
\]

and classifies seventeen Grothendieck rings, each admitting a unitary realization. This classifies the possible based rings; it does not identify all tensor-equivalence classes of their categorifications. The introductory model-source discussion gives conventions and construction references for each model family.

## Reproduce the finite checks

From the repository root, with Python 3.12 and a C++17 `g++` compiler with OpenMP support:

```bash
python3 -m pip install -r supplements/rank5/sharp/requirements.txt
python3 supplements/rank5/sharp/verify.py
```

The pinned Python dependencies are SymPy 1.14.0 and NumPy 2.3.5. Run with assertions enabled. The verifier runs eighteen structural arithmetic checks, regenerates 269 based rings at multiplicity at most four, retains 114 under the exact dimension bound, and checks 97 exclusions and seventeen model identifications. The categorical arguments and the justification of the finite bounds are in the manuscript. Successful computational replay is not a claim of formal certification.

The [supplement README](../../supplements/rank5/sharp/README.md) describes the two verification stages and optional audit probes. The manuscript links to the immutable [fourth-review verification snapshot](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/b479c65c702c6a09a674df7c2f8468b1a48915d3/supplements/rank5/sharp). The publication edition retains the programs, certificate data, model tensors and recorded audit outputs from that snapshot unchanged.

## Earlier bounded census

The earlier [19-page manuscript](papers/manuscript.pdf) and [four-page verification guide](papers/verification_guide.pdf) concern the census through multiplicity twenty. They remain available as historical supporting material with their original file identities. The current unrestricted theorem and sharp finite replay above supersede their role as the main rank-five publication.

## Submission status

The source archive is prepared for Hexagon. This rank-five edition has **not been submitted** by this publication update. The [series submission page](../hexagon/README.md) records the three earlier manuscripts and the prepared rank-five files.
