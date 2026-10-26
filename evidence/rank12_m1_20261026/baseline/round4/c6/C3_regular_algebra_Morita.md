# Why the actual regular-C3 Morita construction does not resolve R561/R628

## Statement

Let C be a complex fusion category containing an actual central pointed subgroup H: a fully faithful braided functor Vec_H^b→Z(C), whose composite with the forgetful functor is fully faithful. Assume the pointed associator is trivial, so b is a bicharacter, and assume b is nondegenerate. Let

    A = ⊕_(h∈H) h

with ordinary subgroup-algebra multiplication. Then the actual tensor Morita dual _A C_A is tensor equivalent to C.

The algebra is not required to be commutative in Z(C). In the nontrivial metric C3 cases it is not commutative there. The category C_A of one-sided modules need not be monoidal.

## Explicit proof by alpha induction

Write c_(h,X):h⊗X→X⊗h for the given half-braiding. All multiplication and half-braiding maps below are actual categorical maps. Choose an associative skeletal realization of the pointed subcategory; by the assumed trivial ordinary associator this is allowed. Coherence then supplies the same construction in the original category.

For X∈C, define

    α(X)=A⊗X

with left regular A-action and right A-action obtained by moving the right A factor left past X using the inverse central crossing and multiplying the two A factors. The multiplication of A is a morphism in Z(C), so these actions commute and obey the bimodule axioms.

The comparison

    α(X)⊗_A α(Y) → α(X⊗Y)

moves the middle A factor past X by the same crossing and multiplies. It is balanced; its inverse inserts the unit of A in the second free module. The half-braiding axioms give the tensor coherence. Thus α:C→_A C_A is a strong tensor functor, with α(1)=A.

A left-A-linear map α(X)→α(Y) is uniquely determined by a map

    f:X→A⊗Y,       f=Σ_(h∈H) f_h,       f_h:X→h⊗Y.

Fix k∈H. Naturality of the half-braiding against f_h says, suppressing coherent associativity maps,

    (f_h⊗id_k)c_(k,X)
      = c_(k,h⊗Y)(id_k⊗f_h)
      = b(k,h)(id_h⊗c_(k,Y))(id_k⊗f_h).

The two sides of the right-A-linearity square, evaluated on the k summand of A, therefore differ exactly by b(k,h). Consequently right-A-linearity is equivalent to

    (b(k,h)−1)f_h=0   for every k∈H.

Nondegeneracy of b forces f_h=0 unless h=1. Conversely, every f_1:X→Y defines a bimodule map. Hence

    Hom_(A-A)(α(X),α(Y)) ≅ Hom_C(X,Y),

and α is fully faithful.

The algebra A is connected and separable (the usual group-algebra separability splitting, divided by |H|). Therefore _A C_A is a fusion category Morita equivalent to C and has the same Frobenius–Perron dimension. A fully faithful tensor functor between fusion categories of equal dimension is an equivalence. This proves the claim.

No ambient braiding on C, no symmetric flip on all of C, and no Müger product splitting inside C are assumed.

## Application to R12_1_561 and R12_1_628

The earlier complete central-lift argument forces an actual braided C3 subgroup in Z(C), faithfully embedded under forgetting, with trivial ordinary pointed associator. Its three possible braidings are b_r(a,b)=ζ3^(rab), r=0,1,2.

* r=0 is Tannakian and is already ruled out by the genuine rank4 tensor de-equivariantization obstruction.
* r=1,2 are nondegenerate bicharacters. The theorem above applies to the actual regular algebra A and shows _A C_A≃C.

Thus this proposed Morita step cannot turn either remaining ring into an excluded different fusion ring: in both nonisotropic cases the dual is tensor equivalent to the original category, preserving R561 and R628 individually. In particular it does not produce R623. The one-sided module category has rank4, but it is not the tensor Morita dual and cannot be used as a rank4 fusion categorification.

This is a rigorous explanation of the limitation of this avenue. It supplies neither a model nor a new exclusion; R561 and R628 remain unresolved.
