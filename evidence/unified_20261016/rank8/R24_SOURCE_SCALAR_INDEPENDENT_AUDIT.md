# Independent source and finite-algebra audit of the R24 square obstruction

Auditor: two-dimension workstream. Date: 16 October 2026.

The latest standard-library `verify_r24_projective_inner_square.py` has been read in
full and replayed independently with Python optimization. All exact source,
character, dual-slot, diagonal-contraction, and two-branch scalar checks
pass. Receipt: `r24_source_scalar_independent_optimized.json`. The final receipt is PASS. Its scope is the source and finite arithmetic; the categorical proof is established in the separately audited `R24_PROJECTIVE_INNER_SQUARE_PROOF.md`.

An additional independent direct read of the compressed rank-eight census
confirms tensor SHA-256
`2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738`.
The neutral model (1,g,r,gr) maps to source labels (0,7,5,6). The odd
invertible s has label1, inverse label2, and square label7. The source is
commutative, its neutral block is closed with r²=1+2r+2gr, and conjugation
by s fixes all four neutral simple labels. Thus every actual realization
provides a label-fixing tensor autoequivalence F=Ad(s) of the neutral
category with F² tensor-isomorphic to Ad(g). This uses actual objects and
associativity, not an asserted existence of an abstract extension.

The verifier checks the complete neutral character table and formal
codegrees (20+8sqrt5,20−8sqrt5,4,4), the indicator-sign arithmetic, and
the exact two-dimensional cubic-rotation trace possibilities. The latter
enumeration leaves only both multiplicity triples (2,0,0) when their traces
sum to4; no reality of a general cubic indicator is assumed.

I independently expanded the three selected resolutions in the restricted
coefficient frame. They are exactly

    q1(0000) = 2r0² + 2xX,
    q3(0000) = 2xX + 2zZ,
    q3(0101) = 2xX + 2yY.

The portable replay now verifies these expansions in a polynomial ring over
Q(sqrt5), keeping incoming/outgoing coefficient partners independent. It
checks all sixteen odd-dual slot substitutions and only the two diagonal
even D flips, whose decorated phases are separately cubes. Thus neither
complex conjugation nor equality of the two decorated cubic phases is
inserted into the finite calculation. The A parity/cyclic/even identities
are checked separately.

Both corner-character possibilities r0=(2−sqrt5±1)/4 yield nonzero yY=zZ,
respectively (sqrt5−1)/8 and (3sqrt5−5)/8. The stated gauge weights
(−2,2),(−2,−2) force u^4=1 when both coefficients are preserved. The
antidiagonal case has scalar square independently. All of this is exact
algebra, and no unitary classification, positive Hermitian form, fourth
indicator, or full F-symbol reconstruction is used.

The categorical incoming-loop/right-bend convention is audited separately
in `R24_INCOMING_LOOP_INDEPENDENT_AUDIT.md`. The restricted coefficient-to-diagram
identification is independently audited by two_d_two, and the projective
functor normalizer by rank6_center. Together these isolate and check the
categorical premises of the finite computation. This audit agrees with
the resulting no-label-fixing-square-root implication and its source
application to R24; the complete theorem has been accepted after the independent component audits.
