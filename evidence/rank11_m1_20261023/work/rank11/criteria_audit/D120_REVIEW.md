# Final independent review of the dimension-120 obstruction

Verdict: the categorical proof and the finite hypothesis replay pass.

The root-owned `induction/verify_dimension120.py` was read in full and executed
successfully in ordinary Python and under `python -O`. It rechecks the exact
source tensor, field irreducibility, eleven distinct scalar homomorphisms,
every character product, the positive dimension character, the complete central
dimension multiset, the two required values χ(g)=1, Bgg=11, the involution
orbits, the closed small subcategory, and both de-equivariant dimension lists.
The two saved low-frame solutions and their search completeness are not used.

Three rank inferences were challenged explicitly:

1. For A=1⊕g, adjunction gives Hom_A(F_A(X),F_A(Y)) of dimension
   δ_(X,Y)+δ_(X,gY). Thus distinct g-orbits cannot identify after
   de-equivariantization. A free orbit yields one simple; a fixed simple
   yields precisely two, interchanged by the sign automorphism of A and hence
   of equal FP dimension. The rank16 conclusion is exact.
2. The dimension24 small subcategory only needs closure and type1²,2,3².
   R82 is not Rep(S4), because its two dimension-three simples form a dual
   pair. De-equivariantization nevertheless has type1³,3; its unique
   dimension-three simple is self-dual and forces the C3+2 table. No
   categorification of the original small subring has been silently fixed.
3. An identity class in BrPic(K) is the regular K-bimodule category, not merely
   a Morita-equivalent category with unspecified rank. Since C5→BrPic(K) is
   trivial, each homogeneous component has exactly four simple objects.
   Therefore the competing rank20 conclusion is justified.

The central Rep(C5) lies inside the actual center after de-equivariantization,
and each of its simple objects forgets to the unit, by decomposition of the
images of A and B and positivity. This supplies a faithful grading rather than
only a formal C5 action. The twisted BrPic bound uses Marshall–Nikshych's
arbitrary-cocycle exact sequence, not an untwisted calculation.

An additional independent categorical review by the structural agent found no
remaining gap in the same chain. The TeX fragment and bibliography were
compiled in a standalone wrapper to check syntax and citation keys.
