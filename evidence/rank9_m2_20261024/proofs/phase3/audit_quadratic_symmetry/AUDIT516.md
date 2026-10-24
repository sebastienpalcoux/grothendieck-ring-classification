# Independent audit of the labelled-center exclusion of R9_2_516

Conclusion: **accept the general complex-fusion-category exclusion of 516**,
using the signed Galois-to-pseudo-unitary gate already independently replayed
and the exact certificate `../quadratic_s_symmetry/R9_2_516_h3.json`.

The new theoretical input is sound. For a scalar irreducible character χ_h of
the commutative Grothendieck algebra, the distinguished simple A_h in I(1) has
positive dimension d_h=D/f_h. If v_k=F(A_k), the induction-character formula
and symmetry of the unnormalized modular S matrix give

    d_h χ_h(v_k) = S_(A_h,A_k) = d_k χ_k(v_h).

This was checked afresh against Deshpande, arXiv:1611.04486, Proposition 2.8,
Section 2.7, equations (36),(39), and the definition of ρ_E there. In particular
ρ_E is the central eigenvalue under the forgetful functor, and for a scalar
character is precisely χ_h∘F. There is no additional normalization factor.
Each equality is split into its rational and sqrt(3) coefficients.
Primary source: https://arxiv.org/pdf/1611.04486 .

The implementation retains the previously audited center Gram, low-codegree,
arithmetic, modular-integrality, Galois-dimension and indicator/rotation
necessary conditions. It introduces a character label for each distinguished
column, requiring total multiplicity one per label. A label can be assigned
only to a column with dimension D/f_h. An actual center gives a nonnegative
integer solution; allowing arbitrary nonnegative rational variables is a
relaxation. Consequently its infeasibility is a valid obstruction. No integral
low-frame selection is assumed. The R516 certificate uses no additional
central-duality restriction.

The independent script `replay516.py` does not import the new system builder.
It verifies directly that the nine displayed quadratic-valued vectors are
nine distinct ring homomorphisms. Since the commutative semisimple algebra has
dimension nine, this is a complete character list. It recomputes every formal
codegree and D/f_h, reconstructs the character assignments and all symmetry
rows on top of the separately audited base system, and checks the resulting
system hash. In this particular case all nine low dimensions are distinct,
so no ambiguity in labelling is hidden in repeated dimensions.

The exact integer ray has 198 rows and checks against all 14,128 columns:

    b^T y = -865016136823898478632059440,
    min_j (A^T y)_j = 0.

Every inequality is checked with Python integer arithmetic. The independently
assembled system hash is
`5eefad664f03df442d3e6bd1a4d6e3032dec109037e74d2bb66b2acc493298ca`.
See `replay516.json`. The large ray coefficients affect convenience of
presentation, not validity. A failed floating-point solve is not used as proof.
The known unitary model 1983 survives the new necessary conditions, as recorded
by the developing agent; the exact separating check is the decisive certificate.

The phase-two gate `phase2/signed/gate_R9_2_516.json` ensures that any complex
categorification has a Galois-conjugate pseudo-unitary categorification of the
same based ring. Therefore this pseudo-unitary center obstruction excludes all
complex categorifications, rather than only pseudo-unitary ones.
