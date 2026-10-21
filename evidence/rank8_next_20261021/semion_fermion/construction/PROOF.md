# An actual rank-eight Morita neighbour of the de-equivariantized GH(C8) category

This argument uses an actual algebra in an existing unitary fusion category.
It does not lift a permutation of modular data to a braided autoequivalence.
The final identification of its fusion tensor with the census is a separate
step in the model workstream.

Let C be the C2 de-equivariantization of the known generalized Haagerup
category for C8. Write its invertibles as g^i, i modulo 4, and its remaining
simples as g^i rho. Then

    g rho = rho g^-1,       rho² = 1 + 2 sum_i g^i rho,
    d(rho) = delta = 4 + sqrt(17).

Grossman–Izumi, [arXiv:1501.07679v2](https://arxiv.org/html/1501.07679v2),
equations(2.21)–(2.22), Example 4.4 and §6, supply the GH(C8) category and the
Q-system 1+rho before de-equivariantization. The strong tensor functor carries
it to a connected separable algebra A=1+rho in C; the image rho is simple.
Thus B=A-bimod(C) is an actual unitary fusion category, Morita equivalent to C.

## Complete free-bimodule rank alternatives

Let I(X)=A tensor X tensor A be free bimodule induction. Its forgetful Gram is

    K_ij = dim Hom_B(I(X_i),I(X_j))
         = [A X_j A : X_i].

Every simple bimodule occurs in some I(X), because the action map from the
free bimodule on its underlying object is a split epimorphism. The tensor-unit
bimodule A has restriction row a=(1,0,0,0,1,0,0,0), in source order
(1,g,g²,g³,rho,g rho,g² rho,g³ rho). Therefore the other rows give a nonnegative
integer Gram factorization of K-a^t a.

The residual has rank 4. Enumerating its 40 integer pivot vectors and then the
complete finite multiplicity box yields exactly seven row types and four
factorizations. Their possible dual ranks are6,8,9,11. The code applies no
numerical infeasibility inference. Simple bimodule dimensions are the
dimensions of their underlying objects divided by dim(A).

The unique rank-eight factor has forgetful rows

    (1,0,0,0,1,0,0,0),
    (0,0,0,0,1,1,1,1) twice,
    (0,0,0,0,2,2,2,2),
    (0,0,1,0,1,1,2,1) twice,
    (0,1,0,1,2,3,2,3),
    (1,0,0,0,3,2,2,2).

Its dimensions are

    1, (3+sqrt(17))/2 twice, 3+sqrt(17),
    (5+sqrt(17))/2 twice, 5+sqrt(17), 4+sqrt(17).

## The known center excludes ranks nine and eleven

The center of C has the modular data in Grossman–Izumi,
[arXiv:1906.07397v2](https://arxiv.org/abs/1906.07397), Definition 6.1 and §6.1.6,
identified with this actual center in Example 6.10 of the preceding paper.
The model workstream's exact comparator identifies every S and T entry.

Its complete twist-one support consists of

    0, pi, k_(2,2,+), k_(2,2,-), g_(1,1), g_(1,3).

The canonical Lagrangian algebra L=I_B(1) in this same center has unit
multiplicity 1 and satisfies normalized S L=L and T L=L. Write its coefficients
on that support as (1,p,x,y,z,w). The gamma row of S gives p=1, the unit row
gives x+y+2z+2w=6, and either k_(2,2) row gives
3(x+y)-2(z+w)=2. Hence

    p=1,             x+y=2,             z+w=2.

These yield exactly nine nonnegative integral vectors. The script checks every
one against all 22 rows of the exact S matrix, as well as complete twist-one
support. Consequently

    rank(B) = dim Hom(L,L)
            = 2+x²+y²+z²+w² ∈ {6,8,10}.

The rank identity also follows directly from induction–forgetful adjunction
and F I_B(1)=sum_X X X*. Together with the complete bimodule Gram, only ranks 6
and8 remain.

## The actual Q-system excludes rank six

Here the associator matters. In the endomorphism realization used by
Grossman–Izumi §6, C lies in End(M crossed C2), with implementing unitary
lambda satisfying lambda²=1. The extended endomorphisms satisfy

    rho'(lambda)=lambda,       alpha'_4=Ad(lambda),
    alpha_2(t_0)=t_4.

The Q-system A=1+rho' has nonzero rho' to rho'² vertex proportional to t_0.
Let beta be conjugation by alpha'_2. The generalized Haagerup relations give
beta(rho')=Ad(lambda) rho'. Identifying beta(rho') with rho' by the
intertwiner u=lambda has u tensor u=1, because rho'(lambda)=lambda. The
transported vertex is therefore

    alpha_2(t_0) lambda = t_4 lambda.

It is orthogonal to t_0: t_0* t_4 lambda=0 by the Cuntz isometry relations.
A unit-preserving object isomorphism between two algebras on 1+rho' acts by a
scalar on the simple rho' summand. Thus it can only rescale the vertex line.
The two orthogonal lines cannot be identified, so A is not isomorphic as an
algebra to g² A g^-2.

The rank-six Gram factor has precisely two invertible simples. In addition to
the tensor unit, the second has underlying object

    g² + g² rho = g² A.

If this bimodule existed, its right-module structure would be isomorphic to
the free simple right module g² A: adjunction gives a nonzero map from that
free module, and their dimensions agree. A left A-action on this invertible
bimodule would then give an algebra isomorphism

    A ≅ internalEnd_A(g² A) ≅ g² A g^-2.

This contradicts the vertex calculation. Equivalently, the standard
correspondence between invertible bimodules with underlying free rank-one
modules and algebra conjugacies gives the same conclusion. Hence rank six
cannot be the rank of the actual B.

**Conclusion:** the actual fusion category A-bimod(C) has rank eight and the
unique restriction/dimension data displayed above. Identifying its complete
fusion tensor requires the remaining fusion-coefficient bound and census
comparison; those are not inferred from modular data alone.

## Exact receipt

`r721_bimodule_rank.py` is self-contained for the Gram enumeration. It binds
the all-entry modular-data comparator and source, verifies source
associativity, exhausts the row/multiplicity boxes, checks all nine S-fixed
vectors, and records both rank cuts. Normal and `-O` outputs are identical.
The Q-system argument is a categorical proof using the explicit formulas,
not an assertion extracted from the arithmetic receipt.
