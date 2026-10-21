# Exact necessary center actions for R8_3_721

This is a separately verified necessary-condition addendum. It excludes two
of four necessary central Gram patterns, not the source fusion ring. It
constructs exact necessary low-center fusion actions, not a center fusion
ring, associator, category, or model. The frozen 25/9 ledger is unchanged.

## Inputs and general-complex scope

The frozen source tensor is R8_3_721, SHA-256
`76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5`.
The source files are in `evidence/rank8_frontier_20261021/`:

- `noncommutative/verlinde_low_721.json`: all four integral Gram patterns,
  both symmetric character assignments, and the twenty low cubic values.
- `noncommutative/integral_gram.py`: complete 240-point Gram domain.
- `noncommutative/character_modular.py`: complete distinguished S rows,
  including the factor `D/(f_E dim(E))` for the two-dimensional source block.
- `review/NC_GALOIS_PU_REVIEW.md`: every complex categorification has a
  pseudo-unitary Galois conjugate; this uses no unitarity conjecture.

The five distinguished central objects are A0=1,A1,...,A4. Each is selfdual:
the full source trace characters satisfy chi(i*)=chi(i), so the known
central S rows are invariant under central duality, and nondegeneracy of S
identifies the object with its dual. Consequently their fusion matrices
are real symmetric integral matrices by Frobenius reciprocity. No
C*-unitarity or Hermitian-matrix assumption is used.

For D=FPdim(C), ordinary Verlinde and S^2=D^2 C imply

    K_(ij,kl) = D^-2 sum_Z S_iZ S_jZ S_kZ S_lZ / d_Z^2
              = sum_Y N_ij^Y N_kl^Y.

After subtracting all five known low contributions, write the residual
matrix as G. If M is the restriction matrix of individual high simples,
and T consists of the residual forgetful products, the high coefficients
X satisfy MX=T, X^t X=G, X>=0 integral. The sibling verifier
`quartic_center_challenge.py` proves that each of the four patterns has a
unique solution X. Its proof uses an exact rank-one residual Gram and
coordinatewise minimum squares, not an optimization solver. The same
normalization passes all 27 electric cubics and 81 fourth moments in
Z(Vec(S3)), including its matrix block m=2,f=3,beta=6/(3*2)=1.

## Labels and the four patterns

Pairs are ordered 11,12,13,14,22,23,24,33,34,44. Individual high simples
with a given restriction type have the following forced pair coefficients:

| Type | Restriction vector | Coefficients |
|---|---|---|
| 0 | (0,0,0,1,1,1,1,1) | (2,2,2,1,2,3,1,2,1,1) |
| 1 | (0,0,0,2,2,2,2,2) | (4,4,4,2,4,6,2,4,2,2) |
| 3 | (0,1,1,1,0,0,0,2) | (2,2,2,1,3,2,0,3,0,0) |
| 4 | (0,1,1,2,1,1,1,3) | (4,4,4,2,4,4,2,4,2,0) |
| 5 | (0,1,1,2,1,2,1,2) | (4,4,4,2,4,4,2,4,2,1) |
| 8 | (0,2,2,4,2,2,2,6) | (8,8,8,4,8,8,4,8,4,0) |

Call the type-0-or-1 group A, the type-3 singleton B, the type-4-or-8
group C, and the eight type-5 simples D. The cardinalities mA,mC are
independently 1 or 4. A singleton A uses type1, four A use type0;
a singleton C uses type8, four C use type4. Thus the center ranks are
16,19,19,22. This is simply a regrouping of the four frozen multiplicity
vectors, not a further hypothesis.

## The entire vacuum cyclic space is already known

Let W have columns e0,...,e4 and the ten now-forced product vectors
Ai Aj. Its exact rank is 9. The simultaneous eigenvalue tuples of
(N1,N2,N3,N4) are the following nine distinct tuples. Put u=33+8sqrt(17)
and u'=33-8sqrt(17).

| Tuple | Multiplicity |
|---|---:|
| (u,u+1,u+1,(u+1)/2) | 1 |
| (u',u'+1,u'+1,(u'+1)/2) | 1 |
| (1,-2,2,1) | 1 |
| (1,2,-2,1) | 1 |
| (1,2,2,5) | 1 |
| (1,-2,-2,1) | mA |
| (1,2,2,-3) | 1 |
| (1,0,0,-1) | mC |
| (-1,0,0,0) | 8 |

The other symmetric assignment exchanges the two signed low tuples and
has the same weighted moments; the verifier covers both explicitly.
Every tuple has positive vacuum weight sum d_Z^2/D^2. Hence the vacuum
cyclic space has dimension exactly nine. The known rank-nine span W is
therefore that entire invariant space.

Select independent columns V of W and retain their words p_alpha. Let
G0=V^t V and

    (B_i)_alpha,beta = D^-2 sum_Z d_Z^2
                       p_alpha(lambda_Z) lambda_i,Z p_beta(lambda_Z).

These moments have degree at most five. The forced action on the cyclic
space, extended as zero on its orthogonal complement, is

    F_i = V G0^-1 B_i G0^-1 V^t.

All F_i are computed exactly over Q. The verifier checks the word Gram,
commutation, and symmetry. Put Q=I-V G0^-1 V^t. Its range is exactly the
sum of the within-group difference spaces of A,C,D. The remaining
simultaneous spectral subspaces have orthogonal projectors PA,PC,PD,
with ranks mA-1,mC-1,7 and sum Q. Every possible low action must be

    N1 = F1-Q+2(PA+PC),   N2 = F2-2 PA,
    N3 = F3-2 PA,         N4 = F4+PA-PC.                 (1)

This is the complete remaining domain, not a canonical-projector ansatz.

## Two exact pattern exclusions

If (mA,mC)=(1,4), PA=0. The forced C-by-C block of N2=F2 is (9/2)J4,
contradicting integrality. With low labels 0,...,4 followed by the frozen
high-type order, these are center labels 7,8,9,10.

If (mA,mC)=(4,1), PC=0. The fixed A-by-A block of N1+N2=F1+F2-Q is
(5/2)J4-I4: diagonal 3/2 and off-diagonal 5/2. This again contradicts
integrality, independently of PA. These are center labels 5,6,7,8.

Both contradictions are checked for both symmetric character assignments.
The ring itself remains unresolved because the other two patterns survive.

## Complete surviving action tuples

For (mA,mC)=(1,1), PA=PC=0, so (1) gives a unique tuple. It is integral
and nonnegative. The high-block traces of N1,...,N4 are (48,56,56,28);
their squared Frobenius norms are (2798,2880,2880,746).

For (mA,mC)=(4,4), write P=PA+PC. The fixed A and C blocks of F_i are:

| Block | F1 | F2 | F3 | F4 |
|---|---:|---:|---:|---:|
| A by A | (5/4)J4 | J4 | J4 | (3/4)J4 |
| C by C | (17/4)J4 | (9/2)J4 | (9/2)J4 | (9/4)J4 |

The following projection argument proves completeness of the finite list.
For an orthogonal projector E, E_ii=sum_j E_ij^2 and 0<=E_ii<=1.
Here PA, PC, and P are orthogonal subprojectors of Q, so their diagonal
entries in the four-element A and C groups are at most Q_ii=3/4.
All projectors in (1) kill the constant vector of each high group,
because their ranges lie in W-perp.

1. Integrality of N1 implies that every diagonal entry of P in A or C
   is 1/4 or 3/4, and each within-block off-diagonal entry is an odd
   multiple of 1/4. For either diagonal possibility, its square plus
   three times (1/4)^2 equals the diagonal. The projection identity
   therefore forces all three off-diagonal absolute values to be 1/4
   and all entries outside that four-element block to vanish.
2. Nonnegative integrality of N2 on A gives (PA)_ii in {0,1/2}; all its
   A entries are half-integers. If its diagonal is zero its row vanishes.
   If the diagonal is 1/2, the zero A-row sum requires an off-diagonal
   entry at most -1/2. The projection norm is already exhausted, so
   exactly one off-diagonal entry is -1/2 and all others vanish. Thus
   PA on A is the sum QA of disjoint two-vertex matching projectors
   (e_j-e_k)(e_j-e_k)^t/2 and has no cross entries.
3. On C, integrality of N2 gives diagonal 1/4 or 3/4 and odd-quarter
   off-diagonal entries for PA. The same norm saturation gives no cross
   entries and within-block off-diagonal absolute values 1/4.
4. N4=F4+2PA-P is integral on the diagonals only when every P diagonal
   in A and C is 3/4. Their zero row sums then force every off-diagonal
   entry to be -1/4. Therefore P is the canonical difference projector
   E_A+E_C; its rank six is exhausted, so it vanishes on D.
5. Since PA is a subprojector of P, PA vanishes on D. On C its complement
   E_C-PA has diagonals 0 or 1/2 and off-diagonals 0 or -1/2. It is a
   matching projector QC. Finally rank(PA)=3 implies that QA and QC
   contain the same number of edges.

Thus, exhaustively,

    PA=QA+E_C-QC,    PC=E_A-QA+QC,    PD=E_D,

where QA,QC are matchings of equal size on four labelled vertices.
There are 1,6,3 matchings of sizes 0,1,2, respectively, giving exactly
1+6^2+3^2=46 labelled tuples. Up to independent within-A and within-C
permutations there are three types, distinguished by matching size.

The verifier enumerates the complete four-vertex matching domains and
checks all 46 tuples exactly. For each it checks symmetry, nonnegative
integrality, the unit column, all forced low products, pairwise commutation,
projector ranks and orthogonality, exact spectral trace and square trace,
and M_full N_i=L_{F(A_i)} M_full. The high traces are (54,50,50,28), with
squared Frobenius norms (2804,2892,2892,752). Full matrices are in the
receipt. These remain necessary data only: products of two arbitrary high
objects, the full center based ring, modular data, and associators are
not constructed.

## Reproduction

From the repository root:

```sh
python evidence/rank8_center_followup_20261021/quartic_center_challenge.py --root .
python evidence/rank8_center_followup_20261021/r721_center_extension.py --root .
python -O evidence/rank8_center_followup_20261021/r721_center_extension.py --root .
```

The scripts write nothing; redirect stdout to retain receipts. Exact
checks use explicit exceptions and remain active under optimization.
The arithmetic uses the frozen source helpers, and is not advertised as
an independent reimplementation of them. Separate computational review audits the
derivation and independently reconstructs the fourth- and fifth-moment data.

The categorical input is standard Verlinde/charge-conjugation algebra;
see Deshpande, *On twisted Verlinde formulae for modular categories*,
arXiv:1811.08447, Theorem 1.1 specialized to the regular module. The
finite-group normalization control can be checked against Coste--Gannon--
Ruelle, *Finite Group Modular Data*, arXiv:hep-th/0001158. General-complex
scope uses the explicitly cited existing Galois-PU gate above.
