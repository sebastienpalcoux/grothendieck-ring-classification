# Graded induction-packet associativity for R6_8_1660

This is a necessary reduction only. The independently replayed exact calculation rejects 533 of the 1,669 prior labelled profiles, leaving 1,136=120+508+508. An independent implementation reproduces every rejection and validates every retained witness; see `../models/packet_gram_audit.md`.

## A general necessary identity

Let M be a braided fusion category with a faithful C2 grading. If A=A₊⊕A₋ is an object split according to that grading and N_A is known, then the fusion matrices P=N(A₊), Q=N(A₋) are respectively the same-grade and opposite-grade blocks of N_A. They necessarily commute:

    PQ=QP.

This tests associativity in a small known part of the fusion ring; it does not reconstruct the other simple fusion matrices.

For M=Z(C), C=R6_8_1660, let h be its already forced central fermion and grade by monodromy with h. Put A=I_C(1), and let R have columns v_Z=F(Z) in base order (1,g,X,gX,σ,T). The projection formula gives

    N_A=RᵀR.

Let R₊ and R₋ be the even and odd column submatrices, and H₊=R₊R₊ᵀ, H₋=R₋R₋ᵀ. For any even column v and odd column w, packet commutativity implies

    vᵀ(H₊−H₋)w=0.                                      (1)

There is also a second exact packet identity in this ring:

    A₊²−A₋²=2(A₊−hA₊),
    P²−Q²=2(1−N_h)P.                                    (2)

To verify the object identity, the known restrictions of A₊ and A₋ are

    u₊=(4,0,6,6,0,8), u₋=(2,2,6,6,0,8),
    u₊−u₋=2(1−g).

At an even simple Z, the coefficient in A₊²−A₋² is v_Z·(u₊−u₋)=2(v₀−v₁); both sides have zero coefficient at an odd simple, and all odd columns have v₀=v₁. The four even low columns have (v₀,v₁)=(1,0); their h-partners have (0,1); the two odd low columns have (1,1); all other columns have (0,0). These are exactly the coefficients of 2(A₊−hA₊). The four even low columns and their h-partners are unique because the original Grothendieck ring is commutative and the six constituents of I(1) have multiplicity one. The high-column statement is already certified at the retained frontier.

## Forcing the even restriction Gram

The old total induction Gram is

    H=H₊+H₋=
    [[6,2,12,12,0,16],
     [2,6,12,12,0,16],
     [12,12,142,138,16,192],
     [12,12,138,142,16,192],
     [0,0,16,16,8,24],
     [16,16,192,192,24,280]].

After the four forced even h-pairs, all remaining restriction vectors have shape (0,0,b,c,z,a). They occur in h-pairs swapping b,c. The sigma-containing types have z=1, b+c=4, a=3; all other types have z=0. Write q=b+c and δ=b−c. Sum one representative contribution per remaining even h-pair, with its multiplicity e. The old exact even-sector dimension balance is

    Σ e(q²+2a²+2z²)=180,   Σ e(2qa)=120.                 (3)

For z=1, this is precisely the old pair weight (36,24), since q=4,a=3. In particular the X,T and gX,T entries of H₊ equal 36+Σeqa=96. The forced pairs and h-invariance therefore give the form

    H₊=
    [[4,0,6,6,0,8],
     [0,4,6,6,0,8],
     [6,6,B,C,E,96],
     [6,6,C,B,E,96],
     [0,0,E,E,F,G],
     [8,8,96,96,G,J]].

Apply (1) to each of the even low columns

    (1,0,1,1,0,2), (1,0,3,3,0,4)

and to the average of the two odd low columns, namely (1,1,3,3,0,4) in either low frame. Direct multiplication gives

    3(B+C)+10·96+4J=1940,
    9(B+C)+24·96+8J=4684.

Consequently J=140 and B+C=140. Since the forced pairs contribute 48 to J,

    Σea²=46.

The forced pairs contribute 56 to B+C, so Σeq²=84. Now (3) forces Σez²=2. Since all z-containing vectors have q=4,a=3, this also gives E=8,F=4,G=12. Thus the necessary moments are exactly

    Σeq²=84, Σeqa=60, Σea²=46, Σez²=2.                  (4)

Only B−C remains undetermined.

## The two possible matrices and uniform asymmetric charge

With (4), H₊−H₋=2H₊−H vanishes outside the two antisymmetric coordinate lines 1−g and X−gX. Its block on 1,g is 2[[1,−1],[−1,1]] and its block on X,gX is

    (2B−142)[[1,−1],[−1,1]].

For an even high column v with δ≠0, the v,v entry of (2) is

    (2B−142)δ²=2δ²,

so B=72. For an odd high column with δ≠0, the corresponding entry is

    −(2B−142)δ²=2δ²,

so B=70. Hence asymmetric high columns cannot occur in both charges.

In low frame zero the two odd low columns themselves have δ=±2. Their unit-minus-g coordinates vanish, so the same argument forces B=70; moreover their contribution exhausts the total X−gX norm, and all high columns are symmetric. In low frame one the low columns are all X/gX symmetric, while H[X,X]−H[X,gX]=4 forces some asymmetric high column. Thus B is 70 or 72, and every asymmetric high fiber has respectively odd or even charge.

The only even Grams are therefore

    H₊(Δ)=
    [[4,0,6,6,0,8],
     [0,4,6,6,0,8],
     [6,6,70+Δ/2,70−Δ/2,8,96],
     [6,6,70−Δ/2,70+Δ/2,8,96],
     [0,0,8,8,4,12],
     [8,8,96,96,12,140]],

where Δ=Σeδ² is 0 in low frame zero and is either 0 or 4 in low frame one. In frame one, Δ=0 means all asymmetric fibers are odd and Δ=4 means all are even.

## Exact search and its scope

`verify_packet_gram.py` starts from the exact 1,669-profile input, retaining all previously permitted low-one h actions. For each profile it uses the existing signed-Galois blocks of possible even-pair/odd-pair/fixed counts, adding only (4) and the uniform asymmetric charge just proved. A finite memoized recursion exhausts those bounded count options. No numerical optimizer is used.

Every returned witness is independently expanded to its full even/odd column multiset inside the script. Integer matrix multiplication checks H₊(Δ), PQ=QP, and P²−Q²=2(1−N_h)P. The implementation never needs to select a permutation of repeated labels for h: (N_h P)[r,s] is computed by applying g to the restriction vector in row r; charge is unchanged by h.

The search reports 43,245,245 new exclusions in the three labelled branches. It establishes neither full center fusion rules nor associators, and the remaining 1,136 profiles are still necessary alternatives only.
