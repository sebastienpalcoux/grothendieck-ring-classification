# Independent audit: R7_4_2019

The proposed model is mathematically valid, subject to the final producer bundle using the stated cohomology class and subgroup trivialization.

Let Q8 act on C² through its standard quaternion representation. InsideU(2) set r=−(1+i+j+k)/2 and s=i_scalar(i−j)/sqrt2. An exact matrix check verifies r³=s²=1, srs=r^−1, and conjugation by r cycles the quaternion axes, while conjugation by s is their signed transposition. The subgroupH=<r,s> is S3, its intersection withQ8 is trivial (nonidentity3-cycles have order3 and odd elements have determinant−1), and G=Q8⋊S3 hasorder48. The restricted representationR=V|H is the standard2-dimensional S3 representation with determinant the sign character.

Define Ω=c2(V)−infl_H^G(c2(R))∈H⁴(BG,Z)=H³(G,U(1)), where inflation is along G→H. Its restriction toH is0. Let z=−1∈Q8, and x=c1(L) for the nontrivial character of<z>. On <z>×H the representation is L⊗R. The Chern-class tensor formula gives

Ω|<z>×H=x²+x c1(R)=x²+xy,

where y is the sign-character class. An explicit normalized U(1)3-cocycle representing this restriction is

ω((a,g),(b,h),(c,k))=(-1)^(abc+a p(h)p(k)).

It is trivial onH. The global representative can be adjusted to restrict to exactly thisω: extend a correcting2-cochain from<z>×H toG. Then choose subgroupcochainψ=1. Thus the group-theoretical fusion category C(G,Ω,H,1) exists. It is unitarizable (indeed group-theoretical); no modular-data sufficiency is asserted.

The standard induced action formulas on the central grades give tensoratorJ_g(z,z)=1 and action multiplicationη_z(g,h)=(-1)^(p(g)p(h)). These identities follow by substitutingω into the usual three-cocycle/slant formulas; the pureabc term vanishes whenever an argument belongs toH. Projective characters on the z-grade are β(g)ρ(g), with β(g)=i^p(g). Hence their tensor square acquiresβ²=sign, so a one-dimensional z-lift hasorder4. This is the only change to the untwisted central-grade representation products.

The noncentral quaternion grades form one free S3-orbit. An independent Hamilton-coordinate calculation verifies that, for each central output1 andz, the six ordered pairs of noncentral grades with that product form a free transitiveS3-set. Any cocycle phases therefore give a twisted regular representation, whose projective irreducible multiplicities are1,1,2. For each noncentral output there arefour pairs, and its stabilizer is trivial. Thus all products involving the6-dimensional simple have the claimed unchanged coefficients.

Independent constructor `audit_2019_model.py` reproduces every coefficient, verifies associativity, checks bothregularfibres and theU2embedding, and finds the model-to-census map

[0,6,5,1,2,3,4].

All343 entries match R7_4_2019; tensorSHA256 is e53b4a423763328d160bf33d459e1e205a57e9d0af120da0b654177d5bc9f73f. The tensor occurs uniquely in the rank7 rawsource, whoseSHA256 is d01245e7f534c3de8f66e7edcf70ba60c710827d1b9c85094b358eb6f134e300.

The categorical input is the standard construction C(G,ω,H,ψ) withω|H=dψ, as defined in Ostrik, arXiv:math/0202130, §3.1. The equivariantization character interpretation follows from the semidirect factorizationG=Q8⋊H; it is not an assumption that an arbitrary object permutation lifts to a tensor action.
