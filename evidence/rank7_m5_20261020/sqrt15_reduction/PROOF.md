# General-to-pseudo-unitary reduction for R7_5_443 and R7_5_1214

Every hypothetical complex fusion category with either based ring is
spherical and Galois conjugate to a pseudo-unitary fusion category.

Apply the repository's complete oriented sphericalization enumeration,
choosing the positive second-indicator lift of every self-dual simple.
For `R7_5_443` it visits 1,100 nodes; for `R7_5_1214` it visits 591,734.
In each case there is exactly one signed quotient: the original tensor N.
Since the positive and negative lift multiplicities are (N+T)/2 and (N-T)/2,
the selected lifts are closed under tensor product. They give a spherical
tensor subcategory of the sphericalization, tensor equivalent to the original
category.

The spherical dimension character cannot vanish on a simple object.
The exact character decomposition shows that every character outside the
Frobenius–Perron Galois orbit does vanish on at least one simple object.
Consequently the spherical dimension character lies in that orbit. A Galois
conjugation therefore makes every simple dimension equal to its
Frobenius–Perron dimension, giving a pseudo-unitary categorification.

Thus any pseudo-unitary obstruction for either tensor is a general complex
categorification obstruction. The conductor-60 center-trace certificates in
the adjacent `criteria` directory provide the further obstruction separately.

`verify_reduction.py` repeats the complete signed enumeration, verifies the
unique tensor, and checks every original character. `discovery.json` pins the
source tensors; its proposed branch metadata is not used to skip enumeration.
