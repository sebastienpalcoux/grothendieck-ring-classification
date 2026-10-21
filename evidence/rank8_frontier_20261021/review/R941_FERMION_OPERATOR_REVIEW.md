# Independent review of the corrected R941 fermion operator

This review certifies a complete necessary operator and charge domain. It does
not certify any infeasibility or any categorification.

Work in the established pseudo-unitary Galois conjugate. The forced central
involution G has twist −1. The five distinguished objects A_i have twist 1
and charges q_i=(1,1,1,1,−1). Their five distinct G-translates have the same
charges and twists −q_i. Their restrictions are reconstructed individually
from source multiplication; no scalar-row translation shortcut is used.

For each character E, put w_E(v)=FPdim(v) chi_E(v). After cancelling the
noncommutative normalization beta_E=D/(f_E dim(E)), G-row orthogonality and
STS respectively give

    sum_Z M_G,Z w_E(FZ)=0,
    sum_Z theta_Z M_G,Z w_E(FZ)=−D chi_E(g).

The characters here are real. The fixed terms are exactly

    Korth_E=sum_i q_i [w_E(v_i)+w_E(g v_i)],
    Ksts_E=sum_i [q_i w_E(v_i)−w_E(g v_i)].

In particular the M2 character satisfies chi_E(gv)=−chi_E(v), not
chi_E(gv)=chi_E(v). Its remaining STS row is identically zero, including
its RHS. An earlier exploratory simplification violated this identity;
that operator and its resulting apparent negative branches are discarded.

For every fixed restriction type j<40, charge +1 simples lie in free G-pairs
with opposite twists. Charge −1 simples may be fixed and remain individual
variables. If p_j is the plus-pair count, total multiplicity m_j gives net
charge 4p_j−m_j, with 0≤p_j≤floor(m_j/2). Independent full-box enumeration
checks all 41,664 assignments over the established 343 integer Gram/cubic
patterns. Exactly 93 assignments on 68 patterns satisfy orthogonality.

The complete height-six individual trace domain has 38 types. Summing the
types of theta and −theta gives exactly 28 pair types. Each pair column is
the sum of the two full old columns, with Gram mass two and first moment
zero. Each negative-charge individual retains its old column and adds
−w_E(v)Tr(theta) to the new STS rows. The rotation auxiliary columns occur
once. The known ten objects contribute the explicit fixed terms above;
the five high translates also move their full old columns to the RHS.

`verify_r941_fermion_operator.py` independently reconstructs all 2,717
universal columns (1,120 pair, 1,520 individual, 77 auxiliary), all 468 rows,
and all 93 selected operators, using exact rational field coordinates.
The actual nine-simple center Z(Ising) verifies the G-row normalization,
including its negative-charge distinguished character. This control also
checks full S² and STS. The producer additionally checks its own fixed-term
builder against the deduplicated actual five-object Ising fixed union.

The source-bound receipt is `r941_fermion_operator_review.json`. Branch
solutions or separators require a separate exact replay on this corrected
operator. No old cached negative certificate is admissible.

The corrected final campaign is independently replayed by
`verify_r941_fermion_campaign.py`, with receipt
`r941_fermion_campaign_review.json`. It checks all 93 complete selected
domains, thirteen distinct exact rays accounting for 77 negative charge
allocations, and sixteen positive rational solutions against every original
equation. The surviving original pattern indices are 40, 45, 65, 70, 137,
140, 151, 154, 186, 189, 200, 203, 228, 229, 235, and 236. Thus this
campaign finishes with sixteen exact finite-system survivors; it gives
neither a global exclusion nor a model for R941.

The separate `verify_r941_integer_witnesses.py` checks twelve subsequent
nonnegative integer witnesses directly against every original paired equation,
with no producer integer-checker import. Its source-bound receipt is
`r941_integer_witness_review.json`. Four other bounded integer searches
remain unresolved. Integer feasibility of these necessary constraints still
does not provide a fusion-category construction.
