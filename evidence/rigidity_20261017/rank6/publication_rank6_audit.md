# Independent review of the rank-six necessary conditions

**AI-generated research · independent verification pending.** This is an independent AI review, not human verification or Lean formalization.

**Verdict: PASS within the stated necessary-condition scope.** The two categorification problems R6_4_155 and R6_8_1660 remain unresolved. The reviewed arguments neither construct compatible associators nor exclude all hypothetical categories.

## R6_4_155: odd cyclic Clifford factorization

The proof uses the existing anticommuting stabilizer hypothesis, with no self-duality or unitarity assumption. Pair insertion is an involution by the normalized module actions. Adjacent insertions anticommute on their shared tensor factor, while disjoint insertions commute.

Naturality of generalized rotation in the unmoved block transports each ordinary adjacent insertion to the next. The cyclic boundary insertion is defined by conjugation. The identity E^n=theta_Z^(-1) is scalar on the Hom space for a simple central target, so conjugation closes after n steps. For any two insertion positions, a cyclic relabelling places both away from the boundary; their commutation sign is then the local adjacent/disjoint sign. No braiding on the underlying category is introduced.

For odd n the F2 adjacency form of the n-cycle has one-dimensional radical: the equations v_(j−1)=v_(j+1) force all coordinates equal. Its twisted group algebra is therefore two full matrix blocks of size 2^((n−1)/2). The central product of all generators is preserved by cyclic permutation, so rotation preserves the two blocks rather than interchanging them.

The model A_j=i gamma_j gamma_(j+1) realizes one block and its simultaneous negative realizes the other. An odd cycle has determinant one. Its spin lift has exactly one sign with nth power one; the sign-vector formula with division by two modulo n gives precisely this normalization. Both blocks have the same cyclic spectrum. The quotient of normalized rotation by the spin implementer acts on multiplicity spaces, has order dividing n, and yields the stated nonnegative integral convolution. Every power of an odd permutation cycle has only odd cycles, so no orthogonal eigenvalue is −1; the spin traces are nonzero. Hence the convolution matrix is invertible over Q.

The path version has n−1 generators and commutator rank 2 floor((n−1)/2). Thus every ordinary simple multiplicity in Y^n has the required power-of-two divisibility. The displayed cubic identity forces m even. The quartic identity gives the n=4 base case, and the fifth-power identity, multiplied by x^(n−5), gives the recurrence for every n>=5. For even m its three terms have valuations at least

```
2+floor((n−2)/2), 3+floor((n−4)/2), 2+floor((n−5)/2),
```

each at least floor((n−1)/2). The cases n=1,2,3,4 start the induction, and duality gives the same result for y. The proof includes m=0.

The independent replay checked all 1,144 blocks and all four invalid-input controls. Normal and optimized runs produced identical receipts. The finite data are correctly described as surviving necessary character constraints; no even-order half-spin result or existence conclusion is used.

## R6_8_1660: all indicators and central phase masses

The saturated projection identity in the existing higher-indicator proof holds for every positive n before its odd-order specialization. The vector w_r lies entirely in the specified multiplicity-one irreducible, and the projection of the unit basis vector is w_r/4. Thus extending the identity to even n introduces no contribution from an unknown modular complement.

The coherent tensor involution gives equal indicators of X and gX at every order. The pointed g sequence is 1 at even orders and 0 at odd orders. The Ising modular formula with theta_sigma=exp(3 pi i/8) has exactly four contributing fusion pairs. They cancel at odd orders and give sqrt(2) cos(3n pi/8) at even orders; at n=2 this is −1, as required. Substitution into the two rational coefficient rows gives the two linear equations in the manuscript and their displayed solution. The period divides 48 because every actual central twist has order dividing 48.

The center-indicator formula gives D nu_n(X_i)=sum_k M_i(k) zeta_48^(kn), so its inverse has the factor D/48 and the negative Fourier exponent exactly as displayed. The two sets of support exponents are conjugate. Positive spherical dimensions and faithfulness exclude an object at any phase with all six masses zero.

At each spin phase, M_sigma and the fixed spin-column dimension give exactly two sigma-containing simples. Neither can be self-dual: a self-duality on its restriction would require the same sign to agree with both the odd sigma multiplicity (indicator −1) and the odd T multiplicity (indicator +1). Since ribbon duality preserves twists and all base simples are self-dual, the two objects form a dual pair with equal columns. Their combined X+gX contribution exhausts that phase mass, forcing b=c=2 from the separate masses. These columns exhaust all six coordinates. Positivity and faithfulness exclude additional sigma-free objects in the phase. Thus the exact total fiber size two is justified.

For the remaining phases, expansion of the dimension-weighted masses in the basis 1,sqrt(2) gives the five Gram moments. Rational independence gives the separate b and c equalities. The homogeneous rows have sum(q−a)^2=0, forcing q=a individually.

The phase-allocation argument accounts for phases 0 and 24 before allocating the remaining inventory: the six unit-induced columns exhaust all six phase-0 masses, and their four forced charge-even fermion partners exhaust all six phase-24 masses. I checked these four exact vector equalities independently, for both low frames. Hence no unallocated twist-one or twist-minus-one object is discarded.

The 640-profile claim is confined to its exact finite input domain of 1,136 labelled restriction profiles. The independent verifier constructs all local five-moment allocations by coefficient convolution and uses exact complement intersections for global allocations. Its Cauchy inequality pruning is necessary for any remaining sum of nonnegative rank-one Gram contributions. Per-type bounds and global inventory checks make the domain finite and complete. Every passing discovery witness is checked for all five moments and its full inventory. The independent receipt gives 68+286+286=640. No unknown modular complement, fusion coefficients or associators are inferred from these profiles.

## Arithmetic and primary-source checks

The root agent's independent SymPy audit checks all 288 phase masses per conjugate choice, every inverse Fourier round trip, all 48 Ising values and the dimension-field basis. My separate exact arithmetic audit checks division by d, all spin-phase mass exhaustions, all ten Gram rows, the homogeneous phase list and both low-frame phase-0/24 exhaustions. It uses rational coordinates in Q(sqrt(2),sqrt(3)), without importing the discovery arithmetic.

Primary sources read directly for this review:

- Ng–Schauenburg, *Congruence Subgroups and Generalized Frobenius–Schur Indicators*, https://arxiv.org/abs/0806.2493, Section 2 and especially Lemmas 2.5–2.7. These give the composition and inverse-twist rotation conventions used above.
- Ng–Schauenburg, *Frobenius–Schur Indicators and Exponents of Spherical Categories*, https://arxiv.org/abs/math/0601012, Theorem 4.1 (center-indicator formula) and Theorem 7.5 (modular indicator formula).

The checker replays certify the specified arithmetic identities. This review checks the categorical deductions from the established manuscript inputs. Neither is a formal proof assistant certificate, and both residual categorification questions remain open.
