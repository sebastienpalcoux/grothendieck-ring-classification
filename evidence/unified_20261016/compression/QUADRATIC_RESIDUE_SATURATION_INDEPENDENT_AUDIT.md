# Independent audit of primitive quadratic twist filtering

Status: **PASS as a necessary modular-representation constraint**.
This does not itself change a categorification status.

I checked `QUADRATIC_RESIDUE_SATURATION.md` against the previously
audited conductor-equality lemma. The local signs, including odd local
quadratic characters, and the Chinese-remainder correction are correct.

At local conductor q, use the action convention
S f(p,q')=f(q',-p). For the displayed vectors F and G one has
PSF=G and PSG=chi(-1)F/q. Thus an eigenvector with eigenvalue
lambda=epsilon*tau/q is F+cG with
c=1/lambda=epsilon*chi(-1)*tau. On a q'-unit orbit, S(F+cG), up
to the common factor chi(-q'), is chi(p/q')+c*1_(p=0).
Its Fourier coefficient at a primitive frequency k is
chi(-1)*tau*(chi(k)+epsilon). Hence the support restriction
chi(k)=epsilon holds locally even when chi(-1)=-1 and tau is imaginary.
Non-unit q' cannot give a primitive frequency because its translation
orbit has length strictly smaller than q.

For a global positive fundamental discriminant f, put
C=product_i chi_i(f/f_i). The quadratic Gauss-sum identity is
sqrt(f)=C*product_i tau_i, so the compression eigenvalue
delta/sqrt(f) requires product_i epsilon_i=delta*C. A global
primitive exponent is k=sum_i k_i(f/f_i) mod f; consequently
chi_f(k)=C*product_i chi_i(k_i)=delta. This condition is common to
all eigen-tensor summands and therefore survives their linear combinations.

The relative-trace values also check exactly: the sum of primitive
f-th roots with chi_f(k)=delta is (mu(f)+delta*sqrt(f))/2.
Dividing by phi(f)/2 gives delta*sqrt(f)/phi(f) when mu(f)=0.
This is delta*sqrt(3)/2 for f=12 and delta*sqrt(6)/4 for f=24.

The statement deliberately concerns only primitive f-th twists.
Twists of proper divisor orders are not eliminated by this refinement.
For the three rank-seven Galois-pseudo-unitary cases, whose compressed
quadratic eigenvalue has delta=-1, it restricts primitive twists to
the negative quadratic residue class. Further induction or indicator
constraints would be needed for any classification consequence.
