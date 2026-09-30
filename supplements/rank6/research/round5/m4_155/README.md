# R6_4_155: certified finite frontier

Status: **open**. The current exact reduction leaves **6 induction profiles, each with a forced pair of low fusion matrices in a semion centralizer**. None is a categorification certificate.

The ring is R′(4), with basis 1,X,X*,h,g,hg, dimension d=4+3√2 for X and X*, and global dimension 72+48√2. The inherited general sphericalization/Galois reduction remains in `research/round4/m4_155/reduction.json`.

Canonical files:

- `frontier_certificate.json`: compact, exhaustive profile domain and sparse exact rays.
- `replay_frontier.py`: reconstructs the pointed/cubic reductions, all 1066 profiles, pointed compatibility, joint word domains, all exact rays, and pointed stabilizer divisibility. Numerical optimizers are disabled.
- `replay_packets.py`: reconstructs every semion packet orientation, restricted adjunction, dual closure, charge splitting of the two low fusion matrices, and the final pointed-action rays.
- `frontier_replay_optimized.json` and `packet_frontier.json`: optimized-Python replay receipts and surviving packet data.
- `software/round5_155.py`: exact R155 reductions, pointed actions, packet enumeration, and discovery helpers.
- `papers/chapters/frontier_155.tex`: mathematical explanation; general criteria are in `unified_gram.tex`.

Run from the repository root:

```sh
python -O research/round5/m4_155/replay_frontier.py
python -O research/round5/m4_155/replay_packets.py
```

The successive profile counts are 1066→874→98→59→25→15→9→6. The first step follows twenty-eight pointed-support rays and eight Clifford-cubic rays eliminating the other low/indicator branches. Joint cubic-word Gram reconstruction supplies 772 empty domains and 4 rays; common coefficient/twist assignments plus ribbon balancing supply 39 further rays. Pointed monodromy stabilizer divisibility then restricts the profiles, and semion-centralizer adjunction reduces them further.

The old rank 36 necessary-data witness is excluded by the complete joint cubic-word coefficient domain. It is not an unresolved solution of the stronger system. Exploratory solver outcomes, including time limits and integer infeasibility without certificates, are not used in the reduction. The semion factorization is a factorization of the Drinfeld center; it does not factor the original category.

The final profile indices are 275,277,279,296,298,306; their center ranks are 60,54,48,52,46,44. The equal pointed quadratic form is excluded. All survivors have q(h)=-1 and q(hg)=-q(g); complex conjugation allows q(g)=i.
