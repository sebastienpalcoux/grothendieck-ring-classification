# Saturated quadratic Galois blocks give exact indicator balances

## The unified lemma

Let C be a pseudo-unitary fusion category with simple dimensions in a real quadratic field K of conductor f, and let D=FPdim(C) be irrational. Let I:C→Z(C) be induction. Assume that every center simple A outside the support of I(1) with

    dim(A)/D not in Q

has twist satisfying theta_A^f=1. This is the conclusion of equality in the quadratic dimension-block compression bound; the proof below needs no more precise residue or twist information.

Choose any nonzero Q-linear map ell:K→Q with ell(D)=0. Let k be a positive integer coprime to f such that the automorphism zeta_f→zeta_f^k fixes K. Then

    sum_i ell(dim X_i) nu_k(X_i) = ell(1),

or, equivalently,

    sum_(i != 0) ell(dim X_i) nu_k(X_i) = 0.             (GI)

The identity is exact in C. In particular it does not take real parts or normalized relative traces of the indicators. No commutativity of K_0(C) is required.

## Proof

Take a common cyclotomic field Q(zeta_N) containing all twists and K, with f dividing N. Choose an integer a congruent to k modulo f and coprime to N. Such an a exists: at primes dividing f it is already a unit; at each prime dividing N but not f impose a congruence a=1 modulo that prime. The Chinese remainder theorem gives all conditions simultaneously. Thus the automorphism tau(zeta_N)=zeta_N^a fixes K and restricts to the kth-power automorphism on the fth roots.

For a center simple A write v_i(A)=[F(A):X_i] and z_A=dim A. Since the dimensions lie in K, so does z_A. The first induction trace identity, including the unit case, gives

    sum_A ell(z_A) z_A theta_A
       = sum_i ell(dim X_i) Tr(theta | I(X_i))
       = D ell(1).                                    (1)

The coefficients ell(z_A) z_A and the right side belong to K and are fixed by tau. Because K is two-dimensional over Q and ell is nonzero with ell(D)=0,

    ell(z_A)=0  iff  z_A/D is rational.

Every term with this property vanishes in (1). If A is outside I(1) and ell(z_A) is nonzero, the hypothesis gives theta_A^f=1, so tau(theta_A)=theta_A^k. If A belongs to I(1), its twist is one, and this equality holds as well. Applying tau to (1) therefore yields

    sum_A ell(z_A) z_A theta_A^k = D ell(1).

The general induction indicator formula identifies the left side with
D sum_i ell(dim X_i) nu_k(X_i). Cancel D. Since nu_k(1)=1, this proves both forms of (GI).

The only categorical trace facts are theta|I(1)=id, Tr(theta|I(X))=0 for a nonunit simple, and Tr(theta^k|I(X))=D nu_k(X). They are Ostrik, arXiv:1309.4822, Theorem 2.5, and Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Adv. Math. 211 (2007), Theorem 4.1.

## Six applications with the same argument

| Rings | K; f | D | ell(a+b sqrt(r)) | k | Nonunit balance |
|---|---|---|---|---:|---|
| R8_2_33,36,76,412,446 | Q(sqrt17); 17 | 136+32sqrt17 | 4a−17b | 2 | sum_noninvertible nu_2 = 4 sum_nonunit invertible nu_2 |
| R8_2_630 | Q(sqrt10); 40 | 120+36sqrt10 | 3a−10b | 3 | nu_3(X3)+nu_3(X4)+4nu_3(X5)=0 |

For the first row, 2 is a quadratic residue modulo17. Every pointed dimension is1 and every nonpointed dimension is4+sqrt17, giving respective weights4 and−1. The first balance contradicts the odd number of pointed involutions and the fewer than four self-dual noninvertibles. This supplies a shorter unified proof of the balance in Q17_INDICATOR_BALANCE_PROOF.md; that file retains its independently audited alternate derivation.

For the second row, the primitive quadratic character of conductor40 takes value+1 at3. Source dimensions give weights (3,3,−4,−1,−1,−4,2,2). Only labels3,4,5 have nonzero nonunit cubic invariant spaces, each of dimension one. Their third indicators have modulus one, so the displayed equality contradicts 4>1+1. In particular the argument does not require those indicators to equal1.

The saturation hypotheses, general-complex scope bridges, and source checks are established in Q17_INDICATOR_BALANCE_PROOF.md and R630_WEIGHTED_GALOIS_INDICATOR_PROOF.md, respectively. Equality in the conductor compression bound is proved in ../compression/CONDUCTOR_EQUALITY_LEMMA.md.
