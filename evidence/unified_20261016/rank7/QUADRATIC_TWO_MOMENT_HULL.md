# A finite two-moment hull for the quadratic conductors 12 and 24

Let K=Q(sqrt(3)) or Q(sqrt(6)), of conductor f=12 or 24. For a root of
unity theta, let t(theta) be the normalized relative trace to K, taking
the trace from any cyclotomic extension containing K and theta. This is
independent of the chosen larger extension. We consider the pair
(t(theta),t(theta^2)) in the real vector space K^2.

**Lemma.** Every such pair belongs to the convex hull of the pairs
obtained from roots of unity of order dividing 2f. In coefficient
coordinates (a,b,c,d), representing (a+b sqrt(r),c+d sqrt(r)), it suffices
to use the following nine vertices:

    (1,0,1,0), (-1,0,1,0),
    (1/2,0,-1/2,0), (-1/2,0,-1/2,0), (0,0,-1,0),
    (0,h,s,0), (0,-h,s,0), (0,0,0,h), (0,0,0,-h),

where (r,h,s)=(3,1/2,1/2) or (6,1/4,0).

Here convex combinations have real nonnegative weights; the assertion
is a necessary moment constraint and does not impose a twist-order bound.

## Proof

For a primitive n-th root, if f does not divide n then the normalized
relative trace is the rational Ramanujan value mu(n)/phi(n). When
f divides n, the ordinary Ramanujan contribution vanishes, since f is
not squarefree. The induced quadratic Gauss sum is nonzero precisely
when n=f*m with m squarefree and coprime to 6. It then equals the
primitive f-th-root value, with a sign depending on the root exponent,
times mu(m) chi_f(m)/phi(m). Thus nonzero irrational first moments
occur only in this case.

Write a=h sqrt(r). For n=f*m the pair is

    (+/- a mu(m) chi_f(m)/phi(m), mu(m)/(2 phi(m)))  if f=12,
    (+/- a mu(m) chi_f(m)/phi(m), 0)                if f=24.

For m=1 these are the two displayed primitive-f vertices. For m>1,
phi(m)>=4. Put w=1/phi(m). Choose the primitive-f vertex with the
required sign of its first coordinate and give it weight w. If f=12
and mu(m)=-1, its second coordinate exceeds the required value by w.
The remaining weight 1-w can supply the rational vertical correction
-w/(1-w), which lies in [-1,1]. In every other case the remaining
correction is zero. The whole rational vertical segment (0,[-1,1])
is already in the convex hull of the order-one, order-two and order-four
vertices. Therefore all these cases lie in the claimed hull.

An irrational second moment with zero first moment occurs only when
n=2f*m, with the same restrictions on m. It is
(0,+/- a mu(m) chi_f(m)/phi(m)), in the segment joining the two
primitive-2f vertices. Higher powers of primes shared with f give zero
in both coordinates, except for purely rational cases below.

For rational nonzero moments, odd squarefree n gives (q,q), with
q=mu(n)/phi(n) in [-1/2,1]; twice an odd squarefree number gives
(-q,q). These lie respectively in the segments joining the order-one
and order-three vertices, and the order-two and order-six vertices.
When n is divisible by four, a rational first moment vanishes and the
second belongs to [-1,1], already covered by the vertical segment.
The remaining cases give (0,0). This proves the lemma.

## Saturation restriction

For a central simple with nonrational dimension ratio z/D in any of
the three rank-seven cases, the audited conductor-equality theorem and
quadratic residue refinement force theta^f=1 and chi_f(k)=-1 at
primitive f-th roots. Hence only the first five rational vertices and
the negative primitive-f vertex (0,-h,s,0) are needed. For f=24,
the additional actual pairs (0,0) and (0,1/2) are already in the
convex hull of those five rational vertices.

The unrestricted nine-vertex hull remains valid on every other row.
Together with the two exact induction trace identities and the Gram
identities this gives a finite rational linear feasibility relaxation.
Any numerical infeasibility must still be converted into an exact
certificate before it can establish a classification result.
