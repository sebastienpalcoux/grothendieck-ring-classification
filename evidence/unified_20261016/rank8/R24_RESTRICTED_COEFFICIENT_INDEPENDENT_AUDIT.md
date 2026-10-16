# Independent audit of the restricted 2D2 coefficient obstruction

Auditor: two_d_two. Date: 16 October2026.

Scope: the coefficient, corner-character, and scalar parts of the minimal R24 proof. This audit uses the C-linear incoming-loop/right-bend lemma separately checked in two_dimension's `PU_2D2_INCOMING_LOOP_AUDIT.md`. That lemma supplies the two paired eigenframes and right-bend matrix E. The subsequent projective normalizer theorem is independently checked in rank6_center's `PU_2D2_PROJECTIVE_NORMALIZER_AUDIT.md`. Together these cover the local argument without a dagger.

I read the original published EIP pp506–507,512–515,528–530, and539, including rendered diagrams and all needed index positions. I also checked the applicable Fuchs–Grøsfjeld linear partial-duality and tetrahedral statements, especially the covector-dual completeness convention in equations2.6–2.7 and Corollary4.9. The numerical identities below are not inferred merely by replacing a conjugation symbol: their incoming indices are fixed by the explicit right-bend table.

## 1. Only the ordinary cubic rotation is used

The ordinary rho cubic rotation is the identity, so the left and right H bends agree. On J, retain arbitrary cubic eigenphases omega_0,omega_1. Their equality is unnecessary. The right J bend remains E, as supplied by the separately audited paired-loop lemma. Both loop eigenlines are one-dimensional, so every commuting cubic rotation is diagonal in this eigenframe, with each omega_i cubed equal to1.

## 2. Exact restricted slot equations

Write a coefficient slot v=(i,j,k,l). The odd dual flip on EIP p528 is

    p(v)=(k,1-j,i,1-l).

It uses the right bends and its scalar is lambda_r^(j+l)=1. Thus the reflected coefficient is the incoming composition-dual coefficient with exactly this index permutation. This map is an involution. No scalar i is conjugated.

For A, the ordinary rho cubic phase is1, so its even maps are

    c(v)=(j,1-k,1-i,l),
    q(v)=(1-k,1-l,1-i,1-j),
    A_v=A_c(v)=A_q(v).

The parity-zero condition removes all eight odd slots. Direct solution of these linear equalities leaves exactly the three entries r,a,A in

    [[r,0,0,A],[0,r,r,0],[0,r,r,0],[a,0,0,r]].

For D, ONLY two even q equations are needed: at v=0000 and v=0101. In both, i=k, so the source phase omega_k*omega_i² is omega_i³=1 independently of any relation between the two decorated phases. Hence

    D1111=−D0000,        D1010=−D0101.

Together with the eight parity zeros these are exactly ten independent linear constraints, leaving the six entries in

    D=[[x,0,0,Z],[0,X,y,0],[0,Y,−X,0],[z,0,0,−x]].

The odd p table sends0000 to0101,0110 to1001, and1100 to0011. Therefore the incoming dual coordinates are x<->X,y<->Y,z<->Z; it also fixes the r slots of A and exchanges a,A. This checks every coefficient pairing used below. No off-diagonal even D flip, no common decorated cubic phase, and no hat tensor is needed.

## 3. The two scalar corner branches

The unit tube corner is the complexified neutral fusion ring; its module A_(1,r) has the source matrices

    g -> [[0,I],[I,0]],
    r -> [[phi,phi0],[phi0,phi]],    phi=2r I.

The repeated letter r here denotes the scalar matrix entry, while the source object is rho. Semisimplicity of the corner representation permits simultaneous decomposition by the g eigenspaces. On g=+1, rho has eigenvalues d=2+sqrt5 and dbar=2−sqrt5. The d character is the central-unit constituent, absent from A_(1,rho) because F(1)=1 contains no rho. Thus phi+phi0=dbar I. On g=−1, the fusion relation reduces to rho²=1, giving (phi−phi0)²=I. Consequently

    (4r−dbar)²=1,
    r=(2−sqrt5+tau)/4, tau=±1.

This argument uses no positivity of a representation or Hermitian diagonalization. It does not select one scalar branch, and does not use a fourth indicator.

## 4. Exactly three diagonal contractions

The first double-tree resolution on EIP p539 at(k,l,k',l')=(0,0,0,0) has two r² terms and two xX terms. The unit channel contributes1/d=sqrt5−2. Therefore

    1=2r²+2xX+(sqrt5−2),
    r²+xX=(3−sqrt5)/2.

The third resolution at0000 contracts the two nonzero entries of columns00 and11 with their composition-duals; this is

    1=2xX+2zZ.

At0101, columns01 and10 similarly give

    1=2xX+2yY.

These contractions use opposite tree bases and their exact composition duals. Diagonal contraction cancels any phase on a vertex with its reciprocal dual phase. The factors(-1)^(l+l') are+1 in all three selected instances. Thus neither a hidden conjugation of i nor a decorated left-bend phase enters any selected equation.

It follows in the two branches respectively that

    yY=zZ=(sqrt5−1)/8,    or    yY=zZ=(3sqrt5−5)/8.

Both numbers are nonzero. This proves the required nonvanishing of y,z without the second/fourth indexed source displays, their possible transcription errors, the hat block, or a general unitarizability assertion.

## 5. Gauge weights and downstream consequence

The defining D tetrahedron has two vertices of each multiplicity type. Inserting paired rescalings (u,u^-1),(v,v^-1) yields the source weights u^-2 v² for y and u^-2 v^-2 for z. This is a monomial basis-change calculation valid for arbitrary nonzero complex u,v; the source's restriction to unit phases is not used. If a label-fixing auto fixes the normalized crossing, it must preserve these two nonzero coefficients, so u^4=1. If it reverses that crossing, its H matrix is antidiagonal and also has scalar square. The independent normalizer audit then excludes a square equal to Ad(g).

Conclusion: the restricted coefficient and corner portions PASS, using the already independently audited incoming-loop/right-bend lemma. The minimal proof should use only the two diagonal D flips and retain arbitrary decorated cubic phases; earlier longer drafts that force the decorated phase or select tau are unnecessary. This is a proof audit, not authorization to update classification ledgers; root review and final source packaging remain separate.
