# Independent review of the R1154 semionic packet theorem

**Verdict: accepted within its stated conditional scope.** All four packet
fusion matrices are necessary in any surviving center, and are forced by
the existing restriction matrix. Their existence as nonnegative integer
matrices proves neither a modular category nor a source categorification.
The reviewer is a separate automated mathematical agent, not an
independent human reviewer.

Reviewed `../../r1154/PROOF.md`, `verify_semionic_packet.py`, the frozen
upstream reconstruction `rank8_next_20261021/r1154/low_action_bounds.py`,
and the producer replay. The replay passes on all 25 pair histograms.

## The spectral projector and invariant spaces

The projector polynomial has value one at -1: its numerator there is
`(-1)(-4)(4)(496)=7936`. An additional independent replay verifies
`(N2+I)P=0`, `P^2=P`, and `trace(P)=4` on every surviving histogram. Thus
P is the full -1 eigenspace projector, without needing a numerical
diagonalization or an assumed characteristic polynomial. The frozen
character table independently identifies its four spectral labels as
precisely the packet labels.

With symmetric unitary s, Verlinde gives `P=s Q s*`. All four vacuum
entries are 1/4, so `Pe0=(su)/2`; the explicit projector instead gives
`Pe0=w/2`. Hence `su=w`. The orthogonal complement of u in the packet
coordinate subspace maps to the orthogonal complement of w in im(P),
which is precisely W. Self-duality of I(g) gives `sw=s^2u=Cu=u`.
Applying `sTs=T^-1 s T^-1` to w then gives `sv=-v`, with the signs in the
proof correct. Consequently its orthogonal complement E in W is
s-invariant. E is also T-invariant.

## Exhaustiveness of the residual two-dimensional case split

Write `A=[[a,b],[b,c]]` and `T=diag(i,-i)`. Its off-diagonal STS equation
is `i b(a-c)=b`. Since A commutes with A squared, unequal duality signs
force b=0. In that case the nonzero diagonal entries are uniquely
`a=i,c=-i`, and both duality signs are negative.

For b nonzero, equal duality signs give `a+c=0` and `a-c=-i`. Thus
`a=-i/2,c=i/2` and `b^2=epsilon+1/4`. When epsilon is positive, the first
row has squared norm 3/2, violating unitarity. When it is negative,
`b=+/- i sqrt(3)/2`. This proves that the displayed three possibilities
are exhaustive, rather than merely examples of solutions. In particular
both same-twist pairs must be dual pairs.

The full four s-columns are determined because each packet basis vector
is u/2 plus a vector in W, and sW=W. The difference of the first two
fusion matrices has no eigenvalue outside the packet: symmetry of s
makes their rows coincide there. Within the packet the denominator is
1/4. Thus the claimed `V diag(4(B0j-B1j)) V*` is exact. Its irrational
off-diagonal entry excludes both mixed residual solutions.

## Projection formula and reconstruction conventions

For the tensor forgetful functor F and its adjoint I, the projection
formula is `I(g) tensor Z = I(g tensor F(Z))`. Therefore the multiplicity
of W equals the inner product of `g tensor F(Z)` with `F(W)`. With
source-by-center restriction matrix M this is exactly `M^t N_g M` in
the chosen convention. Here g is self-dual of order two, so its action
matrix is symmetric and the row/column transpose convention introduces
no ambiguity. No commutativity of the source fusion ring is required.

The independent replay reconstructs every entry directly as

    sum_{j,k} M[j,Z] R[g][j][k] M[k,W],

without using the producer's matrix multiplication formula, and verifies
it equals the sum of the four saved packet matrices on all 25 domains.
Its vacuum row is the four-object packet, fixing the convention.

Finally H is the difference of the two same-twist pair sums. Its
eigenvalues on the four packet spectral labels are `(-4,-4,4,4)` and
vanish elsewhere. Solving these four linear equations gives the four
displayed reconstructions. The producer checks their integer
nonnegativity, unit rows, transpose dualities and commutativity. These
are necessary data only, exactly as the theorem states.

Additional exact checks and source hashes are saved in
`verify_r1154_packet.py` and `r1154_packet_verification.json`.
