# Quartic dimension-field audit

AI-generated research · independent verification pending.

## Scope and result

Reviewed §11, “Uniform bounds for quartic dimension fields,” and §12, “Proof of the uniform bound,” in `manuscripts/rank4/papers/companion_sections/11_quartic.tex` and `12_uniform_bound.tex`, including their stated dependence on the central-column, field-descent, trace, and indicator-moment identities. No mathematical defect was found in the reviewed argument. This is an AI adversarial review and exact arithmetic replay, not human verification or Lean formalization.

The quartic result has the correct conditional scope: a self-dual rank-four category whose FP global dimension generates a quartic field is spherical if its FP global dimension is at least 950. Consequently a nonspherical category in this branch has dimension below 950 and multiplicity at most 30. The global proof combines this with the other field branches and the spherical bound to obtain dimension below 1000 and multiplicity at most 31 without an a priori multiplicity assumption. The final classification additionally uses the finite exhaustive certificates; the entire classification should not be described as computation-free.

## Independently checked reasoning

1. **Common quartic field and ratio.** Central induction places `E/D` in the signed order. The order discriminant ratio makes its norm a positive integer square. All conjugates are positive. The simultaneous central columns and spectral domination imply that `E/D` at the chosen largest signed codegree is the least conjugate. These are sufficient for every use of the ratio in §11; no maximal-order assumption is made.
2. **Outside the biquadratic exception.** The short moment alternatives reduce to `u+v≤4/5`: if `sqrt(2)` is present but `sqrt(5)` is absent, the lower bound `u>13/40` combines with `2u+v≤9/8`. The Schur/trace estimates eliminate every square norm at least nine, leaving norms one and four. The elementary bound on `e3(p)` follows by maximizing the symmetric sums of the last three coordinates.
3. **Product minimum.** The constrained Hessian argument correctly forces a boundary coordinate `1/168`. The relaxed three-coordinate minimum is positive because its square-sum budget is below half the square of its sum. The one-small/two-equal branch gives the minimum. Both rational margins in the manuscript are positive and exactly reproduced.
4. **Ratio estimates.** The inverse-coordinate Cauchy bound and product minimization reduce to the displayed one-variable pairs. The lower endpoints, positive denominator conditions, two polynomial decompositions, and positive quadratic lower bounds are consistent. The normalization budget is increasing in both variables on the specified domain. The resulting trace is strictly below 14.
5. **Arithmetic chart.** Positivity of the pair discriminants follows from `S,J>0` after the positive pair sums and products have been imposed. For an irreducible quartic, the quadratic pair field has nonsquare `A` (or `B` when `A=0`); normality is equivalent to `J` being a square in that field. The stated `J`/`Jd` square tests are equivalent. The reducibility checks are exhaustive because all four roots have already been made positive. The norm-four coefficient divisibilities are precisely the quartic d-number criterion.
6. **Scalar comparison.** Independent companion-matrix functional calculus reproduces all 22 traces of `g(alpha)`. Exact Sturm counts certify the exceptional least-root brackets and the remaining least roots below one. The square completion and final strict margin against `4/5` are correct. The degree-two case uses the d-number divisibility, excluding trace three at quadratic norm two.
7. **Exceptional field relative pairs.** Every conjugate of the ratio lies in the signed order: the relevant central quotient is an order unit because it has norm one. Its coefficient-of-unit trace is a positive integer. Expanding this trace yields the manuscript’s pair identity. The proof that `p_j p_k > d p_i` and the ensuing reciprocal pair inequalities are valid. Independent symbolic minimization reproduces the full bootstrap quadratic.
8. **Exceptional field trace.** The lower bound on the other three signed reciprocal masses and `q0<1/85` give the joint `5U+4V` budget. The inverse-sum bound, its derivative estimate, and all three Cauchy interval bounds give the claimed strict trace bound below twelve.
9. **Exceptional field arithmetic.** The integral basis has even trace. Galois-invariant ideals exclude norms 9 and 36; the unique prime over 2 gives the norm-16 argument. The norm-25 coefficient analysis is exhaustive. The two quartic biquadratic fields among trace-at-most-ten rows are different from `Q(sqrt(2),sqrt(5))`. Independent quadratic enumeration leaves exactly `(3±sqrt(5))/2` and `2±sqrt(2)`, which the square-mass inequalities exclude.
10. **Global conclusion.** A degree-three global dimension forces the FP character field to have degree three because it is a factor of a four-dimensional rational algebra and contains that global dimension. The rational case uses weak integrality. The surviving field degrees two and four are treated by the specified theorems. The multiplicity estimate follows from normal fusion matrices and `N_ij^k≤d_i<sqrt(D)`, so integrality gives 31.

## Exact replay receipts

The following targeted programs in `supplements/rank4/unrestricted/` terminated successfully under ordinary Python execution:

- `audit/exact_small_trace_resolvent_chart.py`: 22 rows; trace cutoffs 10, 11, 12, 13 give 7, 9, 19, 22 rows.
- `audit/scalar_certificates/verify_outside_ratio_950.py`: both ratios and normalization/trace margins pass.
- `audit/scalar_certificates/verify_fixed_biquadratic_950.py`: all rational certificates pass.
- `audit/scalar_certificates/root_exact_audit.py`: outside-field product, ratio, and scalar certificates pass.

Two new independent audit programs are saved alongside this report:

- `independent_quartic_chart.py` and `.json`: enumerates 46,488 coefficient tuples, applies independent Newton pruning, explicit discriminants, exact Sturm positive-root counts, irreducibility, and SymPy Galois groups. It does not use the supplied resolvent witnesses or their positivity/normality tests. It finds 1,054 irreducible totally positive candidates and exactly the same 22 abelian quartics, with the same cyclic/biquadratic group labels.
- `independent_quartic_identities.py` and `.json`: independent rational functional calculus for all 22 scalar traces, Sturm least-root brackets, exact symbolic minimization of the fixed-field bootstrap, the golden-ratio pair-square identity, and enumeration of the fixed-field quadratic ratios. All pass.

The first independent program’s reference-chart SHA-256 is `13392960a9e92955d13e4d66f6c3ac76412b8929bd1dd3d02a4023658538456e`.

## Limits

This audit does not independently establish every categorical input proved in the earlier sections, nor rerun the full finite rank-four ring census. It checks that §11 uses those inputs consistently and that the arithmetic/analytic step is valid. The global conclusion remains dependent on the separate audits of those earlier theorems and the finite certificate coverage.
