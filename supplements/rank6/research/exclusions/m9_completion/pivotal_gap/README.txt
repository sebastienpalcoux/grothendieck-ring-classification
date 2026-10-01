Exact signed-spectrum certificates for R6_9_7018, R6_9_8099, R6_9_8101.
Run: python verify_bundle.py
Optional binding to a package: python verify_bundle.py --source-root /path/to/Rank6_Categorification_M9
Requires Python 3 and SymPy. The bundled complete tensors are SHA-256 checked.
The quadratic 7018 proof must be combined with the higher-degree exclusion in the gauss8200 bundle.
All mathematical checks use explicit exceptions and survive python -O. Execution is deterministic except for the displayed runtime, which is excluded from certificate comparison.
