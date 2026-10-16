# Independent audit of the incoming-loop convention and projective functor action

Auditor: two-dimension workstream. Date: 16 October 2026.

Scope: the local orientation issue in
`PU_2D2_EXPLICIT_DUAL_BRIDGE_DRAFT.md`, and the functor-action part of
`PU_2D2_NO_INNER_SQUARE_DRAFT.md`. The source images on published EIP
pages 506--507 and the corresponding TikZ source were inspected directly.
The orientation convention and resulting loop/bend equations **pass**.
This note does not independently establish the later tetrahedral coefficient
table or the scalar consequences of the tube equations.

## Which incoming operator occurs

There are two different operations that must not be confused. The ordinary
pivotal transpose of an outgoing linear operator has its transpose matrix
on the composition-dual space. In contrast, the operator obtained by applying
the *same tensor functor* to incoming morphisms has the inverse-transpose
matrix. The latter is the incoming wrapping in the EIP bend calculation.

To see the distinction without a dagger, let F=Ad(g), choose object
identifications q_A:F(A)->A and q_B:F(B)->B, and write the two actions on
opposite Hom spaces as

    T_+(f)=q_B F(f)(q_A^{-1} tensor q_A^{-1}),
    T_-(h)=(q_A tensor q_A)F(h)q_B^{-1},

where f:A tensor A->B and h:B->A tensor A. Tensorators are implicit.
Then T_+(f)T_-(h)=q_B F(fh)q_B^{-1}. Since B is simple, composition
pairings are preserved exactly. Consequently

    T_-=(T_+)^{-t}

in composition-dual bases. Expanding the q maps as crossings and evaluation
maps shows that the incoming wrapping has the opposite crossing orientations
from the outgoing wrapping. This conclusion uses functoriality, not a
Hermitian form or complex conjugation.

The original EIP Frobenius diagrams on page 507 use an incoming trivalent
vertex inside each bend: one incident arrow enters and the other two leave.
They are anti-linear only because the paper labels that incoming vertex by
the dagger of an outgoing basis vector. Replacing it by an independent
composition-dual incoming vector gives a linear bend H_- -> H_+ (or J_- ->
J_+). When the wrapping is pulled through this bend, the red crossings
reverse orientation. Thus the operator on the incoming side is precisely
T_- above, not the ordinary transpose of T_+.

The pivotal transpose here is taken relative to the canonical pivotal
structure of F=Ad(g), including its canonical duality comparison. In
particular q_1=ev_g has form defect one. One must not substitute a naive
palindromic identification of g A g* with its dual: that would insert an
extraneous cup sign. The defect of q_r is the two-crossing scalar mu of
EIP Definition 3.2; the decorated identification adds lambda_g. Equivalently,
if q_A and q_B have form defects s_A,s_B, the transpose of the two displayed
functor actions gives R T_+=(s_B/s_A^2)T_- R. This reproduces precisely the
two signs below.

The elementary moves in that pull-through are the crossing/inverse relation
on page 506, the black self-duality bend, and the red self-duality bend.
The crossing convention contributes mu. In the J diagram there is one
additional reversal of the external g self-duality map, contributing
lambda_g. In the H diagram that reversal occurs twice and cancels. The
linear forms of the displayed EIP relations are therefore

    K_H+ R_H = mu R_H K_H-,
    K_J+ R_J = mu lambda_g R_J K_J-,
    K_H-=(K_H+)^{-t}, K_J-=(K_J+)^{-t}.

The left bend has the same covariance. Here mu=1 and lambda_g=-1, so these
are exactly the equations in the bridge draft. No scalar i is conjugated
in these linear identities. Instead, the inversion of the H loop changes
its eigenvalues i,-i to -i,i on the incoming composition-dual basis.

Combining these relations with K_H+ squared=-I and K_J+ squared=I makes
both loop operators skew with respect to their symmetric bent theta
pairings. In a two-dimensional nondegenerate pairing, this forces both
opposite eigenvalues to occur and pairs their eigenlines nontrivially.
Rescaling paired eigenvectors makes the bend matrix

    E = [[0,1],[1,0]].

This checks the required hyperbolic theta-frame normalization. It does not
turn the pairing into a positive or Hermitian one.

## Crossing rescaling and projective actions

The normalized crossing relation on page 506 compares one-click pivotal
rotation with the inverse crossing. A pivotal tensor functor sends a
crossing rescaled by lambda to the left side rescaled by lambda and the
right side rescaled by lambda^{-1}. Hence lambda squared=1. This remains
valid over an arbitrary complex pseudo-unitary category.

The induced action on Hom(r tensor r,r) is well-defined projectively on
tensor-isomorphism classes: changing the identification F(r)->r contributes
one overall scalar, as does a monoidal natural isomorphism. These projective
actions compose. Expanding Ad(g) with the q maps above gives exactly the
three-leg wrapping K_H, up to an overall scalar and possibly reversal.
Reversal replaces K_H by its inverse, which has the same projective class
because K_H squared=-I. Its projective class is nontrivial.

With the stated nonzero mixed coefficients and their weights, the subsequent
normalizer argument is valid: a crossing sign -1 gives an antidiagonal H
matrix with scalar square; sign +1 gives diagonal paired matrices, and
the two nonzero weights force u^4=1. Thus every label-fixing functor has
projectively trivial square on H. This last implication remains conditional
only on the independently checked coefficient identities, not on a dagger
or an unitarizability theorem.


## Final integration

The audited orientation and functor-action conventions above are used in the accepted `R24_PROJECTIVE_INNER_SQUARE_PROOF.md`. The local coefficient premise is supplied by `R24_RESTRICTED_COEFFICIENT_INDEPENDENT_AUDIT.md` and is checked independently in `R24_PAIRED_LOOP_INDEPENDENT_AUDIT.md`. Only the two diagonal decorated even flips and three diagonal resolutions are retained. No assertion about equality of the decorated cubic phases is part of the final theorem. Source and finite arithmetic replays are `r24_projective_inner_square_normal.json` and `r24_projective_inner_square_optimized.json`; their scope does not replace this categorical orientation argument.
