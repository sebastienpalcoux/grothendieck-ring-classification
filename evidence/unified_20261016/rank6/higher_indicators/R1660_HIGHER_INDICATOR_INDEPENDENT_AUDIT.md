# Independent audit of the R1660 higher-indicator refinement

Auditor: two_d_two. Status: PASS, as a necessary-condition refinement only.

I read the complete proof and every line of the portable verifier, independently checked the frozen torus/compression inputs, and replayed the new verifier under optimized Python. Receipt: r1660_higher_indicators_two_d_two_O.json.

## Unique irreducible and projection

The prior exact twist-one-support theorem makes the full T-fixed space precisely the six known low constituents. Its torus multiplicities are therefore (3,1,1,1). I independently loaded the frozen torus_spectra.json and compressed_spectra.json and checked that every eligible irreducible containing chi3 or chi6 has one-dimensional T-fixed space. Requiring the exact compressed scalar −sqrt3/6 or −sqrt6/12 leaves exactly the respective pairs (33,4),(36,5) or (54,4),(61,5).

Because the corresponding full torus multiplicity is one, w_r lies in a unique multiplicity-one irreducible W_r and spans its T-fixed line. The orthogonal projection of e_unit onto W_r is itself T-fixed, hence equals w_r/4: its inner product with w_r is1 and the squared norm of w_r is4. This justifies replacing the central-unit vector by that projection before taking the matrix coefficient. It is stronger information than merely a compressed eigenvalue.

The character average (1/m) sum_j chi(T^j S^-1 T^n S) is exactly the trace on that rank-one fixed line of S^-1 T^n S. I checked the group product [[1−jn,j],[-n,1]]. Since the normalized generator of the fixed line is w_r/2, this trace is (1/4)<s w_r,t^n s w_r>, which equals <s w_r,t^n s e_unit>. There is no missing factor4.

## Conversion to indicators

For ell_r(z) the rational sqrt(r) coefficient of z/D, the low-character formula gives (s w_r)_A=4sqrt(r) ell_r(z_A). These coordinates are real, so the Hermitian scalar product gives exactly the indicated sum without a hidden conjugation. The other vector has coordinates theta_A^n z_A/D. Therefore

    sum_i ell_r(d_i) nu_n(X_i)=m_r(n)/(4sqrt(r)).

I checked the weight scalings 24 ell3=(-1,-1,1,1,-1,-1) and 48 ell6=(-1,-1,-1,-1,-2,2). For odd n, setting x=nu_n(X)=nu_n(gX), t=nu_n(T), these yield 2x−t=1+a_n and −2x+2t=1+b_n. Solving gives exactly x=(3+2a_n+b_n)/2 and t=2+a_n+b_n.

## Finite replay and scope

The standard-library cyclotomic field reduction uses z^16−z^8+1 and checks its sqrt2,sqrt3,sqrt6 and cube-root normalizations. The original tensor and already certified finite-group character tables are hash bound. The new replay exhausts all532 irreducible pairs, rebuilds their torus and compression traces, and computes all matrix coefficients by exact class averages.

The two mixed third traces are not sums of three cube roots, as verified independently by enumerating all ten nonnegative multiplicity triples. The two matched choices give nu3(T)=2 and nu3(X)=2+omega or2+omega². Fifth and seventh values also replay exactly and remain compatible necessary constraints. No unjustified reality of third indicators is assumed. The rank-37 existing witness uses a matched choice; this result does not exclude or construct R1660.

Verified script SHA256: 4685289e27543a7eec533d1f99d6c773ae3e6f7ef1e82fb7839a0b7daca41321
