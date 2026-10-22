# R1768: the irrational-ratio sector has five possible induction Grams

This argument uses the saturated-conductor theorem, its signed prime refinement,
and the exact fibre norm formula proved in `../unified/`. It also uses the
previously proved nontrivial pointed C2 associator and general-to-spherical /
pseudo-unitary Galois reduction. The calculation below therefore applies to a
pseudo-unitary Galois form of any hypothetical complex categorification.

Write s=sqrt(37), u=6+s, D=444+72s=12su, and
alpha=D/D'=73+12s. The simple source dimensions are

    (1,1,5+s,6+s,7+s,7+s,6+s,5+s).

Here “irrational-ratio sector” means center simples with irrational d_Z/D,
other than 1 and A_sigma. Rational-ratio simples are allowed to have primitive-37
twists too; their complete all-order trace domain is retained throughout.

The only twist-one center objects with irrational dimension divided by D are
the two distinguished dimension-orbit objects 1 and A_sigma. Every other
center simple with irrational d/D has primitive-37 twist in the nonsquare
coset. For each of the eighteen such twists, the exact capacity is

    sum_Z (37 b_Z - 6 a_Z)^2 = 144,  d_Z=a_Z+b_Z s.

## 1. Galois eliminates the large-unit dimension family

The normalized center S-matrix has s_0Z=d_Z/D. Modular Galois symmetry gives

    d_(hat sigma Z) = D |sigma(d_Z/D)|.

The square Galois action on the canonical center T-matrix preserves twist
order. The canonical center representation is linear with no anomaly factor.
For d_Z=k alpha the Galois partner has dimension k. A center simple of integer
dimension has forgotten object supported entirely on 1 and g: all six
noninvertible source dimensions have a strictly positive s coefficient.
Every center object whose forgotten object contains 1 belongs to I(1), hence
has twist1. Every center object whose forgotten object contains g belongs to
I(g), hence has twist+i or-i by the previously established pointed theorem.
Neither is compatible with primitive37 twist. Consequently the k alpha
family cannot occur in the irrational-ratio sector.

The complete existing high-column domain has497 restriction columns. Its
nonrational-d/D columns avoiding g have dimensions only k u or k alpha.
Removing the latter leaves25 columns, of dimensions k u for
k in {1,2,3,4,6,12}. This finite-domain statement is arithmetic, not a claim
that any of these objects exists.

## 2. Galois acts by an explicit complement on restriction vectors

Let v=(v_0,...,v_7) be a irrational-ratio restriction vector of dimension k u.
Then v_0=v_1=0. For the nontrivial automorphism sigma of Q(s),

    sigma(d_Z/D) = -d_Z/D,

so the Galois sign is negative and the partner again has dimension k u.
The source character table has six rational characters E, with rational
formal codegrees f_E, and the two FP-conjugate characters. For every rational E,

    s_(A_E,Z) = chi_E(v)/f_E

is rational. Applying modular Galois symmetry to the Z column therefore gives
chi_E(v_hat)=-chi_E(v). The FP and conjugate-FP character values are unchanged,
because the dimension k u of the partner is unchanged and v_hat is integral.

Orthogonality of the eight characters now implies

    v_hat = 2 P v - v,
    P = d d^t / D + d' (d')^t / D',

where P is the rational orthogonal projector onto the two FP character lines.
Direct substitution gives

    P v = (0,0,k/6,k/6,k/6,k/6,k/6,k/6),
    v_hat = (0,0,k/3-v_2,...,k/3-v_7).

In particular,3 divides k, and all six noninvertible coordinates lie between
0 and k/3. Applying this exact complement test to the25 columns leaves six:

* v=(0,0,0,0,1,0,1,1) and w=(0,0,1,1,0,1,0,0), dimension3u;
* 2v and2w, dimension6u;
* z=v+w=(0,0,1,1,1,1,1,1), dimension6u;
* 2z, dimension12u.

The unit and g coordinates are included in these displayed eight-vectors.

## 3. Five complete possible Gram contributions

Choose a primitive37 root zeta. Galois automorphisms with residue l modulo37
act on twists by zeta^k -> zeta^(l^2 k). All18 nonsquare exponents occur.
Quadratic residues l fix v and w; nonresidues interchange them. CRT gives
lifts with the prescribed residue modulo37 and any needed compatible
residues at other primes. Thus, for nonnegative integers a,b,c,d, the total
multiplicities in the irrational-ratio sector have the form

    v,w:9a each;  2v,2w:9b each;  z:18c;  2z:18d.

This is a necessary aggregate statement; it does not assume that each Galois
orbit has exactly18 objects. Orbits with larger stabilizer kernels are also
covered by these integer multiplicities.

For v,w the capacity coefficient is3; for2v,2w,z it is6; for2z it is12.
The eighteen fibre equations therefore imply

    a+4b+4c+16d=16.

Set U=a+4b and V=c+4d. Then U+4V=16, and the complete irrational-ratio-sector
restriction Gram is

    G_37 = 9 U (v v^t+w w^t) +18 V z z^t,
    V=0,1,2,3,4,  U=16-4V.

Every high-column feature in the previous exact cone is homogeneous quadratic
in the restriction vector. The only relative trace ray is that of a
nonresidue primitive37 root:

    ((-1-s)/36,(-1+s)/36,(-1-s)/36,(-1-s)/36).

Hence the full irrational-ratio-sector contribution, including Gram, indicator, rotation and atomic
STS rows, is exactly9U times each of the v and w columns plus18V times the z
column. It can be subtracted from the right-hand side. Every remaining high
column has rational d/D; its complete previously proved all-order trace domain
is retained. No twist cutoff or omitted rational-dimension branch is used.

`finite_fibres_cone.py` checks all five necessary integer branches against all
eight still-admissible second-indicator assignments, using only exact Farkas
certificates for any rejection. If a necessary relaxation survives, its exact
rational witness is recorded instead; it is not a category or a construction.

## 4. The Galois image of the unit has a unique restriction

Let c be the restriction vector of A_sigma. The sign of the Galois image of
unit is positive, since sigma(1/D)=1/D'>0. Each rational-character S row
therefore gives chi_E(c)=chi_E(1)=1. The two FP character values are alpha and
alpha'. Character orthogonality determines all eight coordinates uniquely:

    c = e_0 + ((alpha-1)/D) d + ((alpha'-1)/D') d'
      = e_0 + (d-d')/sqrt(37)
      = (1,0,2,2,2,2,2,2).

Here DD'=5328 and (D-D')/(DD')=1/sqrt(37). This argument determines a
restriction vector, not an algebra structure on its underlying object.
The frozen alpha domain has532 candidate columns; exactly one is this vector.

## 5. Exact outcome and its limits

The saved certificates cover all40 combinations of the five Gram branches
and the eight remaining second-indicator assignments. Exactly39 combinations
have exact Farkas certificates of infeasibility. The sole surviving branch is

    V=4, U=0, indicators(g,X2,...,X7)=(-1,1,1,1,1,1,1).

Thus all six noninvertible second indicators in a pseudo-unitary Galois form
must be+1. With V=4 the integer capacity equation has just two solutions,
(a,b,c,d)=(0,0,4,0) or(0,0,0,1). The irrational-ratio sector consequently has either

* seventy-two simples of dimension6u=36+6sqrt(37), restriction z, with four
  simples at each of the eighteen nonresidue twists; or
* eighteen simples of dimension12u=72+12sqrt(37), restriction2z, with one
  simple at each of the eighteen nonresidue twists.

In both cases its Gram contribution is72zz^t. Forcing the unique alpha
restriction as well still leaves an exactly feasible rational cone. This
witness satisfies the retained necessary equations; it does not prove integer
center data, modular-data existence, pentagon solvability, or categorification.
R8_3_1768 remains unresolved.

For a further integral constraint, the two distinguished objects contribute
73/2664 of the squared global center dimension and the irrational-ratio sector
contributes18/37. Every remaining object has dimension tD/12 for a positive
integer t, so the complete rational sector satisfies sum t^2=70. The four
rational I(1) constituents of dimensionD/6 and the two of dimensionD/12 consume18,
leaving sum t^2=52 for the high rational sector. This is a necessary dimension
identity, not an additional exclusion.

## Replay

Run from the repository root:

    python evidence/rank8_creative_20261022/r1768/verify.py
    python -O evidence/rank8_creative_20261022/r1768/verify.py

The verifier reconstructs and binds the complete frozen atomic domain,
checks the source character arithmetic and finite five-branch reduction,
replays all39 separators against every allowed column, and verifies both
surviving rational witnesses exactly. Every check uses an explicit failure
condition and therefore remains active under Python optimization.
The analytic modular-Galois and saturated-conductor arguments are mathematical
prerequisites recorded here and in `../unified/`; a finite arithmetic replay
does not replace their proofs.
