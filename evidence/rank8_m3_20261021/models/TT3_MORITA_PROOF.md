# A unitary model for R8_3_715

Let Q be the unitary 2D2 category with simples 1,g,r,gr and rules
`g^2=1`, `gr=rg`, `r^2=1+2r+2gr`. Put `d=2+sqrt(5)=phi^3`.
The previously certified nonsplit extension E (R8_2_37) has simples
`a^i,a^i r` for i=0,1,2,3, with `a^2=g`, `ra=a^-1 r`, and the above
square relation. Its construction and independent audit are
`evidence/unified_20261016/rank8/R37_CONSTRUCTION.md` and
`R37_INDEPENDENT_AUDIT.md`; it is an actual unitary fusion category.

Grossman, *Fusion categories associated to subfactors with index
3+sqrt(5)*, arXiv:1612.07185, Section 4.1 and Lemma 4.1, gives Q-systems
A=1+r in Q. The A-A bimodule category in Q is the dual 2D2 category
TT3. Its rules are recorded explicitly in Edie-Michell, arXiv:1904.08909v2,
Definition 2.5. Both Q-systems give these rules.

Form D = A-bimod(E). This is a unitary fusion category. Because A lies
in the neutral component, D inherits a faithful C2 grading whose neutral
component is TT3. Existence is therefore established before any census
comparison. We now determine its entire fusion ring.

Write the TT3 basis as `1,p,q,pq,qp,pqp`, where
`p^2=1+p`, `q^2=1+q`, and `pqp=qpq`. Its dimensions are
`1,phi,phi,phi^2,phi^2,phi^3`. These relations reproduce the published
TT3 table (the last two length-two words are dual to one another).

For each odd simple z of E use the free bimodule F(z)=A z A.
Free/forgetful adjunction gives

`dim Hom_AA(F(z),F(w)) = dim Hom_E(z,A w A)`.

In the order z=(a,a^3,ar,a^3r), exact multiplication in E gives the Gram
matrix

```
1  1  3  3
1  1  3  3
3  3 13 13
3  3 13 13
```

Every simple odd bimodule occurs in some F(z), by adjunction. A nonnegative
integer factor B with G=B B^t therefore records all underlying-object
multiplicities. Since the first diagonal entry is one and the first two
rows coincide, there is one column Y with first two entries (1,1), whose
last two entries must both be 3. The residual last two equal rows have
squared norm 4. Up to column permutations there are exactly two possibilities:

- one further column X=(0,0,2,2)^t;
- four further columns each (0,0,1,1)^t.

For an A-bimodule, its dimension in D is its underlying dimension in E
divided by dim(A)=1+d. Thus Y has dimension
`(2+6d)/(1+d)=2phi^2`. In the first alternative X has dimension
`4d/(1+d)=2phi`. In the second alternative each of the four remaining
simples would have dimension `2d/(1+d)=phi`. The latter is impossible:
tensoring such a simple with p would give an odd object of dimension
phi^2, whereas no nonnegative integer combination of phi and 2phi^2
is phi^2. Therefore the odd component has precisely X,Y of dimensions
2phi,2phi^2.

Dimension equations now uniquely force left and right multiplication
by either p or q on (X,Y) to be the same matrix
`F=[[0,1],[1,1]]`. For example pX=Y and pY=X+Y; comparing rational
coefficients of 1 and phi proves uniqueness. Hence the other neutral
actions are F^2 for pq and qp, and F^3 for pqp. Each odd simple is
self-dual, because duality preserves the grading and dimension and these
two dimensions are distinct. Frobenius reciprocity therefore uniquely
forces all odd-odd products: the coefficient of a neutral basis element
z in X_i X_j is `(N_z)_(i,j)`, where N_z is its action on (X,Y).

This determines all 512 structure constants without using the target
tensor. The program `tt3_morita.py` reconstructs this tensor from the
TT3 word relations and these forced module matrices, verifies
associativity, recomputes the free-bimodule Gram matrix from E, and checks
an exact based isomorphism with R8_3_715. In the model basis
`(1,p,q,pq,qp,pqp,X,Y)` the source-to-model map is
`[0,3,4,6,2,7,1,5]`.

Thus R8_3_715 is unitarily categorifiable. The Morita-dual specialization
and its census identification are derived here; no claim of historical
novelty for the resulting category is required.
