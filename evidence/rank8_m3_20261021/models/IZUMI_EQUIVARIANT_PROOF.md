# Two C2 equivariantizations of NG(C3,6)

Izumi, *A Cuntz algebra approach to the classification of near-group categories*, arXiv:1512.04288v2, Example13.10, supplies the unitary near-group category NG(C3,6), with the normalized solution (x,y)=(sqrt(sqrt(3)/24),0). Lemma13.1 describes actual factor automorphisms gamma_(omega,theta,u), with (omega,theta,u) and (-omega,theta,-u) defining the same automorphism. Their action on the basic intertwiners is gamma(S_g)=omega² S_theta(g) and gamma(T_g(xi))=omega T_theta(g)(u xi). The paragraph before Lemma13.2, p119, explicitly defines the associated strict tensor functor by conjugation.

Choose theta=id. Reflection uses omega=1 and u=diag(1,-1). Phase rotation uses omega=i and u=rotation(pi/2). The latter preserves the solution because its parameter action rotates (x,y) by four times the angle; its square is gamma_(-1,id,-I)=id. These are coherent unitary actions of actual groups of order two.

Both actions fix all four simple objects. The six-dimensional self-fusion multiplicity space is C[C3] tensor C². Its involution is respectively I tensor diag(1,-1) or I tensor iJ, each with three +1 and three -1 eigenvectors. The intertwiners S_g have signs respectively +1 and -1. Consequently the equivariant simples are six invertibles (g,e), g in C3,e in C2, and X_0,X_1. Their complete rules are

    (g,e)(h,f)=(g+h,e+f),
    (g,e)X_f=X_f(g,e)=X_(e+f),
    X_e X_f=sum_g (g,e+f+epsilon)+3X_0+3X_1.

Reflection has epsilon=0 and matches R8_3_334. Phase rotation has epsilon=1 and matches R8_3_274. These tensors are reconstructed independently in model_constructors.py and matched in full against the census by verify_models.py. The phase-rotation specialization and census identification are derived here; no claim of historical novelty is made.
