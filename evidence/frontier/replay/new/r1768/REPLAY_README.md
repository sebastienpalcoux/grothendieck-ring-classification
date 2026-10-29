# R8_3_1768 exact replay and dependencies

The mathematical proof is `PALINDROMIC_EXCLUSION.md`. The main computational
check is `replay_palindromic_center.py`: it rebuilds the complete two-sign
domain from the tensor, reconstructs the published necessary center domains,
and verifies six old rational Farkas certificates. It performs no optimization,
signed-tensor classification, or associator search.

## Runtime

The tested environment was Python 3.12.14 on Linux, SymPy 1.14.0,
NumPy 2.3.5, mpmath 1.3.0, python-flint 0.9.0 and GCC/g++ 13.3.0.
Required third-party Python packages are SymPy and NumPy; mpmath is a SymPy
dependency. python-flint is optional exact-arithmetic acceleration used by
the tested SymPy installation. No floating-point result is accepted as a
certificate. Other versions/platforms have not been validated here.

A `g++` executable must be on PATH, with C++17 and `__int128` support.
The unchanged `gram_vectors_rank8.py` compiles the shipped
`evidence/rank8_m3_20261021/performance/gram_vectors_rank8.cpp` using
`g++ -O3 -std=c++17` when its binary is absent or stale. The extracted
source directory must be writable for this build; the adapter directory
must be writable for its JSON receipt. Do not package an old native binary
as a portability dependency. Compile from the included source.

For a fresh environment, the tested Python versions can be installed with:

```sh
python -m pip install sympy==1.14.0 numpy==2.3.5 mpmath==1.3.0
# Optional acceleration matching the recorded environment:
python -m pip install python-flint==0.9.0
```

SciPy/HiGHS appear only inside unexecuted solver functions in inherited
modules. They are not required for this replay. Likewise the inherited
signed-enumeration and other Gram executables are not invoked. There is
no network dependency after extraction. `recover_replay.py` was only a
source-recovery utility and is not part of the offline verification.

`replay_import_inventory.json` enumerates every static import in the 35
shipped Python source files, including imports inside functions that are
not called. The adapter additionally uses standard-library `runpy`.
Required local modules are shipped under `replay_source/`; their exact
paths, hashes and byte counts are in `replay_sources.json` (40 files
including certificates and native source). Some inherited optional
functions mention local modules absent from this reduced source bundle;
the inventory lists them explicitly. None is reached by either replay
adapter. Ordinary Python installation modules, NumPy, SymPy and their
own dependencies need not be copied into this bundle.

## Relocation and required layout

All executed paths resolve from each script's `__file__`, not the working
directory. There are no absolute workspace paths in the replay adapters.
Preserve the following paths relative to the extracted archive root:

- `new/r1768/replay_palindromic_center.py` and the complete
  `new/r1768/replay_source/` tree;
- `prior/data/current_remaining_cases.py` (the tensor source);
- for the optional short check, `new/r1768/verify_palindromic_exclusion.py`
  and `prior/evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1768.json`;
- the receipts, source manifest, proof and this README alongside the adapters.

No path edit is needed when that layout is preserved. In particular the
adapter resolves its tensor as `H.parents[1] / 'prior/data/current_remaining_cases.py'`,
where `H` is its own directory. If packaging only the `r1768` directory,
include the tensor file separately and change that one adapter input path;
the short verifier also needs its `BASE` changed to the relocated `prior`
directory. Do not change the SHA-bound tensor or any equation/domain builder.
Moving the whole archive is the recommended option.

The adapter replaces only the inherited `streaming.load_ring` entry point,
because the original whole-band census JSON was removed under the project's
cleaned publication policy. The substitute supplies the exact tensor,
case ID and SHA256. No equation, admissible-column generator or certificate
is changed. This already-applied adapter is the only compatibility fix
required; keep the internal `replay_source/` hierarchy unchanged.

From the extracted archive root:

```sh
python new/r1768/verify_palindromic_exclusion.py
python -O new/r1768/replay_palindromic_center.py
```

Both commands also work from another current directory when given the
correct path to the script. They write receipts next to the script and
use explicit failures, not assertions. The existing complete optimized
six-certificate receipt records PASS in 30.485 seconds; the earlier normal
five-certificate replay records PASS in 39.355 seconds. Runtime is machine
dependent. The short check was run both normally and with `-O`.

## Scope of verification

The short check verifies the tensor identities and binds the inherited
forced-indicator receipt. The six-certificate replay is stronger: it does
not assume that old final indicator conclusion. Its proof still uses the
categorical completeness of the inherited center domains and the existing
general-complex sphericalization/Galois gate. The exact gate theorem and
its categorical premises are identified in `PALINDROMIC_EXCLUSION.md`.
The expensive signed enumeration establishing that gate has not been
regenerated in this research pass.
