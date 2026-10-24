# Independent direct exclusion of R9_2_1487

**Accepted, with general complex scope through the audited signed Galois-PU
gate.** This proof needs no LP, trace packet enumeration or numerical solve.

Suppose C is a pseudo-unitary categorification. Its exact simple dimensions
in source order are

    1, 2+2sqrt(3), 2+2sqrt(3), 1, 1, 1, 2, 4+2sqrt(3), 4+2sqrt(3).

The duality exchanges b1,b2 and fixes all other basis elements. The real
scalar character

    χ=(1,2,2,1,1,1,2,−2,−2)

has formal codegree f=Σχ(bi)χ(bi*)=24. The distinguished simple Aχ in I(1)
therefore has dimension D/f=4+2sqrt(3), and its restriction contains the unit
once, because χ is one-dimensional.

This distinguished simple is selfdual. In detail, the central-character
formula says S_(Aχ,Z)=dim(Aχ)χ(FZ). Duality of the spherical S matrix gives
S_(Aχ*,Z)=S_(Aχ,Z*). Since χ(bi*)=χ(bi), the latter equals S_(Aχ,Z) for every
central simple Z. Nondegeneracy of S implies Aχ*=Aχ. This argument uses the
explicit dual-invariance of χ, so it does not assume unitarity of C or rely
on a numerical notion of reality.

Write F(Aχ)=Σvi bi. Then v0=1, all vi are nonnegative integers, and vi=vi*
by selfduality. The two large simples b7,b8 cannot occur, because either alone
already has the full dimension of Aχ and v0 contributes an additional one.
The coefficient of sqrt(3) in dim(F(Aχ)) then forces v1+v2=1. But b1*=b2
forces v1=v2. This is impossible.

`replay1487.py` independently checks all 81 character multiplicativity
identities, all 81 dimension multiplicativity identities, duality, the formal
codegree and global dimension. It also exhausts the six dimension-compatible
restriction columns with v0=1 and verifies that none is selfdual. No code from
the developing labelled-S implementation is imported. Results are in
`replay1487.json`.

The central-character identification was freshly verified from Deshpande,
https://arxiv.org/pdf/1611.04486 , Proposition 2.8 and Section 2.7. Distinguished
I(1) dimensions/multiplicities are the standard induction-codegree theorem
used and independently audited throughout the project. The gate file is
`phase2/signed/gate_R9_2_1487.json`; hence the contradiction rules out every
complex categorification, not only the pseudo-unitary ones.
