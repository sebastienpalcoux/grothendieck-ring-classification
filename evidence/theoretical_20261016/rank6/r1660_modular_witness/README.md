# Exact passing modular-representation witness for R6_8_1660

The twist-one support theorem makes the T=1 space exactly the six constituents
of I(1). Its diagonal-torus character has multiplicities (3,1,1,1) for the
quadratic characters of conductors 1,8,12,24. The complete six-by-six low S
block also determines its compressed-S spectrum. These strengthen the older
signed SL2(Z/48) representation cone and retain the mandatory Z(Ising)
subrepresentation.

Low frame zero, canonical profile 10, admits an exact nonnegative integer
witness for all 1,536 recorded equations and 1,447 variable bounds. Its central
rank is 37. The profile is one of the 1,136 packet-Gram survivors. The witness
shows that this sharpened necessary system does not exclude the entire ring.

Run `python3 replay.py` here. Only the Python standard library is needed.
The output must have `status: PASS` and `mathematical_verdict: PASS_NECESSARY`.
The replay checks source hashes, every integer equation and bound, the original
profile and survivor membership, reconstructs the newly added representation,
torus, compression and profile rows, rebuilds CRT twist spectra, and checks the
mandatory Ising summand.

`system.json` stores sparse integer rows, right sides, bounds and metadata;
`witness.json` stores the integer solution. The included canonical profile,
packet receipt and finite-group character tables are frozen source inputs.
`provenance.json` records their original paths and exact hashes. The derivation
sources are retained for review under `derivation/`; their original SymPy
reconstruction requires the full repository and is not run by this compact
replay. In particular, the first 1,411 actual48 rows and the character-table
derivations are source-bound rather than regenerated here.

This is a passing necessary-system witness. It constructs neither a full S
matrix nor fusion rules in the center, associators, or a fusion category. It
does not solve all joint charge, twist and modular-data completion constraints.
The categorification question remains unresolved.
