# Independent audit: half-E6 central-fermion shear

Conclusion: **accept R9_2_96 and R9_2_1266 as unitary categorical models**.
The construction in `../models_restored/shear.md` was checked independently
at the action, fixed-object, tensor-product and duality levels. No unresolved
H²/H³ or multiplicity-two trace choice remains. The independent tensor
reconstruction `shear_replay.py` imports no phase-three model constructor and
matches all 729 coefficients for each ring; see `shear_replay.json`.

Let E be unitary half-E6 with central fermion f and simple x satisfying
x²=1+f+2x. The existence and central-fermion input were freshly checked against
Aasen–Lake–Walker, arXiv:1709.01941v2, Sections 7.1–7.2, in the preceding audit.
Work with the coherent sVec normal form of this central pointed subcategory.
This permits the multiplication f²=1 to be written strictly; it does not
assume a braiding on E.

On D=E⊠Vec(C2), F(Z,h)=(f^h Z,h), with tensorator moving f^k to the left past
Z by the inverse central half-braiding, is a genuine tensor autoequivalence.
The tensorator pentagon is exactly the central half-braiding identity together
with associative multiplication of the powers of f. Composing F twice gives
the identity object/morphism functor, with tensorator (−1)^(hk): its sole
additional interchange is the crossing of f^h and f^k, whose value is
c_(f,f)^(hk)=(−1)^(hk). This also agrees with direct restriction to sVec×Vec(C2):
on pointed degrees (p,h),(q,k), the tensorator is (−1)^(pk), and the square is
(−1)^(hk). All scalar pentagons and square equations on this pointed part are
checked independently in the replay.

For s=+i or −i, η_(Z,h)=s^h is a monoidal transformation F²→Id, because

    s^(h+k mod 2)(−1)^(hk)=s^h s^k.

Also Fη=ηF, since F preserves h and is complex linear. This is the full
nontrivial action coherence equation for C2, so both choices give actual
unitary categorical actions. There is no subsequent action obstruction to be
assumed zero.

The four fixed underlying simples are (1,0),(f,0),(x,0),(x,1), and there is one
free orbit {(1,1),(f,1)}. Each fixed simple has two equivariant structures:
a fixed-object obstruction is a nonzero complex scalar and has a square root.
The rank is therefore nine. The degree-zero subcategory has literally the
identity action and η=1, so its equivariantization is E⊠Rep(C2). Denote the sign
character by e, and the degree-zero lifts of x by a,ea. Then

    e²=f²=1, ef=fe,  fa=af=a,  a²=1+f+2a.

The essential nontrivial sign concerns the two odd lifts b,eb of (x,1).
For a normalized unitary intertwiner t:fx→x, put r=t c_x^(-1):xf→x.
Naturality of c_f with respect to t, and c_(f,f)=−1, give

    c_x(id_f⊗t)=−(t⊗id_f)(id_f⊗c_x),
    r(t⊗id_f)=−t(id_f⊗r).

Thus tensoring by f changes the odd equivariant structure on both the left and
the right. Precisely fb=bf=eb. This left/right calculation is needed; the claim
would not follow simply from commutativity of the underlying fusion ring.
It also proves that ef stabilizes b on both sides.

Let Y be the simple over the free orbit. Every invertible fixes it. Hence
rigidity gives Y²=1+e+f+ef. Forgetting equivariance, and applying the known
invertible permutations, force on both sides

    aY=Ya=b+eb,  bY=Yb=a+ea,  ab=ba=Y+b+eb.

For example f fixes a and interchanges b,eb, so the two odd coefficients of
ab must agree; their sum after forgetting is two. No trace on the
two-dimensional fusion space remains to be chosen.

The underlying object of b² is 1+f+2x in degree zero. Invariance under ef
forces its x contribution to be a+ea. The stabilizer of b is {1,ef}, so its
invertible contribution is 1+ef if b is selfdual, and e+f if b*=eb. These are
the only possibilities; the dual must lie over the same underlying (x,1).
They give

    b²=1+ef+a+ea,  or  b²=e+f+a+ea.

Finally both possibilities actually occur. If v is an equivariant structure
for η=i, then iv is one for η=−i, because F is complex linear. The tensorator
and unit equivariant structure are unchanged. The induced action on the
one-dimensional pairing Hom((x,1)²,1) is multiplied by i²=−1. This exchanges
its +1 and −1 eigenspaces, hence exchanges the occurrence of 1 in b² and in
b(eb). Thus the two coherent actions realize the two duality cases; it is not
necessary to choose a convention identifying a particular sign of i with a
particular case.

The independent replay constructs the products from these generator
relations, in a different basis order from `shear.py`, and obtains exactly
96 (selfdual odd lifts) and 1266 (paired odd lifts). All operations preserve
unitarity. No additional categorical hypotheses are required.
