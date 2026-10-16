# Independent R24 source and annular-corner audit

Status: **PASS for the source-to-inner-square implication and the two-valued
corner parameter**. This audit does not by itself certify the separate
partial-dual coefficient bridge or a classification decision.

Reviewed: the revised `R24_MINIMAL_DUAL_BRIDGE_DRAFT.md`, which leaves the two
decorated cubic phases arbitrary and does not identify incoming and outgoing
decorated rotations. The earlier proposed equality of those phases is neither
needed nor approved here.

## 1. Exact source binding

I independently reconstructed the multiplicity-two census, selected its
lexicographic entry 24, and checked the full source associativity and Frobenius
identities. Its compact JSON tensor SHA256 is

    2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738

The ordered neutral basis is `(1,g,r,gr)=(0,7,5,6)`. All 64 coefficients agree
with

    g^2=1, gr=rg, r^2=1+2r+2gr.

The basis is closed under multiplication and duality. The source invertible
`a=1` has dual `2`, satisfies `a^2=g=7`, and conjugation by `a` fixes each
neutral basis element. These checks are reproduced without third-party
packages by `verify_r24_inner_square.py`; the independent optimized receipt is
`r24_inner_square_independent_optimized.json`.

In any categorification, the neutral basis therefore spans an actual fusion
subcategory D. The actual invertible object a supplies the tensor
autoequivalence F=Ad(a)|D. Associators and an isomorphism a tensor a -> g give
a coherent monoidal natural isomorphism F^2 -> Ad(g). The source commutativity
proves that F fixes the simple isomorphism classes; it does not assert that F
is tensor-isomorphic to the identity. No central lift, braiding, or dagger is
used. After the independently established Galois pseudo-unitarity reduction,
the canonical pivotal structure of D is preserved by its tensor
autoequivalences.

## 2. The annular corner is an ordinary semisimple representation

Primary source: Edie-Michell--Izumi--Penneys, *Classification of
Z/2Z-quadratic unitary fusion categories*, arXiv:2108.01564v2. I inspected its
TeX source `EIP_source/main.tex`, specifically the general spherical tube
algebra definition, the unit-corner character table, the block action on
A_(1 <- r), the coefficient formula for phi, and the proof of the lemma
labelled `lem:SDidInd` (published Lemma 3.7). The general tube definition uses
composition-dual bases, not adjoints. Its multiplication and the corner action
are linear spherical identities, despite the paper's overall unitary
classification scope.

For D, the unit corner is the complex fusion algebra. Its four characters on
`(1,g,r,gr)` are

    (1,1,d,d), (1,1,dbar,dbar), (1,-1,1,-1), (1,-1,-1,1),
    d=2+sqrt(5), dbar=2-sqrt(5)=-1/d.

The annular space A_(1 <- r) has dimension four, with the two multiplicity-two
summands contributed by its r and gr loop labels. The actual left action has

    P = [[0,I],[I,0]],  R = [[phi,phi0],[phi0,phi]].

The tetrahedral A symmetries used in the minimal draft give
`phi_(k,i)=sum_j A^(j,k)_(j,i)=2 r0 delta_(k,i)`. This is the source's explicit
coefficient contraction. It does not use complex conjugation.

The first character is the restriction of the central tensor unit. Its
multiplicity in A_(1 <- r) is zero: equivalently, the forgetful image of that
central object is the tensor unit, with no r summand. This is the standard
semisimple tube-module/center correspondence, and is also exactly the
argument in the source lemma. A direct check is available using its primitive
central idempotent

    e0 = (1+g+d*r+d*gr)/(2+2d^2).

Since e0 acts by zero, its restriction to the P=+1 eigenspace gives
`phi+phi0=-I/d=dbar I`. This avoids any appeal to a positive or Hermitian
representation. On the P=-1 eigenspace, the fusion relation
`R^2=I+2R+2PR` becomes `(phi-phi0)^2=I`. Substituting phi=2r0 I gives

    (4r0-dbar)^2=1,
    r0=(2-sqrt(5)+tau)/4, tau in {+1,-1}.

Thus both branches in the revised draft are necessary possibilities, and
this reduction remains valid for a pseudo-unitary spherical category
without a C*-structure.

## 3. Remaining separation of responsibilities

The displayed two-valued r0 conclusion is conditional only on the stated
linear A coefficient symmetries; its annular representation argument is
independently approved. The identification of the exact partial-dual slots
and the three diagonal resolutions is a distinct categorical calculation.
Neither numerical agreement with a unitary model nor the mere existence of
an abstract tetrahedral-symmetry theorem would substitute for that check.

The source-to-inner-square implication in section 1 is unconditional and does
not depend on those local coefficient identities.
