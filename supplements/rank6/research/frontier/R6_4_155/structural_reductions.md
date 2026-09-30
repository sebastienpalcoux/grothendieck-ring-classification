# R6_4_155: no braided Morita representative

Status: **unresolved**. The statements below are necessary structural results,
not a categorification or a nonexistence proof. They use the previously certified
six-profile reduction only where explicitly stated.

Write the simple objects as `1,h,g,hg,X,Y`, where `Y=X*`, `hX=X`, `gX=Y`,

```
XY = 1+h+4(X+Y),       X^2 = g+hg+4(X+Y).
```

Thus `d=4+3 sqrt(2)` and `FPdim(C)=72+48 sqrt(2)`. Pass to the
pseudo-unitary Galois representative by the independent uniform argument in
`structural_note.md`.

## Central lifts

The adjoint category is all of C: the product `XY` contains `h,X,Y`, and
`X^2` then contains `g,hg`. Therefore the universal grading group is trivial
and `Aut_tensor(Id_C)=1`.

Any two half-braidings on the same invertible object differ by a tensor
automorphism of the identity. Consequently a central lift of an invertible
object, when it exists, is unique. The certified six-profile result gives
central lifts of all four invertibles and, after complex conjugation,

```
q(1)=1,       q(h)=-1,       q(g)=i,       q(hg)=-i.
```

Their braided pointed subcategory is therefore `Semion tensor sVec`, with
the indicated based identification. The restriction of its associator to
`<g>` and to `<hg>` is the nontrivial class in `H^3(C2,C^*)`.

## Morita obstruction

In fact, C cannot be Morita equivalent to **any braided fusion category**.
The pointed-center group is exactly V4: injectivity proved above bounds
its order by four, and the inherited certificate supplies all four lifts.
Suppose M were a braided Morita representative. Categorical and
Frobenius--Perron dimensions are Morita invariant (EGNO, Proposition 9.3.9
and Corollary 7.16.7), so M is pseudo-unitary. Equip both centers with
their canonical positive spherical structures. The braided equivalence
`Z(M)=Z(C)` preserves these structures by uniqueness (EGNO, Proposition
9.5.1), hence preserves twists.
Every invertible in the kernel of the forgetful map
`Inv(Z(M)) -> Inv(M)` has underlying tensor unit and therefore twist 1.
Since the displayed pointed quadratic form has no nonidentity object of
twist 1, that forgetful map is injective.

Let a underlie the central semion g. The braiding of M and its reverse
supply central lifts `(a,c_{a,-})` and `(a,c_{-,a}^{-1})`. Injectivity
forces both lifts to equal g. Thus a is transparent in M and has
self-monodromy 1. The semion lift has self-monodromy -1, a contradiction.
This covers degenerate braided M as well.

For an arbitrary categorification, transport a hypothetical braided
Morita representative and its Morita data through the same Galois
conjugation used to reach the pseudo-unitary representative. The braiding
and module-category coherence equations are preserved. The contradiction
therefore excludes braided Morita representatives of every general
categorification. It does not exclude unbraided categorifications.


Reference: Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Propositions 9.3.9 and 9.5.1 and Corollary 7.16.7. The four pointed lifts and their twists are supplied by the inherited exact induction-profile certificate.
