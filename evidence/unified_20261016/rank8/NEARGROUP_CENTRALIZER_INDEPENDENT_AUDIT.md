# Independent audit: R8_2_820 and R8_2_869

**Conclusion: both proposed unitary realizations pass the independent audit.**

The source is D. E. Evans and T. Gannon, *Near-group fusion categories and their doubles*, [arXiv:1208.1500](https://arxiv.org/abs/1208.1500), Proposition 6, Table 2, Proposition 7(b), and the paragraph immediately following Conjecture 2. Printed pages in the arXiv PDF are 29–31 and 46–48.

Proposition 6 asserts three C*-fusion categories with near-group rules C5+5. Table 2 separates the first, already constructed in Izumi's work, from two additional conjugate categories. The table records G'=C3×C3 for the first case, with Q'(x,y)=(x²+y²)/3, and G'=C9 for the other two cases, with Q'(x)=±2x²/9. The paragraph following Conjecture 2 explicitly establishes the claimed center data for the finite odd cases through order 13 and identifies the exceptional C3×C3 entry. Therefore using n=5 is within the established finite result; it does not assume Conjecture 2 for arbitrary n. We rely on this published finite center identification, not merely on the existence of abstract modular data in Proposition 7(b).

The five objects a_g are invertible and their restricted S matrix has phases exp(2πi·2mgh/5), where m=1 or 2. This pairing is nondegenerate. Their Müger centralizer inside the actual unitary Drinfeld center is thus a unitary modular category. Its objects are exactly

    a_0, b_0, c_{1,-1}, c_{2,-2}, d_{0,γ}   (γ∈(G'\{0})/±).

There are eight objects. This follows directly from the simple-current monodromy phases in Proposition 7(b), or from its S matrix: the a,b,d indices must be zero and a c pair must sum to zero. Every object in this centralizer is self-dual, so the source's all-lowered fusion coefficients are the ordinary fusion tensor in this basis.

I derived the entire tensor independently from the printed fusion formulas in Proposition 7(b), without using the other verifier's S matrix or Verlinde calculation. With B=b_0, C_x=c_{x,-x}, and D_γ=d_{0,γ}, the nonunit coefficients are determined by symmetry and

- N(B,B,B)=N(B,B,C_x)=N(B,B,D_γ)=1;
- N(B,C_x,C_y)=1+δ_{x,y}, N(B,C_x,D_γ)=1, N(B,D_γ,D_η)=1−δ_{γ,η};
- N(C_x,C_y,D_γ)=N(C_x,D_γ,D_η)=1;
- N(C_x,C_y,C_z)=1+Σ_{s,t=±1}δ_{x+sy+tz,0 mod 5};
- N(D_γ,D_η,D_κ)=1−Σ_{s,t=±1}δ_{γ+sη+tκ,0 in G'}.

The integer-only verifier reconstructs these formulas, checks all associativity equations and all 512 tensor entries after a basis permutation, and binds the original census tensors by immutable SHA-256 digests. Its first maps are:

| G' | Census | Model-to-source labels |
|---|---|---|
| C3×C3 | R8_2_820 | (0,2,6,7,1,3,4,5) |
| C9 | R8_2_869 | (0,3,6,7,1,2,5,4) |

For C3×C3 the representatives are (0,1),(1,0),(1,1),(1,2); for C9 they are 1,2,3,4. The first two representatives may be interchanged without changing the fusion tensor.

Replay: `python verify_neargroup_centralizer_independent.py --repo <repository-root>`. Both normal and `python -O` receipts pass and agree. Files `neargroup_centralizer_independent.json` and `neargroup_centralizer_independent_optimized.json` record the checks.
