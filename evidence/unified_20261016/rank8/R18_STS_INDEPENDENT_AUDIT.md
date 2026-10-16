# Independent audit: the full relative STS constraint for R8_1_18

Status: the categorical identity and all eight exact source targets pass.
This audit alone is not a nonexistence theorem; the remaining finite
nonnegative-system certificate is owned by the accompanying construction.

Let C be a pseudo-unitary hypothetical categorification, D its dimension,
and normalize the S matrix of Z(C) by S(1,Z)=dim(Z)/D. Write chi for the
eight characters of its commutative Grothendieck ring, f_chi for their
formal codegrees, and A_chi for their actual associated summands of I(1).
Write b_chi for the forgetful vector of A_chi. All A_chi have twist 1.

Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
Example 2.9, the character-level definition before Theorem 2.13, and
Theorem 2.13 identify the actual character labels and give, for EVERY
central simple Z,

    S(A_chi,Z) = chi(F(Z))/f_chi.

This is not a statement only about the low-low S block. It is the
identity of the central character chi composed with the forgetful map.
The primary PDF was independently reopened and read in this audit:
https://arxiv.org/pdf/1309.4822 (printed pages 5--6).

Let Cmat_(chi,i)=chi(X_i), X=diag(1/f_chi) Cmat, and let V have columns
v_Z=F(Z). The displayed identity says S_(low,all)=X V. The center has
trivial anomaly, so its normalized modular identity is
S T S=T^-1 S T^-1. Since every low twist is 1, restricting this identity
to the low rows and columns gives

    X (sum_Z theta_Z v_Z v_Z^t) X^t = S_(low,low) = X B^t,

where B has rows b_chi. Character orthogonality for the commutative
based ring is Cmat conjugate(Cmat)^t=diag(f_chi). Thus
X^-t=conjugate(Cmat), and cancellation gives the full, UNWEIGHTED identity

    sum_Z theta_Z v_Z,i v_Z,j
      = sum_chi b_chi,i conjugate(chi(X_j)).

No factor dim(Z), no assignment of equal-codegree characters, and no
assumption of self-duality of the ring or center have been inserted.
The standard modular relation is valid for this pseudo-unitary center;
unitarity of C is not needed. The general-complex scope follows from
the existing two-FP-dimension Galois pseudo-unitarity theorem.

For R18 put d=2+sqrt(5) and K=Q(sqrt(5)). The character values outside
the FP pair lie in Q(zeta_8), disjoint from K. Normalized trace to K is
therefore ordinary normalized Q(zeta_8)/Q trace on these entries.
In model order (1,a,a^2,a^3,rho,a rho,a^2 rho,a^3 rho), mapped to source
(0,1,7,2,3,6,5,4), the six characters are

    a=zeta_8^(2k), rho=+-zeta_8^k, k=1,2,3.

Each has formal codegree 8, and each nonpointed value has normalized
trace zero. The Galois-FP character has value 4-d on every nonpointed
simple, and its low row is 1+X3+X4+X5+X6. The FP low row is 1.
Consequently the relative STS target is 4-d on the entire nonpointed
four-by-four block. For a or a^-1, only the two k=2 characters have
nonzero rational trace (-1); their low profiles sum to one at every
nonpointed coordinate in each of the eight allowed low frames.
For a^2 the k=2 profiles contribute +1 and the other profiles -2;
the Galois-FP row contributes +1. Thus all remaining nonunit entries
of the relative target vanish.

The independent standard-library verifier reconstructs the immutable
source tensor, verifies all six character homomorphisms and formal
codegrees, independently enumerates all eight reciprocal/dual low
assignments, and checks every one of the 8*49 nonunit target entries.

    python -O evidence/unified_20261016/rank8/verify_r18_sts_target.py --repo .

Conclusion: the proposed normalized relative STS target is correct in
all eight low frames. Any later finite certificate may use it without
an extra categorical hypothesis.
