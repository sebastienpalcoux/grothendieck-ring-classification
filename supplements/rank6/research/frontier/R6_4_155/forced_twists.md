# Profile 296: the full twist multiset is forced

This is a necessary reduction, not an exclusion or construction. Work in
the pseudo-unitary representative, normalize the central semion g to
θ_g=i, and put B=⟨g⟩′ in Z(C). Write

    d=4+3√2,  D=72+48√2,  b=2+4d=D/4,
    u=ζ₈⁻¹,  w=ζ₃.

The sole frozen profile-296 packet has 16 even and 10 odd simples for the
fermion h. It has dim(B)=D²/2=8b²=144d² and τ(B)=D/(1+i).

## Odd twists

The fermion permutation has trace 16−10=6. The two odd b objects, the two
odd d objects, and the two odd 3d objects have unique charged restriction
columns, so all six are fixed. The four odd 2d objects therefore form two
free h-pairs, with common twists γ,δ. Duality pairs the d objects (twist
α) and the 3d objects (twist β). The b twists are 1,−i.

Even h-pairs cancel in the Gauss sum, giving

    α+9β+4(γ+δ)=−12u.

Hence α+β∈4O. Every Galois conjugate of (α+β)/4 has modulus at most 1/2;
its algebraic norm forces α+β=0. Thus γ+δ=2α−3u. Every conjugate of the
root ξ=α/u satisfies |2ξ−3|≤2, hence Re ξ≥3/4. The mean real part of the
conjugates of a nontrivial root of order n is μ(n)/φ(n)≤1/2. Therefore
α=u, β=−u, and {γ,δ}={uw,uw²}.

## Even twists and analytic indicator forcing

Let A and L be the known low simples of dimensions 1+4d and b. Their
restriction columns are unique and self-dual, so ν₂(A),ν₂(L)∈{1,−1}.
The frozen complete fusion matrices satisfy

    N_A(i,j)=W_i·W_j−δ_ij if charges agree, and 0 otherwise;
    N_L(i,j)=W_i·W_j if charges differ, and 0 otherwise.

Balancing with L forces the even twists of dimensions 1, 1+2d, 1+4d to
be, respectively, {1,−1}, {i,i,−i,−i}, {1,−1}. In particular the
1+2d entries obey S_(L,j)/dim(j)=−2i/θ_j; these are eigenvalues of the
real symmetric N_L, so θ_j=±i. The low semion transports and h-pairs fix
the signs. This uses reality of a symmetric integer matrix, not unitarity.
The remaining even twists have the form

    d: a,−a,a,−a;       2d: c,−c,e,−e.

Put t=a², p=c², q=e², and F=8+2t+4p+4q. Define restriction-weighted
moments E_±=Σ_even W_j dim(j)θ_j^(±2), O_± similarly for odd simples.
Their invertible coordinates, ordered (1,h,g,hg), all equal
b(1,1,−1,−1). Their X,Y coordinates are dF,dF̄ for E_+,E_−, and
−6id,6id for O_+,O_−. The modular second-indicator formula therefore gives

    ν₂(A)=(|F|²+36)/72,
    ν₂(L)=1+i(F−F̄)/12=1−Im(F)/6.

Since |Im F|≤10, the latter cannot be −1, and F is real. The former is
positive, so it equals 1 and F=±6. Since Re F≥−2, F=6. Consequently

    t+2(p+q)=−1.

The algebraic integer (t+1)/2=−(p+q) has all conjugates of modulus at most
1. If nonzero, its norm forces all those moduli to equal 1, hence t=1.
Thus either t=1 with {p,q}={w,w²}, or t=−1 with q=−p.

The original category's fourth indicator is exactly

    ν₄(X)=4+(1+t²+2p²+2q²)/(3√2).

The fourth rotation acts on a 34-dimensional space; its square has trace
ν₂(X²)=ν₂(g)+ν₂(hg)=−2. (Central transport gives ν₂(g)=ν₂(hg)=−1;
X,Y are non-self-dual.) The multiplicities of 1,−1 therefore sum to 16,
and those of i,−i sum to 18. Hence ν₄(X)∈2Z+2Zi. Its distance from 4 is
at most √2, so ν₄(X)=4. The branch t=−1,q=−p would require 2+4p²=0,
impossible for a root of unity p. This leaves

    a=±1,       {c²,e²}={w,w²}.

All signs can be absorbed within h-pairs; no root-order cutoff or search
is used in this argument.

## Forced spectrum and precise limit

| h charge | Dimension | Twist multiset |
|---|---|---|
| even | 1 | 1,−1 |
| even | d | 1,1,−1,−1 |
| even | 2d | w,−w,w²,−w² |
| even | 1+2d | i,i,−i,−i |
| even | 1+4d | 1,−1 |
| odd | d | u,u |
| odd | 2d | uw,uw,uw²,uw² |
| odd | 3d | −u,−u |
| odd | b | 1,−i |

In the frozen W ordering, a representative exponent list modulo 24 is

    12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0.

The rank-52 center spectrum consists of this list and its shift by 6
modulo 24, since Z(C)=Semion⊠B. Therefore any categorification surviving
profile 296 has FSexp(C)=24. The center anomaly is trivial.

`verify_forced_twists.py` checks the moment identities as exact Laurent
polynomial identities over Q(ζ₂₄), the fourth-indicator formula, all
entries of both final low balancing equations, and the Gauss sum. It
uses no optimizer, enumeration, or numerical tolerance. It locates the
release from its ancestors, or accepts `--package PATH`; an optional
`--output PATH` writes its receipt. The default invocation is

    python -O verify_forced_twists.py

These conclusions do not provide the other fusion matrices, full modular
data, associators, or a fusion category. Profile 296 remains unresolved;
its necessary twist spectrum is now unique, up to the indicated labels
and Galois normalization.
