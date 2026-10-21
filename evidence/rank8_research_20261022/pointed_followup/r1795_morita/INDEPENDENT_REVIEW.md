# Independent review: the forced R1795 subgroup dual

**Accepted scope.** Assuming the independently verified complete pointed
associator obstruction for `R8_3_1795`, every hypothetical complex
categorification has a separable subgroup algebra `A=1+g`, and its Morita
dual has the same Grothendieck ring `R8_3_1795`. This is a necessary
structural result. It constructs no category or associator, proves no tensor
equivalence between the two categories, and excludes no additional ring.

The conclusion remains outside the frozen accepted publication inventory
unless explicitly incorporated by the publication owner. No frozen source
was edited in this review.

## Categorical audit

1. **Existence of the algebra.** The reviewed eight-branch pointed obstruction
   makes the pointed `C2` associator trivial. The accepted Galois-to-pseudo-unitary
   reduction transfers this statement to general categorifications because the
   nonzero class of `H^3(C2,C*)=C2` is Galois invariant. The usual subgroup algebra
   consequently exists and is separable in characteristic zero. This input is
   explicitly assumed; it is not inferred from a feasible module action.

2. **Exactly four simple right modules.** The source action of `g` is free,
   with the four recorded pairs. By free-module adjunction,
   `End_A(X_i A)=Hom_C(X_i,X_i A)` is one-dimensional. Thus each free module
   is simple, and representatives of different pairs are distinct. Every
   simple right module occurs in an induced object, so this exhausts all
   four right modules. Left multiplication by `g` fixes their isomorphism
   classes: `gX_i` belongs to the same source pair as `X_i`, since the source
   ring is commutative.

3. **Exactly eight simple bimodules.** A left `A` action on a right module
   is a `C2` linearization for this genuine group action. On each simple
   right module the multiplier is scalar and is trivializable because
   `H^2(C2,C*)=0`. The two irreducible linearizations are one-dimensional
   and differ by the sign character; both are present and exhaust the
   simples over that right module. This gives eight bimodule simples.
   Their dimensions are the underlying dimensions divided by `FPdim(A)=2`,
   hence the positive list `1,1,6+3sqrt(5),6+3sqrt(5),7+3sqrt(5)` (four
   copies of the last entry). This division also follows by normalizing
   the positive dimension function on relative tensor products to give
   dimension one to the unit bimodule `A`.

4. **The character object is central only in the fusion ring.** The nontrivial
   character bimodule `h` has order two. Tensoring on one side changes the left
   linearization sign and acts freely on its two choices. The underlying
   object `X_i + gX_i` consists of two distinct simples. Both left and right
   `g` actions exchange these two summands. The diagonal map with entries
   `+1,-1` therefore changes both signs simultaneously. It identifies a
   left-sign change with a right-sign change, proving equality of the two
   tensor actions on isomorphism classes. No half-braiding on `h` follows
   or is used.

5. **The quotient is exactly the pair quotient.** For the right modules,
   `(X_j A) tensor_A Y_i` is the right module `X_j tensor Y_i`, independently
   of the left linearization on `Y_i`. Its source expansion gives the recorded
   pair-quotient matrix `Q_i`. The four matrices are linearly independent
   because their unit rows (or columns in the transposed convention) are the
   four standard vectors. Thus equality of action matrices identifies the
   full quotient structure constants, not just a quotient representation.

6. **Selfduality is proved before commutativity is imposed.** A dual preserves
   each pair because the underlying source orbit is selfdual. In the signed
   quotient write `a_i*=e_i a_i`, with `e_i=+1` or `-1`. Its coefficient-of-unit
   trace is cyclic and dual invariant. Consequently
   `tau(a_j^2 a_i)=e_i tau(a_j^2 a_i)`. Since
   `tau(a_j^2 a_i)=e_i T[j,j,i]`, a negative `e_i` forces that coefficient to
   vanish. The three odd quotient coefficients displayed in the proof force
   all three `e_i` to be positive. Only then does the basis-fixing
   anti-involution imply commutativity. In particular the argument does not
   use the invalid inference that equal positive dimensions force the two
   lifts to be selfdual.

7. **Pseudo-unitarity is used only for the dimension obstructions.** Transport
   the whole subgroup-algebra Morita context using the accepted Galois
   reduction. Morita invariance of global dimension and FP dimension makes
   the transported dual pseudo-unitary. Formal-codegree induction may then
   be compared with positive FP dimensions. The free-module, bimodule,
   quotient and selfduality arguments above need no pivotality assumption.

8. **The surviving dual has trivial pointed associator.** Once its ring is
   identified with R1795, the same reviewed pointed obstruction applies to
   it. Alternatively its character subgroup fixes each simple in the
   four-object Morita module category, which trivializes the restricted
   pointed associator. Neither argument identifies the two full associators.

## Independent finite calculation

`independent_review.py` imports no producer routines and does not reuse the
producer's six symbolic associativity polynomials. It uses lexicographically
ordered unordered triples and traverses **every one of the 2,531,250 normalized
assignments**. At each leaf it directly checks commutation of the symmetric
four-dimensional multiplication matrices. The sign-normalization map is
checked on the full eight-element sign group. Integer arithmetic is bounded
by small sums of products of coefficients of absolute value at most five.

The independent enumeration returns the same complete set of **45** signed
tensors. It then checks every unit, selfduality, Frobenius, commutativity and
ordered associativity identity of all 45 full eight-dimensional tensors in
Python integer arithmetic. The asserted positive FP character is checked
against every product; its squared dimension sum is exactly
`540+240sqrt(5)`.

For the obstruction review, it computes the **full eight-dimensional regular
Casimir**, independently of the producer's signed-sector Casimir. Its complete
factorization and exact norm valuations independently give:

| Outcome | Number of covers |
| --- | ---: |
| Formal-codegree norm obstruction | 41 |
| Central-dimension lattice obstruction | 2 |
| Accepted general rank-four bound | 1 |
| Exact match with R1795 | 1 |

For the lattice obstruction, the exact identity
`(60+24sqrt(5))(5+2sqrt(5))=540+240sqrt(5)` is checked. Every possible
forgotten object has radical coefficient divisible by three, whereas the
forced central dimension has coefficient two. This is stronger than a
numerical or bounded semigroup search and covers every nonnegative object.

For the rank-four case, the verifier checks closure and equality of the even
subring with `Q`. Its dimension `270+120sqrt(5)` exceeds `24+12sqrt(3)` by an
exact rational comparison. The general rank-four bound is the explicit earlier
input `finite:cor:sharp-bounds` in
`manuscripts/rank4/papers/companion_sections/14_finite_certification.tex`;
the source was inspected and its hash is bound. This review does not re-prove
that earlier classification theorem.

Finally the remaining tensor is compared coefficient by coefficient with the
canonical R1795 tensor under the recorded unit-preserving permutation. The
receipt binds the producer proof, source and result, the independent verifier,
the canonical tensor and the cited categorical dependencies.

Replay from the repository root:

```sh
python evidence/rank8_research_20261022/pointed_followup/r1795_morita/independent_review.py
python -O evidence/rank8_research_20261022/pointed_followup/r1795_morita/independent_review.py
```

Both commands must regenerate the same `independent_review.json`. They write
only a temporary native executable and leave the proof inputs unchanged.
