# A common sphericality and Galois reduction for the two simple rank-eight rings

**Scope.** This proves a structural reduction for R8_2_820 and R8_2_869. This structural argument does not itself construct or exclude either fusion category. Both now have unitary modular constructions, proved separately in `NEARGROUP_CENTRALIZER_PROOF.md`. The reduction to a spherical category uses a short exhaustive exact sign calculation; the subsequent Galois reduction is theoretical and common to both rings.

## Proposition

Every complex fusion category with either of these based rings admits a spherical structure. For any such spherical structure, its dimension character belongs to the Frobenius–Perron Galois orbit. Consequently, either ring is categorifiable over C if and only if it is pseudo-unitarily categorifiable; an arbitrary categorification can be carried to a pseudo-unitary one by Galois conjugation.

The statement does not assert unitarizability, and does not assert that every categorification is itself pseudo-unitary.

## The common ring presentation needed for dimensions

Write the basis as

    1, a_1, a_2, a_3, a_4, b, c_1, c_2.

In source order, b is label2 for R820 and label3 for R869, c_1,c_2 are labels6,7, and the four a labels are the remaining labels1,...,5. Every basis element is self-dual. Both tensors have the identities

    b^2 = 1 + a_1 + a_2 + a_3 + a_4 + b + c_1 + c_2,
    (b+1)a_i = b^2-1,
    (b-1)c_j = b^2-1.                                      (1)

Here the latter two equations are identities in the integral based ring; subtraction is permitted in the Grothendieck group. The verifier checks their full coefficient vectors, not just their dimensions.

## Spherical section

Use the signed sphericalization construction and the positive-second-indicator normalization established in the existing rank-six manuscript and employed throughout the rank-seven and rank-eight signed certificates. In the sphericalization, choose the positive-indicator lift X_i^+ of each self-dual simple X_i. Write the signed quotient coefficients as

    T_ij^k = N_ij^{k,+} - N_ij^{k,-},
    N_ij^{k,+} + N_ij^{k,-} = N_ij^k.

They satisfy the unit, duality, Frobenius symmetry and associativity identities. Since every source simple is self-dual, cyclic symmetry and dual reversal make T_ij^k fully symmetric in i,j,k. Positive-indicator parity gives

    N_jj^i - T_jj^i = 0 mod4.                              (2)

The parity input is the proved odd-channel Frobenius–Schur result, not its older conjectural formulation; see Liu–Palcoux–Ren–Vercleyen, arXiv:2203.06522v5, Theorem3.9, and the signed-sphericalization application in the existing manuscript.

Every nonzero coefficient of either tensor is1 or2. Every coefficient2 has a repeated label. Hence (2) fixes every repeated coefficient1 to+1 and leaves every repeated coefficient2 in{−2,+2}. The remaining, all-distinct, coefficients are1 and have signed possibilities{−1,+1}. Thus every signed coefficient has its original absolute value, and the entire quotient is described by35 Boolean signs for R820 or36 for R869.

`verify_simple_galois_pu.py` reconstructs these domains directly from the source tensor and imposes every associativity equation. Repeated polynomial identities are deduplicated, leaving215 equations for either ring. The equations are exact integer linear combinations of Boolean monomials z_u z_v, reduced using z_u^2=1. A depth-first traversal checks an equation as soon as all its variables are assigned. Both signs are visited at every unforced variable; this is an exhaustive traversal, with no numerical tolerance, heuristic rejection, unverified solver, timeout, or external dependency. It gives exactly one solution for either tensor: every sign is+1.

The replay visits3071 nodes for R820 and1873 nodes for R869. Source tensors are selected from the census by the published lexicographic indexing and checked against their published SHA256 digests. The full unsigned fusion axioms are independently checked before the sign argument.

It follows that T=N. Therefore X_i^+ tensor X_j^+ has only positive lifts as summands, with exactly the original multiplicities. The positive lifts form a full fusion subcategory of the sphericalization, closed under duality. The forgetful tensor functor restricts to an equivalence with the original category. Restricting the spherical structure gives the claimed spherical structure on C.

## Theoretical Galois reduction

Let d be a spherical dimension character and put x=d(b). Simple spherical dimensions are nonzero. Applying d to (1), if x=1 then d(a_i)=0; if x=−1 then d(c_j)=0. Thus x≠±1, and cancellation in (1) gives

    d(a_i)=x−1,     d(c_j)=x+1.

The first identity in (1) now reads

    x^2 = 1+4(x−1)+x+2(x+1) = 7x−1.

Consequently

    x = (7±3sqrt5)/2 = φ^{±4},   φ=(1+sqrt5)/2.

For the positive sign these are exactly the positive FP dimensions. For the negative sign, extend the nontrivial automorphism of Q(sqrt5) to a field of definition of the spherical fusion category. Its Galois conjugate has the positive dimension character. A spherical fusion category with positive simple dimensions is pseudo-unitary. This proves the proposition.

## Replay

    python verify_simple_galois_pu.py --repo /absolute/path/to/repository
    python -O verify_simple_galois_pu.py --repo /absolute/path/to/repository

Both commands use only the Python standard library. `--output PATH` optionally writes the JSON receipt. The accompanying normal and optimized receipts record the same exact mathematical checks.
