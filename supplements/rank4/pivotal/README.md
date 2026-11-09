# Pivotal fusion categories of rank four

Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis,
*Classifying Grothendieck rings of pivotal fusion categories of rank four*.

**Authors' revision · 9 November 2026 · 17 pages.**

[Read the manuscript](manuscript.pdf) · [LaTeX source](manuscript.tex) ·
[Verification guide](supplementary/README.md) ·
[arXiv record](https://arxiv.org/abs/2609.33272)

The manuscript classifies the Grothendieck rings of pivotal fusion categories
of rank four over ℂ. Its theoretical bound FPdim < 3,600 reduces the problem
to a finite census of **8,977 rings**, with **8,962 exclusions and 15 models**.
Published existence results provide categorifications of the surviving rings.
The code checks the finite census, exclusion certificates, model tensors and
displayed numerical data; it does not formally certify the categorical proofs.

## Reproduce the checks

From this directory:

```sh
python3 -m pip install -r supplementary/classification/requirements.txt
python3 supplementary/check.py --verify-only --workers 4
```

To regenerate the census and certificates as well, omit `--verify-only`.
Add `--deep` for the unpruned census comparison, exhaustive small parameter
boxes and strict dimension-boundary checks. Python 3.10 or later and SymPy
are required; regeneration and the additional deep checks require a C++17
compiler. See the [verification guide](supplementary/README.md) for the full
scope, data format and individual commands.

Keep `manuscript.tex` beside `supplementary/` when copying the package: the
runner checks the manuscript against the verified structured data.

This pivotal paper is separate from the
[general rank-four classification and its replay packages](../README.md).
