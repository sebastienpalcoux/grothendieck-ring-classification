# Independent audit of the inversion construction of R7_4_2665

Status: **PASS**, subject to the explicitly cited, already established unitary
NG(C16,16) existence input. This audit checks the categorical construction and
the source identification independently of the construction author. It is not
an inference of existence from the based-ring computation alone.

## 1. Parent self-Morita equivalence and descent

I checked Izumi's fixed-point formulas in Theorem 11.3 against the proposed
regular-C16 Morita bimodule. The right action is
`alpha'_g = Ad U(-g)` on the fixed-point factor. In particular, the central
permutation of this self-Morita equivalence is **inversion**, not the identity.
The necessary sign follows from

    U(h) rho(U(g)) U(h)* = chi(h,g) rho(U(g)),
    Ad rho(U(g))(U(h)) = chi(h,g)^(-1) U(h).

On the sixteen spectral projections in End(rho kappa), the left and right
actions shift the character labels oppositely. Each central invertible above
g therefore transports to the one above -g. The existence and uniqueness of
these lifts follow from Izumi Theorem 13.4 and the trivial universal grading.
Inversion preserves H=4C16 and its regular central algebra A.

The regular-C16 module is unique: its distinguished simple has internal end
the sum of all sixteen invertibles, and H²(C16,C*)=0. Thus the proof of
Grossman--Jordan--Snyder Lemma 4.7 and Remark 4.8 applies to its square even
though sixteen is not prime. Its square is a regular bimodule with a tensor
autoequivalence on the right. The square fixes every central-invertible label;
Izumi Corollary 13.5 is faithful on those labels, so that autoequivalence is
tensor-isomorphic to the identity. Izumi Remark 12.4 additionally records
self-duality of the orbifold subfactor.

I checked the central base-change argument in
`R12_INVERSION_INDEPENDENT_AUDIT.md`: an invertible bimodule preserving a
commutative separable central algebra A descends to an invertible bimodule
over C_A. The central structure is precisely what makes the right action
balanced. Relative tensor products commute with this descent; changing the
chosen algebra identification twists one side by Aut_alg(A)=H^=C4. This
retains, rather than discards, the possible inner ambiguity when a descended
regular module is identified with a tensor autoequivalence.

## 2. Regularity, inversion, and coherence

The descended module has four simples of dimension one from the four A
structures on kappa, and four simples of dimension t=2+sqrt(5) from the free
sixteen-element orbit. The four invertibles act freely on the first set.
The decomposition rho kappa=sum(b_g), together with
Q(rho)=sum(r^j rho), implies that the four noninvertibles take any chosen
dimension-one module to the four dimension-t modules bijectively. This proves
regularity of the left module, not merely equality of dimension multisets.

The original left alpha_g action multiplies the A-character by chi(h,g),
whereas the right alpha'_g action, transported by U(g), multiplies it by
chi(h,g)^(-1). The latter calculation is on left A-modules and is unaffected
by the inversion used to balance the right algebra. Consequently the
corresponding tensor autoequivalence F satisfies F(r)=r^-1. Adjusting the
algebra identification by a character lets one choose F(rho)=r^-1 rho.
This convention agrees with the verifier's relation rho s=rs rho.

Let T generate the canonical dual C4 action. Central monodromy gives the
tensor isomorphisms

    T² = Inn(r),       Inn(r²) = Id.

Indeed, chi(1,4)²=-1 is the order-two character of H, while chi(2,h)²=1
for h in H. Parent self-duality and descent give
F²=Inn(r^ell) T^j. Since F² fixes all simple labels, 2ell+j=0 mod4.
Thus j is even and F²=Inn(r^(ell+j/2))=Id, with the exponent even.
The fusion rules force U(C_A)=1, so Aut_tensor(Id)=1. The coherence
condition for F² -> Id follows: its two composites differ by a tensor
automorphism of F, and there is no such nontrivial automorphism. Therefore
the crossed product by C2 exists as a unitary fusion category. This step
does not replace a coherent action by an order-two based-ring permutation.

## 3. Reflection dual and the integral-group discriminator

The crossed product has invertible group D8, eight dimension-t simples, and
the rank-sixteen tensor constructed by `dihedral_model()` in the verifier.
The reflection s has a genuine algebra 1+s, since it comes from the
coherent crossed-product C2 action. Its dual has four invertibles, one
dimension-two simple X, and two dimension-2t simples Y,Z. The integral
subcategory is a Tambara--Yamagami category on a group of order four.

The pointed C4 subcategory inherited from C_A has a primitive order-four
associator class. In the factor realization alpha_1^4=Ad(lambda_4) and
alpha_1(lambda_4)=chi(1,4)lambda_4=-i lambda_4. The obstruction of this
cyclic outer action is the corresponding generator of H³(C4,C*); its
order is four, independently of the convention that may invert it.

The integral reflection dual is the group-theoretical category
C(D8,<s>,Omega,psi). Ng--Schauenburg, *Frobenius--Schur Indicators and
Exponents of Spherical Categories*, arXiv:math/0601012v3, Theorem 9.2,
states that its FS exponent is the least common multiple of
|C| ord(res_C[Omega]) over cyclic subgroups C of D8. The subgroup <r>
therefore forces divisibility by 4*4=16. This directly applies to the
reflection dual, so no additional unspecified Morita-invariance assertion
is needed here.

Liu--Ng, *On Total Frobenius--Schur Indicators*, arXiv:1212.1435,
Proposition 5.3, gives FS exponent four or eight for every
Tambara--Yamagami category on V4, for both signs of tau and both
isometry classes of symmetric bicharacter. I checked the proposition and
its indicator proof in the primary PDF. Hence the four invertibles in
the reflection dual form C4.

The free irrational double orbits have trivial stabilizers, so their
induced bimodules Y and Z are simple. Their dual supports interchange,
giving Y*=Z. The relative-tensor induction identities determine their
products, and the C4 discriminator fixes the only ambiguity that is
invisible under the forgetful functor. In the basis
1,g,g²,g³,X,Y,Z, the resulting rules are

    X²=1+g+g²+g³,       XY=YX=XZ=ZX=Y+Z,
    Y²=Z²=g+g³+X+4Y+4Z,
    YZ=ZY=1+g²+X+4Y+4Z,

with g fixing X and interchanging Y,Z, and g² fixing both.

## 4. Exact replay and scope

I read the source-independent constructor and ran

    python -O work/unified/two_dimension/verify_R2665_inversion_model.py \
      --repo repo \
      --output work/unified/rank7_structural/R2665_inversion_independent_replay_O.json

It returned PASS. All 343 rank-seven coefficients match the census under
model-to-census permutation [0,1,6,2,5,3,4]. The verifier also checks the
rank-sixteen fusion axioms, the neutral R8_1_12 tensor, all four Y/Z
relative-tensor products, and all four X versus Y/Z products. The cyclic
associator and FS-exponent assertions in the program are only arithmetic
receipts for the mathematical arguments above; the program does not claim
to reconstruct an associator.

This proves a unitary realization of **R7_4_2665**, and consequently a
general, pivotal, spherical, and pseudo-unitary realization. It does not
prove realizability of R7_4_2603, R7_4_35, or R7_4_2053.

Primary sources checked: Izumi arXiv:1512.04288v2, Theorems 11.3 and 13.4,
Corollary 13.5, Remark 12.4; Grossman--Jordan--Snyder arXiv:1211.6414v2,
Lemma 4.7 and Remark 4.8; Ng--Schauenburg arXiv:math/0601012v3,
Theorem 9.2; Liu--Ng arXiv:1212.1435, Proposition 5.3.
