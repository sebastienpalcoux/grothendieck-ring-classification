# R6_9_3748: complete fusion-categorification exclusion

The proof excludes all characteristic-zero fusion categorifications, with no pivotal, spherical, braiding, or unitarity assumption. The categorical reduction is in `structural_reduction.pdf`; the final center obstruction is in `center_exclusion.pdf`. The corresponding LaTeX sources include primary-source references.

The final obstruction is elementary once the categorical reductions are established. The induction Gram budget and cubic Galois action allow at most four simple objects of any one centralizer dimension. Cauchy's theorem forces a 13-primary twist, whose Galois orbit has at least six objects of the same dimension.

## Reproduce

Install the version of SymPy in `requirements.txt`, then run:

```sh
python verify_all.py
```

The launcher runs every check under `python -O`, with a two-minute bound per job. It is independent of the working directory. The individual commands are:

```sh
python -O verify_sphericality.py --verify
python -O verify_relative_center.py --verify
python -O verify_center_exclusion.py --verify
```

The first exhausts the nine signed sphericalization candidates. The second reconstructs and verifies all fifteen rank-eighteen relative-center fusion tensors, leaving the two one-sided lifts. The third checks the six known centralizer dimensions, complete induction Gram subtraction, cubic Galois action, orbit norm bound, and final six-versus-four contradiction. Correctness gates use explicit exceptions and remain active under optimization.

All arithmetic is exact. The verifiers import only local Python code and SymPy, and do not require an earlier source package, research directory, network connection, or unfinished computation. Running an individual verifier without `--verify` regenerates its certificate; replay is read-only.

## Source fixture

`input_tensor.json` is the complete original row for `R6_9_3748` from `data/unresolved_tensors.json`. Its exact byte hash is pinned in `verify_sphericality.py`, and the other verifiers use that checked loader. The reconstructed tensor is compared with the frozen source tensor in every verifier. `source_metadata.json` retains the canonical source-file hash and basis permutation. The frozen fixture SHA256 is:

```text
7d64ff2cd0dc0cb74c6faeb51bcb70d21d943834b5a0b1faf31828186b647b14
```

The source basis becomes `(1,a,b,X,aX,bX)` through permutation `(0,1,5,2,3,4)`. The tensor is `A[X]/(X²−1−(2+2a+b)X)`, where `a²=1+b`, `ab=a+b`, and `b²=1+a+b`.

The numerical certificates support the proofs; they do not replace the categorical arguments establishing applicability of sphericalization, the regular bimodule, the relative center, and modular Galois symmetry. No factorization of an unbraided ambient fusion category is assumed.
