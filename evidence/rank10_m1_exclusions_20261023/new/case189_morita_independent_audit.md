# Independent audit of the R189 regular-algebra Morita reduction

23 October 2026. The argument in `case189/MORITA_REDUCTION.md` is valid. It proves equality of the dual based-ring type with R189, and does not settle categorifiability.

The following points were checked independently.

1. With trivial pointed associator, A=direct sum of the five invertibles is a connected separable algebra. The two right-module simples A and xA are simple by Frobenius reciprocity and exhaust the two free pointed orbits. Their underlying dimensions are 5 and 5d.
2. Left A-actions are equivariant structures for the genuine left C5-action on right A-modules. Both right-module classes are invariant. Vanishing H²(C5,C×) gives five one-dimensional equivariant structures on each. Consequently the bimodule dual has dimension profile 1^5,d^5.
3. Both pointed actions on the five noninvertibles are free, since a nontrivial stabilizer would force five invertibles into YY*, whose dimension d²=1+4d permits only one invertible summand. Thus their commutation automorphism tau is defined. The unique invertible term in x² forces tau²=1; the duality formulas permit a self-dual representative.
4. For tau=-1, associativity gives x²g=gx², and comparing the noninvertible terms forces translation-by-2 invariance of the five coefficients. Their sum is 4, so this case is impossible. For tau=1, self-duality leaves exactly the four triples (4,0,0),(2,1,0),(0,2,0),(0,1,1), up to automorphisms of C5.
5. The first triple supplies an actual rank-two fusion subcategory with rule x²=1+4x, excluded by Ostrik's rank-two theorem. This does not apply that theorem to the right-module category, which lacks an asserted fusion tensor product.
6. For the middle triples, the scalar character formula f=5(1+w²), with w²=1+tw, gives y=f/5 satisfying y²-(t²+4)y+(t²+4)=0. Taking the quadratic field norm gives the stated quartics, respectively y⁴−15y³+60y²−90y+45 and y⁴−20y³+100y²−160y+80. Both are Eisenstein at 5. The supplied exact verifier was rerun successfully.
7. Every center simple of the original category has FP dimension in Q(√5), because its underlying object is a nonnegative integral combination of objects of dimensions 1,d. Braided equivalence of the Morita centers preserves FP dimensions. The commutative formal-codegree induction theorem in the dual produces a center simple of dimension D/f. A quartic f cannot yield D/f in the quadratic field containing the nonzero D. Thus both middle triples are excluded.

Only the R189 triple remains. Equality of based rings does not provide a tensor equivalence, a central lift of an invertible, or a braiding. The stated open gap is genuine.
