# Arithmetic checks for spherical structures in rank six

These files reproduce the finite computations used in *Spherical structures on fusion categories of rank six*. Run the following commands from this directory.

```sh
python -m pip install numpy sympy
python verify.py --list
python verify.py --jobs 4
```

Use Python 3.10 or later with assertions enabled. The C++ checks require a C++17 compiler with 128-bit integers, such as GCC or Clang. The replay works offline once these dependencies are installed. It copies the inputs to a temporary directory and checks the exit status of every computation. Add `--verbose` to see intermediate counts.

The manuscript links each finite calculation to its verifier or certificate. The root-level scripts treat quadratic codegrees and several quartic bounds. Field-specific computations are grouped in `quadratic_24_28_checks`, `generic_quartic`, `field_checks`, `quartic_more` and `quartic_rational_frontier`. The odd-degree and sextic calculations are in `odd_degree_checks`, `sextic_certificates` and `sextic_complement`.
