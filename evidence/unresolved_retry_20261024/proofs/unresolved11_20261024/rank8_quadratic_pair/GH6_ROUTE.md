# A precise higher-multiplicity Haagerup route for R8_3_1768

## Status

This is a **conditional construction route and a necessary associator
restriction**, not a categorification. Two complete based-module actions,
and four pairs of commuting actions, are certified below. Neither an
associator for the higher-multiplicity Haagerup ring nor a separable algebra
on `1+rho` is supplied.

In particular, a prospective model must use a nontrivial pointed
associator. An untwisted cyclic higher-Haagerup category cannot realize the
specified Morita route. The full census ring remains unresolved.

## 1. The candidate ring and the forced module

Let `H=GH(C6,2)` be the based ring with basis `a_g,b_g=a_g rho`, for
`g in Z/6`, and rules

```
a_g a_h = a_(g+h),
a_g b_h = b_(g+h),
b_g a_h = b_(g-h),
b_g b_h = a_(g-h) + 2 sum_k b_k.
```

Thus `rho=b_0` is self-dual and `rho^2=1+2 sum a_g rho`. Put
`u=6+sqrt(37)`. The positive dimension of every `b_g` is `u`, and

```
u^2=12u+1,
FPdim(H)=6(1+u^2)=444+72sqrt(37)=FPdim(R8_3_1768).
```

Suppose a category with this ring has a connected separable algebra whose
underlying object is `A=1+rho`. For the induction functor `X -> X A`,
Frobenius reciprocity gives the Gram matrix

```
                 [ I6       I6    ]
       M M^t  =  [ I6    I6+2 J6  ].
```

The first six rows of a nonnegative integral factor must be distinct unit
vectors. After removing those six coordinates, the last six rows have
squared norms two and pairwise inner product two. Equality in
Cauchy-Schwarz makes them all the same vector, which is the sum of two
distinct unit vectors. Consequently the factor is unique up to column
permutation:

```
                 [ I6       0 ]
           M  =  [ I6    J6x2 ].
```

There are eight simple right modules: six `m_g=a_g A`, and two more,
`x,y`. The group acts regularly on the first six and permutes `x,y`.
The matrix of `rho` is necessarily

```
                 [ F6      J6x2 ]
          Q   =  [ J2x6       C ],
```

where `F6` is the inversion permutation and `C` is a symmetric,
nonnegative integral two-by-two matrix. The relation
`rho^2=1+2 sum a_g rho` forces both row sums of `C` to be eleven.
If the group fixes `x,y` separately, the remaining eigenvalue `lambda`
of `C` would be an integer satisfying `lambda^2=12lambda+1`, impossible.
The action on `x,y` is therefore the parity quotient `C6 -> C2`.
The same quadratic relation now gives `lambda^2=1`. Exactly two matrices
remain:

```
                [6 5]               [5 6]
          C+ =  [5 6],         C- =  [6 5].
```

These calculations require only Frobenius reciprocity and the based
fusion relations. They are valid as necessary conditions for a general
complex fusion category, without unitarity assumptions.

## 2. Completing the corresponding R1768 module actions

The published complete induction-factor list already contains the
candidate algebra object `1+X3`, of dimension `1+u`, as candidate 7,
factor 2. Its rank-eight induction matrix `B`, in module-by-source
convention, is

```
1 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0
0 0 1 1 1 1 1 1
0 0 1 1 1 1 1 1
0 1 0 0 0 0 1 0
```

The previous file left its full action undetermined. Here we complete
that action exhaustively. This is a refinement of the necessary-data
list, not a proof that this algebra exists.

The rank of `B` is five. Its transpose kernel has the mutually orthogonal
basis `e1-e2,e3-e4,e5-e6`, each of squared norm two. The pointed object
`g=X1` has nontrivial associator and acts freely; after permuting the
identical rows of `B` its unique possible action is

```
     g = (0 7)(1 3)(2 4)(5 6).
```

On the three-dimensional kernel this is
`G=[[0,1,0],[1,0,0],[0,0,-1]]`.
The source actions are symmetric because every source simple is
self-dual. If `L_i` is the regular source action, their determined part is
`A_i=B L_i B^+`, and every possible action has the form

```
          A_i + (1/2) U H_i U^t,
 H_i = [[a,b,c],[b,a,-c],[c,-c,d]],
```

where the columns of `U` are the three displayed kernel vectors.
The six rational characters of R1768 are verified explicitly in the
script. Its other two characters are the conjugate positive-dimension
characters in `Q(sqrt(37))`. They cannot occur on the kernel: both take
`g=1`, but that eigenspace of `G` is one-dimensional over `Q`, so every
rational matrix preserving it has a rational eigenvalue. Thus the six
rational characters give a rigorous spectral bound for every entry of
`H_i`.

For generators `X2,X3,X4`, imposing this bound and nonnegative integral
full entries leaves respectively `2,4,4` possible matrices. Testing all
32 triples against all 64 multiplication relations leaves **exactly two
complete actions**. They are distinguished, for example, by the image
algebra dimensions six and five. Every matrix is saved in
`gh6_route_verified.json`.

## 3. Exact commuting higher-Haagerup actions

For both R1768 completions, put

```
 p = [3,4,7,2,0,6,5,1]
```

in image-list permutation convention. Its six-cycle on the small objects
is `(0 3 2 7 1 4)`, and it transposes `5,6`. For each choice `C+` or `C-`
in Section 1, use the corresponding inversion matrix `Q` in this cycle
coordinate system. The exact checks give

```
 P^6=I,    QP=P^-1 Q,
 Q^2=I+2 sum_(j=0)^5 P^j Q.
```

All twelve matrices `P^j,P^j Q` commute with all eight R1768 matrices.
Enumerating all720 permutations of the six small objects, with the forced
transposition on the large pair, finds precisely two compatible C6
generators: `p` and its inverse. Both choices of `C` work for each source
completion. Thus there are eight marked pairs, or four modulo reversing
the C6 generator. This supplies four explicit representatives of commuting
based actions. It does
**not** supply the mixed module associator or prove Morita equivalence:
these data are necessary decategorified data only.

## 4. The pointed associator is forced in any such categorical route

Suppose that one of these commuting-action pairs is realized by an actual
invertible bimodule category between a category with ring `H` and a
category with ring R1768. Let `[omega_H]` denote its pointed C6
associator. In the canonical identification
`H^3(C6,C*)=Z/6`, it must be class **3**.

First, the two-object orbit `{x,y}` for C6 has stabilizer C3. Restricting
the module category to the pointed subcategory therefore gives
`[omega_H]|C3=0`.

Second, the exact permutation identity is `P^3=M_g`. In the joint pointed
action of `C6 x C2` on the bimodule category, the diagonal involution
`(a^3,g)` fixes every simple object. The module pentagon at a fixed simple
says that the restricted associator is a coboundary. Thus the C2
restrictions of the two pointed associators agree (taking the opposite
on one side does not alter an order-two class). The published general
R1768 pointed-associator theorem gives the nontrivial C2 class.
Hence `[omega_H]|C2` is nontrivial.

For cyclic groups, restriction of class `k mod6` to these subgroups is
`k mod3` and `k mod2`, respectively. The unique solution is `k=3 mod6`.
Equivalently this follows directly from the carry cocycles
`omega_k(a,b,c)=exp(2 pi i k a floor((b+c)/6)/6)` and their cyclic
restriction invariants.

The needed categorical fact about stabilizers is Ostrik, *Module
categories over the Drinfeld double of a finite group*, Example 2.1,
[arXiv:math/0202130](https://arxiv.org/pdf/math/0202130): a module orbit
with stabilizer K requires the associator restricted to K to be a
coboundary. The argument here only uses this elementary necessity, not a
classification of any nonpointed category.

This rules out **the untwisted GH(C6,2), A=1+rho route with these actions**.
It does not exclude the required twisted higher-Haagerup category, nor
R1768 itself. Existing standard untwisted endomorphism constructions
cannot be silently assigned the needed nontrivial pointed class.

## Reproduction and limits

Run `python verify_gh6_route.py` and `python -O verify_gh6_route.py`.
Both pass. Explicit exceptions preserve all checks in optimized mode.
The verifier binds the exact R1768 tensor and published induction-factor
file by hashes; performs the bounded 32-triple completion; checks all
64 source products for each result; and checks all96 commuting actions
for each proposed bimodule pair.

Izumi's *A Cuntz algebra approach to the classification of near-group
categories*, [arXiv:1512.04288](https://arxiv.org/pdf/1512.04288), Sections
10 and 12, does not fill the missing premise here. Its near-group
construction theorems concern specified C*-data and do not assert an
arbitrary twisted GH(C6,2) category or its `1+rho` algebra. In particular,
Section 10's treatment of multiplicity `2|G|` cannot be cited as existence
for the separate parameters `(C36,72)`.
