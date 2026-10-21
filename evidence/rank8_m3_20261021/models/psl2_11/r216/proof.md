# A general dimension-216 obstruction

**Theorem.** No complex fusion category has type `(1,2;2,1;3,2;8,3)`.
This excludes R8_3_810, R8_3_812, R8_3_2492, R8_3_2494, R8_3_2620 and
R8_3_2622. The argument does not assume unitarity.

Use solvability and the cyclic-prime extension/equivariantization sequence
of Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion
categories*, Theorem 1.6, Definition 1.2(ii), and Proposition 4.4. All
dimensions below are Frobenius–Perron dimensions.

A final prime extension of C, dimension 216, would have neutral dimension
108 or 72. Neither has the form `a+4b+9c+64d`, where a is 1 or 2, b<=1,
c<=2 and d<=3. Thus C is D^{C2}: its two invertibles force the last
equivariantization prime to be 2. The base D has dimension 108.

In a cyclic-prime equivariantization, a fixed base simple of dimension e
gives p simples of dimension e, and a free orbit gives one simple of
dimension pe. Cyclic projective stabilizers have only one-dimensional
irreducibles. Base dimensions are rational algebraic integers, hence
integral. Applying this orbit rule forces exactly the two base types

    A=(1,3;3,1;4,6),  B=(1,3;3,1;4,2;8,1).

Neither admits a subcategory of dimension 54 or 36: enumerate
`a+9b+16c+64d`, with a=1 or 3 and the indicated bounds. Hence the last
step for D is a C3 equivariantization of a dimension-36 category E.
Type B is impossible, because its dimension-four simples must be fixed
base simples and would occur in multiples of three, whereas there are
two. Type A forces E to have type `(1,4;4,2)`; the three nonidentity
invertibles form one orbit under the actual C3 action on E. Consequently
their group is V4, not C4.

For either dimension-four simple X of E, reciprocity gives
`16=|Stab(X)|+4m`. The stabilizer order divides four, so it equals four.
Thus all four invertibles occur in XX*, and a noninvertible must occur
as well. The adjoint category E_ad therefore has dimension 20 or 36.
The dimension ratio E/E_ad is the order of the universal grading group;
20 does not divide 36. Hence E_ad=E and U(E) is trivial.

The final solvability step for E cannot be a nontrivial extension,
because its universal grading is trivial. Its last equivariantization
prime is 2, since the invertible group is V4. This supplies a Tannakian
Rep(C2) in Z(E) whose forgetful image is a nontrivial invertible of E.
Transport its nontrivial central simple under the actual C3 tensor action
on E. The resulting three central lifts lie over the three distinct
nontrivial invertibles and are all bosons (self-braiding +1).

The forgetful map Inv Z(E) -> Inv E is injective here. Its kernel is
Aut_tensor(Id_E), canonically Hom(U(E),C*), hence trivial. Therefore the
three lifts and the unit form a closed V4 subgroup: every product is
the unique lift of its underlying invertible. The quadratic self-braiding
form is identically one on this pointed braided subcategory. It is thus
Tannakian, giving a central Rep(V4) in E. De-equivariantization yields
`E=F^{V4}`, with dim(F)=9. The same rational-algebraic-integer argument
shows F is integral. Integral fusion categories of dimension p^2 are
pointed (the standard prime-square case of the prime-power theorem;
see ENO, *On fusion categories*, and EGNO, *Tensor Categories*).
Thus F=Vec_H^omega for H=C9 or C3^2.

Consider the V4 action on H. A nontrivial orbit of length two has cyclic
stabilizer C2, giving forbidden dimension-two simples in E. A nonidentity
fixed point has stabilizer V4. Its projective representation degrees are
either four copies of one (trivial multiplier) or one copy of two
(nontrivial multiplier): the latter follows directly from the twisted
group algebra of V4. The first option gives four extra invertibles, beyond
the four already arising from the fixed unit, and the second gives a
forbidden dimension-two simple. Therefore all eight nonidentity elements
of H lie in free orbits of length four. In particular, each nontrivial
element of V4 acts as a fixed-point-free involution on H.

An odd abelian group has only one fixed-point-free involution: if f^2=1
and f has no nonzero fixed point, then f+1 maps into the fixed subspace
because `(f-1)(f+1)=0`, so f=-1. Equivalently decompose using division
by two. Thus all three nonidentity elements of V4 would act by inversion,
contradicting the group law. This contradiction proves the theorem.

The fresh verifier checks every numerical branching gate, independently
enumerates fixed-point-free involutions on C9 and GL2(F3), and binds the
theorem to each source by recomputing its tensor hash and checking the
complete positive dimension character. All six source tensors have the
claimed type. The new certificate is freshly regenerated after the
workspace reset; no missing prior output is presumed.

Run `python -O evidence/rank8_m3_20261021/models/psl2_11/r216/verify_dimension216.py`.
Default mode compares the regenerated certificate; `--write` regenerates.
