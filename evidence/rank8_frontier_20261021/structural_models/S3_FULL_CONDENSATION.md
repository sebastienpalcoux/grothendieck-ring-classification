# The conditional full-S3 Morita route for R439 and R567

The previously proved C3-fixed-object argument trivializes the pointed
associator only on C3. It does **not** trivialize the remaining order-two
part of H³(S3,C*). We therefore treat the full-S3 algebra as a conditional
construction branch and preserve the other pointed-cocycle branch.

If the full pointed class is trivial, A=sum(S3) is a connected separable
algebra. Passing from the eight-simple C3 module category to right
A-modules uses the free right reflection U in `c3_morita_dual.json`.
Its four free orbits are the pointed pair f0,f1 and the three pairs
Xi,Y(-i). Quotienting the exact left action gives four module simples.
The source S3 fixes the pointed simple and permutes the other three as
the full symmetric group. Both source noninvertibles act by

\[
\begin{pmatrix}0&1&1&1\\1&2&2&2\\1&2&2&2\\1&2&2&2\end{pmatrix}.
\]

The executable
checks the quotient intertwiner and all source multiplication relations.

The dual A-bimodule category is obtained by left S3-equivariantization
of the right-module category. The fixed pointed simple has stabilizer
S3, with projective representation degrees1,1,2. The noninvertible triple
has stabilizer C2, with two one-dimensional projective characters. Here
H²(S3,C*)=H²(C2,C*)=0. For S3 the vanishing follows also from the
C3-by-C2 Lyndon--Hochschild--Serre calculation: the cyclic second
cohomologies vanish and the mixed H¹(C2,Hom(C3,C*)) term vanishes by
coprimality. Thus the conditional dual has rank five and dimensions
1,1,2,d,d, where d=3+2sqrt(3). Each noninvertible equivariant simple has
underlying object 3(X+Y), so division by FPdim(A)=6 gives d.

Write the dual basis as 1,s,V,P,Q. The first three objects form Rep(S3).
The sign representation interchanges P,Q, and V sends either to P+Q,
by restriction of representations to the C2 stabilizer. Hence

`s²=1`, `sV=V`, `V²=1+s+V`, `sP=Q`, `VP=VQ=P+Q`.

These rules hold on both sides directly by rigidity. The set {P,Q} is
dual-stable. Dualizing sP=Q and sQ=P shows that right multiplication by
s also swaps P,Q. Dualizing VP=VQ=P+Q gives the identical right V
action. Since Q=sP=Ps, P and Q commute. Thus the full rank-five
tensor is commutative here, rather than being assumed commutative from
its dimension profile.

Rigidity determines the integral part of PP* to be 1+V. There are only
two duality possibilities for P,Q. Their remaining self-product
coefficients a,b satisfy a+b=6 by the exact FP dimension equation.
Exhausting a=0,...,6 and both dualities, and checking every reciprocity
and associativity equation, leaves eight labelled tensors: all seven
self-dual choices and the dual-pair choice a=b=3. Interchanging P,Q
reduces this to **five based-ring possibilities**.

One of these five tensors, the self-dual a=b=3 case, agrees in all125
coefficients with the repository's known Izumi C3+6 inversion
equivariantization. This is **only a possible dual based ring**. It does
not identify the category with that known construction, prove centrality
of its Rep(C2), or yield a model of R439/R567. The four-simple module
actions are not faithful on the five-dimensional dual algebra, and do not
resolve the remaining coefficients or categorical coherence. The other
four tensors were subsequently matched in all125 coefficients to the
frozen rank-five census and their exact general-complex exclusion proofs
freshly replayed by `rank5_route_bindings.py`, in normal and optimized
Python. They are R5_6_271, R5_5_173, R5_4_82 and R5_3_81. Thus only
the self-dual a=b=3 based ring R5_3_40 remains in this conditional branch.
This uses complete source tensors and checked proofs, not catalog labels.
The known equivariantization category itself is impossible as the dual:
it has a central Rep(C2), whereas the source439/567 has no nontrivial
invertible object in its Drinfeld center, as proved in
`KNOWN_MODEL_ROUTES.md`. Possible other associators on R5_3_40 remain open.

The categorical inputs are subgroup algebras and dual module categories
(EGNO, Chapter7), and the projective-stabilizer orbit description in
Burciu--Natale, arXiv1206.6625, Corollary2.13. The known model comes from
Izumi1512.04288, Example13.10, as documented in the frozen rank-five
model package. No new hypothesis is silently imposed on the original
general-complex categorification question.

Canonical read-only replay, after the C3 module verifier:

```sh
python evidence/rank8_frontier_20261021/structural_models/s3_full_condensation.py
python -O evidence/rank8_frontier_20261021/structural_models/s3_full_condensation.py
```
