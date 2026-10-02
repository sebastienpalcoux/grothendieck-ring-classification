# Necessary integer lifting of restriction products

Date: 2026-10-02. Ring: R6_8_1660. This document proves a necessary profile test; it makes no claim that the ring is excluded or realized.

## 1. Restriction vectors and coefficient bounds

Let C be a fusion category over the complex numbers and F:Z(C)→C the forgetful tensor functor. No pivotal, spherical, or unitary structure is required for the following argument. For each simple central object A write u_A for the vector of multiplicities in F(A). These are nonzero vectors of nonnegative integers. Tensor functoriality gives

    u_A * u_B = Σ_D N_AB^D u_D.

The product on the left is computed using the given base fusion tensor. For nonzero vectors u,v,w define

    Q(u,v;w) = min_{k:w_k>0} floor((u*v)_k / w_k).

Every coefficient N_AB^D is at most Q(u_A,u_B;u_D). Frobenius reciprocity gives

    N_AB^D = N_{D B*}^A = N_{A* D}^B.

All six base simples in the input ring are selfdual, so F(A*) has the same restriction vector as F(A), even when A is not selfdual. Therefore each individual coefficient is bounded by the finite integer

    B(u,v,w) = min(Q(u,v;w), Q(w,v;u), Q(u,w;v)).

If w is the restriction of m_w different central simples, their aggregate coefficient x_w satisfies 0≤x_w≤m_w B(u,v,w). This aggregation preserves the number of simple labels. It does not identify objects that have equal restrictions. It is a relaxation: additional compatibility between individual coefficients can be omitted in a necessary test.

If w is a single invertible base simple, every central simple in that fibre has Frobenius–Perron dimension one and is invertible. An invertible simple appears with multiplicity at most one in the product of two simples. The code accordingly replaces its individual cap by min(B,1).

## 2. Distinguished unit and unresolved central duality

Let 1_Z denote the central unit and e_0 its restriction. Its coefficient in A⊗B is δ_{B,A*}. The input ring being selfdual does not assert that every central object is selfdual.

For each present restriction type u there exists an actual dual pair (A,A*) with both restrictions u. Hence u*u must admit a decomposition with the coefficient of 1_Z fixed to one. If the fibre multiplicity m_u is at least two, there is also an object B in that fibre other than A*. Hence the same restriction product must also admit a decomposition with the coefficient of 1_Z fixed to zero. These are separate necessary tests, with independently chosen output coefficients.

For two different restriction types u and v, B cannot equal A*, so the distinguished unit coefficient must be zero. Together these observations give all unit cases used by the runner without choosing or assuming a central dual permutation.

For a prescribed unit coefficient δ∈{0,1}, remove one copy of the generator e_0 from its fibre and subtract δe_0 from the target u*v. Any remaining central simples whose restriction is e_0 stay in the generator multiset. This distinction matters for general examples such as Z(Vec(C2)); the R1660 input has a unique unit restriction.

The resulting bounded integer problem is

    Σ_w x_w w = u*v − δe_0,     0≤x_w≤m'_w B(u,v,w),     x_w integral,

where m'_w removes precisely the distinguished unit copy. Coordinate bounds using the reduced target can safely reduce the aggregate caps further. A negative target or a completely exhausted infeasible system contradicts the given profile.

## 3. Source coverage and the new test scope

The frozen packet-Gram calculation retained 1,136 labelled profiles. Their full restriction-column multisets are reconstructed from the six low columns and the high-column multiplicities in the pinned source files. Raw repeated columns are counted, not discarded. Every reconstructed multiset is checked against the full six-by-six restriction Gram matrix recorded in the input.

Ignoring charge labels and merging identical ungraded multisets gives 628 distinct problems. Every original low branch, character labelling, and source profile index remains listed as an alias. Thus an ungraded obstruction for a stored multiset applies to all its listed aliases, regardless of their possible charge allocations. No rejection uses the single charge witness stored by the earlier packet-Gram search.

Earlier low-center systems imposed restriction-product constraints for pairs of the six low columns. The present default job omits pairs for which both restrictions have nonzero unit coordinate, and omits invertible input restrictions. It tests the additional low–high and high–high pairs. Skipping any pair weakens a necessary test and cannot invalidate an obstruction found for a tested pair. This is an additional implemented screen; no strict improvement in the actual frontier is claimed before a previous survivor fails it.

## 4. Exact exhaustion, budgets, and returned results

The generator counts have finite caps. The solver enumerates them by depth-first search. Pruning uses only nonnegativity, exact interval bounds, and divisibility by the gcd of the remaining coefficients, applied to every coordinate and every coordinate difference. These conditions are necessary for the residual equation. A state is marked impossible only after exact pruning or after all admissible branches are exhausted.

A node or time limit raises a separate budget condition. It unwinds without marking unfinished states impossible and returns `unknown_budget`. A returned feasible coefficient vector is checked against every exact equation and cap. At the profile level, `profile_rejected` means a candidate obstruction awaiting independent replay; `pairwise_pass` proves only feasibility of all individually selected tests.

The checkpoint binds the complete input hash, algorithm version, and runner-file hash. It stores completed pair results, including witnesses, and the limits used for unknown results. Raising limits or using `--retry-unknown` permits another attempt. A returned candidate includes the source profile key, original aliases, both input restrictions, unit requirement, full bounded system, and all restriction multiplicities, so the finite failure can be reconstructed and replayed.

These arguments are general necessary conditions for fusion categories. Applying them to this particular finite list inherits the assumptions and completeness of the preceding center-profile reduction. Even failure of every listed profile must be independently replayed and combined with that reduction before announcing exclusion of the original ring. Passing all tests supplies neither simultaneous fusion coefficients nor associativity nor a categorical model.

## 5. Controls

The positive controls are the known centers Z(Rep(S3))≃Rep(D(S3)) and Z(Vec(C2)). The first includes three distinct central simples with the same standard-representation restriction; it tests both required unit coefficients. The second includes multiple objects restricting to the base unit and checks that only the distinguished central unit is removed.

Negative and boundary controls include a one-dimensional integer-semigroup hole, incorrect witness rejection, zero-node and zero-time budgets, and checkpoint/input mutation rejection. Independent finite Cartesian-product enumeration checks the bounded solver against small random systems. The supplied receipts report only these controls and a bounded one-profile pilot; the full R1660 scan has not been run.
