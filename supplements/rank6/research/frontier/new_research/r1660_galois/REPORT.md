# R6_8_1660: one signed-Galois / fermion exclusion

The signed Galois action and the tensor involution exclude **low-frame-zero raw profile 133**, reducing the frozen frontier from 1670 to **1669** profiles, with counts **163,753,753**. The ring remains unresolved.

The standalone proof is `research_section.tex`. The portable exact verifier is `verify.py`; run

```bash
python -O two_final/r1660_galois/verify.py --package work_m9_complete/Rank6_Categorification_M9
```

It takes about seven seconds, replays the preceding frozen certificate, verifies 36 exact signed character-row identities, checks an independent two-case proof for the excluded profile, and directly checks feasible orbit-count witnesses for all 1669 remaining profiles. No optimizer or complete center-fusion enumeration is used. `certificate.json` binds the source profiles by SHA-256.

For sigma-containing restriction vectors, the signed Galois map at a=5 exchanges the X and gX coordinates and has sign minus. Thus gamma = pi_5 composed with Z(alpha) preserves each such fiber and flips its primitive-sixteenth-root twists. Gamma commutes with the fermion action and therefore preserves its fixed locus. Duality has no fixed points in that locus and preserves twist, while gamma equates the multiplicities at opposite twists. The h-fixed cardinality is consequently divisible by four.

For profile 133, the even dimension equation has only two possibilities. One contradicts nonnegative odd-pair count; the other forces exactly two h-fixed sigma-containing simples, contradicting this divisibility. This final exclusion is a short arithmetic proof, independently audited by the indicators agent, and does not depend on search exhaustion.

Initial exact tests showed that sigma-fiber four-divisibility alone and Galois-equivariant orbit matching alone remove no profiles. The essential extra point is applying four-divisibility to the **h-fixed locus**, in conjunction with Galois equality of odd-pair counts in two distinct normal restriction fibers.
