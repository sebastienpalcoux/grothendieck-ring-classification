# Independent audit of the C36 near-group model for R12_1_623

## Verdict

The construction applies to the explicitly reconstructed complex spherical TPE precursor. It does not require an arbitrary spherical near-group category to be in a unitary classification, and it does not assert unitarity. The needed transport can be restricted to mixed associators and Fourier idempotents; the difficult all-noninvertible associator block is not involved in the central-H or pointed-square calculation. The remaining noninvertible multiplication is forced by elementary fusion-ring identities.

## Primary sources checked

1. He–Liu–Lu–Palcoux–Ren, https://arxiv.org/html/2610.11652v1: Theorem2.10 constructs the cyclic scalar solution, Theorems2.3 and5.4 reconstruct an actual spherical fusion category, Lemma2.14 gives the Izumi parameter dictionary, and Lemma4.14 supplies algebraic dual-basis transport without Hermitian reflection. Corollary6.6, rather than Proposition6.4, supplies positive spherical Galois conjugates.
2. Evans–Gannon, https://arxiv.org/pdf/1208.1500, Section4.3, Eqs.(4.48)–(4.50): for multiplicity n=|G| the invertible central lifts exist uniquely, with self-braiding b(g,g).
3. Izumi, https://arxiv.org/pdf/1512.04288v2, Section12.1/Theorem12.5: the left and right character shifts and the pointed-channel character average. The stronger Corollary12.7 cannot be substituted, because the restriction of a to H is nontrivial in this application.

## Why positivity is unnecessary for the required central lift

A half-braiding on an invertible g is tested on pairs of simple objects Y,Z. Its hexagons involve only associators with g among the three original inputs. Even for Y=Z=X, these are mixed associators, not the all-X associator. Naturality at the multiplicity vertices is expressed by the three marked group insertions on V=Hom(X tensor X,X).

The algebraic TPE reconstruction specifies these mixed data. In its basis v_h:

    pi_z(g) v_h = chi(g,h) v_h,
    pi_x(g) v_h = v_(h+g),
    pi_y(g) v_h = a(h)/a(h-g) v_(h-g).

Consequently

    pi_x(g) pi_y(g) pi_z(g) = a(g)^(-1) id_V.

This follows solely from a(h-g) chi(h,-g)=a(h)a(g). The remaining mixed identities are bicharacter multiplication and a(g)^2 chi(g,g)=1. Thus the central-invertible calculation of Evans–Gannon transports using ordinary inverse mixed vertices and bilinear dual bases; no coefficient beta or Hermitian reflection condition occurs. The explicit TPE construction is the object being used, so no completeness assertion about arbitrary spherical near-group categories is needed.

For H=6Z/36, b=chi^(-1) restricts trivially to H times H. Uniqueness of the central lifts (the universal grading is trivial) makes the lifts close under multiplication. The regular algebra A=sum_(h in H) h is therefore a genuine connected commutative separable algebra in the center. Its right-module category is a fusion category. This is the categorical construction; the numeric ring match is not being used as a substitute for it.

## The minimal quotient calculation

The six invertible module objects are indexed by G/H=C6. The induced noninvertible splits using the six Fourier idempotents of C[H]. Since H=H-perp, the pairing G/H -> H-hat is perfect. Left and right multiplication shift the Fourier character with opposite signs, so these six noninvertibles form a free orbit and satisfy sigma u_g = u_(-g) sigma.

The pointed summand of sigma squared is determined by the scalar projector

    (1/6) sum_(h in H) a_I(h) b(h,g).

Here a_I(6j)=(-1)^j. The projector is one exactly when g is 3 modulo6. Thus the unique pointed summand is z=u_3. This character calculation uses the mixed vertices and their inverses; it has no positivity or all-X-block input.

We can now avoid the more elaborate noninvertible-channel calculation in Izumi's operator-algebra proof. Write

    sigma squared = z + sum_(j=0..5) m_j u_j sigma.

Associativity with each u_k implies m_(j+2k)=m_j. Thus m_j is a on even j and b on odd j. The dimensions are FPdim(sigma)=3+sqrt(10), so their quadratic equation gives 3(a+b)=6, or a+b=2. Since sigma*=z sigma and the mixed action is inversion, (u_j sigma)*=u_(j+3) sigma and (sigma squared)*=sigma squared. Duality gives a=b. Therefore a=b=1.

All fusion coefficients are now forced and are exactly R12_1_623. This last argument uses only associativity, dimensions, and duality; it avoids a positivity-sensitive interpretation of orthogonal projections.

## Independent replay

verify_R623_condensation.py uses exact exponents modulo72 to check all bicharacter, quadratic, and three-insertion identities; H=H-perp; a|H; the pointed-square coset; and the complete R623 tensor. It independently discovers the basis map

    [0,1,10,11,9,2,3,8,5,4,7,6].

All1728 tensor entries match. Associativity and the entire duality anti-involution are also checked. The replay passes with Python -O. This is an independent application/binding certificate, not a proof of the analytic precursor theorem.

## Explicit generator and the five half-braiding checks

The following expands the central-H bridge in the strict mixed-vertex notation used in Izumi Section12.1 and Evans–Gannon Eqs.(4.6)–(4.10). Products here abbreviate the corresponding coherent string-diagram compositions; no factor representation is needed. Write b=chi^(-1), a_I=a^(-1), and use the normalized mixed intertwiner U_h of that convention. Set

    E_h(k)=b(h,k),             E_h(X)=a_I(h) U_h.

In particular, for the generator h=6 of H,

    E_6(k)=exp(-2*pi*i*k/6),   E_6(X)=-U_6.

The mixed coefficients needed below are exactly

    alpha_k(U_h)=b(k,h)^(-1) U_h,
    alpha_h(S_k)=S_(k+h),       U_h S_k=b(h,k)S_k,
    alpha_h(T_l)=b(h,l)T_l,     U_h T_l=T_(l-h),
    X(U_h) S_(k+h)=S_k,
    X(U_h) T_(l-h)=a_I(l)/a_I(l-h) T_l U_h.

Here S_k is the pointed-channel inclusion k -> X squared, and T_l runs through the marked noninvertible-channel basis. These are the mixed insertion identities. The last one is the same diagonal/shift identity exhibited above in the TPE pi_x,pi_y,pi_z basis. Izumi's displayed formula immediately before Section12.1 writes X(U_h) using precisely these coefficients. The bars on roots of unity in the operator notation mean their inverses. They are not bars on beta and do not assert Hermitian reflection of the TPE solution.

The exhaustive naturality/hexagon equations reduce as follows (EG equation numbers):

- (4.6), two pointed inputs: b(h,k+l)=b(h,k)b(h,l).
- (4.7), pointed input on the left: alpha_k(E_h(X)) E_h(k)=a_I(h)b(k,h)^(-1)b(h,k)U_h=E_h(X).
- (4.8), pointed input on the right: the scalar b(h,k) from E_h(k) cancels b(h,k)^(-1) from alpha_h(U_k); the normalized U maps commute in this mixed calculus.
- (4.9), pointed channel of X squared: its right side is a_I(h)^2 b(h,k+h) S_k=b(h,k) S_k, because a_I(h)^2 b(h,h)=1. This equals S_k E_h(k).
- (4.10), noninvertible channel T_l of X squared: its right side is a_I(h)^2 b(h,l) a_I(l)/a_I(l-h) T_l U_h=a_I(h)T_l U_h. The last equality is the quadratic refinement identity. This equals T_l E_h(X).

These five families cover every simple pair and every fusion-channel basis map. They prove the half-braiding directly, using only b,a_I and the mixed vertex coefficients of the algebraic TPE reconstruction. In particular, they do not invoke a unitary classification, a Cuntz C*-representation, or any positivity assertion. The central restriction to H has trivial braiding because b|H times H=1, exactly as required for the regular algebra.
