# A central dimension-parity obstruction for the exotic dimension-504 ring

**Theorem.** The fusion ring `R9_2_941` admits no fusion categorification over
`C`. This conclusion uses no unitarity assumption. The ring is exactly the
rank-nine, dimension-504 ring in Alekseyev–Bruns–Dong–Palcoux,
arXiv:2507.07023v2, §1.5, Question 1.14; the previously verified tensor
isomorphism is recalled below.

## 1. Notation and categorical input

Use source labels `X0=1`, `Y=X2`, `B1=X1`, `B2=X3`, `B3=X4`, `B4=X5`,
and `C1=X6`, `C2=X7`, `C3=X8`. Their dimensions are respectively
`1,8,7,7,7,7,9,9,9`, and total dimension is `D=504`.
Suppose a categorification C exists. Since C is integral, it has the
canonical positive spherical structure. Its center Z(C) is an integral
modular category of dimension `D^2`. Write F for forgetful functor and I
for its right adjoint. For a central simple Z write

`F(Z) = t*1 + a*Y + sum_j b_j*B_j + sum_l c_l*C_l`,

and let `z=dim(Z)`, `b=sum_j b_j`, `c=sum_l c_l`.
Thus `z=t+8a+7b+9c`.

The following standard facts will be used:

1. `z | D`, because modular square-divisibility makes `D^2/z^2` an
   integer, and `D,z` are positive integers.
2. Since K0(C) is commutative, I(1) is multiplicity-free. Its central
   simples A_chi are indexed by the nine scalar characters, with
   `dim(A_chi)=D/f_chi`. Thus `t` is zero or one. The central dimensions
   in I(1), with multiplicity, are `1,63,56,56,56,56,72,72,72`.
3. If chi is a scalar character, the central character identity gives
   `S_(A_chi,Z)=dim(A_chi)*chi(F(Z))`. By symmetry of S and the Verlinde
   character formula, `dim(A_chi)*chi(F(Z))/z` is an algebraic integer.
4. Set `G=sum_i N_i N_i^T`. The induction Gram identity gives
   `G=sum_Z v_Z v_Z^T`, where v_Z is the restriction column. Consequently
   `v_Z^T G^(-1) v_Z <=1`. Orthogonality of the real scalar characters gives

   `v_Z^T G^(-1) v_Z = sum_chi chi(F(Z))^2/f_chi^2 <=1`.       (1)

   This is an ordinary positive semidefinite matrix identity and requires
   no C*-structure on C.
5. Frobenius reciprocity and dimensions give

   `sum_Z z*[F(Z):X] = dim(I(X)) = D*dim(X)`.                 (2)

For the identity in item 3, see Deshpande, arXiv:1611.04486, Proposition
2.8 and §2.7, especially (36) and the description immediately preceding
it. For item 2 see Ostrik, arXiv:1309.4822, Theorem 2.13.

## 2. Exact character data

The dimension character has formal codegree 504. One rational character
of codegree 8 is

`chi_8(F(Z)) = t-b+c`.

Four rational characters of codegree 9 are

`chi_9,j(F(Z)) = t+b-a-3*b_j`       (`1<=j<=4`).

The other three characters have codegree 7. Put
`alpha=2*cos(2*pi/7)`, `beta=alpha^2-2`, `gamma=1-alpha-alpha^2`.
These are the roots of `x^3+x^2-2x-1`; in a cyclic ordering the three
characters are

`chi_7(F(Z)) = t+a+c1*alpha+c2*beta+c3*gamma`,

and its two Galois conjugates. In particular
`alpha+beta+gamma=-1`, `alpha^2+beta^2+gamma^2=5`.
The appropriate cyclic ordering is verified against every source product
in the accompanying verifier; permuting the C labels has no effect on the
argument.

We use the standard integral basis
`O_(Q(alpha))=Z[alpha]`, with basis `1,alpha,alpha^2`.
For example see G. Eric Moorhouse, *Cyclotomic Fields with Applications*,
Theorem 4.8. The accompanying verifier instead tests characteristic
polynomials over Q, so its arithmetic check does not assume an integral
basis theorem.

## 3. Only two restrictions can have central dimension 63

**Lemma.** If a central simple has dimension 63, its restriction is one
of

`U = Y+B1+B2+B3+B4+C1+C2+C3`,

`V = 1+Y+2*C1+2*C2+2*C3`.

**Proof.** Item 3 applied to the codegree-9 characters gives

`t+b-a-3*b_j == 0 (mod 9)` for every j.                       (3)

Applied to any codegree-7 character it says `(8/7)*chi_7(F(Z))`
is integral. In the integral basis above this forces

`c1 == c2 == c3 == t+a (mod 7)`.                             (4)

The dimension identity is

`t+8a+7b+9c=63`, with `t in {0,1}`.                          (5)

For completeness, here is the entire short reduction of (3)–(5).
Write `r` for the residue of `t+a` in `{0,...,6}`. Since each c_l is
nonnegative and congruent to r, the inequality `t+8a+27r<=63` leaves
only the following aggregate possibilities:

| t | a | b | c | Consequence |
|---:|---:|---:|---:|---|
| 0 | 0 | 9 | 0 | Every b_j is a multiple of 3 |
| 0 | 0 | 0 | 7 | Exactly one c_l is 7 |
| 0 | 1 | 4 | 3 | Every b_j=1 and every c_l=1: U |
| 0 | 7 | 1 | 0 | (3) requires every b_j>=1: impossible |
| 1 | 0 | 5 | 3 | (3) requires every b_j>=2: impossible |
| 1 | 1 | 0 | 6 | Every b_j=0 and every c_l=2: V |
| 1 | 6 | 2 | 0 | (3) requires every b_j>=2: impossible |

In the first row `chi_8(F(Z))=-9`, so its single contribution to
(1) is `81/64>1`. In the second row the three codegree-7 contributions
to (1) sum to `alpha^2+beta^2+gamma^2=5>1`. Both are impossible.
Only U and V remain. QED.

## 4. Two dimension parities force prime-power central simples

The only possible odd central dimensions are the odd divisors of 504:
`1,3,7,9,21,63`.
Dimension 3 is impossible. Dimension 1 is the unit. At dimensions 7,9,21,
the restrictions are respectively a B_j, a C_l, or a sum of three B_j's;
indeed any occurrence of 1 would put the object in I(1), whose dimension
list has none of 7,9,21. At dimension 63 the preceding lemma applies.

Exactly one central simple has restriction V: it is the unique
63-dimensional summand of I(1). Let m be the number of central simples
with restriction U. Apply (2) to Y and reduce modulo 2. Even-dimensional
central objects contribute zero. Among odd-dimensional central objects,
only the unique V and the m copies of U contain Y, each with multiplicity
one. Therefore

`0 == 504*8 == 1+m (mod 2)`;

hence m is odd.

For each l let n_l be the number of central simples restricting to C_l.
Apply (2) to C_l and again reduce modulo 2. The unique V contributes
`63*2`, the U columns contribute `63*m`, and the dimension-9 columns
contribute `9*n_l`. All other contributions are even or zero. Thus

`0 == 504*9 == m+n_l (mod 2)`.

Consequently **every n_l is odd**. In particular, Z(C) contains a simple
of dimension `9=3^2`.

## 5. Contradiction and scope

The source ring is simple and has no braided categorification. The
latter follows by the standard simple braided dichotomy: a nondegenerate
realization would require `7^2 | 504`, while a symmetric realization would
be a finite-group representation ring, which this exotic ring is not.
These ring and braided facts were established in phase4 and in the
published source identifying this ring.

Liu–Palcoux–Ren, arXiv:2102.01663v4, Theorem 5.1, states that the center
of a nonpointed simple complex fusion category is simple exactly when
the category does not admit a braiding. Hence Z(C) is simple.
But Etingof–Nikshych–Ostrik, arXiv:0809.3031, Corollary 7.2, states that
an integral nondegenerate braided category containing a nontrivial
prime-power-dimensional simple contains a nontrivial symmetric
subcategory. Such a subcategory is proper in the nondegenerate Z(C),
contradicting simplicity. This proves the theorem.

The argument applies to arbitrary complex fusion categories because
integrality supplies the positive spherical structure. It never replaces
pseudo-unitarity by unitarity. No associator or indicator classification
is assumed.

## 6. Reproducible arithmetic and provenance

`verify_odd_columns.py` uses Python's standard library and exact rational
arithmetic only. It regenerates the character relations and G from the
original tensor, exhaustively checks all 1,612 bounded dimension-63
vectors, and recovers exactly U and V. It also verifies the complete odd
dimension list and an equivalent 15-entry Gram parity certificate, whose
right side is 937. It does not use an optimizer or the exploratory
candidate list. Output: `odd_columns_verified.json`.

The proof in §3 replaces that finite enumeration with two congruences
and the displayed seven-row argument. The enumeration is an independent
arithmetic cross-check, not the reason to believe the congruences.

The source tensor SHA256 is
`1699b4d0768bbdf652993c18237cffd6df806d0e3d9c325403fcebcea58e2c02`.
The source-to-published basis permutation is `[0,1,5,2,3,4,8,6,7]`, checked
in all 729 coefficients by phase3/audit_models/published_504_tensor.json.

Exploratory files `simple_center.py`, `full_center.py`, and
`integer_gram.py` discovered the obstruction. Their floating-point
optimization output is not used in the proof. The exact Z3 result agrees
but is likewise unnecessary for verification.

Primary sources:

- <https://arxiv.org/pdf/2507.07023v2>, §§1.5,7.5 and Question 1.14.
- <https://arxiv.org/pdf/1309.4822>, Theorem 2.13.
- <https://arxiv.org/pdf/1611.04486>, Proposition 2.8 and §2.7.
- <https://arxiv.org/pdf/2102.01663>, Theorem 5.1.
- <https://arxiv.org/pdf/0809.3031>, Corollary 7.2.
- <https://ericmoorhouse.org/handouts/cyclotomic_fields.pdf>, Theorem 4.8.

## 7. General reusable form of the criterion

Let R be a nonpointed simple integral commutative fusion ring of even
FP-dimension D which has no braided categorification. For any hypothetical
categorification, form the possible restrictions of odd-dimensional central
simples using `z | D`, distinguished formal-codegree dimensions, and the
algebraic integrality of `(D/f_chi)*chi(v)/z`. The distinguished restrictions
with `v_0=1` occur with their prescribed integral multiplicities. The
remaining restrictions with `v_0=0` must satisfy the parity equations

`sum_(z odd) v_Z = 0` in `(Z/2)^rank`,

because `sum_Z z*v_Z = D*d` and D is even. A parity certificate forcing a
nontrivial prime-power central dimension excludes R: the center is simple,
whereas ENO's prime-power theorem supplies a proper symmetric subcategory.
This formulation does not require solving complete induction matrices.
For R9_2_941 only the four coordinates Y,C1,C2,C3 matter; the odd-column
lemma reduces the certificate to two one-line parity deductions.
