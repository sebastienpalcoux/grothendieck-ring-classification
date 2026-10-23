# Independent acceptance audit of R11_1_104

**Accepted:** the supplied group-theoretical data give a unitary realization
of R11_1_104. This audit independently reconstructs every multiplication
coefficient by actual bimodule actions and relative tensor quotients. It does
not import `integral/gt32.py`, use its `kappa` or `extra` functions, or call its
double-coset convolution routine.

The source data are `known_models/jordan_gt_model.json`. The associator
convention is `(X⊗Y)⊗Z → X⊗(Y⊗Z)` with scalar ω(x,y,z). Its stored exponents
are modulo 8; the audit doubles them to use sixteenth roots, also sufficient
for the supplied stabilizer characters. The subgroup is
H={0,8,16,24}, isomorphic to V4, and ψ=1. The audit verifies all group axioms,
normalization, all 32^4=1,048,576 cocycle equations, and all algebra
associativity equations. Thus A=⊕_{h∈H}h is an actual separable algebra in the
unitary pointed category Vec_G^ω. Its category of A-bimodules, with relative
tensor product, is a unitary fusion category of dimension |G|=32.

## Free bimodules directly from the associator

Use F_z=A⊗(z⊗A), with homogeneous basis e_(h,k) of degree hzk. The actions are

    L_a e_(h,k) = ψ(a,h) ω(a,h,zk)^(-1) e_(ah,k),
    R_b e_(h,k) = ω(h,zk,b) ω(z,k,b) ψ(k,b) e_(h,kb).

These follow by reassociating to the adjacent factors of A and multiplying.
The audit checks every action against the three bimodule equations

    L_a L_b|_x = ψ(a,b) ω(a,b,x)^(-1) L_(ab)|_x,
    R_b R_a|_x = ω(x,a,b) ψ(a,b) R_(ab)|_x,
    R_b L_a|_x = ω(a,x,b) L_a R_b|_x.

For a stabilizer a with az=zb, the endomorphism D_a of F_z is determined by
the image L_a R_(b^-1)e_(0,0) of its free generator. On every basis vector it
is extended by D_a e_(h,k)=L_h R_k D_a e_(0,0). The code checks directly that
it commutes with every left and right action.

For each scalar stabilizer label μ, quotient by D_a−μ(a). Every relation
identifies two homogeneous basis vectors up to an exact root of unity.
Connected components with their phase weights give the quotient basis.
The action descends on every relation, not just on the chosen representatives;
all three bimodule equations are checked again. These quotients have
one-dimensional homogeneous fibers and are simple.

The last stabilizer, at z=4, has a noncommutative twisted V4 algebra. This is
checked on the base homogeneous fiber, directly comparing the action of
T_a T_b and T_b T_a on the free generator, with T_a=L_a R_(b^-1).
A four-dimensional semisimple twisted algebra of V4 which is noncommutative
is M_2(C), so it has exactly one irreducible representation of dimension two.
Its regular representation contains two copies of that simple. The audit
retains the whole F_4, hence uses N_10=2M_10 rather than choosing an arbitrary
primitive idempotent. Every other retained module N_i is the simple M_i.

## Completeness and copy multiplicities

The five representatives z=0,1,2,3,4 have pairwise disjoint double cosets
covering all 32 group elements. For each z, the constructed quotient blocks
have total underlying vector-space dimension 16=dim F_z. Since they are
quotients of F_z, distinct, and semisimple, this gives its whole decomposition.
All free bimodules F_z together generate the bimodule category, by the free
bimodule adjunction. This proves the simple inventory is complete.

Independently, all 121 pairwise graded bimodule Hom spaces are computed from
the left/right intertwining equations. Their dimensions are zero off the
diagonal, one for the first ten diagonal entries, and four for F_4. This
confirms distinctness and the copy counts c=(1,1,1,1,1,1,1,1,1,1,2).
The resulting simple dimensions are 1^4,2^7, whose squares sum to 32.

## Relative tensor quotients and fusion multiplicities

For any two retained modules, form the ordinary graded tensor basis and
impose all balancing relations

    (R_h m_x)⊗n_y = ω(x,h,y) m_x⊗L_h n_y.

These are again monomial phase relations. Their complete weighted graphs
produce the exact relative tensor quotient. The induced actions are

    L_a(m_x⊗n_y)=ω(a,x,y)^(-1)(L_a m_x)⊗n_y,
    R_b(m_x⊗n_y)=ω(x,y,b)m_x⊗(R_b n_y).

Every relation and all action axioms are rechecked on each of the 121
products. In particular the quotient has the expected underlying dimension
dim(N_i)dim(N_j)/|H|.

To compute Hom(Q,N_k), use one variable for each homogeneous matrix entry
and impose f L_a=L_a f and f R_b=R_b f. The actions are monomial, so these
linear equations again become a weighted graph. A component with a
nontrivial phase circuit is forced to zero; every other component contributes
exactly one dimension. This computes the full intertwiner space, rather than
sampling characters or relying on the candidate fusion table.

Since N_i=c_i M_i, the desired fusion multiplicity is exactly

    N_ij^k = dim Hom(N_i⊗_A N_j,N_k)/(c_i c_j c_k).

All divisions are exact. All 1331 multiplicities agree with the candidate
tensor and with the input under its explicit based bijection. All 14641
associativity equations are checked as a final consistency test. This is
independent of the discovery implementation, which used double-coset
projective characters and a phase-corrected convolution formula.

## Replay and identity

Run from the workspace root:

    python work/rank11/nonintegral/audit104/verify.py
    python -O work/rank11/nonintegral/audit104/verify.py

Both pass in under one second on the development environment. The verifier
uses only the Python standard library; all critical checks use explicit
exceptions and remain active with optimization. The only data dependencies
are `known_models/jordan_gt_model.json` and the supplied rank-eleven
`tables.txt.gz`. It does not use the exploratory cochain solver or its log.

Input-to-model basis map:

    [0,4,8,5,9,1,2,3,10,6,7].

Canonical input tensor SHA-256:

    0dd2275f9af6f074a7667935309b2535863a8d8d8257d8f82d81efd5860cc346

The exact phase conventions survive this second construction unchanged.
