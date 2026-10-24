# Independent review of the dimension-504 exclusion

The root reviewer accepts the general-complex exclusion of R9_2_941.
This review checked the categorical argument separately from the finite
calculation. It does not infer a categorical premise from a successful
arithmetic test.

1. Integrality of the hypothetical category makes it pseudo-unitary, with
   positive spherical dimensions. Every central object has an integral
   dimension because its forgetful image is an object of the integral
   category. Modularity gives 504²/z² integral, hence z divides 504.
2. Ostrik, arXiv:1309.4822, Example 2.9 and the paragraph immediately
   before Theorem 2.13 give exactly
   S(A_chi,Z)/dim(A_chi)=chi(F(Z)) for each scalar character. Symmetry
   of S makes S(A_chi,Z)/z an algebraic integer. No commutativity or
   unitarity assumption is hidden in this identity. Commutativity is
   used separately to obtain the multiplicity-free I(1).
3. The dimension-63 congruences are necessary: 56/63=8/9 for the rational
   codegree-nine characters, and 72/63=8/7 for the cubic characters.
   For alpha=2cos(2pi/7), the standard integral basis 1,alpha,alpha²
   makes the latter condition precisely c1=c2=c3=t+a modulo seven.
4. The seven aggregate cases exhaust the nonnegative dimension equation.
   In the two exceptional cases the norm bound fails already in a single
   rational character or the three cubic characters. The bound follows
   from B-vv^T positive semidefinite, not positivity of a *-structure.
   Independent replay does not use the author's candidate enumeration.
5. Every odd divisor other than 63 has zero Y-coordinate. At dimension
   63 the unique constituent of I(1) has restriction V; any others have
   restriction U. The dimension of I(Y) forces an odd number of U's.
   The dimension of each I(C_l) consequently forces an odd number of
   central dimension-nine simples restricting to C_l. Even-dimensional
   central objects vanish from both parity equations regardless of their
   multiplicities, so no classification of their columns is required.
6. Ring simplicity is checked directly. The accepted nonbraided result
   excludes the modular possibility by 49 not dividing 504 and the
   symmetric possibility by the published non-group-like tensor.
   Liu--Palcoux--Ren 2102.01663v4 Theorem 5.1 explicitly applies to
   arbitrary complex fusion categories and makes the center simple.
   ENO 0809.3031 Corollary 7.2 then contradicts the forced dimension-nine
   simple. These implications do not assume unitarity.

Primary statements were checked directly in their source texts. The
shortest source for the central character identity is Ostrik itself;
Deshpande's later generalization is a compatible additional reference.

Replay: `python phase5/root/verify_941_independent.py`.
The original author's `verify_odd_columns.py` additionally checks all 729
coefficients of the published tensor identification and the cubic
characters against the source products.

Conclusion: accepted as a general exclusion, not merely an exclusion
within a particular construction or categorical class.
