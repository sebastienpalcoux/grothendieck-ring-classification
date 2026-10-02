# Independent review of three rank-seven equivariantizations

The three constructions are unitary categorical models, with every fusion coefficient checked against the census under the recorded permutations.

## R7_2_1

Take `TY(C3, chi(a,b)=exp(2 pi i ab/3), +1/sqrt(3))` tensored with `Vec(C2)`. If `d(X)` is the TY parity, the involution is `(X,e) -> (I(X),e+d(X))`, where `I` inverts C3. The TY associators are invariant under inversion, and the pointed factor has trivial associator. The parity identity makes the canonical permutation tensorators monoidal; their square is the identity. This is a coherent unitary action.

The fixed invertibles give four one-dimensional objects. Two free orbits of invertibles give two two-dimensional objects, and the free orbit of the two odd TY objects gives one object of dimension `2 sqrt(3)`. Its square has multiplicities `[1,1,1,1,2,2,0]`: the fixed output fibers have an involution of trace zero, and the free output fibers have dimension two. All 343 coefficients agree under `[0,5,1,2,4,3,6]`.

## R7_2_195

Take the diagonal parity subcategory of the same TY category tensored with `Vec(C4,omega)`, where `omega(a,b,c)=i^(a floor((b+c)/4))` for labels 0 through 3. Simultaneous inversion of C3 and C4 has tensorator `i^J(a,b)`, with exponent matrix

```
0 0 0 0
0 0 0 3
0 3 2 1
0 1 0 0
```

Independent exact arithmetic verifies all 256 pointed cocycle equations, all 64 tensor-functor coherence equations, and all 16 square-coherence equations. The action has identity square comparison. In particular, `J(2,2)=2`, so the tensorator on the fixed degree-two invertible squared is -1; its two equivariant lifts have order four. This changes the invertible group to C4. The fixed fibers in the square of the odd orbit still have trace zero, so all other orbit multiplicities have the stated values. The complete tensor agrees under `[0,6,1,2,5,3,4]`.

## R7_4_2

Let S3 act on Q8 by sending each imaginary quaternion basis vector `e_a` to `sign(p)e_(p(a))`. These signed permutation matrices have determinant one and preserve quaternion multiplication. Both central elements are fixed, while the six noncentral elements form a free orbit. This is a strict unitary action on `Vec(Q8)`.

The fixed elements give two copies of the three irreducible S3 representations, of dimensions 1,1,2. Let X denote the object from the free orbit, of dimension six. For either central output in X squared, the six ordered pairs form the regular S3 representation. Each noncentral output has four ordered pairs and trivial stabilizer. Thus

`X^2 = sum_(z=+1,-1; rho in Irr(S3)) dim(rho) (z,rho) + 4 X`.

The other products are ordinary S3 character products, and `(z,rho) X = dim(rho) X`. All 343 coefficients agree under `[0,5,4,1,2,3,6]`. A second reviewer independently derived the quaternion action and all orbit-fiber multiplicities.

These checks establish explicit equivariantization models. No inference of associator existence from an associative fusion tensor is used.
