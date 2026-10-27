# Fresh adversarial audit of the two Galois-pairing exclusions

Date: 27 October 2026. Source repository frozen at
`6a426acf6465dd674351be92dcca41b72f371521`.

## Verdict

The new arguments excluding **R9_2_1607 and R9_2_1976 over C are retained**.
I found no categorical gap in the symmetric-pairing argument. The conclusion
retains the explicit inherited TY/Morita reductions, the lower-rank exclusions
R6_4_6 and R6_4_174 used to remove extreme completions, and the independently
being rechecked reflection-shift theorem. This audit does not treat numerical
agreement as a substitute for any of these categorical premises.

## 1. Pivotal symmetry is the correct notion

The potentially delicate step was checked against the actual source:
Frohlich–Fuchs–Runkel–Schweigert, arXiv:math/0309465, Definition 2.22 and
Proposition 2.25(ii). Definition 2.22 equates the left and right curried maps
of the pairing. In pivotal notation this is precisely
`phi = phi* j`, not merely commutativity relative to a braiding.
Proposition 2.25(ii) applies to a commutative Frobenius algebra with trivial
twist. The canonical algebra I(1) has these hypotheses in the canonical
positive ribbon center. No C*-structure or unitarity is used.

A selfdual simple summand of multiplicity one in a symmetrically selfdual
object inherits a nondegenerate symmetric pairing: nondegeneracy prevents
its simple isotypic block from vanishing, and no other block can pair with
it. A pivotal strong monoidal functor transports this actual pairing.
Applying the same block argument after restriction then forces positive
second indicators on multiplicity-one selfdual constituents. There is no
claim that arbitrary numerical indicators are functorial.

The transpose formula is independently consistent with Shimizu,
arXiv:1208.2433v2, equation (2.7). The canonical-algebra trivial twist and
complete distinguished-object decomposition are in Ostrik,
arXiv:1309.4822, Theorems 2.5 and 2.13.

## 2. Selfduality and restriction of the distinguished object

The zero-shift D8 ring has eight scalar representations and one representation
of degree two. Formal codegrees are D,D',16 six times,4. Ostrik's dimension
formula is D/f_E; the degree of E is its multiplicity in I(1), not an extra
factor in its dimension. Thus the Galois object B has dimension D/D', occurs
once, and is the only constituent of that dimension. Duality permutes the
constituents of I(1) and preserves their dimensions, proving B*=B.

The normalized central-character argument uses chi_E/dim(E), as required on
the two-dimensional block. Its conclusion is F(B)=1+sum X_q. All four X_q
are selfdual in the zero-shift completion. The pairing argument therefore
forces all four second indicators to be +1.

The exact verifier `../unresolved10_20261027/r9_commutative/verify_galois_fs2.py`
was rerun both normally and with Python -O; both passed. It checks every
representation product, codegrees, restriction, source hashes and dualities.
The categorical reasoning above is separate from that finite check.

## 3. Morita comparison can be made independent of all TY sign conventions

Ng–Schauenburg, arXiv:math/0601012, Theorem 4.1 gives

    T_2(C) = sum_V dim(V) nu_2(V)
           = (dim C)^(-1) sum_Z dim(Z)^2 theta_Z^2.

Canonical positive ribbon centers of Morita-equivalent pseudo-unitary
categories agree, so T_2 is invariant. On the rank12 side this is b+4d for
an integer b; on the rank9 side it is a+s d, with a,s integers. Since
`d=4+3sqrt(2)` is irrational, equality forces s=4, without needing to identify
the integral signs explicitly. R1607 has only two selfdual large objects,
so s<=2; R1976 has none, so s=0. Both are contradictions. R137 has four and
is not excluded by this reasoning.

## 4. General-complex scope

I reread the signed-sphericalization theorem and its scalar-character
argument. Canonical sphericalization supplies opposite nonzero dimensions
on the two lifts. The signed quotient has full coefficient domains
{-N,-N+2,...,N}; its dimension character is nonzero on each basis element.
The intrinsic dimension is the signed squared-dimension sum, and if it is
Galois-conjugate to FPdim then number-field descent and scalar conjugation
produce a pseudo-unitary categorification with the unchanged based ring.
This is an existence implication, not an assertion that an arbitrary
original categorification was pseudo-unitary.

I freshly replayed the two relevant archived certificates using the
independent bit-vector verifier with active assertions. Results:

| Ring | Representatives | Orbit tables | Completeness | Time |
|---|---:|---:|---|---:|
| R9_2_1607 | 10 | 14 | UNSAT | 1.76 s |
| R9_2_1976 | 8 | 15 | UNSAT | 1.74 s |

Hashes match the current input tensors. See `signed_gate_receipt.json`.
No long computation, online modification, or new associator search was used.

## Primary sources retrieved afresh

- https://arxiv.org/pdf/math/0309465 — Def. 2.22, Prop. 2.25(ii).
- https://arxiv.org/pdf/1309.4822 — Thms. 2.5, 2.13.
- https://arxiv.org/pdf/math/0601012 — Thm. 4.1.
- https://arxiv.org/pdf/1208.2433 — (2.7), second-indicator transpose.
