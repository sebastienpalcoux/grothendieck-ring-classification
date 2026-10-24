# R8_3_1154 and R8_3_1768 continuation,24 October2026

**Decisions:0 excluded,0 categorified,2 still unresolved.** No repository
or website changes were made.

The published restrictions on R1154 (three center patterns,25 pair
histograms) and R1768 (the final V=4 sector with18 or72 primitive objects)
remain in force. No missing categorical premise is supplied by a
numerically consistent center or by the based actions developed here.

## Completed new work

1. **R1768: the higher-multiplicity Haagerup route is now concrete at the
   based-module level.** The ring `GH(C6,2)` has the required global
   dimension. A hypothetical algebra `1+rho` forces a unique rank8
   induction factor and precisely two possible GH module actions.
   On the R1768 side, published candidate7, factor2 (`1+X3`) previously
   had an undetermined full action. It has exactly two action completions
   after fixing its free pointed action. All64 source products pass.
   Every compatible C6 generator is enumerated: there are two, mutually
   inverse. Combining them with the two GH rho choices gives eight
   marked commuting action pairs, or four modulo generator inversion.
   All96 left/right commutations are checked for each representative.

2. **A conditional categorical obstruction excludes the untwisted
   version of that route.** Any actual Morita bimodule realizing those
   actions forces the pointed C6 associator of the GH category to be
   class3 in `H^3(C6,C*)=Z/6`. Its C3 restriction is zero and its C2
   restriction is the nontrivial one. Thus an ordinary untwisted GH
   construction cannot simply be declared a model. An actual twisted
   GH(C6,2) category and its separable `1+rho` algebra remain missing.

3. **The cyclic144 isotropic-orbifold chain has an associator obstruction.**
   For the specified crossed-product realization of a cyclic
   `C_(m^2)` source, quotienting by its maximal isotropic `C_m` produces
   a pointed C_m class that restricts nontrivially to every nonidentity
   subgroup. At m=12 this blocks the proposed further C2 quotient.
   The result is conditional on the stated first-arrow realization and
   does not assert a general classification of near-group categories.

4. **Independent indicator tests pass.** All100 R1154 semionic-packet
   checks give an independent proof of an already known source sign.
   The18-object R1768 Weil branch has second indicator +1 on each
   primitive object and on alpha. Those tests do not exclude either ring
   or reduce the previous branch counts.

## Model search scope

The existing manuscript/evidence attempts were checked before these
extensions: the semionic packet and closure proof, the excluded
SU(3)_7 product route, complete R1768 module-factor filter, saturated
conductor theorem, Weil block, and prior near-group scaling audit.

Primary literature was checked for the new routes. Izumi1512.04288,
Sections10 and12, supplies conditional reconstruction and orbifold
results, not a category with the newly needed parameters merely because
its equations are written down. The twisted-crossed-product Theorem12.17
would obtain NG(C36,72) from a suitable order144 source only with a
nondegenerate alternating C2² restriction. No two-generator abelian
order144 group can have such a restriction: the possible2-primary groups
are C16, C8×C2, and C4×C4, whose two-torsion restrictions have respectively
rank at most1, at most1, and0. The two-generator existence theorem in
Radchenko–Wheeler therefore does not complete that particular route.

The recent general odd-order Haagerup–Izumi construction and graded
extension literature do not provide the required even-order, higher
multiplicity, pointed-class3 category. A literature search failing to
find such a model is not an exclusion theorem.

## Files and replay

- `GH6_ROUTE.md`: proof and complete categorical scope.
- `verify_gh6_route.py`, `gh6_route_verified.json`: exact completed actions.
- `CYCLIC_ORBIFOLD_ANOMALY.md`: carry-cocycle derivation and route obstruction.
- `verify_cyclic_anomaly.py`, `cyclic_anomaly_verified.json`: exact checks.
- `INDICATOR_CHECKS.md`, `verify_indicator_checks.py`, `indicator_checks.json`:
  indicator proof and exact identities.

All three verifiers use explicit exceptions for required checks. The GH
verifier has passed both ordinary and optimized Python. Scripts named
`*_probe.py` and their receipts are exploratory predecessors; the
`verify_*` scripts and proof files are the reviewed deliverables.
