# Monodromy-resolved fusion products for R8_3_928 and R8_3_941

This is new necessary-condition evidence, dated 2026-10-21. Neither ring is
excluded or constructed. The ten current semion patterns for R928 and fourteen
current fermion allocations for R941 all survive the tests below. The new
integer witnesses concern fusion products of distinguished central objects;
they do **not** settle the separate, previously inconclusive twist allocations.

## Hypotheses inherited from the frozen audit

The reviewed Galois/pseudo-unitary reduction permits the positive spherical
categorification to be used as a necessary test for an arbitrary complex
categorification. The complete center source is
`../../rank8_frontier_20261021/quartic_integer_center/source.json`.
There are five self-dual distinguished central simples A0=1,A1,...,A4, with
monodromy charges (+,+,+,+,-). The source global dimension is

    D = 144 + 96 sqrt(2) + 80 sqrt(3) + 56 sqrt(6).

The forced central invertible G has order two and forgets to the nontrivial
source invertible. Its self-monodromy is -1 for R928 (semion) and +1 for R941
(fermion). The five translates G Ae are distinct from the five Ae and have
canonical high restriction indices 40,41,42,43,57. All other nonzero high
columns have indices 0,...,39, are fixed as restriction vectors by the source
invertible, and have zero coefficients on both source invertibles.

The source has 343 complete integer Gram/cubic patterns. The semion parity
condition leaves15. The fermion charge equations give93 allocations. The
previous full correlated twist and permutation tests leave respectively10 and14.
These claims are inputs, not reproved here. Their files and SHA256 values are
bound in the new receipts. In particular, an ordinary rank-four quotient
obstruction is **not** applied to a fermionic quotient, and no negative scalar
fermion-character assertion is used.

## Pair-product Gram lemma

Write s for the unnormalized modular S matrix of Z(C), so s(1,Z)=d(Z) and
dim Z(C)=D². For a self-dual distinguished object Ae, the already established
source character formula is

    s(Ae,Z) = D/(f_e dim(E_e)) · chi_e(F(Z)).

For a word W in the self-dual Ae and epsilon in {0,1}, the unit coefficient is

    [1 : G^epsilon W]
      = sum_Z d(Z)²/D² · m(Z)^epsilon
          · product_(Ae in W) (s(Ae,Z)/d(Z)),

where m(Z)=s(G,Z)/d(Z) is its monodromy charge. This is the usual Verlinde
diagonalization of fusion; it does not use a unitary associator.

For the ten unordered pairs p=(i,j), 1<=i<=j<=4, let x_p be the vector of
multiplicities of Ai Aj on a chosen set of unknown simple objects. Subtracting
the contributions of every known simple gives

    K_pq = <x_p,x_q>
          = sum_Z s(Ai,Z)s(Aj,Z)s(Ak,Z)s(Al,Z)/(D² d(Z)²)
            - known contributions.

All factors are real because these distinguished objects are self-dual. In
particular no conjugation is being omitted improperly. The known coordinates
for Ae come from the cubic coefficients. Those for G Ae come from the same
cubic formula with the extra factor m(Z). Their coefficients must be
nonnegative integers and must respect the monodromy charge of Ai Aj.

Let M contain the unknown forgetful columns, each repeated once per unknown
simple, and let T contain the known-subtracted restrictions F(Ai Aj). Necessarily

    M X = T,                 X^t X = K.

Put Q=M M^t. A rational row-rank submatrix of Q gives the minimum Euclidean norm
solution X0=M^t Q^+ T, with Q^+ interpreted on the image. Every solution is
X=X0+Y with M Y=0 and X0^t Y=0. Consequently

    H = K - X0^t X0 = Y^t Y

is positive semidefinite and has rank at most number(unknown simples)-rank(M).
If H=0, every unknown multiplicity is forced by X0, and must be a nonnegative
integer. This is elementary real linear algebra applied to an integer fusion
coefficient matrix, not an assumption of categorical unitarity.

Monodromy is multiplicative, so columns and rows are separated by charge. For
R928 the two charges have equal multiplicities within every fixed restriction
type. For R941 their multiplicities are 2p and q, using the93 complete frozen
charge allocations. These counts determine the separate matrices Q.

## Inserting the involution

Let P permute simple objects by G. The same fourth-moment formula with m(Z)
inserted gives X^t P X after subtracting the known objects. For R941, P preserves
charge. The Gram matrices of (X+PX)/2 and (X-PX)/2 are (K+J)/2 and (K-J)/2,
where J=X^t P X. Both must be positive semidefinite. The minimum restriction
norm is subtracted only from the symmetric part, because M P=M.

For all fourteen current R941 allocations, the antisymmetric Gram in the
positive charge sector is zero. Thus x_p(Z)=x_p(GZ) for every positive-charge
unknown simple. A fermion has no fixed positive-charge simple: the balancing
equation theta(GZ)=theta(G)theta(Z)m(Z) would give theta(Z)=-theta(Z).
Accordingly the positive multiplicity problem descends to seven actual pairs.
It is legitimate to divide their restrictions and Gram by two.

For R928, P exchanges charges. The negative-sector vectors are already forced
by H=0; their mixed Gram with the positive sector agrees exactly with the
involution-weighted fourth moment. No ordinary Deligne factorization of C is
inferred from the central semion.

## Finite integer-row lemma and the R941 rigidity result

For a row y=x-X0 of the residual matrix Y, H-y^t y is positive semidefinite.
Thus y lies in the row space of H and y H^+ y^t<=1. Choose pivot columns of H.
Their principal submatrix is positive definite, so its inverse expresses every
remaining coordinate of y in terms of those pivots. The bounds
|y_j|<=sqrt(H_jj) give a complete finite enumeration of possible nonnegative
integer rows x. The code checks the row-space and ellipsoid conditions exactly.

For R941, the common positive sector has canonical types0,9,12,18 with
fermion-pair counts1,3,2,1. Its residual rank is1. In the pair-column order

    (11,12,13,22,23,33,44),

the complete row enumeration has seven possible rows. There are only16
multiset choices with the specified type counts. Exactly one satisfies the
full restriction and Gram equalities:

| Type | Number of fermion pairs | Pair fusion coefficients |
|---|---:|---|
| 0 | 1 | (1,0,1,2,2,3,3) |
| 9 | 2 | (1,2,3,2,4,7,7) |
| 9 | 1 | (2,1,3,3,4,7,7) |
| 12 | 2 | (2,3,5,4,7,12,12) |
| 18 | 1 | (3,4,7,6,10,17,17) |

This uniqueness is up to permutations of equal-type fermion pairs. It is a
rigidity statement about these products, not a complete center fusion ring.
The three negative-charge pair columns (14,24,34) are uniquely forced for all
unknown simples in every case of both rings by the zero residual Gram.

## Exact outcomes and reproducibility

* Uncharged fourth moments: all343 patterns pass for each ring, falling into23
  common moment groups.
* Charge-resolved translated cubic and fourth Gram tests: all15 semion parity
  patterns pass;49 of93 fermion allocations pass. The44 failures have a
  nonintegral or negative translated cubic coefficient. All14 already-current
  fermion survivors are among the49, so this does not change their status.
* Involution-weighted Grams: every remaining case passes; the current R941
  positive antisymmetric Gram is zero.
* Exact nonnegative integer pair completions:10/10 current R928 and14/14 current
  R941 cases. A floating point MILP solver is used solely to locate candidates;
  every accepted candidate is rechecked against the full rational matrices.
  A solver failure would be recorded as inconclusive.
* Unit coefficients of all words of total degree<=10 in A1,...,A4, with and
  without G:2002 coefficients per case, all nonnegative integers. This is a
  finite screen, not a theorem that all higher conditions hold.

Run, from the repository root:

```sh
python evidence/rank8_next_20261021/semion_fermion/verify.py
python -O evidence/rank8_next_20261021/semion_fermion/verify.py
```

The verifier checks every file binding, all24 integer pair completions, the
forced negative sector, the16-case R941 uniqueness enumeration, and actual
Z(Ising) and double-semion fourth-moment controls. It uses explicit exceptions,
so `-O` does not remove checks. The producer scripts can regenerate each JSON
receipt independently; `higher_moments.py --degree 10` specifies its bound.
No old full-domain campaign is rerun or modified.

For the standard categorical background see Etingof–Nikshych–Ostrik,
[On fusion categories](https://arxiv.org/abs/math/0203060), and
Drinfeld–Gelaki–Nikshych–Ostrik,
[On braided fusion categories I](https://arxiv.org/abs/0906.0620), §2.8.
The exact distinguished-row identification and general-complex applicability
remain the separately reviewed frozen inputs named above.

What is still missing is a completion to all central fusion products and
coherent associators, or an obstruction that rules out every current case.
These receipts supply neither, and make no new exoticness certification.
