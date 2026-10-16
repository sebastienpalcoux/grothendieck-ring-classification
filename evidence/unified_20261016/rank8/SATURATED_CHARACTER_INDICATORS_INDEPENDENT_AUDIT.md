# Independent audit of the character-weighted saturated indicator lemma

Auditor: rank6_center. Date: 16 October 2026.

I independently checked `SATURATED_CHARACTER_INDICATORS.md`, including its extension beyond the published fixed-field lemma. The stated formula and the two applications to an arbitrary pseudo-unitary 2D2 neutral category are correct under the explicitly stated saturation hypothesis.

Write ell(z)=p_chi(z/D). In the canonical anomaly-free Drinfeld representation, the exact signed Galois relations give z_pi(A)=epsilon_A D sigma(z_A)/sigma(D) and theta_pi(A)=tau^2(theta_A). Consequently ell_pi(A)=epsilon_A chi(k) ell_A. Applying tau to ell_A z_A therefore introduces the factor chi(k) sigma(D)/D and the reindexed weight ell_pi(A) z_pi(A); the two occurrences of the Galois sign cancel. This cancellation does not require the permutation to be involutive.

A unit k modulo f can be lifted to an exponent coprime to the full cyclotomic conductor: impose the prescribed residue on prime powers dividing f and a nonzero residue at every additional prime. For h inverse to k modulo f, tau(theta_A)=theta_pi(A)^h whenever ell_A is nonzero. This uses theta_A^f=1 outside I(1) and theta_A=1 inside I(1). Zero-weight terms remain zero after permutation. Reindexing the transformed first induction trace and cancelling sigma(D) gives the indicator identity at h. Since inversion permutes the units and chi(h)=chi(k), the conclusion holds for every positive exponent coprime to f. There is no k^2=1 condition and no restriction that tau fix the dimension field.

For 2D2, the dimension-block saturation at conductor 5 and the weights (2,2,-1,-1) give 2+2 nu_2(g)-nu_2(r)-nu_2(gr)=-2. All three nonunit objects are self-dual, so their second indicators are signs; the only solution is (-1,+1,+1). At exponent 3, the same formula gives nu_3(r)+nu_3(gr)=4. Both cubic invariant spaces have dimension two. Each rotation has finite order three, so each trace has modulus at most two. Equality in the triangle bound forces both traces to equal two, hence both rotations are the identity. No assertion that arbitrary self-dual third indicators are real is used.

This audit establishes the lemma and these neutral-category consequences; it does not by itself establish the coefficient-frame theorem or an R24 exclusion.
