# Exact folded SU(2) tensor identification for R8_2_857

This is a structural identification of a based ring, not a categorification.

Start with the usual level-30 SU(2) labels a = 0,1,...,30 and coefficients

    N(a,b;c) = 1 if |a-b| <= c <= min(a+b,60-a-b) and a+b+c is even;
               0 otherwise.

Restrict to even labels a = 2j and identify the pair a and 30-a. Representatives are j = 0,...,7. Sum the coefficients into these pairs. The resulting eight-label tensor is exactly R8_2_857 under the source-to-representative map

    [0, 1, 3, 6, 5, 4, 7, 2].

Its positive dimensions are sin((2j+1)pi/32)/sin(pi/32) in that source order. The partner invertible in the braided even level-30 category is a fermion. Consequently the based-ring folding alone does not give an ordinary fusion-category quotient. The separate conductor-and-sphericalization proof `../compression/R857_GENERAL_PROOF.md` now excludes any ordinary complex fusion categorification; the structural identification in this file alone would not establish that result.

Primary source: P. Bruillard, C. Galindo, T. Hagge, S.-H. Ng, J. Y. Plavnik, E. C. Rowell, Z. Wang, *Fermionic modular categories and the 16-fold way*, arXiv:1603.09294v3, Section 2.4 (the coefficient-summing quotient) and Lemma 3.7 (the even level-4m+2 category and its fermion). Their Example 2.5 illustrates why such a based-ring quotient need not admit an ordinary fusion categorification. Those source statements alone do not settle the level-30 case.

`verify_r857_fold.py` checks all 512 coefficients against the census tensor and its ledger hash. This identification explains the cyclotomic dimension profile and supplies a concrete family for further work; the general exclusion is proved separately in the compression evidence package.
