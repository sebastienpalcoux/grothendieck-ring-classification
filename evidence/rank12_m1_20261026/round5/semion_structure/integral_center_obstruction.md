# R12_1_623: an integral-center obstruction

This is a necessary restriction, not a categorical exclusion. It is independent
of any possible construction of the ring.

Assume the previously established pseudo-unitary categorification and central
semion lift z. Put d=3+sqrt(10), so d^2=1+6d. The complete previous central
induction analysis supplies thirteen possible integer Gram profiles. All
center-simple dimensions have the form a+b*d with a,b nonnegative integers.
The integral noninvertible dimensions in that list can only be 2 or 4.

The only invertibles of Z(C) are 1 and z. Indeed, the kernel of
Inv(Z(C))->Inv(C) consists of tensor automorphisms of the identity, hence is
trivial since U(C)=1. An underlying invertible g can have a half-braiding only
if it commutes with rho in the based ring. Since rho*g=g^{-1}*rho and the
pointed action on noninvertibles is free, this forces g^2=1 in C6. The known
central semion supplies the nontrivial possibility z.

Tensoring by z has no fixed center simple W. The monodromy M(z,W) is a sign
because z has order two, whereas balancing for zW=W would give
1=theta_z*M(z,W), impossible for theta_z=+/-i.

Now suppose a center simple W has even integral dimension n (necessarily 2
or 4 in the complete profile list). In W*W^*, the unit occurs once and z does
not occur, since zW is not isomorphic to W. Its total dimension n^2 is an
integer. Every available simple dimension has nonnegative d coefficient;
therefore every constituent of W*W^* has zero d coefficient. Apart from the
unit, all such constituents have even dimension. We obtain n^2=1+an even
integer, a contradiction.

Consequently no noninvertible integral center simple can occur. In the old
pair coordinates (p,t), whose simple dimension is 2p+6td, all pair types with
t=0 are forbidden. Exactly six of the thirteen profiles remain: zero-based
indices 1,2,7,8,11,12. The attached standard-library verifier reconstructs
all thirteen tiny Diophantine solutions and checks this restriction.

This proof does not claim that any of the six surviving profiles is realized.
It does not assume that a nondegenerate pointed central subcategory splits
from the original nonbraided fusion category.
