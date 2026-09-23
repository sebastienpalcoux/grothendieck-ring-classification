# Additional rank-eight certificates through multiplicity two

This folder contains an independently checked extension of the rank-seven
oriented signed sphericalization code to rank eight.  The categorical
necessity of the sphericalization and its self-dual, positive-indicator
normalization are established in the rank-six manuscript.  The code here
extends the **bounded enumeration and exact checker** to eight labels; the
noncommutative signed component analysis is still restricted to rank six.
Thus a rank-eight signed table with noncommutative multiplication causes
`general_certificate` to return `None`, with no classification claim.

The complete source census is `../data/rank8_tables.txt.gz`.  Each witness
stores that tensor's SHA256 digest, the exhaustive signed quotient tables,
one obstruction per quotient, and all ordinary spherical-character
obstructions.  `signed_certified_campaign.json` freezes the 75 verified
witness IDs and SHA256 hashes: three in multiplicity one, 72 in multiplicity
two.  Each of those certificate files was saved only after the full exact
verifier returned.  Use the final rank-eight main ledger to determine which
are new exclusions, because earlier criteria may have excluded the same
source tensor more efficiently.

To check a chosen witness again from the workspace root:

```sh
python work_rank8/experimental_signed/verify_signed.py R8_2_25
```

For new discovery, `python work_rank8/experimental_signed/try_rank8.py 2_25 15`
recomputes a certificate, performs the exact check, and writes it after
success.  The exploratory scan logs (`scan_m1.json`, `screen_m2.json`,
`scan_m2_full.json`) include timeouts and incomplete searches.  Neither
status is an exclusion.  The first multiplicity-two scan timed out during
verification of `R8_2_483`; a separate 14.54 second complete replay checked
and saved that witness.  `R8_2_260` remains undecided by this stage.

The archived Alekseyev–Bruns–Dong–Palcoux preprint
[`Appendix C.3.2`](https://bimsa.net/doc/publication/14753.pdf) supplies
six further exact full-tensor matches in multiplicity one or two.  Run
`python work_rank8/experimental_signed/verify_appendix.py` to check their
fusion axioms, Frobenius–Perron dimension characters, duality, and full based
isomorphism to the source census.  Its negative transfers for `R8_1_38`
and `R8_1_41` invoke the paper's unconditional Lemmas 4.3 and 4.2,
respectively: no induction matrix, hence no complex fusion category.  This
checker verifies the hypotheses and exact source match; it does **not** rerun
the paper's Normaliz induction search.  The other three identified positive
models are the cited group theoretical categories for `R8_1_24`,
`R8_2_202`, and `R8_2_241`.  The sixth source tensor, `R8_1_3`, remains
unresolved in the archived appendix.
