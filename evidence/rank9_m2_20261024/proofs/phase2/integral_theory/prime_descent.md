# A preserved-central-subcategory obstruction in dimension 6p

**Theorem.** Let p>3 be a prime with p≡1 mod 6. A complex fusion category
cannot have all the following properties:

1. FP dimension 6p, invertibles {1,h}≅C2, and trivial universal grading.
2. Its simple dimensions are 1,1,2 and (p−1)/6 copies of 6.
3. h fixes every noninvertible simple.

**Proof.** Such a category C is integral. By Etingof–Nikshych–Ostrik,
*Weakly group-theoretical and solvable fusion categories*, Theorem 9.2,
it is group-theoretical. Every group of order 6p is solvable: its Sylow
p-subgroup is normal when p>6, and the quotient has order six. Thus C is
solvable by Proposition 4.5(i),(ii) of that paper.

Proposition 4.4 gives a construction by cyclic-prime extensions and
equivariantizations. The last nontrivial step cannot be an extension,
because U(C)=1. The only possible equivariantization prime is two,
because its character group embeds in the two invertibles of C. Therefore
C=E^{C2}, FPdim(E)=3p.

The orbit/stabilizer classification of equivariant simples, together with
H²(C2,C×)=0, shows that a simple fixed by tensoring with h forgets to a
free two-element orbit. Hence E has precisely three invertibles and
(p−1)/3 simple objects of dimension three. The outer C2 swaps the two
nonidentity invertibles, so its permutation on this group C3 is inversion.

For each dimension-three simple X of E, the number of invertible summands
of XX* is the size of its invertible stabilizer, either one or three.
The equality 9=|Stab(X)|+3m forces this size to be three, and m=2.
Consequently E_ad contains all three invertibles and at least one
dimension-three simple. If it were proper, its dimension would be a proper
divisor of 3p, since FPdim(E)/FPdim(E_ad)=|U(E)|. The possibilities 1 and 3
are too small, and p is not 3 mod 9 (indeed p is prime and not divisible
by three), whereas a subcategory containing all invertibles has dimension
3+9k. Thus E_ad=E.

Applying solvability again, E=(Vec_{C_p}^ω)^{C3}. The base has prime
dimension p and is pointed. Its C3 action is nontrivial (in fact free off
the unit), since the three invertibles of E already come from the unit
and all other simples of E have dimension three.

The central Tannakian Rep(C3) in E is unique: the kernel of the forgetful
map on central invertibles is Aut_⊗(Id_E)=Hom(U(E),C×)=1. Thus the outer
C2 action preserves this central subcategory. Equivariantizing it gives
a central Tannakian subcategory Rep(H) in C, where H fits into
1→C3→H→C2→1. Its action is inversion, so H=S3. Sequential central
de-equivariantization therefore expresses C=(Vec_{C_p}^ω)^{S3}, and its
restriction to the normal C3 is the nontrivial action just obtained.
But every homomorphism S3→Aut(C_p) kills C3, because Aut(C_p) is abelian.
This contradiction proves the theorem. It is independent of pivotality,
unitarity, and the pointed associator ω.

This is the dimension-186 argument already proved in the project's
rank-eight manuscript, made uniform in p. It is not claimed as a new
literature theorem or as a full classification of dimension-6p categories.

## Exact application

`R9_2_907` has p=37, dimensions (1,1,2,6,6,6,6,6,6), adjoint ring equal
to the whole ring, and h=1 fixes all seven nonunits. It is excluded in
general complex fusion-category scope. `verify_prime_descent.py` checks
the full source tensor, dimension identities, dualities, invertibles,
fixedness and adjoint generation, and writes the exact certificate.

## Primary references checked

- P. Etingof, D. Nikshych, V. Ostrik, arXiv:0809.3031v2,
  https://arxiv.org/pdf/0809.3031, Theorem 9.2, Proposition 4.4,
  Proposition 4.5(i),(ii), and Proposition 2.10.
- S. Burciu, S. Natale, *Fusion rules of equivariantizations of fusion
  categories*, arXiv:1206.6625, Section 2.
- V. Drinfeld, S. Gelaki, D. Nikshych, V. Ostrik, *On braided fusion
  categories I*, arXiv:0906.0620, Theorem 4.18 and Proposition 4.19.

The preservation/sequential-equivariantization step is the same one
spelled out in `manuscripts/rank8/paper/prime_and_hopf_proofs.tex`,
Proposition `prop:prime-r8`, for R8_2_808 at p=31.
