# Dimension-80 ring rigidity

**Theorem.** Every complex fusion category of type `(1,5;5,3)` has the
based ring of `Rep((C2)^4 semidirect C5)` for the fixed-point-free action.
Its maximum multiplicity is two. Thus R8_3_275, R8_3_276, R8_3_344 and
R8_3_345 are not categorifiable.

The category is solvable by Etingof–Nikshych–Ostrik, *Weakly
group-theoretical and solvable fusion categories*, Theorem 1.6. Use its
cyclic-prime extension/equivariantization sequence (Definition 1.2(ii),
Proposition 4.4). A final prime extension would have neutral dimension
40 or 16. A subcategory here has dimension `a+25b`, with `a in {1,5}`
and `0<=b<=3`, since its invertibles form a subgroup of the group of
order five. Neither 40 nor 16 occurs.

Thus the last step is an equivariantization by C5: its embedded Rep(Cp)
forces p=5. The base D has dimension 16. For a cyclic-prime action, a
fixed base simple of dimension d produces five equivariant simples of
dimension d, while a free orbit produces one of dimension 5d. Projective
representations of cyclic stabilizers are one dimensional. Base dimensions
are rational algebraic integers, hence integral. A fixed dimension-five
object is impossible since 25>16; every free-orbit object is invertible.
Thus D is `Vec_H^omega`, |H|=16, and C5 fixes only the unit of H.

Every invariant subset containing the identity has cardinality one
modulo five. The center of the nontrivial 2-group H is characteristic
and nontrivial, so its order (a power of two dividing 16) must be 16.
Now H is abelian and its characteristic subgroup H[2] is nontrivial;
the same argument gives |H[2]|=16. Hence H=(C2)^4. Its fixed-point-free
order-five linear operator has minimal polynomial
`Phi5(t)=t^4+t^3+t^2+t+1`, irreducible over F2. Its action is unique
up to linear conjugacy (and replacing a generator of C5).

There are five unit characters and three free-orbit simples X_O. Unit
characters act trivially on the latter. Every X_O is self-dual because
inversion on H is the identity. Reciprocity therefore forces all five
unit-character coefficients in X_O X_P to be delta(O,P). The coefficient
at a nonzero orbit Q is the number of pairs (x,y) in O times P with
x+y=z, for any fixed z in Q. Forgetting equivariance proves this count,
and the trivial stabilizers mean no additional projective label can
alter it. This argument does not require omega or the action coherence
to be trivial. Thus the based ring is uniquely the untwisted orbit ring.

The fresh recovery verifier constructs the order-five companion action
on F2^4, all three orbits and all 512 orbit-ring coefficients, checks
associativity and the dimension equations, and finds maximum two. It
independently scans the authoritative census for this dimension type,
recomputes each tensor SHA256 and verifies that precisely the four
stated tensors have maximum three. Their multiplicity contradicts the
forced ring. No unitarity assumption enters the proof.

Run `python -O evidence/rank8_m3_20261021/models/psl2_11/r275/verify_dimension80.py`.
The default compares the entire regenerated certificate; `--write`
explicitly regenerates it after a source restoration. This is a fresh
reconstruction after the workspace reset, not an invented copy of a
missing prior certificate.
