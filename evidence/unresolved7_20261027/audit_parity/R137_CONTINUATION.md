# R9_2_137: forced algebra, exact stronger indicator test, and their limits

**Status remains unresolved.** This pass supplies a categorical strengthening
of the formerly conditional algebra route and checks that the new positive
second indicators do not contradict the existing third-indicator systems.

## 1. The nonpointed algebra is forced

Work in the necessary pseudo-unitary, zero-shift rank-twelve Morita category
D. Put d=4+3sqrt(2), S=sum_q X_q and Delta=8+4d^2. Its pointed subcategory
P is Vec_D8^omega. DMNO Theorem 4.10 supplies a connected etale subalgebra
L of I_D(1) corresponding to P, with dimension

    dim L = Delta/8 = 2+4d.

The distinguished constituents of I_D(1) have dimensions 1, 1+4d,
six copies of 1+2d, and a constituent of dimension 4+8d occurring twice.
The unit occurs once. Comparing the coefficients of 1 and d shows that
the only possible underlying central object of L is 1+B, where B is the
Galois-unit simple. The exact restriction theorem gives

    F(L)=2+S.

The canonical algebra F(I_D(1)) has its algebra augmentation to1; restrict
it to F(L). Separability is preserved by F. In the semisimple category of
F(L)-bimodules, the augmentation splits. Its splitting gives a central
idempotent e with m(e,-)=m(-,e)=j epsilon. Thus the algebra F(L) is a
direct product of the unit algebra and a connected separable algebra A:

    F(L) = 1 x A,                 [A]=1+S.

This proves existence of A in every hypothetical category under discussion;
it is not an assertion that such a category exists.

The correspondence and dimension formula are DMNO,
https://arxiv.org/pdf/1009.2117, Theorem4.10. The canonical augmentation is
also explicitly described in Burciu, https://arxiv.org/pdf/2105.11202,
Section2.2, immediately after(2.6).

## 2. This algebra returns to the central-involution module category

The induction Gram matrix for A has the unique nonnegative integral factor

    [[I8,0],[J_(4,8),I4]].

Write M_g for the eight induced invertibles and N_q for the four residual
modules. Their underlying objects are

    U(M_g)=g+S,             U(N_q)=X_q.

These expressions force the complete action:

    g M_h=M_(gh),     g N_q=N_(q+gH),
    X_p N_q=sum_(gH=p+q) M_g,
    X_p M_g=sum_h M_h+N_(p+gH).

In particular the internal end of N_q is 1+z. Therefore D_A and
D_(1+z) are equivalent module categories. The central algebra argument
does not produce a new independent Morita route: it proves that the
previously conditional nonpointed algebra route is precisely the
central-involution route already available.

This prevents a false claim that the construction solves R137, or that
the rank-twelve module bound itself excludes the ring.

## 3. Both TY signs pass the strengthened short exact test

The previous projected center systems allowed the four large second
indicators to vary. The new symmetric Galois-unit theorem forces all four
to +1. I added those four exact equalities to each previously exported
height-four necessary system, retaining the full induction Gram,
distinguished labels, S symmetry, integral-center restrictions, TY spectrum,
and the surviving source-local Clifford assignment.

Both tests have exact nonnegative rational solutions:

| TY sign | Projected third indicators tested | Equations | Variables | Witness support |
|---|---|---:|---:|---:|
| + | (1/2,1/2,1/2,1/2) |252|22231|102|
| - | (-1,-1,-1,-1) |252|21984|97|

Each run, including the numerical proposal, exact rational reconstruction,
all-equation check and compressed export, took under four seconds. A
feasible necessary-system witness is not a categorical model. The result
only shows that these newly combined restrictions do not complete the
exclusion.

`check_r137_positive_fs2.py` records the experiment; its LP time limit is
15seconds per call. `verify_r137_positive_fs2.py` rechecks both exported
certificates using only exact rational arithmetic and the source-bound
hashes, without a solver. The two prior systems are unchanged frozen git
blobs; the receipt records their SHA256 hashes.

## 4. Other shortcuts explicitly rejected

Self-duality and second indicator +1 do not by themselves make higher
indicators real. Nor does a pointed associativity/duality cochain solve
the pentagons involving noninvertible multiplication. The remaining
relative-center coherence of B supplies no contradiction established in
this pass. No new model is claimed and no online record is changed.
