# A general pivotal odd-isotypic lemma

Let C be a pivotal fusion category over C. For a morphism f:V→V*, write its pivotal transpose as t(f)=f*∘j_V, where j is the pivotal structure. If f is an isomorphism with t(f)=εf, ε∈{±1}, and a self-dual simple S occurs oddly in V, then ν₂(S)=ε.

Indeed, on the S-isotypic block f is a nondegenerate form f_S⊗B, with t(f_S)=ν₂(S)f_S. Thus Bᵗ=(ε/ν₂(S))B. A nondegenerate alternating complex form has even dimension, so odd multiplicity forces ε=ν₂(S). This argument is independent of braiding, positivity, and unitarity.

Two useful forms give uniform consequences.

1. If X is self-dual, the palindromic word X^⊗n has form f_X^⊗n, with transpose sign ν₂(X)^n. Thus every self-dual simple S occurring oddly in X^⊗n satisfies ν₂(S)=ν₂(X)^n. Reversing the tensor factors introduces no braiding because all factors and all morphisms are identical.

2. More generally, let X be arbitrary and let Y be self-dual. Then every self-dual simple S occurring oddly in X⊗Y⊗X* satisfies ν₂(S)=ν₂(Y). This statement does not require X to be self-dual. Suppressing only the standard associativity and dual-tensor coherence maps, use

   F=j_X⊗f_Y⊗id_(X*): X⊗Y⊗X* → X**⊗Y*⊗X* = (X⊗Y⊗X*)*.

   Direct transposition gives

   F*∘j_(X⊗Y⊗X*)
   = j_X⊗(f_Y*∘j_Y)⊗(j_X*∘j_(X*))
   = ν₂(Y) F,

   since pivotal compatibility says j_X*∘j_(X*)=id_(X*). Apply the first paragraph. In particular, every self-dual simple occurring oddly in X⊗X* has positive second indicator.

The explicit adjoint-word transpose identity was independently audited by the rank-six categorical reviewer on 2026-10-16. For the base pivotal-transpose description of ν₂, see Ng–Schauenburg, Higher Frobenius–Schur indicators for pivotal categories, Contemp. Math. 441 (2007), and EGNO, Tensor Categories, the sections on pivotal structures and indicators.

These are necessary sign constraints in a pivotal category. For a general complex categorification, pivotality must first be supplied by a valid theorem or a Galois pseudo-unitarity reduction; the lemma itself does not prove pivotality.
