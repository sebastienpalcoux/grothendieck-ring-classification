# Structural exclusions for the rank-eleven multiplicity-one census

Every accepted exclusion here rules out a fusion category over the complex
numbers. No pivotal, spherical, braided, or unitary structure is assumed unless
its existence is proved as an intermediate consequence. The supplied physical
line numbers, R11_1_1 through R11_1_182, are permanent identifiers. Each receipt
binds to SHA-256 of compact JSON for the tensor in its original basis.

These are applications of literature criteria and lower-rank project theorems.
In particular, the involution-module construction already applies to
noncommutative fusion rings in the accepted lower-rank proof. Its rank-eleven
implementation is not a claim of a new categorical theorem.

## Accepted evidence

| Evidence file | Excluded inputs in that file | Exact replay |
|---|---:|---|
| `baseline.json` | 11 | `verify_baseline.py` |
| `zero_spectrum.json` | 29 | `verify_baseline.py` |
| `one_spectrum.json` | 29 | `verify_baseline.py` |
| `module_exclusions_verified.json` | 36 | `verify_modules_independent.py` |
| `noncomm_exclusions_verified.json` | 21 | `verify_noncomm_independent.py` |
| `inherited_solvability.json` | 6 | `inherited_solvability.py` |

These counts overlap and must not be added. The baseline and spectrum files
have 34 distinct exclusions. The commutative module receipt deliberately
contains only the 36 cases newly decisive after the arithmetic, baseline, and
spectrum criteria. The noncommutative receipt contains all 21 independently
replayed cases; seven are newly decisive at that stage. The parent ledger
combines these with the arithmetic and other theory/model evidence.

An exploratory search that finds no contradiction yields no conclusion.
In particular, a matrix solution is not a model, and a search budget stop is
not an exclusion. Files `modules.json`, `noncomm_modules.json`, and `morita179_*`
are discovery records rather than required accepted certificates. R11_1_179
passes the module and Morita constraints and has a separately constructed
positive model; it is not excluded by any result here.

## Complete based-subring inventory and direct transfer

A subset of the basis containing the unit and closed under products and duals
would span a full fusion subcategory of any hypothetical realization.
Consequently an obstruction to that subring is an obstruction to the whole
ring. This implication uses an explicit obstruction, never absence from a
positive model catalogue.

`baseline.json` inventories all 919 proper, nontrivial, product- and dual-closed
based subrings of the 182 inputs. Their 33 based-isomorphism classes are
represented by explicit tensors. Each occurrence records its subset and an
actual basis bijection. The portable verifier independently enumerates all
nonempty proper subsets and checks every coefficient in every class map.
The unit-only subring is omitted because it is always realized by Vec.

Ten inputs contain directly excluded subrings. For six, a Casimir factor is
`t^2-34t+272`; the d-number divisibility condition fails since
`34^2 mod 272 = 68`. For four, the subring is integral of dimension 30 and has
formal codegree 20, so its central induction constituent would have dimension
`30/20=3/2`. An integral fusion category is pseudo-unitary, and its center is
integral because forgetting a central object gives a sum of objects of integral
FP dimension. Thus this constituent is impossible.

More generally, the Casimir matrix `C=sum_i N_i N_i^T` has eigenvalue `e*f_E`
on a simple representation of dimension `e`, where `f_E` is its formal
codegree. Formal codegrees are d-numbers and multiplying by a nonzero rational
integer preserves that property. The irreducible monic polynomial
`t^d+a_1 t^(d-1)+...+a_d` of a d-number satisfies `a_d^j | a_j^d` for every `j`.
This test does not need commutativity. The four central-induction applications
are checked to be commutative; then `e=1` and the Casimir eigenvalues are the
ordinary formal codegrees.

References: Ostrik, *On formal codegrees of fusion categories*,
[arXiv:0810.3242](https://arxiv.org/abs/0810.3242), Theorem 1.2 and Lemmas 2.6–2.7;
Ostrik, *Pivotal fusion categories of rank 3*,
[arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Theorem 2.13;
Etingof–Nikshych–Ostrik, *On fusion categories*,
[arXiv:math/0203060](https://arxiv.org/abs/math/0203060), Proposition 8.24.

The eleventh baseline case, R11_1_172, is the near-group ring with ten
invertibles and one object of dimension `d=(1+sqrt(41))/2`, satisfying
`d^2=10+d`. Its global dimension is `20+d` and 10 is a formal codegree. A
categorification with precisely the two FP dimensions 1 and d has a
pseudo-unitary Galois conjugate, by Schopieray, *Categorification of integral
group rings extended by one dimension*,
[arXiv:2208.07319](https://arxiv.org/abs/2208.07319), Lemma 3.1. In that category
the central constituent has dimension `(20+d)/10=2+d/10`, which is not in
`Z+Z*d` and therefore cannot be the dimension of its forgetful image. The
portable verifier checks this particular quadratic witness directly.

## Zero and one spectrum

The zero-spectrum and one-spectrum obstructions are finite consequences of the
pentagon equation and invertibility of associativity maps. They are valid for
arbitrary complex fusion categories. We use Liu–Palcoux–Ren–Vercleyen,
*Triangular Prism Equations and Categorification*,
[arXiv:2203.06522v5](https://arxiv.org/pdf/2203.06522v5), Theorems 6.7–6.8.
The one-spectrum equations are (6.13)–(6.18).

The saved witnesses contain respectively nine and ten basis indices. The
portable replay evaluates all six boundary multiplicities, the spectrum sum,
the distinguished multiplicity, and the required scalar one-dimensionality
conditions directly as integers. It imports no search implementation and
requires no compiler. Each search originally used the pinned lower-rank C++
implementation with sufficient array capacity, and its source hash remains in
the discovery receipt. That C++ source is not a replay dependency.

## Involution-module obstruction, including noncommutative rings

Let g be an invertible object of order two in a hypothetical category C, and
let `J={x_a : x_a tensor g = x_a}` be nonempty. A fixed simple gives a rank-one
module category over the pointed subcategory generated by g. Therefore its
C2 associator class is trivial. The connected separable algebra `A=1+g`
exists; no braiding or central lift of g is needed.

Every fixed simple x_a has two simple right A-module structures, denoted
`m_a^+` and `m_a^-`, with underlying object x_a. A free right g-orbit gives
one simple A-module whose underlying object is the sum of the two orbit
members. This follows equivalently from the endomorphism algebra of the free
module: it has dimension two in the fixed case and dimension one in the free
case. The twisted group algebra of C2 splits over C.

Twisting the right A-action by the algebra automorphism that sends g to -g
exchanges the two fixed lifts and fixes the free-orbit module. This twist
commutes with left tensoring by every object of C, even when C is
noncommutative. The anti-invariant Grothendieck group has basis
`v_a=[m_a^+]-[m_a^-]`.

Use row vectors for coefficients of left tensoring and write T_i for its
matrix on this basis. Put `B_i(a,b)=N_{i,x_a}^{x_b}`. The sum and difference
of the two lift multiplicities give

    |T_i(a,b)| <= B_i(a,b),
    T_i(a,b) = B_i(a,b) mod 2.

Frobenius adjunction gives `T_(i*)=T_i^T`; all basis differences have the same
squared norm two, so no weights appear. The unit gives `T_0=I`. Because the
matrices use row vectors for a left action, the fusion relation is

    T_i T_j = sum_k N_(j,i)^k T_k.

This reversal matters for a noncommutative ring. A word `i_1 ... i_r` in the
ring must be evaluated as `T_(i_r) ... T_(i_1)`. The fixed objects must be
right-fixed, and distinct generator matrices are not required to commute.
These are exactly the noncommutative changes in `legacy_noncomm_module.py`.

For multiplicity one, every nonzero B entry allows exactly +1 and -1; a zero
entry forces zero. For each generator we enumerate the entire finite domain,
retaining symmetric candidates when that generator is self-dual. An exact
rational basis of generator words reconstructs every T_i from the chosen
matrices. All bounds, parity, transpose identities, and every fusion product
are then tested. If no tuple survives this complete finite search, the
necessary module does not exist and C cannot exist.

The accepted replay is independent of the sign-gauge reduction used during
discovery. It enumerates all ungauged generator tuples. The rational basis
routine uses a finite-field independence accelerator, but checks the returned
inverse over Q. Failure to find a basis cannot produce an exclusion. All
accepted receipts have three fixed simples, so the domain is finite and small
enough for complete replay. The stored generator set, candidate counts and
number of tested tuples must agree exactly with the fresh result.

The categorical construction already appears in the project's accepted
rank-six and rank-eight work. A verbatim predecessor is retained as
`prior_evidence/ANTI_MODULE_EIGHT_GENERAL_PROOF.md`; it explicitly states that
commutativity of the whole ring is unnecessary. Pointed module categories and
the cyclic algebra construction also appear in Etingof–Gelaki–Ostrik,
*Classification of fusion categories of dimension pq*,
[arXiv:math/0304194](https://arxiv.org/abs/math/0304194), Lemmas 6.1–6.2.
A separate current review is `../criteria_audit/NONCOMM_MODULE_REVIEW.md`.

## Inherited accepted solvability exclusion

R11_1_117, 118, 156, 160, 161 and 163 contain a based copy of the already
excluded ring R8_1_29. The accepted lower-rank proof handles arbitrary complex
categorifications, not just group-theoretical candidate models. Its dimension
is 24, the invertible group is C6, its two dimension-three simples are
self-dual, and its universal grading is trivial. Solvability forces a final
C2 or C3 equivariantization. The proof exhausts both prime branches, retaining
arbitrary associators in the pointed de-equivariantizations.

The original proof, source tensor and finite-hypothesis verifier are retained
byte for byte under `prior_evidence/`. Their SHA-256 hashes match the accepted
receipt. `inherited_solvability.py` first replays the source verifier and then
checks each explicit embedding, all 512 product coefficients, and dual/product
closure. The mathematical exhaustion is in `prior_evidence/solvable_proofs.tex`;
finite checks alone are not claimed to replace that proof. The proof includes
its literature citations, especially ENO solvability and equivariantization.

## Portable replay and dependencies

Run from the workspace root:

```sh
python work/rank11/structural/verify_baseline.py
python work/rank11/structural/verify_modules_independent.py
python work/rank11/structural/verify_noncomm_independent.py
python work/rank11/structural/inherited_solvability.py
```

Only Python, SymPy, the accepted files listed in `dependencies.json`, and the
original rank-eleven gzip are required. The directory can be relocated intact
by setting `RANK11_SOURCE` to the absolute source-gzip path. The default input
is `repositories/fusion-ring-census/results/rank11/tables.txt.gz` relative to
the original workspace root. No old working directory, compiled executable,
positive model catalogue, network access, or exploratory file is required.

Checks use explicit exceptions, not Python assert. The same commands are valid
under `python -O`. Baseline plus all subring embeddings takes about 1.3 seconds;
the 36 commutative module exclusions about 10 seconds; the 21 noncommutative
module exclusions about 325 seconds; inherited solvability less than one
second. Replays write separate `*_replay.json` receipts and leave the accepted
certificate files unchanged.
