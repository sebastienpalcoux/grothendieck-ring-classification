# R65: the trivial pointed-associator branch is impossible

This is a structural refinement of the algebra/module analysis, not an
exclusion of R65 itself. It uses two previously accepted repository results
explicitly: the unrestricted rank-four dimension bound and the general
exclusion of the exact tensor `R8_3_1453`. Their source hashes are pinned in
`pointed_dual.json`.

**Proposition.** In any complex fusion category with Grothendieck ring
`R8_3_65`, the associator class of its pointed subcategory
`Vec_(C4)^omega` is nonzero. Consequently neither of the two rank-two based
module actions admits a categorical module realization over such a category.

The finite Gram/profile analysis in `README.md` leaves six possible based
module actions. This proposition removes the two rank-two actions
categorically. Their four underlying connected-algebra candidates have saved
indices `18,21,26,29`. The remaining R65 list has eight algebra objects, eight
induction factors, and four possible categorical module actions, of ranks
`4,4,8,8`. Across the four quadratic rings, the resulting totals are **144
algebra objects, 178 induction factors, and 30 fully determined action
classes**. The original 148/182/32 arithmetic-stage counts remain preserved in
the earlier receipts so that the categorical deduction has a distinct source.

## The noncentral subgroup dual

Let `g` generate the pointed C4 and let `H=<g^2>`. Suppose omega is trivial.
Then the actual subgroup algebra `A=1+g^2` exists. This algebra is not assumed
central, commutative in a braiding, or Tannakian.

There are four simple right A-modules, one for each right H-orbit of source
simples. The two pointed orbits and two noninvertible orbits all have length
two. Left tensoring by H fixes each right-module isomorphism class, because
the source multiplication is commutative. Each fixed simple has two distinct
left H-linearizations: the possible projective multiplier is trivializable
since `H^2(C2,C*)=0`. Thus the dual fusion category
`B=A-bimod(C)` has eight simple objects. Four have dimension one and four have

`d=(11+5 sqrt(5))/2`, with `d^2=1+11d`.

The four invertible bimodules are entirely inside the original pointed
subcategory. In untwisted `Vec_(C4)`, an invertible A-bimodule is specified by a
coset `xH` and a character `chi` of H. Take a basis in degrees `xh`, give it
the regular right H-action, and multiply the left H-action by chi. Tensoring
over A multiplies the characters and cosets. Therefore the group of these
four invertibles is

`H^hat x (C4/H) = C2 x C2 = V4`.

This does **not** assert a trivial associator on the dual pointed subcategory.
The nontrivial character changes the two linearizations of each fixed
right-module simple, while the nontrivial coset interchanges the two
noninvertible right-module orbits. Hence the four noninvertibles in B form a
free transitive V4-orbit.

## Complete reduction of the possible dual fusion rules

We give the argument for either abelian group G of order four; only V4 is
needed for the contradiction. Choose a noninvertible rho. Right multiplication
by G on its free left G-orbit has the form

`rho g = phi(g) rho`

for an automorphism phi of G. The product rho^2 has a unique invertible
summand u: this follows from the free action and Frobenius reciprocity. Write

`rho^2 = u + (sum_h n_h h) rho`, with `sum_h n_h=11`.

Comparing the invertible and noninvertible terms in `rho^2 g=rho(rho g)` shows
`phi^2=1` and that the coefficient function n is invariant under the subgroup
`{g phi(g)^(-1):g in G}`. If phi is nontrivial, this subgroup has order two for
either C4 or V4. Its cosets would make the total 11 even. Therefore phi is the
identity and the fusion ring is commutative.

The duality relation gives `rho*=u^(-1)rho` and
`n_h=n_(u h^(-1))`. This involution of G has an odd total coefficient sum, so
it has a fixed point h with `h^2=u`. Replacing rho by `h^(-1)rho` gives a
self-dual rho with

`rho^2=1+N rho`, `N=N*`, `sum n_h=11`.

For V4, changing rho by a group translate and applying a group automorphism
permutes the four coefficient positions as the full group
`AGL(2,2)=S4`. Thus every possible V4 dual ring is one of the **27 unordered
nonnegative partitions of 11 into four parts**. For C4, the corresponding
complete list is the 21 vectors `(a,b,c,b)` with `a+c+2b=11`, modulo exchanging
a and c. The finite program constructs every tensor and verifies the fusion
axioms exactly.

## Formal-codegree norm obstruction

All these rings have exactly two distinct Frobenius–Perron dimensions, 1 and
irrational d. Every categorification is Galois conjugate to a pseudo-unitary
one by Schopieray, *Categorification of integral group rings extended by one
dimension*, Lemma 3.1, DOI
[10.1112/jlms.12789](https://doi.org/10.1112/jlms.12789). This is the same
`two_FP_values` reduction used in the frozen `rank8_signed_bridge.py`.
It applies directly to B; no assumption about preservation of a chosen
spherical structure under Morita equivalence is needed.

For a group character chi put `m=chi(N)`. Here m is an odd integer. The two
extensions of chi have `rho`-values solving `x^2=1+m x`, and formal codegrees

`f=4(1+x^2)`.

Their quadratic trace and norm are

`Tr(f)=4(m^2+4)`, `Norm(f)=16(m^2+4)`.

The pseudo-unitary global dimension is

`D=4(1+d^2)=250+110 sqrt(5)`, `Norm(D)=2000`.

The dimensions of the corresponding distinguished simple summands in the
Drinfeld-center induction of the unit are `D/f`, so these quotients must be
algebraic integers. Taking the norm in the compositum of the two quadratic
fields shows that

`125/(m^2+4)`

is an integer. Indeed the compositum norm is this rational number or its
square, and a rational number whose positive integer power is an integer must
itself be an integer. Since m is odd and `|m|<=11`, necessarily

`|m|=1 or 11`.

This exact necessary norm test leaves just three V4 coefficient partitions:

| N coefficients | Remaining obstruction |
|---|---|
| `(0,0,0,11)` | A translate of rho generates a rank-two subring `rho^2=1+11rho`. |
| `(0,0,5,6)` | Two invertibles and two noninvertibles form a rank-four subring of dimension `125+55 sqrt(5)`. |
| `(2,3,3,3)` | The complete tensor is isomorphic to the previously excluded `R8_3_1453`. |

The first is impossible by Ostrik's general
[Fusion categories of rank 2](https://arxiv.org/abs/math/0203255) classification.
The second exceeds the unrestricted rank-four upper bound
`24+12 sqrt(3)` in the repository's
`manuscripts/rank4/papers/companion_sections/14_finite_certification.tex`,
Corollary `finite:cor:sharp-bounds`. The third is identified by an exact
512-coefficient based isomorphism and uses the accepted general exclusion in
`evidence/rank8_frontier_20261021/global_induction/results/R8_3_1453_h4.json`.
The program checks and records all three subring/isomorphism certificates.
The accepted R1453 proof is an input, not replaced by a numerical status flag
or a new bounded search.

Every possible dual ring is therefore impossible. This contradicts the
existence of B and proves omega is nonzero.

For comparison, the same finite norm calculation in the C4 family leaves
`(0,0,11,0)`, `(5,0,6,0)`, and `(2,3,3,3)`; the first two have the same lower-rank
obstructions, and the third is R65 itself. This explains the concrete role of
using the order-two subgroup dual: its invertible group is V4 under the
trivial-associator hypothesis.

## Consequences and remaining scope

In either rank-two based module, every invertible fixes every simple module.
Choosing the corresponding scalar module-associativity maps would produce a
two-cochain whose coboundary is omega. Thus any actual rank-two module category
would force omega=0, contrary to the proposition.

There is also a uniform cohomological refinement. Identify
`H^3(C4,C*)=Z/4` by the square of the first Chern class of a generating
character. Restriction to the subgroup C2 is reduction modulo two, because
that character restricts to the generating character of C2. In every rank-four
based action in our complete list, each simple has stabilizer C2. An actual
module category therefore trivializes omega on that stabilizer. Since the
zero class is excluded, **rank-four module categories require class 2**.
Categories with class 1 or 3 can have only the two rank-eight based actions.

Conversely, in class 2 the subgroup restriction is trivial, so the actual
algebra `1+g^2` exists. Its dual again has four invertibles and a free orbit of
four dimension-d simples. The group of four invertibles is either C4 or V4;
the exact two-family classification above excludes V4 and leaves only R65 in
the C4 case. Thus this conditional subgroup dual has **the same Grothendieck
ring R65**. The Morita module category has rank four also on the dual side, so
the dual pointed associator is class 2 as well. This is a conditional
Grothendieck-ring self-duality statement. It neither constructs a category
with R65 nor identifies the dual categorically with the original category.

We have not ruled out nonzero classes in `H^3(C4,C*)`, supplied an associator,
or excluded R65. In particular the two rank-four and two rank-eight necessary
based-module actions remain. The statement about four removed algebra
candidates uses the complete, unique induction factors already verified in
`integral_gram.json` and `profile_closure.json`.

Reproduce the finite algebraic certificate without modifying frozen inputs:

```sh
python evidence/rank8_next_20261021/quadratic/pointed_dual.py
python -O evidence/rank8_next_20261021/quadratic/pointed_dual.py
```

The theory of subgroup-algebra modules and duals is the standard module
category/bimodule construction in EGNO, *Tensor Categories*, Chapter 7.
All external and repository theorem dependencies have been stated explicitly.
