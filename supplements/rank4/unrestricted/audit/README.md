# Exact supplementary checks

`check_regressions.py` reconstructs the fifteen model dimension characters,
compares optimized and reference signed enumerators at multiplicities one and
two, and compares characteristic polynomials and d-number decisions using
independent arithmetic implementations. `check_shortcut_algebra.py` checks
scalar identities. Both use explicit checks that remain active under Python
optimization.

The quartic resolvent chart and scalar-certificate scripts support exact
algebra in the theoretical bound. They do not establish the categorical
hypotheses needed to apply those identities.

**AI-generated research · independent verification pending.** No proof-assistant
formalization or independent human certification is claimed.
