# R623: a forced central semion, central-lift restriction

This is a necessary restriction, not a full exclusion. It strengthens the
previously proved nontrivial pointed C2 associator condition. The central-lift
construction is the same one detailed in C3_central_lift.md. It does not supply
a full exclusion, and no online classification depends on it.

Let C be the pseudo-unitary Galois conjugate of a hypothetical category for
R12_1_623. Its fusion rules are

    G=C6=<g>, z=g^3, rho g=g^-1 rho,
    rho^2=z+sum_{g in G}g rho, rho*=z rho.

Conjugation by z fixes every simple and defines a genuine C2 action, including
for the forced nontrivial pointed associator. Put E=C^<z>. Each simple has two
equivariant lifts, so E has12 invertibles and12 noninvertibles. The kernel
K=Rep(C2) acts freely on these lifts.

## Its pointed extension is split

The pointed part C_pt is Vec_C6^omega. Since C6=C3 x C2 and the factors have
coprime orders, its associator class is a product of classes on C3 and C2.
Thus, as a pointed fusion category, it is a Deligne product
Vec_C3^omega3 tensor Vec_C2^omega2. The inner C2 action acts trivially on the
first factor and is the canonical conjugation action on the second. Its
pointed equivariantization is

    Vec_C3^omega3 tensor Z(Vec_C2^omega2).

For both classes omega2, the twisted double has pointed fusion group C2 x C2:
toric code for the trivial class, double semion for the nontrivial class.
Hence the12 invertibles of E form A=C6 x C2, with kernel the second C2 and
quotient the original C6. The alternative abstract extension C12 is unavailable.

## Complete fusion-rule refinement

Choose a lift r of rho. Write its right pointed action as r a=tau(a)r. Since
it projects to inversion on C6 and fixes the central kernel, its two possible
forms are

    tau(a,b)=(-a,b+epsilon*a), epsilon=0 or1,

in additive coordinates modulo6 and2. Its unique pointed square term is one
of t'=(3,0),(3,1). Associativity forces tau(t')=t', so epsilon=1 is impossible.
Thus tau is inversion on A.

The six noninvertible terms in r^2 form a section S of A->C6, and

    r^2=t'+(sum_{s in S}s)r.

Associativity of r^2 with each a in A forces S invariant under (tau-id)A=2A,
the order-three subgroup. Associativity with r gives tau(S)=S, and duality gives
S*=t'^-1S. There are only64 initial sections for each t'. Exhausting these
conditions gives two survivors in each case, related by translating by K.
Changing r by the kernel invertible translates S in precisely this way, so
S can always be normalized to a subgroup B complementary to K and containing
t'. Explicitly B is either {(a,0)} or {(a,a mod2)}.

The adjoint fusion subcategory E_ad has exactly B union Br. The forgetful
functor maps its simples bijectively to those of C; hence E_ad -> C is a tensor
equivalence. In particular, this conclusion is categorical, rather than a
claim that a based-ring product automatically supplies a tensor factorization.

## The semionic central lift

Every equivariant lift of z has a central half-braiding in E obtained from the
equivariant structure mu_z of each object. The unique one belonging to E_ad
therefore transfers to a central lift of z in C. It has order two as a central object: its underlying object has order two,
and U(E_ad)=1 makes the half-braiding on each fixed underlying invertible unique.
Thus its central square is the canonical central unit.

The previously audited indicator argument proves nu_2(z)=-1. In the canonical
pseudo-unitary pivotal structure this is equivalent to the nontrivial pointed
associator on <z>. A braided central lift of this order-two pointed category
must have semion or reverse-semion braiding, with twist +i or-i. It cannot be
Tannakian or fermionic. This statement concerns the pointed associator and
must not be confused with the known central fermion in R326, where nu_2(z)=+1.

Thus a remaining category for R623 would have a central semion with underlying
invertible z, acting freely on all simples and satisfying rho*=z rho. A further
argument excluding that configuration would complete this case. Ordinary
Müger splitting inside C is not available because C is not braided. No such
splitting is assumed here.

Portable exact replay:

    PYTHONDONTWRITEBYTECODE=1 python -O verify_R623_C2.py

It checks all source tensor products, both possible pointed square terms,
both possible lifted actions, and all64 sections per fixed-term action.
