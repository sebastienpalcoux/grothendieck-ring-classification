# An exact integral trace obstruction for center profile 306

The inherited exhaustive frontier consists of six profiles
275,277,279,296,298,306. The present certificate excludes profile306,
whose proposed center has rank44. The five remaining center ranks are
46,48,52,54,60. R6_4_155 remains unresolved.

Use the established pseudo-unitary Galois reduction and the inherited
low-frame and pointed-twist theorem. Every surviving frame has low
index6, second indicators `(0,0,1,-1,-1)`, and four equivalent character
assignments. They differ only by permutations of equal restriction
columns. The builder checks the low columns, all four assignments and
this quotient, the six inherited profile identifiers, and the absence
of additional spectral pruning.

The builder calls the existing exact `round3_m4.system` at height6 in
Q(zeta24), fixes the profile's restriction-column multiplicities, and
imposes the inherited pointed twist support. It introduces two kinds
of original variables:

* the number of actual central simples with a specified restriction
  column and specified tuple of normalized relative twist traces;
* the number of actual rotation eigenvalues with a specified tuple of
  normalized relative traces on `Hom(1,X^n)`, for 3<=n<=6.

Both kinds are nonnegative integers. Grouping objects or eigenvalues
by equal normalized trace tuples does not divide their multiplicities.
The equations are the inherited Gram, higher-indicator, rotation,
Galois-balance and character-balance necessary conditions. They do not
assume unitarity, an exchange action, or an exact third-indicator value.

The certificate stores49 successive integer-bound deductions:16 on
rotation counts and33 on central-simple counts. To certify an upper
bound x_j<=u, its sparse exact Farkas ray proves infeasibility after
adding x_j>=u+1 and the preceding bounds. Integer-valued x_j therefore
satisfies the upper bound. Lower bounds are proved analogously. A final
exact ray contradicts the original equations together with all49 bounds.
Only the original count variables are rounded; newly introduced slack
variables are treated solely as nonnegative.

`verify_integral_306.py` rebuilds the system and checks every ray using
exact integer arithmetic. It blocks numerical optimization before
importing the builder, uses explicit checks that remain active under
Python's `-O` flag, and has no discovery-time dependency. Run from the
package root:

```
python -O research/frontier/R6_4_155/verify_integral_306.py
```

The frozen prerequisite six-profile proof remains in
`research/round5/m4_155`; its optimizer-free replay establishes the
input frontier. The new certificate is `exact_integral_306.json`, and
its portable exact builder is `integer_trace_system.py`.
