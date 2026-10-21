# R1154: bounded simultaneous pair-product refinement

This is a separately verified necessary-condition addendum to the frozen evidence. It refines a necessary
central-object pattern domain and makes no ring exclusion or categorification
claim. The general-complex interpretation is conditional on the already accepted
Galois-to-pseudo-unitary reduction. The low self-duality and fourth-Verlinde
normalization are as independently reviewed for the common quartic Gram lemma.

The input domain comprises all 1,238 cubic survivors among the 14,211 exact
integral Gram patterns for low index 31. The verifier reconstructs the cubic
coefficient rows and the complete survivor list, binds the ordered 16 high-column
types, and checks all 35 scalar quartics exactly (including irrational parts and
divisibility). It verifies that every pattern has the same restriction Gram
`Q = M M^T` of rank 3. The pair Gram `G` has rank 3 in every case.

For the minimum-norm solution `X0` to `M X = T`, every residual Gram is
`G-X0^T X0 = alpha h^T h`, with
`h=(1,0,1,-1,0,0,0,1,-1,1)` in lexicographic pair order
`11,12,13,14,22,23,24,33,34,44`. All four values of `alpha` are positive, so
all 1,238 patterns pass the real PSD and residual rank bound. Orthogonality of
the minimum-norm solution gives every possible factorization the form
`X=X0+t h`, `M t=0`, `sum(t_i^2)=alpha`.

For one individual high row let `q=X0[i,0]`. Since `h[0]=1`, integrality forces
`t_i=n-q` for an integer `n`. All ten coefficient inequalities give a closed
integer interval `L<=n<=U`; the zero entries of `h` and all congruences are
checked separately. The least possible square is attained by the clipped floor
or ceiling of `q`. If the sum of these coordinate minima, counted with the exact
high multiplicities, exceeds `alpha`, no required factorization exists.

| alpha | Original patterns | Minimum-square exclusions | Propagation exclusions | Remaining |
|---|---:|---:|---:|---:|
| 92/205 | 8 | 8 | 0 | 0 |
| 262/205 | 864 | 852 | 6 | 6 |
| 672/205 | 300 | 32 | 48 | 220 |
| 1082/205 | 66 | 0 | 0 | 66 |
| Total | 1,238 | 892 | 54 | 292 |

The second, optional screen uses only individual coordinate domains. Start with
`t_i=n-q` in the allowed interval and `t_i^2<=alpha`. Repeatedly require the sum
of minimum squares to be at most `alpha`, the sum of maximum squares to be at
least `alpha`, and zero to lie in each coordinate interval of `M t`. For each
single candidate value, apply the lower norm and linear interval tests with that
one row fixed and the other rows free. A failing value is removed from every
interchangeable row of the same high type. Each removal is necessary, and the
finite domains only shrink. Here there are at most four values per coordinate
and at most three passes; no coupled assignments are enumerated. The 54 further
exclusions terminate as 34 upper norm failures, 16 linear interval failures, and
4 lower norm failures. The 292 remaining domains are not feasibility witnesses.

The frozen height-six campaign excludes indices
`207,208,376,377,898,899,1407,1408`. These are exactly the first group above and
are already among the 892 first-stage exclusions. Thus the union excludes 946
patterns, 938 beyond the earlier height-six exclusions, and the intersection of
all surviving domains has size 292. The reconciliation uses the frozen
certificate labels and hashes; it does not rerun the height-six system.

The three portable scripts accept `--root REPO` and write JSON only to stdout.
Their normal and `python -O` outputs are byte-identical. The first receipt binds
26 repository source files and its verifier hash; the second binds the first
receipt and its own verifier; the third additionally binds the frozen height-six
certificate. All checks use explicit exceptions rather than assertions.

Files: `r1154_quartic_necessary_filters.py/.json`,
`r1154_quartic_coordinate_propagation.py/.json`,
`r1154_quartic_reconcile.py`, `r1154_quartic_reconciliation.json`.
