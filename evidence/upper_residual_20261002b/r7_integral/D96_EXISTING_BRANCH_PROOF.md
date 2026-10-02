# R7_2_113 and R7_2_273: the published dimension-96 branch

The existing proof
`supplements/rank7/papers/D96_GENERAL_EXCLUSION_PROOF.md` applies with
the same hypotheses and scope. It originally certified R7_2_252 and
R7_2_315. It is reproduced unchanged in `D96_PREVIOUS_PROOF.md` to keep
this evidence directory independently readable.

For the two present tensors the dimensions are

\(1^2,2,3^2,6^2\), the universal grading is trivial, and the sign
invertible fixes the dimension-two object and both dimension-six
objects, while exchanging the dimension-three objects. The exact
source verifier checks each of these premises at the actual census
basis indices, rather than assuming an isomorphism to either old
ring.

The old proof forces, successively,

\[
\mathcal C=\mathcal D^{C_2},\quad
\mathcal D:\ 1^3,3^5,
\quad
\mathcal D=(\mathrm{Vec}_{A}^{\omega})^{C_3},\quad |A|=16,
\]

and then combines the steps to

\(\mathcal C=(\mathrm{Vec}_{A}^{\omega})^{S_3}\).
The only possible action orbit pattern on

\(A\) is 
\([1,3,6,6]\). Its order-three automorphism is fixed-point-free;
the transposition has exactly two fixed elements. The elementary
order-sixteen group argument in the existing proof forces

\(A=C_4^2\) or 
\(C_2^4\), and an involution of either group fixes at least four
elements. The contradiction excludes categorification generally.

The current verifier independently repeats the complete involution
enumerations for these two groups. It does not change the scope of
the existing proof.
