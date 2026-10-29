# Independent review of the six-dimensional STS block

The block lemma in `r928/REPORT.md`, section 6, is valid under its stated spectral-projection and matching premises. It gives a necessary phase/matching restriction, not a categorification or ring exclusion.

The projector onto the four H columns is, by the known B3 spectrum,

    S P_H S* = P_f + P_e + P_V,

where H=U direct-sum V, U and V are the two pair-sum and two pair-difference spaces, and e is the selected outside-pair difference. Let F=span(f,e). The four H twists are distinct within their dimension fiber, so all four H labels are self-dual; therefore S^2 is the identity on H. It follows that S maps H onto F+V and maps F+V back onto H. Their intersection V is consequently S-invariant. Unitarity then makes S interchange U and F.

The known image of f is the normalized sum of all four H labels. Since H rows are real, the U--F block is a real orthogonal matrix. After changing the harmless sign of e it is exactly

    R = (1/sqrt(2)) [[1,1],[1,-1]].

Moreover S^2 is the identity on F. On the difference e, the charge-conjugation permutation can act as the identity only when the two selected outside labels are individually self-dual, which validates the real-block treatment; this is not an assumed self-duality of all unknown simples.

For H twists (a,ia,-a,-ia), T exchanges U and V by A=diag(a,ia), and its F block is diag(1,lambda). If M is the S restriction to V, the U--U part of STS=xi T^-1 S T^-1 gives

    M = xi^-1 A R diag(1,lambda) R^t A.

Multiplying the explicit two-by-two matrix gives

    M^2 = (a^4 lambda/xi^2) I.

Since M^2=I, a^4 lambda=xi^2. This calculation uses the actual anomalous STS identity and retains xi; there is no dropped central-charge phase.

For the selected orientation xi^2=i, the H162 branch requires lambda at exponent 1512 modulo 1728, and H378 requires exponent 648. The finite candidate outside-pair lists have the former and not the latter. The arithmetic in `verify_six_dimensional_block.py` therefore correctly retains only the H162 branch and its A1512 pair. The same lemma applies to patterns 186 and 40 once their respective matching reductions have been justified.

This audit checks the block lemma and its exponent substitution. The earlier pattern-186 phase chain has a separate independent audit. It does not assert that every separate pattern-40 enumeration was independently reconstructed in this file.
