# Independent scope audit of three inherited proof trees

The proof trees in `../computation/` for R7_5_1964, R7_5_4530 and
R7_5_4531 use existing mathematical necessary conditions. This audit
checks their scope and branch structure; the independently regenerated
normal and optimized checker receipts in that directory check the finite
enumerations and exact arithmetic. Acceptance requires those replays.

## R7_5_4530 and R7_5_4531

In either source ring, each candidate spherical dimension character either
vanishes on a simple object or belongs to the same cubic orbit. In that
cubic orbit, the dimension-order certificate excludes the category:
the forgetful image of a constituent of the centrally induced unit has
dimension D/f, while forgetting forces its dimension into the integer
span of the simple dimensions. The supplied exact linear functional is
integer-valued on that span and takes the value **4/3** on D/f.
This uses spherical dimensions, not assumed positive dimensions.

The complete canonical signed enumeration has four quotients for R4530
and one for R4531. R4531's sole quotient is the source ring itself.
R4530 has three additional quotients; in each, one character orbit has
a zero simple dimension, while the remaining quartic orbit fails the
formal-codegree divisibility condition at the source codegree 9.

A quotient gauge-equivalent to the source corresponds to choices of
lifts whose products contain no opposite lifts. Those lifts form a tensor
section of sphericalization and transfer a spherical structure to the
original category. The original spherical obstruction therefore excludes
every such branch. The conclusion, after complete enumeration replay, is
a **general complex exclusion** for each source ring.

## R7_5_1964

The original spherical dimension characters comprise three zero-dimension
orbits, one norm obstruction, and one Frobenius–Perron Galois orbit. The
last can be conjugated to a pseudo-unitary category and invokes the
induction proof. All **5,025** low induction frames in that proof fail the
ordinary induction moment inequality. No branch in this particular proof
actually needs character labelling, Galois pruning, or rotation.

The complete oriented signed enumeration has **52** quotients. Four are
gauge-equivalent to the original ring. The other 48 are exhausted by
character covers: 160 zero-dimension obstructions and 72 norm
obstructions in total. The gauge argument just given closes the four
remaining branches using the original spherical proof.

Thus this proof also has **general complex** scope, conditional only on
successful exact exhaustive replay, not on a pivotality conjecture.

## Code reviewed

The scope-critical routines are `oriented_signed.problem` and
`enumerate_all` (canonical oriented lift domains and associativity),
`oriented_extension.verify` (complete signed quotient coverage),
`proofs.check_sphere` (all spherical dimension characters),
`dimension_order.verify` (exact integral linear functional), and
`character_induction.verify` (complete low frames and exact moment tests).
All are under `supplements/rank7/software/`.

## The other three members of the 5,025-frame family

R7_5_5343, R7_5_5623 and R7_5_5778 use the same induction-moment
strategy. Every one of their 5,025 low frames is excluded by an ordinary
moment inequality; their proof trees require no extra character-induction
theorem. The complete signed covers have the following counts:

| Ring | Signed quotients | Gauge-original branches | Character covers | Obstructions within covers |
| --- | ---: | ---: | ---: | --- |
| R5343 | 12 | 2 | 10 | 22 zero, 10 duality, 10 norm, 2 field-degree |
| R5623 | 40 | 8 | 32 | 96 zero, 48 norm |
| R5778 | 16 | 4 | 12 | 24 zero, 12 duality, 12 norm, 4 field-degree |

Each original spherical character outside the FP orbit is separately
excluded by a zero, duality, or norm condition. Duality obstructions
properly enforce equality of the categorical dimensions of dual simples;
the source rings need not be self-dual. Their general scope is valid
subject to the same independently completed normal/optimized replay.
