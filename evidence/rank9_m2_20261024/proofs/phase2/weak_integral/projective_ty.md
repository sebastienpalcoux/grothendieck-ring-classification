# A parity-coherence equivariantization family

**Conclusion.** `R9_2_21` is the Grothendieck ring of a unitary fusion category.
The construction below applies uniformly to every odd integer p>=3. It is new
as an application to this ledger, not a claim of priority for equivariantization.

Let C=TY(C_p,chi,tau), where chi(x,y)=exp(2 pi i xy/p) and tau=1/sqrt(p).
Write m for its noninvertible object. The inversion s:x->-x, m->m preserves
chi. The standard orthogonal action gives a C2 action by unitary tensor
functors, with the usual summand permutations on m tensor m. See Gelaki,
Naidu and Nikshych, *Centers of graded fusion categories*, arXiv:0905.3117,
Proposition4.8 (the orthogonal group action).

There is a unitary monoidal natural automorphism e of the identity functor
which is +1 on every x in C_p and -1 on m. Monoidality follows directly from
the C2 grading: even-even and odd-odd products are even; mixed products are
odd. The inversion action fixes e.

Put G=C2 x C2, written g=(a,b), and first pull back the inversion action by
(a,b)->a. Modify its composition constraint F_g F_h -> F_(g+h) by

    eta(g,h)=e^(b*c),  g=(a,b), h=(c,d).

This still defines a genuine categorical G action: the modification satisfies
the pentagon because b*c is a normalized C2-valued group 2-cocycle. Explicitly,
b*c+(b+d)*u = d*u+b*(c+u) mod2 for h=(c,d), k=(u,v). Thus this is a construction
of associators through equivariantization, not merely an associative based ring.
All functors, tensorators and coherence modifications are unitary.

Consider C^G. On the pointed part the modification is trivial, so the integral
subcategory is (Vec_Cp)^G = Rep(C_p semidirect G), using the character-group
identification C_p~=C_p-hat. The action of G on C_p is inversion by its first
factor, hence this is Rep(D_(2p) x C2), where D_(2p) denotes the dihedral group
of order 2p. For odd p it has four invertible simples and p-1 simples of
dimension 2.

The orbit of m is a singleton. Its stabilizer multiplier is
beta((a,b),(c,d))=(-1)^(b*c), up to inversion (which is identical here).
The twisted group algebra has generators U,V with U^2=V^2=1 and UV=-VU;
it is M2(C). Consequently there is exactly one irreducible beta-projective
representation, of dimension2. Hence C^G has exactly one remaining simple
M, whose FP dimension is 2sqrt(p). Every even simple X satisfies
X tensor M = M tensor X = FPdim(X) M, since there is only one odd simple.
The dual of M is again M. Frobenius reciprocity gives

    M tensor M = sum_(X even) FPdim(X) X.

These formulas determine the entire ring. Its rank is p+4, dimension 8p,
and maximum structure constant is2. For p=5 its dimensions are
(1,1,1,1,2,2,2,2,2sqrt5), global dimension40 and rank9.

`projective_ty.py` constructs the even tensor independently as the Deligne
product of the explicit dihedral character-ring formula and Rep(C2), adjoins
M by the displayed rule, checks the fusion axioms, checks the cocycle and
nondegeneracy, and compares all 729 tensor entries after an explicit
unit-preserving basis permutation. The unique match among the 81 input
survivors is R9_2_21, with source-to-model permutation

    [0,1,3,5,7,6,4,2,8].

The exact certificate is `models.json`. No numerical matching or unproved
braiding assumption enters the construction.
