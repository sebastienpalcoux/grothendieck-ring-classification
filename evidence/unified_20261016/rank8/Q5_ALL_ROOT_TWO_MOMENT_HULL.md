# An all-root two-moment hull over Q(sqrt(5))

Let K=Q(sqrt(5)), let t_K be normalized relative trace from a common cyclotomic extension to K, and put u_±=(-1±sqrt(5))/4. For every root of unity θ, the pair (t_K(θ),t_K(θ²)) lies in the convex hull of the following seventeen points:

1. The five rational points (1,1),(-1,1),(1/2,-1/2),(-1/2,-1/2),(0,-1).
2. The six points
   (u_+,u_-), (u_-,u_+),
   (-u_+,u_-), (-u_-,u_+),
   (0,-u_+), (0,-u_-).
3. Negative one-half times each of those six points.

This is a necessary convex constraint for arbitrary root orders. It requires no exponent-prime or conductor bound and makes no assertion that every convex combination is a genuine root pair.

Proof. If the root order n is not divisible by five, K has trivial intersection with Q(θ), so both relative traces are the ordinary Ramanujan averages μ(n)/φ(n) and μ(n/gcd(n,2))/φ(n/gcd(n,2)). For odd squarefree n these are (q,q), q∈[-1/2,1]; for twice an odd squarefree n they are (-q,q). For n divisible by four the first is zero and the second lies in [-1,1]. All these pairs lie in the five-point rational hull; nonsquarefree odd factors yield zero.

Now write n=2^a 5^b m with m odd and coprime to five. If b≥2 or m is not squarefree, both moments vanish: the ordinary Ramanujan term and the induced quadratic Gauss term vanish, and squaring does not remove an odd repeated factor. If a≥3, both moments also vanish, since their orders retain a factor four in the induced Gauss multiplier.

It remains that b=1, m squarefree, and a=0,1,2. The induced quadratic Gauss formula says that inserting the odd coprime factor m multiplies both coordinates of the primitive pair by q=μ(m)/φ(m), with a possible interchange of the signs ± arising from the quadratic character of m. The primitive pairs for orders 5,10,20 are exactly the six points in item2: squaring interchanges the two quadratic trace values at order5 because (2/5)=-1; the order10 first coordinate changes sign; at order20 the first coordinate vanishes. For m=1, q=1. For every other odd m, φ(m)≥2, hence q∈[-1/2,1]. Each scaled pair therefore lies on the segment joining the primitive pair and its negative half. This proves the seventeen-point hull.

The vanishing and induced-multiplier formulas can also be checked from

 t_K(ζ_n^k) = μ(n)/φ(n) + ε sqrt(5) μ(n/5) χ_5(n/5)/φ(n)

when 5|n and gcd(n/5,5)=1, with ε=χ_5(k); the irrational term is zero otherwise. This formula is used only for primitive ζ_n^k. For the second moment, replace n by n/gcd(n,2) and k by 2k/gcd(n,2) in the primitive-order description; equivalently take the primitive root represented by θ². The sign relation between the two coordinates is already built into the six primitive pairs.
