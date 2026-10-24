# Independent categorical audit of the rank-nine pullback models

The proposed constructions for `R9_2_1396` and `R9_2_1397` pass the categorical existence audit. They are genuine group-theoretical, hence unitarizable, fusion categories. Their fusion tensors are determined by the known rank-five seed and the character groups described below. The parent verifier is responsible for the independent source-to-model tensor isomorphism replay.

This audit concerns existence, coherence, the quotient fusion rules, and the fixed-channel trace data. It does not infer categorification from associativity of a candidate tensor.

## 1. The input is an existing category

Liu–Palcoux–Ren, *Classification of Grothendieck rings of complex fusion categories of multiplicity one up to rank six*, arXiv:2010.10264v5, Section 4.4, gives unitary solutions of the pentagon equations for the rank-five dimension-24 category used here. In the project's registry it is `LPR-24`.

Write its simples as `1,h,V,P,Q`, of dimensions `1,1,2,3,3`. The relevant products, read from the published fusion matrices, are

\[
h^2=1,\quad hV=V,\quad hP=Q,\quad
V^2=1+h+V,\quad VP=VQ=P+Q,
\]
\[
P^2=Q^2=h+V+P+Q,\qquad PQ=1+V+P+Q.
\]

In particular `P*=Q`. These are the actual nonselfdual seed rules, not those of `Rep(S4)`.

## 2. Descent to the near-group category

Let the seed category be `L`. Its adjoint subcategory is all of `L`: `PQ` contains `V,P,Q`, and `V^2` then supplies `h`. Its invertible group is `C2`.

Since dimension 24 has only two prime divisors, ENO Theorem 1.6 says that `L` is solvable. Definition 1.2 and Proposition 4.4 express solvability by successive cyclic-prime extensions and equivariantizations. The last nontrivial step cannot be an extension because `L_ad=L`. The only possible equivariantizing prime is two, since its character group embeds into the invertibles. Consequently

\[
\mathcal L=\mathcal B^{C_2}
\]

for an actual coherent action, not merely an order-two ring automorphism.

The action of `h` on the source simples determines the forgetful images:

\[
F(1)=F(h)=1,\quad F(V)=a+a^{-1},\quad F(P)=F(Q)=X.
\]

Here `a` has order three and `X` has dimension three. This follows from the standard orbit/stabilizer description of equivariant simples: a fixed simple downstairs has two equivariant lifts, whereas a free orbit has one lift. Cyclic stabilizers have no nontrivial projective representation obstruction. Thus `B` has type `(1^3,3)` and

\[
aX=Xa=X,\quad X^*=X,\qquad
X^2=1+a+a^{-1}+2X.
\]

The outer involution exchanges `a,a^{-1}` and fixes `X`.

## 3. The actual coherent S3 action

The same solvability argument applies to `B`: it has dimension 12, its adjoint category is itself, and its invertible group is `C3`. Thus

\[
\mathcal B=\mathcal P^{C_3}.
\]

The character group fixes `X` and acts freely on the three invertibles. Hence `P` has four invertible simples, with `C3` transitive on the three nonidentity ones. Its group is `V4`, not `C4`, because `Aut(C4)` has no element of order three. Therefore `P=Vec_{V4}^{omega}` for some associator `omega`.

The central `Rep(C3)` in `B` is preserved by every tensor autoequivalence of `B`. Here is the needed uniqueness argument. A monoidal automorphism of the identity has a scalar `t` on `X`. Since `X` occurs in `X^2`, one has `t^2=t`, hence `t=1`; all three invertible scalars then equal one. Thus `Aut_tensor(Id_B)=1`. Two central lifts of one invertible differ by a central invertible whose underlying object is the unit, equivalently a monoidal automorphism of `Id_B`. The forgetful homomorphism on central invertibles is therefore injective. The central `Rep(C3)` already supplies all three underlying invertibles, so its full central subcategory is unique.

The actual outer `C2` action consequently restricts to a braided action on this central `Rep(C3)`, including its original coherence transformations. Its equivariantization embeds centrally and fully faithfully in `B^{C2}=L`. Explicitly, the half-braiding of an equivariant central object with an equivariant object of `B` is its original half-braiding in `B`; equivariance makes this a morphism in `B^{C2}`, and the original hexagon remains valid. This also verifies the coherence assertion directly.

This central symmetric category is Tannakian: its forgetful functor to `Rep(C3)`, followed by the usual fiber functor to vector spaces, is a symmetric fiber functor. It has two one-dimensional simples and one two-dimensional simple, since the action inverts the nontrivial `C3` characters. Its Tannaka group has order six and is nonabelian; hence it is `S3`.

De-equivariantization by this embedded central `Rep(S3)` gives

\[
\mathcal L\simeq(\operatorname{Vec}_{V_4}^{\omega})^{S_3}
\]

with an actual coherent `S3` action. Equivariantization/de-equivariantization are inverse 2-equivalences (DGNO Theorem 4.18(i), Proposition 4.19; also ENO Proposition 2.10). Their compatibility with the normal subgroup `C3` identifies the intermediate category with the `B` above. In particular the normal `C3` acts transitively on the three nonidentity elements of `V4`. The resulting object action of `S3` is faithful: a homomorphism `S3 -> Aut(V4)=S3` nontrivial on its normal `C3` cannot factor through the abelianization.

There is no need to guess a cocycle representative or to promote a bare outer automorphism to a categorical action. The action is obtained from an existing category by de-equivariantization.

## 4. Pullback and existence

For `A=C9` or `A=C3 x C3`, choose a surjective homomorphism `q:A -> C3`, and set

\[
G_A=\operatorname{Dih}(A)=A\rtimes_{-1}C_2.
\]

The map `q` extends to a surjection `G_A -> S3`, carrying the involution to a transposition. Pulling back the actual `S3` action constructed above gives an actual `G_A` action, including all associativity/coherence data. Define

\[
\mathcal C_A=(\operatorname{Vec}_{V_4}^{\omega})^{G_A}.
\]

This is a fusion category of dimension `4*18=72`.

It is group-theoretical. Indeed, its crossed product `P rtimes G_A` is pointed: all pairs consisting of an invertible of `P` and a group element are invertible. ENO Proposition 2.2 makes the equivariantization Morita equivalent to that crossed product. Galindo–Hong–Rowell Theorem 5.20 therefore supplies unitarizability. This avoids any additional assumption about preserving a particular C*-structure while descending the seed.

## 5. Why the generated quotient tensor is forced

Put `E_A=P^A` and `K=ker(q)`, of order three. The intermediate category contains the inflation of `B=P^{C3}`. In particular it contains its simple `X_0`, with the same square as `X` above.

The invertibles of `E_A` form the character group `Ahat`. Its restriction map

\[
\mathrm{grade}:\widehat A\longrightarrow\widehat K\simeq C_3
\]

is surjective, with kernel the inflated `C3` character group. Every character of `K` extends to `A`. Choose extensions `lambda_j` of the three characters and let `X_j=lambda_j X_0`. These are all the noninvertible simples, each of dimension three. A different choice of extension differs by a kernel character, which fixes `X_0`, so the label is well defined up to isomorphism. The existence of `X_0` already trivializes the relevant projective stabilizer obstruction.

For `b,c in Ahat` and `j,k in C3`, tensor multiplication is consequently

\[
bc=b+c,\qquad bX_j=X_jb=X_{j+\mathrm{grade}(b)},
\]
\[
X_jX_k=\sum_{\mathrm{grade}(b)=j+k}b+2X_{j+k}.
\]

The action of the outer involution is `b -> -b` and `X_j -> X_{-j}`. This is precisely the quotient tensor and involution in `pullback_equivariant_models.py`. The cyclic case uses `Ahat=C9` with grade reduction modulo three. The split case uses `Ahat=C3 x C3` with grade the second coordinate.

## 6. Why the fixed-channel traces are forced

The only fixed simple objects in `E_A` are `1` and `X_0`. Their full subcategory sits in the inflated copy of the seed descent, so all their equivariant tensor-channel traces are inherited from `L`.

Choose one equivariant lift `P` of `X_0`; the other is `Q=hP`. In the seed, `P^2` contains `h` and not `1`, while the underlying unit-channel multiplicity in `X_0^2` is one. Thus the involution has trace `-1` on `Hom(1,X_0^2)`. Moreover `P^2` contains one copy of each of `P,Q`; the two-dimensional `Hom(X_0,X_0^2)` therefore has trace zero. Unit channels have their canonical trace one.

These are exactly `tau(9,9,0)=-1` and `tau(9,9,9)=0` in the generator. Replacing the lift of `X_0` by its negative cannot alter either datum.

For an equivariant output supported on a free orbit, Frobenius reciprocity gives the unaveraged underlying multiplicity. For an output supported on a fixed simple, its chosen sign eigenspace has dimension `(dimension + signed trace)/2`. If either input is supported on a free orbit, the involution permutes the summands of the relevant Hom-space without a fixed summand, so its trace is zero. Thus there are no unspecified additional traces or tensorator parameters in the generated tensor.

The simples upstairs have dimensions `(1,1,2,2,2,2,3,3,6)`: two lifts of the unit, four free invertible orbits, two lifts of `X_0`, and one free orbit `{X_1,X_2}`. The two dimension-three lifts are distinct duals by the negative unit-channel trace.

The generator matches the cyclic case to `R9_2_1396` and the split case to `R9_2_1397`. The exact tensor comparison is a separate finite certificate, not an additional categorical assumption.

## Primary references checked

- Z. Liu, S. Palcoux, Y. Ren, arXiv:2010.10264v5, Section 4.4: <https://arxiv.org/pdf/2010.10264v5>.
- P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and solvable fusion categories*, Theorem 1.6, Definition 1.2, Propositions 2.2, 2.10, 4.4: <https://arxiv.org/pdf/0809.3031>.
- V. Drinfeld, S. Gelaki, D. Nikshych, V. Ostrik, *On braided fusion categories I*, Theorem 4.18 and Proposition 4.19: <https://arxiv.org/pdf/0906.0620>.
- C. Galindo, S.-M. Hong, E. C. Rowell, *Generalized and quasi-localizations of braid group representations*, Theorem 5.20: <https://people.tamu.edu/~rowell/GHRarx1.pdf>.

Audit outcome: **accepted categorical existence and unitary realization**, conditional only on the separately replayed exact source-to-generated-tensor identification for each named census ID.
