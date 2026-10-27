# Quaternionic invertibles force a regular Morita context for R8_3_1768

## Result

Let `C` be a categorification of R8_3_1768 and transport it to a
pseudo-unitary Galois form, as permitted by the existing general-complex
gate. If an indecomposable semisimple `C`-module category has a dual
with a quaternionic invertible simple (second indicator minus one),
then that module category is equivalent to the regular module category.
Its dual is therefore tensor equivalent to `C` with the opposite tensor
product.

In particular, **no category with the GH(C6,2) fusion rules can be
Morita equivalent to a categorification of R8_3_1768**, regardless of
associator, arithmetic input, or choice of algebra object. This is
stronger than the `1+sigma` route obstruction.

It remains a restriction on possible models, not a general exclusion
of R1768.

## 1. The parity obstruction for any root of a module category

In the canonical positive spherical structure on `C`, the source
indicators are

\[
                 (1,-1,1,1,1,1,1,1).
\]

The source dimensions are

\[
 (1,1,5+\sqrt{37},6+\sqrt{37},7+\sqrt{37},
             7+\sqrt{37},6+\sqrt{37},5+\sqrt{37}).
\]

Suppose a dual category `D` contains a quaternionic invertible `Q`.
Choose **any** simple object `m` in the connecting module category,
and present `D` by the internal-end algebra `A_m` in `C`. The positive
module trace makes this a symmetric separable Frobenius algebra.
The forgetful functor from `A_m`-bimodules to `C` is pivotal Frobenius,
so it sends the negative-sign selfduality of `Q` to a nondegenerate
negative-sign pairing of its underlying object `U_m(Q)`.

By the pairing lemma in `UNIVERSAL_GH6_ROUTE_OBSTRUCTION.md`, every
positive-indicator selfdual source simple occurs in `U_m(Q)` with even
multiplicity. All six noninvertibles are of that type. Each has
coefficient one at `sqrt(37)` in its dimension. Consequently

\[
   [\sqrt{37}]\dim_C U_m(Q)\quad\text{is an even integer}.
\]

Because `Q` is invertible,

\[
                      \dim_C U_m(Q)=\dim_C A_m.
\]

Thus the square-root coefficient of the internal-end dimension must
be even at **every** simple module object. It is not enough for it to
be even only at the initially chosen root.

## 2. Applying the complete saved factor list

The previously exhaustive necessary module-factor filter leaves 21
induction factors. Its source is
`evidence/rank8_research_20261022/pointed_followup/r1768_modules/`.
Their complete induction matrices and root dimensions are in
`evidence/rank8_next_20261021/quadratic/profile_closure.json`.

For an induction matrix `B` and root algebra `A`, internal-end dimensions
at every simple module are exactly

\[
             \dim A_m=\frac{(B_m\cdot\mathbf d)^2}{\dim A}.
\]

This uses only FP dimensions and the standard canonical normalization
of module dimensions. It does not require completion of the still
undetermined action matrices. The old profile-closure proof already
derives and uses this identity.

An exact check of the 21 saved factors gives:

* Seventeen factors have an internal end with an odd square-root
  coefficient. They cannot have a quaternionic invertible in their
  dual.
* The other four factors, with `(candidate_index,factor_index)` equal
  to `(0,0),(26,15),(42,0),(46,19)`, each have an internal end of
  dimension **one**.

The second outcome forces an actual internal-end algebra to be the
tensor unit: it is connected, so contains the tensor unit once, already
exhausting its FP dimension one. Its module category is the regular one. This conclusion does not
depend on the unresolved based-action completions.

For transparency, the square-root coefficients for the four factors
are respectively

\[
\begin{split}
 &(0,10,12,14,14,12,10,0),\\
 &(10,0,0,12,12,14,14,10),\\
 &(12,0,0,10,10,14,14,12),\\
 &(14,0,0,10,10,12,12,14).
\end{split}
\]

The positions with coefficient zero have full dimension one, not
some unspecified rational integer; the verifier checks both rational
coordinates.

This proves the first assertion.

## 3. Excluding every GH(C6,2) Morita construction

Let `H` have these higher-Haagerup fusion rules and suppose it were
Morita equivalent to `C`. Transport the whole context to the positive
spherical setting. Put `u=6+sqrt(37)`.

The source's weighted second-indicator total is `T_2(C)=6u`. In `H`,
the unit and the unique selfdual nonidentity invertible contribute
`1+epsilon`, with `epsilon in {+1,-1}`. Its six large simples are
selfdual of dimension `u`, so

\[
                  T_2(H)=1+\epsilon+u\sum_{j=0}^5\nu_2(b_j).
\]

Morita invariance and irrationality of `u` force `epsilon=-1` and
all six large indicators to be plus one. Thus `H` necessarily contains
a quaternionic invertible.

Sections 1--2 then force the connecting module category to be regular.
Its dual has rank eight, while `H` has rank twelve. This contradiction
excludes **every** such Morita equivalence. No assumption on pointed
class, on a `1+sigma` algebra, or on an RW realization is needed.

## 4. Scope and checks

The proof uses the completeness of the previously saved necessary
algebra/module factor domain; it does not rerun that long enumeration.
Its derivation and exact complete-domain certificates are in the two
source folders above. The new calculation rechecks their SHA-256
bindings, the exact source tensor and dimension character, all 21
induction Gram identities, and the exact internal-end dimensions. Both
normal Python and `python -O` runs of `verify_morita_parity.py` pass
in less than a second.

This does not remove any of the 21 factors from the possible module
categories of an arbitrary hypothetical R1768 category. Rather, 17
cannot connect it to a category with a quaternionic invertible; the
other four are regular when categorically realized. No claim of
existence of any nonregular module category is made.

An independent investigator refiltered all 61 predecessor factors,
recovered the same 21 retained factors, and recomputed every quadratic
profile in `../r8_928_941/audit_r1768_profiles.py`; normal and optimized
runs both pass. This independently confirms all 17 odd witnesses and
the four regular factors. The same investigator reviewed the categorical
pairing argument and its positive pivotal normalization.

The central Weil-sector route was also considered. Its forced
18-object or 72-object columns omit the quaternionic source object,
so this pairing parity does not contradict them. A selfdual rational
central column with odd quaternionic-source multiplicity must have
all other multiplicities even; nonselfdual columns occur in dual
pairs. These conditions alone do not exclude the remaining central
rational sector. Therefore R1768 remains unresolved.

The categorical pairing and pivotal references are detailed in
`UNIVERSAL_GH6_ROUTE_OBSTRUCTION.md`. The argument transports specific
selfduality isomorphisms; it never treats Frobenius--Schur indicator
numbers as functorially preserved.
