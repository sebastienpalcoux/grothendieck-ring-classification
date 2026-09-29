# Noncommutative signed spectra and Casimir saturation

Let R be a noncommutative rank-six fusion ring for which every hypothetical
categorical signed quotient is noncommutative. A noncommutative reduction
modulo two suffices; alternatively, exhaust and exclude its commutative
signed sector by the exact character tests below.
Suppose its two linear characters form one real quadratic Galois orbit,
with positive global dimension D in E=Q(sqrt(q)), q squarefree and q=1 mod 4.
Let c denote its unique two-dimensional representation's formal codegree.

Every hypothetical complex fusion categorification has a sphericalization.
The quotient in which the central sign object acts by -1 is an oriented
signed integral algebra A, with coefficients t_ij^k congruent to N_ij^k
modulo two and |t_ij^k| <= N_ij^k. The coefficient-of-unit inner product is
positive definite and has the signed basis orthonormal, and duality is its
adjoint. Thus A_C is a finite-dimensional C*-algebra. Because its reduction
modulo two is noncommutative, or its entire commutative sector has been
excluded, A_C is noncommutative. In dimension six its
Wedderburn decomposition must be C + C + M_2(C).

The spherical dimension character is real and dual invariant. Its field K
has degree at most two, since its Galois conjugates are linear characters.
Central induction applied to the original-character summands of the
sphericalization gives Delta/f in O_K for every original formal codegree f.
In particular D belongs to K; hence K=E and the two linear signed codegrees
are Delta and its conjugate Delta'. Here Delta is the global dimension of
the original hypothetical category. This uses no pivotal structure on that
original category. See the existing dimension-field containment lemma in
papers/chapters/biquadratic_trace.tex and Ostrik, arXiv:1309.4822, Theorem2.13.

There is just one two-dimensional irreducible representation of A_C, so its
formal codegree h is Galois invariant. Formal codegrees are algebraic
integers; consequently h is a positive rational integer. The standard
formal-codegree identity and Casimir trace give

    1/Delta + 1/Delta' + 2/h = 1,
    Tr(Delta) + 8h = sum_(i,j,k) (t_ij^k)^2 <= T,
    T = sum_(i,j,k) (N_ij^k)^2.

The coefficient 8 is essential: on the four-dimensional matrix block the
Casimir acts by 2h. The reciprocal identity implies h>2. Induction also
gives Delta/h in O_E. The original codegrees require Delta/D, Delta/D' and
Delta/c in O_E. Finally Delta is a d-number (Ostrik, arXiv:0810.3242,
Theorem1.2). Its two embeddings are positive, as also follows directly from
the positive signed *-algebra and a real dimension character.

These are a finite exact system: write Delta=(a+b sqrt(q))/2, with a,b
integers of the same parity, a>0, and b^2 q<a^2. Then a<=T-24, and a is
divisible by c. For each a,b the reciprocal identity uniquely determines
h=2/(1-a/Norm(Delta)). Test the displayed integrality requirements and
a^2/Norm(Delta) integral, the quadratic d-number condition. The software
enumerates a superset of all possible categorical solutions, using only
exact rational arithmetic. Empty output excludes categorification.

If every surviving spectrum has trace T, every signed coefficient has its
original absolute value. Exhaust the oriented sign-only associativity
equations, imposing neither commutativity nor indicator normalization.
When every solution is a dual-compatible sign gauge of R, its two dimension
characters are Galois conjugate to the positive character. Therefore a
categorification would have a pseudo-unitary Galois conjugate: its global
dimension then equals the FP dimension (ENO's pseudo-unitarity criterion).
A pseudo-unitary induction obstruction can finish the general exclusion.

## Application to R6_6_170

The original codegrees are 148+24sqrt(37), 148-24sqrt(37), and4, with
representation multiplicities1,1,2. Here T=328. The finite spectrum system
leaves precisely Delta=148+/-24sqrt(37), h=4, both saturating T.
The full sign-only enumeration has1631 DFS nodes and16 solutions; all16
are dual-compatible gauges of R. There are19 complete multiplicity-weighted
induction frames, obtained from146 and25 candidate restriction columns.
Every frame violates an ordinary exact Gram/moment condition. Thus no
pseudo-unitary category exists, and the reduction proves nonexistence of
any complex fusion categorification.

The tensor-only implementation is software/round3_noncommutative.py. Its
verifier reconstructs the finite arithmetic system, all oriented signed
tables, and all19 induction branches; it never invokes a numerical optimizer.

## Exhausting the commutative sector and two further applications

R6_7_200 and R6_8_491 have commutative reductions modulo two. Here the
alternative gate is essential. The oriented coefficient-orbit problem is
restricted by t_ij^k=t_ji^k, intersecting all original parity intervals,
including a forced zero when the opposite coefficient vanishes. This
exhausts every commutative signed quotient without indicator normalization.
Every dual-compatible sign gauge is retained. For each character component,
a zero dimension, disagreement of dual dimensions, or exact original
formal-codegree norm divisibility failure rejects that component.

The two rings yield respectively176 and208 signed tables, forming11 and13
sign orbits and27 and53 character components. All components are rejected.
The norm witnesses use the actual original quadratic codegree polynomial
t^2-1560t+1872, at prime3 or13. The matrix-block formal codegree is12,
not the regular Casimir eigenvalue24. No noncommutative signed table is
silently omitted: that sector is handled by the preceding theorem.

For both rings the remaining noncommutative spectrum system leaves only
Delta=780+/-216sqrt(13), h=12, with saturated Casimir trace1656. Their
sign-only searches have4927 and6463 nodes and16 solutions each; every
solution is an original sign gauge. Each pseudo-unitary induction problem
has10 complete low frames, all rejected by exact ordinary Gram/moment
conditions. Thus both rings are generally excluded. The separate sector
verifier is software/round3_commutative_sector.py; its certificate is
embedded into the complete general certificate before release allocation.

The reusable oriented_extension.nc_certificate helper was also corrected
to distinguish noncommutative source formal codegrees from Casimir
eigenvalues. This changes no inherited allocation: all seven previously
excluded noncommutative census tensors use the multiplicity-weighted
induction checker, which already has the correct normalization. In the
corrected helper each of these three new source tensors passes its own
dimension-character arithmetic, as it must; their exclusions require the
additional complete argument above.
