# Joint Galois spectrum of all distinguished center fusion matrices

Let A_E be the distinguished center simples indexed by irreducible source
representations. In a pseudo-unitary categorification, the simultaneous
eigenvalue tuple at a center simple Z is

    lambda_E,Z = D chi_E(FZ)/(f_E dim(E) dim(Z)).

This is the full Deshpande distinguished S-row normalization divided by
S_1,Z=dim(Z). In particular dim(E)=2 for the matrix representation and
its distinguished central simple is counted once in the spectrum.

The fusion matrices N_AE in the braided center commute, are diagonalized
by S, and have integer entries. A field automorphism sends the common
kernel of (N_AE-lambda_E I)_E semilinearly onto the common kernel with all
lambda_E conjugated. Consequently their dimensions agree. Thus joint
spectral multiplicities must be Galois invariant. The labels E remain
fixed: no permutation or conjugation of the chosen integer matrices is
made. This theorem applies to noncommutative source rings as well.

The canonical verifier builds the five-component eigenvalue tuple exactly
for every complete low/high restriction column in R721 and R1154, in their
quadratic fields. It counts each distinguished low simple once and uses
the saved exact high integer multiplicities. It tests the unique nontrivial
field automorphism on the full tuple, rather than each coordinate in
isolation.

For R721, the complete four integer Gram patterns are freshly reconstructed
by the exact affine-box enumerator and matched to the frozen receipt. All
four pass joint spectral balance. For R1154, the full14211 integer Gram
receipt and the complete1238 cubic/spectral surviving indices are bound
by hashes; the low/high domains and tensor are rebuilt exactly. All1238
pass joint spectral balance. Thus no extra exclusion or model is claimed.

The source-bound Galois-pseudo-unitary gates already proved for these two
rings make these necessary tests applicable to any complex categorification
after Galois transport. Unitarity is not assumed. The same theorem's actual
Z(Fib) control and quartic R928/R941 application are in
`../r928_semion_rotation/joint_spectrum.py/.json`.

```
python evidence/rank8_frontier_20261021/noncommutative_joint_spectrum/verify.py
python -O evidence/rank8_frontier_20261021/noncommutative_joint_spectrum/verify.py
```
