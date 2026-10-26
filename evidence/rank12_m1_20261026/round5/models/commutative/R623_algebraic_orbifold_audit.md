# Algebraic orbifold bridge for the new cyclic near-group precursor

The new primary source is He–Liu–Lu–Palcoux–Ren,
*Triangular prism equations for near-group categories: algebraic solutions
and a unitary conjecture*, arXiv:2610.11652v1, 8October2026:
https://arxiv.org/html/2610.11652v1.
This supersedes the earlier search statement that no order36 precursor had
been found. It constructs spherical near-group categories for every cyclic
order, and their pseudo-unitary Galois conjugates. Unitarity for arbitrary
order is not claimed and is not used below.

## The categorical construction to audit

Take its cyclic near-group category N for C36, with parameters in Eq2.19.
In the notation of Izumi1512.04288v2, Lemma2.14 of the new paper identifies

\[
\langle g,h\rangle_I=\chi(g,h)^{-1},\qquad a_I(g)=a(g)^{-1}.
\]

For H=<6> of order6, H=H-perp and a_I(6j)=(-1)^j. Thus g_a modulo H is
3, and Izumi's square formula has pointed term alpha(-g_a)=alpha(3).

The required construction is the category of modules for the central
separable algebra A=direct-sum(h in H) alpha_h. Its FP dimension is
FPdim(N)/6. It is important to construct this central algebra, rather than
merely apply a C*-theorem to a category whose unitarity is not established.

## Why the finite orbifold computation is algebraic

1. The pointed subcategory of the reconstructed near-group category is
   untwisted in the stated gauge. The noninvertible simple is fixed by the
   group. Inverses of the mixed vertices and bilinear dual bases can be
   used throughout. No positive inner product is needed for these choices.

2. Evans–Gannon, *Near-group fusion categories and their doubles*,
   arXiv:1208.1500, Section4.1 equations(4.6)–(4.10), writes the complete
   half-braiding equations on the generating vertices. Their Section4.3,
   equations(4.48)–(4.50), verifies that at multiplicity m=|G| each alpha_g
   has a unique central lift, with braiding on pointed objects given by
   the near-group bicharacter. This is the m=n calculation, not the
   distinct m=n−1 statement of Theorem5.

3. The identities in that check involve the bicharacter, mixed-vertex
   inverses, and the group actions on the multiplicity space. They are
   algebraic identities in the scalar data. The new paper Section4.7
   supplies precisely the required non-Hermitian interpretation: Eq4.56
   defines X,Z,Y,Q,B,R,A; Eq4.60 gives their group/corner transport; and
   Lemma4.14 proves consistency of all reflected tetrahedra by the
   parameter involution tau from Lemma2.13 and bilinear dual changes.
   Lemma2.14 supplies the parameter dictionary. Therefore the old
   half-braiding computation can be performed in this reconstructed
   spherical category using inverse and bilinear-dual vertices. One must
   not replace the new coefficients by their ordinary complex conjugates.

4. The braiding of these lifts restricts trivially to H×H, since H is
   bicharacter-isotropic. Their group multiplication is central by
   uniqueness of the lifts. The regular algebra A is consequently
   commutative in Z(N), and separable over C. Ordinary algebraic module
   category theory then produces the fusion category N_A.

5. Izumi1512.04288v2, Lemma12.2 and the proof of Theorem12.5, compute this
   category using character idempotents. The free image of the original
   noninvertible has endomorphism algebra C[H], hence splits into the six
   character summands. The left and right actions of alpha_g translate
   the character in opposite directions (the displayed equations just
   before Theorem12.5); this gives inversion mixed action.

6. On the pointed part of sigma^2, the projector is the Fourier average

   \[
   |H|^{-1}\sum_{h\in H}a_I(h)\langle h,g\rangle_I
       =1_{g+g_a\in H^\perp}.
   \]

   Thus the pointed support is the single coset -g_a when H=H-perp.
   The second character-projector calculation in the proof of
   Theorem12.5 gives each noninvertible coefficient |H-perp/H|=1.
   Every normalization involves a nonzero group order or a dual-basis
   pairing. The source's isometries can be replaced by inclusion/projection
   pairs; their orthogonality equations are algebraic splitting equations.
   No positivity or operator-algebra completion enters these rank and
   fusion-coefficient calculations.

The resulting presentation is therefore

\[
\alpha^6=1,\quad\sigma\alpha=\alpha^{-1}\sigma,\quad
\sigma^2=\alpha^3+\sum_{j=0}^{5}\alpha^j\sigma.
\]

This is the desired R623-type presentation. The project still needs its
usual exact based-ring binding to the stored R12_1_623 tensor before a
classification entry is changed. This note audits the algebraic extension
of the cited orbifold proof; it makes no unitary-model claim and provides
no model for the commutative561/628 rings.

Primary references read directly:

- https://arxiv.org/html/2610.11652v1, Lemmas2.13–2.14, Section4.7,
  Lemma4.14, and algebraic reconstruction.
- https://arxiv.org/pdf/1512.04288v2, Section12.1, Lemmas12.1–12.2,
  Theorem12.5, and Corollary12.7.
- https://arxiv.org/pdf/1208.1500, Section4.1 equations(4.6)–(4.10)
  and Section4.3 equations(4.48)–(4.50).
