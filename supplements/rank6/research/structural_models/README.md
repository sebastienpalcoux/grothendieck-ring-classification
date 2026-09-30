# Three unitary conformal models

The categorical proofs are in the manuscript and the per-model proof notes.
Run `python -O software/conformal_models.py --verify` from the package root.
It reconstructs and compares all 216 fusion coefficients for each model.

The published B2 graph data are recorded with source PDF hashes. To repeat
the optional graph extraction, run `python research/structural_models/fetch_graph_source.py`,
then the two `extract` scripts; this requires internet access and PyMuPDF.
The ordinary arithmetic replay is offline and uses the frozen graph data.
