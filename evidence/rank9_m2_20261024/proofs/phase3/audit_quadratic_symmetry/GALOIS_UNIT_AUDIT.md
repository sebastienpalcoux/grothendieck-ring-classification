# Independent audit of the Galois-unit restriction criterion

**Accepted.** The criterion gives general complex exclusions of
R9_2_114, R9_2_128, R9_2_1487, R9_2_1635, R9_2_1636 and R9_2_1959 after their
separately audited signed Galois-to-pseudo-unitary gates. The exact independent
replay is `replay_galois.py`, with results in `replay_galois.json`.

## The categorical identity

Suppose C is pseudo-unitary, its based ring R is commutative, its FP-dimension
field is the real quadratic field K, and every formal codegree belongs to K.
Write D=FPdim(C), let σ be the nonidentity automorphism of K, and let B be the
distinguished central simple corresponding to the scalar character σ∘FPdim.
Then dim(B)=D/σ(D) and [1:F(B)]=1.

For any scalar irreducible character χ_h, with formal codegree f_h, let A_h be
its distinguished simple in I(1). The induction-character formula and symmetry
of S give

    (D/f_h) χ_h(F(B))
      = S_(A_h,B)
      = S_(B,A_h)
      = (D/σ(D)) (σ∘FPdim)(F(A_h))
      = (D/σ(D)) σ(D/f_h)
      = D/σ(f_h).

Therefore

    χ_h(F(B)) = f_h/σ(f_h).

This proof does not require χ_h itself to take values in K. Only the dimension
of A_h and its formal codegree must lie there. This distinction matters for
several cases in the sweep. The normalization of S and the correspondence
between χ_h and A_h were checked against Deshpande, arXiv:1611.04486,
Proposition 2.8 and Section 2.7, equations (36),(39).

Let C_R be the regular fusion Casimir, the matrix of left multiplication by
Σ_i bi bi*. In the commutative case it acts on χ_h by f_h. There is a rational
polynomial p such that p(f_h)=f_h/σ(f_h) for every h: modulo a rational linear
codegree factor use the residue 1, and modulo a monic quadratic factor with
constant term n use t²/n. The latter equals f_h/σ(f_h), because
f_h σ(f_h)=n. The distinct factors are coprime, so the polynomial exists by
rational interpolation. All characters of R have thus agreed on

    N_(F(B)) = p(C_R).

The regular representation is faithful, and its row at the unit is exactly
the based coefficient vector of F(B). This row must be a nonnegative integer
vector with unit coefficient one. A fractional entry is a categorical
contradiction, independent of all center-column enumeration or LP relaxations.

## Fresh exact reconstruction

The independent replay imports no developing-agent criterion, uses no stored
polynomial, and does not enumerate center candidates. It reconstructs the raw
fusion matrices and scalar algebra, checks the quadratic FP field, and verifies
that every codegree factor has all its roots in that field. Rather than using
the developing Chinese-remainder implementation, it builds the rational linear
system whose columns are the remainders of 1,t,t²,… modulo every distinct
codegree factor, and solves for p's coefficients.

It then checks the full matrix equality

    p(C_R) = Σ_i vi N_i,

checks its eigenvalue formula in every irreducible character field, and checks
that the vector has dimension D/σ(D). The six fractional restrictions are:

| Ring | Forced restriction in source order |
|---|---|
| 114 | (1,0,0,0,1/2,1/2,1,0,0) |
| 128 | (1,0,0,1/2,1/2,1/2,1/2,0,0) |
| 1487 | (1,1/2,1/2,0,0,0,0,1/2,1/2) |
| 1635 | (1,1/2,1/2,0,0,0,0,0,1) |
| 1636 | (1,1/2,1/2,0,0,0,0,1/2,1/2) |
| 1959 | (1,1/2,1/2,1/2,1/2,0,0,0,0) |

The independently established unitary models 96,1266,1983 all pass. The still
undecided cases 137,1607,1976 pass this necessary condition; no realization is
inferred for them.

The signed gates are `phase2/signed/gate_R9_2_<ID>.json`; their full general
scope was independently audited in this phase. Thus failure of the criterion
excludes all complex categorifications of the six listed rings.

## Noncommutative extension

The same argument works when an irreducible E has degree e_E: on a central
class v, write λ_E(v)=χ_E(v)/e_E for its scalar eigenvalue. Then
S_(A_E,Z)=(D/f_E)λ_E(FZ), so λ_E(FB)=f_E/σ(f_E). The regular Casimir acts by
e_E f_E, whose ratio to its σ-conjugate is again f_E/σ(f_E), because e_E is
an integer. Hence one can interpolate the regular Casimir's distinct factors
directly, provided they all split in K. Equivalently normalize its action by
the representation-degree operator first; these constructions coincide.

An independent degree-normalized implementation under
`../noncomm1975/galois_unit.py` gives nonnegative integral vectors for both
1975 and1848, so it yields no exclusion there. This extension has no missing
factor of e_E in the character normalization.

Primary source checked: https://arxiv.org/pdf/1611.04486 . The rational
interpolation and the resulting integrality obstruction are the deductions
made here from that induction-character identity and modular S symmetry.
