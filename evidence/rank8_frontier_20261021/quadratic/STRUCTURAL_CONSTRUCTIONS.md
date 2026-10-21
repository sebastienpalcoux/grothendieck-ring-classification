# Complete construction obstructions for the six quadratic residuals

This note excludes construction routes for `1055,1768,1795,3258,3413,3472`.
It does **not** exclude their general categorifiability. The exact replay is
`structural_constructions.py`; all hypotheses are checked from source tensors.

For each ring all 128 subsets containing the unit are tested for duality and
product closure. The only proper nontrivial fusion subring in 1055,1768,1795
is the pointed `C2` subring. The other three have no proper nontrivial fusion
subring. Every global FP dimension is irrational. Thus none admits a
nontrivial faithful finite-group grading: its neutral component would be
pointed of FP dimension one or two, whereas faithful grading multiplies
that dimension by the integer order of the grading group.

Every nontrivial group equivariantization contains `Rep(G)`. This cannot be
the whole category here, whose FP dimension is irrational. The subring
audit rules out every such construction for 3258,3413,3472 and reduces the
question to `G=C2` for 1055,1768,1795. These last possibilities also fail:

* For 1055, the complete forced `A=1+g` module search has four solutions,
  all with difference-space action `S_g=-I`. If the pointed `C2` lifted
  centrally as a Tannakian subcategory, the central commutative algebra
  `A` would give a tensor quotient sending `g` to the unit. Its left action
  on every right `A`-module would therefore be the identity, forcing
  `S_g=I`, a contradiction. This argument uses the complete finite search,
  not the mere existence of one negative-sign solution.
* For 1768 and 1795 the unique nontrivial invertible acts freely on all eight
  simples. In a `C2` equivariantization an orbit of length two in the base
  contributes one simple fixed by tensoring with the sign representation;
  a fixed base simple contributes a pair exchanged by sign. This follows
  from the orbit/projective-stabilizer description of simples and
  `H²(C2,C*)=0`. The observed free sign action therefore forces every base
  simple to be fixed and the base to have rank four. Its dimension is
  respectively `222+36√37` or `270+120√5`, both greater than 45.
  The repository's unrestricted rank-four theorem gives the upper bound
  `24+12√3<45`, a contradiction. The exact rank-four quotient tensors and
  dimensions are included in the evidence, with all representative choices
  and multiplication identities checked.

The same rank-four bound eliminates the generalized-near-group branch
`(integer multiplier, invertible group order, noninvertible orbit size)
=(3,2,2)` for 1055 and 1768. Its proposed rank-four base has dimension
`148+24√37>45`. Together with the rank-two exclusions already recorded in
`RESIDUAL_QUADRATIC_SEARCH.md`, only the dimension branches `(1,6,6)` and
`(2,3,3)` remain for those two rings; no actual construction is supplied.

The rank-four bound is an **explicit repository theorem dependency**, not
a new theorem proved by this audit. Its precise source is
`manuscripts/rank4/papers/companion_sections/14_finite_certification.tex`,
Corollary `finite:cor:sharp-bounds`; the replay pins its SHA-256 digest.
It applies to arbitrary complex fusion categories in that manuscript.
The external pivotal-only rank-four theorem is not silently substituted
for this unrestricted statement.

The equivariantization inputs may be found in S. Burciu and S. Natale,
[*Fusion rules of equivariantizations of fusion categories*,
arXiv:1206.6625v2](https://arxiv.org/abs/1206.6625v2), especially the
orbit/projective-stabilizer description, and in
[EGNO, *Tensor Categories*](https://math.mit.edu/~etingof/egnobookfinal.pdf).
By A. Bruguières and S. Natale,
[*Central Exact Sequences of Tensor Categories, Equivariantization and
Applications*, arXiv:1112.3135](https://arxiv.org/abs/1112.3135), every
dominant tensor functor of FP index two is an equivariantization, so the
same obstruction also rules out such index-two tensor quotients.

These statements do not rule out arbitrary noncentral algebra objects,
fermionic rather than Tannakian structures, arbitrary Morita partners,
or associators on the residual rings. The free involution does not by
itself imply a central lift or a trivial pointed associator.

Read-only replay (checks remain active under optimization):

```sh
python evidence/rank8_frontier_20261021/quadratic/structural_constructions.py
python -O evidence/rank8_frontier_20261021/quadratic/structural_constructions.py
```
