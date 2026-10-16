# Exact Verlinde obstruction to the historical rank-37 witness

Scope: this rejects the particular rank-37 necessary-system witness in `evidence/theoretical_20261016/rank6/r1660_modular_witness/witness.json`. It does not exclude R6_8_1660 or any other restriction/twist profile. The older witness remains a valid solution of its explicitly stated weaker system.

Use the source order (1,g,X,gX,sigma,T), with T=sigma X. In the historical witness let A be its low constituent with

    F(A)=1+X+gX+2T.

Its twist exponent 4 modulo48 contains precisely two simples B_+,B_-, both with

    F(B_+)=F(B_-)=X+gX+2T.

The supplied finite modular-representation decomposition has exactly two dimensions at this twist. One belongs to W=(61,5), a multiplicity-one twelve-dimensional irreducible with simple T spectrum and a one-dimensional T-fixed line. The other belongs to the one-dimensional irreducible H=(0,1). These are checked from the exact local SL(2,Z/16) and SL(2,Z/3) character tables, not inferred from a dimension match.

Write L_{E,i}=S_{E,A_i} for the six known low columns. Reciprocity gives L=VX^t, where X_{a,i}=chi_a(X_i)/f_a and V consists of the actual forgetful rows. Let Q be the rank-one spectral projector of the known low S block onto its eigenvalue -sqrt6/12. The prior exact compression theorem identifies this projector with W's T-fixed line. Consequently the squared W coordinate of a simple E in the vector S e_W is

    a_E=L_E Q L_E^*.

All quantities here are real in this particular witness, and the checker verifies that fact. At phase4 the two L rows coincide and a_E is nonzero. Hence the normalized sum b=(e_{B_+}+e_{B_-})/sqrt2 is W's phase4 line; the normalized difference h=(e_{B_+}-e_{B_-})/sqrt2 is H. This identifies the lines canonically up to their harmless scalar phases.

By Verlinde, multiplication by A on the center is

    N_A=S diag(r_E) S^*,    r_E=S_{A,E}/S_{0,E}.

For a twist phase t in W define

    q_t=(sum_{E:theta_E=zeta48^t} r_E a_E) /
        (sum_{E:theta_E=zeta48^t} a_E).

Because W has simple T spectrum and all denominators are nonzero, q_t is the expectation of diag(r_E) on W's normalized phase-t line. The transition probabilities are determined without choosing S entries:

    p_t=Tr_W(P_4 S P_t S^-1).

For a local factor of modulus m this is the exact character average

    (1/m^2) sum_{j,k mod m} zeta_m^(-4_local*j-t_local*k)
                       chi(T^j S T^k S^-1).

CRT takes the product of the two local averages. The exact values are:

| t | 0 | 16 | 6 | 22 | 12 | 28 | 18 | 34 | 24 | 40 | 36 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p_t | 1/12 | 1/24 | 1/6 | 1/12 | 1/12 | 1/24 | 1/6 | 1/12 | 1/12 | 1/24 | 1/12 | 1/24 |
| q_t | 15 | 3 | -1 | -1 | -1 | -1 | -1 | -1 | 15 | 3 | -1 | -1 |

Thus <b,N_A b>=sum p_t q_t=2.

On H, S acts by a scalar, so S^*h is again a multiple of h. The two phase4 eigenvalues r_{B_+}=r_{B_-}=-1 are equal. Therefore <h,N_A h>=-1, and the cross expectation <b,N_A h> vanishes: after applying S^*, the h vector remains the antisymmetric difference supported at phase4, while the W vector has symmetric phase4 coordinates and diag(r_E) is scalar there.

Since e_{B_+}=(b+h)/sqrt2, it follows that

    N_{A,B_+}^{B_+}=(2-1)/2=1/2.

This contradicts integral fusion multiplicities. The argument does not depend on arbitrary phases in irreducible realizations or any of the signs occurring in a full S completion. The same coefficient holds for B_-.

## Replay and limits

`verify_r1660_witness_verlinde.py` is a standalone standard-library replay supporting `--repo` and automatic repository discovery. It binds all six inputs by SHA256, rechecks every historical necessary-system equation and bound, verifies the phase fiber and active irreducible support, and computes every character probability and weighted ratio exactly over Q(zeta48). It uses the equivalent rational projection weight a_E=L6(v_E)^2/96 and identifies the low character from its formal codegree D/dim(A). The normal and independently optimized receipts agree.

An independent numerical reconstruction also found 32 symmetric modular S completions of this same representation and restriction profile; all have half-integral Verlinde coefficients. That exploration motivated the short exact argument above and is not used as evidence for the contradiction.

No other candidate profile is claimed to satisfy the specific phase and representation premises above. Extending the obstruction requires new analysis of those remaining profiles.
