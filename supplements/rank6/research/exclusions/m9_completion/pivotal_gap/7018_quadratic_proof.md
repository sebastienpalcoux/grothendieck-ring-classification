# R6_9_7018: exclusion of the quadratic signed dimension field

This proof concerns arbitrary complex fusion categorifications, under the intermediate hypothesis that their sphericalization dimension field has degree2. The separate higher-field proof by the Gauss agent excludes degrees4 and6 and completes general nonexistence.

The dimension-field-containment lemma forces E=Q(sqrt5)⊂K and[K:Q]≤6. In the degree2 sector, K=E. The original formal codegrees have polynomials

X²−4225X+21125, X²−150X+1125, X²−30X+45.

Their principal ideals are respectively65sqrt5 O_E,15sqrt5 O_E,3sqrt5 O_E: the relevant unit factors are(29+13sqrt5)/2 and2+sqrt5, both of norm−1. Since the spherical global dimension Δ is divisible by every original codegree, it lies in195sqrt5 O_E. Write

Δ=195sqrt5(x+y sqrt5)/2=(975y+195x sqrt5)/2,
x≡y (mod2), y>0, x²<5y².

Its two embeddings contribute975y to signed Casimir trace, bounded above by original trace4405. Thus1≤y≤4. The quadratic d-number condition is5y²−x² |20y², leaving16 possibilities for(x,y), including rationalΔ whenx=0.

The full tensor modulo2 is F4×F4×F4. The verifier establishes this without a lookup: Frobenius squared is identity, so the algebra is reduced with factors F2 orF4; rank(Frobenius−1)=3 and totalrank6 force threeF4 factors. Therefore every rational character-field summand of the signed algebra has even dimension. Removing the dimension-character fieldE leaves rank4. Since each remaining formal codegree lies inE, the remaining four codegrees partition into two conjugate pairs inE, with a rational pair necessarily repeated. This covers a quartic character field as well: a quadratic codegree then occurs twice at each embedding, or a rational codegree occurs four times.

For eachΔ, let f=(S+b sqrt5)/2 and f'=(S−b sqrt5)/2 be one such pair. SetN=ff'. Necessary conditions are

* N is a positive divisor ofNorm_E(Δ), sinceΔ/f is integral;
* S²−4N=5b², S≡b(mod2), S>2, N>S−1;
* ifb≠0, N dividesS² (the quadratic d-number test);
* bothΔ/f andΔ/f' are integral;
* for the secondpairg,g', allfourcodegrees have sum≤4405−Tr_E(Δ), and
  S/N+(g+g')/(gg')=1−Tr_E(1/Δ).

Ifb=0, S is even and f=f'=S/2 is an integer>1. Every enumeration bound follows from the trace cap; there is no arbitrary cutoff.

Only(x,y)=(±1,1) survives these arithmetic tests. For bothchoices, the six codegrees would have polynomial

(X²−975X+190125)(X²−975X+1125)(X²−975X+7605).

Its reduction modulo2 is(X²+X+1)³. The original Casimir characteristic polynomial modulo2 is(X²+X+1)(X+1)⁴. Signed multiplication matrices have the same reduction as the original matrices, so their Casimir characteristic polynomials must agree modulo2. Contradiction.

`verify_7018_quadratic.py` reconstructs all conditions from the full tensor, explicitly checks every finite branch, and writes `R6_9_7018_quadratic_certificate.json`. Both normal Python and `python -O` replay in about0.33seconds; proof checks do not rely on removable assertions.
