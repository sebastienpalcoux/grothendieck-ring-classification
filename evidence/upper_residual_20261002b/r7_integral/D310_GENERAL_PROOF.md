# R7_4_963: square-free dimension 310

The exact tensor has simple dimensions

\(1^2,2^2,10^3\), global dimension

\(310=2\cdot5\cdot31\), and no fusion subring dimensions other
than

\(1,2,10,310\). The verifier enumerates every dual-closed unital
subset and checks closure against all source coefficients.

By ENO Theorem 9.2 an integral fusion category of this square-free
dimension is group-theoretical. Write any proposed realization as

\(\mathcal C(G,\omega,H,\psi)\), with

\(|G|=310\) and

\(\delta\psi=\omega|_H\).
Its identity-double-coset subcategory has the representation ring of

\(H\) and dimension 
\(|H|\). Thus 
\(|H|=1,2,10,310\).
The standard double-coset parametrization gives dimensions

\[
[H:H\cap xHx^{-1}]\,\dim\pi,
\]

with 
\(\pi\) an irreducible projective representation of the indicated
intersection. This retains arbitrary 
\(\omega,\psi\).

If 
\(|H|=1\) the category is pointed. If

\(|H|=2\), each intersection has order one or two, its projective
representations have degree one, and every simple dimension is at
most two. Neither case has a dimension-ten object.

If 
\(|H|=10\), it must be the nonabelian group

\(D_{10}\): a cyclic 
\(H\) would already contribute ten invertibles. The identity
double coset then accounts for the two dimension-one and two
dimension-two objects of the census, so every outside double coset
must contribute only dimension-ten objects. An intersection of order
two yields dimension-five objects, and an intersection of order five
yields dimension-two objects. An intersection of order ten gives
projective degrees at most 
\(\sqrt{10}\), and cannot produce dimension ten. Therefore every
outside intersection is trivial.

The Sylow-31 subgroup 
\(N\) of 
\(G\) is normal, because its number divides ten and is congruent
to one modulo 31. Since 
\(H\) is a complement, 
\(G=N\rtimes H\). But 
\(\operatorname{Aut}(N)\) is cyclic, so the order-five commutator
subgroup of 
\(D_{10}\) acts trivially on 
\(N\). For any nonidentity 
\(x\in N\), this subgroup lies in

\(H\cap xHx^{-1}\), contradicting triviality of the outside
intersection. This elementary argument avoids any additional
Frobenius-group theorem.

Finally 
\(H=G\) implies 
\([\omega]=0\), and the category is equivalent to

\(\operatorname{Rep}(G)\).
Again 
\(N=C_{31}\) is normal, and the quotient of order ten splits by
coprime Schur–Zassenhaus. The quotient cannot be cyclic, as it would
provide ten linear characters. Thus it is

\(D_{10}\), acting on

\(N\) through a cyclic image of order at most two. On characters
of 
\(N\), an orbit of size two has stabilizer

\(C_5\), while an orbit of size one has stabilizer

\(D_{10}\). Since the extension splits and the characters of

\(N\) extend to their inertia subgroups, their corresponding
irreducible dimensions are at most two. This contradicts the
dimension-ten census simples.

Consequently no complex fusion categorification exists. The result
uses integrality to apply the square-free group-theoretical theorem;
it makes no unitarity or pivotality assumption. The standard
group-theoretical parametrization is also recalled in ENO
arXiv:0809.3031, proof of Lemma 9.5.
