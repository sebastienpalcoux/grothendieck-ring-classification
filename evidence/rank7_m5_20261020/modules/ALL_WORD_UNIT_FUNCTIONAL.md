# Finite all-word unit-functional integrality

This is a necessary condition on a complete proposed center restriction domain.
It neither constructs a fusion ring nor proves monomial nonnegativity.

## Spectral formula and finite order

Let C be a pseudo-unitary fusion category, let D=FPdim(C), and let A_E be
the simple summand of I(1) indexed by an irreducible source character E.
For the present commutative source rings all such characters have degree one.
Write f_E for its formal codegree. If a simple Y of Z(C) has restriction row
v_Y and dimension z_Y, the central fusion eigenvalue of A_E at Y is

    lambda_E(Y) = D chi_E(v_Y)/(f_E z_Y).

It is an algebraic integer. The coefficient of the tensor unit in any
integer polynomial P in these commuting low simple classes is

    tau(P) = sum_Y z_Y^2/D^2 P(lambda_E(Y)).

This follows from the simultaneous modular diagonalization of the center
fusion matrices: the unit weight of the column Y is S_(0,Y)^2=z_Y^2/D^2.
Consequently tau(P) is an integer for every integer polynomial. For each
monomial it is a nonnegative integer. An arbitrary integer linear
combination of monomials may have negative unit coefficient.

Fix finitely many possible spectral points containing the complete candidate
domain. Choose a common number field K containing all the eigenvalues and
put A=product_points O_K. The tuples lambda_E lie in A. The ring
B=Z[1,lambda_E] is a subgroup of the finitely generated free abelian group
A, and hence is finitely generated as an additive group. Equivalently,
start with the additive span of 1 and all lambda_E, repeatedly multiply
its basis by the generators and take the integral span. This ascending
chain stabilizes. At stabilization it is exactly B. Checking tau on any
additive basis then checks the integrality of every word, in every degree.
There is no guessed maximum word length.

This argument allows a domain larger than the eventual support. It gives
linear congruences in the multiplicity of each possible row orbit. Missing
possible rows would invalidate an exclusion based on that domain; it would
still be a valid check of the particular proposed support.

## Exact modular shortcut for these two source rings

Put phi=(1+sqrt(5))/2. The fields and integer bases are

* R7_5_3895: K=Q(sqrt(5)), O_K=Z[phi], d=2;
* R7_5_5039: K=Q(sqrt(5),sqrt(-2)), O_K=Z[phi,j], j^2=-2, d=4.

For the second statement, the quadratic discriminants 5 and -8 are
coprime. The product basis discriminant is 5^2*8^2=1600, equal to the
biquadratic field discriminant 5*(-8)*(-40). Thus this product basis is
indeed integral and maximal. Multiplication uses phi^2=phi+1 and j^2=-2.

In both cases D=80*(9+4sqrt(5))=80*(5+8phi), and 5+8phi is a unit with
inverse 13-8phi. Therefore

    W_Y = 6400*z_Y^2/D^2 = z_Y^2*(233-144phi)

lies in O_K. Set M=6400*d and use the rational functional

    rho(h) = [sum_Y Tr_(K/Q)(W_Y h_Y)]/M.

For a genuine integer word, each complete weighted spectral orbit is
Galois-invariant, so tau(P) is rational and rho(P)=tau(P). The implementation
checks this invariant explicitly: it applies phi -> 1-phi, and also
j -> -j in degree four, to the entire multiset of pairs (eigenvalue tuple,
scaled weight), for the low bundle and for every individual high orbit.
This check does not assume that the signed linear transport T sends every
row to a nonnegative row. It directly checks the resulting actual row
orbits, so the possibility of actual transport -T(v) is retained.

For every integer multiplicity vector, rho(M A) is integral. Consequently

    tau(B) subset Z  iff  rho(B+M A) subset Z.

It is enough to compute the finite-index full-rank lattice L=B+M A. Start
with M A, 1, and the lambda_E, and repeatedly close under multiplication by
the lambda_E. This is an increasing chain of subgroups of the finite
abelian group A/M A and must stabilize. Equality of two successive exact
row Hermite normal forms proves closure. The computation uses all source
characters, including the one whose central eigenvalue is identically 1.
Duplicate eigenvalue signatures may be compressed because every word is
constant on those coordinates; the trace weight retains each occurrence.

Apply rho to an additive HNF basis h of L. For a high row orbit o define

    a_h,o = sum_(Y in o) Tr(W_Y h_Y) mod M,
    b_h   = sum_(Y in fixed low bundle) Tr(W_Y h_Y) mod M.

The resulting necessary and sufficient all-word integrality conditions on
this domain are

    b_h + sum_o a_h,o*n_o = 0 mod M,

where n_o is the actual multiplicity per row, summed over its phase
packets. A second HNF reduces this finite family of congruences. These
constraints have integer slacks of either sign. They must not be imposed
with a nonnegative slack merely because monomial unit coefficients are
nonnegative.

## Implementation and exact checks

`all_word_order.py` verifies each complete source character and formal
codegree directly against the raw rank-seven tensor, computes the spectral
eigenvalues in the displayed integer basis, requires their integrality,
and checks the weighted Galois invariance just described. It then computes
bounded exact modular row HNF by Bezout insertion; the integer bound is
checked before vectorized int64 arithmetic. No Python assertions are used.
The replay verifier checks against FLINT HNF on 560 deterministic
pseudorandom matrices of sizes 1 through 14 and moduli 8,25,80,12800 (seed20261020). The core
algorithm is elementary: maintain a triangular basis containing M Z^n;
insert a row by the extended Euclidean algorithm at each pivot. Reductions
modulo M use the untouched later ambient sublattice. Finally reduce above
each pivot from left to right. Each operation preserves the lattice.

The JSON receipt records the tensor and domain hashes, every closure index
and lattice hash, whether stabilization occurred, all reduced congruences,
and exact checks of the supplied necessary-data witnesses. A PARTIAL
receipt contains valid necessary congruences but does not certify all-word
closure. A STABILIZED receipt does.

## Positivity and limitations

Monomial nonnegativity is additional. A general HNF basis element is an
integer polynomial with possibly negative coefficients, so its tau need
not be nonnegative. For a polynomial P, positivity of tau(P P*) follows
already from positive spectral weights, and by itself adds no new test to
valid complex spectral data. Integrality of these norms and mixed Gram
entries is included in all-word closure. An embedding of the resulting
integral trace lattice into the free lattice of simple central objects,
with nonnegative multiplication and prescribed low basis vectors, would
be strictly stronger. Passing the current criterion does not establish
such an embedding or coherent associators.

The latest R3895 fixture stabilizes in nine rounds, giving 75 reduced
congruences on 145 high orbits. Its current witness passes every one, and
therefore passes every low-word unit-integrality condition. The two R5039
fixtures use the same 76-orbit domain and stabilize in eleven rounds,
giving 31 reduced congruences; their current witnesses likewise pass.
These are limits of this obstruction, not categorification claims.
