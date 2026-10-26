# D32 round4 — all18 cases resolved offline

- **New models:** R12_1_419 and R12_1_530.
- **New general-complex exclusions:** R12_1_128,144,147,173,237,275,285,294,301,318,412,415,422,431,524,536.
- **Unresolved:** zero in this family.
- **Prior positive retractions:** zero.

The proof first forces an actual order-two algebra with pointed neutral Morita dual. It then classifies both possible source types. The generalized-Ising branch retains an essential nonsplit group extension; its two actual Liptrap reference categories supply the new models. ENO extension theory and the Shapiro isomorphism reduce all other associators to complete group-cohomology parameter lists. A separate independent audit has accepted both the categorical converse and the full finite enumeration.

`theory.md` contains the complete argument. `results.json` records permanent census identifiers and decisions. The exact original tensors remain frozen in `original_tensors.json`.

Portable replay, requiring Python and NumPy:

```
python -O verify.py
python -O finite_bicharacter_lemmas.py
python -O shapiro_check.py
python -O exhaustive_catalog.py
python -O structural_binding.py
```

The positive replay checks34,816 Liptrap identities,512 exact Fourier blocks,65,536 group-cocycle equations and all1,728 target coefficients for each new model. The complete catalog checks96 generalized-Ising constructions and46 TY action/square choices. The structural replay checks all24 retained census tensors and separates the16 excluded ones from the eight allowed rings.

Independent replays and the categorical acceptance note are in `../audit_models/`. They use full monomial Hom equations for all96 subgroup bimodule categories, independent equivariant Hom calculations for all46 TY cases, and separate colored-product-graph nonisomorphism checks.

`accepted_manifest.json` identifies the accepted proof and replay files. Other research scripts in this directory preserve the exploration history; failed bounded ansätze make no contribution to any exclusion. No online or repository revision was performed.
