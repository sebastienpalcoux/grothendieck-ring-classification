# Independent audit: R137 full-vector Galois orbits and fourth rotation

29 October 2026. **Accepted as necessary conditions.** Both strengthened
systems still admit exact nonnegative rational witnesses. No model or
exclusion follows.

## Whole restriction vectors

The full character table hypothesis is essential; merely fixing the source
FP-dimension field would not suffice in general. R137's nine explicitly
listed, distinct ring homomorphisms were checked against every multiplication
coefficient; they exhaust the rank-nine commutative semisimple ring and all
lie in Q(√2).

I retrieved and read Deshpande, arXiv:1611.04486, Proposition 2.8, §2.9 and
Corollary 4.5. The source gives S(A_E,Z)/dim(A_E)=χ_E(FZ) in this
one-dimensional-character case. Together with dim(A_E)=D/f_E this gives
normalized s(A_E,Z)=χ_E(FZ)/f_E exactly as used. Thus an automorphism fixing
K fixes every entry in these distinguished rows. The normalized unit row
lies in K and is positive, so the signed Galois column permutation has sign
+1 at every column. All character values of FZ are therefore unchanged.
They separate the source ring, proving equality of the entire restriction
vector, not just its dimension.

The squared-twist rule is used with the canonical anomaly-one center
normalization. All units modulo lcm(ord(theta),8) fixing √2 extend to units
of the full cyclotomic conductor, so computing the square orbit modulo that
least common multiple does not omit possible automorphisms. A k-element
orbit supplies k distinct center simples with the same column. Removing
them from the Gram decomposition proves G−kvvᵀ≥0. For positive definite
G this is equivalent to kvᵀG⁻¹v≤1.

The later strengthening uses the established Galois-unit character formula:
F(B)=1+X3+X4+X5+X6. I checked the supplied complete character calculation
against every formal-codegree ratio f/σ(f). Subtracting the unit column and
this B column gives H=G−e0e0ᵀ−vBvBᵀ. The same orbit inequality is valid
for the remaining high columns; the implementation applies it only to
v[0]=0, safely avoiding the distinguished columns. The required low B column
is independently imposed. The residual matrix H is positive definite, as
also checked by exact positive elimination pivots.

## Fourth rotation and TY signs

I checked the four-cycle insertion algebra directly. With generators A_j,
the central products A0A2 and A1A3 have four sign blocks. In the ++ fixed
block rotation exchanges two anticommuting Pauli generators, giving an
opposite eigenvalue pair. In the -- block it sends (P,Q) to (Q,−P), giving
an adjacent fourth-root pair. The other two blocks are exchanged and give
the regular four-root spectrum. This proves the claimed spectrum accounting
without an inner product or unitarity assumption.

For each large source simple, the tensor gives dim Hom(1,X⁴)=18 and
X²=1+h+2ΣY. The inherited positive FS2 theorem gives tr(E²)=ν2(X²)=10
for the fourth rotation E. The
three possible block counts are (a+,a−,b)=(5,0,4),(6,1,2),(7,2,0).
Consequently both real and imaginary parts of ν4 are even integers between
−4 and 4. The normalized trace to Q(√2) is its real part. The argument
uses the already proved source-local anticommutator, which applies to both
TY signs; it introduces no TY-sign restriction or hidden unitarity premise.
The saved witnesses impose projected fourth indicator 2, not the stronger
unprojected assertion ν4=2. The receipt labels were corrected accordingly.

## Independent exact replay

Two independent standard-library scripts in this directory rebuild G from
the frozen tensor, compute its (or H's) inverse exactly, reconstruct each
physical restriction vector from the old Gram equations, independently
enumerate the first-four trace types and minimum square-Galois orbits,
verify every supplied norm and removed column, rebuild all eight quartic
bound rows and four branch rows, and check every equation and every
nonnegativity condition of the saved rational witnesses. The old 252
equations are unchanged; each new system has 264 equations.

| Filter | TY sign + support | TY sign − support | Removed variables per sign |
|---|---:|---:|---:|
| Full-vector orbit, projected ν4=2 |117|119|6716|
| Forced Galois-unit residual Gram, projected ν4=2 |102|112|7222|

Both replays pass. The all-zero height-four trace has minimum square orbit
three, attained at order144. Orders outside the finite moment box have
zero moments and orbit lower bounds at least four (2-primary direction)
or nine (3-primary direction), so the finite table is not an assumption
that all twists have bounded order.

Files:
- verify_r137_continuation_audit.py and r137_continuation_audit_receipt.json
- verify_r137_forced_galois_audit.py and r137_forced_galois_audit_receipt.json

These checks certify the stated finite relaxation and witnesses. They do
not construct modular data, a modular category, or a categorification of R137.
