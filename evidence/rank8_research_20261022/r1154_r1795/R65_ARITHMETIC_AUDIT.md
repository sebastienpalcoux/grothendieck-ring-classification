# Independent arithmetic audit of the R65 pointed-phase exclusion

Result: **PASS** for the three decisive files
`../r65/pointed_phase_k0_fourier.json`,
`../r65/pointed_phase_k1_fourier.json` and `../r65/pointed_phase_k2.json`.
No arithmetic or domain-coverage defect was found in these certificates.
The mathematical pointed-induction lemma is audited separately; this audit
checks its implementation and the exact finite separation step.

The audit script is `audit_r65_phase.py`, with receipt `audit_r65_phase.json`.
It does not import the new `PointedPhaseCone` subclass or use its filtered
oracle. It imports the accepted parent `AtomicCMRealSTS` cone, reconstructs
the permitted columns independently from the phase/multiplicity conditions,
and evaluates the saved integral separators on every explicit sparse column.
The complete parent metadata and the resulting domain hash agree with the
saved certificates. All calculations are exact integer/rational arithmetic.

| Pointed class | Nonfixed second indicator | Columns checked | Minimum column pairing | Zero pairings | RHS pairing |
| --- | ---: | ---: | ---: | ---: | --- |
| 0 | -1 | 2413 | 0 | 541 | strictly negative |
| 0 | +1 | 2413 | 0 | 106 | strictly negative |
| 1 or 3 | -1 | 1992 | 0 | 238 | strictly negative |
| 1 or 3 | +1 | 1992 | 0 | 207 | strictly negative |
| 2 | -1 | 2222 | 0 | 116 | strictly negative |
| 2 | +1 | 2222 | 0 | 104 | strictly negative |

The script derives the four second-indicator branches directly from the
source tensor and checks the four-pointed-object induction Gram block:
diagonal entries 8 and off-diagonal entries 0. It verifies that no low
induction column contains a nontrivial source invertible, and retains every
low and rotation column. Generator high columns are filtered by exactly the
proved phase types; the class-zero and odd-class Fourier variants impose
multiplicity one and noninvertible coefficient sum at most 11.

## All-order trace coverage

The displayed bound 40 is a bound on finite **representatives of joint
relative traces**, not a bound on possible twists. The source global
dimension is \(250+110\sqrt5\), of norm 2000, so the inherited categorical
Cauchy theorem permits exponent primes 2 and 5. Write a root order as
\(n=2^a5^b\).

For powers \(j=1,2,3,4\), the reduced root order is
\(m=n/\gcd(n,j)\). If \(a\ge4\), every such \(m\) is divisible by 4:
the rational Ramanujan trace vanishes, and the quadratic-character Gauss
trace vanishes as well. If \(b\ge2\), every such \(m\) is divisible by 25;
again both trace components vanish. Thus every order outside
\(a\le3,b\le1\) contributes the all-zero four-tuple, which is present in
the domain. The remaining orders divide 40.

These are the trace types of **central twists**. The independent rotation
operators on third tensor powers may have third-root eigenvalues. Their
separate rotation columns remain in the cone unchanged; the exponent prime
restriction on central twists is not imposed on those operators.

Independently of the inherited Gauss-sum implementation, the audit computes
all relative traces for every primitive root of every order dividing 40 by
arithmetic in \(\mathbb Q[x]/\Phi_{\operatorname{lcm}(5,n)}(x)\).
The averaging subgroup consists of units \(u\) with \(u\equiv\pm1\pmod5\),
and the fixed radical is represented by
\(\sqrt5=1+2(\zeta_5+\zeta_5^{-1})\). This gives exactly the same 13 joint
trace types. Direct polynomial checks at orders 16, 25, 80 and 200 also
confirm the zero tuple outside the finite box; completeness follows from
the preceding valuation argument, not from these sample checks.

The forced phase types are independently checked in this same cyclotomic
arithmetic: primitive order 16 gives \((0,0,0,0)\), primitive order 8 gives
\((0,0,0,-1)\), and primitive order 4 gives \((0,-1,0,1)\).

## Audit boundary

This independently verifies the new restriction and Farkas arithmetic. It
uses the previously accepted categorical necessity and construction of the
283-row parent cone, including its complete restriction-column domains,
full character-field S symmetry and CM real STS equations. It does not
claim to reprove every earlier theorem. The direct class-zero certificates
mean that the prior trivial-pointed-class Morita exclusion is not a dependency
of this new unified exclusion. The remaining dependencies are explicitly
listed in the producer's `../r65/PROOF.md`.

Run from the repository root:

```sh
python evidence/rank8_research_20261022/r1154_r1795/audit_r65_phase.py
```
