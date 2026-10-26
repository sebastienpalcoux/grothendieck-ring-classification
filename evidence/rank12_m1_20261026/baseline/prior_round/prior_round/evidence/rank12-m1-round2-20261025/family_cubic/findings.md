# All twenty cubic cases are excluded over C

The sixteen `cubic_C7` cases and four `cubic_C9` cases from the first-round unresolved list are excluded from arbitrary complex fusion categorification. The arguments use separable subgroup algebras and categorical Morita equivalence. They need no pivotal, spherical, pseudo-unitary, unitary or braided hypothesis. The C9 argument does not assume that an arbitrary original category is equivalent to a known unitary model.

`results.json` records every permanent input ID and its exact witness. `input_tensors.json` and `input_families.json` are bound snapshots of these twenty inputs. `python verify.py` and `python -O verify.py` both pass. The replay checks the source tensor bindings, all required source-ring incidences, the complete positive dimension characters, subgroup premises and the exact nonintegral norms. The categorical lemmas below are mathematical premises proved here, not conclusions inferred from a tensor match.

## 1. Paired stabilizer integrality

Let C be any complex fusion category, let X,Z be simple, and let H be a subgroup of invertible objects such that

1. h X is isomorphic to X for every h in H;
2. h Z and Z h are isomorphic to Z for every h in H;
3. the multiplicity m of Z in X X* is positive.

Then

\[
\frac{m\operatorname{FPdim}(Z)}{|H|}
\]

is an algebraic integer.

Choose isomorphisms h X -> X. Their scalar multiplication constants define an associative algebra A with underlying object the direct sum of h in H, and make X a left A-module. This is the usual twisted subgroup algebra: the module pentagon supplies its associativity, including the restriction of the ambient pointed associator. It is connected and separable in characteristic zero. The transpose action makes X* a right module over this same algebra A. Thus X X* is an A-bimodule by its commuting outer actions.

Because H fixes Z on both sides, the entire Z-isotypic summand mZ is stable under these actions. In particular, it is an object of the fusion category Bimod_C(A), not merely a vector-space subobject. Its Frobenius–Perron dimension in that category is m FPdim_C(Z)/FPdim_C(A). This must be an algebraic integer.

This use of the paired product X X* matters. For unrelated objects X,Y fixed by a noncyclic H, the two projective stabilizer cochains need not determine the same subgroup algebra. No such identification is made here.

The standard dimension normalization is EGNO, *Tensor Categories*, Exercise 7.16.9(i), printed page 169, and Morita invariance of total FP dimension is Corollary 7.16.7. Both hold without a pivotal structure. Author's final text: <https://math.mit.edu/~etingof/egnobookfinal.pdf>.

## 2. Direct application: sixteen C7 cases

Put a=2 cos(pi/7), the largest root of a^3-a^2-2a+1, and b=a^2-1. Each of the sixteen rings has dimensions

\[
1^{\times8},\quad (2a)^{\times2},\quad (2b)^{\times2}.
\]

Choose X of dimension 2b as specified by the certificate. Its left stabilizer H has order four, H also fixes X on the right, and X occurs once in X X*. Apply the paired criterion with Z=X and m=1. The required algebraic integer would be b/2. But its monic polynomial and field norm are

\[
t^3-t^2-\tfrac14t+\tfrac18,\qquad
N_{\mathbb Q(a)/\mathbb Q}(b/2)=-\tfrac18.
\]

The norm of an algebraic integer in a number field is a rational integer. This excludes all sixteen cases.

Their input suffixes are 32, 131, 152, 184, 217, 245, 286, 290, 297, 302, 339, 411, 416, 458, 465 and 527.

## 3. A rank-three Morita lemma

Suppose B is any complex fusion category with simples 1,g,T and rules

\[
g^2=1,\qquad gT=Tg=T,\qquad T^2=1+g+T.
\]

Let A=1+g, with its associative algebra structure supplied by the fixed simple T. Then Bimod_B(A) is pointed of dimension six.

Here is an elementary proof, valid for every original categorification of these rules. The category M of left A-modules has exactly three simples: M_0=A and two modules M_+,M_- with underlying object T. On T, the g-action squares to a nonzero scalar; normalizing that scalar gives its two possible eigenvalues. All three modules have underlying FP dimension two.

The A-bimodules supported on 1+g are precisely A and u=A_sigma, where sigma is the algebra automorphism acting by -1 on g. They are invertible. Tensoring with u fixes M_0 and exchanges M_+,M_-. Every other simple bimodule has underlying object qT, so its dimension in the dual category is the positive integer q. Morita invariance gives total dimension six. Consequently, either all six simples are invertible, or the remaining squared dimension four is occupied by a unique simple Q of dimension two.

Suppose the latter occurs. Uniqueness gives Q*=Q and uQ=Q. The object Q M_0 is supported on M_+,M_-, has total multiplicity two, and is invariant under u. Thus Q M_0=M_++M_-. By reciprocity, the multiplicity of M_0 in Q M_+ is exactly one. Since all three module dimensions agree, Q M_+ has total multiplicity two. But uQ=Q forces this output to be u-invariant; the coefficients of M_+,M_- must therefore agree. An odd remaining total multiplicity cannot be distributed between that exchanged pair. The coefficient of M_0 cannot increase because it is exactly one. This contradiction proves that the dual is pointed.

Equivalently, the hypothetical action matrix Q would be symmetric, have all row sums two, satisfy UQ=Q for U fixing 0 and swapping +,-, and have Q_{0,+}=Q_{0,-}=1. Its + row would have sum 1+2n=2 for an integer n, which is impossible.

## 4. Morita enlargement and exclusion: four C9 cases

Put b=2 cos(pi/9), the largest root of b^3-3b-1, and write

\[
x=1+2b,\qquad y=2b^2-2.
\]

Each of the four rings has type

\[
1^{\times4},\quad 2^{\times2},\quad x^{\times4},\quad y^{\times2}.
\]

The integral subring B_0 has dimension twelve and contains a rank-three subring B of the preceding lemma. The exact labels are:

| Ring | g | T | h outside B |
| --- | ---: | ---: | ---: |
| R12_1_38 | 11 | 10 | 1 |
| R12_1_39 | 11 | 10 | 1 |
| R12_1_218 | 7 | 11 | 3 |
| R12_1_219 | 6 | 11 | 3 |

Here h is invertible and hgh*=g. Every one of the six nonintegral simples is moved by g, and left and right multiplication by g agree on their labels.

Assume a categorification C exists, and take the actual algebra A=1+g inside B. In the Morita dual C'=Bimod_C(A), the full subcategory D_0=Bimod_{B_0}(A) has dimension twelve. Its subcategory Bimod_B(A) is pointed of dimension six by the lemma. Conjugation by h sends A to an algebra with the same underlying object 1+g and nonzero multiplication on g^2. Any two such algebra structures are isomorphic, by rescaling the g summand. Thus hA admits an invertible A-bimodule structure outside Bimod_B(A). The resulting group of invertibles in D_0 has order at least twelve, so D_0 is pointed of order twelve.

For a nonintegral orbit {V,gV}, an A-left module has underlying V+gV. A right g-action has two sign choices: after choosing its intertwiner, its square is a nonzero scalar and can be normalized. Equivalently, the two-sided stabilizer is the diagonal C2 and H^2(C2,C*)=0. Thus each free two-element orbit gives exactly two simple A-bimodules with dimension FPdim_C(V). There are two x-orbits and one y-orbit. Consequently C' has precisely

\[
1^{\times12},\qquad x^{\times4},\qquad y^{\times2}.
\]

This statement does not claim that C' is multiplicity free. No full tensor computation in C' is needed.

The elements 1,x,y are linearly independent over Q, and

\[
y^2=6+2x+2y.
\]

For any y-dimensional simple Y in C', comparison of coefficients in this dimension basis shows that Y Y* contains six invertibles, total x-dimensional multiplicity two, and total y-dimensional multiplicity two. The left stabilizer L of Y therefore has order six, as does its right stabilizer R. Each of the left and right group actions permutes only two y-dimensional labels, so L and R fix both of them. Their intersection has order at least three (indeed three or six) inside the group of twelve invertibles, and therefore contains a subgroup H of order three.

Some y-dimensional simple Z occurs in Y Y* with multiplicity m in {1,2}. The subgroup H fixes Y on the left and Z on both sides. The paired stabilizer criterion now requires my/3 to be an algebraic integer. Yet

\[
N_{\mathbb Q(b)/\mathbb Q}(y)=-24,\qquad
N_{\mathbb Q(b)/\mathbb Q}(my/3)=-\frac{8m^3}{9},
\]

which is not an integer for m=1 or 2. This excludes R12_1_38, R12_1_39, R12_1_218 and R12_1_219.

## 5. Scope and independent scrutiny

These are theoretical exclusions with short exact premise checks, not conclusions from a failed construction search. The rank-three lemma and the C9 enlargement argument were independently read and checked by the exclusion-audit agent and the parent agent before acceptance. Independent human verification remains pending.

The methods use familiar separable algebra and Morita constructions, organized here to obtain these exclusions. No claim is made that the lemmas are new in the literature, or that the tensor-equivalence classes of arbitrary original categorifications have been classified.
