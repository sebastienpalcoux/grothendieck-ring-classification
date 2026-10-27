# Independent audit of the R1768 quaternionic Morita obstruction

Date: 27 October 2026. Offline research against frozen commit
`6a426acf6465dd674351be92dcca41b72f371521`.

## Verdict

The new proofs in `../r8_1768/UNIVERSAL_GH6_ROUTE_OBSTRUCTION.md` and
`../r8_1768/MORITA_QUATERNIONIC_RIGIDITY.md` are sound, subject to the
explicitly inherited general-complex gate, indicator theorem, and complete
necessary module-factor domain. The stronger conclusion is valid:

**No categorification of R8_3_1768 is Morita equivalent to any category
with the GH(C6,2) fusion rules, for any associator.**

This is a restriction on Morita models, not an exclusion of R1768.
The old necessary commuting based actions never forced such an equivalence.

## The categorical bridge

The delicate issue is the pivotal structure, rather than the final
parity arithmetic. After transporting a hypothetical Morita context to
the pseudo-unitary Galois form, both fusion categories are pseudo-unitary.
Choose their canonical positive spherical structures.

For a connected separable algebra A, its regular right module is simple:
`End_A(A)=Hom(1,A)=C`. A positive module trace exists by Schaumann,
Proposition 5.8. Apply his Theorem 6.6 to **this regular module**. Its
internal end is the original algebra A, with its original multiplication
up to algebra isomorphism. This yields a symmetric special Frobenius
structure on A itself; merely invoking a Morita-equivalent algebra would
not have been enough for the fixed-object argument. Normalize the
structure by `mu Delta=id_A`, `epsilon eta=dim(A)`.

The induced pivotal structure on A-bimodules has the trace relation

    dim_H U(M) = dim_H(A) dim_{A-bimod}(M).

It follows by closing the bimodule evaluation/coevaluation, using the
separability projector, and then the counit and unit. Both sides use
the same normalized symmetric Frobenius structure. In the present
positive spherical category the quotient is positive for every simple
bimodule. Thus the induced pivotal structure is the canonical positive
one. There is no sign freedom left when comparing indicators.

Mulevicius explicitly makes the forgetful functor from A-bimodules a
pivotal Frobenius functor. A Frobenius functor preserves duality, even
though it need not be strong monoidal. Its pivotal comparison commutes
with transposition. Therefore a negative selfduality isomorphism gives
a nondegenerate negative selfduality on the underlying object. This
does not assert that numerical indicators are preserved by forgetting.

On a positive-indicator selfdual simple constituent X, a negative pairing
induces an alternating nondegenerate bilinear form on its multiplicity
space. Its multiplicity must consequently be even. This is the only
parity statement used.

## Independent exact arithmetic

The accompanying `audit_r1768_profiles.py` imports no producer module.
It binds the source tensor and two inherited certificate files by
SHA-256, checks the positive dimension character and all induction Gram
identities, and independently refilters every one of the 61 preceding
factors using the free pointed involution. It then recomputes every
internal-end dimension directly as

    dim(internalEnd(M_r)) = (B[r,:] dot d)^2 / dim(A).

It obtains exactly 21 retained factors, including all 15 whose full
action has not been determined. Of these, 17 have a simple module whose
internal-end dimension has an odd coefficient of sqrt(37). The other
four, indexed `(0,0), (26,15), (42,0), (46,19)`, each contain an internal
end of dimension one. The full witnesses are in `r1768_profile_audit.json`.
Normal and optimized Python both pass in under one second.

This is an independent replay of the new arithmetic and the last filter,
not a rerun of the older exhaustive enumeration. Its coverage chain is:

1. The initial complete box has `a_0=1`, selfduality, and
   `0<=a_i<=floor(d_i)`. The bound is the diagonal-entry bound for a
   nonnegative module action with PF eigenvalue d_i. The saved exact
   Gram test leaves 115 possible algebra objects for R1768.
2. `rank8_next_20261021/quadratic/README.md` proves finite exact integral
   Gram enumeration, necessary action-row bounds, and internal-end
   profile closure. These sound filters leave 61 factors on 49 objects.
3. The nontrivial pointed associator forces a free involution on every
   module basis. The independent final filter above leaves all 21
   possible factors. No uncompleted full action is discarded.

The earlier completeness proof and certificates remain an explicit
input. In particular, “21 factors” does not mean that 21 categorical
module categories have been constructed.

## Why the stronger theorem follows

Let D be any Morita dual of a hypothetical positive R1768 category C,
and suppose D has a quaternionic invertible Q. Rebase its module
category at any simple m. Then D is the category of bimodules over
`A_m=internalEnd(m)`, with the same canonical positive pivotal structure.
The underlying object of Q has dimension `dim(A_m)`.

In C, all six nonpointed simples are selfdual with positive second
indicator, and each has coefficient one on sqrt(37). The parity lemma
therefore makes the coefficient of sqrt(37) in `dim U(Q)` even. Any
of the 17 odd-profile factors is impossible. Each of the four remaining
factors has an internal end equal to the tensor unit, so the module
category is equivalent to the regular C-module. Its dual is C or its
opposite, according to conventions, and has rank eight.

Consequently a nonregular Morita representative of C has no quaternionic
invertible. If D had the GH(C6,2) rules, write `u=6+sqrt(37)`. The
dimension-weighted total second indicator of C is 6u. Morita invariance
and the GH simple dimensions imply

    1 + nu_2(g^3) + u sum_j nu_2(g^j sigma) = 6u.

Irrationality forces `nu_2(g^3)=-1`, and all six large indicators are +1.
This gives a quaternionic invertible in a rank-twelve representative,
contradicting the preceding dichotomy. No assumption on its pointed
associator or on the algebra object is needed.

## Primary sources checked directly

* G. Schaumann, *Traces on Module Categories over Fusion Categories*,
  arXiv:1206.5716v3, Proposition 5.8, Theorem 6.6, and Lemma 2.9:
  <https://arxiv.org/pdf/1206.5716>.
* V. Mulevicius, *Condensation inversion and Witt equivalence via
  generalised orbifolds*, arXiv:2206.02611v1, Section 3.3 and equation
  (3.41), Section 4.1, and Example 4.15 (Example 4.18 in the published
  version): <https://arxiv.org/html/2206.02611v1>.

The full arXiv HTML and PDF were retrieved for this audit, beyond the
earlier indexed excerpt. The proofs require no unitarity assumption.
