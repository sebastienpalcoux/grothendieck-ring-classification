# Independent packet-Gram audit for R6_8_1660

2026-10-02. **PASS.** The necessary profile domain reduces from 1669 to
1136, with 533 newly excluded labelled restriction profiles. This is a
profile reduction; R6_8_1660 remains unresolved.

| Branch | Input | Excluded | Retained |
|---|---:|---:|---:|
| Low 0, labels (0,5,4,1,3,2) | 163 | 43 | 120 |
| Low 1, labels (0,5,4,1,2,3) | 753 | 245 | 508 |
| Low 1, labels (0,5,4,1,3,2) | 753 | 245 | 508 |
| Total | 1669 | 533 | 1136 |

## Mathematical necessity

The matrices P and Q are the actual fusion matrices of the even and odd
summands A+ and A- of I(1), provided a categorification exists. This is because
N_{I(1)}=R^T R and the monodromy grading isolates its two homogeneous parts by
their matrix supports. The center is braided, so P and Q commute. No braiding
of the original rank-six category or its relative center is needed.

The additional object identity A+^2-A-^2=2(A+-hA+) is also valid. At an even
simple its left coefficient is its restriction vector paired with
F(A+)-F(A-)=2(1-g). The known low restrictions and their forced h-partners
identify these coefficients with the right side. At odd simples both sides
are zero. Consequently the corresponding fusion matrices satisfy
P^2-Q^2=2(I-N_h)P.

The numerical part of `packet_gram_proof.md` was checked independently:

- The total Gram H and the fixed first two rows of H+ agree with the retained
  induction data. Residual even h-pairs contribute the moments stated there.
- The old even-dimension equations force the X,T and gX,T entries to be 96.
  Pairing packet commutativity with the two indicated even low columns and
  the average odd low column gives exactly the two displayed equations.
  They force B+C=140 and J=140, hence the moments 84, 60, 46, 2.
- The sigma-containing vectors all have z=1, q=4, a=3. Thus the last moment
  fixes the remaining entries involving sigma to 8, 4, and 12. Only the
  X-minus-gX entry remains free.
- On an asymmetric even restriction, the diagonal square identity forces
  B=72; on an asymmetric odd restriction it forces B=70. Hence they cannot
  occur in both charges. Low frame zero already has two asymmetric odd low
  restrictions, exhausting the total asymmetric norm. Low frame one forces
  some asymmetric high restriction. This proves that the only matrices are
  the two H+(Delta) in the proof, with Delta=0 or 4, and proves the common
  charge rule used in the search.

The source proof's sentence about the negative odd coefficient was flagged
for simplification: both objects have even support, so odd coefficients are
zero. This is a wording issue and does not change the identity.

## Independent exact replay

`audit_packet_gram.py` does not import the new probe or the prior Galois
verifier. It independently:

1. Checks the profile-source SHA-256 values and rebuilds the prior retained
   index sets from the earlier rejection lists.
2. Removes forced low/high pairs and rebuilds h-orbits and the signed
   Galois-5 blocks directly from the restriction vectors.
3. Enumerates the bounded even-pair, odd-pair, and fixed counts by starting
   from odd and fixed counts, independently of the probe's enumeration.
4. Uses a separate memoized recursion, with reversed block order, to test all
   six moment/rank equations for every permitted low action and Delta.
5. Reproduces every rejected index in all three branches exactly.
6. Checks that every supplied survivor witness expands to exactly its
   original restriction multiset, and verifies both full integer matrix
   identities P Q=Q P and P^2-Q^2=2(P-N_h P).

The full independent replay takes approximately three seconds and passes.
Its output is `packet_gram_independent_receipt.json`. It is an exact bounded
integer calculation, without a floating-point optimizer or center-fusion
reconstruction.

## Scope and dependencies

The argument uses the already retained positive spherical/Galois reduction,
the central fermion and known low columns, the earlier h-orbit and signed
Galois conditions, and the earlier even-dimension/rank equations. This audit
does not rerun every historical certificate establishing those inputs.

The 1136 survivors have compatible necessary packet data; this does not
construct their remaining fusion matrices, twists, associators, or any model.
No general fusion-category exclusion for the original ring is claimed.
