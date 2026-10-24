# Independent audit of the R9_2_1848 orbifold model

**Verdict: PASS, with the near-group existence theorem explicitly cited.**
R9_2_1848 is realized by a unitary fusion category obtained from a unitary
near-group category `NG(C18,18)` by Izumi's isotropic-subgroup orbifold.
The categorical construction is justified by literature, and an independent
exact verifier matches all 729 source coefficients. No claim is made that
this audit reconstructs or freshly checks the source near-group associator.

## The source category is asserted to exist exactly

Paul G. Budinski's 2021 thesis, *Exotic Fusion Categories and Their Modular
Data*, Table 3.1 includes four `C18+18` solutions. In §3.3.1 (printed p.41)
the author explicitly states that the list is proved complete for `n<=20`
using §3.3.2. Thus C18 lies within the range of the claimed proof. Immediately before §3.3, printed p.40, the author also states that the defining polynomials were explicitly found for every Galois orbit for n<=19, although omitted for space. This includes C18.

Section 3.3.2, printed pp.46–47, specifically addresses the distinction
between numerical roots and exact solutions. It replaces the approximate
parameters by specified roots of algebraic polynomials, clears denominators
so each residual is an algebraic integer, and checks that all conjugates of
that residual have modulus below one. The norm then forces the residual to
vanish. This is an exact algebraic certification method, not an assertion
that a small numerical residual alone is enough. The section says this is
how the listed solutions are proved exact; C14 is used to explain the
method. The C18 polynomial and all root-isolation/error records are not
included in the proposed certificate, so this audit relies on the thesis's
stated construction rather than independently replaying that computation.

The table's `J_18^1` has pairing parameter `m=1`; §3.1 gives
`<x,y>=exp(2*pi*i*x*y/18)` and `a(x)=exp(-pi*i*x^2/18)`.
The near-group reconstruction is Theorem 3.1.1, citing Evans–Gannon
Corollary 5, in the Cuntz-algebra/unitary setting developed there.
There is no requirement to extend a classification of unitary categories
to arbitrary spherical categories: here a single existing unitary model is
used to prove existence.

## All orbifold hypotheses hold

Izumi, *A Cuntz algebra approach to the classification of near-group
categories*, arXiv:1512.04288v2, §12.1 and Theorem 12.5, constructs the
orbifold inside endomorphisms of an actual crossed-product factor.
Its assumptions are an existing C* near-group category with `m=|G|` and
an isotropic subgroup `H subset Hperp`; no extra numerical ansatz is used.

For `G=C18`, choose `H={0,6,12}`. Direct exponent arithmetic gives

- `Hperp={0,3,6,9,12,15}`;
- `H subset Hperp`;
- `a(h)=1` for every h in H, so one can choose `g_a=0`;
- `G/H=C6`, `Hperp/H=C2`, and `G/Hperp=C3`.

The theorem and the preceding irreducible decomposition give six distinct
invertibles and three distinct noninvertibles. With `g` generating C6
and `X=sigma`, their fusion laws are

`g^6=1`, `g^3 X=X`, `Xg=g^(-1)X`,

`X^2=1+g^3+2*(X+gX+g^2X)`.

These objects are closed under multiplication and duals, and X generates
them: X² includes all three noninvertibles and g³, while products of two
of the noninvertibles produce a generator of C6. Thus the generated
category has exactly these nine simples. Their noninvertible dimension is
`(9+3sqrt(11))/3 = 3+sqrt(11)`.

Unitary associators are inherited from the endomorphism category and
crossed-product construction. The theorem supplies coherence; checking
ring associativity alone is not being used to infer it.

The subgroup calculation in fact works for every unit nondegenerate
bicharacter parameter m on C18 and every corresponding quadratic
refinement: H has odd order and is isotropic, forcing a|H=1. Thus the
fusion-ring conclusion does not depend on a delicate choice among the
four displayed C18 solutions.

## Independent exact transport

`verify_independent.py` does not import the model author's generator or
use the saved model tensor. It reads R9_2_1848 from the original research
verification corpus and derives every product from the quotient-group
arithmetic and the displayed theorem formula. The resulting model-to-source
map is

`[0,1,4,8,3,2,5,7,6]`.

It verifies all 729 coefficients, the unit, all associativity equations,
both Frobenius reciprocity identities, duality, and the FP dimension
equations in `Q(sqrt(11))`. All checks pass. The original source SHA256 is
`42681407529a88aaaf34a909975776d8d1008ee8a99b6e231263dcb1aae9ff5c`.
The receipt is `independent_verification.json`. The author's final `phase5/quadratic_noncomm/REPORT.md` was also inspected: its construction, basis map, scope limitation and quoted theorem hypotheses agree with this audit.

## Primary sources inspected

- Budinski thesis PDF and its extracted text, preserved in
  `phase5/quadratic_noncomm/Budinski2021.pdf` and `.txt`:
  <https://ualberta.scholaris.ca/bitstreams/3f73f320-a2a2-4184-ad81-d8708764f725/download>.
  Source SHA256: `48e02112b25b13d54893d919b435bcb24c8215545ae98aa13db1e47bd10dfb78`.
  Relevant locations: Theorem 3.1.1, Table 3.1, §§3.3.1–3.3.2.
- Izumi full paper <https://arxiv.org/pdf/1512.04288v2>, §12.1,
  Lemma 12.2, the decomposition preceding Theorem 12.3, Theorem 12.5,
  and Remark 12.6(1). The file named `Izumi2016-orbifold.pdf` in the
  author's new folder is a later slide deck; this audit uses the full
  arXiv paper for the theorem and its proof.

No original author files, earlier phases, repositories, or online pages
were modified by this audit.
