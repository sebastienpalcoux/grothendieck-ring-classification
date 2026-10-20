# Low-block Verlinde normalization and independent witness check

Assume a pseudo-unitary categorification and its canonical modular center.
Write `D` for the dimension of the original category, so the center has
dimension `D^2`. For a simple summand `E` of the induced unit, let `chi_E` be
the corresponding based-ring character and `f_E` its formal codegree.
Commutativity makes these summands multiplicity one, and their dimensions are
`d_E=D/f_E`.

The central-character identity gives the unnormalized entry

\[
\widetilde S_{E,V}=d_E\chi_E(F(V)).
\]

Consequently the normalized entries are
`S_{E,V}=chi_E(v)/f_E` and `S_{1,V}=z/D`, where `v=F(V)` and
`z=FPdim(V)`. Substitution into Verlinde gives

\[
N_{EF}^{G}
=\frac{D}{f_Ef_Ff_G}
  \sum_v m_v\frac{\chi_E(v)\chi_F(v)\overline{\chi_G(v)}}{z_v}.
\]

The implementation in `integral_gram/verlinde.py` uses the fully symmetric
product without conjugation. Its values are therefore **`N_{EF}^{G*}`**.
They are still nonnegative integers. All 56 unordered triples among the six
nonunit low objects are valid necessary conditions. The remaining 28
unordered triples involving the unit follow from low-row orthogonality; the
independent checker also recomputes them explicitly.

`verify_low_verlinde_witness.py` starts with the source tensor, the exact
character table, low restriction columns, and the exported integer support.
It checks character multiplicativity and recomputes the complete restriction
Gram matrix, center dimension, all 49 low-row orthogonality equations, and all
84 symmetric low Verlinde coefficients. It does not import the discovery
coefficient caches or call an optimizer. It additionally rejects corrupted
multiplicities. Normal and optimized-Python receipts bind the frozen witness
snapshot and checked inputs.

These computations verify only the recorded necessary data. They do not
construct a modular category, a complete fusion table for its center, or a
categorification of the original ring. Conversely, numerical mixed-integer
infeasibility for a different case is not an exclusion without a finite exact
certificate.
