# Exact structural restrictions on five frontier rings

This file records construction-family and braided-category obstructions. It does
**not** assert that any of these five rings lacks a general complex fusion
categorification. The accompanying verifier binds every assertion about a ring to
its full source tensor and records explicit basis witnesses.

## The adjoint subcategory

For each of R65, R439, R567, R901 and R1463, repeatedly closing the supports of
all products `X X*` under multiplication yields all eight simple objects. Thus
the adjoint subcategory of any categorification is the whole category. Every
faithful group grading consequently has trivial grading group. This excludes
all nontrivial faithful group extensions, in particular crossed products, as
constructions of these specific categories. It does not exclude their being
Morita equivalent to a graded category.

## Fibonacci subcategories: R901 and R1463

Each ring has exactly one nontrivial basis element `t` with `t²=1+t`: source
index 5 for R901 and 7 for R1463. Multiplication by `t` partitions the basis
into four regular Fibonacci pairs `(a,t a)`. In any based-ring factorization
`Fib ⊗ B`, the simple objects of the complementary factor are necessarily the
four `a` with `N[t,a,a]=0`. These bases are, respectively, `[0,1,2,7]` and
`[0,1,3,6]`. They are not closed under multiplication: R901 has
`N[1,1,3]>0`, and R1463 has `N[3,3,4]>0`. Therefore neither ring is a
Deligne product of a rank-two Fibonacci/Yang--Lee category with a rank-four
category. Uniqueness of `t` rules out a different identification of the factor.

They also admit no braided categorification, including nonunitary ones. If a
braiding existed, its restriction to the rank-two subcategory D would be
nondegenerate: the only fusion subcategories of D are Vec and D itself, and D
cannot be symmetric, since symmetric fusion categories are integral whereas
the nontrivial FP dimension here is `(1+sqrt(5))/2`. The nondegenerate
subcategory factorization theorem would give `C = D ⊠ D'`, contradicting the
explicit failure of the only possible complementary basis to be closed.
This argument uses no pivotality or nondegeneracy hypothesis on C.

Precise primary statements: Drinfeld--Gelaki--Nikshych--Ostrik,
[On braided fusion categories I](https://arxiv.org/pdf/0906.0620),
Corollary 2.46 (symmetric fusion categories are integral), and Theorem 3.13
(factorization by an arbitrary nondegenerate fusion subcategory). In particular,
commuting basis elements in an unbraided category have **not** been assumed to
commute coherently or define a central subcategory.

## The generalized near-group R65

The invertibles are cyclic of order four. For `g=1`, the source indices of
`1,g,g²,g³` are `[0,1,7,2]`; for `rho=5`, the orbit is `[5,3,6,4]`, and

`rho² = 1 + 3 rho + 3 g rho + 2 g² rho + 3 g³ rho`.

Thus the noninvertible FP dimension satisfies `d²=1+11d` and is
`d=(11+5 sqrt(5))/2`. The invertible action on the four noninvertibles is free
and transitive. By Schopieray,
[Irrational braided generalized near-groups](https://arxiv.org/pdf/2212.14009),
Theorem 1, an irrational braided generalized near-group category is a pointed
factor times one of the two indicated adjoint quantum-group categories. The
noninvertible FP dimension is therefore either `(1+sqrt(5))/2` or
`1+sqrt(2)`. Their minimal polynomials, `x²-x-1` and `x²-2x-1`, differ from
`x²-11x-1`. This excludes a braiding for R65 over C, but it does not classify
unbraided generalized near-group categories.

## Two S3-invertible generalized near-groups: R439 and R567

Both rings have six invertibles forming the nonabelian group S3 and two
noninvertibles in a transitive orbit with C3 stabilizer and common dimension
`d=3+2 sqrt(3)`. Their rings are already noncommutative, excluding braidings.
Neither is a C2-equivariantization of **any** complex near-group category of
type C3+6. Indeed a based C2 action on the neutral near-group ring acts on its
C3 either trivially or by inversion. For the trivial action all four simples
are fixed; the vanishing of `H²(C2,C*)` gives two equivariant simples above
each, hence rank eight. The six invertibles then form a central extension of
C3 by the character C2, and so form an abelian group, not S3. For the inversion
action, the unit and noninvertible are fixed and the other two invertibles
form one free orbit: the equivariantization has rank five, with dimensions
`1,1,2,d,d`. These alternatives exhaust based actions; a failure of a based
action to lift coherently only reduces the possible constructions.

There is no near-group C3+6 fusion subcategory in either tensor, and, more
strongly, the full adjoint closure already forbids a C2 crossed extension.
This corrects a tempting dimension-only identification: the actual crossed
product retains the near-group coefficient 6 in its neutral component,
whereas the two census rings have exact maximum coefficient 3.

The general equivariantization orbit description and dimension formula are
given in Burciu--Natale,
[Fusion rules of equivariantizations of fusion categories](https://arxiv.org/abs/1206.6625),
Theorem 2.12 and Corollary 2.13. This argument is independent of whether the
underlying category or its action is unitary.

## Replay and scope

```
python evidence/rank8_frontier_20261021/structural_models/verify_structural_scope.py
python -O evidence/rank8_frontier_20261021/structural_models/verify_structural_scope.py
```

Both default invocations are read-only. The JSON receipt retains
`general_complex_outcome: unresolved` separately from every restricted
construction-family outcome. No statement here exhausts arbitrary Morita
duals, noncentral condensations, or multistep extension/equivariantization
chains.
