# Tensor support and the remaining joint spectral freedom

All 25 accepted histograms pass the following exact checks on the four
fusion matrices reconstructed in PROOF.md.

Each packet object Z, together with Z*, generates the entire center:
every simple occurs in a word of length at most two in Z and Z*. This
follows entrywise from the strict positivity of the vacuum row of
I+N_Z+N_Z^t+(N_Z+N_Z^t)^2. Thus packet support does not produce a proper
fusion subcategory or a contradiction from a missing tensor component.

Every packet fusion matrix has characteristic polynomial

    x^(n−8)(x−1)^2(x+1)(x+5)(x²−270x+225)(x²+2x+5).

Let K3=N_A3−N_A1 and K4=N_A4+N_A1, whose full matrices were forced by
the preceding evidence. The four packet matrices, N_A2, K3 and K4 are
pairwise commuting normal matrices. Their joint eigenspaces consist of
nine one-dimensional spaces and one space of dimension n−9 on which
all four packet matrices and N_A2 vanish, K3 acts as +1 and K4 as −1.

The verifier certifies this without numerical eigensolvers. It checks
that the common scalar space has dimension n−9 and that the linear
combination

    L=N_Z0+3N_Z1+9N_Z2+27N_Z3+81N_A2+243K3+729K4

has characteristic polynomial

    (x+486)^(n−9)(x−7414)(x−3159)(x−446)
    (x²−359748x+226527876)(x²−388x+37652)(x²−260x+18196).

The degree-nine factor is square-free and does not vanish at −486.
The nine remaining eigenspaces are therefore individually separated;
all operators preserve them because they commute with L. On the common
scalar space, every endomorphism commutes with all seven operators.
Consequently their simultaneous complex commutant has dimension
9+(n−9)²: 205, 153, 409 for patterns 6971, 8766, 8772 respectively.

This identifies exactly the remaining linear spectral freedom of these
forced operators. It does not complete the unknown fusion matrices or
construct a modular category. In particular, full tensor support is
consistent with a large unresolved common eigenspace.

Replay: `python3 evidence/rank8_creative_20261022/r1154/verify_packet_closure.py`.
The complete 25-branch receipt is `packet_closure.json`.
