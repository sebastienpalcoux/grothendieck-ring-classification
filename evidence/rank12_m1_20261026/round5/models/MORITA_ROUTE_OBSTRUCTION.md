# Central-invertible obstruction to several model routes

This excludes specific construction routes, not the three fusion rings.
The R623 model is constructed separately in `R623_NEAR_GROUP_MODEL.md`.

Let C have the ordinary C6 generalized-Haagerup rules R326:

    G=C6, rho g=g⁻¹rho, rho²=1+Σ(g∈G)g rho.

Its universal grading is trivial: rho² contains every noninvertible, and
products of these recover every invertible. Thus a central lift of a fixed
invertible, if it exists, is unique; the kernel of Inv(Z(C))→Inv(C) is
Aut⊗(Id_C)=Hom(U(C),C×)=1. An underlying central invertible g must commute
with rho. The free G orbit and inversion mixed rule imply g=g⁻¹, so

    Inv(Z(C)) injects into {1,z}.

For each of the two explicit C6 examples of Grossman–Izumi,
[*Drinfeld centers of fusion categories arising from generalized Haagerup
subfactors*](https://arxiv.org/html/1501.07679v2), Example4.5, there is a
central fermion. Hence their centers have precisely two invertibles, with
the nontrivial one's self-braiding −1.

The previously proved restrictions in
`../../rank12-m1-round4-20261026/c6/C3_central_lift.md` and
`../../rank12-m1-round4-20261026/c6/R623_central_semion.md` say:

* Every categorification of R561 or R628 has a central C3 subgroup.
* Every categorification of R623 has a central semion on z, with
  self-braiding ±i in its pseudo-unitary conjugate.

Categorical Morita equivalence preserves the braided Drinfeld center.
Consequently neither commutative target nor R623 can arise as a Morita
dual, for any algebra object, of either of those two Grossman–Izumi
categories. The argument also applies to their Galois conjugates: −1
remains −1, and the cardinality of central invertibles is unchanged.

The argument for the commutative targets is stronger than this example
list. Every category with either inversion-type ring R326 or R623 has at
most two central invertibles by the same elementary calculation.
Therefore no category with either ring is Morita equivalent to a
category with R561 or R628, whose center has at least three invertibles.
In particular, the new R623 model supplies no Morita route to561/628.

This does not classify all associators for R326. Izumi's Sendai2016 slides
list four C6 generalized-Haagerup solutions, while Grossman–Izumi's
Example4.5 imposes an additional Q-system equation and treats two. We do
not extrapolate its central-fermion assertion to unexamined solutions.

Ordinary Galois conjugation, changing only associator coefficients, and
taking the opposite category also do not turn these inversion rings into
the commutative targets. Grading-based zesting has no nontrivial grading
to use, since U=1. These observations prevent invalid model claims; they
are not noncategorifiability proofs for561/628.
