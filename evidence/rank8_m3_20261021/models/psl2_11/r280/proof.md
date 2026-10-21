# A general split-module obstruction in dimension 280

**Theorem.** Neither R8_3_1051 nor R8_3_2415 is the Grothendieck ring of a
complex fusion category. No unitarity or weak group-theoreticity is assumed.

Normalize the bases by `[0,3,4,5,6,1,2,7]` and `[0,1,2,3,4,5,7,6]`,
respectively. Both then have dimensions `[1,1,5,5,6,8,8,8]`. Write g for
the nontrivial invertible, X for the first dimension-five object, and
U0,U1,U2,U3 for the four fixed objects of dimensions 6,8,8,8.
The source-bound verifier checks all the following identities exactly:

* g swaps the unit pair and the dimension-five pair, and fixes every Ui;
* X is self-dual;
* its action among the four fixed objects has coefficient matrix

      [[1,1,1,1], [1,0,2,1], [1,2,0,1], [1,1,1,1]];

* its regular matrix is annihilated by `p(t)=t(t-5)(t-1)(t+1)(t+2)`.

Suppose a categorification C existed. The simple U0 fixed by g supplies
a rank-one module category for the pointed subcategory Vec_C2^omega:
its span is preserved by this action. A rank-one module requires omega
to be a coboundary. Thus the regular algebra A=1+g actually exists as a
connected separable algebra object in C. This argument is categorical
and does not impose a unitary associator.

Consider the category M of right A-modules and its left C action.
Each free g-orbit gives one simple A-module. Each fixed Ui gives two
simples Ui,+ and Ui,-, since H²(C2,C*)=0. Their inductions satisfy
`F(Ui)=Ui,+ + Ui,-`. Hence M has two free-orbit simples (dimensions
1 and 5) and four split pairs (dimensions 3,4,4,4).

The action matrix of self-dual X on M is symmetric, by rigidity.
Induction is a module functor, so the block between the i-th and j-th
split pairs has both row and column sums equal to the displayed source
coefficient r_ij. Therefore that block is

    [[u, r_ij-u], [r_ij-u, u]],  with 0 <= u <= r_ij.

The coefficients between a free-orbit simple and the two members of a
split pair are equal: the free module is F(V) for either member V of its
free orbit, and `X F(V)=F(XV)` contains each fixed induction as the sum
of its two summands. Symmetry supplies the reverse equalities.
Consequently the four differences `Ui,+ - Ui,-` form an invariant
subspace for the X-action. On it the symmetric matrix S has entries
`2u-r_ij`. Swapping the signs of each difference is allowed. Gauge the
three nonzero first-row off-diagonal entries to +1. Every possible S is
then exactly of the form

    [[a,1,1,1], [1,0,b,c], [1,b,0,d], [1,c,d,e]],

where a,c,d,e are independently ±1 and b is -2,0,2. There are exactly
48 possibilities; no nonnegative matrix completion has been omitted.

The source regular-matrix identity p(N_X)=0 is the based-ring identity
p(X)=0, since the regular representation is faithful (apply to the
unit). Every C-module action, including this action on M and its
invariant difference space, must therefore satisfy p(S)=0. Exact integer
evaluation rejects all 48 candidate matrices. The certificate records
a nonzero entry of p(S) for each one. This contradiction proves the
theorem for both source tensors.

The fresh recovery verifier independently binds the normalization,
source polynomial and block entries to the two pinned tensor SHA256s,
then evaluates the full degree-five polynomial on all 48 possibilities.
It does not use a Perron-eigenvalue shortcut. The certificate is freshly
regenerated after the workspace reset.

Run `python -O evidence/rank8_m3_20261021/models/psl2_11/r280/verify_split_module.py`.
The default compares the entire certificate; `--write` regenerates it.
