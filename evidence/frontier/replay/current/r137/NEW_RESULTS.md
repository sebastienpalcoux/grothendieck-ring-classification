# R9_2_137: the positive Tambara–Yamagami sign is excluded

## Accepted scope

**The ring remains unresolved.** This continuation excludes the positive
Tambara–Yamagami parameter in the necessary positive spherical representative.
The negative parameter is not excluded and no category is constructed.
The new exclusion uses the project's inherited complete center domain and its
previous proof that the positive TY branch has all four projected third
indicators equal to 1/2. It does not assume unitarity. Passing the domain and
its rational relaxations is not a categorification.

The mathematical additions are a full restriction-column Galois complement
and integral Verlinde coefficients for the Galois conjugate of the unit.
The latter excludes the positive TY branch through nine exact rational
inequalities, independently replayed on every permitted column.

## 1. An exact full-column complement

Use the census basis 0,...,8. The invertibles have indices 0,1,2,7;
Y=X8 has dimension 2; X3,...,X6 have dimension d=4+3 sqrt(2).
Write D=144+96 sqrt(2), D'=144-96 sqrt(2), r=D/D'=1+4d.
For a central simple Z write v=[FZ] and

    a=v0+v1+v2+v7+2v8,  b=v3+v4+v5+v6,  dim(Z)=a+bd.

All nine characters of the source fusion ring take values in K=Q(sqrt(2)).
For the distinguished simple A_E in I(1), its normalized modular row is

    s(A_E,Z)=chi_E(v)/f_E.

Let sigma be a modular Galois automorphism restricting nontrivially to K.
The signed column rule gives

    chi_E(v_sigmaZ) = epsilon_Z (f_E/sigma(f_E)) sigma(chi_E(v_Z)).

The exact nine-character calculation, verified against every product in the
source tensor, transforms v as follows:

    (Tv)i=vi                    for i=0,1,2,7,8;
    (Tv)i=a-vi                  for i=3,4,5,6.

Thus v_sigmaZ=epsilon_Z Tv. If a>0, at least one unchanged integral
coordinate is positive, forcing epsilon_Z=+1. Consequently every large
coordinate individually satisfies vi<=a. If a=0, T v=-v, positivity forces
epsilon_Z=-1, and the restriction column is unchanged.

The center's canonical anomaly is 1, so theta_sigmaZ=sigma^2(theta_Z).
Since sigma^2 fixes K, the normalized trace to K of every theta_Z^n is
unchanged. Therefore the total multiplicity of each (v, joint trace type)
equals that of (Tv, the same type), when a>0. Multiplicities are aggregated
over duplicate relaxation variables: no individual variable matching is
assumed.

For the published positive-TY domain, positivity removes 8,752 additional
variables beyond the previous filter. Missing partners in the *complete*
domain remove another 269, and 2,508 aggregate equalities remain. These
missing-partner deletions rely on domain completeness, not on an arbitrary
root-order cutoff.

## 2. Integral fusion coefficients from the known Galois row

Let B be the Galois conjugate of the central unit. The inherited character
argument forces

    F(B)=1+X3+X4+X5+X6,  dim(B)=r.

B is selfdual and appears once in I(1). Its complete normalized modular row is

    s(B,Z)=sigma(dim Z)/D' = (a+(4a-b)d)/D.

The source ring is commutative, so the nine A_E all occur once in I(1).
Their rows are real. Verlinde therefore gives

    N_{BB}^{A_E}
      = sum_Z ((a+(4a-b)d)^2 chi_E(v_Z))/(D (a+bd) f_E).

In particular,

    N_{BB}^{B}
      = sum_Z (a+(4a-b)d)^3/(D^2 (a+bd)).

These are linear functions of the actual numbers of central simples of each
restriction type. Every value must be a nonnegative integer. In the fixed
quadratic basis, its irrational coefficient must vanish.

The old positive-TY rational witness gives N_{BB}^B=5/6. Several other
coefficients even have nonzero irrational parts. It is therefore not
modular data. This observation alone rejects only that witness; the following
uniform bounds exclude its entire TY sign.

## 3. The finite integral contradiction

Write A0 for the distinguished character of codegree 4; A1±,A2± for the
two pairs of codegree 8; A3± for the pair of codegree 16. The remaining
characters are the FP character (central unit) and its conjugate (B).
Put n_E=N_{BB}^{A_E} and n_B=N_{BB}^B.

For the positive TY sign, the previously accepted complete third-indicator
argument forces all four projected third indicators to be 1/2. No value of
the fourth indicators is fixed here: the four old test equations setting
them to 2 are removed. Only the proved fourth-indicator bounds are retained.

The nine rational certificates prove:

| Assumptions added at this stage | Bounds |
|---|---|
| Necessary positive-TY center system and full Galois complement | 1/2 <= n_B <= 31/18 |
| Therefore n_B=1 | 0 <= n_{A3-}, n_{A3+} <= 17/30 |
| Therefore n_{A3-}=n_{A3+}=0 | 0 <= n_{A1-},n_{A1+},n_{A2-},n_{A2+} <= 3/4; 0 <= n_{A0} <=1 |

All these multiplicities are integers. Hence the four codegree-8
multiplicities also vanish. But adjunction and the exact source tensor give

    sum_E N_{BB}^{A_E} = [F(B^2):1] = 5.

The unit contributes 1, B contributes 1, and A0 contributes at most 1;
all six others contribute zero. The sum is at most 3, a contradiction.
Thus the positive TY sign is impossible.

Each certificate is of the form lambda*A + mu*U >= c, with mu>=0,
checked coefficientwise for all 5,996 allowed variables; its bound is
lambda*b. The exact values above are rational, not rounded solver values.
The solver only proposed the certificates. Their independent replay uses
integer and rational arithmetic and no optimizer.

## 4. Verification and remaining negative branch

- `exact_bounds.json` contains the nine rational separators and every row binding.
- `../unified/audit_r137_positive_certificates.py` is an independent, optimizer-free
  replay, using independently implemented Q(d) arithmetic.
- `../unified/audit_r137_verlinde.py` separately verifies the old witness's 5/6
  value and all 264 old equations.
- The two character/complement audits independently verify the exact tensor,
  all characters, and the full transformation T.

The final negative-TY relaxation has an **exact nonnegative rational witness
of support 124**, in `negative_strong_exact_witness.json`. It satisfies all
256 inherited equations after removing the two previously selected indicator
test branches, full-column Galois complement equalities, all 45 integral
nonnegative entries of the distinguished fusion-by-B block, and their 45
vanishing irrational parts. Its four projected third indicators are 1/2
and its four projected fourth indicators are 2, so their discrete Clifford
restrictions are satisfied as well.

It also satisfies the new strict bound v^t G^-1 v < 3/4 for every central
column outside I(1). The universal <=3/4 bound follows from the modular
STS equation, positivity of the known real twist-one rows, and row
normalization. Equality forces twist -1 and S_ZZ=1/2. In this ring,
orthogonality with the unit row and an exact integer parity argument rule
out equality altogether; the independent unified note gives that proof.

The saved rational witness is replayed by
`../unified/audit_r137_negative_strong_witness.py`, without an optimizer.
Its proposal was reconstructed and its nonzero equations checked exactly
before this independent replay. These remain necessary conditions:
unknown central fusion rules and associators are not supplied. This is
not a model and does not establish existence of the negative branch.
Earlier exploratory proposals are superseded by this one.

The independent verifier
`../unified/audit_r137_negative_strong_witness.py` also passes: it rebuilds
the quadratic-field arithmetic and checks all 256 general inherited rows,
the supported Galois pairings, the strict mass bound, all 45 integer fusion
entries and all eight projected indicators. Independent human review
remains pending.

## 5. Literature check and construction routes

The recent Radchenko–Wheeler construction (arXiv:2609.21892, Section 5)
produces near-group categories of type (G,|G|). It does not directly supply
R137 or its forced rank-12 D8 Morita representative. A dimension-matching
near-group candidate here would have |G|=8, multiplicity 16 and noninvertible
dimension 2d, which is outside that construction. Equal global dimension
does not supply a Morita equivalence or an algebra.

Primary references for the added restrictions are Deshpande,
arXiv:1611.04486 (distinguished center rows), and Dong–Lin–Ng,
arXiv:1201.6644 (modular Galois and squared-twist rule), together with
Verlinde's formula. All use in a general-complex classification remains
through the project's explicitly stated existence reduction and complete
center-domain theorems.
