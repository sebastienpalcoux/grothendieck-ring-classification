# Independent replay of the R3895 conditional probing certificates

This note concerns the final finite conditional systems for `R7_5_3895`.
It does not, by itself, assert that every conditional system has been excluded.
The whole-ring conclusion additionally requires the complete source, signed
quotient, low-frame, character-label, phase, and cyclic-character reductions
and the successful replay of every remaining conditional branch.

The independent verifier is `verify_r3895_probing.py`. It uses only the Python
standard library and does not import the numerical search, its branch-matrix
builder, or its domain-pruning helpers. Its public `verify(case, phi, r, s)`
function is read-only. Normal and optimized-Python receipts are audit outputs,
not premises of the proof.

## Source-derived branch matrix

The verifier pins the canonical tensor with SHA-256
`590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0`.
It recomputes the induction Gram matrix directly from the structure constants:

\[
B_{ih}=\sum_{k,j}N_{ki}^{j}N_{kh}^{j}.
\]

The complete frozen C8 system is a separate, source-regenerated input. From
that input the independent verifier reconstructs the conditional matrix as
follows.

1. It identifies each old saturated conductor-five orbit by its complete
   restriction-row tuple, rather than by an assumed unchanged orbit index.
   It transfers actual object multiplicities, checks divisibility by each C8
   packet size, and requires a unique complete saturated phase for every
   affected orbit.
2. It subtracts the selected low rows and the fixed saturated packets from
   the Gram matrix. If one copy of an integer packet already leaves a
   negative entry or a matrix that is not positive semidefinite, its
   nonnegative integer multiplicity is necessarily zero. These removals are
   recomputed using exact rational Schur complements.
3. It fixes the selected cyclic-four character for source object 1. The
   complete multiplicity tuple is
   \((r,9-r,s,2-s)\), with \(0\leq r\leq9\),
   \(0\leq s\leq2\), all entries integral. Completeness of the earlier
   exclusion of the other choices is checked by the whole-chain verifier.
4. It recomputes every orbit capacity directly, as explained below.
5. It compares the entire resulting integer matrix and right-hand side
   against the certificate hash. It also checks every pinned source-input
   hash in the certificate.

No optimizer status contributes to this reconstruction.

## Necessary orbit capacities

Write \(R\) for the residual restriction Gram matrix after the fixed packets
have been subtracted, and \(H_o=\sum_{v\in o}vv^t\) for an orbit Gram
matrix. If the remaining packet variables for orbit \(o\) are \(x_j\)
with positive integral packet sizes \(u_j\), then its actual multiplicity is

\[
t_o=\sum_j u_jx_j.
\]

Every remaining orbit contributes a matrix with nonnegative entries that is
positive semidefinite. Consequently \(R-t_oH_o\) must have both properties.
For each entry with \((H_o)_{ij}>0\), this gives the finite bound
\(t_o\leq\lfloor R_{ij}/(H_o)_{ij}\rfloor\). The verifier scans every
integer up to the smallest such bound and checks positive semidefiniteness
exactly. It additionally checks that the admissible values form an initial
interval. Let its maximum be \(M_o\).

Since \(t_o\) is a multiple of \(g_o=\gcd_j u_j\), the necessary capacity is

\[
t_o\leq g_o\left\lfloor M_o/g_o\right\rfloor.
\]

It is encoded with a nonnegative integer slack. No assertion that this bound
is sufficient, or that every multiple below it is attainable, is required.

## Complete exact probing chain

All variables of the conditional matrix are nonnegative integers. A split
at an integer \(k\) is the exhaustive disjoint alternative
\(x_j\leq k\) or \(x_j\geq k+1\). The verifier rejects a split that is
not nontrivial within the previously retained bounds.

Each certificate step supplies an exact integer Farkas covector for one side.
Lower and upper bounds are represented respectively by
\(x_j-s=\ell\) and \(x_j+s=u\), with \(s\geq0\). The verifier checks
every original column and every bound-slack column: the covector must be
nonnegative on all columns and strictly negative on the right-hand side.
This proves that the discarded side has no nonnegative real solution and,
in particular, no nonnegative integer solution. The other side is retained.

The final covector must exclude the entire remaining side. Therefore a chain
of \(m\) discarded sides and one final contradiction is an exhaustive
finite integer tree with \(m+1\) exact leaves. The recorded final bounds
must equal those reconstructed from all the splits. When a separately
expanded tree is present and `check_tree=True` (the standalone default), the
verifier also checks that it is exactly the tree represented by the chain.
The whole-chain replay and the aggregate `verify_r3895_all_probing.py` use
`check_tree=False`: the chain itself is the complete finite proof, and a
later optional expanded-tree file must not change the frozen proof inputs.

The verifier expressly requires `complete_conditional_exclusion` and a
terminal covector. A partial checkpoint, a numerical infeasibility report,
or a successful replay of only the currently stored necessary bounds cannot
pass this gate.

## Whole-chain boundary

The final `verify_r3895_cyclic_chain.py` wrapper is responsible for regenerating
the original C8 systems, validating their mathematical hypotheses and
integral auxiliary variables (including the frozen norm-slack parity
identity), establishing the complete remaining branch list, and calling this
independent verifier on every member of that list. The probing replay adds
no pivotality assumption and makes no positive-characteristic claim.
