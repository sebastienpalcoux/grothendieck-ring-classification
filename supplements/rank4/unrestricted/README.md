# Unrestricted rank-four classification: exact certificate package

**AI-generated research · independent verification pending.** The mathematical
arguments and data require independent expert verification; they are not
Lean-formalized. Exact computational checks do not formalize categorical proofs.

The general rank-four manuscript proves a theoretical bound `FPdim < 1000`
and multiplicity at most 31, then classifies the complete finite range. It
identifies fifteen Grothendieck rings, proves sphericality of every rank-four
complex fusion category, and gives the sharp bounds
`FPdim ≤ 24 + 12√3` and multiplicity at most 6.

This directory contains the standalone computational part. The adapted papers
are in `manuscripts/rank4/papers/` in the repository and research bundle.

```sh
python3 verify_package.py
python3 supplementary/check.py --deep
python3 verify_package.py
```

Requirements: Python, SymPy, and a C++17 compiler with OpenMP. The optional
`python-flint` backend performs the same exact polynomial arithmetic. Install
Python requirements from `supplementary/classification/requirements.txt`.

The default replay freshly regenerates the ordinary census and the entire
signed cover. The `--deep` option also removes dimension pruning, compares the
complete parameter set, tests every multiplicity-two parameter assignment,
compares reference signed enumerators, and checks scalar identities.

The ordinary census has **1,692 rings: 1,642 self-dual and 50 with one dual
pair**. Its ledger has **1,677 exclusions and 15 models**. The broader signed
cover has **92,795 orbits**, of which **2,217** pass the common arithmetic
conditions. Its **1,182 positive orbits** have **1,173 exclusions and nine
self-dual models**. These are distinct scopes.

To check the paper's generated tables from this directory in the repository:

```sh
python3 verify_package.py --manuscript-root ../../../manuscripts/rank4/papers
python3 supplementary/check.py --deep --manuscript-root ../../../manuscripts/rank4/papers
```

For an independently extracted package, omit `--manuscript-root`, or supply
the actual path to the accompanying `papers` directory. Generated tables are
compared byte-for-byte; the checker does not modify the paper. The manifest
freezes source, deterministic data, generated tables, and delivered receipts.
Fresh timing reports may change when verification is rerun.

The full-census ledger selects arithmetic witnesses in a canonical polynomial
coefficient order. Both optional arithmetic backends therefore reproduce the
same ledger bytes. Delivered normal and optimized replay receipts are checked
against the shipped census and ledger hashes.

The branch-by-branch census coverage proof is in the manuscript appendix;
`source/census_appendix.tex` provides its source alongside the enumerator.
Necessary categorical criteria and existence references are in the manuscript.
The scripts verify their finite hypotheses and arithmetic consequences.
