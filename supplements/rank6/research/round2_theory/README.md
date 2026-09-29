# Stabilizer rotation beyond the two-dimensional case

The new categorical criterion is implemented in
`software/stabilizer_rotation_higher.py`. It applies to any simple object Y,
including one which is not self-dual, fixed by an invertible involution g.
A negative stabilizer commutator is read from an exhaustive antiinvariant
module representation. Set n=dim Hom(1,Y^3)=N[Y,Y,Y*]. The three pair-insertion
operators are anticommuting involutions cyclically permuted by pivotal
rotation. Their Clifford representation gives

    nu_3(Y)=-(a+b*omega+c*omega^2), a+b+c=n/2,

with a,b,c nonnegative integers. In particular n is even. If 3 is absent from
the Frobenius–Schur exponent's prime support, the allowed indicator values are

    -n/2 + 3*b, 0 <= b <= floor(n/4).

For a real relative trace field and unrestricted prime support, the averaged
values are n/4-3*a/2, for 0<=a<=n/2. The engine first uses the weaker interval
[-n/2,n/4] through two nonnegative slack variables. If that system does not
produce an exact separating ray, it checks every discrete averaged value.
All separating rays are independently verified using integer arithmetic.

The proof, including the non-self-dual case and the eight-dimensional exact
Clifford algebra check, is in the independently audited
`papers/chapters/stabilizer_rotation.tex`. No equality of modular data with a
particular category enters this criterion.

## Scope and replay

`higher_stabilizer_patterns.json` records complete bounded module branches
for every eligible inherited unresolved tensor. `higher_campaign.json`
classifies all forty inherited inputs, distinguishing ineligibility, absence
of an exact obstruction, completed pseudo-unitary exclusions, and explicit
budget overruns. Its input list is frozen independently of later changes to
the classification ledger. The multiplicity-three case is handled by the
separate dimension-two stabilizer campaign.

The `*_higher.json` files contain discovery outcomes at height three;
`*_higher_h6.json` are additional height-six attempts. A surviving relaxation
means only that this necessary sieve has not excluded the input. It is not a
construction, a categorical existence claim, or a verified associator.
`higher_positive_controls.json` records all fifty-four supplied positive
models, including the precise eligibility of each one.

For an exclusion certificate, run from the package root:

```sh
python -O software/stabilizer_rotation_higher.py R6_4_416 \
  --output research/round2_theory/R6_4_416_higher.json --verify
```

General nonexistence additionally requires a verified general-to-pseudo-unitary
reduction. The composite certificate kind is
`general_stabilizer_rotation_higher`; `verify_general` verifies both components.
The reduction may also be the exact payload `{"kind":"two_fp_values"}`;
the verifier checks that the tensor has precisely two distinct FP dimensions,
then applies the previously cited general-to-Galois-pseudo-unitary theorem.
No outcome in this research directory edits the classification ledger by itself.

`resume_higher.py` is a discovery-only checkpoint driver. It reuses the exact
second-indicator rows and checks selected assemblies against the original
engine. Its complete candidates are explicitly marked unverified until
`package_higher_general.py`, run with `python -O`, replays the unmodified
public verifier with optimization entry points disabled. Candidate-ray files
are search checkpoints, not additional mathematical assumptions.

## Completed campaign summary

The quadratic higher-dimensional engine supplies three complete pseudo-unitary
exclusions: R6_4_174, R6_4_416, and R6_4_427. Each now has a verified general
composite certificate. Among the forty frozen inherited inputs, one is handled
by the separate multiplicity-three engine, four have completed nonexclusion
runs, and thirty-two lie outside this engine's current local or trace domain.
The independent quartic engine applies to additional inputs outside this domain.

| Input | Low frames | Surviving labellings | Exact interval systems | Height |
|---|---:|---:|---:|---:|
| R6_4_174 | 10 | 8 | 128 | 6 |
| R6_4_416 | 895 | 2 | 32 | 3 |
| R6_4_427 | 315 | 8 | 32 | 6 |

All fifty-four positive models were classified for eligibility: forty-three
lack an eligible local rotation branch, four are outside the trace domain,
and all seven eligible runs completed without a false exclusion. The historical
height-six budget overruns for R6_5_638 and R6_7_1225 remain explicit in the
campaign index; they are not interpreted as exclusions. R6_4_174's initial
height-six budget was resolved by complete discovery and a 1027.73-second
optimizer-disabled exact general replay.

## Separate relative-center exploration

`relative_center_selfdual_signed_scan.json` is exploratory arithmetic on
self-dual signed quotients for a hypothetical relative center of R6_3_215.
It is not used in the classification proof. Three nongauge sign orbits pass
its codegree field/norm sieve; two are incompatible with the required common
stabilizer signs. Rejecting the remaining nongauge orbit would still leave
the original gauge orbit. In particular, a central fermion whose underlying
object is g is not excluded merely by trivial universal grading. The half-E6
category is a useful warning against that inference. The independent local
rotation argument supplies the actual multiplicity-three exclusion.
