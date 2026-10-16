# Independent audit of the R314/R432 pointed-support obstruction

Reviewed `TWISTED_HALF_BRAIDING_OBSTRUCTION.md` and
`verify_twisted_half_braiding.py` on 16 October 2026. Both ordinary and
optimized Python replays passed; receipts are the adjacent
`twisted_half_braiding_independent{,_optimized}.json` files.

**Verdict: the proof gives a general complex categorification obstruction
for both source rings. No pivotality or unitarity hypothesis is used.**

## Transport of the right module action

The source identities make (-)⊗X a genuine equivalence from D to the
complementary left module category M: it takes distinct simple objects
bijectively to all simples of M. It is fully faithful on the scalar
endomorphism spaces, and thus on all morphisms by semisimplicity.
The coherent right D action then becomes right tensoring by a strong
monoidal functor F. Its prescribed permutation of the four simples
makes F an autoequivalence. This step gives coherent natural crossings
X a→F(a) X, rather than mere objectwise identifications.

## Multiplication and the F/F² transport

The two right crossings give X² a→F²(a) X². Because the decomposition
C=D⊕M is a direct sum of D-bimodule subcategories, restriction to M
preserves the right-action coherence. The M component is zX with
z=1⊕g. Replacing X a by F(a)X and using the fully faithful left-module
equivalence gives eta_a:zF(a)→F²(a)z, with the tensorator equation
displayed in the proof. Equivalently this comes from the bimodule functor
D_(F²)→D_F obtained by projecting multiplication.

Applying a strong monoidal quasi-inverse to F changes this to an
F-twisted central structure on F^(-1)(z). The monoidal unit/counit
identifications give F^(-1)F²≅F; they do not require F²≅Id. Since F
fixes both pointed simples, transporting F^(-1)(z)≅z preserves the
two distinct simple support labels. Thus equation (4) has the asserted
naturality and tensor-product coherence.

## The support-label contradiction

At r, the twisted central isomorphism has no diagonal blocks, because
r and gr are nonisomorphic. Both off-diagonal blocks are isomorphisms.
Tensor-product coherence at r⊗r therefore makes two exchanges of the
z support label. Every associator and every tensorator tensored with z
preserves its label: this is precisely naturality with respect to the
two idempotent projections of z=1⊕g. It remains true when r⊗r has
several simple summands, and does not require any scalar or strict
associator normalization.

For a nonzero inclusion r→r⊗r, naturality then compares a nonzero map
landing in support label i with a nonzero map landing in support i+1.
Both are nonzero because the inclusion is split and the crossed maps
are isomorphisms. Orthogonality of the direct-sum projections makes
their equality impossible. This is an intrinsic categorical
contradiction, not a condition on a selected gauge.

## Finite inputs

The verifier binds both tensors, checks all neutral products, the full
left/right complement stability, the regular module bijection, the right
action permutation, the module component of X², and the unique support
permutations. It checks the actual r→r² coefficient. There is no solver,
search cutoff, numerical tolerance, or conditional assertion in the
verification path.
