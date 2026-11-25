# Arithmetic checks for spherical structures in rank six

These files reproduce the finite computations used in *Spherical structures on fusion categories of rank six*. Run the following commands from this directory.

```sh
python -m pip install numpy sympy
python verify.py --list
python verify.py --jobs 4
```

Use Python 3.10 or later with assertions enabled. The C++ checks require a C++17 compiler with 128-bit integers, such as GCC or Clang. The replay works offline once these dependencies are installed. It copies the inputs to a temporary directory and checks the exit status of every computation. Add `--verbose` to see intermediate counts.

The manuscript links each finite calculation to its verifier or certificate. The driver runs the checks used by the current proof. The root-level scripts treat quadratic codegrees and several quartic bounds. Field-specific computations are grouped in `quadratic_24_28_checks`, `generic_quartic`, `field_checks`, `quartic_more` and `quartic_rational_frontier`. The odd-degree and sextic calculations are in `odd_degree_checks`, `sextic_certificates` and `sextic_complement`.

The final moment test at conductor twenty-four has a short standalone [verifier](field_checks/moments/quartic24_two_primes.py). It enumerates residues in the integral basis and writes one row of counts for each modulus. For every possible seed, either the count modulo 8 or the count modulo 11 is zero.

For the ten quartic fields whose dimension orbit has reciprocal mass one half in both character algebras, the [height verifier](quartic_more/ten_half_height.py) excludes trace at least 20. It calls the [integer interval calculation](quartic_more/half_bound.py) for three conductor tuples that cover the ten fields. The [lattice enumeration](verify_quartic_half_ten.py) excludes every remaining primitive ratio through trace 19.

The [conductor-13 check](sextic_complement/sextic13_descent.py) verifies a lattice containment for each of fifteen primitive ratios. At conductor eight, the [short-profile check](silver_short_profiles.py) tests 216 rational inequalities for the pairs (4,16) and (4,9). For cyclic conductor twenty the [candidate verifier](quartic_more/c20_candidates.py) checks the [separating inequalities](quartic_more/c20_duals.json) by exact arithmetic.

The conductor-twelve [recurrence check](twelve_three_twelve.py) treats the rational rows of codegrees 3 and 12. At conductor fifteen, the [period calculation](generic_quartic/c15_lattice.py) verifies the basis and trace-dual identities used in the proof. For a distinct quadratic pair at conductor twenty-four, the [quartic verifier](generic_quartic/general24/verify.py) checks the trace cutoff and a rational separating inequality for each of the 247 primitive ratios through trace 188. The [proof review](proof-review.md) records the changes to the argument.
