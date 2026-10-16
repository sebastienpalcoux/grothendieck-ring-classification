# Independent audit of the rotational R7_4_2053 obstruction

**Current classification status.** R7_4_2053 is now excluded by [the separately audited R18 endpoint argument](R2053_R18_MORITA_REDUCTION.md). This audit verifies only the earlier rotational-branch obstruction; its original mathematical scope and replay receipt remain unchanged.

Status: **PASS as a necessary-condition refinement only**.
At the stage audited here, the surviving neutral branch was R8_1_18;
that separate endpoint is now excluded as linked above.

I reviewed `R2053_ROTATIONAL_FS_OBSTRUCTION.md` and its verifier, and ran
the verifier independently with optimized Python. The receipt is
`R2053_rotational_fs_independent_O.json`. It checks the source integral
TY(C4) sector, the rotational dihedral cube, and both exact indicator sums.

The pivotal form lemma is valid without a braiding. In a strict pivotal
realization, if f:X->X* has transpose epsilon*f, then the dual of the
word X^n is the reversed word of identical factors. Consequently f^tensor n
is a morphism to precisely that dual word. Dualization reverses the
component morphisms, but all are the same f, so its transpose has sign
epsilon^n. No exchange of distinct factors, and no braiding, is invoked.
On a self-dual simple isotypic summand S^m, nondegeneracy and the
transpose identity induce a multiplicity-space form of sign
epsilon^n/nu_2(S). A skew-symmetric nondegenerate form requires even m.
Thus for odd n and odd m the indicators agree. In particular an odd
unit multiplicity forces epsilon=+1. This is a genuine form-theoretic
restriction in a pivotal category, and the prior Galois-pseudo-unitarity
reduction supplies the required positive spherical structure here.

The source-independent rotational product gives rho^3=P+(1+4P)rho,
P=1+r+r^2+r^3. Both the unit and r^2 occur once, so their indicators
are +1. For the canonical positive pivotal structure on a pointed C4
category, the indicator of r^2 detects the restriction of the H^3(C4)
class to C2. The restriction sends the class k modulo four to k modulo
two, so k is even. Every cyclic subgroup term in the Ng--Schauenburg
group-theoretical exponent formula then divides eight: rotation terms
divide 4*2 and reflection terms divide 2*2.

I also checked the Shimizu sum directly: for either nondegenerate C4
bicharacter, the 64 tuples with a+b+c+d=0 give exponent multiplicities
(8,24,8,24) modulo four. The normalized sum is zero, independently of
the sign of tau. Hence nu_8 of the two-dimensional TY simple is zero,
whereas an exponent dividing eight forces it to equal two. This is
the claimed contradiction for the rotational branch.

The proof does not silently exclude the reflection-support branch:
that branch has no unit in rho^3, so the key indicator consequence is
unavailable. No global classification count should change from this
refinement alone. No gap was found in the argument as scoped.
