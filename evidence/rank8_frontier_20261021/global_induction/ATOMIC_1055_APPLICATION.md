# R1055 full-field atomic spectral exclusion

The general atomic spectral theorem is in ATOMIC_SPECTRUM.md. For R8_3_1055,
all eight characters lie in Q(sqrt37,sqrt(-3)); the primitive generator
sqrt37+sqrt(-3) has polynomial u^4-68u^2+1600. Conjugation fixes sqrt37 and
negates sqrt(-3), and the exact table checks source duality against it.

The full-field integrality filter removes553 high candidates, leaving566
restriction vectors in352 complete duality orbits. The independent
character-labeled low simplices have sizes1534,1534,613,184,184,1515,184.
The height-four operator has211 equations and16695 columns:5748 low choices,
352*31 high phase columns, and35 rotation columns. Full complex S symmetry is
imposed in the four rational field coordinates; no STS factorization outside
the FP field is used. Both possible second-indicator assignments admit exact
full-domain integer separators.

The saved complete general lift has four oriented signed branches, all gauge
equivalent to the original ring. The ordinary spherical character alternatives
are checked separately, including their zero-dimension obstructions and the FP
Galois orbit. Thus this is an exclusion over arbitrary complex fusion categories.
Independent normal and optimized replays verify all16695 columns for both rays.

The result is atomic_spectrum_results/R8_3_1055_h4.json, and the canonical exact
replay is verify_accepted_atomic.py. Independent review:
quadratic/review_atomic_complex_1055.py and ATOMIC_COMPLEX_1055_REVIEW.md.
