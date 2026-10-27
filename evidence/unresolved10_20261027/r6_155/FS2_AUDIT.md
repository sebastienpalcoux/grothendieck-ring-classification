# Independent pivotal / second-indicator audit for the rank-nine reduction

Date: 2026-10-27. This is a research audit, not an exclusion certificate.

**Later development:** `GALOIS_FROBENIUS_FS2_AUDIT.md` independently accepts
a different argument excluding R9_2_1607 and R9_2_1976, using the symmetric
Frobenius structure on the canonical center algebra. It does not use the
quadratic-refinement proposal or the exploratory cochain trials below.
The negative conclusions below concern that earlier approach alone.

## Conclusion

The suggested universal nondegenerate quadratic-refinement rule for the four
self-dual large objects has **not** been established. The available pointed
bimodule cochains allow both character-shaped and nondegenerate-quadratic-shaped
trial sign patterns. In particular, the zero-sum pattern required by
`R9_2_1976` is not eliminated by this argument. No new categorification or
exclusion status follows.

The distinction is important: the nondegenerate left/right pairing on the
order-two stabilizer proves invertibility of a pointed bimodule; it does not
by itself prove that the indicators on its four simple objects are a
nondegenerate quadratic refinement on the quotient group.

## A rigorous necessary constraint for R9_2_1976

Let C be its hypothetical pseudo-unitary representative, with the canonical
positive spherical structure. Its four large simples are two nontrivial dual
pairs, so their second indicators vanish. Its four invertibles have indicator
1 and its dimension-two Tambara--Yamagami object Y has indicator epsilon=-1.
Consequently

    sum_i dim(i) nu_2(i) = 4 + 2 epsilon = 2.

The weighted expression is a spherical Morita invariant in this setting:
the center-induction formula gives

    sum_i dim(i) nu_2(i)
      = (1/dim(C)) sum_{Z simple in Z(C)} dim(Z)^2 theta_Z^2.

A Morita equivalence preserves the center and its canonical positive pivotal
structure. In the D8 pointed dual, the pointed contribution is again
4+2 epsilon: the four elements in the even V4 have indicator 1, the two
odd involutions have indicator epsilon, and the two order-four rotations
have indicator zero. Thus, after excluding reflection duality shift and
retaining zero shift, its four self-dual large objects necessarily satisfy

    sum_{q in D8/<z>} nu_2(X_q) = 0.

This establishes the proposed contradiction's first half. Its second half,
the claimed nonzero sum of signs, requires an additional theorem.

## Exact bridge from rigid duality to FS signs

The following elementary identity isolates precisely what must be computed.
It is valid in a pivotal fusion category without a unitarity assumption.

Work in a skeletal realization. Let D be the chosen left-dual functor, and
identify each self-dual simple X_q with D(X_q). A complex-linear contravariant
functor is the identity on scalar endomorphisms. The transposition on
Hom(X_q,D(X_q)) is

    f |-> D(f) j_{X_q}.

This one-dimensional map has trace j_{X_q}; hence

    nu_2(X_q) = j_{X_q} in {+1,-1}.

Let the dual tensorator have orientation

    f(U,V): D(U tensor V) --> D(V) tensor D(U).

When the tensor products in question are simple, denote its scalar by the
same letter. The tensorator of D^2 is

    J(U,V) = D(f(U,V)) / f(D(V),D(U)).

Since D is complex-linear, the numerator has the same scalar f(U,V).
Monoidality of the pivotal structure gives

    j_{U V} = J(U,V) j_U j_V.

Therefore, for an invertible g and self-dual X and gX,

    nu_2(gX)/nu_2(X)
       = j_g f(g,X)/f(X,g^{-1}).                    (1)

In the usual skeletal Vec_G^omega convention with ev_g=1 and
coev_g=omega(g,g^{-1},g)^{-1}, positive dimension fixes

    j_g=omega(g,g^{-1},g).

Formula (1) needs the **actual rigid dual tensorator**. An arbitrary
stabilizer coboundary witness is not automatically that tensorator.

References for the transposition and its agreement with the pivotal second
indicator: K. Shimizu, *Frobenius--Schur indicator for categories with
duality*, arXiv:1208.2433v2, equation (2.7), Definition 2.8 and Remark 2.13.
The double-dual tensorator identity above follows directly by applying the
contravariant functor twice; no extra classification theorem is used.

## Audit of the cochain normalization

The companion agent's `r9_noncommutative/probe_full_module.py` constructs the
full transitive module associator from the stabilizer cochain. Its acting
group is K=G x G, acting by (g,k)X=gXk^{-1}, with

    Omega=omega(first) / omega(second).

For the zero-shift classes beta+2 gamma_D16 and the two optional cross
two-cocycles, it verifies the full opposite-equivalence cochain equation
for eta. Its scalar tables are useful evidence, but identifying eta with
f in (1) needs care: the chosen right-action normalization already involves
duality in the pointed category.

I checked this with the smallest exact calibration example. Take the regular
bimodule of Vec_C2^omega, where omega(1,1,1)=-1, choose the diagonal
stabilizer and beta=u=0, and apply the same induced module-cochain formulas.
Then, in exponent notation modulo 8,

    eta((1,0),x)=0, eta((0,1),x)=4

for both x. The actual indicators of its two simples are [1,-1]. The
eta-difference alone gives this correctly, whereas adding a second pointed
j_g term gives the incorrect [1,1]. Thus eta cannot be substituted blindly
for the raw f in (1). The supplied companion script intentionally calls
these calculations `pivotaltrial` rather than asserting a theorem.

Both trial normalizations still give the same relevant warning. With
q ordered (00,10,01,11), the four cross-cocycle classes give:

| Cross class | eta-difference trial | Sum | Trial after another pointed factor | Sum |
|---|---|---:|---|---:|
| 00 | +,-,+,- | 0 | +,-,-,+ | 0 |
| 01 | +,-,+,+ | 2 | +,-,-,- | -2 |
| 10 | +,-,+,+ | 2 | +,-,-,- | -2 |
| 11 | +,-,+,- | 0 | +,-,-,+ | 0 |

An overall sign is immaterial for the distinction between zero and nonzero.
These tables do not construct a fusion category. They show why one cannot
infer a universal nondegenerate polar form from the present partial data.
An exclusion would need either a correct rigidity calculation ruling out
the zero-sum classes, or an independent categorical reason those two
cross-cocycle classes cannot occur.

**Additional witness-freedom caution.** The displayed script uses the first
coboundary witness u found. All other witnesses include u times a character
of L. Such characters can take independent signs on P and S and kill Z,
so they preserve u-u composed with swap=0. In the induced eta construction,
the left-p step from the basepoint has stabilizer element 1, whereas the
right-p step has stabilizer element diagonal P; the same holds for S.
Changing u by these characters therefore changes the trial q-sign pattern
by an arbitrary character of Q. In particular a character-shaped pattern
with sum zero can become the all-positive pattern. The displayed table is
not an exhaustive list of indicator patterns even at the trial level.
It cannot exclude R9_2_137 after the symmetric-Frobenius argument forces
all four indicators to be positive.

## A false alarm checked and withdrawn

There is no basepoint duality-square obstruction in the displayed witness.
The pure left stabilizer is h_L=(1,1,0,1), not (1,1,1,1), and the pure right
stabilizer is h_R=(0,0,0,1). Their u-values agree. The companion calculation
checks u-u composed with swap is zero on all 16 stabilizer elements for all
four zero-shift cross classes. An initial handwritten coordinate suggestion
using n=1 was immediately corrected and supplies no obstruction.

## Sources and scope

- K. Shimizu, arXiv:1208.2433v2,
  https://arxiv.org/abs/1208.2433.
- L. Vainerman and J.-M. Vallin, *On Z/2Z-extensions of pointed fusion
  categories*, arXiv:1210.1732, especially Sections 2.2.2 and 3.1.1 for the
  opposite-category convention used in the companion calculation,
  https://arxiv.org/abs/1210.1732.
- S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and exponents of
  spherical categories*, Adv. Math. 211 (2007), 34--71, for the
  center-induction formula.

This audit does not import an obstruction for a faithful Z2-graded extension:
the actual large-by-large products contain large simples, so such a grading
has not been constructed. It does not equate a consistent module cochain
with the existence of an ambient fusion category.
