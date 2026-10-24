# Seven restored unitary models

The earlier lower-positive registry omitted the known unitary half-E6 fusion
ring with simples 1,f,x and x²=1+f+2x. These seven rank-nine rings must therefore
be realized, not excluded by that registry. The constructions below use the
unitary half-E6 category E, including its specified central fermion f, from
Aasen-Lake-Walker, Section 7: https://arxiv.org/abs/1709.01941.

| Ring | Unitary construction | Exact record |
| --- | --- | --- |
| R9_2_71 | E⊠Ising | product_models.json |
| R9_2_79 | E⊠Rep(S3) | product_models.json |
| R9_2_499 | E⊠PSU(2)_5 | product_models.json |
| R9_2_2020 | E⊠Vec(C3) | product_models.json |
| R9_2_1218 | Fermionic Ising-parity zest of E⊠Ising | ising_zest_models.json |
| R9_2_96 | Central-fermion shear equivariantization, selfdual odd lifts | shear_models.json |
| R9_2_1266 | Central-fermion shear equivariantization, dual odd lifts | shear_models.json |

The first four are Deligne products of established unitary categories. Their
tensor constructors are independent of the census and use the standard SU(2)
fusion formula for the even part at level five.

For R9_2_1218, grade E⊠Ising by the Ising parity. Let lambda(a,b)=f^(ab) for
a,b in C2 and define the new tensor product of homogeneous objects by
X⋆Y=lambda(a,b)⊗X⊗Y. The central f has trivial pointed associator and
self-braiding -1. In the usual associative-zest pentagon, the four-cocycle
obstruction is therefore (-1)^(abcd). The normalized scalar three-cochain
omega(a,b,c)=i^(abc) has exactly this coboundary:

  omega(b,c,d) omega(a,b+c,d) omega(a,b,c)
  / (omega(a+b,c,d) omega(a,b,c+d)) = (-1)^(abcd).

Addition in the arguments is modulo two. This identity is checked at all
sixteen quadruples in `ising_zest.py`. Tensoring with central f and using its
half-braiding gives the comparison maps; multiplying the associator by omega
makes its pentagon commute. All scalars have unit modulus and the input is
unitary, so this is a unitary fusion category. The multiplication changes only
odd-by-odd products, multiplying their output by f. This gives the recorded
exact tensor. The construction is an application of associative zesting with
an explicit obstruction trivialization; it does not assert the existence of
a braided zest. A general reference is Galindo-Mora-Rowell,
https://arxiv.org/abs/2311.17255, Section 3.

The two shear actions, their coherences, all fusion rules and the proof that
both odd duality types occur are given separately in `shear.md`.

`verify_restored_models.py` reconstructs all seven models, checks every based
fusion-ring axiom, compares all 7×729 source coefficients using the exact
basis permutations, and checks the sixteen fermionic cochain equations.
The shear constructor separately checks 2×486 forgetful tensor equations.
