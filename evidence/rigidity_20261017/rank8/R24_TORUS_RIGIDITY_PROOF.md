# An inner-square obstruction from short gauge weights

Research manuscript, 17 October 2026. **AI-generated research · independent verification pending.** This argument has received independent adversarial reviews within the AI workflow; it has not been independently human-verified or Lean-formalized.

## Theorem

Let D be a pseudo-unitary fusion category over C with simple objects 1,g,r,s=gr, fusion rules

    g²=1,  gr=rg=s,  r²=1+2r+2s,

and canonical second Frobenius–Schur indicators

    ν₂(g)=−1,  ν₂(r)=ν₂(s)=1.

There is no tensor autoequivalence T inducing the identity permutation on simple objects and satisfying T² ≅⊗ Ad(g).

The proof uses the finiteness of tensor functors between fixed fusion categories, ENO, *On fusion categories*, Theorem 2.31. No classification of associators, numerical tetrahedral symmetry, positivity of a Hermitian form, or nonzero individual F-symbol is required.

## 0. From the source ring to the theorem's hypotheses

The source tensor for R8_2_24 has SHA-256

    2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738.

Its neutral basis in the order (1,g,r,s) is (0,7,5,6); the odd invertible a has label1, inverse label2, and square g of label7. The complete source is commutative, and conjugation by a fixes every neutral label. Therefore any categorification supplies the actual label-fixing tensor functor T=Ad(a)|D, not merely a permutation of a based ring. Coherent composition of inner functors gives

    T²≅⊗Ad(a²)|D=Ad(g).

The source has exactly two FP dimensions, 1 and d=2+sqrt(5). By the published Galois-conjugacy formulation of Schopieray, *Categorification of integral group rings extended by one dimension*, Lemma 3.1, a complex categorification has a pseudo-unitary Galois conjugate. Apply this to the entire category, including a and its inner tensor functor. The neutral subcategory D is pseudo-unitary with dimensions (1,1,d,d).

Here we explicitly reuse two retained, separately audited theoretical lemmas: [`CONDUCTOR_EQUALITY_LEMMA.md`](../../unified_20261016/compression/CONDUCTOR_EQUALITY_LEMMA.md) and [`SATURATED_CHARACTER_INDICATORS.md`](../../unified_20261016/rank8/SATURATED_CHARACTER_INDICATORS.md). Neither uses an associator transport for the neutral category. Their precise input and consequence in the present case are as follows.

Put D₀=20+8sqrt(5), with conjugate D₀'=20−8sqrt(5). The four formal codegrees are D₀,D₀',4,4, and the unit/quadratic-partner difference in the twist-one dimension block has compressed S-eigenvalue

    1/D₀−1/D₀'=−1/sqrt(5).

Its quadratic torus character has conductor5, so this attains the compression bound. The conductor-equality lemma says its cyclic modular subrepresentation factors through level5. Consequently every central simple A outside I(1) whose dimension ratio dim(A)/D₀ has a nonzero quadratic coordinate has twist of order dividing5. Terms in I(1) have twist1.

For clarity, the signed indicator step can be given in full. Let ell(z) be the rational coordinate of z/D₀ in the nontrivial quadratic character component, scaled so that its values on (1,g,r,s) are (2,2,−1,−1). Choose a cyclotomic automorphism sigma with exponent k modulo5, using CRT to make the exponent coprime to the full cyclotomic conductor. Let pi and epsilon_A be its modular permutation and signs, and write z_A=dim(A). Modular Galois symmetry gives

    z_(pi A)=epsilon_A (D₀/sigma(D₀)) sigma(z_A),
    ell(z_(pi A))=epsilon_A chi5(k) ell(z_A),
    theta_(pi A)=sigma²(theta_A).

The signs cancel in

    sigma(ell(z_A)z_A)
      =chi5(k)(sigma(D₀)/D₀)ell(z_(pi A))z_(pi A).

The first induction trace, weighted by ell, is

    sum_A ell(z_A)z_A theta_A=D₀ ell(1).

Apply sigma and reindex by pi. Every nonzero term has twist dividing5, including twist1 terms from I(1). If h is the inverse of k modulo5, sigma(theta_A)=theta_(pi A)^h. Cancel sigma(D₀) and apply the induction indicator formula to obtain

    sum_X ell(dim X)nu_h(X)=chi5(k)ell(1).

Inversion permutes the unit residues and preserves their quadratic character. Thus the same formula holds with h renamed k. At k=2 it is

    2+2nu₂(g)−nu₂(r)−nu₂(s)=−2.

All three labels are self-dual simples, so these indicators are signs. This forces nu₂(g)=−1 and nu₂(r)=nu₂(s)=1, exactly the hypotheses of the theorem. No cubic indicator or decorated rotation is needed in the proof below.

This completes the reduction of R8_2_24 to the theorem. The source-binding checker [`verify_r24_source.py`](verify_r24_source.py) checks the hash, all64 neutral coefficients, source associativity, the actual invertible a, and its neutral conjugation action; it does not purport to check any categorical argument.

## 1. A local pivotal calculation

Use a strict monoidal rigid realization retaining its pivotal structure and the explicitly specified simple self-duality identifications; the pivotal map j need not be the identity. Let Z and gZ have indicator +1, and let g have indicator −1 and positive categorical dimension 1, as guaranteed by pseudo-unitarity. Choose dual objects g*=g and Z*=Z with identity self-duality identifications. Thus the pivotal maps on these simples are j_g=−id_g and j_Z=id_Z. Put e=ev_g:g²→1. The pivotal trace identity dim(g)=−e coev_g=1 fixes the sign of the coevaluation. Then

    coev_g=−e⁻¹,
    e⊗id_g=−id_g⊗e : g³→g,
    e*=−e⁻¹.                                             (1)

Use the inner tensor functor F(X)=gXg with tensorator and unit

    J_X,Y=−id_gX⊗e⊗id_Yg : F(X)F(Y)→F(XY),
    J_0=e⁻¹:1→F(1).

This is a representative of the usual inner autoequivalence class. With these duality choices, ordinary inner conjugation has tensorator +e and unit −e⁻¹; the natural isomorphism with component −id gives the displayed convention.

The monoidal identification of its square with the identity is

    η_X=−e⊗id_X⊗e : ggXgg→X.                            (2)

The signs in these formulas follow directly from (1). In particular, the adjacent contraction e⊗id_X⊗e has the wrong sign on the unit of F²; its negative is monoidal. The canonical dual comparison on Z is

    δ_Z:F(Z*)→F(Z)* = −id_gZg.                           (3)

Indeed the transported evaluation is

    J_0⁻¹ F(ev_Z) J_Z*,Z
      =−e (id_g⊗ev_Z⊗id_g)(id_gZ⊗e⊗id_Zg),

which is the negative of the usual nested evaluation of gZg.

Choose any nonzero c:gZ→Zg. For arbitrary self-duality maps φ_g,φ_Z, the map ψ=(φ_Z⊗φ_g)c is a self-duality of gZ. The defining FS identity ψ* j_gZ=ν₂(gZ)ψ implies

    (φ_Z⁻¹⊗φ_g⁻¹)c*(φ_g⊗φ_Z)
      =[ν₂(gZ)/(ν₂(g)ν₂(Z))]c=−c.

Thus in the chosen identity charts, c*=εc with ε=−1. Define

    q=(id_Z⊗e)(c⊗id_g):gZg→Z,

and the nonzero scalar κ by

    (id_Z⊗e)(c⊗id_g)(id_g⊗c)
      =κ(e⊗id_Z):ggZ→Z.                                 (4)

Dualizing q and using (1) gives

    q*=−ε(id_g⊗c)(e⁻¹⊗id_Z),
    qq*=−εκ id_Z.

Relative to (3), the form defect γ of q therefore equals εκ. In detail, q*φ_Zq=γδ_ZF(φ_Z), whose two sides in these charts are respectively −εκ id and −γ id.

The composition defect λ is defined by qF(q)=λη_Z. It is κ. An explicit calculation, with identity subscripts suppressed, is

    qF(q)
      =(Z e)(c g)(g Z e g)(g c g g)
      =(Z e)(Z g e g)(c g g g)(g c g g)
      =−(Z e e)(c g g g)(g c g g)
      =−κ(e Z e)=κη_Z.                                   (5)

The second equality is interchange, the third is e(g e g)=−(e⊗e), and the fourth is (4) tensored with e. Consequently

    λ/γ=−1.                                               (6)

The ratio is unchanged by rescaling q, since both defects are multiplied by the same square.

Apply this calculation with Z=r. On H=Hom(r²,r), let K be the action of F in the q-chart. Let β(f,h)=tr_r(fhᵗ), using the full categorical transpose from the symmetric self-duality of r. Composition duality and semisimplicity give a nondegenerate pairing; involutivity of transpose and transpose-invariance of spherical trace make it symmetric. Equations (2) and (6) give

    K²=λ⁻¹ id_H,
    β(Kf,Kh)=γ⁻¹β(f,h)=−λ⁻¹β(f,h).                      (7)

Hence K is not scalar: a scalar matrix would have identical square and pairing multipliers. Since dim H=2, K has two distinct opposite eigenvalues. In particular its projective class is a nontrivial involution. This local fact is independent of every choice of normalization of c or q.

## 2. One simultaneous chart for a putative square root

Suppose T²≅⊗F. A tensor autoequivalence preserves the canonical pseudo-unitary pivotal structure. First fix its unit chart using its monoidal unit map. Choose simple-object identifications for T(g) and T(r), and rescale them so that the induced action fixes e and ev_r. Both rescalings are possible independently over C. Extend these identifications multiplicatively, using the tensorator, to all strict words in g and r. Coherence then makes the transported action strictly multiplicative on these words. Define the identification of T(s) with s from the word s=gr; do not independently rescale it. Distinct words that represent isomorphic objects are connected by the explicitly displayed morphisms, not by additional identifications.

The induced action on the one-dimensional space Hom(gr,rg) sends c to αc. Applying T to (4), with Z=r, shows α²κ=κ, hence α=±1. This uses only the fixed e and the nonzero double-crossing scalar, not a choice of pivotal rotation convention.

The operator K above is homogeneous of degree −1 in c: q occurs once on the output and q⁻¹ twice on the inputs. All its other structural maps are fixed. Therefore

    T_H K T_H⁻¹=α⁻¹K.                                    (8)

If α=−1, T_H exchanges the two K eigenlines, so T_H² is scalar. This is incompatible with its projective square being [K], a nontrivial involution. Thus α=+1.

All morphisms composed from e,c,c⁻¹,ev_r and the corresponding cups are now fixed by T. In particular, the nonzero form

    ev_s=(e⊗ev_r)(id_g⊗c⁻¹⊗id_r):grgr→1                (9)

is fixed in this same induced s-chart. Its associated self-duality is symmetric because ν₂(s)=1. This construction is the reason that no independent normalization of s, and no hidden scalar on mixed channels, is allowed or needed.

For X=r,s define the full-transpose form on V_X=Hom(r²,X) by

    B_X(f,h)=tr_X(fhᵗ).

The self-duality on r² is the tensor product of the two r self-dualities, using the reversed dual order. Since both factors are r, it has the same domain and codomain as required. All the incident self-duality signs are +1; hence transpose is involutive, B_X is symmetric, and composition duality makes it nondegenerate. The fixed forms on r and s imply that T preserves B_X exactly. Thus

    T_H∈O(2,C),    T_J∈O(2,C),   J=Hom(r²,s).             (10)

An orthogonal matrix in dimension two with determinant −1 squares to the identity. Since T_H² is projectively nontrivial, det(T_H)=+1. Choose a hyperbolic basis of H. Then

    T_H=diag(u,u⁻¹),    u⁴=−1.                            (11)

The second equation follows because [T_H²]=[K] is a nontrivial involution: its eigenvalue ratio is −1. For J, there are two cases. If det(T_J)=+1, choose a hyperbolic basis with T_J=diag(v,v⁻¹). If det(T_J)=−1, choose an eigenbasis with T_J=diag(1,−1). No local statement about an inner loop on J is used.

## 3. Transporting all fusion spaces

Write g_a=g^a and r_a=g^a r for a∈F₂. Thus g_0=1,g_1=g,r_0=r,r_1=s. The complete rules are

    g_a g_b=g_(a+b),
    g_a r_b=r_(a+b)=r_b g_a,
    r_a r_b=g_(a+b)+2r_(a+b)+2r_(a+b+1).

All multiplicity-one vertices have bases formed from the fixed structural maps. This includes the evaluations r_a r_b→g_(a+b). To make the two-dimensional transports explicit, choose

    A_ab:r_a r_b→g_(a+b)r²

as follows:

    A_00=id,  A_10=id,
    A_01=c⁻¹⊗id_r,
    A_11=(e⊗id_r²)(id_g⊗c⁻¹⊗id_r).

For m=a+b choose B_abc:r_c→g_m r_(m+c) to be the identity when m=0 or c=1, and e⁻¹⊗id_r when m=1,c=0. For f:r²→r_(a+b+c), its transported vertex is

    B_abc⁻¹(id_gm⊗f)A_ab : r_a r_b→r_c.                  (12)

Every structural transport map in (12) is fixed by T; f itself carries the H or J action. Hence these vertices have exactly the H action when a+b+c=0 and exactly the J action when a+b+c=1. There are no additional scalar characters. The thin vertex r_a r_b→g_m is (id_gm⊗ev_r)A_ab. The remaining thin maps use e,c and the unit maps. Incoming bases are composition-dual and have inverse eigenvalues.

Choosing one such transport for each fusion space suffices. No equality between different transport paths is asserted.

## 4. A uniform bound on every associator weight

First consider det(T_J)=+1. Give the two H basis vectors weights ±(1,0), the two J vectors weights ±(0,1), and all thin vertices weight (0,0). These define a two-dimensional diagonal gauge torus U(z,w). Every F coefficient has the signed sum of its four vertex weights.

Every such weight lies in

    W={(p,q)∈(2Z)²: |p|+|q|≤4}.                         (13)

Here is a proof including all labels and all scalar channels. Represent an F coefficient by its six-edge, four-vertex tetrahedral incidence pattern. Mark its noninvertible edges. A vertex has 0,2 or3 marked incident edges, and it is thick precisely when it has3. Summing marked incidences counts each edge twice, so the number of thick vertices is even. Next assign bit a to both g_a and r_a. A thin or H vertex has incident bit sum0; a J vertex has bit sum1. Summing the four vertex sums again counts every edge twice, so the number of J vertices is even. The number of H vertices is therefore even too. Each contributes ±1 to its coordinate, proving evenness; there are only four vertices, proving the norm bound.

Let L be the integer lattice generated by weights of actual nonzero F entries. Monoidality of T gives u^p v^q=1 for each such weight. If L has rank two, it contains (4,0) and (0,4). Indeed two independent nonzero vectors from W already generate these vectors: after dividing by2, the possible vectors are axes of length1 or2, and diagonals (±1,±1). Two independent axes, an axis and a diagonal, or two independent diagonals each contain both doubled coordinate axes in their span over Z. Thus u⁴=v⁴=1, contradicting (11).

If L has rank below two, its annihilator in (C×)² contains a positive-dimensional torus. Every element of this torus fixes every F entry.

Now consider det(T_J)=−1. Its two eigenvalues are +1 and −1. Track only the H exponent p in each F entry. The same counting proof gives p even and |p|≤4. If p=±2, the H factor u^p is ±i, which cannot be canceled by the J factors ±1 or thin factors1. If p=±4, all four vertices are H vertices; there is no J factor, and u^p=−1. Such coefficients vanish. Therefore every nonzero F entry has H exponent0, and the one-dimensional torus acting diag(t,t⁻¹) on each transported H space and identically on every other space fixes all F entries.

## 5. Tensor-functor rigidity gives the contradiction

In either case a positive-dimensional diagonal gauge torus fixes the entire associator and every unit channel. In a skeletal semisimple realization, its fusion-space matrices are tensorators for the identity underlying linear functor; invariance of all F matrices is exactly their monoidal coherence equation.

These tensor functors remain infinitely many after quotienting by monoidal natural isomorphisms. Such an isomorphism has scalar components on simple objects, so its induced change on H=Hom(r²,r) and J=Hom(r²,s) is scalar. A nonconstant diagonal torus has a varying projective eigenratio on at least one of H,J, which these scalar changes cannot remove.

This contradicts ENO Theorem 2.31, which gives only finitely many tensor functors up to equivalence between two fixed fusion categories. The assumed square root T does not exist. ∎

## Application and checking scope

Section0 supplies the category D, the indicators in the theorem, and T=Ad(a)|D with a²=g, after Galois passage to the pseudo-unitary setting. The theorem therefore excludes a complex categorification of R8_2_24. The categorical proof remains subject to independent human verification and Lean formalization; the finite checks certify only their stated source and combinatorial claims.

The independent local derivation is also recorded in [`R24_TYPED_INNER_DUALITY_AUDIT.md`](R24_TYPED_INNER_DUALITY_AUDIT.md). The finite checker `verify_full_f_weights.py` enumerates 136 nonempty F blocks and 1472 coefficient slots, checks 104 ordered independent weight pairs and 5888 reflection-case phases. It certifies the combinatorial claims only; it is not a substitute for the categorical proof.

Primary rigidity source: P. Etingof, D. Nikshych and V. Ostrik, *On fusion categories*, Annals of Mathematics 162 (2005), 581–642, Theorem 2.31, p.592; https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf .

Galois reduction reference: A. Schopieray, *Categorification of integral group rings extended by one dimension*, Journal of the London Mathematical Society108 (2023),1617–1641, published Lemma3.1; https://doi.org/10.1112/jlms.12789 .
