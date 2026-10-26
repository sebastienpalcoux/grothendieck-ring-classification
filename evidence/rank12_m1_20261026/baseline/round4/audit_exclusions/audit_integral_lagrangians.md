# Independent audit of the integral-Lagrangian extension lemma

I read `../root/integral_lagrangian_lemma.md` and checked its two potentially
delicate categorical premises independently. The proof passes, with the
explicit normalization and integrality explanations below.

## Canonical module dimensions and composition

The published Etingof--Nikshych--Ostrik paper, *Fusion categories and homotopy
theory*, https://ems.press/content/serial-article-files/36746?nt=1 , Section
2.5, defines canonical module-object dimensions by

    FPdim(internalHom(X,Y)) = d(X)d(Y).

Proposition 2.2 gives sum_X d(X)^2=FPdim(C), and Remark 2.3 characterizes the
normalization by positivity and the module action. For a transitive module
over Vec_G^omega associated with a subgroup N, all |G|/|N| simple objects
therefore have dimension sqrt(|N|).

Section 4.2, Proposition 4.13, explicitly uses multiplicativity of these
dimensions for the canonical functor into a relative tensor product of
invertible bimodule categories. Its proof applies without change to a
composable pair of Morita bimodules with different endpoint categories:
all endpoints are Morita equivalent and have equal global FP dimension.
Equivalently they are blocks in a common linking multifusion category.

In the root lemma all endpoints are pointed. Every simple in each of the
three module blocks consequently has constant dimension sqrt(n0), sqrt(n),
or sqrt(n'), respectively. The product of two nonzero composable simples
is nonzero. (Rigidity makes the middle unit a summand of X*X, so a zero
product would contradict the nonzero second object.) If its total simple
multiplicity is k, the exact equation is

    sqrt(n0*n) = k*sqrt(n'),  k a positive integer.

Thus an integral first Morita bimodule preserves the rational square class
of n, in particular the condition that n is a square. Applying the inverse
gives preservation of the subset in both directions. The center-action on
Lagrangians agrees with this composition of the associated module categories.
No arbitrary rescaling of module dimensions is being assumed.

## Integrality under categorical Morita equivalence

Here is a direct proof sufficient for the application. If C is integral,
every simple of Z(C) has integral FP dimension because its forgetful image
decomposes into objects of C and tensor functors preserve FP dimension.
For D Morita equivalent to C, Z(D) is braided equivalent to Z(C), hence is
integral. The induction functor I_D has

    FPdim(I_D(X)) = FPdim(D)*FPdim(X).

Its left side is an integer. FPdim(D)=FPdim(C) is an integer, so FPdim(X)
is rational; it is also an algebraic integer, hence is an integer. Thus D
is integral. This avoids trying to infer integrality from an arbitrary
decomposition under a dominant functor without justification.

In a faithful graded fusion category, the ordinary FP dimensions in a
component have squares summing to the neutral global dimension. They
therefore agree with the canonical module normalization above. An integral
graded category has integral Morita bimodule components in the precise
sense needed by the lemma.

## Odd invariant subset and group identifications

For A4 x C2 the only normal abelian subgroups of square order are the trivial
subgroup and the unique normal V4. The latter has exactly two ordinary
invariant alternating forms. If the twisted invariant-form set is nonempty,
it is a torsor under those two forms; otherwise it contributes zero. Thus
the integral Lagrangian subset always has size one or three. For SL(2,3),
the only normal abelian subgroups are 1 and its central C2; only 1 has square
order, giving a singleton integral subset. Every 2-group action preserving
either odd subset fixes a Lagrangian, so the extension criterion applies.

The graded Morita construction from a stable Lagrangian in the pointed
order-eight neutral category uses an actual algebra in that neutral
category. Its entire C3-graded dual is pointed, and its reverse algebra lies
in the neutral pointed component. Hence the resulting group Gamma has a
normal subgroup A of order eight and quotient C3. Schur--Zassenhaus splits
it. Among order-eight groups, only C2^3 and Q8 admit nontrivial order-three
automorphisms; their semidirect products are A4 x C2 and SL(2,3).

If the action on A were trivial, coprime Kunneth splits the associator on
A x C3 into its two factors. The reverse algebra is in the A factor. Taking
its dual therefore leaves the C3 factor untouched, while its A-factor dual
is the original pointed neutral category. This would make the original
dimension-twenty-four category pointed, contradicting its noninvertibles.

Finally a C2-equivariantization is Morita equivalent to its crossed product.
Applying the actual neutral Morita algebra gives a faithful C2 extension of
the pointed Gamma category. The whole category remains integral by the
center proof above, so its odd component preserves the odd integral-
Lagrangian subset. The resulting GT conclusion is valid for arbitrary
complex categorifications and includes nontrivial action coherence.

Result: PASS. The proof explicitly repairs the otherwise invalid implication
that an arbitrary equivariantization of a GT category is automatically GT.
