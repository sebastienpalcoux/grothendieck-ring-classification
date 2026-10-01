# Signed trace saturation: 7741 and 7742

These two rings have no complex fusion categorification. The proof uses the
formal-codegree trace ideal to bound the signed Casimir deficit, the diagonal
associativity triangle inequality to force every magnitude to be maximal,
and saturation to normalize every repeated-index coefficient positively.
Only 1,024 assignments to distinct-index signs remain; exactly the original
positive tensor is associative. A spherical section would therefore exist,
contradicting the retained exact spherical obstruction.

Run from any directory:

```sh
python -O verify.py --source-root /path/to/Rank6_Categorification_M9
```

Within the canonical package, the source root is found among the verifier's
ancestors. Python, SymPy, and the package's standard dependencies are required.
No discovery optimizer is invoked. All correctness checks remain active with
Python optimization. `tensors.json` contains the full frozen canonical inputs,
bound to independent fingerprints in the verifier. `spherical_certificates.json`
contains only the two necessary inherited proof trees. The verifier regenerates
all bounded magnitudes and signs directly and replays both proof trees.

For 7741 the trace bound is 6,705, the Casimir trace is 6,813, and 389 magnitude
profiles are tested; for 7742 the corresponding numbers are 6,705, 6,805, and 241.
Every profile except the original magnitudes violates a diagonal triangle
inequality. The complete mathematical justification appears in the manuscript's
multiplicity-nine completion section.
