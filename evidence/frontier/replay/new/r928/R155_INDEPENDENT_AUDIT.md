# Independent audit of R155 connected-algebra and dual-rank arguments

29 October 2026. This audit concerns §§1 and3 of
`../r155/MORITA_RING_RIGIDITY.md`, not an independent reconstruction of the
inherited spherical/Galois or central-lift theorems.

The argument checks out under its stated pseudo-unitary and module-trace
premises. In particular:

* Connectedness makes every pointed free module simple. The pointed support
  is its stabilizer and has multiplicities0 or1. The two excluded order-two
  associator restrictions leave precisely H={1} or{1,h}. The selfdual
  Frobenius internal end has equal X,Y coefficients, so A_k,B_k are exhaustive.
* For B_k, positivity of q=2+8k-2k² bounds k by4. For k=1,3 each nonzero
  residual coefficient sum is a positive multiple of7 but is smaller than6.
  For k=2, the sum of squares of coefficient sums is36, each sum is a positive
  multiple of3, and the only alternative to four sums3 would be one sum6.
  That alternative forces a=b=3 and violates total inner product8. Equality
  in the remaining norm bound makes the four vectors two(1,2), two(2,1).
  Their internal-end dimensions force A_1. For k=4, norm2 and zero mixed
  product force two X and two Y residual simples; each has internal-end
  dimension1 and therefore makes the module category regular.
* In §3 the module regular-object formula has normalization vᵀv=8. It yields
  sum p²=36,sum pq=24,sum q²=18. The four central lifts give four distinct
  invertible dual simples, because their action matrices differ. After their
  removal, Cauchy equality32*18=24² forces p:q=4:3, including the fact that
  any remaining q=0 would have p=0 and hence cannot be a nonzero object.
  Integrality gives (p,q)=t(4,3), with positive integer t; sum t²=2 means
  exactly two nonpointed simples, both of dimension4+3sqrt2.
* A selfdual simple has a symmetric action matrix. Odd u+v=3 makes that
  impossible for either large simple, so they are dual to one another.
  This step does not require faithfulness of the entire dual based-ring
  representation. The pointed actions fix/exchange these two distinct
  matrices as stated. Frobenius reciprocity and dimensions then give
  ZZ*=1+h+4(Z+Z*); the matrix product gives uv=2, selecting(1,2),(2,1).

No additional algebra existence, uniqueness of module structures, tensor
self-equivalence in the A_1 case, or nonexistence of R155 follows from this
argument. The note correctly limits the conclusion to Morita **based-ring**
rigidity for the pseudo-unitary representative.
