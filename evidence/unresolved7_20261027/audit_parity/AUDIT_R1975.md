# Fresh adversarial audit of the R9_2_1975 exclusion

Date: 27 October 2026. Source snapshot: `6a426acf6465dd674351be92dcca41b72f371521`.

**Verdict: the exclusion is retained. No mathematical error was found in the
new argument or the audited scope reductions.** The distinction between
replaying finite identities and proving their categorical applicability is
maintained throughout this audit.

## 1. Categorical existence gate

I read the signed-sphericalization theorem and the actual R1975 gate, rather
than treating the previous PASS receipt as a proof. In sphericalization the
signed coefficient domain is the full parity interval, including zero for
multiplicity two; a dimension character has nonzero entries and equal dual
entries. Thus omitting zero products is justified, while omitting all zero
coefficients individually would not be.

The two signed branches have possible global dimensions respectively
`144 +/- 96 sqrt(2)` and `16`. The latter is impossible because the original
scalar formal codegree `f=144+96sqrt(2)` lifts to `2f` in sphericalization,
so `16/f` must be an algebraic integer, whereas its norm is `1/9`.
The former dimensions are the two conjugates of FPdim. Number-field descent
and Galois transport consequently yield a pseudo-unitary categorification
of the same based ring whenever any complex categorification exists.

Fresh replay of `replay_r1975_gate.py` returned PASS, two representative
branches, two complete orbits, and final UNSAT in 0.54 seconds. The original
tensor hash was
`8b30652d59e868a120b6c423e46a99ab51f6032af752dc0082a3d80fd9e61323`.
Assertions were enabled. The eight-bit associativity check is exact because
the unreduced integer bound is at most 72.

Taking the actual subgroup-algebra Morita dual preserves both intrinsic
global dimension and FP dimension. Thus use of a positive spherical
structure on the dual is legitimate. This makes no claim that an arbitrary
original category is unitary, pivotal, or itself pseudo-unitary.

## 2. Exhaustive Morita and pointed-associator inputs

I read `NEW_RESTRICTIONS.md`, `1975_FORCED_ASSOCIATOR.md`, the common
`THEOREM.md`, `DUAL_COMPLETION.md`, and `FORCED_D8_ASSOCIATOR.md` rather
than importing the final status labels.

The integral TY origin and two distinct large-object stabilizers force the
nonalternating bicharacter. The isotropic subgroup algebra exists over C.
Its pointed Morita sector is D8; the TY sign changes its associator, not
its underlying group. The actual source-module completion leaves the
extreme branch and two uniform branches. The extreme branch contains the
specified R6_4_155 subcategory and an invertible normalizer exchanging two
of its invertibles. The inherited unique-central-lift/twist obstruction
for that rank-six category removes it. This prior rank-six center theorem
remains an explicit dependency; it is not replaced by the unproved
nonexistence of R6_4_155.

For the two uniform branches, the full pointed associator class is fixed.
The cyclic restrictions are not used without a detection theorem:
Goff--Mason--Ng, Lemmas 4.4--4.5, prove that the order-four factor of
H^3(D8,C*) is detected on the rotation C4; the remaining inflation subgroup
has no nonzero class trivial on all order-two cyclic subgroups. This
justifies replacing the actual class by the displayed cocycle.

## 3. Opposite and normalizer conventions

Vainerman--Vallin, Sections 2.2.1, 2.2.2 and 3.1.1, were checked directly.
After the second-coordinate inversion their opposite is factor swap and
inverse cochain. Their conjugation correction is exactly the displayed
kappa. Consequently duality with shift q requires

`phi_q^*(beta gamma) kappa_q T^*(beta gamma)`

to be a coboundary. The fact that the full fusion category is not Z2-graded
does not invalidate this necessary condition on its self-dual pointed
bimodule component. No graded-extension reconstruction theorem is used.

The all-complex cancellation is valid: for a central element e, the
commutator with e in any scalar central extension is a character. It kills
the commutator subgroup and is multiplicative, with no root-of-unity
restriction on gamma. The additional identity C_gamma(PS,(PS)^2)=1 follows
by lifting PS and observing that a lift of its square differs from the
square of the lift only by a central scalar.

For reflection shifts the product invariant is -1. For rotation, the
individual invariant forces C_gamma(P,Z)=1, hence C_beta-gamma(P,Z)=-1.
The rotation branch itself has an eighth-root coboundary witness. A
fourth-root-only search would therefore be wrong; the accepted exclusion
does not make that mistake.

## 4. Relative-center parity

This is the most convention-sensitive step. The argument may be restricted
to A=<p,z>=V4, where the chosen pointed associator is identically one.
Consequently the diagonal action uses the ordinary strict pointed
convention. Restricting a central half-braiding produces a projective
A-action on the X_0-isotypic multiplicity space. Its multiplier is beta
restricted to diagonal A, or its inverse; both have commutator -1.
Thus the two operators anticommute, and the determinant argument forces
the multiplicity to be even. This does not assume a globally trivial
diagonal D8 tensorator, an ordinary D8 representation, or a pivotal
square condition.

## 5. Independent normalized Galois-unit calculation

The scalar characters are (psi,t), with t^2=2 psi(alpha) for nontrivial
psi and t=d,d' for the trivial psi. Their formal codegrees are six copies
of 16 and D,D'. The remaining irreducible is the degree-two D8 module,
on which all X's act by zero; its formal codegree is 4. These exhaust the
algebra since 8+2^2=12. The regular Casimir eigenvalue on the last block
is 8, not 4.

I checked the central-character theorem directly in Deshpande,
Proposition 2.8 and Section 4.3 (especially Corollary 4.5), together with
Ostrik Theorem 2.13. On central elements it uses the scalar
`lambda_E=chi_E/dim(E)`. For B=A_(sigma FP), S symmetry yields

`(D/f_E) lambda_E(FB) = (D/D') sigma(D/f_E) = D/sigma(f_E)`.

Therefore FB acts by f_E/sigma(f_E) on every irreducible. The central
element 1+sum X_q has exactly those scalars, including 1 on the
degree-two block. Semisimplicity gives equality, not merely equality
of dimensions. Its X_0 multiplicity is one, contradicting the preceding
evenness.

Both `verify_galois_parity.py` and `verify_duality_obstruction.py` were
freshly replayed successfully in under one second total. Their role is to
check source bindings, all finite cocycle inputs and the complete matrix
identity; the categorical arguments above supply applicability and scope.

## Primary sources freshly checked

- Vainerman--Vallin, https://arxiv.org/pdf/1210.1732, Sections 2.2.1,
  2.2.2 and 3.1.1.
- Goff--Mason--Ng, https://arxiv.org/pdf/math/0603191, Lemmas 4.4--4.5.
- Ostrik, https://arxiv.org/pdf/1309.4822, Theorem 2.13.
- Deshpande, https://arxiv.org/pdf/1611.04486, Proposition 2.8 and
  Section 4.3, Corollary 4.5.

No online files or classification ledgers were changed.
