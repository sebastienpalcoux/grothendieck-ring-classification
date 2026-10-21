# Complete distinguished-S-symmetric low-frame obstruction

For a pseudo-unitary category with commutative rank-eight fusion ring, each
irreducible ring character E labels exactly one distinguished simple A_E in
I(1). Its dimension is beta_E=D/f_E and its twist is1. The tensor unit is the
simple labeled by the FP character. The exact induction-restriction formula
S(A_E,Z)=beta_E chi_E(FZ) and symmetry of S require, for every pair E,F,

    beta_E chi_E(v_F)=beta_F chi_F(v_E).

Consequently enumerate every complete low restriction frame with its prescribed
unit row and dimensions, retaining the necessary entrywise nonnegative and
positive semidefinite residual Gram condition. For each frame enumerate every
bijection with the eight characters having the required dimensions. If none
satisfies the displayed equalities, pseudo-unitary categorification is impossible.
This obstruction uses only low induction data and distinguished S symmetry;
it requires no high columns, twist traces, STS equations, or linear programming.

For R8_3_1463 the seven raw low-column sets have sizes20,9,4,4,12,12,6. They
produce exactly2024 complete frames. Every character lies in Q(sqrt3,sqrt5),
and the source-bound implementation verifies all tensor multiplication identities,
character orthogonality, duality and the FP embedding. An exhaustive permitted
bijection search finds no symmetric labeling of any frame. No partial-S
algebraic-integrality filter is needed to obtain these raw low sets.

`low_s_symmetry.py` reconstructs and checks this complete finite witness. Its
saved general lift also replays the ordinary spherical character alternatives
(two norm obstructions and the FP Galois orbit) and all four oriented signed
branches, each gauge equivalent to the original ring. Thus the final conclusion
holds for arbitrary complex fusion categories, without a pivotality hypothesis.
The canonical read-only entrypoint is `verify_accepted_generic.py`; the result
is `generic_results/R8_3_1463_low_s.json`. The earlier STS certificate remains
separate corroborating research evidence and is not a dependency of replay.

The formula and its orientation use Deshpande, arXiv:1611.04486, equation39,
Lemma4.3 and Corollary4.5, specialized to commutative Grothendieck rings.
