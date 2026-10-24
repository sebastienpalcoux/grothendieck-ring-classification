# A fermionic folded-SO(3) obstruction

This document develops a categorical obstruction, not merely an arithmetic test. Its local trivalent step and its descent through the Temperley-Lieb negligible ideal must both be retained. Applying a classification of *morphism-generated* trivalent categories directly to the ambient categorification would leave a gap.

## Statement

For n>=3, let T_n be the based ring obtained from the even SU(2)_{4n-2} fusion ring by identifying the free pairs V_{2j} and V_{4n-2-2j}. It has rank n. Its distinguished basis x_0=1,x_1,...,x_{n-1} satisfies

`x_1*x_0=x_1`,

`x_1*x_j=x_(j-1)+x_j+x_(j+1)` for 1<=j<n-1,

`x_1*x_(n-1)=x_(n-2)+2*x_(n-1)`.

**Theorem.** T_n has no pseudo-unitary complex fusion-category categorification.

R9_2_920 is T_9. The independently replayed signed gate in `../signed/gate_R9_2_920.json` says that if this ring had any complex fusion-category categorification, a Galois conjugate would be pseudo-unitary. Thus the theorem excludes R9_2_920 in general scope.

## 1. Local trivalent relations in a hypothetical category

Suppose C is a pseudo-unitary categorification, with its canonical positive spherical structure, and let X represent x_1. It generates every simple of C. Its FP dimension is

`d = 1+2*cos(pi/(2n))`,

and the dimensions of Hom(1,X^k), for k=0,1,2,3,4, are 1,0,1,1,3. In particular X is selfdual. Morrison-Peters-Snyder Lemma 2.2 applies to these invariant dimensions and gives symmetric self-duality. Choose a nonzero trivalent vertex in Hom(1,X^3).

Rotation of the one-dimensional trivalent space acts by a cube root of unity. The local determinant calculation in Morrison-Peters-Snyder, Proposition 7.1, excludes a nontrivial rotation eigenvalue when the four-point space has dimension at most three and d!=2. Here d>2, so the vertex is rotationally invariant. Its bigon scalar is nonzero by rigidity and multiplicity one, and rescaling the vertex normalizes it to one.

The local determinant argument in MPS Proposition 4.1 then gives

`d+t-d*t-2=0`, i.e. `t=(d-2)/(d-1)`.

This step uses only the actual ambient four-point dimension, not generation of all morphisms. Moreover a three-by-three Gram minor of the four basic tree diagrams equals `d^3*(d^2-d-1)`, which is nonzero for d>2. Thus these diagrams span the entire ambient four-point space. Its trace pairing is nondegenerate, so the Gram-kernel relation in MPS Lemma 4.11 holds as an actual morphism identity. Together with the loop, tadpole and normalized bigon relations, this is the quantum SO(3) local presentation.

## 2. The required functor before semisimplification

Put `delta=2*cos(pi/(4n))`, so d=delta^2-1, and q=exp(pi*i/(4n)). Let TL_delta denote the planar Temperley-Lieb category *before* quotienting negligible morphisms. The second Jones-Wenzl idempotent p_2 is defined since delta!=0. The full tensor subcategory on powers of p_2 has the trivalent presentation just obtained.

One precise presentation route is Fendley-Krushkal, Theorem 4.3: the chromatic algebra has a trivalent H-I, loop and tadpole presentation. Set Q=d+1 and rescale the normalized MPS vertex tau to `v=sqrt(d-1)*tau`. The MPS Lemma 4.11 relation becomes their Figure 9 H-I relation; the bigon, triangle and edge-loop values become Q-2, Q-3 and Q-1, respectively. Their Lemma 7.1 injects this chromatic algebra into the doubled TL algebra, sending each edge to p_2 and each trivalent vertex to the corresponding three p_2 strands. The MPS doubled-strand vertex coefficient `sqrt(delta/(d-1))` becomes their coefficient `sqrt(delta)` under this rescaling.

The image is the full p_2 corner: their noncrossing-partition basis without singleton blocks (Lemma 4.4) has the Riordan dimension of the corner. Here is a parameter-independent dimension check. In the additive Karoubi TL category, `V^2=1 direct-sum p_2` for every delta!=0. Since `dim Hom(1,V^(2m))=Catalan_m` by the planar matching basis, the direct-sum decomposition gives `Catalan_m=sum_(k=0)^m binomial(m,k)*dim Hom(1,p_2^k)`. Its binomial inverse is the Riordan sequence, also counting those noncrossing partitions. This proves equality of dimensions at this root of unity, without a generic-specialization assumption. The injective chromatic map is therefore onto each corner. Bending gives the presentation for Hom spaces with an even total number of boundary edges.

For an odd total number of boundary edges, split one boundary edge using the normalized trivalent vertex. This embeds that Hom space into one with even total boundary count: collapsing the split edge is a left inverse because the normalized bigon is the identity. The even space is spanned by the presented trivalent diagrams, so collapsing them spans the odd space. Relations also transfer: split an alleged odd relation, use the even presentation, and collapse again. This proves the full Hom-space presentation, including odd boundary count. It supplies the explicit split/retract argument omitted in the earlier wording; see the independent phase-three audit at `../../phase3/audit_signed_so3/AUDIT.md`.

Consequently the actual local relations in C give a pivotal tensor functor from the additive Karoubi completion of this p_2 category to C, sending p_2 to X. Since `V^2=1 direct-sum p_2`, its additive Karoubi completion is the full even part of TL_delta. No claim that the functor is full is required.

## 3. Killing the negligible ideal using positive dimensions

Set ell=4n. The Jones-Wenzl idempotent p_(ell-1) is well defined: its recursion only uses the nonzero quantum integers [1],...,[ell-1]. Its categorical dimension is [ell]=0. Goodman-Wenzl, Proposition 2.1, says that the negligible tensor ideal of TL_delta is generated by p_(ell-1).

The even part contains the idempotent object

`P = (V^ell, p_(ell-1) tensor id_V)`.

Its pivotal dimension is [ell]*delta=0. A pivotal functor to C sends P to an object of dimension zero. Every nonzero object in the canonical spherical structure of a pseudo-unitary fusion category has strictly positive dimension. Therefore its image is the zero object, and the functor kills the identity of P.

The restriction of the TL negligible ideal to the even subcategory is generated by P. Indeed a morphism in the ideal factors as a sum through tensor products of p_(ell-1) with strands. Since ell-1 is odd and the source and target are even, the total number of the extra strands is odd. Using the TL braiding to move those strands next to p_(ell-1), each such factorization factors through P tensored with an even number of strands. Thus it is killed by the functor.

It follows that the functor descends to the semisimplified even SU(2) category

`F: D=PSU(2)_(4n-2) -> C`.

It is dominant, because X=F(V_2) generates C. This argument kills explicit trace-zero *idempotent objects*. It does not incorrectly assume that every trace-zero morphism in a pseudo-unitary category is zero.

## 4. The forced central algebra cannot exist

The SU(2) fusion recursion determines the images under F of all even simples: they are exactly the folded pairs x_j. In particular the nontrivial invertible object `f=V_(4n-2)` is sent to the unit, and no other simple besides 1 and f has a unit constituent in its image. Adjunction therefore gives

`A=right_adjoint(F)(1)=1 direct-sum f`.

The induced algebra of a dominant tensor functor has a canonical commutative separable central-algebra structure: A is a connected commutative separable algebra in Z(D), whose underlying object in D is as above. This follows from Bruguières-Natale, Proposition 5.1 and Corollary 5.6, or directly from the adjunction and the two projection-formula identifications `A tensor Y ~= right_adjoint(F)(F(Y)) ~= Y tensor A`.

The fusion category D has trivial universal grading. Indeed V_2 generates D and is a summand of V_2 tensor V_2; the degree of V_2 therefore satisfies g=g^2 and is the neutral degree. Hence `Aut_tensor(Id_D)=1`. Half-braidings on a fixed invertible object, if they exist, form a torsor under this group. Thus f has only one central lift.

The standard SU(2) braiding supplies that lift. Since the level 4n-2 is 2 modulo 4, its invertible f is the transparent fermion of the even subcategory, with `c_(f,f)=-id_(f tensor f)`. Thus the central summand f in A necessarily has fermionic self-braiding.

Commutativity forces the multiplication component `m: f tensor f -> 1` to satisfy `m=m*c_(f,f)=-m`, so it must vanish in characteristic zero. There is no component to f because f^2=1 and f!=1. Hence f would be a square-zero ideal in A. The resulting sequence of right A-modules `0 -> f -> A -> 1 -> 0` cannot split: every underlying map from 1 to A is a scalar multiple of the unit, and a nonzero such map is not A-linear from the quotient module, where f acts by zero. This contradicts semisimplicity of the A-module category (equivalently, separability of A). This is the contradiction.

## Rank-nine specialization and independent audit

For n=9 the source label ordering along the path is

`[0,1,8,2,6,4,5,3,7]`.

The generator has exact dimension `1+2*cos(pi/18)`, approximately 2.969615506; the earlier low-precision profile number 2.969459 is inaccurate and should not be propagated. The exact fusion tensor and algebraic character computations were not changed. The folded global dimension is `9/(2*sin(pi/36)^2)`.

The complete based-ring identification has been cross-checked against all 729 structure constants by `../models/folded_so3_diagnostic.py`, with result in the adjacent JSON file. Its source-to-folded permutation is `[0,1,3,7,5,6,4,8,2]`; this is the inverse of the path ordering above. The construction is explicitly a based-ring diagnostic, not an ordinary fusion-category model.

The independent categorical audit is **APPROVED**, with no additional categorical hypotheses: `../signed/R920_audit.md` and `../signed/R920_audit.json`. Its replay script `../signed/audit_R920.py` independently checks all 729 source structure constants, all 324 products of parent simples against the quotient map, the low invariant dimensions, and the general-scope signed-gate dependency. The audit separately supplies the local normalization, full Riordan corner-dimension proof, even-negligible parity argument, and central-fermion contradiction. R920 is therefore included in the accepted exclusion manifest.

## Primary references

- S. Morrison, E. Peters, N. Snyder, *Categories generated by a trivalent vertex*, Propositions 4.1 and 7.1, Lemma 4.11, and the SO(3) construction: <https://arxiv.org/abs/1501.06869>.
- P. Fendley, V. Krushkal, *Link invariants, the chromatic polynomial and the Potts model*, Theorem 4.3, Lemmas 4.4 and 7.1: <https://arxiv.org/abs/0806.3484>.
- F. M. Goodman, H. Wenzl, *Ideals in the Temperley Lieb Category*, Proposition 2.1: <https://arxiv.org/abs/math/0206301>.
- A. Bruguières, S. Natale, *Exact sequences of tensor categories*, Proposition 5.1 and Corollary 5.6: <https://arxiv.org/abs/1006.0569>.
- The independently verified general-to-Galois-pseudo-unitary gate is in `../signed/THEOREM.md` and `../signed/gate_R9_2_920.json`.
