# A new tensor-quotient obstruction for R6_8_1660

Status: a structural necessary theorem, not a categorification or a nonexistence theorem for the ring. No current center-profile count changes.

## Theorem

Let C be the established pseudo-unitary Galois form of a hypothetical categorification of R6_8_1660, with its positive spherical structure. Every dominant **pivotal** tensor functor F:C→D to a pivotal fusion category is an equivalence.

Consequently there is no proper unitary tensor quotient of a hypothetical unitary categorification. Here a unitary tensor functor uses the canonical positive pivotal structures, which it preserves.

We do not silently remove the pivotal-functor hypothesis for arbitrary tensor functors. This theorem does not prohibit nontrivial module categories or the three already retained Morita-dual based rings.

## Inputs already proved in the release

The simples are 1,g,X,gX,σ,T=σX, with

    g²=1, gσ=σ, σ²=1+g,
    X²=1+[3(1+g)+4σ]X.

The positive second-indicator signs are

    ν₂(σ)=-1;  ν₂(1)=ν₂(g)=ν₂(X)=ν₂(gX)=ν₂(T)=+1.

Every indecomposable C-module category has six simples, and its Ising restriction has two regular three-object blocks. In each block order the objects as two leaves and a middle vertex. The action of X has the form

    N_X=P⊗I+Q⊗N_g+R⊗N_σ,
    U=P+Q, V=P-Q,
    U=[[a,b],[b,6-a]], R=[[c,f],[f,4-c]].

Up to exchanging the two blocks, the four types are:

| Type | a | b | c | f | Ratio r of second-block to first-block leaf dimensions |
|---|---:|---:|---:|---:|---|
| I | 0 | 1 | 0 | 0 | 3+2√2+2√3+√6 |
| II | 2 | 3 | 2 | 2 | 3−2√2+2√3−√6 |
| III | 1 | 2 | 0 | 1 | √2+√3 |
| IV | 1 | 2 | 1 | 2 | (√2+√6)/2 |

Every listed r is greater than one. The possible V choices affect P,Q but not the two entries used below.

These inputs are in `supplements/rank6/papers/chapters/frontier_1660.tex` and `frontier_1660_morita.tex`.

## Proof

1. View D as a C-module category through F. Dominance makes it indecomposable, so the complete six-object based-module list applies. Tensor functors preserve FP dimensions. Since FPdim(Fσ)=√2<2, the object Fσ is simple. Further Fg cannot be the unit: otherwise (Fσ)²=2·1, contrary to the multiplicity-one unit coefficient in the product of a simple with its dual. Thus 1,Fg,Fσ form a full Ising fusion subcategory of D.

2. The unit of D is a leaf in an Ising block. It cannot be a middle vertex because Fg fixes the middle vertex but Fg⊗1≠1. Normalize the dimension vector at this unit. In the displayed ordering the dimensions are

       (1,1,√2,r,r,√2r).

   The unit must be in the first block: if it were in the other block, the first-block leaves would have FP dimension 1/r<1. All simple objects of a fusion category have FP dimension at least one.

3. In a pivotal semisimple category, let U have a nondegenerate self-duality of transpose sign +1. Every self-dual simple W of sign −1 occurs in U with even multiplicity. Indeed, on the W-isotypic summand a self-duality is a fixed skew self-duality of W tensored with a form on the multiplicity space; for their product to be symmetric, that form must be nondegenerate alternating. Its dimension is even.

   A pivotal tensor functor carries the symmetric nondegenerate self-dualities of X,T to symmetric nondegenerate self-dualities of F(X),F(T). It carries the skew self-duality of σ to a skew self-duality of the **simple** object Fσ. We use this symmetry-type statement, not the false general identity ν₂(FX)=ν₂(X).

4. Let the unit be the first leaf. The coefficient of Fσ in F(X) is the middle-to-leaf entry c of N_X. The coefficient in F(T)=Fσ⊗F(X) is the same entry of N_σ N_X, namely P₁₁+Q₁₁=a. Therefore both a and c must be even. This excludes type III because a=1, and type IV because a=c=1.

5. Type II has a simple object Y with FP dimension

       r=3−2√2+2√3−√6.

   The rational root bounds

       1414/1000<√2<1415/1000,
       1732/1000<√3<1733/1000,
       2449/1000<√6<2450/1000

   give 148/125<r<1189/1000<6/5. In particular 1<r and r²<36/25<2. This is impossible in a fusion category. If Y is noninvertible, YY* contains the unit and at least one other simple, so r²=FPdim(YY*)≥2. If Y is invertible, r=1.

6. Only type I remains. At its first leaf the internal end has coefficients N_Z[1,1]=δ_{Z,1}, hence R_F(1)=1 for the right adjoint R_F of F. The tensor-functor projection formula gives

       R_F F(Z) ≅ Z⊗R_F(1) ≅ Z.

   Thus F is fully faithful. Since it is dominant, it is a tensor equivalence. ∎

## A reusable criterion

For a known pivotal fusion category C, a candidate based module can underlie a pivotal tensor quotient only if, at a candidate unit vertex m, the image-column multiplicities of every positive-indicator self-dual source object are even on each negative-indicator self-dual target simple. A simple source whose image remains simple determines the target sign. Apply this before reconstructing the target fusion ring.

The rank-six case uses only one negative target (the Ising spin), two positive sources (X and σX), two nimrep entries (a,c), and the elementary FP-dimension gap (1,√2).

## Primary background sources

- Bruguières–Natale, *Exact sequences of tensor categories*, https://arxiv.org/abs/1006.0569, especially the induced central algebra and projection formula; its primary HTML is https://arxiv.org/html/1006.0569v1.
- Etingof–Gelaki–Nikshych–Ostrik, *Tensor Categories*, author manuscript https://math.mit.edu/~etingof/egnobookfinal.pdf: FP dimensions, tensor functors, and §9.5 canonical spherical structure.
- Penneys, *Unitary dual functors for unitary multitensor categories*, https://arxiv.org/abs/1808.00323, for pivotal functors and standard unitary duals. For the unitary corollary one can also argue directly: a unitary functor preserves the norms of standard evaluation/coevaluation maps, and it preserves FP dimensions; hence their images are standard duality solutions.

## Verification

`verify_tensor_quotient_obstruction.py` checks all twelve raw signed V choices (ten based modules after the two leaf relabellings), the fusion-matrix identities, the two image multiplicities, and the rational dimension-gap certificate, using integer and rational arithmetic. It does not solve associators, reconstruct centers, or claim to exclude the original ring.
