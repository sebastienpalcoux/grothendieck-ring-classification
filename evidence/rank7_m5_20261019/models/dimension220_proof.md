# A dimension-220 descent obstruction

**Unused alternative research argument.** This is not the certificate used
by the final classification. The accepted exclusion of `R7_5_4757` is the
shorter cyclic-isotypic obstruction. The associated script verifies only
the tensor premises of the longer argument below.

**Claim.** The fusion ring `R7_5_4757` has no complex fusion categorification.

## Exact premises

The positive dimension vector in the census basis is `(1,1,1,4,10,10,1)`.
The invertibles form the cyclic group of order four; its unique involution
fixes all three noninvertibles. The adjoint closure is the full ring.
The formal codegrees are `220,5,44,44,4,4,4`, so the simple summands of
the induced unit in the center would have dimensions
`1,44,5,5,55,55,55`. All half partitions excluding the unit are two of
the three entries 55; each complement contains both entries 5.
`dimension220.py` checks every dimension equation, the codegree polynomial,
all 64 half subsets, the invertible multiplication/action, and adjoint closure.

## From the half partitions to a dimension-110 category

The half-partition proposition in the rank-seven manuscript applies with
`(p,q)=(5,11)`, and makes any categorification C weakly group-theoretical.
For precision, that proposition uses the integral pseudo-unitary structure,
Ostrik's induced-unit theorem, and ENO's prime-power/Tannakian arguments;
no braiding of C is assumed.

Every finite group whose order divides 220 is solvable. If 11 divides its
order, its number of Sylow 11-subgroups divides 20 and is 1 modulo 11,
so its Sylow 11-subgroup is normal. The quotient has order dividing 20,
and is solvable by Burnside's two-prime theorem. If 11 does not divide the
order, Burnside applies directly. A nilpotent category Morita equivalent
to C has dimension 220. The groups in its successive extension series
have orders dividing 220, so they are solvable. By ENO Proposition 4.5(i),
this category, and consequently C, is solvable.

The full adjoint closure rules out a last extension step in the
cyclic-prime construction of a solvable category. The last step must
therefore be `C = D^{C2}`: a prime-order character subgroup embeds in
the invertible group C4, and hence its order is two. Twisting equivariant
structures by its nontrivial character exchanges the two simples over a
fixed underlying simple; a character-fixed simple instead lies above a
free two-element orbit. The two pairs of invertibles in C therefore yield
two invertibles in D. The character-fixed objects of dimensions 4,10,10
yield two simples each of dimensions 2,5,5. Thus D is integral and has type

`(1,1,2,2,5,5,5,5)`, of global dimension 110.

By ENO Theorem 9.2, every integral fusion category of dimension
`110=2*5*11` is group-theoretical. We next rule out this type for every
group-theoretical category of that dimension, including arbitrary
allowed associators and projective stabilizers.

## No group-theoretical category of the descended type

Write `D = C(G,omega,H,psi)` with `|G|=110`. The identity double-coset
sector is the ordinary representation category `Rep(H)`. A simple on
the double coset of g has dimension

`[H : H intersect gHg^{-1}] * dim(pi)`,

where pi is an irreducible projective representation of the intersection.
All subgroups of G have squarefree order. Such a group has trivial
Schur multiplier: restriction to a Sylow p-subgroup is zero, since that
subgroup is cyclic, and restriction followed by transfer is multiplication
by its index, prime to p, on the p-primary component. Therefore every
projective stabilizer representation has ordinary irreducible degrees.

The possible orders of H are `1,2,5,10,11,22,55,110`.

* Orders 5 and 11 give at least five invertibles. A group of order 55 is
  either cyclic or `C11 semidirect C5`, hence has at least five linear
  characters. All contradict the two invertibles of D.
* At order 22, the cyclic group gives too many invertibles; the dihedral
  group gives five dimension-two simples, more than D's two.
* At orders 1 and 2, the double-coset formula cannot give a dimension-five
  simple.
* At order 10, H must be the nonabelian group D10. The Sylow 11-subgroup
  K of G is normal, and `G=K semidirect H` since H is a complement. The
  action of D10 on K factors through its quotient C2, because `Aut(K)`
  is abelian. The characteristic C5 in H consequently centralizes K and
  is normal in G. Every intersection `H intersect gHg^{-1}` contains C5,
  and hence is either C5 or H. Its index in H is at most two, and the
  possible simple dimensions are one or two, never five.
* At order 110, H=G and D=Rep(G). Schur--Zassenhaus gives
  `G=C11 semidirect Q` for a group Q of order ten. If Q is cyclic, the
  quotient C10 gives at least ten linear characters. If Q is dihedral,
  its normal C5 centralizes C11, so G has an abelian subgroup C55 of
  index two. All irreducible representation degrees are then at most
  two. Both alternatives contradict the descended type.

Every case is impossible. This proves the claim for arbitrary complex
fusion categories, without an additional pivotality or unitarity assumption.

## Primary references and scope

* Etingof--Nikshych--Ostrik, *Weakly group-theoretical and solvable fusion
  categories*, [arXiv:0809.3031](https://arxiv.org/abs/0809.3031),
  Propositions 4.4 and 4.5; Theorem 9.2; and the references listed for the
  manuscript's half-partition proposition.
* Ostrik, *Pivotal fusion categories of rank 3*,
  [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Theorem 2.13 and
  Proposition 2.8, for induced-unit dimensions and the half-partition step.
* Gelaki--Naidu, *Some properties of group-theoretical categories*,
  [arXiv:0709.4326](https://arxiv.org/abs/0709.4326), for the double-coset
  and projective-stabilizer description (the manuscript's corresponding
  group-theoretical dimension formula).

The new ingredient is the descent to the impossible dimension-110 type.
The certificate alone checks finite tensor premises; the categorical
conclusion uses the argument and cited theorems above.
