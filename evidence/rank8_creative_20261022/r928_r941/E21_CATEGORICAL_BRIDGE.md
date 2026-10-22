# The E21 graph is the fusion graph of a unitary category

This note supplies the categorical existence input for the independent exact tensor
identification in `../r982`. It does not infer categorification merely from an
associative graph algebra.

Let \(N\subset M\) be the local conformal inclusion associated to
\(SU(3)_{21}\subset (E_7)_1\). Either chiral alpha-induced system, closed under
subobjects and finite sums, is a rigid unitary tensor category of finite-index
endomorphisms of \(M\). Denote it by \(\mathcal E\). Its unit is the identity
endomorphism. Its fundamental alpha-induced object has fusion graph
\(\mathcal E^{(24)}\), also denoted \(\mathcal E_{21}\) when the level rather than
the height is used as subscript.

The original computation is J. Böckenhauer and D. E. Evans, *Modular Invariants,
Graphs and alpha-Induction for Nets of Subfactors. III*, **Commun. Math. Phys. 205**
(1999), 183–228, [arXiv:hep-th/9812110v2](https://arxiv.org/abs/hep-th/9812110),
[DOI](https://doi.org/10.1007/s002200050673). In §6.4, the E^(24) example begins
on manuscript p.51. Manuscript p.52 gives the 24 irreducible chiral sectors and
their decompositions; p.53 states surjectivity of alpha-induction on the fusion
ring and gives its fundamental fusion graph in Figure13. These are computations
inside the actual endomorphism categories, not a proposed nimrep alone.

An independent later source is D. E. Evans and M. Pugh, *SU(3)-Goodman–de la
Harpe–Jones subfactors and the realisation of SU(3) modular invariants*,
**Rev. Math. Phys. 21** (2009), 877–928,
[arXiv:0906.4252v2](https://arxiv.org/abs/0906.4252). Manuscript pp.4–5 identify
the inclusion as local/type I and identify its chiral graph with the E^(24)
nimrep. Manuscript p.26 again identifies both the M–N and alpha graphs with
the stated graph. Table1 on p.45 records the type-I realization.

For explicit unitary cell data, see D. E. Evans and M. Pugh, *Ocneanu Cells and
Boltzmann Weights for the SU(3) ADE Graphs*, **Münster J. Math. 2** (2009),
95–142, [arXiv:0906.4307v2](https://arxiv.org/abs/0906.4307), §14,
Figure16 and Theorem14.1, manuscript pp.39–41. The theorem gives the unique
cell system up to equivalence for E^(24).

## Why the exact graph reconstruction identifies a category

Suppose a based fusion ring has a designated unit basis vector \(e_0\) and a
fundamental object with multiplication matrix \(G\). Its dual has matrix
\(G^t\). If the vectors \(p(G,G^t)e_0\) span the whole vector space, and
\(G\) and \(G^t\) commute, each basis vector is represented by such a polynomial.
Consequently its multiplication matrix is the same polynomial in \(G,G^t\).
Thus the graph, its unit, and this cyclicity calculation determine the entire
fusion algebra uniquely. This is a linear-algebra argument; it uses existence of
the category only to identify the resulting algebra with categorical fusion.

The independent calculation in `../r982` verifies precisely this cyclicity for
the 24-vertex E21 graph, reconstructs all 24 multiplication matrices, and checks
every one of the 512 entries of the neutral rank-eight tensor against R8_3_982.
The neutral triality component is a full fusion subcategory of \(\mathcal E\),
and therefore inherits its unitarity. The triality argument and the dimension
calculation are also independently recorded in `../unified`.

No braiding on the whole chiral category or on its neutral component is asserted.
The two chiral systems have a relative braiding, while their intersection is the
local sector category; this distinction is explicit in the original paper.

## A useful algebra object supplied by the construction

If \(V\) is the fundamental object in the degree-one component of
\(\mathcal E\), then \(V\otimes V^*\) belongs to the neutral component and has
its canonical connected separable algebra structure. The E21 fusion tensor gives
\(V\otimes V^*=1+X_5\) in the canonical R982 labelling. Thus the algebra whose
module equations had survived the preceding search is realized by this model.
The corresponding module category is the degree-one component; it is an
invertible bimodule over the neutral component. Its dual category is accordingly
equivalent to the same neutral component. This observation does not by itself
construct a categorification of R928 or R941.
