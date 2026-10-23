# New R928 / R941 actual-twist orbit campaign

This package searches new necessary systems. It does not replay a known rational
phase witness as an exclusion search. Its phase variables count actual roots,
and its cyclic rotation variables count individual Fourier eigenspaces.

The complete inherited domains are R928 patterns 40,49,186,191, and R941 charge
allocations 8,19,21,31,34,43,45,56,60,72,73,77,79,85. These are the surviving
domains of the repository's exact previous reductions. Those reductions, the
positive spherical/Galois gate, categorical Cauchy prime support, the forced
central semion/fermion theorem and the saturated support theorem remain
prerequisites. This adapter does not claim independently to reprove all earlier
reductions. A new exclusion applies globally only after combining a certificate
for every branch with those established prerequisites.

## Why the actual twist domain is finite

Put K=Q(sqrt(2),sqrt(3)) and
D=144+96sqrt(2)+80sqrt(3)+56sqrt(6). The repository's categorical Cauchy argument
permits only primes 2 and 3 in twist orders. The adapter additionally checks
exactly that the quartic norm of D is a nonzero integer supported on these
primes.

Every possible simple object of the hypothetical center has one of the five
low or sixty-five high restriction vectors in source.json. Its positive
dimension, and every distinguished S-row entry, lies in K. The normalized unit
row is S_0Z=d_Z/D and lies in K pointwise.

Take a cyclotomic automorphism sigma_a with a=1 mod24. It fixes K and i.
The modular Galois row formula sends the unit row to a signed simple row.
Since it fixes the unit row pointwise and S is invertible, its permutation fixes
the vacuum and the vacuum sign is +1. The column formula evaluated in the unit
row, together with positive dimensions, then makes every column sign +1.
Each distinguished row is fixed pointwise; hence the full character evaluation
vector of the restriction column is preserved. The adapter verifies exactly that
all seventy candidate restriction columns have pairwise distinct full character
evaluation vectors. Thus the Galois permutation preserves every restriction
type. The central invertible row lies in K too and shows that it preserves
monodromy charge.

For the canonical anomaly-free modular representation of a center, the
Galois twist formula now reads

    theta_(pi_a(Z)) = theta_Z^(a^2).

Consider a primitive root of order 2^r 3^s. The square image of the subgroup
a=1 mod24 has local sizes

    2^max(r-4,0),       3^max(s-1,0).

Indeed its 2-primary square image is the subgroup 1 mod16, and its
3-primary square image is 1 mod3. The CRT makes their product the root orbit
size. Every root in this orbit must occur with the same nonnegative integer
multiplicity, among actual simple objects of that same restriction type and
charge.

The saturated masks force the twist order to divide 12 or24 except for high
types12 and23. The adapter checks that these are exactly the two types with
both masks zero. In every retained branch each exceptional type has at most
eight actual objects. Consequently an actual root orbit has size at most8,
forcing r<=7 and s<=2. Every actual twist therefore divides

    N = 2^7 * 3^2 = 1152.

This is a proved bound for these inherited branches, not an exploratory order
cutoff. The packet count equations automatically rule out orbits too large for
the available multiplicities, providing the sharper joint bound.

For roots dividing1152, the square subgroup is exactly the units1 mod48.
Its orbit sums consequently lie in Q(zeta48). The adapter independently checks
this in Q[x]/Phi_1152(x), using Phi_1152(x)=Phi_48(x^24). It does not replace an
orbit sum by an averaged relative trace.

## Meaning of phase variables

Every integer phase variable x means multiplicity per actual root. For an
ordinary root orbit O, its count contribution is |O|x and its k-th moment
contribution is x sum_(theta in O) theta^k.

For R928 a packet contains a positive-charge orbit O and its negative-charge
central-semion translate iO. Its cost in the pair-count equation is |O|x.
Its uncharged moment is x(sum O^k + i^k sum O^k), and its charged moment has
a minus sign on the translated part. The two charges remain separate even
when their numerical root sets coincide. The chosen semion twist is i; the
opposite orientation is its complex conjugate and is covered equivalently.

For R941 a positive-charge packet is the set O union(-O), with multiplicity x
per actual root, and costs |O union(-O)|x/2 fermion pairs. This set is deduplicated
when O=-O. Negative-charge packets use single squared-Galois orbits and cost
|O|x individual objects.

The five low objects have twist1. Their five known translates have twists iq
for R928, and -q for R941, where their low charges are (1,1,1,1,-1).
They are fixed contributions. All sixty-five high multiplicities are bound to
the inherited integer pattern or charge allocation. Unknown twist1 objects can
have only types12 and23, as required by the previous dimension block theorem.

## Distinguished and invertible S-row constraints

For a source irreducible E of dimension n_E and formal codegree f_E, the low
object A_E has dimension D/f_E and row scale beta_E=D/(f_E n_E). The adapter
checks these normalizations and distinguished row symmetry exactly.

After division by the two row scales, distinguished STS reads

    sum_Z theta_Z chi_E(FZ) chi_H(FZ)
      = f_H n_H chi_E(F A_H).

After division by beta_E, the forced central invertible G row reads

    sum_Z theta_Z q_Z d_Z chi_E(FZ)
      = D theta_G^(-1) chi_E(g).

In particular chi_E(g)=q_E n_E; there is only one factor n_E in the target.
All coordinates of these complex equations in Q(zeta48) are imposed.

The signed saturated spectral equations are imposed for every exponent of both
conductors12 and24:

    sum_(theta_Z=zeta_f^k) L_f(d_Z)^2
      = 4f [t_f w^-_(f,k) + (1-t_f) w^+_(f,k)],

where L12(a+b sqrt2+c sqrt3+e sqrt6)=3c-a-b and
L24(...)=6e-a-2b. The exact endpoint weights come from
composite_verification.json. The independent parameters0<=t_f<=1 are continuous.
Neither these mixtures nor normalized relative traces are made integer.

## Full cyclic Fourier integrality

The center formula is

    nu_m(V) = D^(-1) sum_Z theta_Z^m d_Z [FZ:V].

The adapter imposes the known first and second indicators. For each m needed
below, it also imposes nu_m(X_i) in Q(zeta_m) by fixed-field equations: its
coordinates already lie in Q(zeta48), so it must be invariant under every unit
u mod48 with u=1 mod gcd(m,48). This puts it in the intersection field
Q(zeta_gcd(m,48)).

For rotation E_n on Hom(1,X_i^n), let g=gcd(n,k), m=n/g. Its k-th power trace is

    Tr(E_n^k) = sigma_(k/g)(nu_m(X_i^g)).

Here X_i^g is expanded using the original source fusion tensor. Its full
decomposition, not just X_i, weights the indicator formula. The automorphism
on Q(zeta48) is any compatible unit u congruent to k/g modulo gcd(m,48).
The preceding invariance equations make that choice independent of extension.

The model embeds the entire expression in Q(zeta_lcm(48,n)). In particular
order9 uses Q(zeta144); a ninth root is never inserted into Q(zeta48).

The Fourier multiplicities are nonnegative integers:

    n*m_j = H + sum_(k=1..n-1) zeta_n^(-jk) Tr(E_n^k),

where H=dim Hom(1,X_i^n) is computed from the source tensor. To avoid large
common integer baselines, write m_j=floor(H/n)+y_j. Then

    n*y_j = H mod n + sum_(k=1..n-1) zeta_n^(-jk) Tr(E_n^k).

Every y_j is a new integer variable, because m_j is an actual eigenspace
dimension. This is a derived integrality statement, unlike integrality of
compressed or averaged trace atoms.

All variable bounds are finite and exact. The center identity
sum_Z d_Z[FZ:V]=D FPdim(V) and unit-modulus twists imply
|nu_m(V)|<=FPdim(V). Hence |Tr(E_n^k)|<=FPdim(X_i)^g.
All FP coefficients are checked nonnegative, and the safe rational upper bound
a+2b+2c+3e is used for a+b sqrt2+c sqrt3+e sqrt6. Thus

    B = ceil((sum_(k=1..n-1) upper^gcd(n,k))/n)+1

bounds |y_j|. Intersecting this with 0<=m_j<=H gives the stored bounds.

Default orders are3,4,6,8,9,12,16. Additional orders up to48 can be selected
with RANK8_FOURIER_ORDERS, for example "3,4,6,8,9,12,16,18,24".
Higher orders are optional strengthening; no claim of categorification follows
from feasibility at any finite collection.

## Exact results and limitations

All model equations are reduced to primitive integer rows; bounds are exact
integers. The two spectral endpoint parameters are the only continuous
variables. The adapter includes no floating point arithmetic.

A solver's numerical infeasibility flag is not a proof. A new exclusion needs
the package engine's exact rational leaf certificates and complete integer
branch coverage. An exact feasible necessary-data model leaves the case open;
it does not provide the missing center S-rows, center fusion rules, pentagon
solution, or a fusion category. A timed-out search likewise leaves the case
unresolved and should be resumed from its saved state.

The independent source tests check the canonical tensor hashes, all seventy
character signatures, dimension/row normalization, prime support, local orbit
sizes, orbit-sum field inclusion, exact coefficient type, finite bounds and the
continuous status of the endpoint mixtures.
