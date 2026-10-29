# R6_8_1660: accepted spin constraints

27 October 2026. **The ring remains unresolved. Neither complete spin branch
is excluded.** The accepted result is the restricted statement below.

## Inputs

Use the positive spherical Galois representative, source order
`(1,g,X,gX,sigma,T)`, r=sqrt(2),
`d=3+2sqrt(2)+2sqrt(3)+sqrt(6)`, D=4(1+d^2).
All source simples are selfdual. The center's phases9,15,33,39 each contain
one dual pair, with restriction `(0,0,2,2,1,3)`.

At phase12 all columns have form `(0,0,b,c,0,a)`, and, with q=b+c,

    sum q^2 = sum qa = sum a^2 = 4.

Thus q=a for each column. At phase36 the analogous sums are `(36,20,12)`.
These are the established full phase-mass theorem in
`manuscripts/rank6/papers/chapters/frontier_1660_phase_masses.tex`.
The induction Gram has H_XX=H_gX,gX=142 and H_X,gX=138, so
`sum_all (b-c)^2=8`. In low frame0 the low columns already contribute8;
in frame1 they contribute0. The total high asymmetry budgets are therefore
0 and8 respectively. The four forced high fermion partners are symmetric.
See `frontier_refined.tex` for the low columns and complete Gram.

The prior complete modular-character exhaustion leaves either
`W_16,2 + W_20,2` or `W_44,2` as the charge-conjugation-negative
representation meeting the spin phases. W_44,2 has dimension6 and simple
T spectrum `{9,12,15,33,36,39}`.

## 1. W_44,2 forces frame1 and an asymmetric phase12 packet

Its negative phase12 line requires a dual pair. The q=a, sum q^2=4 identities
allow either one q=2 column or four q=1 columns. A single simple is selfdual,
so the latter is necessary: there are two columns X+T and two gX+T, using
the separate X and gX phase masses. Their asymmetry contribution is4.
This excludes low frame0, but leaves4 of frame1's high budget.

## 2. W_44,2 is incompatible with symmetric phase36

Suppose every phase36 column is symmetric, so q is even. Its Gram gives

    sum (q-2a)^2=4,    sum a(q-2a)=-4.

All q-2a are even; there is precisely one exception q-2a=+2 or-2. The
second identity forces the exception to be `(q,a)=(2,2)`, and every other
column has q=2a. The exceptional column is unique, hence its central simple
is selfdual. It is absent from the negative charge-conjugation space.

Let A be the distinguished Galois-unit simple for
`sigma_5: zeta48 -> zeta48^5`. Its restriction is `1+2X+2gX+2T`, and
`beta=dim(A)=1+(4+2r)d=D/sigma_5(D)`. The distinguished character formula
and S-symmetry give the Verlinde spectral ratio

    r_Z = s_A,Z/s_1,Z = beta sigma_5(dim Z)/dim Z.

This is -1 on spin restrictions, +1 for q=a, and -1 for q=2a.
A is selfdual, by uniqueness of its low restriction/dimension.

For the normalized dual difference u at phase9 in W_44,2, the exact
S-transition probabilities to phases12,15,36,39 are each1/4; those to9,33
are0. They are short finite-character averages
`Tr(P_9 s P_t s^-1)` in the modulus16 and modulus3 factors, not fitted
matrix entries. Under the symmetric-phase36 hypothesis, therefore,

    <u,N_A u> = 1/4-1/4-1/4-1/4 = -1/2.

But for u=(e_B-e_B*)/sqrt(2), this equals
`N_{A,B}^B - N_{A,B*}^B`, an integer. Contradiction.
Thus W_44,2 requires asymmetric phase36 columns as well.

## 3. Surviving configurations

Frame1 has total high asymmetry budget8. The phase12 packet uses4 and
leaves4; thus Parts1-2 do not exclude W_44,2 altogether.

If the phase12 packet has even fermion monodromy, its four fermion partners
lie at phase36, again with q=a=1. They use the remaining asymmetry budget.
Subtracting their Gram contribution leaves `(32,16,8)`, forcing all other
phase36 columns to have q=2a. The W_44,2 negative phase36 line can lie on
the q=a packet, where its spectral ratio is+1. The displayed expectation
then becomes0 and passes integrality. In fact integrality forces that
placement: the expectation is `(rho-1)/4` with -1<=rho<=1, hence rho=1.

If the phase12 packet is odd, its dual pair in the X+T restriction fiber
has a fermion-translated dual pair in the gX+T fiber. Negative phase12 then
has dimension2. Extra negative irreducibles exist: `(2,2)` (phase12 alone)
and `(6,2)` (phases12,36). No contradiction with these configurations
was proved.

For W_16,2 and W_20,2 the spin transition probabilities are respectively
`(15:1/4,30:1/2,39:1/4)` and `(9:1/4,33:1/4,42:1/2)`.
The homogeneous phase30/42 ratios give the integral expectation0.
This alternative also survives.

## 4. A signed-permutation rigidity theorem

Let A_7 be the distinguished Galois-unit simple for sigma_7, which fixes
sqrt(2) and negates sqrt(3). Its spectral ratio is-1 on every non-spin
high column and+1 on every spin column. All six low central simples are
selfdual by the established second-indicator cut; their forced high
fermion partners are also selfdual. Hence on the entire negative
charge-conjugation space, N_A7 has only eigenvalues+1,-1.

In the orthonormal basis `(e_Z-e_Z*)/sqrt(2)`, one vector per dual pair,
N_A7 is symmetric integral: its entries are differences of fusion
coefficients. Its square is identity, so each row has squared norm1.
Therefore it is a signed permutation matrix, and an involution. Equivalently

    N_A7 | V_- = -I + 2 s P_spin s^-1 | V_-.

Here P_spin projects onto the four negative spin lines. This is independent
of the spin-representation choice. No contradiction or construction follows
from this constraint alone.

## Verification and provenance

`verify_spin_constraints.py` regenerates the exact field ratios and the
transition probabilities in a few seconds. It uses the already frozen
character tables and cyclotomic arithmetic helper; no search or unknown
S-matrix is involved. Additional positive-line expectations were integral and supplied no exclusion.

The independent audit is `../audit_fs2/R1660_SPIN_AUDIT.md`.
The exact source tensor is `data/current_remaining_cases.py`, SHA256
`697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267`.
The preceding results inherit the project's spherical reduction and phase
theorem; they do not replace their categorical proofs.
