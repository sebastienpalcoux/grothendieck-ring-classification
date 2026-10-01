# Exact Gauss and higher-dimension-field certificates

This portable bundle needs Python 3.10 or later and SymPy. It was checked with Python 3.12 and SymPy 1.14.0. It does not import the classification package, query a changing unresolved list, download anything, or invoke an optimizer or compiler.

Run from any working directory:

```sh
python /path/to/bundle/verify_bundle.py
python -O /path/to/bundle/verify_bundle.py --negative-controls
```

Every verification check uses an explicit exception and remains active with `-O`. The verifier reads the frozen full tensors in `tensors.json`, checks the independent hashes in `tensor_sha256.json`, and reconstructs every certificate in `certificates.json`.

The three outputs have deliberately different scopes:

| Input | Certified conclusion |
|---|---|
| R6_9_8200 | No complex fusion category has this Grothendieck ring. |
| R6_9_7018 | Any categorification forces signed dimension-character field Q(sqrt(5)); degrees four and six are excluded. |
| R6_9_8785 | Any categorification forces signed dimension-character field Q(sqrt(5)); degrees four and six are excluded. |

The higher-field result is one component of the separate general exclusion of 7018. It is not by itself a noncategorifiability certificate for 7018 or 8785.

`gauss8200_proof.tex` proves the even-codegree isolation, parity and saturation reduction. `gauss_family_method.tex` supplies the general Gauss-family proof. `gauss_family.py` reconstructs the all-orders pseudo-unitary Gauss obstruction, including every low and high column. `higher_fields_proof.tex` proves the complete conductor bounds and the different-ideal and quartic-spectrum arguments. `common.py` contains only the small exact arithmetic routines needed by these files.

For integration, both `exclusion8200` and `higher_fields` expose `certificate(R)` and `verify(R, certificate)`, where `R` is a full integer multiplication tensor. The mathematics is checked from the tensor. Identifiers are used only to bind the three frozen publication fixtures.

The optional negative controls alter a certified trace bound or omit a conductor branch and require rejection. `SHA256SUMS` records the publication files independently of the tensor fingerprints.
