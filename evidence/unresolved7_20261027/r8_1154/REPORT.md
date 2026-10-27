# R8_3_1154: new theoretical restrictions, still unresolved

The individual continuation obtained three results. None supplies a
complete model or a general-complex exclusion, so the ring remains open.

1. **All six noninvertible trivalent rotations must be identity.** The
   rank-ten equivariantization has dual lifts x and ux of X4, and vx and
   uvx of X5. A new odd-indicator doubling lemma restricts their third
   indicators to twice a cube root. Exact short certificates then force
   all six noninvertible source third indicators to be 2, uniformly on
   every remaining center pattern. This removes 33 discrete indicator
   branches. All three all-2 center patterns have exact feasibility
   witnesses. The categorical proof and all 39 branch records were
   independently audited. See `ODD_ROTATION_THEOREM.md` and
   `../audit_parity/AUDIT_R1154_ODD_ROTATION.md`.

2. **There is no nontrivial integral object in the center.** A short
   argument using positive irrational FP coefficients, the noncentral
   invertible g, and full adjoint closure proves Z(C)_int=Vec for every
   complex categorification, without center enumeration or a spherical
   assumption. Hence no Morita partner can be a nontrivial finite-group
   extension or equivariantization. In the auxiliary rank-ten category,
   the sole possible Tannakian group descent is the already known C2
   one. See `INTEGRAL_CENTER_OBSTRUCTION.md`.

3. **Three additional direct model families are ruled out uniformly.**
   The natural golden-field candidates Fib^6, GH(C4,1) times Fib^3,
   and GH(C4,1)^2, even after arbitrary pointed tensor factors, cannot
   produce the target by central connected-separable-algebra
   condensation. The last, dimension-compatible index-three case
   forces a central full C4 condensation and then the forbidden
   rank-two ring x^2=1+4x. See `HAAGERUP_PRODUCT_ROUTES.md`.

The first result narrows the unknown trivalent associators sharply; it
does not determine their pentagon equations. The model-family arguments
do not exclude arbitrary noncentral Morita algebras or different ambient
categories. No classification ledger, manuscript, repository remote, or
website was changed.

## Exact checks

    python evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py
    python -O evidence/unresolved7_20261027/r8_1154/verify_odd_rotation.py
    python evidence/unresolved7_20261027/r8_1154/verify_integral_center.py

These use small exact matrices and direct ring arithmetic. They finish in
seconds. The discovery scripts `probe_...` are not the authority for the
accepted theorem; the optimizer-free exact replay and independent audit
are. Numerical feasibility is never counted as a category.
