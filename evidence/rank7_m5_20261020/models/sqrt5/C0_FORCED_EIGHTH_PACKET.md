# A forced eighth-moment packet in the remaining conductor-eight branch

This refines the four surviving active phase assignments for each of the two
R5039 label classes. Coverage of the preceding active assignments is a
separate certificate. The argument below does not by itself exclude a ring.

Write s=sqrt(5), D=720+320s. The active orbit24 consists of the two nonunit
restriction rows(0,1,1,1,1,1) and(1,0,1,1,1,1), each repeated8 times and
with a common order64 relative phase. Their sum is
v50=(1,1,2,2,2,2). Each has relative dimension z/D=s/40. Its eighth phase
is (sigma sqrt(2)+i tau sqrt(2))/2 with sigma,tau in{+1,-1}. Thus the active
contribution to the vector of eighth indicators has sqrt(10) and
 i sqrt(10) coordinates sigma*v50/10 and tau*v50/10.

Every eighth indicator lies in Q(zeta_8), so both of these unwanted
sqrt(5)-containing coordinates must vanish after all contributions are added.
After the independently replayed residual Gram pruning, the only inactive
packets contributing to these coordinates are:

- orbit45, v45=(1,1,1,1,1,1), z/D=1/16, order320 packet unit16;
- orbit50, v50 as above, z/D=s/20, order320 packet unit16.

An orbit45 packet contributes (+/-)v45/8 to each unwanted coordinate. An
orbit50 packet contributes (+/-)v50/10. Every sign pair occurs with two
possible choices of the fifth-primary trace sign. The vectors v45 and v50
are linearly independent.

The residual Gram matrix after fixing the active packet gives exact upper
bounds17 and34 for the total numbers of objects with rows v45 and v50.
These bounds apply to all their phase assignments jointly. Thus there is
at mostone order320 packet on orbit45 and at mosttwo on orbit50.
Independence of the row directions forces the signed orbit45 sum to zero,
which is impossible for one packet. Hence there are no orbit45 order320
packets. The signed orbit50 packet sums must equal -sigma and -tau.
Their total number is therefore odd and at mosttwo, hence exactlyone.
Its real and imaginary signs are forced; precisely two relative phases
remain, distinguished by the fifth-primary trace sign.

Other phases on orbit50 remain allowed. In particular, this argument fixes
its order320 packet total to one, not its entire row multiplicity to16.
The other phase variables must be retained in subsequent systems.

`verify_c0_forced_eighth_packet.py` reconstructs the induction Gram matrix
directly from the pinned fusion tensor, replays every retained/removed
phase column with exact rational Schur complements, verifies the complete
unwanted-coordinate support, and derives both forced phase choices for all
eight active assignments across both label classes. Normal and -O runs
pass, with reports `c0_forced_eighth_packet_normal.json` and
`c0_forced_eighth_packet_optimized.json`. No numerical optimizer or producer
Gram-pruning helper is used by this replay.
