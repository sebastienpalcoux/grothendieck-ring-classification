# R9_2_1975: the Galois-unit object contradicts a forced projective parity

**Conclusion: R9_2_1975 has no fusion categorification over C**, using the
previously audited TY/Morita and general-to-pseudo-unitary reductions and the
new two-part obstruction below. The first part removes reflection duality;
the second removes rotation duality. There is no new model and no numerical
search over pentagons.

This is an offline research result. No public classification files have been
changed. The source snapshot and dependencies are specified in `REPORT.md`.

## 1. The necessary Morita category

The existing reduction of an arbitrary hypothetical complex categorification
of R9_2_1975 produces a rank-twelve Morita category. Its earlier extreme branch
was excluded in the project. In the two surviving uniform branches its
invertibles form G=D8, H=Z(G)=C2, Q=G/H=V4, and its other four simples are X_q,
q in Q, with

    g X_q = X_q g = X_(q+gH),
    X_p X_q = sum_(gH=p+q+alpha) g + 2 sum_(t in Q) X_t,
    X_q* = X_(q+alpha).

Here d=FPdim(X_q)=4+3sqrt(2), d²=2+8d, and
D=8+4d²=144+96sqrt(2). The shift alpha is a reflection or rotation coset.

The independently replayed signed gate `phase2/signed/gate_R9_2_1975.json`
proves that any complex source categorification has a Galois conjugate which
is pseudo-unitary. Its exact source hash agrees with the input here. Taking
the actual Morita dual preserves pseudo-unitarity: both intrinsic global
dimension and FP dimension are Morita invariant. This is an existence
reduction, not a claim that every original category is unitary. A fresh
independent bounded replay checks both signed branches and final completeness;
see `../r6_1660/r1975_gate_replay_receipt.json`. The new pointed-bimodule
arguments themselves are valid over C without a pivotal or unitary assumption.

The pointed subcategory is Vec_G^omega. Its full associator class, not only its
cyclic restrictions, is determined by the previous TY-origin calculation and
the H³(D8,C*) detection argument in `rank9/POINTED_BIMODULE.md`, Section 2.
Use exactly the cocycle and coordinate convention in `REPORT.md`. The present
commutators work for both possible TY signs, so the earlier negative-sign
restriction and third-indicator argument are not needed for this exclusion.

## 2. Duality forces a nontrivial diagonal projective commutator

The acting group K=G x G acts by (g,k)X=gXk^-1. The stabilizer of X_0 is
L=G x_Q G, written as G x C2 by (g,e) -> (g,gz^e). Put

    p=(1,0,0), s=(0,0,1), z=(ps)^2=(1,1,0),
    P=(p,0), S=(s,0), Z=(z,0), E=(1,1) in L.

The pointed-bimodule cochain has the form beta' = beta gamma, where beta is
the displayed cochain of `REPORT.md`, and gamma is an **arbitrary complex**
ordinary two-cocycle on L. For commuting elements write

    C_gamma(A,B)=gamma(A,B)/gamma(B,A).

Let T exchange the two K-factors, and let phi_q be the stabilizer automorphism
induced by conjugation with (q,1). Categorical duality with shift qH requires
the two-cocycle

    c'_q = phi_q^*(beta') * kappa_q * T^*(beta')

to be a coboundary. The normalizer correction kappa_q and this precise opposite
convention are justified in `REPORT.md`, Section 2, from Vainerman--Vallin,
Sections 2.2.1, 2.2.2 and 3.1.1. This uses duality of a bimodule, not a claim
that the full rank-twelve category is Z2-graded.

The already proved invariant

    C_(c'_q)(P,E) C_(c'_q)(S,E) = (-1)^(x+y+n), q=(x,y,n),

excludes both reflection cosets for every gamma. Therefore only the rotation
coset remains; take q=ps=(0,1,1), or its other lift qz.

For either rotation lift, direct substitution in the displayed beta gives

    C_(c_q)(P,E)=1,                 C_beta(P,Z)=-1.                 (1)

The change in the first expression upon replacing beta by beta gamma is
exactly C_gamma(P,Z). Here is a proof covering all complex gamma. Since E is
central, C_gamma(-,E) is a character, kills Z=[P,S], and has square one on P.
For some a in F2,

    phi_q(P)=P(ZE)^a,  phi_q(E)=E,  TP=P,  TE=ZE.

Thus

    C_(phi_q^*gamma)(P,E) C_(T^*gamma)(P,E)
      = C_gamma(P,E)^2 C_gamma(P,Z)
      = C_gamma(P,Z).

Every coboundary has trivial commutator on commuting pairs. Duality and (1)
therefore imply C_gamma(P,Z)=1 and hence

    C_(beta')(P,Z) = -1.                                      (2)

This implication is insensitive to arbitrary cochain gauges and imposes no
root-of-unity bound. Indeed the rotation duality equation by itself has an
eighth-root trivialization; its consistency was checked separately and must
not be mistaken for the contradiction proved next.

## 3. Every central restriction has even multiplicity at X_0

Restrict to the even subgroup A=<p,z>=V4 of G. The chosen omega is identically
one on A³. Consequently the diagonal A action X -> gXg^-1 has the ordinary
strict pointed convention, with no nontrivial opposite/rigidity cocycle on A.
In particular its stabilizer multiplier at X_0 is beta' restricted to the
diagonal A, or its inverse according to the direction of the structure maps.
Either direction has commutator -1 at P,Z by (2).

For any object W in the Drinfeld center of the rank-twelve category, its
half-braiding with Vec_A gives a diagonal A-equivariant structure on F(W).
Conjugation by A fixes each X_q. Therefore the X_0-isotypic multiplicity space
V=Hom(X_0,F(W)) is invariant and carries a projective A-representation with
the preceding multiplier. The two invertible operators U_p,U_z satisfy

    U_p U_z = - U_z U_p.

Taking determinants shows (-1)^dim(V)=1. Thus

    [F(W):X_0] is even for every W in Z(C').                    (3)

This short argument uses only the strict even V4 subcategory. It does not
assume that a global diagonal D8 tensorator has been normalized trivially.
It does not use Frobenius--Schur indicator signs, a pivotal square coherence,
unitarity, or a classification of arbitrary spherical categories.

## 4. The Galois-unit restriction has multiplicity one at X_0

We apply the project's Galois-unit argument directly to the pseudo-unitary
rank-twelve Morita category, rather than trying to transfer source restriction
vectors through Morita equivalence.

Let sigma send sqrt(2) to -sqrt(2). The algebra of the displayed uniform ring
has eight scalar irreducibles and one irreducible of degree two. Explicitly:

* For the trivial character of Q, all g act by 1 and all X_q act by d or
  d'=4-3sqrt(2). Their formal codegrees are D and D'=sigma(D).
* For each of the three nontrivial characters psi of Q, there are two scalar
  representations g -> psi(gH), X_q -> t psi(q), where t²=2 psi(alpha).
  Each has formal codegree 8+4*2=16.
* The two-dimensional irreducible of D8 extends by X_q -> 0: z acts by -I,
  and each group coset sum in X_p X_q is zero on it. Its formal codegree is
  |G|/2=4. The regular Casimir acts on this block by 2*4=8, not by 4.

These are all irreducibles since 8*1²+1*2²=12. For

    v=1+sum_(q in Q) X_q,

the central scalar on a rational-codegree irreducible is 1, while on the two
dimension characters it is

    1+4d = D/D',       1+4d' = D'/D.

Thus on every irreducible E, v acts by f_E/sigma(f_E).

For completeness, the categorical Galois argument also retains the degree
normalization. Let A_E be the distinguished simple in I(1), with
dim(A_E)=D/f_E. Let B=A_(sigma FP). On a central class let
lambda_E=chi_E/dim(E) denote the scalar eigenvalue. The central-character
identity and the symmetry of the unnormalized modular S matrix give

    (D/f_E) lambda_E(F(B))
      = S_(A_E,B) = S_(B,A_E)
      = (D/D') (sigma FP)(F(A_E))
      = (D/D') sigma(D/f_E) = D/sigma(f_E).

Therefore lambda_E(F(B))=f_E/sigma(f_E). The two central elements F(B) and v
agree on every irreducible of a semisimple algebra, and hence are equal:

    F(B)=1+X_0+X_1+X_2+X_3.                                  (4)

The distinguished-object theorem is Ostrik, Theorem 2.13 and Section 2.3,
and the central-character identity is also given by Deshpande, Proposition
2.8 and Section 2.7. The project's independently audited noncommutative
extension is `phase3/audit_quadratic_symmetry/GALOIS_UNIT_AUDIT.md`.

Equation (4) has multiplicity one at X_0, contradicting (3). Therefore the
rotation branch is impossible. With the reflection obstruction and the prior
extreme-branch exclusion, no Morita alternative remains. The existing
general-complex existence reduction proves the claimed exclusion of
R9_2_1975.

## 5. Exact replay, dependencies and review

`verify_duality_obstruction.py` checks the cochain identities and the
all-complex commutator theorem's explicit input. `verify_galois_parity.py`
binds to the archived original and rotation tensors, checks their source
hashes, checks (1), the triviality of omega on A³, the complete fusion-rule
formula, and the full rational matrix identity reconstructing (4). It does
not enumerate possible associators or center objects.

The essential previous dependencies are:

* `unresolved11_20261024/rank9_noncommutative/NEW_RESTRICTIONS.md`:
  source TY structure, Morita alternatives, exclusion of the extreme branch,
  and historical reductions.
* `rank9_m2_20261024/proofs/phase2/signed/THEOREM.md` and the archived
  `gate_R9_2_1975.json`, freshly replayed in
  `../r6_1660/r1975_gate_replay_receipt.json`: the direct source
  Galois-to-pseudo-unitary existence reduction.
* `unresolved11_retry_20261024/rank9/POINTED_BIMODULE.md`, Sections 1--3:
  the full pointed associator class and stabilizer convention. The cubic
  indicator argument in its Section 4 is not needed here.
* `rank9_m2_20261024/proofs/phase5/quadratic_comm/ty_module_subtask/`:
  the prior TY-origin associator proofs.

Independent categorical, normalization and general-scope review is recorded
in the sibling agents' audit reports; the present argument was revised to
use only the strict even V4 for the projective-parity step.

The source gate's original archive is `evidence/rank9_m2_20261024/replay.zip`,
SHA-256 `38b4339c86c71fdba65cc7a72df57b16248b508f11dbe8fdb2016c43d77e6ff2`.
Morita invariance is ENO, *On fusion categories*, Theorem 2.15 and Corollary
8.14, https://arxiv.org/pdf/math/0203060. No assertion that an arbitrary
fusion category is spherical or unitarizable is inserted into this proof.

Primary references:

1. L. Vainerman, J.-M. Vallin, *On Z/2Z-extensions of pointed fusion
   categories*, https://arxiv.org/pdf/1210.1732, Sections 2.2.1, 2.2.2, 3.1.1.
2. V. Ostrik, *Pivotal fusion categories of rank 3*,
   https://arxiv.org/pdf/1309.4822, Section 2.3 and Theorem 2.13.
3. T. Deshpande, *On centers of bimodule categories and induction-restriction
   functors*, https://arxiv.org/pdf/1611.04486, Proposition 2.8 and Section 2.7.
4. C. Goff, G. Mason, S.-H. Ng, *On the gauge equivalence of twisted quantum
   doubles of elementary abelian and extra-special 2-groups*,
   https://arxiv.org/pdf/math/0603191, Lemmas 4.4--4.5 (prior associator gate).
