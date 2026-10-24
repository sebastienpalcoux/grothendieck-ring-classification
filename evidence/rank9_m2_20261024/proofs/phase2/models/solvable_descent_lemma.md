# Solvable descent with trivial universal grading

Let C be a nontrivial solvable fusion category with C_ad=C. Then C is a
G-equivariantization for some cyclic group G of prime order. Consequently
there is a Tannakian subcategory Rep(G) in Z(C) whose forgetful image embeds
fully faithfully in C. If the invertible group of C is C_p, necessarily G=C_p.

Indeed, Etingof--Nikshych--Ostrik, *Weakly group-theoretical and solvable
fusion categories*, [arXiv:0809.3031](https://arxiv.org/abs/0809.3031),
Proposition 4.4(3), realizes C by a sequence beginning at Vec, each step an
extension or an equivariantization by a cyclic prime group. A final nontrivial
extension would be a faithful nontrivial grading of C, contradicting C_ad=C.
The final step is therefore an equivariantization. Its canonical central
Rep(G) embeds in C; its p invertible characters form a subgroup of Inv(C).
This proves the last assertion and supplies a genuine Tannakian lift,
without an additional braiding or boson assumption. Section 2.6 of the same
paper gives inverse de-equivariantization and the canonical reconstruction
(C_G)^G ≃ C. Theorem 1.6 supplies solvability whenever FPdim(C)=p^a q^b.

For the known unitary rank-five category LPR-24 this applies directly.
Liu--Palcoux--Ren,
[arXiv:2010.10264v5](https://arxiv.org/abs/2010.10264v5), Section 4.4,
construct unitary associators for the ring with basis 1,g,z,x,y and rules

- g²=1, gz=z, gx=y, gy=x;
- z²=1+g+z, zx=zy=x+y;
- x²=y²=g+z+x+y, xy=1+z+x+y, x*=y.

Its FP dimensions are 1,1,2,3,3. The product xx*=1+z+x+y already places
z,x,y in the adjoint subcategory, and z² then places g there. Thus C_ad=C.
Its invertible group is C2, and its global dimension is 24. The lemma yields
an actual coherent C2 action on a unitary category B with C≃B^{C2}.
De-equivariantization identifies 1 and g, splits z into two invertibles a,a²,
and identifies x,y with a simple m of dimension three. Hence

    a³=1, am=ma=m, m²=1+a+a²+2m.

The induced C2 action exchanges a and a² and fixes m. Its equivariantization
has precisely the LPR-24 rules above, so the required action includes the
nontrivial information in the duality x*=y. No unverified lifting of a
based-ring automorphism is used. This is a categorical input for the model
construction owned by phase2/group_models, not by itself an asserted rank-nine
model match.
