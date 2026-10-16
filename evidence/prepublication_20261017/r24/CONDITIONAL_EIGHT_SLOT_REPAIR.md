# Candidate eight-slot replacement for the R24 coefficient bridge

Date: 2026-10-17. Status: **independent review completed with an unresolved categorical transport gate; not a certified replacement proof**.

This document leaves the frozen `R24_PROJECTIVE_INNER_SQUARE_PROOF.md` untouched. It replaces its decorated even flips and its six-parameter D reduction. It assumes the previously stated loop/right-bend lemma and the forced ordinary cubic rotation on H. It makes no assertion about either decorated cubic phase.

## The exact remaining lemma

Work in strict notation, with associators and the monoidal comparison maps restored canonically in a nonstrict category. Put A=r, G=g, S=G tensor A, and d=dim(A)=dim(S). Let e:G tensor G -> 1 be the chosen evaluation isomorphism and e^-1 its inverse. Choose composition-dual bases

    f_i:A A -> A,       h_i:A -> A A,
    t_i:A A -> S,       u_i:S -> A A,

so f_i h_j=delta_ij id_A and t_i u_j=delta_ij id_S. Write bar(i)=1-i. The right bends in both directions on H and J have matrix E; the left bends on H also have matrix E. The outgoing ordinary loop has K_H+=diag(i,-i), and the incoming one is K_H-=(K_H+)^-t=diag(-i,i).

Choose the mixed bases

    P_j=id_G tensor f_j: S A -> S,
    P^vee_j=id_G tensor h_j: S -> S A,
    Q_j=(e tensor id_A)(id_G tensor t_j): S A -> A,
    Q^vee_j=(id_G tensor u_j)(e^-1 tensor id_A): A -> S A.

These are paired: P_j P^vee_k=delta_jk id_S, Q_j Q^vee_k=delta_jk id_A. This follows by cancelling e with e^-1 and using t_j u_k=delta_jk id_S. Any source convention using an opposite orientation of the g evaluation must be translated at this point, rather than inserting a sign later.

Define the coefficients by the following **typed scalar endomorphisms**:

    A^(i,j)_(k,l) id_A = f_k(id_A tensor f_l)(h_i tensor id_A)h_j,
    B^(i,j)_(k,l) id_A = f_k(id_A tensor f_l)(u_i tensor id_A)Q^vee_j,
    C^(i,j)_(k,l) id_S = t_k(id_A tensor f_l)(h_i tensor id_A)u_j,
    D^(i,j)_(k,l) id_S = t_k(id_A tensor f_l)(u_i tensor id_A)P^vee_j.

Define their opposite-tree coefficients separately:

    A^vee^(i,j)_(k,l) id_A = f_j(f_i tensor id_A)(id_A tensor h_l)h_k,
    B^vee^(i,j)_(k,l) id_A = Q_j(t_i tensor id_A)(id_A tensor h_l)h_k,
    C^vee^(i,j)_(k,l) id_S = t_j(f_i tensor id_A)(id_A tensor h_l)u_k,
    D^vee^(i,j)_(k,l) id_S = P_j(t_i tensor id_A)(id_A tensor h_l)u_k.

These definitions make the vee coefficients entries of the inverse F matrix with opposite row/column placement. **Vee is not scalar complex conjugation and is not yet a slot permutation.**

The lemma to establish from the oriented EIP crossing and partial-bend diagrams is

    A^vee_v=A_p(v),             D^vee_v=D_p(v),

    B_v=b_l D_c(v),             B^vee_v=b_l^-1 D^vee_c(v),
    C_v=b_l D_c2(v),            C^vee_v=b_l^-1 D^vee_c2(v),

where b_l=-i(-1)^l and

    p(i,j,k,l)=(k,bar(j),i,bar(l)),
    c(i,j,k,l)=(j,bar(k),bar(i),l),
    c2(i,j,k,l)=(bar(k),i,bar(j),l).

The two odd relations involve right bends only. The forward B/C relations are EIP's formulas with omega_H=1, but their reuse here requires the following common-frame derivation.

### Proposed explicit trace transport

All four displayed scalar endomorphisms may be replaced by their spherical trace divided by d. The asserted B and C trace equalities, prior to substituting any loop eigenvalue, are

    tr_A[f_k(id tensor f_l)(u_i tensor id)Q^vee_j]
       = tr_S[t_bar(i)(id tensor (K_H+^-1 f_l))
                    (u_j tensor id)P^vee_bar(k)],

    tr_S[t_k(id tensor f_l)(h_i tensor id)u_j]
       = tr_S[t_bar(j)(id tensor (K_H+^-1 f_l))
                    (u_bar(k) tensor id)P^vee_i].

Their opposite-oriented counterparts are

    tr_A[Q_j(t_i tensor id)(id tensor h_l)h_k]
       = tr_S[P_bar(k)(t_j tensor id)
                    (id tensor ((K_H-)^-1 h_l))u_bar(i)],

    tr_S[t_j(f_i tensor id)(id tensor h_l)u_k]
       = tr_S[P_i(t_bar(k) tensor id)
                    (id tensor ((K_H-)^-1 h_l))u_bar(j)].

The factor-by-factor variance table is:

| Source | Bent factors | Unbent factor | Fixed ordinary factor | Destination |
|---|---|---|---|---|
| B | incoming J_i -> outgoing J_bar(i); outgoing H_k -> incoming H_bar(k) | incoming J_j | outgoing H_l | D_(j,bar(k),bar(i),l) |
| B^vee | outgoing J_i -> incoming J_bar(i); incoming H_k -> outgoing H_bar(k) | outgoing J_j | incoming H_l | D^vee_(j,bar(k),bar(i),l) |
| C | outgoing J_k -> incoming J_bar(k); incoming J_j -> outgoing J_bar(j) | incoming H_i | outgoing H_l | D_(bar(k),i,bar(j),l) |
| C^vee | incoming J_k -> outgoing J_bar(k); outgoing J_j -> incoming J_bar(j) | outgoing H_i | incoming H_l | D^vee_(bar(k),i,bar(j),l) |

The proposed diagrammatic proof bends exactly those factors using R_H/R_J, cancels adjacent g evaluation/coevaluation pairs and inverse crossings, and rotates the fixed H_l face once (B) or twice (C). The ordinary rotation is the identity. The remaining red strand should be precisely the inverse ordinary wrapping, K_H+^-1 on f_l and (K_H-)^-1 on h_l. Substitution then gives b_l and b_l^-1, respectively.

**Review gate:** the exact oriented cancellation from each typed trace word to the stated remaining loop must be independently checked. The table records types and indices; types alone do not prove the residual loop or its scalar. The proof is not certified until that gate is closed. No decorated left bend is allowed in the derivation.

Independent-review outcome: the rank-eight reviewer checked the typed endomorphism domains, the variance/index table, the cup calculation, and the finite contractions. The remaining-loop claim was not independently certified. EIP's crossing reverses the orientation of the G strand, and the G self-duality form is skew (second indicator -1). Consequently a reversed G cap can contribute a sign; the P/Q charts written here must be explicitly matched to those oriented diagrams before the asserted b_l/b_l^-1 transport is valid. The generic identity U^-t for composition-dual transport does not resolve that chart-identification problem. This document therefore remains a conditional research target and must not authorize an R24 classification change.

No commutation of p and c is used. In particular we do not assert B^vee_v=B_p(v), since the odd tetrahedral move for B need not land in the B family. Only after the separately computed opposite B/C transport reaches D^vee is D^vee_v=D_p(v) substituted. This avoids conflating odd slot identification with the opposite-frame transport.

## The unit-channel contraction (algebraically checked)

Choose self-dual A evaluation/coevaluation with lambda_A=1, and set

    U=d^-1/2(ev_A tensor id_A): A^3 -> A,
    U^vee=d^-1/2(coev_A tensor id_A): A -> A^3.

The ordinary bend identities give

    f_k(id tensor f_l)U^vee
        = d^-1/2 f_k h_bar(l)
        = delta_(k,bar(l)) d^-1/2 id_A,

    U(id tensor h_l)h_k
        = d^-1/2 f_bar(l)h_k
        = delta_(k,bar(l)) d^-1/2 id_A.

Therefore their product is delta_(k,bar(l))/d. This uses both oriented bends E and composition duality; it uses no dagger.

## Eight-slot coefficient calculation (checked independently twice)

The ordinary H tetrahedral symmetries and parity give

    A=[[r0,0,0,aU],
       [0,r0,r0,0],
       [0,r0,r0,0],
       [aL,0,0,r0]].

Use only parity for D:

    D=[[x,0,0,Z],
       [0,X,y,0],
       [0,Y,W,0],
       [z,0,0,w]].

The p relation pairs x/X, y/Y, z/Z, W/w, and aL/aU. Put S0=xX+Ww. F/G column completeness and the candidate transport lemma give:

| Matrix and column | First block | Second block | Unit |
|---|---:|---:|---:|
| F^(r,r,r)_r, column (0,1) | A: 2r0^2 | B: S0 | 1/d |
| F^(r,r,r)_(gr), column (0,0) | C: Ww+zZ | D: xX+zZ | 0 |
| F^(r,r,r)_(gr), column (0,1) | C: Ww+yY | D: xX+yY | 0 |

Thus

    2r0^2+S0+1/d=1,
    S0+2zZ=1,
    S0+2yY=1,

and yY=zZ=r0^2+1/(2d).

The unchanged annular-corner argument supplies r0=(2-sqrt(5)+tau)/4, tau=+1 or -1. Hence

    yY=zZ=(sqrt(5)-1)/8       (tau=+1),
    yY=zZ=(3sqrt(5)-5)/8      (tau=-1).

Both are nonzero. The y/z gauge weights are the same as in the original coefficient convention (or their simultaneous passive-coordinate inverses), so the existing projective normalizer argument follows once the categorical lemma is established.

## Verification boundary

`verify_eight_slot_algebra.py` verifies the eight-slot permutations, both forward and separately specified opposite B/C transports, the three actual F-column expansions, and the two nonzero field values. It deliberately reports zero classification decisions. It cannot establish the categorical trace equalities in the review gate.
