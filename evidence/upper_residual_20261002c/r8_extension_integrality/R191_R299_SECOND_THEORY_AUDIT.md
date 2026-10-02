# Second theory audit: R191/R299

Status: APPROVED for a general complex exclusion, subject to the source checker premises.
Auditor: restore_r8_nonintegral, independent of the proof author.

I read the complete proposed proof and independently opened Galindo,
*Clifford theory for graded fusion categories*, arXiv:1010.5283v3,
Theorem 1.3, Proposition 5.3, and the proof of Theorem 1.3 on page 19.

The theorem uses the dual of the **induced** module L = D tensor_B N.
It does not identify the dual of the original two-object odd module M
as pointed. The present proof makes this distinction correctly. The
actual D action on M supplies a coherent extension of N, while its
transitive V4 restriction is indecomposable. Therefore every hypothesis
of Theorem 1.3 is satisfied. Proposition 5.3 identifies the neutral
dual as B*_N. The subgroup decomposition V4 = H times K gives
B*_N = Rep(H) tensor Vec_K = Vec_V4 with trivial associator.

The C3 graded bimodule class of D is nontrivial: its nonneutral component
has rank one as a left Vec_V4 module, unlike the rank-four regular
component. Hence its order is three. Morita conjugation preserves that
order. In the semidirect neutral model, a tensor autoequivalence class
of order three cannot lie in the cohomological kernel H^2(V4,C*) = C2.
The induced permutation of V4 consequently has order three. The
pointed Morita group is V4 semidirect C3 = A4.

The square-kernel extension-integrality criterion was checked separately
against Gelaki--Naidu arXiv:0709.4326 Theorems 4.1 and 5.1, and ENO
arXiv:0909.3140 Corollary 3.13 and Theorem 1.3. Its twisted pointed
module identity block is ordinary Rep(N), so the argument covers every
omega. The normal abelian subgroups of A4 are 1 and V4, both square
order. Thus every extension of a neutral model compatible with the
source odd module is integral. The source odd dimension sqrt(6)
contradicts this. No pivotal, spherical or unitary hypothesis enters.

No mathematical gap was found. The original neutral ring alone is not
asserted to have only group-theoretical categorifications; the coherent
odd module is essential to this argument.
