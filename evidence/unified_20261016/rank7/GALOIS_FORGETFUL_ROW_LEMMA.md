# Galois transport of complete forgetful rows

This is a necessary condition for a pseudo-unitary fusion category with
commutative Grothendieck ring. It does not construct a center or categorification.

Let C be such a category, with its canonical spherical structure, global
dimension D, characters chi_E of K(C), and formal codegrees f_E. Write F for
the forgetful functor from Z(C). Normalize the center S matrix by S_00=1/D.

Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
Section 2.3, immediately before Theorem 2.13 (printed pp. 5--6), defines
A_E in Z(C) by the equality of characters

    chi_E(F(A)) = S_(A,A_E) / S_(0,A_E).

Theorem 2.13 then identifies these A_E as precisely the multiplicity-one
constituents of I(1), and gives dim(A_E)=D/f_E. Consequently
S_(0,A_E)=1/f_E. Thus the displayed character identity is part of the
definition in the source, not an additional assumption about tube algebras.

Let sigma be a cyclotomic Galois automorphism and let pi_sigma and
epsilon_sigma(A) in {+1,-1} satisfy the standard normalized modular
Galois identity

    sigma(S_(A,B)) = epsilon_sigma(A) S_(pi_sigma(A),B).

Applying sigma to the character identity and using integral multiplicities
in F(A) proves

    chi_E(F(pi_sigma(A)))
      = epsilon_sigma(A) (f_E/f_(sigma E)) chi_(sigma E)(F(A)).       (1)

Here (sigma E)(x)=sigma(chi_E(x)); in particular
f_(sigma E)=sigma(f_E). The characters form a basis of the dual of
K(C) tensor C, so (1) uniquely determines the entire forgetful row of
pi_sigma(A), up to the modular sign. The result is stronger than the
dimension transformation alone.

For the central unit, the sign is positive. Indeed, the multiplicity
vector m of I(1) is integral and nonnegative and satisfies S m=m
(Ostrik Proposition 2.8). Galois conjugation gives G_sigma m=m, where
G_sigma is the signed permutation above. Its support is therefore
preserved with positive signs. In particular epsilon_sigma(1)=+1.
Thus the row v=F(pi_sigma(1)) is forced by

    chi_E(v)=f_E/f_(sigma E).                                      (2)

Character orthogonality gives the especially useful explicit formula

    v_i = sum_E chi_E(b_i*) / f_(sigma E).                          (3)

Every v_i must be a nonnegative integer, v_0=1, and this exact vector
must occur among the candidate I(1) rows with its required dimension.
For other rows, (1) can be reconstructed with

    (T_sigma)_(i,j)
      = sum_E chi_E(b_i*) chi_(sigma E)(b_j) / f_(sigma E),

so v(pi_sigma(A))=epsilon_sigma(A) T_sigma v(A).
All coefficients of T_sigma are rational: the character values lie in a
cyclotomic field, whose abelian Galois group permutes the summands and
commutes with sigma. This rationality does not assert integrality of
T_sigma on arbitrary lattice vectors; integrality on actual forgetful
rows is precisely a necessary condition.

No involutivity of the full permutation pi_sigma is assumed. If sigma
acts as an involution on the character field, then T_sigma is involutive;
the full modular permutation can still have a larger order.

Source checked directly: https://arxiv.org/pdf/1309.4822,
Proposition 2.8, Example 2.9, and the definition preceding Theorem 2.13.
Independent audit: rank6_center, 2026-10-16.
