# R8_2_312: a Galois-invariant pointed associator obstruction

## General necessary criterion

Let D be a two-dimension fusion ring: every simple has Frobenius--Perron
dimension1 or the same d>1. Suppose every pseudo-unitary categorification
of D restricts on a specified order-two invertible g to the nontrivial
pointed associator class in H^3(C2,C*)=C2. Then every complex
categorification of D has that same nontrivial restriction.

Indeed, the published Lemma3.1 of Schopieray, *Categorification of integral
group rings extended by one dimension*, Journal of the London Mathematical
Society108(4),2023, DOI10.1112/jlms.12789, says that any categorification
of a two-dimension ring is Galois conjugate to a pseudo-unitary fusion
category. It does not assert that the original categorification is itself
pseudo-unitary. Galois conjugation preserves the based ring and its
distinguished order-two invertible. A normalized3-cocycle on C2 is
represented by the scalar omega(g,g,g)=+1 or-1. Every field automorphism
fixes these scalars. Consequently the trivial and nontrivial classes are
separately Galois invariant, giving the assertion.

If such D is a fusion subcategory of C and C has a simple M fixed by g,
then C cannot exist. The one-object orbit {M} is a rank-one module category
over Vec_C2^omega. Choosing an isomorphism gM -> M identifies the module
associativity with a scalar2-cochain psi, and the module pentagon gives
dpsi=omega. Hence a rank-one module exists only when [omega]=0,
contradicting the preceding invariant restriction. This argument does not
need a pivotal structure on C or simultaneous Galois conjugation of its
other subcategories.

## The pseudo-PSU(2)_6 restriction

The rank-four pseudo-PSU ring has basis1,g,x,y, with

    g^2=1, gx=xg=y, gy=yg=x,
    x^2=y^2=g+x+y, xy=yx=1+x+y, x*=y.

Its dimensions are1,1,d,d, with d=1+sqrt(2); all64 dimension products
are checked in the adjacent source verifier. Thus Schopieray's lemma
applies to an arbitrary categorification of this subring.

Larson, *Pseudo-unitary non-self-dual fusion categories of rank4*,
arXiv:1401.1879, Section5, Proposition5.5 and the Case1 contradiction
in the proof of Theorem5.8, proves that for the case c=1 the canonical
pseudo-unitary second indicator of g is-1. More explicitly, the twists
of the four summands of I(g) have square nu2(g). The branch nu2(g)=+1
is theta=1 and is impossible even for c=1: a required sum needs at least
eight roots of unity although at most seven are available. Therefore
nu2(g)=-1.

The canonical pseudo-unitary pivotal structure restricts on a pointed
subcategory to dimension1 on both objects. In Vec_C2^omega with this
structure, the elementary indicator formula is

    nu2(g)=omega(g,g,g).

One may alternatively evaluate the single rotation on Hom(1,g*g)
directly. Thus Larson's negative indicator is exactly the nontrivial
H^3(C2,C*) associator class. The general criterion transports this
intrinsic associator restriction through Galois conjugation.

## Census application

`verify_r312.py` rereads the complete pinned rank-eight census, locates
the pseudo-PSU subring by a full coefficient-preserving injection, and
exhibits an outside simple fixed by its g. The recovered source has
pseudo subring[0,7,1,2] and fixed simples[3,4,5,6]. These assertions
are checked from the tensor, not assumed from the prose.

Hence **R8_2_312 admits no fusion-category categorification over C**.
In particular it admits no pivotal, spherical, pseudo-unitary, unitary,
or braided categorification. The proof uses the published corrected
Galois-conjugacy statement and does not confuse it with a universal
pseudo-unitarity assertion.

## Primary sources

- Schopieray, https://doi.org/10.1112/jlms.12789, published Lemma3.1.
- Larson, https://arxiv.org/pdf/1401.1879, Proposition5.5 and Theorem5.8.
- Ng--Schauenburg, https://arxiv.org/pdf/math/0601012, second indicators
  of spherical pointed categories and the center indicator formula.
- EGNO, https://math.mit.edu/~etingof/egnobookfinal.pdf, classification
  of module categories over pointed fusion categories.
