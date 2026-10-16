# R24 categorical bridge: adversarial prepublication audit

Audit performed: 2026-10-16. Public review record: 2026-10-17.

## Verdict

**The current `R24_PROJECTIVE_INNER_SQUARE_PROOF.md` is not certified as a general exclusion proof. There is a concrete unproved, and incorrectly justified, decorated-phase cancellation in its passage from the paired right-bend frame to the two diagonal D flips.** The finite checker assumes this cancellation; it does not test it.

This is not a counterexample to the noncategorifiability claim. It is a defect in the offered proof, with a promising repair described below. In particular, a phase-free eight-parameter D argument has the same scalar conclusion and removes both disputed D flips. That alternative still needs an explicit typed categorical transport lemma for B, C, and their composition-duals before it should be counted as a repaired proof. It must not be silently substituted for the existing argument.

I read the final proof and all six associated R24 audit notes, then inspected primary formulas rather than treating those notes as evidence for one another. The independent rank-eight auditor separately confirmed the phase-index issue and the eight-slot algebra below. Neither of us claims an independently completed categorical proof of the proposed replacement transport lemma.

## Sources actually inspected

Local EIP source:

`/workspace/scratch/b038cfaffb82/work/unified/simple_global/EIP_source/main.tex`

Local published PDF and page images:

`/workspace/scratch/b038cfaffb82/work/unified/two_d_two/EIP_published.pdf`

Local FG source text/PDF:

`/workspace/scratch/b038cfaffb82/work/unified/simple_global/FG2106.txt`

`/workspace/scratch/b038cfaffb82/work/unified/simple_global/FG2106.pdf`

Public primary source: https://ems.press/content/serial-article-files/51094 (EIP, published pp. 493–568), and FG arXiv:2106.16186. I also opened the published EIP PDF through the web retrieval tool to bind the local material to the cited paper.

Useful exact locations in the EIP TeX:

- Lines 817–819: explicit statement that the paper's numerical tetrahedral symmetries are unitary, with a footnote proposing FG as a possible route to an extension.
- Lines 1120–1270: outgoing K loops and the antilinear Frobenius operators L and R; their square, covariance, and cubic relations.
- Lines 1274–1487: the unitary Frobenius basis and its phase/eigenline compatibility.
- Lines 2189–2205: the identification of A, B, C, D with actual F-matrix blocks.
- Lines 3298–3315: the B/C transports and A/D symmetries.
- Lines 3402–3691: explicit sample diagram derivations of the A odd flip, rotation about the ordinary face, and two-left-bend flip. The analogous D even flip is left to the reader.
- Line 4499: before entering the relevant unitary branch, EIP explicitly has equality of the two decorated cubic phases.
- Lines 4710–4720: the first and third double-tree equations used by the packet.

FG locations inspected: composition-dual conventions (2.6)–(2.7); Lemma 3.13(ii); modified partial duals and Proposition 3.22; Definition 4.1 and formulas (4.3)–(4.5); Definition 4.5 and (4.12)–(4.21); Theorem 4.8 and Corollary 4.9, including the caution immediately following the corollary.

## 1. What the contragredient argument really proves

For a tensor functor F, object identifications q, and composition-paired spaces V+=Hom(X tensor Y,Z), V-=Hom(Z,X tensor Y), the two actions are

    T+(f)=q_Z F(f)(q_X^-1 tensor q_Y^-1),
    T-(h)=(q_X tensor q_Y)F(h)q_Z^-1,

with tensorators understood. Their composition is q_Z F(fh)q_Z^-1. Thus

    <T+ f,T- h>=<f,h>,       T-=(T+)^-t.

This is valid without a dagger. It supports the distinction made by the incoming-loop audits. The inverse-transpose equation by itself says nothing about an independently defined partial bend unless that bend has first been identified with the relevant functorial wrapping.

If the stated loop/right-bend isotopies and symmetric nondegenerate theta pairings have been established, the subsequent hyperbolic-frame argument is sound: in dimension two K_H^2=-1 and K_J^2=1, together with the stated covariance, force opposite eigenlines and allow both right-bend matrices to be E. There is no need for positivity in that linear-algebra step.

The categorical computations of the q_r/q_gr form defects and of the exact right-bend/wrapping identification remain actual diagram computations, not consequences of the matrix statement. I found no contradiction to them in the EIP definitions. Their validity, however, does not automatically determine the left bends or the numerical even-flip phases. That distinction is where the current proof goes wrong.

## 2. Incoming and outgoing decorated left bends carry different indices

Use the packet's paired bases for J+ and J-. Write

    R+:J- -> J+ = E,       R-:J+ -> J- = E,
    E=[[0,1],[1,0]],       bar(i)=1-i.

Let L-:J+ -> J- and L+:J- -> J+ be the two oriented left bends. In the EIP normalization with lambda_r=mu=1 they are inverse maps. If the outgoing cubic rotation is defined by

    C+=R+ L-=Omega=diag(omega_0,omega_1),

then necessarily

    L-=E Omega,            L+=Omega^-1 E.

Consequently, for outgoing basis e_i and composition-dual incoming basis e^i,

    L-(e_i)=omega_i e^(bar(i)),
    L+(e^i)=omega_bar(i)^-1 e_bar(i).

The second formula has **bar(i)** in its phase index. It is not omega_i^-1 unless the two decorated phases are equal. Changing which oriented cubic composite is called C+ changes the naming of the phases, but does not remove this paired-index distinction.

This is easy to witness exactly. Set omega_0=1 and omega_1=zeta, with zeta^3=1 and zeta!=1. Take K_J+=K_J-=diag(1,-1), R+=R-=E, and L-/L+ as above. Then

- L+L-=L-L+=1;
- both oriented cubic composites have cube 1;
- all stated loop/right-bend covariance equations hold;
- the left bends also anticommute with the J loop in the stated manner;
- the two decorated outgoing phases are unequal.

This is a countermodel to the asserted implication from the retained local matrix hypotheses to same-index phase cancellation. It is deliberately **not** claimed to be the data of a fusion category.

## 3. Where this affects the actual primary-source flip

EIP's tetrahedral coefficient has opposite variance at slots i and k. In the explicit tetrahedron, the vertex i has one input and two outputs; vertex k has two inputs and one output. In the D block these are the incoming and outgoing J vertices, respectively. This also follows from the actual F-block identification

    D^(i,j)_(k,l) = (F^(r,r,r)_(gr))^((gr;i,j))_((r;k,l)).

The two-left-bend maneuver in EIP's explicit A flip derivation first bends the outgoing k vertex and then the incoming i vertex. Its unitary phase is written omega_k/omega_i. The D formula at line 3315 has the corresponding decorated phase omega_alpha,k omega_alpha,i^2.

For genuinely independent composition-dual spaces, the displayed oriented-bend table instead produces the mixed-variance phase

    omega_k / omega_bar(i)

in this convention, or its inverse if the whole flip is read in the reverse direction. For i=k this is generally omega_i/omega_bar(i), **not** omega_i^3. A further compatibility identity could force it to one, but that identity is not proved in the current packet. Indeed, the packet explicitly declines to compare the two decorated phases or to prove the relevant left-bend compatibility.

In the unitary derivation the distinction is invisible because EIP has already proved omega_alpha,0=omega_alpha,1. Transplanting the numerical formula while declining to retain the hypothesis that makes its phase indexing harmless is not justified.

It follows that the two claimed signs

    D_1111=-D_0000,        D_1010=-D_0101

have not been derived in the advertised arbitrary-phase paired frame. Therefore the six-parameter D normal form and the contractions as written in the current proof are not established by the offered argument.

This is a concrete gap, not merely a demand for more exposition. The line `need(v[0]==v[2], 'decorated phase occurs as its cube')` in `verify_r24_projective_inner_square.py` assumes precisely the wrong inference under the retained hypotheses. The verifier checks index equality, not the oriented left-bend coefficient.

## 4. What FG does and does not supply

FG does give a useful general result: pseudo-unitarity supplies the required epsilon signs, and a suitable rigidity gives a linear S4 action leaving the appropriately normalized F/G evaluation invariant. This supports attempting a C-linear extension.

It does not identify EIP's numerical coefficient slots after choosing only an outgoing eigenbasis. Formula (4.3) acts on four tensor factors using explicit partial duals. Equations (4.13)–(4.21) retain those partial duals and their matrix entries. Immediately after Corollary 4.9 the authors explicitly warn that partial duals need not send chosen basis morphisms to chosen basis morphisms, and that numerical 6j identities depend on gauge.

Here the right-bend frame is useful additional information. It still leaves the oriented decorated left-bend matrices shown in section 2. Citing Corollary 4.9 and saying the phases cancel does not replace inserting those matrices in the specified tensor factors.

## 5. A materially simpler repair: retain all eight even D slots

The two disputed even D flips are not needed for the scalar nonvanishing argument. Retain instead

    D=[[x,0,0,Z],
       [0,X,y,0],
       [0,Y,W,0],
       [z,0,0,w]],

where W and w are independent. Keep the odd composition-dual slot map

    p(i,j,k,l)=(k,bar(j),i,bar(l)),

which uses right bends. Its pairings are x<->X, y<->Y, z<->Z, W<->w. Define S=xX+Ww.

If the three selected resolutions are established in this larger frame, their expansions are

    1=2r0^2+S+1/d,
    1=S+2zZ,
    1=S+2yY.

Subtracting gives

    yY=zZ=r0^2+1/(2d).

For r0=(2-sqrt(5)+tau)/4, tau=+1 or -1, these are respectively

    (sqrt(5)-1)/8,       (3sqrt(5)-5)/8,

both nonzero. This algebra is completely independent of the decorated left bends, the D even flips, and whether W=-X or w=-x. The existing normalizer argument needs only y,z nonzero with their weights, so it would survive this change.

One must not cite the existing p.539 equations unchanged as a proof of those larger-frame resolutions. A cleaner route is direct F/G completeness in the following actual matrix columns.

### Candidate paired transport lemma

Let F0=F^(r,r,r)_r and F1=F^(r,r,r)_(gr), with A,B the p=r,p=gr blocks of F0 over q=r, and C,D the corresponding blocks of F1. Write X^vee for the inverse-matrix coefficient with reversed tree variance, not complex conjugation. The needed categorical statement is

    D^vee_v=D_p(v),
    A^vee_v=A_p(v),

and, with b_l=-i(-1)^l,

    B_v=b_l D_c(v),          B^vee_v=b_l^-1 D^vee_c(v),
    C_v=b_l D_c2(v),         C^vee_v=b_l^-1 D^vee_c2(v),

where

    c(i,j,k,l)=(j,bar(k),bar(i),l),
    c2(i,j,k,l)=(bar(k),i,bar(j),l).

The outgoing formulas are the EIP B/C formulas at lines 3298–3299 with lambda_r=1, lambda_g=-1 and omega_H=1. There is a structural reason these are better candidates than the D even flip: they rotate about the fixed face l, which is an ordinary H face in B,C,D. The explicit EIP derivation of this three-cycle uses a left bend at that ordinary face and right bends at the others. Thus L_H=R_H=E and R_J=E should suffice; a decorated L_J should not occur.

The reciprocal factors must be proved on the actual oriented opposite diagrams. Their intended origin is the contragredient loop: the residual red-loop scalar b_l on one tensor factor becomes b_l^-1 on its composition-dual factor. This is credible and compatible with the general paired-transport principle U^-t, but the type-level identification of these exact B/C transports with U and U^-t must be included, not inferred solely from the outgoing numerical formula.

The final needed unit-channel identity is

    F0_(1;(k,l)) G0_((k,l);1)=delta_(k,bar(l))/d.

With evaluation and coevaluation scaled by d^-1/2, bending the ordinary trivalent vertex with R_H=E gives each of the two factors delta_(k,bar(l))/sqrt(d). This provides the proposed direct cup calculation; its orientation should be recorded alongside the B/C transport diagrams.

### Exact finite expansions once that lemma is supplied

The relevant columns and contributions are:

| Actual F column | First block contribution | Second block contribution | Unit contribution |
|---|---:|---:|---:|
| F0, (k,l)=(0,1) | A: 2r0^2 | B: xX+Ww | 1/d |
| F1, (k,l)=(0,0) | C: Ww+zZ | D: xX+zZ | 0 |
| F1, (k,l)=(0,1) | C: Ww+yY | D: xX+yY | 0 |

These are standard column contractions of F with its composition-dual inverse. The two selected columns of F1 involve no unit channel. This route also avoids relying on the index reshuffling in the printed p.539 double-tree displays.

Both this auditor and the independent rank-eight auditor expanded these slots. The unresolved work for a full repair is categorical, not arithmetic: prove the displayed B/B^vee and C/C^vee transport table in one common frame, and explicitly record the cup calculation. A fresh audit should check those typed diagrams without treating EIP's unitary numerical identities as already extended.

## 6. Other possible repair and final disposition

The indicators also force nu3(gr)=2. It is conceivable that identifying Hom((gr)^2,gr) with J and transporting the ordinary gr rotation determines the decorated phases, making their ratio one. No explicit compatible identification or rotation calculation establishing that consequence was found in the current proof or audits. It must not be assumed. The eight-slot approach appears to avoid this extra problem altogether.

The source-to-inner-square implication and the downstream projective normalizer algebra were not refuted here. The defect is in the middle categorical coefficient bridge. Existing scalar receipts can be correct and still fail to certify that bridge because they start from its asserted six-parameter normal form.

**Publication recommendation for the current packet:** do not describe R24 as a generally established exclusion on the strength of this proof. Either supply and independently check a replacement categorical lemma (the eight-slot route above is a concrete target), or retain R24 as unresolved/conditional. Absence of a categorical counterexample is not verification of the missing implication.

## 7. Follow-up replacement attempt and final audit outcome

After the initial finding, I wrote `CONDITIONAL_EIGHT_SLOT_REPAIR.md` with exact typed endomorphism formulas for A/B/C/D and their separate opposite-tree coefficients, four proposed trace transport equalities, an explicit variance/index table, and the complete eight-slot scalar calculation. The independent rank-eight reviewer checked those types and the finite algebra.

The unit contribution was independently closed by the displayed normalized cup/cap calculation. The treatment of odd/even slot maps was also checked: p is applied only after the independently specified B/C opposite transport reaches D^vee; p and c are not silently commuted. The checker explicitly detects that p c p differs from c on twelve of the sixteen slots.

The exact remaining obstacle is a common-frame orientation/sign calculation. EIP's chosen crossing reverses G-strand orientation, and G has second indicator -1. Neither reviewer could certify that every proposed trace move leaves precisely the claimed inverse H loop with no extra reversed-G-cap sign or mixed-basis chart factor. Invoking generic inverse-transpose transport would assume the compatibility one is trying to establish.

Accordingly the replacement is **not certified**. `verify_eight_slot_algebra.py` passes in normal and optimized modes, but both receipts intentionally record `classification_decisions: 0` and `categorical_transport_certified: false`. The original proof remains unsupported at its identified phase step, and the proposed repair remains a precise conditional research target. No frozen evidence or manuscript was modified by this audit.
