# Exact cubic comparison on the two trivalent maps

Use the explicit maps r,s,t0,t1,t0',t1' defined in `R1768_TWISTED_PRECURSOR_AUDIT.md`. The outcome is

    R=I_2.

Thus the first, linear associativity equation for 1+sigma is automatically satisfied. It provides no exclusion and does not reduce the two multiplication variables to one.

## The contraction

The maps l_i=s(t_i' tensor 1_sigma) form a basis of Hom(sigma³,1), with dual basis d_j=(t_j tensor 1_sigma)r=t_j r. The coefficient matrix comparing s(1_sigma tensor t_i') with l_j is

    R_ij=s tau(t_i') t_j r.

Write z=(0,6), Z=lambda_z, and use a,l,m,n for diagonal elements (a,a), etc. Since tau(Z)=−U_z Z and s tau(p)=s, expanding gives

    R_ij=(-1)^i/144 sum_(a,l,m,n)
      lambda_(-a) S'_a U_z^i Z^i rho(T'_(l+iz))
      T_(m+jz) Z^j S_n lambda_n.

Here i,j∈{0,1}; the four sums range over the twelve diagonal elements.

The identity alpha_z rho=rho lets Z pass through rho(T'_g). Further,

    S'_a U_z^i=(-1)^(ia)S'_a,
    Z^i T_(m+jz)=(-1)^(im)T_(m+jz)Z^i,
    Z^(i+j) S_n=S_(n+(i+j)z)Z^(i+j).

In RW's formula for rho(T'_g), its first and third terms vanish in the contraction rho(T'_g)T_b S_c. Only its middle term remains, giving

    rho(T'_g)T_b S_c = (lambda/12) q(g)B(g+c,b) S_c.

This contraction is independent of the finite quantum dilogarithm values E(g). Consequently S'_a forces a=n+(i+j)z. If i≠j this is impossible because a,n are diagonal and z is not; hence R_ij=0.

If i=j, a=n and Z^(i+j)=1. The remaining expression is

    R_ii=lambda/1728 sum_(a,l,m)
      (-1)^[i+i(a+m)] q(l+iz) B(l+a+iz,m+iz).

The two factors are

    q(l+iz)=(-1)^[i(l+1)],
    B(l+a+iz,m+iz)=(-1)^[i(l+a+m)].

Every summand therefore equals one. There are 12³=1728 summands, proving

    R=lambda I_2.

## The RW scalar for this actual input

RW §4.3 identifies lambda with the Dedekind eta multiplier mu_gamma. For gamma=[[145,12],[12,1]], the standard eta-multiplier formula for positive c gives

    mu_gamma=exp(pi i[(a+d)/(12c)−s(d,c)−1/4]).

Here s(1,12)=55/72 and (145+1)/144=73/72, so the exponent is zero. Thus lambda=1. The same value follows directly from gamma=T^12 S T^(−12) S^(−1), using eta(z+12)=−eta(z) and eta(−1/z)=sqrt(−iz)eta(z).

The companion standard-library verifier checks the rational Dedekind sum and all finite signs in the diagonal contraction. It does not check the quadratic associativity equation or construct a separability idempotent. The nonlinear, E-dependent part of the algebra problem remains open.

## One normalization equation from the quadratic part

One coefficient of the quadratic associativity equation is also independent of E. Distinguish the RW duality parameter d_RW from FP dimension: put c=d_RW/12 and kappa=sqrt(d_RW)/sqrt(12), so kappa²=c. RW has d_RW=−12/E(0), and its specified Stark realization has c=6−sqrt(37), although the positive FP dimension is 6+sqrt(37).

Evaluate the sigma-output associativity equation on (r tensor 1_sigma). Its left side equals 1_sigma. Direct cancellation with RW's rho(S'_g) formula gives

    (1_sigma tensor s)(r tensor 1_sigma)=c^(-1)1_sigma.

The other coefficients are

    t_i' tau(t_j') r p = delta_ij (-1)^i lambda^(-1)/kappa ·p.

To see this, use s and t_i' with their displayed primed bases. Only the first term of rho(T'_g) survives when it is followed by S_n. Its coefficient is lambda^(-1)/(sqrt(d_RW)sqrt(N)), with sqrt(N)=12. The off-diagonal term contains pZp=0. On the diagonal the remaining 12³ terms have phase (-1)^i. This gives exactly the coefficient above. The denominator sqrt(d_RW) is essential; it is not a numerator.

Since lambda=1, any multiplication must therefore satisfy

    b0²−b1²=(c−1)/kappa.

This is a nonempty conic over C. It is a necessary normalization equation, not a solution of the remaining E-dependent coefficients. In particular it supplies no exclusion or algebra existence claim.

Primary formula source: Radchenko--Wheeler, arXiv:2609.21892v1, §4.3 (lambda=mu_gamma) and §5.3 (rho(T'_g)); https://arxiv.org/pdf/2609.21892v1.
