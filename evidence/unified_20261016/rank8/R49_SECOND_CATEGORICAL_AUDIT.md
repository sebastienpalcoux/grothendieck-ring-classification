# Independent audit of the R8_1_49 exclusion

The complete theorem in `rank8/R49_FS_MORITA_PROOF.md` was independently
reviewed against the source profile and the earlier involution-Morita
reduction. Result: PASS for an exclusion over C.

1. The published two-FP-dimension Galois theorem supplies a pseudo-unitary
   categorification if any complex categorification exists. It does not
   assert that the initial category is unitary or pivotal.
2. The pivotal parity argument is valid without a braiding. Pivotal duality
   reverses the tensor word and the morphism factors, but the three factors
   and three copies of the same self-duality morphism coincide. Thus the
   tensor form has transpose sign epsilon cubed. Its restriction to each
   self-dual isotypic block is nondegenerate, and an alternating multiplicity
   form cannot have odd dimension.
3. The source self-dual rho has each of the four invertibles once in its
   cube. The unit first forces its sign positive; then u=3 has positive
   indicator. The two remaining noninvertibles may be mutually dual; the
   proof correctly makes no unnecessary full-self-duality assumption.
4. The positive spherical indicator of the nontrivial object of Vec_C2^omega
   detects its associator class. Consequently 1+u is an actual separable
   algebra. No central lift, braiding, or de-equivariantization is needed.
5. The pointed double-orbit stabilizers have order two, with trivial Schur
   multiplier. They produce four invertibles in the Morita dual. The unique
   free noninvertible double orbit produces one simple of dimension 2d.
   These exhaust the simples. Its square therefore has coefficient 8 on
   the unique noninvertible, since (2d)^2=4+8(2d).
6. The two possible order-four invertible groups give precisely the
   independently excluded near-group terminals (V4,8) and (C4,8).

A fresh optimized execution of the publication verifier completed with
exit status zero. Its complete output is `R49_independent_optimized.json`.
The verifier reopens the census and replays the immutable cyclic terminal;
this audit separately supplies the categorical checks above.

This does not extend to R8_2_412, whose cube multiplicities on the
invertibles are even.
