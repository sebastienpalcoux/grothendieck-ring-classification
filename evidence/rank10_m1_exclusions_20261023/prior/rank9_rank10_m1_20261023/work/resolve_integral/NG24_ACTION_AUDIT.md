# Independent audit of the dimension-24 near-group action branch

**Verdict: accepted.** The argument in
`work/resolve_rank9_neargroup/NG_ACTIONS.tex` covers all complex
categorifications of the type `(1^8,4)` ring and every coherent involution
with exactly two fixed invertible objects. Its equivariantizations have
based ring `R9_1_12` or `R9_1_108`, and cannot have `R9_1_62` or `R9_1_87`.
This is a branch conclusion; a global exclusion requires the other
branches as well.

The audit consulted the actual text of Izumi, arXiv:1512.04288v2,
particularly Section 3, Remark 3.6, Definition 4.8, Theorem 4.9 and
Lemma 6.13. The finite verifier was rerun successfully: two dihedral and
six quaternion involutions, all matching the stated input tensors.

## Why the normal form includes tensorators

Transport an arbitrary unitary tensor autoequivalence to the chosen
simple representatives, so its object action is `g -> phi(g)` and
`rho -> rho`. Let `L` be its tensorator. The strict left absorption
`g rho = rho` implies that `L_(g,rho)` is a scalar `lambda_g`.
A natural-isomorphism component on each invertible g normalizes all these
scalars to one. The tensorator pentagon on `(g,h,rho)` then forces
`L_(g,h)=1`: a residual pointed 2-cocycle is impossible. A further scalar
on rho normalizes the trivalent image of the cup S_1; it does not undo
the left-absorption normalization.

In these formulas the trivalent images are
`L_(rho,rho)^(-1) F(S_g)` and `L_(rho,rho)^(-1) F(T)`.
Thus the proof is not implicitly assuming an initially strict functor.
Since `S_g=alpha_g(S_1)`, naturality and the same absorption coherence
force the first image to be exactly `S_(phi(g))`, without a separate
family of S_g phases. The second image is a unitary W on
`K=Hom(rho,rho^2)`. Compatibility with the left action and the normalized
cup gives

`W pi(g) W* = pi(phi(g))`, and `W j = j W`.

Izumi's generating-morphism statement then determines the functor on
all morphisms. Equivalently these are the tuple-equivalence conditions
in Definition 4.8 after the preceding normalizations. Consequently the
normal form describes arbitrary tensorators, not only strict label
permutations or a selected family of examples.

For each phi, the intertwiner is unique up to phase by irreducibility of
pi. Commuting with the antiunitary j restricts that phase to a sign.
The quotient between W and -W fixes S_g and negates T. It is tensor
isomorphic to the identity with components `eta_g=1`, `eta_rho=-1`;
naturality on these generators suffices. There is no remaining
identity-on-objects autoequivalence omitted by the enumeration.

## All categories, scalar parameters, and action coherences

Every complex category of dimension 24 is solvable and hence weakly
group-theoretical, so the cited unitarizability theorem applies. The
unitary equivalence and action can be transported back to the original
complex category. Izumi's integral classification then gives exactly
the three third-root parameters for each of D8 and Q8. These are the
six tuples with `j_1=j`, `j_2=epsilon*zeta*j`, `V=U_K=pi`, and `l=0`.
The normal-form equations commute with both antiunitaries for every
third root zeta; none is discarded or assumed real.

A tensor automorphism of the identity has scalar 1 on every g, because
`g rho=rho`, and scalar 1 on rho, because rho occurs in rho squared.
Hence `Aut_tensor(Id)=1`. An involutive tensor-autoequivalence class has
no further square-coherence choice or action obstruction. For the
explicit representatives the unique square isomorphism is visible:
`eta_rho=+1` for the dihedral matrices and `eta_rho=-1` for the quaternion
matrices, with `eta_g=1` in both cases. It is invariant under the functor,
so satisfies the action coherence equation directly.

## Duality and the finite check

The cup S_1 is fixed in the normalized presentation. Thus the two
rho lifts, whose equivariant scalars satisfy `u^2=eta_rho`, are self-dual
exactly when `eta_rho=+1`. All required D8 intertwiners are real
reflections and square to +1. All required Q8 intertwiners lie in SU(2)
and square to -1. In both cases their trace on K is zero. These facts
are independent of zeta and determine every large-object coefficient
along with the pointed orbit calculation.

`python work/resolve_rank9_neargroup/verify_ng_actions.py` checks all
8 D8 automorphisms and all 24 Q8 automorphisms, selecting 2 and 6
involutions respectively. Gaussian-integer matrices, with a common
square-root normalization removed, verify the equations exactly.
The reconstructed tensors are associative and match all coefficients
of R12 and R108 under explicit permutations. The output is
`work/resolve_rank9_neargroup/ng_actions.json`.

No additional unitary restriction, omitted scalar parameter, hidden
pointed tensorator, or unaccounted square sign remains in this branch.
