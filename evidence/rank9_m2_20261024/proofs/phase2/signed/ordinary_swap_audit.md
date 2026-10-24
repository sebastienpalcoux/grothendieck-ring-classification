# Independent categorical audit of the ordinary-swap model

**Verdict: approved as a unitary model of `R9_2_1983`.**

The construction uses an existing unitary category and genuine central
condensation/equivariantization operations. Existence is not inferred from
associativity of the resulting integer tensor or from its forgetful map.
I checked the model derivation in `phase2/models/ordinary_swap.md`, its
constructor, and the prior equal-phase diagonal-fermion theorem in the
rank-six manuscript, Section 6, “A diagonal fermion with a fixed point”.

The published half-E6 input is Aasen--Lake--Walker,
[arXiv:1709.01941v2](https://arxiv.org/pdf/1709.01941), Sections 7.1--7.2 and
Appendix D.1. Equation (240) explicitly gives the fermionic central lift of
the invertible object, including its negative self-braiding and the `-i`
half-braiding on the noninvertible. Equations (235) and (467) give the
pivotal/action normalization used in the inherited fixed-point calculation.
These are data of the actual half-E6 category; no formal generalization to
uncategorified near-group parameters is admitted.

## Descent and the ordinary swap

The algebra `A=1+(f,f)` is the regular algebra of the diagonal central
Tannakian C2 subcategory. Factor swap is an ordinary unitary tensor functor
on the Deligne product, preserves this central algebra, and the identity
algebra equivariance obeys its C2 coherence. Hence it descends to an actual
C2 action on the module fusion category `Q`.

On the fixed object `(x,x)`, the two A-actions are `+(t,t)` and `-(t,t)`.
Ordinary factor swap preserves each tensor. There is no super interchange
sign here: this is the Deligne product of ordinary fusion categories.
Thus the two resolutions `u,v` are separately fixed, while `a,a'` are
exchanged. Their non-self-dual resolution is the one supplied by identical
half-E6 factors with equal local rotation phase, as required in the existing
theorem. Replacing one input by its conjugate would change the argument.

## The central lift really is equivariant

This point deserves a fuller explanation than a bare ring-level commutation
claim. The central objects `z1=(f,1)` and `z2=(1,f)` both centralize A:
their monodromy with its nontrivial summand is the product of two fermionic
minus signs, hence `+1`. Their free A-modules consequently acquire descended
half-braidings with **every** A-module. In the central local-module
construction, `z2=z1*(f,f)` and the condensed object `(f,f)A` is the unit.
It follows that `z1 A` and `z2 A` are isomorphic as central objects of Q.

Factor swap exchanges these two central objects. Their underlying module is
the simple invertible `g`. Its module-isomorphism space is one-dimensional,
so every nonzero module isomorphism between them is a scalar multiple of a
central isomorphism and is therefore central too. In particular the displayed
map exchanging `e0,e1` is central. It squares to the identity for the
ordinary algebra equivariance. It therefore equips `g` with a coherent
equivariant **central** structure. The natural central functor from
equivariant central objects of Q to `Z(Q^C2)` gives the asserted central lift
of `t`. This justifies commutation with all simple classes in the target,
not only in its pointed subcategory.

## Why the lift has order four

The scalar computation can be derived directly from balancing, rather than
assumed. In the pointed part, right multiplication by the algebra generator
exchanges `e0,e1`. Its left action is the negative of this, because the
central half-braiding of `(f,f)` with either homogeneous component is `-1`.
Thus balancing requires `mu(1,j)=-mu(0,j+1)`, with indices modulo two;
right A-linearity requires `mu(i,j+1)=mu(i,j)b`. With `mu(0,0)=1`, these give

```
mu00=1, mu01=b, mu10=-b, mu11=-1.
```

Simultaneously exchanging both indices negates all four values. The
tensor-square equivariance of the chosen lift of g is therefore the
nontrivial character epsilon of C2, not the unit equivariance. Consequently
`t^2=epsilon` and the four invertibles form C4. The independent arithmetic
audit checks balancing, right linearity, and this swap sign on each pair.

## Completeness of the fusion-rule derivation

The two equivariant structures on each fixed simple differ by epsilon.
Therefore `t` acts transitively on the four simples above u and v; its square
exchanges the two structures above a fixed underlying object. The object X
above the free orbit `{a,a'}` is fixed by every invertible. These facts and
the forgetful functor force the displayed X-products coefficient by
coefficient. Centrality of t supplies both left and right formulas.

The square of one chosen Y contains one odd power of t, one X, one even
translate of Y and one odd translate of Y. Rigidity and Frobenius reciprocity
force the exponents to satisfy `b+c=a (mod 4)`. The four possibilities form
a single orbit under `Y -> t^r Y`; the constructor's normalization
`(a,b,c)=(1,2,3)` therefore loses no categorical possibility. These relations
determine every product and are independent of the target census tensor.

The reconstructed category is unitary because the input categories,
central separable algebra, swap action, and equivariantization are unitary.
Fresh verification passes all fusion axioms, all 486 forgetful identities,
and all 729 coefficients under the stated source-to-model permutation.
The independent checks and tensor digests are in `ordinary_swap_audit.json`.
