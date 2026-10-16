# Exact terminal obstruction for the cyclic near-group ring K(C4,8)

Run `python verify.py` from any directory. Python, SymPy, and NumPy are required. SciPy is used by an archived discovery function but is not imported or called by this replay.

This package extracts one complete tensor and its certificate from the earlier `Rank5_Unified_Frontier.zip` (SHA256 `057aff6c4f910136a4486eeb65b0fa69020560d40d2ab9a6a1257de8a4cb54cb`). It is not the later complete-through-20 archive. The five Python modules and four mathematical source files are unchanged members of the earlier archive. Their hashes, the full source-container hashes, and the later published rank-five PDF used for comparison are recorded separately in `provenance.json`.

The verifier independently constructs the complete K(C4,8) tensor, identifies it with the archived tensor, checks the based-ring axioms, regenerates all six central-support branches at height six, and verifies all integer separating inequalities. The four separating values are -800, -220, -320, and -80. The remaining two balanced branches force the nonintegral fusion coefficient 1/2. No floating-point discovery or optimization enters acceptance.

The mathematical input is the cyclic-four central-support criterion in `papers/cyclic_support.tex`, supported by the finite joint relative-trace lemma in `papers/finite_indicators.tex`. In the current rank-five PDF this is Theorem 6.3, with the same k=2 branch allocation. The proof applies to arbitrary complex fusion categories: Thornton's Theorem 1.3 first supplies a pseudo-unitary Galois conjugate of any near-group categorification. The criterion then excludes this conjugate. It assumes neither a braiding on the original category nor an initially chosen pivotal structure.

This is a terminal input for the new R8_2_170 inverse-Morita argument. It does not by itself identify that rank-eight tensor, perform the grading twist, or construct its algebra object; those categorical steps are recorded in the surrounding proof and independent audit.
