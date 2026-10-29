# A general-complex exclusion of R8_3_1768

29 October 2026. **New result; the pairing lemma and its tensor application
have been independently audited by r155 and r1154:** the
previously forced second indicators contradict a necessary pairing parity
in the ordinary tensor products of the category itself. No new module
category or algebra-existence premise is needed.

## 1. Conjugation preserves the symmetry sign of a selfduality

Let C be a pivotal semisimple rigid C-linear category. Write
j_V:V->V** for the pivotal structure and

    f^t = f* j_V

for the pivotal transpose of f:V->V*. Suppose f is invertible and
f^t=epsilon f, epsilon in {+1,-1}. For any object X the object

    W = X tensor V tensor X*

has a nondegenerate selfduality of the same sign.

One can check this in a strict pivotal model: W*=X tensor V* tensor X*,
and the map

    h = id_X tensor f tensor id_(X*)

satisfies h^t=id_X tensor f^t tensor id_(X*)=epsilon h.
This calculation is independent of choices of bases, associators or a
braiding. Explicitly, in general notation take h=j_X tensor f tensor
id_(X*). Its transpose is

    h* j_W = j_X tensor (f* j_V) tensor (j_X* j_(X*))
           = epsilon h,

using j_(X*)=(j_X*)^(-1). Associativity and dual-tensor comparison maps
are suppressed by coherence. Equivalently,
the conjugation functor X(-)X* preserves the sign of the displayed
selfduality, although it is not in general strong monoidal.

If a selfdual simple S has second indicator delta, a nondegenerate
epsilon-selfduality on W restricts on its S-isotypic block to the fixed
delta-selfduality of S times a nondegenerate bilinear form on its
multiplicity space. Transposing gives symmetry sign epsilon/delta on
that vector space. Therefore

    epsilon != delta  =>  [X V X* : S] is even.                 (P)

This is a parity statement about multiplicities, not a claim that the
numerical second indicator is functorial. Nonselfdual constituents may
pair with their duals and do not enter (P).

## 2. Applying the lemma to the already forced R1768 signs

Assume a complex categorification of R8_3_1768 exists. The published
sphericalization/Galois existence reduction supplies a pseudo-unitary
categorification with the same tensor. In its canonical positive pivotal
structure, the complete saturated-conductor/indicator argument already
forces

    nu_2(X0)=1, nu_2(g=X1)=-1,
    nu_2(X2)=...=nu_2(X7)=1.

All eight simples are selfdual. The source tensor gives

    X2^2 = 1 + X2 + X3 + 2X4 + 2X5 + 2X6 + 2X7,
    gX2=X7, gX3=X6, gX4=X5,

with inverse pairings under g and g^2=1. The ring is commutative, so

    X2 g X2* = g + 2X2 + 2X3 + 2X4 + 2X5 + X6 + X7.          (1)

Apply (P) with X=X2 and V=g. The left side of (1) admits a
nondegenerate negative-sign selfduality. Both X6 and X7 have positive
second indicator and occur with multiplicity one. Either is a
contradiction. Therefore the pseudo-unitary categorification supplied by
the existence reduction cannot exist, and **R8_3_1768 has no complex
fusion categorification**.

Only an existence implication from the general-complex gate is used.
There is no assertion that every arbitrary original categorification
comes with a selected positive pivotal structure.

### Exact general-complex dependency and premise review

The gate is **Theorem `thm:research-four-general-spherical` ("Four general
sphericalization reductions")** in
`manuscripts/rank8/paper/m3_research_20261022.tex` at publication commit
`d920cc2531d8b03583c797886a3c2ab6170a281a`. An unchanged copy is provided in
`inherited/m3_research_20261022.tex`. It explicitly includes R8_3_1768
and states that every complex fusion categorification admits a spherical
structure and has a pseudo-unitary Galois conjugate. Our proof needs only
the weaker existence implication.

Its categorical premises have been reviewed from the manuscript:

- In canonical sphericalization, dual-compatible lifts exist. A selfdual
  simple's dual cannot be its opposite lift because spherical dimensions
  agree on duals, are nonzero, and the sign object reverses dimension.
  The signed quotient has the full parity domains, cyclic trace symmetry,
  dual reversal and ordered associativity. Commutativity is not assumed.
- The R1768 gate enumerates those domains modulo six independent sign
  normalizations: 49 normalized tensors, 3,136 unrestricted tensors and
  28 gauge classes. Its necessary dimension-character tests exclude the
  27 classes other than the class of the original tensor. In particular,
  sphericalization central induction requires delta/f to be an algebraic
  integer for every formal codegree from both sign sectors. A norm-valuation
  failure or a zero simple dimension is a valid obstruction.
- Lemma `lem:research-spherical-section` then supplies a spherical
  structure on the original category: after a lift-sign change making
  the signed tensor equal the original tensor, all negative-lift
  multiplicities vanish. The positive lifts form a fusion subcategory
  tensor-equivalent to the original category.
- For R1768, all ordinary dimension characters outside the FP Galois
  orbit have a zero entry. A spherical dimension character therefore
  lies in that orbit. A number-field model and Galois conjugation give
  a spherical category with positive FP dimensions, hence a pseudo-unitary
  category. The manuscript cites ENO Theorem 2.30 and its following remark
  for the number-field step. This does not assume a unitary classification
  or an equivalence with a separately constructed model.

This review checks the categorical implication and identifies the exact
inherited finite-search input. It does **not** independently regenerate
the signed enumeration. Its source-bound receipt remains
`evidence/rank8_research_20261022/pivotality/general_spherical_gates.json`,
whose SHA256 is recorded below. That existing completeness certificate is
an explicit dependency of the general-complex conclusion.

## 3. Why the previous Morita filter missed this

The earlier filter used the parity of the total sqrt(37) coefficient
of a restriction, which only records the sum of its noninvertible
multiplicities. In (1) that sum is ten and is even. But the two odd
positive-indicator summands must each have even multiplicity, not merely
an even total. This is precisely the information lost in passing from
the full restriction vector to its FP dimension.

The four previously retained regular factors are not exemptions from
the pairing lemma. Regular Morita algebras X X* are always available;
their bimodule forgetful realization gives the same conjugation object
X g X*. Applying the full multiplicity test there yields the
contradiction above. The proof in Section 1 avoids invoking that
Morita interpretation altogether.

## 4. Exact certificate and inherited inputs

Run `python verify_palindromic_exclusion.py`; normal and optimized Python
use explicit exceptions. The verifier binds the exact tensor SHA256,
checks the archived accepted indicator result, checks (1) in two
independent tensor contractions, and records both offending
multiplicities. It does not replace the published proof of the forced
indicator assignment or the general-complex existence reduction.

There is now a stronger, independently executed exact replay that does
not take the final 40-branch indicator conclusion on trust. The full
conjugation-parity graph on the eight labels has exactly the components

    {0,2,3,5}, {1,4,6,7}.

Thus every possible second-indicator vector must be

    (1,epsilon,1,1,epsilon,1,epsilon,epsilon), epsilon=+1 or -1.

`replay_palindromic_center.py` checks all 128 sign assignments against the
exact tensor to certify this domain. It then reconstructs the unchanged
published necessary center domains and replays precisely six existing
Farkas certificates:

- The all-positive vector is excluded by the earlier C2 Fourier cone.
- The negative-pointed vector is excluded in each of the five complete
  primitive-37 Gram branches V=0,1,2,3,4.

For each certificate the program checks a nonnegative pairing with
every allowed column of its full cone, and a strictly negative pairing
with the right-hand side. The five latter domains have 6,100 columns
each; the former has 10,711. It also independently replays the finite
source-character, Galois-complement and five-branch arithmetic. All
metadata agree with the frozen published domains. No optimizer or
associator search is called. The optimized replay passes in 30.485 seconds;
its exact output is `palindromic_center_receipt.json`. A prior normal
five-certificate replay passed in 39.355 seconds.

Forty unchanged source/certificate files (3.54 MB) are pinned to publication
commit d920cc... in `replay_source/`; `replay_sources.json` records every
SHA256. The old whole-band input census JSON was removed by the project's
cleaned publication policy. The replay adapter replaces only its source
loader by the identical SHA-bound tensor from the frozen bundle. The
equation builders, complete column domains and separators are unchanged.

The categorical completeness of those center domains, the saturated
conductor theorem and the general-complex existence gate remain explicit
mathematical inputs. The new replay reduces the computational dependency
to exactly the already certified branches required by the pairing lemma.

Inherited accepted inputs:

- `manuscripts/rank8/paper/m3_creative_20261022.tex`, Proposition
  `prop:creative-r1768-sector`: six noninvertible second indicators +1 and
  pointed second indicator -1.
- `evidence/rank8_creative_20261022/r1768/verification.json`:
  SHA256 `2a2472719aa4e953b7f514dfb4f811a4bef162b2c779cf4bb367a6c21bb977b8`;
  39 of 40 complete Gram/indicator branches excluded, the retained
  assignment is (-1,1,1,1,1,1,1).
- `evidence/rank8_research_20261022/pivotality/general_spherical_gates.json`:
  SHA256 `89ad25baeb05b69c95519670eb4cdd894a29d3b7f4d920535b1f404f46ba13d4`.

The prior exploratory `REPORT.md` in this directory was written before
the full-multiplicity observation. Its conditional structural results
remain logically correct but are superseded by this exclusion. The direct
categorical pairing argument was independently accepted in
`../r155/AUDIT_R1768_CONJUGATION.md` and
`../r1154/AUDIT_R1768_CONJUGATION_PAIRING.md`; r1154 also independently
reconstructed the tensor contraction and parity graph. These audits do
not replace the explicitly inherited gate or center-domain premises.
See `REPLAY_README.md` for runtime dependencies and relocatable replay
instructions. No online revision has been made.
