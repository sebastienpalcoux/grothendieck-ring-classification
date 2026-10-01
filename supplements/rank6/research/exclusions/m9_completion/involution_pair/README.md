# Two multiplicity-nine general exclusions

This bundle certifies general nonexistence for R6_9_529 and R6_9_2455. The mathematical argument is in proof.md.

Run the exact verifier from optimized Python, using the existing rank-six package for read-only mathematical primitives:

    python -O verify.py --source /absolute/path/to/Rank6_Categorification_M9 --id R6_9_529
    python -O verify.py --source /absolute/path/to/Rank6_Categorification_M9 --id R6_9_2455

Omitting the ID verifies both. When installed within the source package, its ancestor directory is the default source. Otherwise the default is work_m9/Rank6_Categorification_M9 under the current working directory.

The frozen complete tensors are bound to hard-coded SHA-256 hashes. The verifier does not read an unresolved ledger. It checks exact Cauchy-pruned induction domains, every character labelling, every self-dual second-indicator sign assignment, all Farkas rays, spherical character reduction, complete saturated oriented sign enumeration, and the full 1057-polynomial quartic domain. No numerical optimizer is allowed.

The source package's Python dependencies, a C++17 compiler, and ordinary Python are needed. The two supplied Gram-vector primitive files are unchanged copies of the package's exact native helper, placed here so compilation never writes into the source package. Native compilation and its temporary files stay inside this bundle.

The certificate files contain 48 exact unrestricted-indicator rays for 529 and 992 for 2455. The other low frames are rejected by exact Gram/moment inequalities or absence of character-reciprocity labellings. Every small finite domain is regenerated, rather than accepted from an enumeration count alone.
