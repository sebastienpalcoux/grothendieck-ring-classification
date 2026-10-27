# R6_8_1660: two further module-category obstructions

27 October 2026. **Two proposed module realizations are excluded. The source
ring remains unresolved.** The application uses the pivotal-Frobenius pairing
lemma developed in the parallel rank-eight analysis: for a positive symmetric
separable internal-end algebra A, the forgetful functor from A-bimodules to C
is pivotal Frobenius, hence transports a nondegenerate selfduality pairing
with its transpose sign. Numerical Frobenius-Schur indicators need not be
preserved, and no such assertion is made.

A selfdual simple of the dual category therefore cannot forget to an object
with odd multiplicities of both positive- and negative-indicator selfdual
source simples. There is no choice of its own sign that could accommodate
both: the opposite-sign multiplicity space would have to be symplectic and
therefore even-dimensional.

The source signs are `(1,1,1,1,-1,1)` on `(1,g,X,gX,sigma,T)`.
For a module based at its first leaf m, let N_i be the source action matrices
and Q the action of a simple of the Morita dual. The underlying A-bimodule
has restriction coefficients

    [U(Q):X_i] = (N_i Q)[m,m].

This is internal-Hom reciprocity: U(Q)=internalHom(m,Qm). It is not a
dimension match. All matrices and duals below are the exact archived
`action_matrices` and `dual` fields in
`supplements/rank6/research/frontier/new_research/r1660_categorical/dual_actions_receipt.json`.

* Type III_mixed, solution0, simple4 is selfdual and restricts to sigma+T.
  Both coefficients are odd, with opposite signs. This module category
  cannot exist. The algebra support was1+X; the alternative equal-sign
  type III is a distinct module structure and is not excluded by this step.
* Type IV_mixed, solution1, simple2 is selfdual and restricts to
  X+gX+sigma+T. Again the odd signs conflict. This realization with algebra
  support1+X+T cannot exist.

The same contradiction appears at additional simples in these branches:
III_mixed simple5 restricts to4X+4gX+sigma+7T; IV_mixed simples3,4,5 have
restrictions `(0,1,7,8,1,10)`, `(1,0,8,7,1,10)`, `(1,1,10,10,1,15)`.
One contradiction per branch suffices.

## What survives

* Type II, the possible original-ring self-Morita partner, passes the test.
* Type III_same, solution0, the R8_3_941 route, passes. Its only odd-sigma
  restrictions are2X+2gX+sigma+4T at the nonselfdual pair6,7. There is no
  selfdual-sign contradiction for that pair.
* Type IV_mixed, solution0, the rank-six Ad(E6)-based alternative, passes.
* Type III_same, solution1 was already removed by the previous second-indicator
  comparison; it is not counted as newly excluded here.

Thus the new filter removes two realizations of potential self-Morita
partners. It does not remove any of the three remaining based-ring types
from the entire possible Morita list, and does not force a nonpointed
algebra to exist.

The independent audit rebuilds the source actions and replays both short
contradictions in `../audit_fs2/`; its source-bound receipt is authoritative
for the exact matrix calculation. The categorical scope is conditional on
the separately proved positive pivotal-Frobenius lemma, with its module-trace
and symmetric-algebra normalization hypotheses explicitly retained.
