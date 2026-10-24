# A joint quadratic center obstruction

The rank-nine multiplicity-two fusion rings **R9_2_1569** and **R9_2_1886** admit no complex fusion-category categorification. The certificates here exclude pseudo-unitary categorifications; the independently verified signed Galois-pseudo-unitarity gates in `../signed/` upgrade this to general scope. No existence of a pivotal structure on an arbitrary fusion category is assumed.

Both rings have dimension profile `1^4, 2, (2+sqrt(6))^4` and global FP dimension `D=48+16sqrt(6)`. They contain a rank-six subring with profile `1^4,(2+sqrt(6))^2`. Existence of the latter does not imply existence of these extensions. Its exact tensor was retained as a positive control and passes the same relaxed center test through order six.

## Necessary center data

Let C be a pseudo-unitary categorification of a commutative based ring R, with its canonical positive spherical structure. Write F:Z(C)->C for forgetful and I for its adjoint. For every central simple Y put

`v(Y)_i = [F(Y):X_i]`, `z(Y)=FPdim(Y)=sum_i v(Y)_i d_i`.

The exact induction Gram matrix B, computed from the ring, satisfies

`B_ij = dim Hom(I(X_i),I(X_j)) = sum_Y v(Y)_i v(Y)_j`.

Consequently each nonzero restriction vector v obeys all entrywise inequalities `v_i v_j <= B_ij` and the positive-semidefinite inequality `vv^T <= B`. Since B is positive definite, the last condition is equivalent to `v^T B^-1 v <= 1`. In particular `0 <= v_i <= floor(sqrt(B_ii))`, so the enumeration is finite and exhaustive.

Because R is commutative, I(1) is multiplicity free. Its simple summands A_h are indexed by the one-dimensional characters h of R, have dimension D/f_h, and have twist one. Thus `v_0` is zero or one, and the number of columns with `v_0=1` and dimension z equals the multiplicity of z among the values D/f_h. The code implements these counts as linear equations, without selecting and enumerating whole low-column frames first.

For every central simple Y, the number D/z(Y) is an algebraic integer: modular formal-codegree integrality gives `(D/z(Y))^2` integral, which implies integrality of D/z(Y). Moreover z(Y) is a d-number. Precisely, Ostrik's braided squared-norm theorem applies to Y in the center; pseudo-unitarity identifies that squared norm with z(Y)^2. For every Galois automorphism sigma, both `(z/sigma(z))^2` and its inverse are algebraic integers. Integral closure then makes z/sigma(z) and its inverse algebraic integers, hence units. This proves the d-number assertion for z without assuming a general theorem about FP dimensions of arbitrary fusion categories. In the quadratic field Q(sqrt(q)), the condition is checked by `4a^2/(a^2-qb^2) in Z` for z=a+b sqrt(q), b nonzero. Algebraic integrality of a+b sqrt(q) is checked by integrality of its trace 2a and norm a^2-qb^2.

## Additional modular integrality filter

Let N_v be the matrix for multiplication by the based-ring element sum_i v_i X_i. The ring Casimir B acts on the h character by f_h. The eigenvalues of

`M_v = (D/z) B^-1 N_v`

are `(D/f_h) h(F(Y))/z`. The induction-character formula identifies these with `S_(A_h,Y)/z`, which are algebraic integers by the modular Verlinde character formula. Therefore every coefficient of the monic characteristic polynomial of M_v must be an algebraic integer.

This is tested without constructing a splitting field: first compute the rational characteristic polynomial of B^-1 N_v; multiply its coefficient of degree n-j by `(D/z)^j`; then test that quadratic number for algebraic integrality. A rejected vector cannot occur as the restriction of any central simple. This criterion is necessary only; vectors passing it are retained regardless of whether any central simple actually realizes them.

## Quadratic Galois balance

Let sigma be the nontrivial automorphism of the quadratic dimension field, extended to a cyclotomic splitting field of the center. Modular Galois symmetry permutes central simples and gives

`z(Y) -> abs((D/sigma(D))*sigma(z(Y)))`.

The absolute value selects the positive FP dimension. Every dimension must have an available partner under this involution, and the total number of central simples of either partner dimension is the same. Removing unavailable dimensions and imposing these count balances are necessary conditions. They do not require the permutation to preserve restriction vectors or twist values. In these two certificates the Galois-balance rows themselves have coefficient zero in the final separating ray.

## Joint trace equations

For a central simple of twist theta, attach the joint normalized relative-trace vector of `theta,theta^2,theta^3` over the quadratic dimension field. The Cauchy theorem for spherical fusion categories implies that only primes dividing the norm of D can divide the twist order. Here the primes are 2 and 3. The normalized relative traces of powers of arbitrary such roots of unity give exactly the finite list used by `sources/higher_traces.py:trace_types`; at height three it has 15 members, represented by orders dividing 144, together with the zero packet already included in that list. Orders outside the divisor box have all three relative traces zero: a prime-power conductor exponent beyond the box cannot be removed by taking any power at most three. The rational terms are Ramanujan-sum averages; the quadratic terms are primitive quadratic Gauss sums. Both signs are retained. These are joint packets, so different powers of the same twist cannot be chosen independently.

Write t_k for such a packet. The Ng-Schauenburg center-indicator formula gives

`sum_Y v(Y)_i z(Y) t_k(Y) = D * Tr_K(nu_k(X_i))`.

At k=1 the right side is zero for a nonunit simple. At k=2 it is zero for a nonselfdual simple and is +/-D for a selfdual simple. The existing odd-multiplicity indicator lemma forces +1 when some X_j X_j* contains X_i with odd multiplicity. All other signs are relaxed to the full interval [-1,1], giving necessary linear equations with nonnegative slack variables.

The order-three rotation on Hom(1,X_i^3) has cube equal to the identity. Its dimension is the exact integer `[X_i^3:1]`, and its relative trace is a nonnegative linear combination of the normalized character traces of third roots of unity, of total mass `[X_i^3:1]`. This yields the order-three rows. The implementation permits analogous simultaneous constraints for higher orders, but only order three is needed for these exclusions.

Each central restriction vector and allowed twist packet is assigned a nonnegative real multiplicity. The exact Gram equations, the I(1) dimension counts, the dimension-pair counts, and all trace equations then form `A x = b, x>=0`. Every actual center supplies a solution after taking the indicated Galois averages. Relaxing integral multiplicities and indicator signs only enlarges the feasible set.

## Exact contradiction and replay

For both rings the raw-vector enumeration yields 817 vectors. The exact arithmetic and modular filters retain 120 central restriction columns. The height-three system for R9_2_1569 has 111 equations and 1514 variables; that for R9_2_1886 has 109 equations and 1510 variables. The same separating functional applies after the evident relabeling of the rank-six neutral part: it has 32 nonzero entries, satisfies `A^T y >= 0` entrywise, and gives

`b^T y = -5136`.

If x were nonnegative with Ax=b, then `-5136=b^Ty=x^T A^T y>=0`, a contradiction.

The stored ray is in each `R9_2_*_qcenter_h3.json`. To replay from the exact fusion tensors, run from the research root:

```sh
python phase2/quadratic_theory/verify_quadratic_center.py
```

The verifier rebuilds the entire exact integer system, checks all metadata, and evaluates the Farkas inequalities with Python integers. It does not invoke an LP solver. It separately enumerates the full 1,536,640-vector bounded box in Python and checks equality with the native enumerator's 817-element raw set. `verification.json` records both PASS results and SHA-256 hashes of the reconstructed systems. Thus the numerical optimizer is used only to discover a candidate ray, never to certify infeasibility.

The other quadratic attempts in `center_batch.json` are recorded as no conclusion or bounded incomplete attempts. They must not be counted as exclusions. Some batch attempts predate the modular filter and are distinguishable by their metadata.

## Sources and dependencies

- V. Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13 and the induction discussion: <https://arxiv.org/abs/1309.4822>.
- T. Deshpande, *On centers of bimodule categories and induction-restriction functors*, Section 2.7, equations (36) and (39), and Section 4.3, for the induction-character formula used by the modular integrality filter: <https://arxiv.org/abs/1611.04486>.
- V. Ostrik, *On formal codegrees of fusion categories*, including the d-number theorem for squared norms of simples in braided categories, applied as explained above: <https://arxiv.org/abs/0810.3242>.
- S.-H. Ng and P. Schauenburg, *Frobenius-Schur Indicators and Exponents of Spherical Categories*: <https://arxiv.org/abs/math/0601012>.
- P. Bruillard, S.-H. Ng, E. C. Rowell, Z. Wang, *Rank-finiteness for modular categories*, Theorem 3.9 (Cauchy theorem) and modular Galois symmetry: <https://arxiv.org/abs/1310.7050>.
- A. Schopieray, *Categorification of integral group rings extended by one dimension*, final published version, especially the Galois action on dimensions: <https://doi.org/10.1112/jlms.12789>. The older preprint's stronger wording of its pseudo-unitarity lemma must not be substituted for the final Galois-pseudo-unitary statement.
- Project implementations: `sources/higher_traces.py`, `sources/tensor_rotation.py`, `phase2/integral_theory/center_lp.py`; general-scope gate proof and complete certificates in `phase2/signed/THEOREM.md` and `phase2/signed/gate_verification.json`.
