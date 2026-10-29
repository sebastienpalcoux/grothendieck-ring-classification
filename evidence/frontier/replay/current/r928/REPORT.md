# R928 continuation: one explicit rank-20 modular datum

**Result.** Three of the four previously retained center patterns are now
excluded. The remaining pattern186 admits an explicit complete S,T datum
with a nonnegative integral rank-20 fusion tensor. Its categorical realization
and the required algebra are not constructed; R928 remains unresolved.

All conclusions here concern the accepted positive modular factor B in the
inherited general-complex existence reduction. No new existence reduction
is asserted. Put D=(144,96,80,56), L=D/sqrt(2), where tuples use
(1,sqrt(2),sqrt(3),sqrt(6)). The four low objects B0,...,B3 are exactly
the scalar-character constituents of I(1), with restriction-unit
multiplicity one and positive semion monodromy charge. Thus they belong
to B and their twists are 1. This is explicit in source.json and
m3_frontier.tex, sections Integral central multiplicities and Forced
central involutions. The fifth canonical constituent has negative charge;
its semion translate W belongs to B, has dimension D/4, and twist i after
choosing the orientation xi(B)=exp(pi*i/4). The other orientation is the
complex conjugate and gives the same exclusions.

## 1. Two patterns are impossible

Use normalized S. In patterns49,191 the unique simple H of dimension L/2
has first four S-row entries (1,-1,-1,1)/2. They exhaust its row norm1;
every other entry, including S_HH, is zero. Since the first four twists
are1, (STS)_HH=1. But STS=xi T^-1 S T^-1 gives (STS)_HH=0.
This contradiction requires no unknown fusion rule, twist, or numerical
search. Independent check: ../unified/audit_r928_bosonic_row.py.

## 2. Four Fourier vectors in the retained patterns40,186

Let a=(1,1,-1,-1)/2, b=(1,-1,1,-1)/2,
c=(1,-1,-1,1)/2, and e=(1,1,1,1)/2, supported on B0,...,B3.
They are all fixed by T. The known Galois-unit rows determine S times
each vector, exactly; the displayed formulas are obtained by the four sign changes of the dimension field.

Write E and F for the unique objects of dimensions
(6,4,4,2) and (34,24,20,14); write A for the fiber of dimension
(14,10,8,6), B for the fiber of dimension(20,14,12,8), and H for the
four objects of dimension(24,18,14,10)=L/4. Pattern40 has nine A and
three B objects. Pattern186 has five A, three B, and one K of dimension
(28,20,16,12), twice the A dimension.

The exact known vectors give:

* S a has low part -sqrt(6)*a/6 and coefficient sqrt(6)/6 at E,F and
  each of the three B objects.
* S b has low part -sqrt(3)*b/6; high coefficients are -sqrt(3)/6 at E,
  +sqrt(3)/6 at F and each A, and +sqrt(3)/3 at K if present.
* S c=(sum_H e_H)/2.
* S e has support only on the first five objects.

The a,b cross STS entry is zero and forces theta_E=theta_F=t.
The diagonal a entry gives

    sum_B theta_B = -1 - 2t - sqrt(6)*xi.

The diagonal b entry gives

    sum_A theta_A + 4theta_K = -1 - 2t - 2sqrt(3)*xi

in pattern186; omit the K term in pattern40. The c diagonal gives
sum_H theta_H=0. These are exact complex equalities, not relative traces.

## 3. Why full square-Galois orbits apply to these fibers

For any cyclotomic Galois automorphism sigma, normalized S symmetry gives

    d_{pi_sigma(j)} = L * abs(sigma(d_j/L)).

The restriction of sigma to Q(sqrt2,sqrt3) is one of the four sign changes.
Direct substitution using each tuple above shows that the dimension sets
A, B, H, and K each map to themselves; the two dimensions E,F map to
the set{E,F}. This is a full-Galois statement, not merely a claim for the
kernel of the dimension field. It is checked independently using the
four sign changes. Multiplicity therefore bounds each twist's full
square-Galois orbit.

Normalize the linear modular representation with gamma=exp(pi*i/12),
gamma^3=xi. The twist relation is
theta_pi=theta_j^(u^2)*gamma^(1-u^2). Every relevant Galois exponent u is
coprime to24, so u^2=1 mod24 and the gamma factor is1.

Cauchy's theorem for modular categories implies the twist orders have
prime support{2,3}: Norm(D)=2^14*3^2 and dim(B)=D^2/2. For a root of
order 2^a*3^b, its full square-Galois orbit has size
2^max(a-3,0)*3^max(b-1,0). Surjectivity of reduction on cyclotomic unit
groups ensures this counts the complete orbit for any larger conductor.

Consequently:

* E,F share one twist, so t has order dividing24.
* The three B twists have orders dividing48 or72.
* The unique K twist has order dividing24.
* The five A twists in186 have orders dividing96 or72.
* The four H twists have orders dividing96 or72.
* The nine A twists in40 have orders dividing192,144,or216.

These are unions of bounds, not permission to use every root in their
least common multiple. Each fiber is a multiset union of complete square
orbits, with integral orbit multiplicities.

## 4. Exact finite reductions for pattern186

The three-B equation is checked in Q(zeta288) by verify_phase_reduction.py. For xi+,
write phases as exponents modulo144. Exactly four possibilities survive:

    t60: B=(96,96,108)
    t84: B=(36,96,96)
    t96: B=(60,60,108) or(36,84,84).

All these twists in fact have order dividing12. The opposite orientation
is obtained by complex conjugation.

The same verifier uses Q(zeta288), with Phi288=x96-x48+1,
and enumerates complete square orbits of permitted sizes. Every nonsingleton permitted orbit has zero sum. The five-A and
K equation yields exactly ten allocations, recorded in phase_reduction_verification.json; all
A,K twists are in mu24. This search visits161497 short combinatorial
nodes, underone second here, rather than an associator search.

The H equation and full orbit condition yield312 possible quartets.
The verifier applies only the Anderson--Moore--Vafa equations with three
W inputs, whose coefficients are known from N_W:

    (theta_W^3 theta_X)^M_X
       = product_r theta_r^(3*N_W[W,r]*N_W[r,X]),
    M_X=(N_W^2)[W,X].

Forty-eight allocations survive. The modular indicator formula for W is

    nu_m(W)=(1/dim(B))*sum_ij N_W[i,j] d_i d_j (theta_i/theta_j)^m.

Using N_W in this formula is valid regardless of the unknown dual
permutation: replace the second index by its dual; dimensions and twists
are unchanged. Since N_WW^W=17, braided self-duality parity forces
nu2(W)=1. The verifier keeps twelve allocations.

For an order-four rotation nu4(W) belongs to Z[i]. The verifier rejects
ten more allocations because the exact value is outside Q(i). Two remain:

All phases in zeta1728: t=1152; B=(720,720,1296);
A=(288,288,864,1512,1512); K=936; W=432.
The H quartet is either
(162,594,1026,1458) or(378,810,1242,1674).
Their nu4(W) values are2 and40; both have nu3(W)=5.

A further matching and modular-block argument reduces these two to one;
see the following section. These are necessary data only, not categories.

## 5. Integral projections force matchings

For patterns40,186 the previously known second fusion matrix has the form
N_C=M+Q0+Qres, where C=B3, Qres is supported off the first five labels,
Qres is positive semidefinite, Qres^2=2Qres, and rank(Qres)=3. The exact
baseline M+Q0 is integral. Thus Qres is an integral symmetric matrix.
It kills the strictly positive dimension vector, since the omitted spectral
subspace is orthogonal to the Frobenius--Perron column.

Each diagonal entry q is an integer in{0,1,2}. If q=2, the equation
(Qres^2)_ii=2q forces all off-diagonal entries in that row to vanish;
then Qres*d=0 is impossible. A zero diagonal gives a zero row. At a
unit diagonal the same equation gives precisely one off-diagonal entry
of absolute value one; the positive dimension vector forces that entry
to be -1, joining two equal-dimensional objects. Hence Qres is exactly
three disjoint blocks [[1,-1],[-1,1]], on pairs of equal FP dimension.
This replaces an unknown real projection with a small exact matching list.

For186 there are354 such matchings. Applying the three-C Vafa equations
and the second/third C indicators to the two retained phase assignments
forces two H antipodal pairs and one of the following equal-twist pairs:
A at phase288, A at phase1512, or B at phase720 (exponents modulo1728).
The finite verification and independent proof are in the companion pair
agent's matching files. There are three candidate matchings per phase. The ordered replay is
matching_vafa.py, matching_indicator.py, matching_higher.py.

## 6. A six-dimensional modular block forces one matching

Let H twists be(a,ia,-a,-ia), and pair H0 with H2 and H1 with H3.
Let U be the span of the two normalized pair-sums and V the span of the
two normalized pair-differences. Let f=(1,-1,-1,1)/2 on the four canonical
objects. Let e be the normalized difference of the selected outside pair,
whose two objects have the same twist lambda. Put F=span(f,e).

The known H-column projection is ff^t plus the three matching projections.
Consequently the H-by-H block of S has squared norm equal to the projection
onto V. Norm saturation implies S preserves V, and S interchanges U and F.
The four H twists are distinct, so the H objects are selfdual. S^2=1 on H
then forces S^2=1 on F as well; in particular the selected outside pair is
selfdual individually. The known uniform sum of H columns gives
S f=(sum_H e_H)/2. Thus, after a harmless sign choice for e, the U--F
block is the orthogonal Hadamard matrix

    R=1/sqrt2 [[1,1],[1,-1]].

On V, write S=M, a real symmetric involution. On U+V, T interchanges
U,V with matrix A=diag(a,ia); on F, T=D0=diag(1,lambda).
The U--U block of STS=xi T^-1 S T^-1 gives

    R D0 R^t = xi A^-1 M A^-1,
    M=xi^-1 A R D0 R^t A.

Squaring the last explicit two-by-two matrix gives

    M^2=(a^4 lambda/xi^2) I.

Therefore a^4 lambda=xi^2=i. In the phase branch beginning162,
a=zeta32^3, so lambda=zeta8^7; only the A phase1512 pair has that twist.
In the branch beginning378, a=zeta32^7 forces lambda=zeta8^3, which no
candidate outside pair has. That branch is impossible.

Thus pattern186 has a unique remaining twist multiset and a unique N_C
matching, up to permutations inside identical dimension/twist fibers:

    low twists1; W=i; E=F=zeta3^2;
    A=(zeta6,zeta6,-1,zeta8^7,zeta8^7);
    B=(zeta12^5,zeta12^5,-i); K=zeta24^13;
    H=zeta32^3*(1,i,-1,-i).

The matching pairs are the two H antipodal pairs and the two A objects
of twist zeta8^7. Conjugating all phases covers the opposite semion
orientation. The block proof was independently rederived by the root
agent and checked by the pair agent.

The block itself gives no contradiction. The two virtual fusion matrices
H0-H2 and H1-H3 reconstructed from it are integral. Section9 completes
this block to an explicit full modular datum and based fusion ring;
the categorical realization remains open.

## 7. The same reduction for pattern40

Pattern40 has nine A objects and no K. The exact first-twist equation
is the same, with four A objects of phase936 in place of the K contribution.
The complete square-orbit domain is reconstructed by a meet-in-the-middle
enumeration of mu24 singleton sums, with complete zero-sum square orbits
filling the remaining multiplicity. There are32 A allocations for each
of t60,t84 and120 for t96, in the earlier modulo144 notation for t.

The finite necessary conditions reduce this domain as follows:

| Constraint | Remaining phase allocations |
|---|---:|
| Three-W Vafa equations |174|
| Second indicator of W |12|
| Fourth indicator of W |2|

The two remaining phases differ only in the H quartet. In modulo1728
notation both have

    E=F1152; A=(288,288,864,936,936,936,936,1512,1512);
    B=(720,720,1296); H starts162 or378 with steps432.

There are5427 integral-projection matchings. For each phase, three-C Vafa
leaves1347, the second C indicator leaves85, and the third leaves9. These
nine consist of both antipodal H pairs and one outside equal-twist pair:
the A288 pair, the A1512 pair, one of the six A936 pairs, or the B720 pair.
The six-dimensional STS argument of section6 eliminates the H378 branch
and forces the A1512 pair in the H162 branch. Thus pattern40 also has one
remaining twist multiset and matching, up to relabeling indistinguishable
objects. The exact exponent check is verify_six_dimensional_block.py.

The two surviving patterns now differ in a single dimension/twist fiber:
pattern40 has four objects of dimension(14,10,8,6) and twist zeta24^13;
pattern186 has one object of twice that dimension and the same twist.
This observation is not a condensation construction or a claimed relation
between hypothetical categories.

## 8. Pattern40 is excluded by signed Galois symmetry

Remove the six-dimensional modular block of section6 and the forced
semion representation on e=(B0+B1+B2+B3)/2 and W. The remaining representation
has rank15 in pattern40 and rank12 in pattern186. With gamma=zeta24 and
linear T=theta/gamma, its exponent multiplicities are

    23:2, 15:2, 3:2, 11:1, 20:1, 9:2, 17:1, 12:m,

where m=4 for40 and m=1 for186.

This representation factors through SL2(Z/24). One elementary way to see
this, starting from the known conductor96 representation, is CRT. On the
SL2(Z/32) factor, T24 has cube T8. The kernel of reduction32 to8 is the
additive trace-zero matrix space I+8 sl2(Z/4). Conjugates of the upper
unipotent T8 generate its upper, lower and diagonal directions. Since T24
acts trivially on this complementary representation, the entire kernel
acts trivially. The SL2(Z/3) factor is unchanged.

The complete, exactly verified character tables of SL2(Z/8) and SL2(Z/3)
give210 product irreducibles. All four decompositions of the pattern40
spectrum contain three copies of the sign character, on which S=T=-1.
The companion level24 proof verifies the tables, considers both signs of
the central element, and independently checks this forced multiplicity
by two linear identities on the irreducible spectra.

The three-dimensional sign subspace lies in the four-dimensional T=-1
eigenspace, precisely the four A objects of twist zeta24^13. If v is in
this sign subspace, the unit entry of S v=-v gives sum(v_j)=0, because all
four normalized dimensions equal1/(4sqrt3). The sign subspace is therefore
exactly their three-dimensional zero-sum space V.

Choose a cyclotomic Galois automorphism with exponent5, which reverses
sqrt3. It preserves the four-object fiber and has common Galois sign -1
there. Since S acts as the rational matrix -I on V, Galois symmetry forces
the underlying four-point permutation to act as -I on V. Its total trace
would be 1-3=-2, impossible for a permutation matrix. Pattern40 is excluded.

The complete finite proof is ../r155/level24/R928_PATTERN40_OBSTRUCTION.md;
its verifier is verify_r928_pattern40.py. The separate audit is
../unified/audit_r928_pattern40.md. This is a pattern exclusion, not an
exclusion of R928 itself.

## 9. An explicit complete modular datum for pattern186

The remaining rank-20 case has an exact full S matrix. Beyond the forced
six-dimensional and semion blocks, its representation decomposes into
blocks of dimensions4,6,2. Convenient real matrices for the first two are

    S4 = 1/sqrt6 *
      [-1, sqrt2, sqrt2, 1;
        sqrt2, 1, 1, -sqrt2;
        sqrt2, 1, -1, sqrt2;
        1, -sqrt2, sqrt2, 1],

    S6 = 1/sqrt12 *
      [-1, sqrt2, sqrt2, 1, sqrt2, 2;
       sqrt2, 1, 1, -sqrt2, -2, sqrt2;
       sqrt2, 1, 1, -sqrt2, 2, -sqrt2;
       1, -sqrt2, -sqrt2, -1, sqrt2, 2;
       sqrt2, -2, 2, sqrt2, 0, 0;
       2, sqrt2, -sqrt2, 2, 0, 0].

Their linear T exponents modulo24, in these orders, are(23,15,9,17) and
(23,15,3,11,20,12). The final two-dimensional block is minus a semion
matrix up to a sign change of one basis vector, with T exponents(3,9).
The exact embeddings of these blocks into the twenty simple labels are
specified in verify_modular_data.py. They use the sum/difference bases
of the equal-dimension, equal-twist pairs. The verifier constructs S
entirely from these exact radical expressions; no floating point enters
the verification or exported datum.

The explicit witness passes:

* symmetry of S, S squared equal to the identity, and the exact STS identity;
* the prescribed positive dimension row and all8000 Verlinde identities;
* nonnegative integral fusion coefficients, the unit and self-dual basis;
* all160000 Anderson--Moore--Vafa equations;
* simplicity of the resulting based ring;
* all twenty second indicators equal1, and all third indicators with
  nonnegative integral trivalent rotation multiplicities.

The independent audit also reconstructs the field arithmetic, checks all
integer associativity equations, all balancing equations, and the fourth
indicators. Separate finite checks record all-simple indicators through
order12 and prime-order rotation multiplicities. Passing these conditions
is not a construction of associators or a category.

The exact S,T data are in rank-20_modular_data.json, and the full based
multiplication tensor is in rank-20_fusion_tensor.json. These are additional
necessary-data witnesses, not a new model counted by the project.

## 10. Scope and remaining problem

Patterns40,49,191 are excluded. Pattern186 is the sole retained center
pattern. It now has an explicit complete modular datum and a simple
rank-20 based ring. No claim of categorical realization follows from that
datum, nor is the required connected etale algebra constructed.

The full S witness uses the positive-central representation branch.
The construction is directly verified; a categorical uniqueness assertion
is not needed or made. Simultaneous complex conjugation covers the other
semion orientation.

A tempting known construction has the same dimension: dim(B) equals
dim(SU(3)_21)/9. Its standard central-C3 local quotient, however, has
rank31, not20: its85 triality-zero weights give28 free three-element
orbits and the fixed weight(7,7), which splits into three simples.
The E21 neutral rank-eight category is already the known case R8_3_982.
These dimension coincidences therefore do not supply a model for R928.

All calculations use small finite exact domains. No optimizer, pentagon
search, or unbounded enumeration is used. The new arguments and arithmetic
have separate agent audits. Independent human verification remains pending.
The inherited general-complex existence reduction and complete original
four-pattern derivation remain essential premises; numerical or exact
matrix checks do not prove those earlier categorical theorems.

## Primary dependencies

* Dong--Lin--Ng, Congruence property in conformal field theory,
  https://arxiv.org/abs/1201.6644 (normalized modular Galois identities).
* Bruillard--Ng--Rowell--Wang, Rank-finiteness for modular categories,
  https://arxiv.org/abs/1310.7050 (Cauchy theorem).
* Ng--Schauenburg, Frobenius--Schur Indicators and Exponents of Spherical
  Categories, https://arxiv.org/abs/math/0601012 (modular higher indicators).
* Anderson--Moore--Vafa determinant identity; the explicit formulation is
  reproduced in Etingof's notes https://math.mit.edu/~etingof/langsem.pdf.

The self-contained finite replay is `verify_phase_reduction.py`; it uses only
the Python standard library and regenerates all ten A/K allocations and
all312 H quartets, rather than assuming the displayed lists. The first two
pattern exclusions have the separate independent row-norm verifier.
The accepted general-complex gate and complete four-pattern derivation
remain inherited dependencies. Exact arithmetic does not prove them.


## Exact identification in The Anyon Atlas

The rank-20 modular datum is the existing record [B20-02148](https://anyonatlas.org/data/B20-02148), Galois orbit 20.167. This identifies the proposed factor B, not the full center Sem times B. A safe exact cyclotomic comparison checks all 400 S entries, 20 twists and 8000 fusion coefficients under the project-to-Atlas permutation recorded in atlas/atlas_match_receipt.json. The normalization is S_Atlas=L S_project, L=D/sqrt2. No novelty of the modular datum is claimed.

On 29 October 2026 the Atlas labels it Not CS and its Known Categorifiable selector does not include it. Its displayed possible algebra 1+X7+X11+X18, of dimension D/2, may condense to semion B02-00007; the export does not guarantee this algebra. Those data are not an algebra or categorical construction. R928 remains unresolved.

Run python r928/atlas/verify_match.py from the current proof root, or run the bundled combined checker. Source: the exact JSON export from the public record, accessed 29 October 2026; hashes and the explicit permutation are in the receipt.
