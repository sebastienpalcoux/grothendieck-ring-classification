# A common Galois pseudo-unitarity reduction for three rank-seven rings

**Proposition.** Every complex fusion categorification of R7_4_106,
R7_4_2155, or R7_3_146 is Galois conjugate to a pseudo-unitary category.
This is a reduction of scope, not an exclusion or construction.

## The positive involution quotient

In all three source rings the nontrivial invertible g exchanges two
pairs {a,ga}, {b,gb} and fixes a single remaining simple f. In the first
and third rings all simples are self-dual. In R7_4_2155, a*=ga and the
others are self-dual. Use source labels

| Ring | g | a | b | f |
|---|---:|---:|---:|---:|
| R7_4_106 | 1 | 2 | 3 | 6 |
| R7_4_2155 | 3 | 1 | 5 | 4 |
| R7_3_146 | 1 | 2 | 3 | 6 |

Pass to the canonical sphericalization of a hypothetical category, and
then to its signed based algebra T at epsilon=-1. Choose the lift of g
with spherical dimension +1. Then g^2=1: the other possible lift of the
unit has dimension -1. Similarly g is central in the signed based
algebra, since its left and right products have the same underlying
simple and the same nonzero spherical dimension. Its product with the
chosen lift of f is exactly f. Choose the other lifts in pairs so that
g a=ga and g b=gb with positive coefficient.

Take the algebra quotient T/(g-1). Its basis is 1,a,b,f. Its duality is
trivial, including when a*=ga before taking this quotient. Therefore
it is commutative. Frobenius reciprocity gives the following complete
form of its multiplication:

    a² = 1 + A a + B b + r f,
    ab = B a + C b + w f,
    b² = 1 + C a + D b + z f,
    af = 2r a + 2w b + l f,
    bf = 2w a + 2z b + m f,
    f² = 2 + 2l a + 2m b + n f.

Equivalently, the symmetric coefficient pairing has weights 1,1,1,2
on 1,a,b,f. The factors of two come from the two representatives in
each free orbit; they must not be omitted.

Every coefficient is an integer of the parity of the corresponding
source coefficient or sum, and its absolute value is at most that
source bound. In the parameter order (A,B,C,D,r,w,z,l,m,n), the bounds
are

    sqrt(3) pair: (0,3,4,8,1,2,4,2,3,4),
    sqrt(6) case: (3,3,4,4,2,2,2,2,3,2).

Changing signs of a,b,f allows A>0 whenever A is odd, B>0 in both
families, and r>=0; when r is odd, r>0. The coefficient A is zero in
the sqrt(3) family. These normalizations lose no candidate quotient.
They need not remove every duplicate: the first family retains two
sign-equivalent final rows.

## Six associativity equations

Commutation of the three multiplication matrices is equivalent to

    AC - B² + BD - C² + 2rz - 2w² + 1 = 0,
    Al + Bm - l² + nr - 2r² - 2w² + 1 = 0,
    Aw - Br + Bz - Cw - lw + mr = 0,
    Bl + Cm - lm + nw - 2rw - 2wz = 0,
    Bw - Cr + Cz - Dw - lz + mw = 0,
    Cl + Dm - m² + nz - 2w² - 2z² + 1 = 0.

The bounded integer solutions are very small: there are eight normalized
quotients for the sqrt(3) pair and eleven for the sqrt(6) case. These
lists can be obtained by substitution: since B is 1 or 3, the first
equation determines D; if r is nonzero, the third and second determine
m and n respectively. If r=0, only the displayed small m,n domains
remain. The verifier lists every solution and checks all matrix products.

## The global dimension is a root of one explicit four-by-four matrix

Let delta be the global dimension of the original category. The signed
dimension character takes g to 1 and thus factors through this quotient.
Writing its values on a,b,f as u,v,w0, the dimension of the seven-simple
category is

    delta = 2 + 2u² + 2v² + w0².

This remains true in R7_4_2155 because a*=ga has the same signed
dimension. Consequently delta is an eigenvalue of

    Q = 2 I + 2 M_a² + 2 M_b² + M_f².

Induction to the center of the sphericalization makes delta/f_E an
algebraic integer for every source formal codegree f_E: the dimension
and the epsilon=+1 formal codegrees are both doubled, so the two
factors cancel. In particular

    f_E = 48(7+4 sqrt(3))   in the first family,
    f_E = 48(5+2 sqrt(6))   in the second.

The expressions in parentheses are algebraic units (each has norm 1).
Multiplying delta/f_E by that unit proves the crucial condition

    delta/48 is an algebraic integer.

The rational formal codegrees alone have least common multiple 24 and
would not give this stronger condition.

For each of the nineteen small quotients, factor det(xI-Q) over Q. For
an irreducible factor p(x), a root delta can have delta/48 integral if
and only if the monic polynomial proportional to p(48x) has integral
coefficients. Only the following rows survive:

| Family | (A,B,C,D,r,w,z,l,m,n) | possible factor for delta |
|---|---|---|
| sqrt(3) | (0,3,-4,8,1,-2,4,-2,3,4) | x²-672x+2304 |
| sqrt(3) | (0,3,4,8,1,2,4,2,3,4) | x²-672x+2304 |
| sqrt(6) | (3,3,4,4,2,2,2,2,3,2) | x²-480x+2304 |

Thus

    delta = 336 +/- 192 sqrt(3), or
    delta = 240 +/- 96 sqrt(6),

respectively. These are exactly the source Frobenius–Perron dimensions
and their conjugates. If delta is the positive Frobenius–Perron value,
the category is pseudo-unitary by definition. Otherwise extend the
nontrivial quadratic Galois automorphism to a number field of definition
of the fusion category. Global dimension is Galois-equivariant and the
based ring is unchanged. The conjugated category then has global
dimension equal to its Frobenius–Perron dimension, hence is pseudo-unitary.
This proves the proposition without initially assuming any pivotal
structure.

## What this resolves and what it does not

The three general categorifiability questions are now equivalent to
existence of pseudo-unitary categorifications. They remain unresolved.
Their full-induced-unit compression quantity equals one, which satisfies
the necessary bound. Equality does not put the entire S-image of the
quadratic Galois vector in the twist-one subspace: only its projected
squared norm saturates the local bound. No contradiction follows solely
from that equality or from the pseudo-unitarity reduction.

## Inputs and references

The finite inputs are rederived from the original census by
`verify_three_case_galois_pu.py`; the complete normalized quotient lists,
polynomials, and source hashes are included in its receipt. This is a
bounded symbolic verification of the displayed algebraic calculation,
not a numerical associator search.

The categorical inputs are the canonical sphericalization theorem and
Ostrik's induced-unit/formal-codegree integrality theorem, as used in the
existing manuscript's signed quotient criteria. For global dimension,
pseudo-unitarity, and algebraic number fields of definition, see
Etingof–Nikshych–Ostrik, *On fusion categories*, and EGNO, *Tensor
categories*, Sections 9.5–9.6. The latter is available at
https://math.mit.edu/~etingof/egnobookfinal.pdf.
