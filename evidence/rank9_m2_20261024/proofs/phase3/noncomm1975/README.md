# Noncommutative R9_2_1975: bounded theoretical and exact continuation

**Status: unresolved.** None of the tests recorded here is a categorical
existence proof or an exclusion.

The based algebra is C^5 plus M_2(C), with dimensions
`1, d, d, d, d, 1, 1, 1, 2`, where d=4+3√2 and
FPdim(C)=144+96√2. The integral rank-five subring is of
Tambara–Yamagami type for V4. The only nontrivial invertible basis element
central in the based ring is b5. The regular Casimir acts on an irreducible
representation of degree e by e times its formal codegree; all code and
formulas here retain this degree factor.

`center.py` reconstructs the rank-six induction Gram form and its exact
range, enumerates every individually admissible nonnegative integer
restriction vector, and applies dimension integrality, d-number,
modular S-ratio integrality and Galois dimension pairing. There are 468
initial vectors, 96 after dimension arithmetic and 80 after the remaining
filters, including 12 low-column candidates. The modular operator is
`(D/z)(2I-P_scalar) C_regular^-1 N_v`, where the scalar-character subspace
has dimension five. The weighted induction multiplicity of the matrix
block is two.

The joint center constraints through rotation order six produce no exact
Farkas obstruction (`result_h6.json`). `symmetry.py` adds labelled
S symmetry for all real scalar characters and the normalized trace of
the degree-two block, exact duality pairing, and the sum of the S-symmetry
equations for the two remaining complex scalar characters. This stronger
253-equation, 1291-variable system also gives no exact obstruction
(`symmetry_h6.json`). The reported infeasible solver status in these files
concerns the search for a separating ray, not the primal categorical
relaxation; no conclusion of categorifiability is drawn.

The Galois-unit restriction identity has the same normalization in the
noncommutative case: the scalar by which F(A_(σFP)) acts on an irreducible
E is f_E/σ(f_E). Its unique forced vector is
`[1,1,1,1,1,0,0,0,0]`, which is nonnegative integral. Thus the new criterion
does not exclude 1975. The implementation and exact output are
`galois_unit.py` and `galois_R9_2_1975.json`. Applied independently to
root-owned 1848, it likewise passes, with vector `[1,0,0,0,0,1,1,1,0]`.

Finally, four bounded refinements respectively forbid the central lift
of b5, or restrict its available twist packets to fermion, boson, or
boson/fermion packets. All four searches return no exact separating ray
(`force_invertible.py/json`). These attempts therefore establish neither
the existence nor the necessity of a central bosonic or fermionic lift.
No de-equivariantization or new model is claimed from them.
