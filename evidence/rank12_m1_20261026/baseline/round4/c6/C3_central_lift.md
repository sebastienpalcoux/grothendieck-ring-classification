# A forced central C3 lift for R12_1_561 and R12_1_628

This note proves a new necessary restriction, not yet a full exclusion.
The outstanding issue is isotropy of the resulting central C3. An unrestricted
claim that a nondegenerate central pointed category splits from a nonbraided
fusion category must not be used.

## Input and actual action

Write G=C6, H=<g^2>=C3. In both rings the noninvertibles form a free G orbit,
all basis elements commute, and

    rho^2 = t + sum_{g in G} g rho,
    t=1 for R561,  t=g^3 for R628,
    d=3+sqrt(10), d^2=1+6d, D=120+36sqrt(10).

The full tensor presentations and triviality of the universal grading are
checked in verify_C3_sections.py. Any complex category can first be replaced
by its pseudo-unitary Galois conjugate. The conjugation lemma proved in
R332_proof.md supplies a genuine H action, including for a nontrivial original
pointed associator. Since the ring is commutative, this action fixes every
simple isomorphism class.

## All possible equivariantized based rings

Put E=C^H. Every stabilizer is cyclic H, whose second cohomology with C* is
zero. Hence every simple of C has exactly three simple equivariant lifts,
all of the same FP dimension. E has 18 invertibles A and 18 noninvertibles.
Its pointed group fits into the central extension

    1 -> K=Hhat=C3 -> A -> C6 -> 1.

A central extension of a cyclic group is abelian: a lift of its generator and
the central kernel generate the total group. Thus A is C18 or C6 x C3, with
the evident quotient map to C6. The pointed action on noninvertibles is free
and transitive. Indeed, a stabilizer projects to a stabilizer of the original
free action, and a nontrivial kernel character changes the equivariant lift.

Choose one lift r of rho. There is an automorphism tau of A with r a=tau(a)r.
It induces the identity on A/K and fixes K (the kernel Rep(H) is central).
The unique invertible summand of r^2 and associativity give tau^2=1 because A
is abelian. Writing tau(a)=k(a)a with k(a) in K gives tau^2(a)=k(a)^2 a;
therefore k(a)=1, as K has odd order. Thus tau=id.

Replacing r by a kernel translate changes the invertible term t' of r^2 by a
square in K. Consequently it can be normalized to 1 in R561, or to the unique
involution z of A in R628. The remaining six terms of r^2 give a section
S of A->C6, exactly one element in each fiber, with

    r^2 = t' + (sum_{s in S}s)r.

Duality says r*=t'^-1 r, and imposes S*=t'^-1 S. This covers every fusion-rule
ambiguity coming from tensorators and equivariant structures.

For t'=1 there are nine sections in each group: the lifts of the identity and
of the involution are forced, and the lifts of exponents1 and2 determine their
inverse partners. For t'=z there are27 sections: the involution a -> z-a pairs
the quotient exponents as (0,3),(1,2),(4,5), and each pair has three choices.
The complete domain consists of72 sections in total.

## A character-norm obstruction removes every non-subgroup section

For a group character chi:A->C*, put

    epsilon=chi(t'),  s=sum_{a in S}chi(a),  h=s^2/epsilon.

The two extensions of chi to the based algebra send r to the two roots of
x^2-sx-epsilon. Their formal codegrees satisfy

    f_+ f_- = 18^2 (4+h).

Indeed f=18(1+epsilon^-1 x^2). Since S*=t'^-1S, h is real and nonnegative.
The global dimension of E is 3D=360+108sqrt(10), with norm12960, whose only
prime factors are2,3,5. Both (3D)/f_+ and (3D)/f_- must be algebraic integers
by spherical central induction. Therefore

    (3D)^2/[18^2(4+h)]

must be an algebraic integer. If the cyclotomic norm of4+h has a prime factor
p outside{2,3,5}, this is impossible: the numerator and18 are p-adic units at
every prime above p, whereas4+h is not. Passing to the compositum with
Q(sqrt(10)) cannot remove the negative valuation.

The replay uses exact remainders modulo Phi18 or Phi6 and exact resultants to
compute the norms for every character until it finds a witness. It finds:

| Ring | A | Sections | Arithmetic exclusions | Survivors |
|---|---|---:|---:|---:|
| R561 | C18 | 9 | 9 | 0 |
| R561 | C6 x C3 | 9 | 6 | 3 |
| R628 | C18 | 27 | 27 | 0 |
| R628 | C6 x C3 | 27 | 24 | 3 |

Every surviving section is a subgroup B of A and a complement to K. Thus its
based ring is the tensor product of the original rank12 ring and Z[C3].
This table is exhaustive, not a sampled search. Typical forbidden primes are
13,37,541; the certificates retain an individual character and exact norm for
each of the66 rejected sections.

## The adjoint subcategory gives a tensor section

For a surviving subgroup section, E_ad has precisely the simples
B union Br. The equation rr*=1+sum_{b in B}br generates them, and this set is
closed under multiplication and duality. The forgetful tensor functor
E_ad -> C maps these simples bijectively onto those of C and sends each simple
to a simple. It is therefore fully faithful and essentially surjective, hence
a tensor equivalence. This is stronger than a based-ring tensor decomposition
of E; it supplies an actual tensor section of E->C.

## Central lifts from the inner-action equivariantization

There is a canonical source of central objects in E. For h in H, an
equivariant lift of u_h has a half-braiding with an equivariant object (X,mu)
obtained from

    mu_h : u_h tensor X tensor u_h* -> X,

by tensoring with u_h and cancelling u_h* tensor u_h. Thus it is an isomorphism
u_h tensor X -> X tensor u_h. Its hexagon is exactly the monoidality of mu_h;
its compatibility with the H-equivariant structures is the action-coherence
identity. On the pointed H subcategory, choosing the lift is the usual choice
of a projective character for the twisted conjugation action. Because H is
cyclic, all these projective representations are one-dimensional and exist.
Multiplying the lift by a character in K preserves centrality. Equivalently,
this is the canonical central construction from the twisted double of the
pointed subcategory Vec_H^omega into Z(C^H).

All three equivariant lifts of each h are therefore central in E. Exactly one
lies in E_ad. These selected underlying lifts are closed under tensor product because E_ad
is a fusion subcategory and has exactly one lift over each h. Their half-braidings
restrict to E_ad. To check closure also AS CENTRAL OBJECTS, use U(E_ad)=1:
two half-braidings on a fixed invertible differ by a tensor automorphism of the
identity, and these are characters of the universal grading. Hence the
half-braiding on each underlying invertible is unique. Products of the selected
central lifts must therefore carry the selected half-braiding. This gives a
fully faithful braided central lift of H there.
Transport through E_ad equivalent to C gives an actual central pointed C3
subcategory of Z(C) whose forgetful image is the original H.

A braided pointed category of odd cyclic order3 has trivial ordinary pointed
associator. Thus the earlier possible nontrivial H3(C3,C*) restriction is also
removed, and the regular H algebra exists. The central braiding can still be
Tannakian or one of the two nondegenerate metric C3 braidings.

## What is proved and what remains

The old unproved premise "there is a central lift of C3" has been replaced by
an argument using an actual inner action and72 exact finite refinements.
If the forced lift is Tannakian, the prior rank4 de-equivariantization applies:

    X^2=1+3X+3gX (R561), or X^2=g+3X+3gX (R628),

and both are already excluded. The nondegenerate central C3 alternatives have
not been eliminated here. A proof must use the free action on ALL simple
objects, other specific fusion rules, or a valid categorical construction.
Plain Müger splitting cannot be invoked inside a nonbraided C.

The portable replay uses only frozen inputs, Python, and SymPy:

    PYTHONDONTWRITEBYTECODE=1 python -O verify_C3_sections.py

It runs in under a second, checks both original presentations and their adjoint
closures, regenerates all72 sections and exact norms, and certifies that the
only surviving sections are the six subgroup sections. No optimizer, external
repository import, unitarity assumption, or long computation is involved.
