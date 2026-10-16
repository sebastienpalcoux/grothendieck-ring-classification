# Independent audit of the R820/R869 spherical and Galois reduction

Audited `work/unified/simple_global/SIMPLE_GALOIS_PU.md` and its source-bound
standard-library verifier on 16 October 2026. This is a structural reduction;
neither ring is thereby constructed or excluded.

## Categorical argument

The signed sphericalization argument is sound with the stated normalization.
The two lifts of a self-dual source simple are themselves self-dual: duality
preserves spherical dimension, whereas tensoring with the sign object changes
the nonzero dimension's sign. The lift with second indicator +1 is therefore
well defined. Cyclic reciprocity and dual reflection make the signed tensor
fully symmetric when every basis label is self-dual.

The parity restriction used here follows from the genuine odd-channel theorem:
Liu–Palcoux–Ren–Vercleyen, *Triangular Prism Equations and Categorification*,
arXiv:2203.06522, Theorem 3.9. In a pivotal fusion category a self-dual simple
with indicator −1 cannot occur with odd multiplicity in an adjoint product.
Thus each negative-lift multiplicity in a square channel is even, giving
`N_jj^i − T_jj^i ≡ 0 (mod 4)`. This fixes a multiplicity-one square channel
and leaves only ±2 for a multiplicity-two square channel. I checked the
primary theorem text through the arXiv PDF, rather than using an even-channel
conjecture.

When the unique signed solution is the original nonnegative tensor, every
negative-lift multiplicity is zero. The selected lifts really form a fusion
subcategory of the sphericalization, and the forgetful functor restricts to
a tensor equivalence with the original category. Consequently the conclusion
is sphericality of every hypothetical categorification, not merely existence
of an unrelated spherical model.

For every spherical dimension character, the three stated integral ring
identities give `d(a_i)=x−1` and `d(c_j)=x+1`, since nonzero simple dimensions
exclude `x=±1`. The distinguished square then gives `x^2−7x+1=0`. These are
exactly the two Galois conjugate FP dimension characters. Conjugating the
category and its spherical structure to the positive character produces a
pseudo-unitary category. No unitarizability is inferred.

## Finite calculation

Both normal and optimized Python replays passed, independently invoked with
the repository argument. Receipts are:

- `simple_galois_pu_independent.json`
- `simple_galois_pu_independent_optimized.json`

I inspected the algorithm as well as its output. It binds the tensors by hash,
rechecks all source fusion axioms and all three presentation identities,
reconstructs 35/36 Boolean domains directly from the source, and expands every
ordered associativity equation. Reduction of Boolean monomials by XOR is valid
because the variables square to one. The DFS tests an equation only after all
its variables have been assigned and visits both possible signs at every
unforced variable. Its only pruning is failure of an exact integer equation.
The all-positive solution is unique after 3071/1873 nodes, respectively.

**Verdict: no gap found in the stated general-to-spherical and Galois-PU
reduction. Both rings now have separately proved unitary constructions; this reduction alone does not settle existence.**
