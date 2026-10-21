# Rep(PSL(2,11)) and structural certificates

`verify_psl2_11.py` constructs all determinant-one matrices over F11,
quotients by ±I, enumerates all conjugacy classes, and counts every
class-sum product. It then checks an explicit exact character table
against that independently computed class algebra: every normalized
central character is a unital algebra homomorphism, all character inner
products are orthonormal, and the positive degrees square-sum to 660.

These tests certify actual group characters rather than just an
orthogonal numerical table. The center of C[G] is a product of copies
of C, one for each irreducible representation. Each verified unital
central character therefore equals that of a genuine irreducible;
orthogonality fixes its positive degree and the eight distinct rows
exhaust the eight conjugacy classes. Taking exact character inner
products constructs all fusion coefficients.

The result matches all 512 coefficients of R8_3_724. The fresh recovered
model basis has degrees `[1,5,5,10,10,11,12,12]`; the model-to-source map
is `[0,1,2,6,7,3,4,5]`. The source-to-model inverse is explicitly stored
in `certificate.json`. This is a unitary finite-group representation
category. Source SHA256 is recomputed and pinned by the verifier.

After the workspace reset, this verifier and its certificate were
independently reconstructed and recomputed; they do not pretend to be
byte-identical to the unavailable previous group enumeration output.
Replay with

    python -O evidence/rank8_m3_20261021/models/psl2_11/verify_psl2_11.py

Other independently replayable results in this directory:

* `r360/`: the stable-relative-cocycle twisted A6/A5 model for R8_3_3342;
* `r275/`: dimension-80 ring rigidity, excluding four source tensors;
* `r216/`: the general dimension-216 obstruction, excluding six tensors;
* `r280/`: the split-module polynomial obstruction for two tensors;
* `f4_level3_attempt.py`: one exact failed quantum-group Morita-source
  attempt, explicitly not a general categorical exclusion.

The structural theorem manuscript fragment is `structural_m3.tex`.
