# Uniform obstructions to several quantum constructions of R1154

These are obstructions to specified construction families, not an
exclusion of R8_3_1154. Put `phi=(1+sqrt(5))/2`, `d=phi^3=2+sqrt(5)`,
and `v=d^2=phi^6`. The target dimension is `D=60v`.

## 1. A general dimension test

Let C be nondegenerate braided, P a pointed nondegenerate braided
category of order N, and A a connected étale algebra in `C x P`.
If the category of all right A-modules has global FP dimension D, then

```
FPdim(A)=N FPdim(C)/D,
FPdim((C x P)_A^0)=D^2/(N FPdim(C)).
```

These are DMNO, arXiv:1009.2117v2, Lemma3.11 and Corollary3.32.
The second expression must be an algebraic integer. In particular, if
`FPdim(C)=c v`, where c is rational, then `3600/(cN)` is an integer:
v is an algebraic unit, so an algebraic integer times its inverse is
an algebraic integer, and a rational algebraic integer is integral.

For `C=SU(4)_6`, c=800, the required number is `9/(2N)`, impossible
for every positive integer N. For `C=SU(5)_5`, c=2000, it is `9/(5N)`,
also impossible for every N. Braiding reversal has no effect on the test.

## 2. Exact global dimensions

The quantum Weyl denominator formula gives

```
FPdim(SU(n)_k)= n(n+k)^(n-1)
 / product_(j=1)^(n-1) (2 sin(pi*j/(n+k)))^(2(n-j)).
```

At n+k=10, write `a_j=2 sin(pi*j/10)`. Then

```
a_1=phi^-1,  a_3=phi,
a_2^2=sqrt(5)/phi,   a_4^2=sqrt(5)*phi,
a_5=2.
```

For n=4 the denominator is `5 phi^-6`; for n=5 it is
`25 phi^-6`; for n=6 it is `500 phi^-6`. The numerators are
4000, 50000 and 600000, respectively. Thus

```
FPdim(SU(4)_6)=800v,
FPdim(SU(5)_5)=2000v,
FPdim(SU(6)_4)=1200v.
```

The standard primary reference for the formula is Coquereaux,
arXiv:1003.2589, §§2.1–2.2 and the SU(n) specialization in §4.
The exact verifier independently sums the squares of all simple-object
dimensions in each alcove and reproduces these values.

## 3. A stronger positive-coordinate test, including SU(6)_4

Suppose a Q-linear functional ell on the dimension field satisfies
`ell(1)=0`, and is nonnegative on all simple-object FP dimensions, with
equality only at invertibles. A rational-dimensional connected separable
algebra is then supported on invertibles. Each invertible occurs with
multiplicity at most one: its free module and the regular A-module are
simple, so free-module adjunction and Schur's lemma give
`dim Hom(g,A)<=1`. Hence `FPdim(A)<=|Inv(C)|`.

Tensoring with any pointed category P of order N preserves this property
and multiplies the bound by N. A braiding on P, when needed, only makes
the full-module fusion construction meaningful; the positive-coordinate
obstruction itself requires no nondegeneracy or unitarity.

For `SU(n)_(10-n)` with n=3,4,5,6, use the field basis
`1,phi,t,phi*t`, where `t=2cos(pi/10)` and `t^2=phi+2`.
The exact quantum Weyl product

```
dim(a_1,...,a_(n-1)) =
 product_(i<j) [a_i+...+a_(j-1)+j-i]/[j-i],
[m+1]=t[m]-[m-1], [0]=0,[1]=1,
```

enumerated over the complete alcove shows all three nonconstant field
coordinates are nonnegative. Their sum vanishes at exactly the n
invertibles. The complete alcove sizes are 36,84,126,126. This is an exact
rational calculation in a degree-four number field, not a numerical
positivity inference. The verifier and receipt accompany this note.

Consequently the following required rational algebra dimensions all
exceed the respective pointed-support bounds, for every N:

| Source tensored with pointed P of order N | Required FPdim(A) | Upper bound |
|---|---:|---:|
| SU(4)_6 | 40N/3 | 4N |
| SU(5)_5 | 100N/3 | 5N |
| SU(6)_4 | 20N | 6N |
| SU(3)_7 x Fib | 5N | 3N |
| E14 | 5N/3 | N |

For SU(3)_7 x Fib, the field-coordinate statement is the already checked
72-label calculation in the previous `QUANTUM_SUBGROUP_ROUTE.md`; it also
follows from the present positive-coordinate list and multiplication by
phi. Its dimension is300v. This extends the old N=1 obstruction to every
pointed factor.

For E14 use the actual rank-fourteen modular category newly constructed
in `../global/R189_RANK14_COROLLARY.md`. Its dimension is100v and its only
invertible is1. The displayed simple dimensions all have positive d
coefficient except the unit (using `d^2=1+4d`), so the criterion applies
directly. Thus the new category does not automatically provide an R1154
model after adjoining arbitrary pointed factors.

These results do not prohibit additional nonpointed factors, different
ambient categories, noncentral algebra constructions, neutral components,
or a sequence involving other categorical operations.

Run `python verify_r1154_quantum_extensions.py`.

Sources:
https://arxiv.org/pdf/1009.2117
https://arxiv.org/pdf/1003.2589
