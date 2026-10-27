# Test of the new symmetric étale-summand parity lemma

This addendum tests the following new lemma, whose general categorical
proof is being independently audited by the root agent: a selfdual simple
B occurring with multiplicity one in the canonical étale algebra I(1)
inherits a nondegenerate symmetric pairing, so any negative-indicator
selfdual simple in F(B) has even multiplicity.

**Result: no contradiction for R1154, R928, or R941.** The exact check
`distinguished_parity.py` runs in about one second. This addendum does not
assert a categorification or change any classification status.

## R1154: the full character calculation

For the unique surviving rank-ten normal form, use basis
(1,u,v,uv,x,ux,vx,uvx,y,vy). Its second indicators are

    (1,1,-1,-1,0,0,0,0,-1,1).

Let sigma exchange sqrt(5) with -sqrt(5), fixing i. If B_sigma is the
Galois image of the central tensor unit, the modular Galois/character
formula gives

    chi_E(F(B_sigma)) = f_E / sigma(f_E).

Solving these ten character equations gives the unique exact vector

    F(B_sigma) = 1+2x+2ux+2vx+2uvx+4y+4vy.

The verifier checks the ratio identity at every character, including the
four nonreal ones. In particular y has coefficient 4, not an odd
coefficient. The other negative objects v,uv are absent.

The same parity test passes for every other selfdual distinguished
constituent of I_B(1). Here is the full list of their restrictions:

| Distinguished constituent | Restriction vector |
|---|---|
| Unit | (1,0,0,0,0,0,0,0,0,0) |
| Galois unit | (1,0,0,0,2,2,2,2,4,4) |
| Real character with f=8 | (1,0,0,0,2,2,1,1,4,3) |
| First character with f=10 | (1,1,0,0,1,1,2,2,2,3) |
| Second character with f=10 | (1,1,0,0,1,1,2,2,2,3) |
| Character with f=40 | (1,0,0,0,0,0,1,1,0,1) |

The other four distinguished constituents come from nonreal characters
and are not selfdual; the lemma does not apply separately to them.

Here is a categorical way to recover the listed columns without a new
large enumeration. Under the equivariantization functor Q:B -> C,

    Q(1)=Q(u)=1, Q(v)=Q(uv)=g,
    Q(x)=Q(ux)=X4, Q(vx)=Q(uvx)=X5,
    Q(y)=X1+X2, Q(vy)=X6+X7.

Under the center Morita equivalence Z(B)=Z(C) tensor Z(S), an object
Z tensor t restricts under Q to F_C(Z) if t forgets to 1 in S, and to
g F_C(Z) if t forgets to s. This follows directly by taking the even
component of the bimodule A tensor (F_C(Z) tensor F_S(t)).

The only selfdual twist-one candidates for the displayed dimensions
with nonzero unit multiplicity come from source distinguished objects
A0,A1,A2,A4,A4,A3, respectively, tensored with either the unit or boson
of Z(S). In particular the source semionic packet cannot replace A2,
because its objects are nonselfdual. The possible additional high source
column of dimension D0/5 has neither unit nor g in its restriction, so it
cannot contribute a distinguished constituent after this transfer.
Selfduality in B requires equal coefficients on x,ux and on vx,uvx;
multiplicity one in I_B(1) fixes the coefficient of 1 to one. These
conditions and the five frozen source low columns force exactly the
vectors in the table. The verifier checks their Q-images explicitly.

All coefficients at negative-indicator indices v,uv,y are even. Thus
the stronger étale-summand lemma supplies no further obstruction here.

## R928 and R941

The established R928 indicator vector is

    (1,0,0,0,0,0,0,-1).

Only g=X7 is selfdual with negative indicator. Its action on the simple
basis is free. Frobenius reciprocity therefore gives

    [g:X tensor X*]=[g tensor X:X]=0

for every simple X. Consequently g is absent from F(I(1)) and hence
from every distinguished restriction. This proves uniformly that the
new lemma cannot find a negative constituent in any of these objects.

The established R941 indicator vector is

    (1,0,0,1,1,1,1,1).

There is no negative-indicator selfdual simple at all. Again this
particular obstruction cannot apply.

These are exact scoped negative results for the new criterion; they do
not suggest that other categorical obstructions have been exhausted.
