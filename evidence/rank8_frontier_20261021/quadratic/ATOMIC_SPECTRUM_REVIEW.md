# Independent review of full-character-field atomic S symmetry

The new `global_induction/atomic_spectrum.py` system is a necessary
pseudo-unitary central-induction relaxation. It has a separate simplex for
each non-Frobenius–Perron character, with independent rational mixtures of
restriction columns. It is weaker than the complete joint-frame hull.
Consequently a feasible certificate is not a fusion category, a center,
or even an integral joint frame. A complete exact separating functional
excludes the pseudo-unitary case. General complex scope is obtained only
from the additional complete oriented signed lift.

Let the commutative based ring have characters `chi_E`, formal codegrees
`f_E`, and Frobenius–Perron global dimension `D`; put `beta_E=D/f_E`.
The distinguished simple `A_E` of the induction of the unit has dimension
`beta_E` and multiplicity one. Write `v_E` for its restriction. The
induction/character formula gives

\[
 S(A_E,Z)=\beta_E\chi_E(FZ).
\]

The orientation follows by specializing Deshpande,
[arXiv:1611.04486](https://arxiv.org/abs/1611.04486), Lemma 4.3 and
Corollary 4.5, to the identity bimodule and one-dimensional characters.
Symmetry of the modular S-matrix therefore gives the linear equations

\[
 \beta_E\chi_E(v_F)-\beta_F\chi_F(v_E)=0.
\]

This is symmetry, not conjugate symmetry. No complex conjugation is
inserted into this equation even when the character field is nonreal.
The equations with the FP character follow from `v_FP=1` and
`FPdim(v_E)=beta_E`. Every actual distinguished simple has its column in
the old complete finite domain. Taking the union of equally dimensional
old column sets for each character cannot omit an actual choice.

The partial-S eigenvalue

\[
 \lambda_{E,Z}=\frac{\beta_E\chi_E(FZ)}{\operatorname{FPdim}(Z)}
\]

is an eigenvalue of an integral fusion matrix in the center, so it is an
algebraic integer. In a full splitting field `L`, the characteristic
polynomial of multiplication by `lambda` over `Q` is integral exactly
when `lambda` is an algebraic integer: necessity follows from its
conjugates, and sufficiency follows from that monic polynomial. The
quartic and sextic adapters check this polynomial; they do not mistake
integer coordinates in a possibly nonintegral power basis for integral
closure.

The new S equations are imposed in every rational coordinate of `L`.
Their high-column and rotation-column coefficients are zero. Thus the
existing relative twist moments remain in the FP field; no trace is
incorrectly moved across a larger character-field coefficient. This
variant deliberately imposes no STS equation. Its only additions to the
reviewed ordinary induction/rotation cone are the full-field integrality
filter, character labeling, and linear S symmetry.

`review_atomic_spectrum.py --ring 3413` independently reconstructs all S
coefficients, verifies every omitted FP equation, compares each score of
the factored oracle with a direct column dot product for three integer
functionals, and retains all twelve restriction types of the known model
`Fib tensor Vec(C2 times C2)`. An exact rational feasible certificate for
that model is transferred by semantic variable keys, then checked anew.
For R3413 it also directly evaluates the saved separator on every one of
the 4485 columns and checks every indicator branch, then replays the
complete signed certificate. The receipt is
`review_atomic_spectrum_3413_results.json`. The source and certificate
hashes are bound in that receipt; default invocation is read-only.
