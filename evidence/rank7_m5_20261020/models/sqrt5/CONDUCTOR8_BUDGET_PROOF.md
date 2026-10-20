# A conductor-eight twist budget for R5039

This is a necessary condition on a hypothetical pseudo-unitary
categorification of R7_5_5039. It does not, by itself, prove an exclusion.
The representation-theoretic setup and universal primitive-vector model are
those of Schopieray, arXiv:2609.35287v1, Lemma 4.1. The following refinement
uses larger unipotent subgroups rather than only the twist-fixed projection.

## Uniform local bound

Let `M=2^a`, `a>=3`, `G=SL_2(Z/M)`, and `U=<t>`. Let `chi=chi_{-8}`
be the quadratic character with values `+1` on 1 and 3 modulo 8 and `-1`
on 5 and 7 modulo 8. In any unitary representation of G, for `r=0,1,2`,

\[
\left\|P_{\langle t^{2^r}\rangle}s
       \bigm|_{V^U_\chi}\right\|^2\leq\frac{2^r}{8}. \tag{1}
\]

As in the cited lemma, it suffices to prove this in
`Ind_U^G 1=C[Omega]`, where Omega is the set of primitive column vectors.
The functions in `V^U_chi` split orthogonally into the big cell, spanned by
`F(p,q)=chi(q)[q odd]`, and the small-cell subspace, supported on `p odd,
q even`. This is the same decomposition used in the proof of Lemma 4.1.

On the big cell, averaging `sF(p,q)=chi(-p)[p odd]` over translations
`p -> p+2^r q j` gives zero unless `q` is divisible by `2^(3-r)`. In that
case it is unchanged. Consequently its squared norm is exactly `2^r/8`
times the squared norm of F.

For the small-cell part put `g(z)=f(1,z)` for even z. Torus equivariance
and U-invariance give

\[
f(p,z)=\chi(p)g(pz),\qquad
g(z)=\chi(1+uz)g(z+uz^2). \tag{2}
\]

The sum of g on `z=2 mod 4` is zero: use `u=2`, so the character
multiplier is -1. The sum on `z=4 mod 8` is zero: use `u=1`.
Both substitutions permute their indicated congruence class, since

\[
(z+uz^2)-(z'+uz'^2)=(z-z')(1+u(z+z'))
\]

and the second factor is odd. Therefore, for `r=0,1,2`, the only surviving
coset average of g modulo `2^r` is the zero coset, and its sum equals
`H=sum_{z=0 mod 8} g(z)`.

The output of the averaged Weyl action is supported on `q odd` and
`p=0 mod 2^r`, has magnitude `(2^r/M)|H|`, and has
`M^2/2^(r+1)` possible nonzero entries. Its squared norm is

\[
2^{r-1}|H|^2
\leq 2^{r-1}\frac M8\sum_{z=0\bmod8}|g(z)|^2
\leq \frac{2^r}{8}\|f\|^2,
\]

where `||f||^2=(M/2) sum_{z even}|g(z)|^2`. This small-cell image is
supported on odd q, while the big-cell image has even q; they are
orthogonal. This proves (1). Frobenius reciprocity transfers the inequality
to every irreducible representation with U-fixed vectors and hence to every
unitary representation, exactly as in the proof of the cited lemma.

Equality on the small-cell part requires g to be constant on `z=0 mod 8`
and zero elsewhere. The two top singular directions are therefore
`F(p,q)` and `chi(p)[q=0 mod 8]`, both pulled back from level eight. This
equality observation is supplementary; the budget below uses only (1).

There is also an exact operator identity. If `R_r` denotes the operator in
(1), the big-cell norm and the small-cell squared norm both scale by `2^r`
relative to `r=0`, and their images remain orthogonal. Polarization gives

\[
R_r^*R_r=2^r R_0^*R_0,\qquad r=0,1,2. \tag{1a}
\]

## Application to the center

The conductor-eight vector is `w=e_{A_+}-e_{A_-}`, where the two
codegree-eight characters are

\[
\chi_\pm=(1,-1\pm\sqrt{-2},-1\mp\sqrt{-2},0,0,0,1).
\]

Its norm squared is 2. For a center simple object Y with restriction row v,

\[
(s w)_Y=\frac{\sqrt{-2}}4(v_1-v_2),\qquad
|(s w)_Y|^2=\frac18(v_1-v_2)^2. \tag{3}
\]

In particular `sum_Y (v_1-v_2)^2=16`; this also follows directly from the
source induction Gram matrix. In the remaining low frame all seven
`I(1)` rows have `v_1=v_2`, so this entire budget belongs to additional
center simples.

Write the FS exponent as `N=2^a m`, with m odd. Apply (1) to the
2-primary factor and leave all odd-primary factors unrestricted. The
projection then selects precisely those twists whose **2-primary order**
divides `2^r`, regardless of their odd part. Thus

\[
\sum_{Y:\operatorname{ord}_2(\theta_Y)\leq2^r}
       (v_1-v_2)^2\leq 2^{r+1},\qquad r=0,1,2. \tag{4}
\]

The three bounds are 2, 4, and 8. This distinction is essential: the
projection used in (4) is onto the specified 2-primary spectrum, not just
onto the globally fourth-root twists.

In fact (1a), tensored with the identity at the odd-primary factors, shows
that the difference-square masses of twists of exact 2-primary orders
1, 2, and 4 are respectively `b,b,2b`, for a common `0<=b<=2`.

The Cauchy theorem restricts exponent primes here to 2 and 5. Among the
ten nonzero/zero relative two-moment types used in the trace calculation,
the nonzero types have orders 1 or 5, 2 or 10, and 4 or 20. Consequently
the cumulative difference-square budgets on these three groups are at
most 2, 4, and 8 respectively. The zero two-moment phase must carry at
least 8 of the total budget 16. Requiring an arbitrary zero-phase object
is much weaker: the relevant zero-phase objects must have `v_1!=v_2`.
The exact operator identity strengthens this to **individual** upper
bounds 2, 2, and 4 for the three nonzero phase groups. Their masses need
not satisfy equality with each other: zero-phase twists with odd part
divisible by 25 may also contribute to one of the exact 2-primary masses.

Combining the first bound with conductor-five saturation gives another
useful formulation. Every high row with `v_3!=v_4` is forced to have a
primitive fifth-root twist, so

\[
\sum_{Y:v_3\ne v_4}(v_1-v_2)^2\leq2.
\]

In an integer orbit enumeration, any four-element orbit with both
differences nonzero is therefore impossible. A two-element orbit with
both differences nonzero can contribute only with absolute first
difference 1 and multiplicity 1.

## Extension through order eight and a sign-safe dichotomy

The same local calculation extends to `r=3`. In the small-cell argument,
perform the cancellation separately on `z=2 mod 8` and `z=6 mod 8`
using `u=2`, and on `z=4 mod 8` using `u=1`. Only the zero coset modulo
8 survives. The big-cell image is now the full Weyl image. Therefore

\[
R_3^*R_3=8R_0^*R_0,
\]

and the actual difference-square masses at exact 2-primary orders
1, 2, 4, and 8 are `c,c,2c,4c`, with `0<=c<=2`.

Duality changes `k=v_1-v_2` to `-k` and preserves the twist. Every active
object (`k!=0`) has a distinct dual with the same squared contribution.
Hence c is an even integer and is either 0 or 2. If c=0, all active twists
have 2-primary order at least 16. If c=2, these four order groups already
exhaust the complete budget 16, so all active twists have 2-primary order
at most 8.

No active twist can have fifth-primary order at least 25. In the c=2
case the largest individual 2-primary-order bucket has budget 8. A
source-field-fixing fifth-primary Galois orbit has length at least 5
within one fixed restriction row; its distinct dual row doubles the
cost to at least 10, exceeding any bucket. In the c=0 case, the
2-primary order is at least 16, so the independent square Galois action
also has an even orbit within the row. Together with the fifth-primary
orbit and the distinct dual row this costs at least 20, exceeding the
entire budget.

For c=0, a 2-primary order `2^a` costs at least `2*2^(a-3)` in one
row and its distinct dual. Thus `a<=6`. The active orders are restricted
to

\[
\begin{array}{c|c}
c=0&16,32,64,80,160,320\\
c=2&1,2,4,5,8,10,20,40.
\end{array}
\]

All these arguments use duality and automorphisms fixing the complete
source character field. They do **not** assume that the raw quadratic
transport T has nonnegative entries on restriction rows. In general the
actual Galois row can be `-T(v)` rather than `T(v)`; unsigned transport
orbit arguments must not be substituted here. In particular, the
two-row possibility in the preceding section is retained.
