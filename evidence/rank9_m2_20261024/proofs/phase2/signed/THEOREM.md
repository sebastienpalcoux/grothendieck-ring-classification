# Nonzero products in the signed sphericalization quotient

## General criterion

Let `R` be a fusion ring and suppose that a fusion category over the complex
numbers has Grothendieck ring `R`. Pass to its canonical sphericalization and
choose a lift of each simple object, with the unit lifted to the unit and duals
lifted compatibly. The two lifts differ by the central invertible object
`epsilon` of categorical dimension `-1`. In the quotient of the Grothendieck
algebra by `epsilon + 1`, the chosen lifts give a basis `x_i` with

```
x_i x_j = sum_k T[i,j,k] x_k,
T[i,j,k] in {-N[i,j,k], -N[i,j,k]+2, ..., N[i,j,k]}.
```

The table `T` is associative and satisfies the unit, dual-reversal, and cyclic
Frobenius identities. The categorical dimension descends to a scalar algebra
character `d` on this quotient, and `d(x_i)` is nonzero for every simple lift.
Consequently

```
x_i1 x_i2 ... x_is != 0             for every finite word in simple basis elements.
```

Indeed, its image under `d` is the nonzero product of the nonzero simple
dimensions. This argument does not require commutativity, a pivotal structure
on the original category, pseudo-unitarity, or a Frobenius--Schur indicator
normalization.

Only the degree-two instance is needed here:

```
for every i,j, at least one T[i,j,k] is nonzero.
```

For multiplicity at most two this is automatic whenever `N[i,j,0]` is nonzero
or an odd channel occurs. Otherwise it is the finite disjunction that at least
one of the corresponding trace variables is `+2` or `-2`. A signed product
whose even channels all have trace zero is therefore forbidden before any
character-field calculation. This is a new optimization and unified criterion
in the project; its proof is an elementary consequence of sphericalization and
nonvanishing simple dimensions, not a claim that these foundations are new.

Foundations: Etingof--Nikshych--Ostrik, *On fusion categories*, Ann. Math. 162
(2005), 581--642, especially the squared-norm and spherical-dimension results;
https://arxiv.org/abs/math/0203060. For sphericalization, see also the same
authors, *An analogue of Radford's S^4 formula for finite tensor categories*,
https://arxiv.org/abs/math/0404504.

## Application to the nine incomplete rank-nine cases

For each ring below, enumerate all oriented signed associative tables after
imposing this necessary nonzero-product condition. Only dual-compatible basis
signs and verified based automorphisms of the input ring identify branches.
No signed coefficient is restricted to `+/-N`: multiplicity-two coordinates
retain the full `{-2,0,2}` domain.

| Ring | Remaining representative signed tables |
|---|---:|
| R9_2_686 | 15 |
| R9_2_690 | 2 |
| R9_2_726 | 2 |
| R9_2_728 | 3 |
| R9_2_736 | 22 |
| R9_2_1187 | 22 |
| R9_2_1241 | 4 |
| R9_2_1377 | 2 |
| R9_2_1424 | 2 |

Every remaining branch is excluded by a replayed established condition:
signed Casimir d-numbers; nonzero equal-dual scalar dimensions; formal-codegree
field/norm restrictions; dimension-order integrality; or the original
spherical exclusion when a signed tensor is a gauge of the original tensor.
In the last situation the selected lifts form a tensor-closed spherical
section: saturation `|T|=N` with the original signs means that every summand of
each selected tensor product is again selected.

The union of the impossible zero-product sector and these finitely many
closed branches exhausts every sphericalization of every potential
categorification. Thus **all nine rings are excluded in the general complex
fusion-category scope**.

## Reproducibility

`nonzero_products.py` discovers the complete branch certificates with an exact
pseudo-Boolean encoding. Each `R9_2_*.json` contains the input digest, clauses,
representative values, and exact branch obstruction. `verify_nonzero_products.py`
rebuilds associativity with an independent eight-bit-vector encoding, checks
the actual integer tensors, replays the algebraic obstructions, independently
constructs the gauge/automorphism orbit, and requires final `UNSAT`.
Every unreduced associativity equation has absolute value at most 72, so
eight-bit zero is equivalent to integer zero. `verification.json` records the
fresh replay outcome.

## A general-to-pseudo-unitary reduction from signed global dimensions

There is a related useful gate, without assuming that the signed table is a
gauge of the original one. Let `F` be the Frobenius--Perron global dimension of
`R`. Suppose every signed table passing the foregoing necessary conditions,
and every scalar dimension character on that table not excluded by established
field/norm/lattice tests, has

```
Delta = sum_i d(x_i) d(x_i*)
```

with the same irreducible minimal polynomial over the rationals as `F`.
Then any categorification of `R` has a Galois conjugate that is pseudo-unitary.

To prove this, note that `Delta` is the intrinsic global dimension of the
original category: its sphericalization has two lifts of each simple, with
opposite dimensions and the same squared norm, so its global dimension is
`2 Delta`. Fusion categories admit models over algebraic number fields. An
embedding carrying `Delta` to its conjugate `F` extends to an automorphism of
the algebraic closure of the rationals. Apply it to the structural constants
of the category. This preserves its fusion rules and hence `F`, while its
intrinsic global dimension becomes `F`. Equality of these two dimensions is
the definition of pseudo-unitarity, and the canonical positive spherical
structure then exists by ENO Proposition 8.23.

Thus an obstruction valid for pseudo-unitary categorifications of the same
based ring can be used after this gate to exclude arbitrary categorifications.
The gate alone does not imply existence and is not an exclusion.

The number-field descent and scalar-extension facts can also be found in
Davidovich--Hagge--Wang, *On Arithmetic Modular Categories*, Proposition 4.3
and Lemma 2.8, https://arxiv.org/abs/1305.2229. The intrinsic global-dimension
definition and pseudo-unitary theorem are in ENO cited above.

`galois_pu_gate.py` records the full signed dimension-character proof for each
successful gate in `gate_R9_2_*.json`. Running
`verify_nonzero_products.py --gates` independently replays those proofs and
records `gate_verification.json`. The accepted minimal-polynomial comparison
is exact; no approximate dimension match is used.

This reduction succeeds for the twenty rings
`R9_2_114`, `128`, `137`, `500`, `515`, `516`, `920`, `1235`, `1372`, `1373`,
`1487`, `1569`, `1607`, `1635`, `1636`, `1886`, `1959`, `1975`, `1976`,
and `1983` (all identifiers have the prefix `R9_2_`). Across them there are 72
representative signed tables after the necessary reductions. Together with
the nine exclusions and the 52 previously established gates, this means every
one of the 72 first-stage survivors left after the nine exclusions can be
treated in pseudo-unitary scope after a justified Galois conjugation.
Independent verification receipts, rather than discovery summaries, are
the authority for which computational certificates have completed replay.
