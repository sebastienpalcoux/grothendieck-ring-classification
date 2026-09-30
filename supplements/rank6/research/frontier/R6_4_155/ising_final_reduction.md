# R6_4_155: canonical Ising extension and its relative center

Status: **unresolved**. This note gives necessary categorical structure,
not a realization or a nonexistence proof. Work with the pseudo-unitary
Galois representative C. The inherited pointed-center certificate supplies
central invertibles h,g with twists -1,i respectively, and

```
hX=X,  gX=Y=X*,  XY=1+h+4(X+Y),  X^2=g+hg+4(X+Y).
```

Put `d=4+3 sqrt(2)` and `delta=d/sqrt(2)=3+2 sqrt(2)`.

## The canonical twelve-simple extension

Choose a braided Ising category I with simples 1,psi,sigma. In
`Z(C tensor I)`, the object `h tensor psi^+` is a central boson.
De-equivariantizing C tensor I by its central Rep(C2) gives a
pseudo-unitary fusion category D of dimension `144+96 sqrt(2)`.

The standard orbit description gives twelve simples:

```
1,h,g,hg               dimension 1,
s,gs                    dimension sqrt(2),
X,Y                     dimension d,
P,Q,R,S                 dimension delta.
```

Here s is the image of sigma. The categories C and I embed fully
faithfully. The free modules on X tensor sigma and Y tensor sigma split
into P+Q and R+S, respectively; the C2 stabilizer has no nontrivial
projective obstruction because `H^2(C2,C*)=0`. Thus
`sX=P+Q` and `sY=R+S`.

Frobenius reciprocity and dimensions give
`sP=Ps=sQ=Qs=X` and `sR=Rs=sS=Ss=Y`. Consequently hP=Q;
choose R=gP and S=gQ. The full central lift of g descends through the
condensation. From `s^2=1+h` and `sP=Ps=X` one obtains

```
(1+h)P^2=X^2.
```

Nonnegative coefficient comparison now forces

```
P^2=a+2X+2Y = a+2s(1+g)P,       a in {g,hg},
P*=aP.
```

Indeed the h-orbits {g,hg}, {X}, {Y} account for the displayed terms;
all other h-orbits have zero coefficient in X^2. The two choices of a
are isomorphic as based rings, by interchanging g and hg. This determines
the entire fusion ring of D over its subring `Ising tensor C2`.

## The central lift is automatic

The opposite Ising factor in

```
Z(C tensor I)=Z(C) tensor I^+ tensor I^-
```

centralizes the condensation boson h tensor psi^+. It therefore descends
to a braided functor `J:I^- -> Z(D)`. This functor is fully faithful:
in the free-module adjunction for `A=1+(h tensor psi^+)`, the extra
summand has Z(C)-coordinate h, so supplies no morphisms between objects
of I^-. The underlying functor is exactly the Ising inclusion I into D
already described above. Equivalently these are local modules in the
standard center formula `Z(D)=Z(C tensor I)_A^0`.

Let `E=Z_I(D)`, the relative center over this Ising subcategory. The
central lift J gives a fully faithful tensor section `S:D -> E` of the
forgetful functor: for X in D and V in I, use the inverse of the
half-braiding of J(V) with X. The two half-braiding hexagons supply the
relative half-braiding and tensor axioms. Naturality implies every
D-morphism is an E-morphism between these lifted objects, which proves
fullness as well as faithfulness.

The canonical copy of `Z(I)=I^+ tensor I^-` in E has a full central
lift from `Z(I)^rev`. The restriction S(I) is one Ising factor; denote
the other by K. Then `K intersect S(D)=Vec`: if an object belongs to
both, its forgetful image lies in I, hence it belongs to S(I), and the
two factors of Z(I) meet only in Vec.

The central structure of K defines the tensor product functor
`K tensor S(D) -> E`. It is fully faithful. For simple objects k,k' in K
and x,x' in S(D), rigidity identifies its morphism space with
`Hom(k'^* k, x' x*)`; only tensor-unit summands can be common to these
two subcategories, giving exactly the product of the two original
morphism spaces. Finally

```
FPdim(E)=FPdim(I) FPdim(D)=FPdim(K tensor D),
```

so this fully faithful functor is an equivalence. Thus

```
Z_I(D) is tensor equivalent to K tensor D.
```

In particular the relative center has rank36 and a single necessary
based-ring type. With coefficient ring `B=Ising^2 tensor C2`, it is

```
E=B+BT,       T^2=G+2 sigma2(1+G)T,       T*=GT.
```

This construction requires no exchange autoequivalence of C and no
unitarity assumption. It does not turn D, its relative center, or their
necessary based rings into an independently constructed categorification
of C.

References: DGNO, *On braided fusion categories I*, arXiv:0906.0620,
for nondegenerate Ising factorization and central de-equivariantization;
Gelaki--Naidu--Nikshych, *Centers of graded fusion categories*,
arXiv:0905.3117, for relative centers and their dimension formula. The
pointed-center premise is the inherited R155 frontier certificate.
