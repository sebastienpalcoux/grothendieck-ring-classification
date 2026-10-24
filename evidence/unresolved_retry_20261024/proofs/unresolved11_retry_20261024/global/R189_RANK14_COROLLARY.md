# The rank-fourteen modular candidates are categorifiable

This consequence uses the actual rank-ten category constructed in `R189_INDEPENDENT_MODEL_AUDIT.md`. It does not infer a category from numerical modular data.

## The center argument

Write C=SU(4)_6, B=000+060+202+222, D=C_B, and K for the ten-object fusion subcategory with ring R10_1_189. Its invertibles are g^i=τ_(2i), i modulo 5.

DMNO, arXiv:1009.2117v2, Theorem 3.20, Lemma 3.29 and Corollary 3.30 construct a braided embedding

    (C_B^0)^rev → Z(C_B).

The underlying functor is the inclusion of local modules: this follows directly from the forgetful-functor construction of equation (22), used in Theorem 3.20. Restrict the half-braidings of τ_(2i) from D to K. This gives a fully faithful braided functor from the order-five pointed subcategory into Z(K). Full faithfulness also follows directly: its underlying objects are pairwise distinct invertible simples of K.

In the canonical unitary ribbon structure its quadratic form is the inverse SU(10)_1 quadratic form:

    q(g^i)=exp(−2πi·(2i)(10−2i)/20)=ζ_5^(i²).

The associated bicharacter is ζ_5^(2ij), hence nondegenerate. The universal grading group of K is trivial: x² contains g^ix for i=1,2,3,4; products and duals then generate g and x. Thus Inv Z(K)→Inv K is injective. Consequently this metric C5 is exactly the pointed part of the center.

Müger decomposition now gives an actual unitary modular category E with

    Z(K) ≅ C(C5,q) ⊠ E,
    FPdim(E) = FPdim(K)²/5 = 100(2+√5)².

Applying the previously proved exhaustive conditional metric-C5 reduction to this actual center identifies its modular data with the q=1,c=2 candidate. Reversing the braiding gives the conjugate q=4,c=3 candidate. This last identification depends on the completeness argument and exact calculation in `unresolved11_20261024/rank10_case189/REPORT.md`, §§5,7; it is not a fresh independent verification of every entry of that enumeration.

## A direct WZW realization of the rank-fourteen factor

There is also an independent concrete description. Put J=600, so J has order four, J²=060 and twists θ_J=i, θ_(J²)=1. The algebra L=000+060 is an actual subalgebra of B, as proved in the independent model audit. Form

    Q=C_L^0.

The image of J in Q is an invertible of order two and twist i, so it generates a semion category S. Define E'=S'⊂Q, the Müger centralizer.

Local L-modules arise from SU(4)_6 weights of even 4-ality. Those in E' have 4-ality zero. There are 22 such weights. The action of J² is

    (a,b,c) ↦ (c,6−a−b−c,a).

Exactly two of these 22 weights are fixed: 121 and 303. Each fixed weight splits into two simple L-modules; every nonfixed orbit gives one. Hence

    rank(E')=(22−2)/2+2·2=14.

The quantum Weyl formula gives the following actual simple-object dimensions and twists. Repeated rows at fixed weights denote the two distinct resolved modules.

| Orbit representative | Multiplicity | Dimension | Twist |
|---|---:|---:|---|
|000|1|1|1|
|004, 024|2|1+d|ζ5|
|303 (fixed)|2|1+d|ζ5⁻¹|
|012, 032|2|1+3d|ζ5⁻¹|
|121 (fixed)|2|1+3d|ζ5|
|020|1|2d|ζ5⁻²|
|101|1|2d|ζ5²|
|105|1|d|1|
|113|1|5d|−1|
|202|1|d²|1|

Here d=2+√5. Their squares sum to 100d². The exact arithmetic receipt is `r189_rank14_wzw_receipt.json`; its verifier uses rational arithmetic in Q[t]/(t⁴−5t²+5), with t=2cos(π/10).

The algebra B descends through L to a connected étale algebra A in Q by DMNO §3.6, Proposition 3.16. Its underlying object is 1+U, where U is the nonfixed orbit {202,222}. Both orbits have 4-ality zero, so A belongs to E'. Its dimension is 1+d². Therefore E'_A is an actual fusion category of dimension FPdim(K).

For completeness, its equivalence with K follows from the grading. B has 4-ality zero, so D=C_B inherits the faithful Z4 grading of C. Its neutral part has dimension FPdim(D)/4=FPdim(K). Every object g^i and g^ix in the direct rank-ten construction lies in that neutral part: τ_(2i) has 4-ality zero, while τ_5 and β both have 4-ality two. Thus K is the whole neutral part. Under the module-in-stages equivalence, E'_A identifies with precisely this neutral part, since its underlying C objects have 4-ality zero. Hence E'_A≃K.

Finally Z(E'_A)≃E'⊠((E'_A)^0)^rev by DMNO Corollary 3.30. The local-module factor has dimension five. Thus E' is the concrete WZW realization of the complementary rank-fourteen category above (up to the already specified orientation conventions). This argument also constructs the algebra 1+U that was missing in the previous necessary-data analysis.

Primary categorical reference: A. Davydov, M. Müger, D. Nikshych, V. Ostrik, *The Witt group of non-degenerate braided fusion categories*, https://arxiv.org/pdf/1009.2117, §§3.3–3.7, Lemma 3.29, Corollary 3.30. Conformal branching reference: R. Coquereaux, G. Schieber, *Quantum symmetries for exceptional SU(4) modular invariants associated with conformal embeddings*, https://arxiv.org/html/0805.4678v4, §§1.4.3,1.4.5.
