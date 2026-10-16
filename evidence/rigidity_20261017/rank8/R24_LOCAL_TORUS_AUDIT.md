# Independent local audit of the R24 torus argument

Research checkpoint. This note independently checks the local pivotal argument in
`../unified/R24_TYPED_INNER_DUALITY_AUDIT.md` and its compatibility with the
normalization in `../r24/TORUS_RIGIDITY_DRAFT.md`. It does not change any published
classification. The argument here is mathematical; no finite computation is
being represented as a proof of a categorical statement.

## 1. Intrinsic forms, with all map types

Let the category be pivotal and semisimple over C. Let r and X, where X=r or s,
have second indicator +1. Choose symmetric self-dualities
`phi_r:r→r*` and `phi_X:X→X*`. Put A=r⊗r and
`u_A=phi_r⊗phi_r:A→A*`; reversing the dual tensor order causes no type problem
because the two factors agree. For h:A→X define

    t_X(h)=u_A^-1 h* phi_X : X→A,
    B_X(f,h) id_X = f t_X(h).

This is a C-bilinear form. Transpose reverses composition and squares to the
identity on these Hom spaces. Hence transposing the scalar composite shows
`B_X(f,h)=B_X(h,f)`. The composition pairing
`Hom(A,X) × Hom(X,A)→End(X)=C` is nondegenerate by semisimplicity, and t_X is
an isomorphism; therefore B_X is nondegenerate. This argument uses neither a
dagger nor a choice of basis and its composition-dual. In particular, it does
not import a basis-dependent form from Fuchs--Groesfjeld or identify this form
with an EIP partial bend.

Any pivotal tensor autoequivalence whose chosen object charts preserve these
self-dualities preserves B_X exactly. One can equally use the pivotal trace of
the displayed scalar composite; that just multiplies B_X by dim(X).

## 2. Independent check of the inner-functor sign ratio

Use a strict monoidal rigid realization with a pivotal structure, choosing
right duals g*=g and Z*=Z and self-duality identifications equal to identities.
Here j_g=-id and j_Z=id; this does not mean that the pivotal structure is
strictly the identity. Let `e=ev_g:gg→1`. Its coevaluation is `-e^-1`, and

    e g = -g e : ggg→g,              e*=-e^-1.

For F=g(-)g use the monoidal constraints

    F_2(X,Y)=-gX e Yg,       F_0=e^-1,
    eta_X=-e X e : F²(X)→X.

The signs in the unit triangle and in eta follow from `e g=-g e`. The standard
nested evaluation on gZg is `e(g ev_Z g)(gZ e Zg)`, while transport through F is
its negative. Thus the canonical duality comparison is `delta_Z=-id`.

For a nonzero crossing `c:gZ→Zg` let epsilon be the scalar of its transpose in
the chosen self-duality charts. More invariantly,

    tau(c)=(phi_Z^-1⊗phi_g^-1)c*(phi_g⊗phi_Z):gZ→Zg.

The self-duality `psi=(phi_Z⊗phi_g)c:gZ→(gZ)*` obeys
`psi* j_(gZ)=nu2(gZ) psi`. Expanding this equality using
`phi_Y* j_Y=nu2(Y) phi_Y` gives

    tau(c)=epsilon c,
    epsilon=nu2(gZ)/(nu2(g)nu2(Z))=-1.

This identity is unchanged by rescaling c. Define

    q=(Z e)(c g):gZg→Z,
    (Z e)(c g)(g c)=kappa(e Z):ggZ→Z.

The last scalar is nonzero since every constituent is invertible. Dualizing
q gives `q*=-epsilon(g c)(e^-1 Z)`, so

    qq*=q*q=-epsilon kappa id.

Relative to delta_Z, the self-duality defect in
`q* phi_Z q=gamma delta_Z F(phi_Z)` is therefore
`gamma=epsilon kappa`.

Here is the square calculation with the intermediate typed composites made
explicit. Each line is a map `ggZgg→Z`:

    qF(q)=(Z e)(c g)(gZ e g)(g c gg)
          =(Z e)(Zg e g)(c ggg)(g c gg)
          =-(Z e e)(c ggg)(g c gg)
          =-kappa(e Z e)
          =kappa eta_Z.

The second equality interchanges operations on disjoint tensor factors. The
third uses `e(g e g)=-(e⊗e)`, itself an immediate consequence of `e g=-g e`.
Thus the square defect lambda is kappa, and

    lambda/gamma=epsilon=-1.

Rescaling q multiplies lambda and gamma by the same square. In particular the
ratio is intrinsic to the charts under consideration, and no absolute
normalization of kappa is required.

On H=Hom(Z²,Z), the induced action K obeys

    K²=lambda^-1 I,
    B_Z(Kf,Kh)=gamma^-1 B_Z(f,h).

The exponent -1 in both expressions is the one output chart minus the two
input charts. Since the two scalar multipliers are opposite, K cannot be
scalar. In dimension two K has two distinct opposite eigenvalues. Each
eigenline is isotropic for B_Z: on that line the eigenvalue square is
lambda^-1, whereas the form multiplier is -lambda^-1. Nondegeneracy pairs
the two lines. This proves the local H-loop claim independently of unitarity.

## 3. Common normalization for the square-root functor

Let T be a C-linear tensor autoequivalence fixing the labels. In the
pseudo-unitary setting T preserves the canonical pivotal structure. Choose
its g and r object charts so that it fixes `e:gg→1` and the r evaluation form
`e_r:rr→1`. Each condition is achieved by a square-root rescaling of its own
simple chart, and the two rescalings are independent. Use the tensor product
chart for s=gr, rather than independently rescaling s.

The action on c is multiplication by a nonzero scalar alpha. The two chart
rescalings cancel from this scalar because both source and target of c
contain one g and one r. Apply T to the defining double-pass identity for
kappa. It fixes e and kappa, and replaces its two c factors by alpha c;
therefore alpha²=1.

For alpha=+1 a suitable s evaluation is the explicitly typed composite

    e_s=e_r (r e r)(c g r):g r g r→1.

This is the evaluation associated to the self-duality
`(phi_r⊗phi_g)c:gr→(gr)*`. It is nonzero and is symmetric since nu2(s)=+1.
Every constituent is T-fixed, so e_s is T-fixed in the structural s chart.
Thus the two intrinsic forms B_r and B_s above are simultaneously T-invariant.
No independent s rescaling and no decorated partial-bend formula is needed.

All thin maps and every chosen transport from a thick fusion space to H or J
can be built from e, e_r, c, their inverses, and tensor products/composition.
For alpha=+1 these are all fixed. In particular this gives the exact, rather
than merely projective, eigenvalues in the transported bases needed by the
weight argument.

Finally, K_c is the action of F in a chart q linear in c. Its action on H
contains one q and two q^-1 factors, so `K_(alpha c)=alpha^-1 K_c`. Transport
by T commutes with inner conjugation by g through its chosen g chart; e is
fixed, so the tensorator and unit constraints above are fixed as well. Hence

    T_H K_c T_H^-1 = alpha^-1 K_c.

If alpha=-1, T_H interchanges the two distinct K_c eigenlines and T_H² is
scalar. But a monoidal isomorphism T²≅F identifies their actions on H up to a
scalar, contradicting the non-scalar projective action of K_c. A putative
square root must therefore have alpha=+1. Its H action is an isometry
commuting with K_c, hence `diag(u,u^-1)` in the paired eigenlines. Its square
has the projective eigenratio of K_c, giving `u^4=-1`.

## Audit conclusion

The intrinsic form construction, the inner-functor sign ratio, the crossing
sign dichotomy, and the common structural normalization all pass this
independent typed audit. These checks establish the local premises used by
the revised torus argument. The proof of the full associator weight bound and
the rigidity contradiction is a separate part of that argument and is not
replaced by this local audit.
