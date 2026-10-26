# Independent audit of the dimension-120 classification and Ising construction

## Dimension 120

The categorical converse in `../d120/theory.md` has been independently reviewed. The following steps are accepted for arbitrary complex categorifications, without an assumed unitarity premise.

1. The exact first-Morita hypotheses are verified independently on all fifteen remaining tensors. The dual has type `(1^20,5^4)`. The prime-dimensional pointed-dual lemma in `forced_group_theoretical.md` proves that its second dual is pointed.
2. The reverse algebra has dimension ten. The actual free B--R bimodule, for regular algebras of dimensions five and two, has ten distinct invertible constituents and transitive support, hence is simple. Its internal end has dimension `10^2/(5*2)=10`. This establishes the subgroup order; it is not guessed from dimension divisibility.
3. The subgroup must be D10. Every normalizer coset contributes character degrees `(1,1,2,2)`, forcing normalizer order twenty. All other double cosets have size fifty and stabilizer C2. A solvable order-120 ambient group would have a Hall subgroup of order forty containing D10; it could contain no size-fifty double coset, a contradiction.
4. The nonsolvable order-120 possibilities reduce to A5 x C2, S5, and SL(2,5). The latter has no D10. In S5 and the trivial graph in A5 x C2, the induced neutral category has dimensions `(1,1,2,2,5,5)`. A dimension-five simple times its dual has dimension 25, exceeding the sum 16 of those neutral simple dimensions, so it cannot have all multiplicities at most one. Only the reflection-sign graph remains.
5. The 5-primary relative cohomology vanishes by restriction/transfer. The 3-primary part is C3 and is fusion-rule invisible by the coprime-twist lemma. The Sylow `V4 x C2` invariant bound and the independent global classes u,v,w show that the ambient 2-primary part is C2^3. Each restricts to the same nonzero class on D10; the relative part is C2^2.
6. All four resulting relative binary classes are explicitly constructed. The independent program `audit_graph_twist.py` checks source module axioms and computes every tensor-product multiplicity by grade-preserving Hom-space equations, independently of the constructor's character projections. All four classes pass in normal and optimized Python.

The new models are **R12_1_142, R12_1_361, R12_1_444**. The control is R12_1_25. The complete converse therefore excludes **R12_1_161, R12_1_211, R12_1_262, R12_1_265, R12_1_312, R12_1_362, R12_1_388, R12_1_453, R12_1_469, R12_1_472, R12_1_503, R12_1_516** over C.

## The new dimension-32 models R12_1_240 and R12_1_408

Take the matched C2-grading subcategory of the product of an Ising category and `Vec(D16,omega)`. Write D16 elements `(a,b)`, with a modulo eight and b modulo two, multiplication `(a,b)(c,d)=(a+(-1)^b*c,b+d)`. The grading is a modulo two. Set

    omega((a,b),(c,d),(e,f))
      = exp(2*pi*i*a*(-1)^b*floor((c+(-1)^d*e)/8)/8).

The rotation coordinate is a crossed one-cocycle modulo eight. Its integral lift has a twisted Bockstein two-cocycle; their cup product has trivial coefficient action, giving the displayed normalized three-cocycle. The independent finite verification checks all 65,536 three-cocycle identities as well.

The object `(1,s)` is an involution with trivial associator on its cyclic subgroup, so `1+(1,s)` is an actual connected separable algebra. Its bimodule category has dimension 32 and the saved fusion tensor of R12_1_240. This is an existence construction, not a lift of a presumed ring automorphism.

The source associators needed for this particular algebra have an Ising tensor-unit argument, so the Ising contribution is identically one; no unverified three-odd matrix associator enters the computation. The more general audit formulas agree with the standard Tambara--Yamagami C2 associators.

`audit_ising_dual.py` independently reconstructs the source fusion rules, verifies all bimodule equations and pairwise simplicity, checks completeness by global dimension, constructs each balanced quotient, and obtains every fusion coefficient from full Hom-space equations. It passes all 1728 coefficients for R12_1_240 and its untwisted control R12_1_28 in both normal and optimized Python.

R12_1_408 uses the same categorical construction with the semidihedral group of order sixteen, multiplication `(a,b)(c,d)=(a+3^b*c,b+d)`, and a saved sixteenth-root-valued cocycle. Its existence is independently established by checking every one of the 65,536 normalized three-cocycle identities on the frozen table; it does not depend on accepting the lift-search implementation. Both selected involutive algebras, with Ising coordinate 1 or psi and group coordinate the reflection, have trivial restricted associator and give the same target tensor. All source module equations and all 1728 coefficients pass the independent Hom-space audit for both witnesses, including optimized Python. The first witness uses the Ising tensor unit, so all needed Ising associator factors are one.

## The new dimension-48 models R12_1_414 and R12_1_531

The ambient groups are respectively `S4 x C2` and the fiber product `S4 x_(C2) C4`. In each case the selected subgroup H of order four maps isomorphically to the abelian quotient Q. Its inverse section and projection to S4 define a homomorphism `s: G -> S4`. If V is the transferred fourth-root-valued three-cocycle on S4, the cocycle `omega=pr*(V)-s*(V)` is a genuine difference of two pullbacks, and its restriction to H is identically zero. Thus the trivial subgroup cochain defines an actual regular algebra. No gauge choice is presumed to trivialize a nonzero restricted cohomology class.

For existence, the transferred origin is not needed as a computational premise: `audit_d48.py` independently verifies each actual saved group table, all 5,308,416 three-cocycle equations, normalization, and trivial subgroup restriction. It then checks all monomial bimodule axioms and full simple-object completeness. It recomputes all 1728 tensor coefficients using grade-preserving Hom equations, independently of the constructor's character projections. The source tensor identifications for R12_1_414 and R12_1_531 pass in normal and optimized Python.

## Portable replay

The four replay programs `verify.py`, `audit_graph_twist.py`, `audit_ising_dual.py`, and `audit_d48.py` use frozen inputs in the local `frozen` directory. Their hash inventory is `frozen/sha256.json`. The cocycle-array checks require NumPy; no repository imports, internet access, symbolic solver, or group database are needed for these positive/exclusion-premise audits. The bounded low-induction experiments are historical attempts rather than classification certificates.

## Dimension 144: accepted exclusion of one Morita branch

The complete appended argument in `../d144/findings.md` has been reviewed. It proves that the t=0 branch of the first Morita reduction is impossible. It does **not** exclude R12_1_180, R12_1_181, R12_1_320 or R12_1_321, which retain the t=3 branch.

In t=0, internal-end dimension arguments force the second integral dual to have type `(1^24,4^3)`. The possible square-root-two splitting of the odd sector either vanishes or would produce a dimension-96 subcategory of the dimension-144 category. The latter violates algebraic-integer dimension divisibility. Thus the full second dual has type `(1^24,4^3,(3sqrt(2))^4)`.

The commuting left and right transitive actions on the three dimension-four objects force a normal common stabilizer H of order eight. Associativity excludes the inverted right quotient action. Choosing a self-dual dimension-four object leaves two coefficient vectors, `(2,0,0)` and `(0,1,1)`. The second has a formal codegree with irreducible polynomial `f^2-99f+2376`; since 2376 does not divide 99 squared, it is not a d-number. The first therefore gives an actual near-group subcategory B of dimension24 and a faithful C3-grading of the dimension-72 integral dual D.

The odd module is indecomposable over B, with four equally sized normalized simples of dimension sqrt(6). Dimension24 implies solvability and hence unitarizability, so the unitary near-group classification is applicable to the actual original B. This is the required categorical premise; the algebraic construction alone is not substituted for a classification theorem. The group-theoretical descriptions of B use S4 with subgroup C4. The module-category dimension formula is `sqrt(4*|K|)*dim(pi)/s`, where `s=|C4 intersection gKg^-1|`. Cyclic stabilizers force `dim(pi)=1`. The only numerical choices are `(K order,s)=(6,2)` or `(24,4)`. A point-stabilizer S3 has trivial intersection with any C4, ruling out the former. The latter requires K=S4 and the trivial associator class.

Both choices in `H^2(S4,C*)` for the subgroup cochain are retained. For either rank-one module over `Vec(S4)`, the dual category is tensor-equivalent to Rep(S4): the subgroup cochain cancels from the module-functor representation law. Thus no additional module choice evades the argument.

Galindo, *Clifford theory for graded fusion categories*, [arXiv:1010.5283v3, Corollary6.4](https://arxiv.org/html/1010.5283v3), now applies directly: M is a D-module whose restriction to the neutral B is indecomposable. Its D-dual is a C3-equivariantization of Rep(S4). A C3 action fixes every simple of Rep(S4), since each dimension has fewer than three representatives. Cyclic projective stabilizers therefore give type `(1^6,2^3,3^6)`. But M is an invertible D-bimodule, so its D-dual must have the type of D, `(1^24,4^3)`. This contradiction excludes t=0. The use of Corollary6.4 avoids assuming a splitting of a quasi-trivial extension.

The first dual consequently has the unique necessary type `(1^6,2^12,3^2,(3sqrt(2))^4)`. Its pointed S3 subcategory has associator trivial on C3 because C3 fixes a dimension-three object, and trivial on C2 because the actual reverse algebra has dimension two. Restriction to the Sylow subgroups detects all of `H^3(S3,C*)`, so the associator is trivial. The original rank-three subcategory is therefore `C(S3,1,C2,1)`, which equals `(Vec(C3))^(C2)` and hence ordinary Rep(S3) by the inversion-compatible Fourier equivalence. Its dimension-six function algebra exists. This does not establish a central embedding in the entire category.

## Bounds on the negative conclusions

The low-induction feasibility experiments yielded no obstruction: six cases have exact feasible moment/positive-semidefinite witnesses, while the two dimension-144 cases remained solver-unknown within the short budget. Neither outcome was promoted to categorification or noncategorification.

A preliminary proposed rejection of `(H8,m=2)` solely by the abelian-group theorem was caught during independent review: noncommutative D8 and Q8 examples exist. The final branch exclusion above explicitly retains and analyzes them. No full dimension-144 ring exclusion is accepted here.
