# Independent categorical audit: R239, R290, and the R181 descent

The constructions for R8_2_239 and R8_2_290 are approved as actual unitary
fusion categories. The central-subgroup descent used for the general
exclusion of R8_2_181 is also approved. This audit rechecks the categorical
existence arguments in `NONINTEGRAL_PROOFS.md`; matching an associative
integer tensor by itself would not suffice.

## R239: the subgroup algebra and the Morita dual are justified

For `A=C7`, write the hyperbolic quadratic form on `A⊕A*` as
`q(x,y)=exp(2πixy/7)`. The matrices
`r=diag(2,4)` and `s=[[0,1],[1,0]]` preserve it because `2·4=1 mod7`.
They generate a copy of `S3`: the diagonal matrix has order three, the swap
has order two, and `srs=r⁻¹`.

ENO, arXiv:0909.3140, Corollary 1.2 identifies this orthogonal action with
a Brauer–Picard action on `Vec_C7`; Theorem 1.3 is the actual extension
existence result. Its first obstruction has coefficients
`Inv Z(Vec_C7)=C7²`, with the specified action. Every positive-degree
cohomology group vanishes: these groups are killed by `|S3|=6` and are
7-primary, so multiplication by six is invertible. This also eliminates
any ambiguity from the second-stage torsor.

For completeness the last obstruction group is genuinely zero. In the
Lyndon–Hochschild–Serre sequence for `C3◁S3`, every entry in total degree
four vanishes. The only possibilities are `H4(C3,C*)=0`, positive
`C2`-cohomology with 3-primary coefficients (zero by averaging), and
`H4(C2,C*)=0`. Thus `H4(S3,C*)=0`, with the trivial scalar action
appropriate to linear tensor functors. The extension therefore exists.

The `C3` restriction has pointed components: `r` is induced by an actual
group automorphism of `C7`. Its invertible group is `C7⋊C3`; the extension
splits because `H2(C3,C7)=0`. The action is multiplication by two, up to
replacing a generator with its inverse. This is the Frobenius group F21.

Its associator class can be removed, rather than merely assumed away.
In total degree three for `C7◁F21`, all mixed entries vanish by coprime
averaging. The invariant part of `H3(C7,C*)=C7` vanishes: multiplication
by two on `C7` acts there by multiplication by four. Hence
`H3(F21,C*)` is inflated from `H3(C3,C*)`. In the sequence for
`C3◁S3`, inversion acts trivially on `H3(C3,C*)`, and its degree-three
edge term survives; thus restriction
`H3(S3,C*)→H3(C3,C*)` is onto. Twisting the whole S3 extension removes
the pointed restriction's class. The ordinary subgroup algebra
`B=⊕_{h∈C3} h` is then associative and separable.

Passing to its bimodules is consequently a valid Morita construction.
The even component is the dual of `Vec_F21` with respect to the subgroup
algebra, namely `(Vec_C7)^C3≃Rep(F21)`. This identification uses the
actual split action, not just equality of fusion dimensions.

The three reflection components have rank one over `Vec_C7`. On their
coset, left and right `C3` multiplication have a stabilizer isomorphic to
`C3`; for a reflection `s`, the relation `r^i s r^j=s` means `j=i`.
Projective irreducibles of that cyclic stabilizer are ordinary after a
coboundary change, because `H2(C3,C*)=0`. They give exactly three odd
bimodules. Twisting their stabilizer character on the left and right has
opposite signs, giving
`alpha_i m_j=m_{i+j}` and `m_j alpha_i=m_{j-i}`. This also supplies a
direct justification of the Fourier-transport sentence in the proof.

Each odd object has dimension `sqrt7`: the underlying object is the sum
of three reflection-sector objects and the bimodule dimension is divided
by `FPdim(B)=3`. The two three-dimensional even simples act as the sum
of the three odd simples. Duality is a translation `j↦j+c`, since it
commutes with the two opposite alpha actions; involutivity gives `2c=0`
in `C3`, hence every odd simple is self-dual. Frobenius reciprocity now
forces `m_j m_k=alpha_{j-k}+X+Y`. These products agree with the independent
constructor and the whole census tensor. Finally, an S3 extension of a
pointed category is weakly group-theoretical; that property is preserved
by Morita equivalence. GHR, arXiv:1105.5048, Theorem 5.20 supplies
unitarity. No unproved assumption about a central Rep(C3) in the original
S3 extension is used: the subgroup algebra was constructed directly.

## R290: modularity, symmetry, and the unitary extension

In unitary `SU(3)_4`, the pointed generator `(4,0)` has order three and
twist `exp(2πi·4/3)`. Its quadratic form on `C3` is nondegenerate.
Its Müger centralizer is precisely the triality-zero subcategory, with
labels
`(0,0),(3,0),(1,1),(0,3),(2,2)`. Hence this rank-five adjoint subcategory
`PSU(3)_4` is modular and has no nontrivial invertible objects. This is a
centralizer and modular factorization, not a bosonic quotient by the
nondegenerate pointed C3.

The Dynkin diagram swap interchanges the Chevalley generators with
indices one and two. It preserves the R-matrix and the compact star
structure and descends through the negligible ideal. It therefore gives
the required unitary braided autoequivalence, not only a permutation of
labels. Edie–Michell, arXiv:2002.03220, Corollary 2.7 constructs the
braided symmetry; its restriction to the adjoint category is explicitly
discussed in Section 3. It exchanges `(3,0)` and `(0,3)` and fixes the
other three labels.

The unitary obstruction theory is Cui–Galindo–Plavnik–Wang,
arXiv:1510.03475, Sections 3.2–3.4. The first obstruction has zero
coefficient group because `Inv(PSU(3)_4)=1`. The second lies in
`H4(C2,U(1))=0`, by the cyclic-group cohomology formula. Thus a faithful
unitary C2-crossed extension actually exists. The model used here is this
extension before equivariantization. Bischoff, arXiv:1807.06131,
Proposition 1.1 applies to arbitrary faithful crossed extensions of a
modular tensor category and yields exactly three odd simples; it has no
conformal-net realization hypothesis.

The finite NIM uniqueness argument in the proof is also valid. The
neutral generator X has characteristic polynomial
`(t²+t+2)(t³−2t²−t+1)`. The cubic is irreducible over Q by the rational
root test and has discriminant 49, so it has three distinct real roots.
Its positive Frobenius–Perron root must occur in the three-dimensional
odd action; hence that action has exactly this characteristic polynomial.
Commutativity and dual-transpose action make the action normal, and real
eigenvalues force it to be symmetric. Its trace and squared trace are two
and six. Exhausting the consequent six nonnegative entries gives exactly
one matrix up to simultaneous basis permutation. The remaining actions
are the displayed polynomials in that matrix. The three positive
eigenvector coordinates are pairwise distinct, so duality fixes all three
odd simples. Crossed braiding supplies the right action and reciprocity
supplies every odd product. Therefore the full integer tensor is forced
by the actual category, rather than selected because it matches a census.

The neutral and NIM calculations use exact integers and rationals. The
FP dimension lies in `Q(2cos(2π/7))`, equivalently the degree-three real
subfield of `Q(ζ7)`; no numerical approximation is required. The
existence proof needs no large center computation or modular-data search.

## R181: why the central order-three subgroup exists

For the neutral category `D=Rep(F21)`, the adjoint-generated condition
implies `U(D)=1`. The forgetful map `Inv Z(D)→Inv D` is therefore
injective, and the canonical central Rep(C3) already provides all three
invertibles. Consequently `Inv Z(D)=C3`, not a larger group that could
have an undetected lift.

An invertible odd bimodule induces an automorphism of this central C3.
The central left action is transported to the corresponding right action.
The ring says that these two C3 permutations on the three odd objects
agree and are faithful. The transported central generator must therefore
be the same generator, rather than its inverse. Uniqueness of the lift
fixes the central objects, so the relative-center involution fixes this
subgroup pointwise.

Since `H2(C2,C*)=0`, each fixed central simple admits an equivariant
structure. All six possible lifts form an abelian group in the braided
center: its kernel is the two characters of C2 and its quotient is C3.
It has a unique order-three subgroup. That subgroup maps bijectively onto
the neutral C3, and its self-braiding is inherited from the original
Tannakian subgroup, hence is trivial. It gives a central Rep(C3) that
forgets faithfully into the full category. De-equivariantization is
therefore legitimate; it produces a dimension-fourteen TY(C7) category
and retains the multiplication-by-two/four C3 action. Neither action
preserves a nondegenerate symmetric bicharacter of C7 because
`2²≠1` and `4²≠1 mod7`. The exclusion applies to general complex fusion
categories. No use is made of an incorrect transparent-fermion principle
for a category that was never assumed braided.

## Sources inspected

- ENO, https://arxiv.org/abs/0909.3140, Corollary 1.2, Theorem 1.3,
  Sections 7–8 and the pointed-extension appendix.
- GHR, https://arxiv.org/abs/1105.5048, Theorem 5.20.
- Edie–Michell, https://arxiv.org/abs/2002.03220, Corollary 2.7 and the
  charge-conjugation discussion in Section 3.
- CGPW, https://arxiv.org/abs/1510.03475, Sections 3.2–3.4.
- Bischoff, https://arxiv.org/abs/1807.06131, Proposition 1.1.
- Relative-center equivariantization: GNN,
  https://arxiv.org/abs/0905.3117, Theorem 3.5.
