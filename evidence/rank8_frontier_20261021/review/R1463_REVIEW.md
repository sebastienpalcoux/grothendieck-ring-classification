# Independent review of the R1463 general exclusion

Accepted conclusion: R8_3_1463 has no categorification by a complex fusion
category. Separate AI review independently verifies the essential low-only
obstruction and a larger unrestricted signed domain; it is not human review
or proof-assistant formalization.

In a pseudo-unitary categorification of a commutative fusion ring, the
distinguished central simples A_E have dimensions beta_E=D/f_E and
restriction columns v_E. Deshpande's induction character formula gives
S(A_E,A_F)=beta_E chi_E(v_F). Symmetry of S therefore requires
beta_E chi_E(v_F)=beta_F chi_F(v_E). The tensor unit is the FP-labeled
constituent. This argument uses no high central constituents, twist phases,
indicator assignments, STS relation, or modular-integrality filter.

The reviewer reconstructed all eight distinct characters in the exact FP
field and checked every multiplication identity and every orthogonality
identity. A separate affine integer enumeration reconstructed all raw
restriction domains, with sizes 20,9,4,4,12,12,6. The bounds follow from the
unit row and diagonal entries of the full induction Gram matrix.

`verify_r1463_low_symmetry.py` uses a fixed 3+4 join of all row-sum choices,
without the producer's native frame enumerator or its partial-PSD/Cauchy
pruning. Of the 2,488,320 raw Cartesian choices, 73,040 satisfy the unit-row
equations. Quotienting only permutations of identical column sets leaves
23,648 choices. Exact rational Schur-complement checks retain precisely
2,024 entrywise nonnegative, positive-semidefinite residual Gram frames.
Every one of their 8,096 dimension-compatible bijections with the full
character table fails S symmetry. The independent optimized replay passes.

The general scope is also checked. The canonical minimal producer's full
optimized replay passes, including its four normalized signed branches.
The reviewer additionally exhausts all 512 parity-compatible signed tensors
without positive-indicator domain normalization or commutativity assumptions.
All ordered tensor identities are rechecked. Exactly 128 tensors are
dual-compatible sign gauges of the original ring. The other 384 fail an
explicit necessary adjoint-parity test: for a self-dual object i, neither
possible second-indicator sign nu makes every

    N(j,j*,i) - nu T(j,j*,i)

divisible by four. A skew self-dual simple has even multiplicity in every
Y tensor Y*, giving this condition in sphericalization. Every failure is
checked at its two recorded rows. Thus every possible categorification
has a spherical section of its sphericalization.

The two ordinary non-FP character factors both give categorical dimension
polynomial t^2-20t+80. The FP formal codegree has polynomial
t^4-240t^3+4560t^2-28800t+57600. In any common number field L, the norm of
delta/f is (80^2/57600)^([L:Q]/4)=(1/9)^([L:Q]/4), not an integer. The
induced-unit integrality theorem excludes these alternatives. The remaining
quartic character orbit is the FP orbit, so a spherical categorification
would have a pseudo-unitary Galois conjugate. The low-only obstruction
already excludes that possibility.

Canonical producer: `global_induction/verify_accepted_generic.py` and
`generic_results/R8_3_1463_low_s.json`. Independent review replays:
`verify_r1463_low_symmetry.py` and `verify_r1463_signed_unrestricted.py`.
The earlier large STS certificate is corroborating discovery evidence and
is unnecessary for this proof. Shared frozen primitives are explicitly
limited to exact character/number-field arithmetic and the ordered signed
associativity generator; low restriction and frame enumeration were
implemented separately for this review.

Primary theorem references are Deshpande, arXiv:1611.04486, Lemma 4.3 and
Corollary 4.5, and Ostrik, arXiv:1309.4822, Theorem 2.13, Corollary 2.14
and Section 5.1; the sphericalization parity argument is the one recorded
in the existing signed-lift proof package.
