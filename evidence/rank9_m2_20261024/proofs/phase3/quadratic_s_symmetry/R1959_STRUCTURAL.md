# R9_2_1959: the self-dual dimension lattice excludes categorification

Use the independently verified Galois-pseudo-unitarity gate. Suppose C is
pseudo-unitary and put s=sqrt(3). Its dimensions are

    1,2+2s,2+2s,4+2s,4+2s,1,1,1,2,

with D=96+48s. Duality exchanges b_1,b_2 and b_3,b_4 and fixes the rest.
Consequently the coefficient of s in the dimension of every self-dual object
is divisible by four: each nonrational contribution occurs in a dual pair.

The scalar character

    chi=(1,2,2,-2,-2,1,1,1,2)

is dual-invariant and has formal codegree24. The corresponding distinguished
central simple A has dimension D/24=4+2s. As in the general criterion,

    S_(A*,Z)=S_(A,Z*)=dim(A)chi(FZ*)=dim(A)chi(FZ)=S_(A,Z),

so nondegeneracy forces A*=A. Its restriction is therefore self-dual, but
its dimension has s-coefficient2, contradicting divisibility by four.

This proves the pseudo-unitary obstruction, and the signed gate proves that
R9_2_1959 has no complex categorification. No induction Gram bound, indicator,
twist-order enumeration, or LP is required. The second failed character of
codegree8 gives the same contradiction with dimension12+6s, but is unnecessary.

The central-simple/character correspondence is Ostrik's Theorem2.13
(https://arxiv.org/pdf/1309.4822); the S identity is Deshpande's Corollary2.18
(https://arxiv.org/pdf/1611.04486). Exact source character and duality checks
are in `real_character_restrictions.py` and `real_character_results.json`.
