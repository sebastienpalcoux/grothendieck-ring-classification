# Independent semion-branch audit of the proposed R623 construction

## Verdict and scope

The revised construction, with the mixed-associator explanation in
`../premises/R623_model_audit.md` and the elementary final multiplicity
argument below, supplies a complex categorification of R12_1_623. It does
not require unitarity of the C36 near-group precursor. The analytic
existence theorem is used as a primary-literature theorem; the finite
replay is not represented as a fresh proof of that analytic theorem.

The source directly checked was He--Liu--Lu--Palcoux--Ren,
https://arxiv.org/html/2610.11652v1: the cyclic scalar construction,
algebraic categorical reconstruction, the parameter dictionary in
Lemma 2.14, and algebraic transport in Section 4.7. The cited unitarity
claim is a separate conjecture and is not used.

## The categorical bridge

A blind application of Izumi's C*-orbifold theorem to a pseudo-unitary
category would be insufficient. The revised argument needs only its
mixed-morphism calculation, which is specified directly in the algebraic
TPE reconstruction. In particular, testing a half-braiding on an
invertible against a product Y tensor Z involves associators having that
invertible among their input objects. It does not involve the all-X
associator block. The three marked insertions on the X-multiplicity space
are the explicit algebraic matrices X(g),Y(g),Z(g) of TPE Eq.(4.56).
Their product is a(g)^(-1) times the identity; the other required scalar
relations are bicharacter multiplication and a(g)^2 chi(g,g)=1. These are
valid without a Hermitian reflection identity.

The central invertible calculation in Evans--Gannon,
https://arxiv.org/pdf/1208.1500, Eqs.(4.6)--(4.10) and (4.48)--(4.50), thus
uses the same mixed data. For multiplicity |G| the weight-zero line is
one-dimensional, which is precisely the condition used there to obtain
the central lifts. No beta-dependent all-X block is needed in this step.

For H=6C36, the resulting pointed braiding is trivial on H times H.
The ordinary pointed associator is trivial because the unique
noninvertible supplies a rank-one module category for the pointed part.
Consequently the regular H algebra is an actual connected commutative
separable algebra in the center, and its module category is an actual
fusion category. This is the decisive existence step.

## Completeness of the object list

Free modules on the 36 invertibles identify exactly along H cosets and
supply six simple invertibles. The endomorphism algebra of the induced
noninvertible is the six-dimensional group algebra of H, after the mixed
vertex normalization. Its six primitive Fourier idempotents therefore
supply exactly six simple summands. Every module simple occurs in a free
module on an input simple, so this list is exhaustive.

The perfect pairing G/H with H-hat makes the left and right actions on
these six summands free and transitive, with opposite character shifts.
The normalized dimension of each is d=3+sqrt(10). The pointed channel in
the square of the zero-character summand is selected by

    (1/6) sum_(h in H) a_I(h) b(h,g).

Since a_I(6j)=(-1)^j, this character average selects exactly the coset
3 modulo 6. Thus sigma^2 has precisely one pointed summand, the involution
z, and sigma^*=z sigma. These are mixed-channel and finite Fourier
calculations, not statements about positivity of operator-algebra maps.

## Short replacement for the noninvertible-channel calculation

Write sigma^2=z+sum m_j g^j sigma. The inversion mixed rule and associativity
force m_(j+2)=m_j. Thus there are only two coefficients, m_even and m_odd.
The dimension equation gives m_even+m_odd=2. Under duality,
(g^j sigma)^*=g^(j+3) sigma, while (sigma^2)^*=sigma^2, so the two
coefficients agree. Both are therefore 1.

This argument eliminates the need to transfer the more elaborate
noninvertible-channel isometry calculation from a C* proof. All products
are now forced. I reran the independent verifier under Python -O; all
1728 census structure constants matched and its associativity and duality
checks passed.

## Checks not promoted beyond their scope

The central-semion necessary conditions derived earlier are consistent
with this construction. The proposed general rule that a central semion
must split from a nonbraided category is false; the explicit C4 cocycle
counterexample in this directory verifies this directly.

One can predict a center profile by formally transporting the full
unitary near-group-center table, but that full table requires an additional
algebraic completeness check for this precursor. No center rank or full
modular data is claimed from that transport here. It is unnecessary for
the fusion-category construction.
