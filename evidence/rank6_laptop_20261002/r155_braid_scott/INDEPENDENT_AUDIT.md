# Independent audit of the local B3 spectral obstruction

This audits the mathematical necessity of the proposed test. It does not
claim that either unresolved rank-six ring is excluded.

On V=Hom(b,a^3), write A=σ1, B=σ1σ2, D=σ1σ2σ1. Then
D=BA and D²=B³=Z I, where Z=θb/θa³. All three operators are
diagonalizable: A has finite-order braiding eigenvalues, and B,D satisfy
square-free scalar-power polynomials. Every irreducible Jordan–Hölder
subquotient inherits the same scalar Z, and its spectra are submultisets
of the three full spectra. Characteristic polynomials multiply in exact
sequences, so these submultisets partition all three spectra even if the
original B3 representation is not semisimple.

For every constituent of dimension r, determinant gives

    det(D)=det(B)det(A).

For r>1, write mA(α), mB(β), mD(δ) for eigenvalue multiplicities on that
constituent. The following are necessary:

    Σα mA(α)^2 + Σβ mB(β)^2 + Σδ mD(δ)^2 ≤ r²+2;

    max(mA)+max(mB) ≤ r,
    max(mA)+max(mD) ≤ r,
    max(mB)+max(mD) ≤ r.

The second condition is elementary: two eigenspaces with dimensions
summing to more than r intersect. Their common eigenvector is also an
eigenvector of the third operator because D=BA. It spans a forbidden
common invariant line.

The first condition is Scott's rank inequality applied to the
conjugation action on End(V) of the identity-product triple
(D^{-1},B,A). The fixed spaces of the individual conjugations have
dimensions Σ m(λ)^2. Irreducibility and Schur's lemma give a
one-dimensional common fixed space, and the trace pairing identifies
the dual invariant space with the same space. Scott therefore gives
3r²−Σm² ≥ 2r²−2.

There is a further cheap necessary scalar-twist version of Scott:

    mA(α)+mB(β)+mD(δ) ≤ r whenever δ=αβ.       (* )

Indeed apply Scott on V itself to
(δD^{-1}, β^{-1}B, α^{-1}A). Their product is I, the tuple remains
irreducible, and for r>1 neither V nor its dual has a fixed vector.
The ranks therefore sum to at least 2r. This condition supplements
pair-max bounds when all three indicated eigenvalues occur.

For reference, Scott's inequality has the following short direct proof.
For X1X2X3=I on W, form

    d0: W → ⊕i Im(Xi−I),  w ↦ ((Xi−I)w)i,
    d1: ⊕i Im(Xi−I) → W, (u1,u2,u3) ↦ u1+X1u2+X1X2u3.

Then d1d0=0, ker(d0) is the common fixed space, and the annihilator
of Im(d1) is the common fixed space in W*. Thus

    Σ rank(Xi−I) ≥ 2 dim(W)−dim(W^G)−dim((W*)^G).

The primary source is L. L. Scott, *Matrices and cohomology*, Annals of
Mathematics 105 (1977), 473–492, DOI 10.2307/1970920:
https://annals.math.princeton.edu/1977/105-3/p03 .
The proof above removes any dependence on a generic-eigenvalue
assumption or on a finite image of the whole braid representation.

## Scope and implementation requirements

* All possible constituent sizes 1 through dim(V) must be allowed.
  An upper cutoff at four or any other fixed size cannot certify failure
  for larger blocks.
* For r=1, use determinant and the prescribed scalar roots. Do not apply
  the irreducible r>1 pair or scalar-twist inequalities to characters.
* A block passes if its complete spectra admit any partition into
  candidate constituents satisfying the necessary conditions. Such a
  partition is not a construction of an actual representation.
* An exhaustive failure rules out the prescribed local B3 spectra.
  A timeout or exhausted resource budget must produce UNKNOWN, never
  a negative conclusion.
* All determinant/phase equalities must be exact, in a common cyclotomic
  exponent modulus. With A,D in ζ48 and B in ζ72, ζ144 suffices.
* A categorification exclusion additionally requires justified exact
  spectral input and a proof that every candidate categorification has
  that input. This audit concerns the representation-theoretic step.

## Independent BJT phase check and controls

The rendered printed page 16 of Barter–Jones–Tucker,
*Eigenvalues of rotations and braids in spherical fusion categories*,
arXiv:1611.00071v2, was inspected independently. Its bending identity
has the factor θa, and therefore the braid trace has θa^{-1}.
The center targets for Δ and β are respectively (a*,b) and (1,b).
The n=2 sum on that page is

    ν2(c,b;a)=Σd,e (θd/θe)^2 S[c,d] conjugate(S[b,e]) N[d,e,a].

The exact dimension-two SU(2)4 control confirms both the phase and
target convention. Labels are 0,…,4, twists θj=ζ24^{j(j+2)}, and
Sij=sin((i+1)(j+1)π/6)/sqrt(3). At a=b=1,

    A=diag(ζ24^9,ζ24^1),
    F=[[1/sqrt(3),sqrt(2/3)],[sqrt(2/3),−1/sqrt(3)]],
    σ2=F A F.

Direct exact matrix multiplication yields the braid relation,
Z=−i, trace(D)=0 and trace(B)=−sqrt(3)/2+i/2. Exact evaluation of
the generalized indicator sums gives the same two traces. The spectra
are A exponents {9,1} modulo24, B exponents {18,42} modulo72, and
D exponents {18,42} modulo48, all with multiplicity one. This is a
nontrivial irreducible dimension-two positive control.

The dimension-three SU(2)4 block a=b=2 gives

    A: {16,8,4} mod24;
    B: {56,8,32} mod72;
    D: {32,32,8} mod48.

Its traces are trace(B)=0 and trace(D)=−1/2−sqrt(3)i/2. Both blocks
saturate the squared-multiplicity Scott inequality.

Two additional partition controls are useful. The direct sum of two
copies of the dimension-two block must pass through a 2+2 partition,
even though applying Scott to the entire reducible dimension-four
block would fail. Conversely A={1,1}, B={ζ3,ζ3²}, D={1,1}, Z=1
passes the total determinant and scalar-power checks but admits no
constituent partition: the r=2 candidate violates pair-max, while
neither r=1 candidate satisfies D=BA.
