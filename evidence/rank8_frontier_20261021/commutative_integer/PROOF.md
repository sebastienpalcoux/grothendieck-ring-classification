# Integer central Gram, spectral, and cubic constraints

The initial hypothesis is a **pseudo-unitary complex fusion category** with
commutative rank-eight Grothendieck ring. A negative result in this domain
becomes a general-complex exclusion only after a separate complete signed
sphericalization and dimension-character argument. No integer-lattice
membership, feasible relaxation, or numerical optimization status is a
construction of a fusion category.

Let `D=FPdim(C)`, let `chi_E` be the eight ring characters, and put
`beta_E=D/f_E`. The character with `chi_E(X)=FPdim(X)` is located by exact
equality; its index is not assumed to be zero. In particular, the FP indices
in the present quadratic adapters are 4 for R1768 and 6 for R1795.
The distinguished central simples `A_E` in `I(1)` occur once because the
source ring is commutative. Their dimensions are `beta_E`. The tensor unit
is the distinguished simple for the FP character.

We use the unnormalized modular matrix, whose unit row gives dimensions.
Deshpande, *On centers of bimodule categories and induction-restriction
functors*, arXiv:1611.04486, Lemma 4.3 and Corollary 4.5, gives

    S(A_E,Z) = beta_E chi_E(F(Z)).

The character orientation and this normalization are already independently
reviewed in `global_induction/PARTIAL_S_AND_STS.md` and its review receipts.
Let `E*` be the character obtained by source duality. The modular Verlinde
formula, with `dim Z(C)=D^2`, gives the following contribution of one central
simple with restriction vector `v` to a distinguished fusion coefficient:

    c_EFG(v) = beta_E beta_F beta_(G*)
               chi_E(v) chi_F(v) chi_(G*)(v) / (D^2 dim(v)).

Thus `N_(A_E,A_F)^(A_G)=sum_Z c_EFG(F(Z))`. In particular the third character
is dualized. The program checks source character multiplication, duality,
and orthogonality through the frozen character-table adapters. It uses all
196 triples `E<=F`, `G`, with each index non-FP; this contains redundancies
but omits no equation in this stated family. The symmetric normalized
triple-product cache preserves exactly these 196 output equations.

## Finite integer system

For each non-FP character E and each allowed low restriction v of dimension
beta_E, introduce an integer `x_(E,v)>=0` with sum_v x_(E,v)=1. Thus these
variables are genuinely one-hot. Low duality gives
`x_(E,v)=x_(E*,v*)`. Full distinguished modular symmetry is imposed in every
coordinate of the full character splitting field. The central tensor unit
is fixed once and moved to the right-hand side.

Alternatively, one may fix each member of a complete list of fully labeled
low frames separately. That is the R982 path. Its range/PSD pruning retains
all possible high columns: if `H=sum v v^T`, then each nonzero v belongs to
`range(H)` and `v^T H^+ v<=1`. This is checked on an exact nonsingular
principal rank submatrix, without floating eigenvalues.

For high restrictions, use one nonnegative **integer** variable per complete
source-duality orbit of restriction vectors. It counts the number of central
simples of each member restriction. A duality-fixed restriction may have any
nonnegative count. These variables are not the averaged phase-trace weights
of the earlier cone, and those phase-trace weights are never assumed integral.

The Gram equations are

    sum_low x_v vv^T + sum_high n_O sum_(v in O) vv^T = B - fixedGram.

The diagonal equations give finite upper bounds on every high variable.
The code uses an enlarged bound when independent low choices have not yet
been fixed; enlarged bounds are safe necessary relaxations.

Expand every cubic coefficient in the **full splitting-field power basis**.
All nonconstant coordinates must vanish. The constant coordinate must equal
a new nonnegative integer variable `N_EF^G`. The power basis need not be an
integral basis: these equations ask for equality to a rational integer, not
for arbitrary algebraic integrality. The upper bounds on the new variables
come from the fixed constant contribution plus the sum of positive
variable coefficients times their finite upper bounds. This remains a
valid upper bound even when some coefficients are negative.

The isolated `quadratic/atomic_galois_balance.py` adds further integer rows.
For every A_E, the numbers

    lambda_E(v) = beta_E chi_E(v) / dim(v)

are the eigenvalues of its integer fusion matrix, one per central simple.
Consequently the total multiplicities of every complete Galois orbit of
these eigenvalues agree. Exact automorphisms and full orbit coverage are
checked in the splitting field. The fixed constituents contribute to the
right-hand side. A missing conjugate can force a nonnegative candidate
multiplicity to vanish, but no conjugate may be omitted from the audit.

## Exact arithmetic conclusions

After clearing denominators, all equations have the form `A z=b`, with
integer A,b and explicitly bounded nonnegative integer variables.

* The finite-box propagator applies one exact equality at a time to tighten
  integer intervals and checks its residual coefficient gcd. Every step is
  necessary. Its complete deterministic sequence is reconstructed on replay.
* A modular annihilator `y A=0 mod m`, `y b!=0 mod m`, for any integer m>1,
  is an exact integer-lattice obstruction. A rational annihilator
  `y A=0`, `y b!=0` is also an obstruction. Both are verified against **every
  original column**, independently of the Hermite discovery algorithm.
* Row Hermite form is computed on the list of column vectors, retaining its
  nonzero rows between batches. Equality/reduction in that lattice can show
  signed integer lattice membership. It does not enforce nonnegative bounds
  and is never described as a model or as full integer feasibility.
* A numerical MILP result is only a proposal. An affirmative result is used
  only after all entries, bounds, and original equations pass an exact
  integer check. A numerical infeasibility status proves nothing here.

`verify_lattice.py` independently checks 600 complete finite-field systems,
80 incremental-versus-one-shot exact Hermite calculations, and 300 complete
bounded integer systems. `verify_control.py` uses the actual 64-simple center
of Fibonacci tensor Vec(C4), with complex characters. It checks every Gram,
full-S, duality and cubic equation, then every modular, Hermite and box
validation. The Galois adapter separately checks all eight actual degree-64
integer characteristic polynomials, including nonreal eigenvalues.

All published results store source/domain hashes and compact witnesses or
reconstruction receipts. Dense integer matrices are regenerated exactly and
are not serialized as publication artifacts.

## Additional exact reductions

The FP-dimension identity for a tensor product gives the sharper universal
bound `N_(A_E,A_F)^(A_G) <= floor(beta_E beta_F / beta_G)`. The isolated
`quadratic/fp_fusion_bounds.py` reconstructs these positive dimensions in the
FP field from allowed restriction columns and uses its exact ordered
embedding to take the floor. It takes the minimum with the earlier bound;
it changes no equation or variable interpretation.

If an eigenvalue occurring in a proposed restriction has a Galois conjugate
absent from every remaining restriction and fixed constituent, equal
multiplicities force that entire candidate to have zero nonnegative
multiplicity. Iterating this deletion is valid because no actual simple can
be the first deleted counterexample. A fixed constituent encountering a
missing conjugate instead certifies that the domain is impossible. The
isolated quadratic implementation records the full original domain and the
missing-conjugate evidence; actual complex-center controls must remain.

`equations.py` divides each integer equality by the gcd of all its entries
including its right-hand side, normalizes its sign, and removes exact
duplicate or zero equalities. These operations preserve the solution set
over the integers. The representative row and signed scale are retained.
A compact-system annihilator can be lifted by the inverse row scales,
cleared of denominators, and directly checked on the original system.
This compression is independent of numerical rank or tolerance.
