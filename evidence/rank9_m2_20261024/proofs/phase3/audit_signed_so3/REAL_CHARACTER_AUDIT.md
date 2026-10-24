# Independent audit: dual-invariant scalar characters

**Verdict: approved.** The restriction obstruction used for R9_2_1487 is valid for a hypothetical pseudo-unitary categorification. In fact, the argument applies to scalar characters of a noncommutative fusion ring as well. The bounded follow-up below produces no additional exclusions.

## Categorical argument

Let C be a pseudo-unitary fusion category with its canonical spherical structure, let F: Z(C) -> C be the forgetful functor, and let I be its right adjoint. Put D = FPdim(C). For a one-dimensional character chi of K(C), the distinguished simple object A_chi occurring in I(1) satisfies

    [I(1):A_chi] = 1,
    dim(A_chi) = D / f_chi,
    S(A_chi,Z) / dim(A_chi) = chi(F(Z)).

The correspondence between irreducible characters of K(C) and the distinguished central simples does not require K(C) to be commutative. See Deshpande, *On centers of bimodule categories and induction-restriction functors*, [arXiv:1611.04486](https://arxiv.org/abs/1611.04486), Proposition 2.8, Section 2.7, and the character identity in Lemma 4.3. Only the one-dimensional characters are used here.

Assume chi(X*) = chi(X) for every basis object. Since F preserves duals and the modular S-matrix satisfies S(A*,Z) = S(A,Z*),

    S(A_chi*,Z) = dim(A_chi) chi(F(Z*))
               = dim(A_chi) chi(F(Z))
               = S(A_chi,Z).

Invertibility of S implies A_chi* = A_chi. This proof uses dual-invariance directly and does not assume that the category is unitary or invoke complex conjugation of S-matrix entries.

Consequently the vector v of multiplicities in F(A_chi) must satisfy

    v_i >= 0 integral,  v_0 = 1,  v_i = v_(i*),
    sum_i v_i FPdim(X_i) = D / f_chi.

Nonexistence of such a vector excludes a pseudo-unitary categorification. A separately proved general-to-pseudo-unitary gate is required to conclude non-categorifiability in general. For weakly integral rings that gate is the standard pseudo-unitarity theorem; for the non-weakly-integral cases in this project it is the previously audited signed/Galois gate.

The additional induction Gram bounds are legitimate: writing B_ij = [F I(X_j):X_i], the rows of restriction multiplicities give B as a sum of outer products, so v_i v_j <= B_ij. For a noncommutative ring the correct formula is

    F I(X_j) = sum_Y Y X_j Y*.

Replacing this formula by multiplication by a commutative Casimir element is not justified in general. The attached sweep uses the full formula.

## Bounded follow-up on the weakly integral residuals

`weak_real_restrictions.py` reads the original exact tensors in `work/verification_corpus.json` and the residual profile snapshot in `phase3/results/unresolved.json`. It computes scalar characters exactly, tests dual-invariance exactly, and enumerates self-dual restriction vectors with the dimension and Gram bounds above. All dual-invariant scalar-character components encountered have rational formal codegree; none were omitted by the bounded codegree restriction.

The 15 rings are 12, 392, 585, 746, 941, 959, 1025, 1209, 1246, 1254, 1303, 1709, 1759, 1965, and 1988 (all with prefix R9_2_). In particular, noncommutative R9_2_1965 is included with the correct induction formula.

There are **77 Galois components representing 103 dual-invariant scalar characters**. Every component has a self-dual, nonnegative integral restriction witness satisfying the individual Gram bounds. The exact witnesses are recorded in `weak_real_restrictions.json`.

**Result: no additional exclusions from this test.** These witnesses satisfy necessary conditions only; they are not constructions of central simples or categorifications, and the test does not impose simultaneous compatibility among all distinguished simples.

Replay from the research root:

```sh
python phase3/audit_signed_so3/weak_real_restrictions.py
```

No phase-2 files or online material were modified for this audit.
