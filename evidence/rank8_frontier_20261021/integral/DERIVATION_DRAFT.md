Superseded by the completed and independently reviewed proof in PROOF.md.

# Draft: structural reduction of R8_3_3344 to group theory

**Unreviewed working derivation. No general exclusion is certified yet.**

Let C categorify R8_3_3344, and let D be the subcategory on indices
0,1,2,6,7. The tensor is the Rep(A5) tensor, simple as a based ring and
of dimension60. ENO09 Theorem9.12 implies D is tensor equivalent to
Rep(A5), without a unitarity assumption. Let M be the full additive
subcategory on indices3,4,5. It is preserved by left and right D actions.
The left action of either dimension3 object is J3, so M is indecomposable
as a left module, and in particular as a D-bimodule. The right action is
the same. The five action matrices are I,J,J,I+J,2J-I.

Because Rep(A5) is symmetric, D-bimodules are modules over
Rep(A5 x A5). The classification of indecomposable modules gives
M=Rep_alpha(K), for K a subgroup of A5 x A5 and a multiplier alpha.
The dimensions of its three projective irreducibles form a positive
common eigenvector of the left action. J forces this vector to be
(q,q,q). Hence |K|=3q^2.

Write H1,H2 for the projections of K. If either projection is A5,
Goursat's lemma and simplicity give either a graph of an automorphism
of A5 (both projections A5) or a direct product A5 x H. In the graph
case every multiplier sector of A5 has at least4 irreducibles (ordinary
rank5, spin rank4). In the product case H^2(A5 x H,C*) splits as the
product of the two Schur multipliers because A5 has no characters;
projective irreducibles factor, giving at least4 again. Thus neither
projection is A5.

The multiplication spectrum of the left dimension3 object is 3,0,0.
On a twisted representation ring the spectrum of multiplication by an
ordinary representation is its character evaluated on the alpha-regular
conjugacy classes. The A5 character of degree3 vanishes only on the
3-cycles. Thus each projection contains an element of order3. The proper
subgroups of A5 containing order3 are C3,S3,A4 (up to conjugacy).
Consequently |K| divides a product of two numbers in {3,6,12}. Combined
with |K|=3q^2, this leaves |K|=3,12,48.

Now take A=Fun(A5) in D and the Morita dual E={}_A C_A. Its diagonal
part {}_A D_A is Vec(A5), with60 invertibles. Its other part N={}_A M_A
is the module category obtained from Rep_alpha(K) by the regular
algebra Fun(A5 x A5). K acts freely on A5 x A5, so it has exactly
3600/|K| simples. The left/right A5 actions are transitive jointly,
therefore their FP dimensions are constant. E has dimension360,
so N has dimension300 and each simple has dimension
sqrt(300 |K|/3600)=q/2.

|K|=3 gives dimension1/2 and is impossible. |K|=12 makes E pointed.
For |K|=48, both projections must be A4 and Goursat gives
K=A4 x_{C3} A4, with kernels V4 in both factors. The Vec(A5) left
action on N has stabilizer V4, so all75 simples X of N have dim2
and XX* is precisely the sum of the four invertibles in that stabilizer.
The adjoint E_ad is therefore pointed. It contains V4 and its conjugates
under A5, so E_ad=Vec(A5). E is a faithful graded extension of Vec(A5)
of index6. Each homogeneous component is an invertible Vec(A5)-bimodule.
An invertible bimodule over Vec(G) has stabilizer kernels that are abelian
normal subgroups of G. A5 has no nontrivial such subgroups, so all such
bimodules are bitorsors (60 simples of FP dimension1). This contradicts
the dimension2 simples in N. Thus |K|48 is impossible, E is pointed,
and C is group-theoretical.

## Separate group-theoretical exhaustion still being checked

Any GT model has presentation C(G,omega,H,psi), |G|360. The center of
R3344 has no invertibles (ring G(C)=1, universal grading trivial), so
G has no nontrivial linear characters and must be perfect. The only
perfect group of order360 is A6. H must also be perfect because the
identity double coset is Rep(H), hence H=1,A5,A6. The endpoints have
wrong dimensions/rank. The two A5 classes are interchanged by an outer
automorphism, reducing to the point stabilizer.

Need complete relative H3(A6,A5;C*) calculation. Expected: H2(A6)->H2(A5)
is onto; kernel H3(A6)->H3(A5) has order2, represented by the already
certified mu2 stable class. Transfer kills primes except2,3. Sylow3 is
C3^2 and its C4 normalizer rotates coordinates; invariant H4 integral
classes are spanned by x^2+y^2 and restrict nontrivially to the coordinate
C3 in A5, ruling out the3-primary kernel. The2-primary kernel is killed
by2 and can be computed by stable mod2 cohomology on D8 and V4, with
H2-restriction included to handle Bockstein ambiguity.

If this expected calculation holds, all presentations reduce to the
untwisted case (rank9) or the old mu2 model R3342. The latter has all
three diagonal off-sector coefficients2, whereas R3344 has all three3.
