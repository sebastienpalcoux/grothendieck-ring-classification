# Typed inner-duality calculation for R24

Research status: independent derivation of the local projective obstruction required by the torus proof. The parent and the independent literature agent reproduced the duality-comparison, square-functor, and defect-ratio signs. This remains a research checkpoint, not a publication update; the assembled proof is being independently reviewed.

## 1. Convention and typed maps

Work in a strict monoidal rigid category with a pivotal structure; the pivotal isomorphism is not assumed to be the identity. Let g be an invertible self-dual simple with g² isomorphic to 1 and second indicator −1. Let Z and gZ be self-dual simples with indicator +1. Choose the right dual structures so that g*=g and Z*=Z, with the chosen selfduality identifications equal to the identity maps. Then j_g=−id_g and j_Z=id_Z. Set e=ev_g:g²→1. The right coevaluation is −e⁻¹, and the snake identity is equivalent to

    e⊗id_g = −id_g⊗e : g³→g.                          (1)

In particular e*=−e⁻¹. These conventions deliberately keep the pivotal sign; identifying g with g* does not make j_g the identity.

Use the inner tensor functor F(X)=gXg with tensorator and unit

    J_X,Y = −id_gX⊗e⊗id_Yg : F(X)F(Y)→F(XY),
    J_0 = e⁻¹ : 1→F(1).

Both unit identities follow from (1). Its square has the monoidal identification

    η_X = −e⊗id_X⊗e : F²(X)=ggXgg→X.                  (2)

The minus sign is essential. The unnormalized contraction ηraw=e⊗id_X⊗e sends the square functor's unit to −1, not +1. Equivalently, ηraw_XY J^(2)_X,Y = −ηraw_X⊗ηraw_Y, so η=−ηraw is monoidal.

The canonical comparison δ_Z:F(Z*)→F(Z)* is −id_gZg. Indeed the transported evaluation is

    J_0⁻¹ F(ev_Z) J_Z*,Z
      = −e (id_g⊗ev_Z⊗id_g)(id_gZ⊗e⊗id_Zg),

whereas the standard nested evaluation on the object gZg is the same composite without the minus sign. This calculation concerns the rigid duality comparison, not a dagger.

## 2. Crossing transpose from the FS definition

Take any nonzero c:gZ→Zg. In conventions with arbitrary simple selfduality maps φ_g:g→g* and φ_Z:Z→Z*, the correct crossing transpose is

    τ(c)=(φ_Z⁻¹⊗φ_g⁻¹)c*(φ_g⊗φ_Z):gZ→Zg.

The map ψ=(φ_Z⊗φ_g)c:gZ→(gZ)* is a selfduality on the simple gZ. The FS definition ψ* j_gZ=ν₂(gZ)ψ, together with φ_X* j_X=ν₂(X)φ_X, gives

    τ(c) = [ν₂(gZ)/(ν₂(g)ν₂(Z))] c = −c.             (3)

This is independent of scaling c. In the chosen identity selfduality charts, c*=εc with ε=−1.

## 3. Two scalars and their invariant ratio

Define

    q=(id_Z⊗e)(c⊗id_g):gZg→Z,

and κ∈C× by the typed double-crossing identity

    (id_Z⊗e)(c⊗id_g)(id_g⊗c)
        = κ(e⊗id_Z) : ggZ→Z.                        (4)

All spaces involved are one-dimensional because gZ is simple and g is invertible. No chosen value of κ is needed.

Dualizing q gives

    q* = (id_g⊗c*)(e*⊗id_Z)
       = −ε(id_g⊗c)(e⁻¹⊗id_Z).

Thus (4) implies

    qq* = −εκ id_Z.                                 (5)

The transported canonical form on F(Z) is δ_Z=−id. Therefore the form defect γ, defined by q*φ_Zq=γδ_ZF(φ_Z), is

    γ=εκ.                                          (6)

There is a second scalar λ defined by qF(q)=λη_Z. To calculate it, start with ggZgg, move both left g strands across Z using the two c's, and compare the nested contraction of the four remaining g strands with the adjacent contraction. Relation (1) contributes exactly one minus sign:

    qF(q)=−κ(e⊗id_Z⊗e)=κη_Z.

For an expanded check, suppressing identity subscripts but retaining the tensor-word order gives

    qFq=(Z e)(c g)(g Z e g)(g c g g)
        =(Z e)(Z g e g)(c g g g)(g c g g)
        =−(Z e e)(c g g g)(g c g g)
        =−κ(e Z e).

The second line is interchange, the third is (1), and the fourth is (4).

Consequently

    λ=κ,          λ/γ=ε=−1.                        (7)

Rescaling q multiplies λ and γ by the same square. Thus their ratio is independent of object-identification normalization. This is the useful invariant conclusion; absolute assertions such as γ=1 need an additional crossing normalization and are unnecessary.

## 4. Consequence on the cubic multiplicity space

For H=Hom(Z²,Z), take the full categorical transpose induced by the symmetric form on Z and define β(f,h)=tr_Z(fhᵗ). Semisimplicity and rigidity make β nondegenerate. Involutivity of transpose and cyclicity of the pivotal trace make it symmetric. The action K of F on H in the q-chart obeys

    K²=λ⁻¹ id_H,
    β(Kf,Kh)=γ⁻¹β(f,h).

If K were scalar, these two multipliers would coincide. Equation (7) says they are negatives, so K is not scalar. For dim H=2 it has two distinct eigenlines, since K² is a nonzero scalar. The same-line values of β vanish because an eigenvalue squared is λ⁻¹ while the similitude multiplier is −λ⁻¹. Nondegeneracy therefore pairs the two opposite eigenlines, giving a hyperbolic matrix E after rescaling paired vectors.

This proves precisely the local projective nontriviality and hyperbolic eigenline statement needed for the torus argument. It uses only ν₂(g)=−1, ν₂(Z)=ν₂(gZ)=+1, not the unitary classification or the withdrawn numerical tetrahedral relations.

## 5. Independent algebra audit of the global torus step

The rank-four fusion rules imply every full F coefficient has weight (a,b) in (2Z)² with |a|+|b|≤4 after all thin maps are fixed and every thick space is structurally transported from H or J. The evenness proof counts marked incidences on the tetrahedron and the XOR of the g-label bits; it applies to every coefficient, not only a selected submatrix. The separate exhaustive enumerator reports 136 nonempty F blocks and 1472 slots.

A full-rank lattice generated by such short even weights contains (4,0) and (0,4). Thus a finite torus stabilizer forces u⁴=v⁴=1. Alternatively, if the weight lattice has rank below two, its annihilator contains a positive-dimensional torus. Its image in tensor autoequivalences modulo natural isomorphisms remains infinite: a natural transformation acts scalarly on both H and J. A positive-dimensional subgroup of the two-dimensional torus varies at least one coordinate, whereas projectively scalar actions on both H and J require t²=w²=1 and form only a finite subgroup.

If the J action has determinant −1, use eigenvalues +1,−1. Under u⁴=−1, an H weight ±2 contributes ±i and cannot be canceled by a J sign. An H weight ±4 requires four H vertices and contributes −1 with no J vertex. Therefore every surviving F coefficient has H weight zero, which gives an H-only continuous stabilizer. This removes any need to derive a primitive J loop defect.

## 6. Common structural chart and crossing covariance

Let T be a label-fixing tensor autoequivalence. Pseudo-unitarity makes the positive pivotal structure canonical, so T preserves it. Rescale the identifications T(g)→g and T(r)→r separately so that T fixes e:g²→1 and the chosen symmetric r evaluation. Each normalization requires only a nonzero complex square root. Define the identification T(s)→s through s=gr and the tensorator; do not rescale it independently.

For any chosen nonzero c:gr→rg, write T(c)=αc. Applying T to the doublepass identity (4), whose other structural constituents are fixed, gives α²κ=κ. Thus α=±1 without any EIP crossing convention.

The canonical comparison T Ad(g)≅Ad(g) T is built from the chosen g identification. It is monoidal because that identification preserves e. Functorial transport of the action K_H(c) therefore gives

    T_H K_H(c) T_H⁻¹ = K_H(αc) = α⁻¹ K_H(c).

The last equality follows because q_r appears once at the output and twice inversely at the two inputs. If α=−1, T_H is antidiagonal in K_H's two eigenlines and T_H² is scalar. But T²≅Ad(g) makes its projective square equal the nonscalar projective K_H, a contradiction. Therefore α=+1.

Now T fixes e,c,c⁻¹, the r cup/cap, their inverses when invertible, and every selected composite of them. In particular it fixes the nonzero s selfduality evaluation

    ev_s' = ev_r (id_r⊗e⊗id_r)(c⊗id_gr):grgr→1.

This is the evaluation induced by the selfduality ψ_s=(φ_r⊗φ_g)c. It is symmetric because ν₂(s)=+1. Its construction uses the already chosen s chart and requires no independent s renormalization.

The thin channels are all such fixed maps: gg→1 is e; gr→s is identity; rg→s is c⁻¹; gs→r is e⊗id_r; sg→r is q_r; rr→1 is ev_r; sr→g is id_g⊗ev_r; rs→g uses c⁻¹ then id_g⊗ev_r; ss→1 is ev_s'. Unit channels are identities. Their composition-dual inverses/inclusions are fixed as well.

Every thick Hom(r_a r_b,r_c) can be transported to H or J by one selected word in e,c,c⁻¹ and identities. All such words are T-fixed. No agreement between alternative transport paths is required. This provides exact eigenvalue weights with no thin scalar offsets.

The full-transpose forms on H and J are therefore T-invariant in this same chart. Since T_H commutes with the two K_H eigenlines, it is diag(u,u⁻¹) in a hyperbolic basis. Its projective square must have eigenratio −1, giving u⁴=−1. On J, the determinant-plus and determinant-minus cases are exactly those treated in Section 5.

These arguments close the common-chart and crossing-covariance gates, subject to independent review of the assembled proof. No old right-bend, decorated tetrahedral, or EIP unitary coefficient relation is a premise.
