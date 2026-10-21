# A unitary model for R8_3_475

Let Fib be the unitary Fibonacci category with simple objects 1,tau and
`tau^2=1+tau`. The cyclic permutation of three identical Deligne factors
is a canonical coherent unitary C3 action on Fib cubed. Its
equivariantization is therefore an existing unitary fusion category.
This argument does not assume a lift of an abstract permutation of
simple objects: it uses the actual functor permuting the factors,
with its canonical tensorator and composition isomorphisms.

There are two fixed simple triples, (1,1,1) and (tau,tau,tau). Their
canonical equivariant structures, multiplied by the three linear C3
characters, give simples A_e and B_e for e in Z/3. The remaining six
triples form two free orbits, of Hamming weights 1 and 2. They give
simples P and Q. Thus the equivariantization has exactly eight simples,
with dimensions `1,1,1,phi^3,phi^3,phi^3,3phi,3phi^2`.

To compute a fusion coefficient, equip the underlying multiplicity
space Hom(V_i tensor V_j,V_k) with the induced C3 representation and
take its invariant dimension. The identity trace is exactly the number
of admissible triples of supporting binary words, since every Fibonacci
fusion multiplicity is zero or one. A nonidentity group element has no
fixed word-triple unless each of the three underlying words is a fixed
triple. In the fixed case the multiplicity space is either zero or the
tensor cube of a one-dimensional Fibonacci multiplicity space; cyclic
permutation has trace one, multiplied by the character scalar
`omega^(e_i+e_j-e_k)` (or its inverse, which gives the same average).
Consequently the coefficient is

`(h + trace(g) + trace(g^2))/3`,

where h is the underlying fusion-path count. For three fixed supports
this is h when `e_k=e_i+e_j` and zero otherwise. In all other cases it
is h/3. This determines the entire fusion tensor from the Fibonacci
rule alone.

`fibonacci_cyclic.py` implements this calculation, verifies its integer
coefficients and associativity, and compares all 512 coefficients with
R8_3_475. In model order `(A_0,A_1,A_2,B_0,B_1,B_2,P,Q)`, the
source-to-model bijection is `[0,1,2,5,4,6,7,3]`.

The construction is standard finite-group equivariantization applied
to a canonical permutation action; its exact census identification is
derived here. No classification of categories with matching dimensions
is used.
