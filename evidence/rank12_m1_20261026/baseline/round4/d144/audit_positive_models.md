# Independent continuation audit of the four retained D144 models

Status: retained for R12_1_79, R12_1_80, R12_1_322 and R12_1_323. No promotion of R180,R181,R320,R321.

## A previous source limitation was removed

Round2 explicitly disclosed that its m=0 S-matrix came from the previous lower-rank project rather than a fresh read of the primary paper. In this audit the complete Teo--Hughes--Fradkin paper was fetched successfully and page49 was inspected directly, including the rendered equation6.53. Every block agrees with the stored full twelve-object matrix. TableIX on page47 supplies the dimensions, twists, and m=0,1,2/s=0,1 parameterization. Thus the missing fresh-primary-transcription check is now completed.

Primary paper: https://arxiv.org/pdf/1503.06812 (arXiv1503.06812v2). Equation6.53 has the three-by-three block

    [[-8 cos(4 pi m/9), -8 cos(4 pi (m-3)/9), -8 cos(4 pi (m+3)/9)],
     [-8 cos(4 pi (m-3)/9), -8 cos(4 pi (m+3)/9), -8 cos(4 pi m/9)],
     [-8 cos(4 pi (m+3)/9), -8 cos(4 pi m/9), -8 cos(4 pi (m-3)/9)]].

For m=0 these entries are exactly (-8,4,4). For m=1, writing y=2cos(pi/9), they are (4y^2-4y-8,4y,8-4y^2). This is exactly the stored polynomial basis implementation; the full matrix, including all four sqrt(2) rows, agrees. The ordering matches TableIX.

## Categorical existence is separate from Verlinde arithmetic

Cui--Galindo--Plavnik--Wang, https://arxiv.org/pdf/1510.03475, Section6.2 (printed pages20--22), constructs the SO(8)_1 triality gauging, sequentially through SU(3)_3. Proposition3 and the gauging discussion in Section3.4 give genuine unitary G-crossed extensions and equivariantizations, with associativity choices forming the H^3(G,U(1)) torsor after the obstructions vanish. This is the source of categorical existence, not the fact that an S-matrix passes numerical consistency tests.

The full S3 extension exists. Its H^3(S3,U(1))=C6 variations include all three restrictions on C3, while the C2 variation changes spins but not the displayed S-matrix. The m=0 variation is therefore an actual associator/SPT modification of an existing crossed extension. Teo--Hughes--Fradkin's TableIX and surrounding discussion identify these variations and equation6.53 gives their modular matrix. No completeness claim about all categorifications of the ring is needed. The source formula for m=0 is now directly checked rather than inherited unchecked from the rank-eight project.

The parameter m in our files denotes the retained m=0 or m=1 fusion tensor. It does not assert that exactly two tensor-equivalence classes exhaust all gauging choices. The m=2 tensor is isomorphic to m=1, but that observation is not required for the four positive decisions.

## The two bosonic zests

The sign charge z is an actual object in the canonical central Rep(S3), with order2, trivial associator on its Rep(C2) subcategory, and self-braiding +1. The integer/noninteger parity grading is exact. The central-valued cocycle lambda(a,b)=z^(ab) therefore gives the associative tensor product

    X star Y = X tensor Y tensor z^(deg(X)deg(Y)).

Its scalar obstruction is trivial: the relevant self-crossing of z is +1. The associator is constructed using the actual central half-braiding, not from centrality in the fusion ring. All ingredients are unitary. This retains R322,R323 as actual models.

## Replay and scope

`verify_positive_models.py` independently reconstructs each exact tensor, checks all1728 coefficients under its frozen basis permutation, and records the input hash. It also checks the full parity grading and actual ring-level order2/current action. These exact checks verify identification; the categorical existence and central-lift premises above remain separate cited mathematics.

The four unmodeled permutations still need coherent tensor lifts. Neither equation6.53 nor this audit supplies those lifts.
