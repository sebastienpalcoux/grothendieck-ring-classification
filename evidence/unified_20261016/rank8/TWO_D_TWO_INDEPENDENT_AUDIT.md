# Independent audit: four general 2D2 graph-pair exclusions

Verdict: PASS. The explicit coordinate convention has been incorporated into the manuscript proof. The categorical bridge does not assume that the hypothetical category is unitary, pivotal, or spherical. The checked algebraic certificate concerns the complex generator equations, not a search restricted to self-adjoint solutions.

## Exact source-tensor hypotheses

`verify_2d2_source_graphs.py` independently reads the complete census, restores the multiplicity-two indexing, binds each tensor to the decision-ledger SHA-256, and checks the faithful C2 grading, all 64 neutral coefficients, both internal ends, and both rooted module graphs. Normal and optimized Python produce identical PASS receipts.

The fixed graph has edges 01,12,23,24,35,45,56,67, rooted at 0. Even vertices are 0,2,5,7. The source identifications are:

| Census ring | Graph vertices 0,...,7 to source labels | (1,g,r,gr) | X |
|---|---|---|---|
| R8_2_152 | (0,1,5,3,4,7,2,6) | (0,6,5,7) | 1 |
| R8_2_153 | (0,1,5,3,4,7,2,6) | (0,6,5,7) | 1 |
| R8_2_166 | (0,3,7,1,2,6,4,5) | (0,5,7,6) | 3 |
| R8_2_495 | (0,2,6,4,5,3,7,1) | (0,1,6,3) | 2 |

For every row, XX*=X*X=1+r, g²=1, gr=rg, and r²=1+2r+2gr. The object r generates the entire neutral category. Both incidence matrices N_(a,X)^m and N_(X,a)^m are the displayed graph; in particular the principal graph pair is (2D2,2D2), with both complete even parts of rank four. The graph is connected, so X generates the full odd module.

Writing d=2+sqrt(5), phi=(1+sqrt(5))/2, and delta=sqrt(3+sqrt(5)), its positive PF vector in graph order is

    (1,delta,d,delta*phi,delta*phi,d,delta,1).

The verifier checks the PF equations in Q(sqrt(5)) after dividing odd weights by delta. Equal weights at the two depth-three vertices are therefore established independently of any pivotal assumption on the original category.

## From an arbitrary category to an algebraic shaded planar algebra

Let D be the neutral rank-four category and M the odd component. Schopieray's two-dimension Galois pseudo-unitarity lemma applies to D. A field automorphism of C realizing this conjugacy can be applied to the entire category and its module structure. This preserves all the based multiplicities above. Thus D can be equipped with its positive canonical spherical structure. No spherical structure on the original rank-eight category is inferred.

Schaumann, arXiv:1206.5716v3, Proposition 5.8 (printed page 30), supplies a module trace on M with positive FP weights. Theorem 4.5 (printed pages 20–21) is stronger than a statement about the dual diagonal category: it constructs the double-adjoint isomorphism for every module functor between any two traced module categories and proves compatibility with composition. Applied to D and M, it therefore equips the entire category of D-module endofunctors of D direct-sum M with a pivotal structure. This explicitly justifies the linking-category step. Corollary 4.6 gives compatibility with the dual action, and Proposition 5.10(iv) gives the spherical dual.

The module-trace scale is chosen so that the fundamental object corresponding to X has both loop values delta. This is possible because the displayed positive PF vector satisfies both adjacency equations. Under the action on D direct-sum M, the two-shaded linking category maps faithfully to matrix endofunctors. Semisimple resolutions of the identity give the path-matrix representation. Choosing dual bases with respect to the nondegenerate trace gives the usual graph cup and cap coefficients. Faithfulness follows because a nonzero natural transformation is nonzero on some simple object. Thus the resulting shaded planar algebra embeds algebraically in the graph planar algebra of 2D2.

This is precisely the algebraic part of the pivotal construction in Grossman–Morrison–Penneys–Peters–Snyder, arXiv:1810.06076: Theorem 3.45 explicitly concerns pivotal multitensor categories without a star, and Theorem 3.70 explicitly includes the nonunitary setting. The cup/cap computation of Theorem 3.75 uses the chosen evaluation and coevaluation coefficients; dual bases give both maps directly without taking one to be the adjoint of the other. Their final Theorem 3.77 is stated with dagger hypotheses and is not being cited as an unrestricted embedding theorem.

## The generator and the complex certificate

At depth three, f3 P3 f3 is Cp direct-sum Cq. Its primitive idempotents have equal trace because their PF weights agree. Consequently T=p-q has T²=f3 and trace zero. The trace pairing is nondegenerate, and P3=TL3 direct-sum CT. Pairing any cap of T with every element of P2 proves uncappability: the corresponding cups lie in TL3. Rotation preserves the trace-orthogonal complement of TL3, so T is a rotational eigenvector. This step uses a bilinear trace pairing, not a Hermitian inner product.

Morrison–Penneys, arXiv:1406.3401, Lemma 3.2 explicitly rules out the two primitive cubic rotational eigenvalues for an uncappable solution of T²=f3 in the 2D2 graph planar algebra; that lemma has no self-adjointness hypothesis. I also independently replayed the new portable `verify_gpa_omega_certificate.py`: over Q(sqrt(5),omega), it reconstructs the rank-144 linear constraints and all 90 distinct square equations, then verifies that an explicit constant linear combination of five of them is 1. This excludes both primitive cubic roots algebraically. The two-click rotation has order three, so these and 1 exhaust the possibilities.

I read and replayed `two_d_two/verify_gpa_certificate.py`. It independently generates all 152 loop coordinates and all path-matrix square equations; checks the rank-144 cap/rotation system; and verifies both directions of equality between the square-equation ideal and its seven displayed normal forms using explicit degree-at-most-three polynomial identities. All arithmetic is in Q(sqrt(5)), without a conjugation condition. For the normalization, if p=(p0,p1,p2,p3), put A_p=sqrt(w(p1)w(p2)); then T_rect=A T_spherical A^(-1). This makes the TL projector entries w(p_i)/sum_neighbor w, the cap kernels unweighted sums, and the two-click rotation coefficient w(v0)w(v5)/(w(v2)w(v1)). These are exactly the formulas reconstructed by both portable verifiers. The added Laurent-family checks identify every solution as one of two signs of T(lambda), lambda nonzero, and verify the opposite primitive winding weights of the two free coordinates. An oriented-edge character implements lambda by a graph planar algebra automorphism because interior edge factors cancel. The base solution is self-adjoint in spherical path coordinates, as checked by the diagonal weight ratios.

## Why higher-depth data cannot escape the argument

After graph gauge, the unknown planar algebra contains the subalgebra generated by the self-adjoint base solution. Morrison–Penneys Lemma 3.4 and Theorems 7.8–7.9 establish that this generated subalgebra is the known unitary 2D2 planar algebra. Its positive box dimensions equal the rooted-loop dimensions of 2D2, which are also the dimensions of the unknown planar algebra. Therefore the two subalgebras coincide in every positive box space. One-click rotation identifies all positive-degree negative box spaces, and both zero-box spaces are C. This excludes extra higher-depth data without applying a positivity-based jellyfish theorem to the hypothetical planar algebra.

The known dual graph in Morrison–Penneys Theorem 7.9 has level sizes (1,1,1,2,4,1); hence its even rank is 1+1+4=6. The source-bound graph pair above has both even ranks four. Planar-algebra equality cannot preserve these incompatible ranks. All four source tensors therefore have no fusion-category categorification over C.

The conclusion does not classify every category with the rank-four 2D2 fusion ring. It applies to categories carrying the specific 2D2 module graph, which is forced by each of the four tensors.

Primary source URLs:

- https://arxiv.org/pdf/1206.5716
- https://arxiv.org/pdf/1810.06076
- https://arxiv.org/pdf/1406.3401

