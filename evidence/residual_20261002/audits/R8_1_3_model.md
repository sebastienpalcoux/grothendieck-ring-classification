# Independent audit of the R8_1_3 twisted group-theoretical model

Audited 2 October 2026. Result: the construction in
`../../../supplements/rank8/software/twisted_group_theoretical_c2.py` proves unitary categorifiability of
R8_1_3, assuming the standard construction of bimodules over a separable algebra
in a unitary pointed category. This is an actual categorical construction,
not an inference from matching a dimension list.

Let G=C5 semidirect C4, with the generator of C4 acting on C5 by multiplication
by 2. Write elements as (a,b), b in {0,1,2,3}, and let

    omega(x,y,z)=(-1)^(b(x) floor((b(y)+b(z))/4)).

This is the inflation of the standard parameter-2 C4 cocycle. The exact
script checks all 20^4 cocycle identities. For H={1,s}, s=(0,2), its restriction
to H is trivial, so A=1+s is the standard connected unitary separable algebra
in Vec_G^omega. The category of A-bimodules, with tensor product over A, is an
actual unitary fusion category of global dimension 20.

## Verification of the action and tensor conventions

The associator on homogeneous grades x,y,z is the scalar omega(x,y,z).
Since b(s)=2, both omega(s,s,x) and omega(s,x,s) are 1. Consequently the
script may choose every left action L_s with phase 1, and the mixed bimodule
axiom is exactly R_s L_s=L_s R_s. The remaining right-module axiom is

    R_s(R_s(v_x)) = omega(x,s,s) v_x = (-1)^b(x) v_x.

The two size-two double cosets have representatives commuting with s. On
each, the two simple bimodules have L_s^{-1}R_s eigenvalues i^p and -i^p,
where p=b(x) modulo 2. On a size-four double coset the stabilizer is trivial,
so there is a single simple bimodule, of dimension one in every homogeneous
grade. This accounts for all simple bimodules: four with categorical dimension
1 and four with categorical dimension 2.

For the balanced tensor product M tensor_A N, the defining relation is

    r_x e_(xs,y) = omega(x,s,y) e_(x,sy).

Replacing x by xs gives

    e_(x,y) = omega(xs,s,y)/r_(xs) e_(xs,sy),

which is precisely the script's quotient phase
`w(mul(x,s),s,y)-A['R'][mul(x,s)][1]` modulo 4.
The tensor-product right action has phase omega(x,y,s) times the right-action
phase of N; the left action has phase 1 because omega(s,x,y)=1. Thus the
script computes the genuine L_s^{-1}R_s operator on every stabilizer fiber.
Its trace and dimension determine the multiplicities of the two one-dimensional
stabilizer types. For trivial stabilizers, the grade-fiber dimension gives the
multiplicity directly. No associativity convention is omitted.

## Exact identification

An independent replay completed successfully, checking the cocycle and all
finite action/quotient identities, the unit, all associativity identities and
the dimensions. The only census match is R8_1_3, tensor SHA256

    8e5341d955006cc35e17908037e4552c31d1d97cbed4844002f68b353ee140b1

with model-to-census permutation

    [0,7,1,2,5,3,6,4].

The final check compares all 8^3 tensor coefficients. Existence and unitarity
come from the pointed-category bimodule construction; the tensor replay
identifies the existing category with the census ring. No classification of
all associators on that ring is asserted.
