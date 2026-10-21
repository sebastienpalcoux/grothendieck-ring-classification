# Independent review of the R436 and R3344 general obstructions

The two new arguments support **general complex noncategorifiability**,
subject to their explicitly cited mathematical inputs. Neither argument
assumes that an arbitrary integral or pseudo-unitary category is unitary.
This is a separate computational and mathematical review by another AI
agent; it is not independent human review or a formal proof-assistant check.

## R8_3_436

The source-bound all-512-coefficient crossed-ring match and the exact
all-branch scalar TPE calculation replayed under `python -O`.
The following potentially serious gaps were specifically checked:

1. Thornton's Theorem 1.3 applies without a braiding hypothesis and permits
   simultaneous field conjugation of the category and its tensor functor.
2. The odd self-multiplicity supplies the required positive second indicator
   by the pivotal Fuchs--Runkel--Schweigert theorem.
3. Theorem 2.3 of the October 2026 TPE preprint, viewed merely as an
   existence equivalence, would be insufficient. Its Section 2 expressly
   derives the scalar data from spherical categories; Theorem 4.12 determines
   their full normalized tetrahedral table. Corollary 5.5 unitarizes this same
   table once its Hermitian equations hold. This addresses the distinction
   between constructing one category with the fusion rules and unitarizing
   every category under consideration.
4. Both nondegenerate bicharacters, both dimension roots, all even quadratic
   refinements, and the rotation scalar are accounted for. The reduction to
   the real quadratic `z^2-t*z+1/3`, with discriminant `-d/3`, is exact.
5. Grossman--Jordan--Snyder define tensor autoequivalences in the ordinary
   complex sense (Definitions 2.3 and 3.3, Corollary 3.7). Their Section 4.2
   statement that each Izumi--Xu choice has trivial outer group therefore
   applies to the transported conjugation functor. Inner conjugations fix
   labels in this commutative rank-four ring.

The October preprint's full spherical parametrization and unitary
reconstruction are indispensable external theorem inputs. No Stark
conjecture or general near-group unitarity conjecture is used.

Primary sources consulted:

- https://arxiv.org/pdf/1102.4640, Theorem 1.3.
- https://arxiv.org/pdf/2203.06522, Theorem 3.9.
- https://arxiv.org/html/2610.11652v1, Definition 2.1, Proposition 2.7,
  Theorem 4.12, Corollary 5.5.
- https://arxiv.org/pdf/1211.6414, Definitions 2.3 and 3.3, Corollary 3.7,
  Section 4.2, printed page 10.

## R8_3_3344

The structural proof reduces every hypothetical category to a
group-theoretical one. The delicate steps checked were:

- The rank-three complement is an indecomposable `Rep(A5 x A5)` module.
  Its projective irreducible dimensions must be equal because the displayed
  `J3` action has a one-dimensional positive eigenspace. This gives the
  necessary subgroup order equation `|K|=3*q^2`.
- The subgroup projection argument and the projective character spectrum
  reduce the possible orders to 3, 12, and 48.
- Morita transformation by `Fun(A5)` on both sides is correctly computed
  using projective equivariant bundles on the free `K`-set `A5 x A5`.
  It has `3600/|K|` simples, with a jointly transitive action of invertibles;
  their equal FP dimensions are consequently `q/2`.
- In the order-48 case, each dimension-two simple has `XX*` supported
  exactly on its `V4` stabilizer. The adjoint category is `Vec(A5)`.
  An invertible homogeneous component would have pointed dual, whereas
  its stabilizer `V4` is not normal and a disjoint-conjugate double coset
  produces a dimension-four simple in that dual. This is a contradiction.
- The center and universal-grading argument forces the group in every
  group-theoretical presentation to be perfect. The full finite catalogues
  reduce it to `A6`, and its relevant subgroup to `A5`.
- Restriction-transfer annihilates the relative third-cohomology kernel
  by 6. The explicit normalizer action on integral fourth cohomology of
  `C3 x C3` excludes its 3-primary part. The mod-two stable computation,
  together with the coefficient exact sequence and surjective Schur
  restriction, bounds the remaining kernel by two elements. The old
  nonzero relative cocycle supplies the second element.
- Surjective second-cohomology restriction removes any additional choice
  of the subgroup two-cochain. The two resulting constructions have rank
  nine or the already verified R3342 tensor; neither is R3344.

The no-import checker `verify_relative_cohomology_independent.py` independently
validates the complete saved cohomology basis and every stable class. It uses
permutation multiplication and highest-bit elimination of boundary columns,
instead of the discovery code's semidirect-product arithmetic and augmented
boundary equations. It checks all 360 conjugations for each class. The
degree-two and degree-three stable/kernel sizes are respectively `(2,1)`
and `(4,2)`. Its report is `relative_cohomology_independent.json`.

Fresh checks also passed for the 162-group order-360 GAP scan, perfect-group
counts on every divisor of 360, the tensor/A5 subgroup/nimrep certificate,
the discovery stable-cohomology verifier, and the frozen R3342 verifier's
512-coefficient tensor match. The Python checks were run with optimization
enabled, retaining their explicit validation gates.

Primary sources consulted:

- https://arxiv.org/html/0809.3031v2, Theorem 9.12.
- https://arxiv.org/pdf/math/0111139, Section 3.4, Theorem 2.
- https://arxiv.org/pdf/0909.3140, Theorem 6.1.
- https://arxiv.org/pdf/0709.4326, Theorem 5.1 and its explicit construction.
- https://personal.math.ubc.ca/~adem/simple.pdf, Theorem 1.3.

The finite scripts verify the stated arithmetic and source hypotheses.
The Morita, module-category, transfer, and stable-elements theorems remain
mathematical dependencies, as the main proof explicitly records.

## R8_3_921

Accepted as a general-complex exclusion after an independent mathematical
review and fresh optimized replay of all 131,072 ungauged matrices.

The separable algebra argument only uses the fixed-point module of the
order-two invertible. Its split difference vectors all have squared length
two in the simple-module basis; hence the inherited duality matrix relation
is the ordinary transpose in this basis. Commutativity then makes `S_3`
real normal without imposing categorical unitarity. The two irreducible
quadratic factors have discriminants 40 and -12. All six rational
characteristic-polynomial possibilities are exhausted by the trace and
Euclidean Frobenius-norm bounds. Only two copies of the complex quadratic
remain. The exact regular-ring transport identity forces `S_6=0`, whereas
its fixed-point diagonal has odd parity. This contradiction uses neither
`S_g=I` nor pivotality or sphericality.

The optimized producer replay confirmed 2,096 normal matrices and 16
source-annihilator survivors, all killed by the forced quadratic. The
finite replay is supplementary to the complete trace/norm argument.
