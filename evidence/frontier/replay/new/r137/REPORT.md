# R9_2_137: full restriction Galois orbits and fourth-rotation bounds

29 October 2026. **R9_2_137 remains unresolved.** No model or general
exclusion is established in this investigation. Both TY signs still admit
exact nonnegative rational witnesses for a strictly stronger necessary
center system. These witnesses are not categories or modular data.

The investigation adds three theoretical restrictions to the accepted
27 October frontier. The previous forced nonpointed algebra gives only
the already-known central-involution Morita context; it is not counted
again as a construction.

## 1. Galois automorphisms preserve full restriction columns

**Lemma.** Let C be pseudo-unitary with commutative Grothendieck ring, and
let K contain its full character table and its global dimension D. Let
v_Z be the restriction column of a simple Z in Z(C). Every modular Galois
automorphism sigma fixing K preserves v_Z.

**Proof.** For each irreducible character chi_E of K0(C), the corresponding
distinguished object A_E in I(1) satisfies dim A_E=D/f_E. Write s=S/D for
the normalized center matrix. The central-character identity gives

    s(A_E,Z) = chi_E(FZ)/f_E.

All these entries lie in K. The modular Galois rule on columns is
sigma(s(A_E,Z))=epsilon_sigma(Z) s(A_E,pi_sigma(Z)). The unit row is
dim(Z)/D; it belongs to K and is positive, as is the permuted entry.
Therefore epsilon_sigma(Z)=+1 and dim(pi_sigma(Z))=dim(Z). The remaining
distinguished rows now give equal values of every chi_E on FZ and
F(pi_sigma(Z)). The complete character table separates elements of the
commutative semisimple ring. Hence their entire restriction columns agree.
The convention using pi_sigma inverse instead yields the same orbits.

For a center the canonical anomaly-one normalization has T=theta. If
sigma sends roots of unity to their a-th powers, its label permutation
satisfies theta_(pi_sigma Z)=theta_Z^(a^2). Thus if the square-Galois orbit
of theta_Z under automorphisms fixing K has size k, there are at least k
distinct simples with the same column v_Z. The induction Gram matrix G
therefore obeys

    k v_Z v_Z^t <= G,
    or equivalently k v_Z^t G^(-1) v_Z <= 1.

The inequality is positive-semidefinite. It is stronger than comparing
only dimensions of Galois partners.

The same proof extends to a noncommutative source ring if K contains every
irreducible character value: insert the degree factor dim(E) in the
denominator. Each FZ is central in K0(C), and irreducible central characters
separate that center. The R137 calculation uses only the commutative case.

For R137 every character lies in K=Q(sqrt(2)). This was checked exactly
against the complete nine-character table, not inferred from FP dimensions
alone. In the standard census basis its Gram matrix is

    9 1 3  8  8  8  8 3  0
    1 9 3  8  8  8  8 3  0
    3 3 9  8  8  8  8 1  0
    8 8 8 76 64 64 68 8 16
    8 8 8 64 76 68 64 8 16
    8 8 8 64 68 76 64 8 16
    8 8 8 68 64 64 76 8 16
    3 3 1  8  8  8  8 9  0
    0 0 0 16 16 16 16 0 16.

For example, every primitive ninth-root sector has orbit length at least
three, with the SAME restriction column in all three positions. The
height-four joint trace type that is zero at all four moments also has
minimum orbit length three (attained at order144). Orders beyond the
finite moment box 2^5*3^2 have zero first-four traces; their square-Galois
orbits have size at least four in the 2-primary direction or nine in the
3-primary direction. Thus no truncation of root orders is being assumed.

This lemma is an additional condition, not a proof that every old column
violating it occurred in an actual center. It was applied as a necessary
filter to the old center relaxation.

Primary inputs: Deshpande, *On centers of bimodule categories and
induction-restriction functors*, Proposition2.8 and Section4.3,
https://arxiv.org/abs/1611.04486; Ostrik, *Pivotal fusion categories of
rank3*, Theorem2.13, https://arxiv.org/abs/1309.4822; Dong–Lin–Ng, *Congruence Property In Conformal Field Theory*, Lemma4.2
(the canonical center normalization and its squared-twist rule),
https://msp.org/ant/2015/9-9/ant-v9-n9-p03-s.pdf.

## 2. A sharp fourth-indicator restriction

Let X be any of the four large simples of R137 in the necessary positive
representative. The accepted source-local anticommutation theorem supplies
four cyclic pair-insertion involutions on V=Hom(1,X^4). Adjacent
involutions anticommute; opposite ones commute. Fourth pivotal rotation E
permutes them cyclically and satisfies E^4=1.

The four-cycle insertion algebra has two blocks fixed by rotation and one
exchanged pair. The fixed-block cyclic spectra, up to fourth-root shifts,
are {1,-1} and {1,-i}; the exchanged pair has the four regular eigenvalues.
This is the n=4 instance of the previously proved even-cycle theorem.
For character accounting, the regular spectrum is the sum of two adjacent
pairs. Thus every cyclic spectrum is a sum of opposite pairs {lambda,-lambda}
and adjacent pairs {lambda,i lambda}, with lambda a fourth root.

Exact tensor multiplication gives

    dim V=18,
    X^2=1+h+2 sum_(four large Y) Y.

The forced second indicators of all four Y and h are +1. Grouping four
strands into two pairs gives

    tr(E^2)=nu_2(X^2)=10.

Let a_+,a_- count opposite pairs with squared eigenvalue +1,-1 and let b
count adjacent pairs. Then

    a_+ + a_- + b = 9,
    2(a_+-a_-)=10,
    b=4-2a_- <=4.

Only adjacent pairs contribute to tr(E); each contributes a number with
real and imaginary parts both equal to +/-1. Consequently

    Re nu_4(X), Im nu_4(X) belong to {-4,-2,0,2,4}.

In particular the normalized trace to Q(sqrt2) has only those five real
values. This is considerably narrower than the ordinary cyclic bound14.
No claim that nu_4 itself must be real is made.

The argument uses the established positive-FS2 theorem, the actual
anticommuting stabilizers, and pivotal rotation, not numerical indicator
preservation under a forgetful tensor functor.

## 3. A center with no hidden tensor factors

The source ring has exactly the proper fusion subcategories inside its
integral TY subcategory: each nonintegral simple generates the whole
source ring. The accepted theorem says that Z(C)_int is Vec or sVec.
Furthermore C cannot be braided: a braiding would lift all four distinct
source invertibles to the center, which has at most two invertibles.

Any nonintegral fusion subcategory K of Z(C) therefore forgets dominantly
onto C. It has FP dimension strictly greater than D: equality would make
the restriction of the forgetful tensor functor an equivalence, supplying
a braiding on C. If K and its centralizer K' were both nonintegral, the
product of their dimensions would exceed D^2, contrary to the modular
centralizer formula. Hence K' is contained in Z(C)_int.

It follows by double centralization that:

* if Z(C)_int=Vec, then Z(C) is simple;
* if Z(C)_int=sVec generated by f, the entire subcategory lattice is
  Vec, sVec, f', Z(C). The fermion centralizer f' is s-simple and nonsplit.

The nonsplitting follows because a decomposition f'=M tensor sVec would
supply a proper nonintegral fusion subcategory M distinct from f' and
Z(C). In either case the center has no nontrivial nondegenerate tensor
factor. Consequently no realization whose center decomposes nontrivially
as a Deligne tensor product can be Morita equivalent to R137.

This is a construction-family exclusion, not an exclusion of R137.
The modular centralizer theorem is DGNO, *On braided fusion categoriesI*,
https://arxiv.org/abs/0906.0620. The tensor-functor dimension argument is
standard fusion-category dimension theory.

## 4. Short exact experiment and its result

The original frozen height-four systems include the complete induction
Gram, codegrees, dimension Galois closure, low-character S symmetry,
integral-center restriction, TY eighth-root spectrum, source-local cubic
Clifford constraints, and forced positive second indicators. The new
filter removes 6,716 (column,trace-type) variables from EACH system.

The full restriction columns and trace types were matched to original
variables using every inherited base-system row. No arbitrary numerical
matching or dimension-only substitution was used. Original equations are
unchanged. The quartic bounds were added, and then all four projected
fourth indicators were set to the admissible value2 as a test branch.

| TY sign | Original variables | Orbit columns removed | Exact witness support after orbit and discrete quartic constraints |
|---|---:|---:|---:|
| + |22231|6716|117|
| - |21984|6716|119|

The short solver only proposed support. Each witness was reconstructed
with rational row reduction and checked against EVERY equation exactly,
with nonnegative coefficients and no removed columns. Thus both signs
still pass this stronger NECESSARY relaxation. These are projected
indicator systems: neither a full unprojected spectrum nor an actual
modular category is constructed.

Scripts and receipts are local in this directory. No repository or
website revision was made. Independent human verification remains pending.

## 5. Additional subtraction of the two forced central simples

The same normalized Galois-unit argument already used in the project
forces the source restriction

    F(B)=1+X3+X4+X5+X6,   dim B=17+12 sqrt2.

Indeed the six other non-FP character values on the sum of the four large
simples vanish, as does the remaining rational character; the two FP
characters give the required ratios D/D' and D'/D. Every other formal
codegree is rational. The complete nine-character check confirms this.
Both B and the unit are distinct central simples. Consequently an orbit
of a high column satisfies the stronger bound

    k vv^t <= H=G-e0 e0^t-vB vB^t.

The residual matrix H has rank9 and determinant6849298432. The additional
screen also deletes any B-labelled low column other than vB. In total
this deletes7,222 original variables for each TY sign (506 more than the
first filter). Both systems STILL have exact nonnegative rational
witnesses with all four projected fourth indicators2: supports102 and112
for the positive and negative signs respectively. Every inherited
condition and all12 newly added equations were checked exactly.

The first filter and its117/119 witnesses are retained as an independently
auditable intermediate result. The stronger result has its own receipts
and frozen exports; no failed search is presented as a proof.

## Replay

Run `python verify_structural.py` and either
`python orbit_discrete_screen.py --verify` or
`python forced_galois_screen.py --verify` from this directory. The latter
two use the inherited sources and input systems in `../../prior`; they
import SymPy, python-flint, NumPy and SciPy, but their verify branch does
not call an optimizer. Both signs replay264 equations each. The frozen
`R137_tau_*_orbit_quartic_replay.json.gz` and
`R137_tau_*_forced_galois_replay.json.gz` contain full exact matrices,
witnesses and variable metadata for independent standard-library checks.
The structural verifier needs only the Python standard library. Input
bindings are in `receipt.json`.
