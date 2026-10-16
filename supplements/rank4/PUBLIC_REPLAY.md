# Reproduce the rank-four classification

> **AI-generated research — independent verification pending.** Treat these results, proofs, code and data with caution. They have not yet been independently verified by human experts or formalized in Lean. A successful computer replay checks the implemented finite certificates; it does not replace those forms of verification.

The complete rank-four certificate is now available in this repository. No private attachment is needed. Thirteen binary parts preserve the exact original **75,825,461-byte** gzip stream; the first twelve parts are 6 MiB and the last is 327,989 bytes. The restoration helper uses only the Python standard library and checks every part plus the complete stream before installing it.

## Restore and verify

From a fresh clone of the repository, run:

```sh
python3 tools/restore_data.py
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

Requirements are Python 3.10 or newer, the pinned Python dependencies, and a C++17 compiler (`g++`). The first command restores the pinned large input datasets; the second restores `supplements/rank4/certificates/classification.jsonl.gz`. No precompiled verification binary is trusted.

The expected certificate SHA-256 is:

```text
969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f
```

To check the public parts without writing the restored stream, use `python3 supplements/rank4/restore_certificate.py --verify-only` from the repository root. `--output PATH` selects another destination. An existing destination with different contents is refused.

The full verifier audits all input tensors and their identities, regenerates the shared signed catalog, then checks every certificate and every required bounded signed or induction search. The expected bounded result is **889,530 rings: 15 realized, 889,515 excluded, zero unresolved**, with **7,084 signed records and 801,047 signed candidate tables** under the recorded certificate allocation. The shared exhaustive gate checks **6,470,006 signed sign/permutation orbits**, retaining 30,207 after the necessary arithmetic filters. This is a classification through multiplicity 128; the unrestricted fifteen-ring classification remains a conjecture.

## Further checks

From `supplements/rank4`, the packaged regression and companion commands are:

```sh
python3 test_verifier.py
python3 test_applications.py
python3 test_extension.py
python3 test_signed_scaling.py
python3 test_global_signed.py
python3 test_global_signed_queries.py
python3 verify_companion.py
```

The prepublication audit also independently regenerated the full unsigned census using the original archived enumeration program. Its source, unchanged and with a hash manifest, is preserved separately under [`evidence/prepublication_20261017/rank4/unsigned_recount_sources`](../../evidence/prepublication_20261017/rank4/unsigned_recount_sources). From that directory, run:

```sh
python3 count_rings.py --bound 128 --threads 2
```

This requires `g++` with OpenMP. It imports no census, has no default timeout, and writes all 128 exact-multiplicity counts under `oeis/`. The fresh audit obtained 889,157 self-dual classes and 373 classes with one dual pair; every count matched the pinned census manifest. The separate source package records the exact program used for this additional audit and does not replace the current classification verifier.

## Evidence and provenance

See the [dated rank-four replay report](../../evidence/prepublication_20261017/rank4/rank4_replay.md), its fresh JSON receipts and complete logs. Original-release and current-publication replays are identified separately. All checks are AI-performed and remain subject to the verification caution above.

The certificate was recovered from:

```text
FusionFrontier.tar.xz
  Rank4/Rank4_Dong_Palcoux_Through128/Rank4_Through128/
    certificates/classification.jsonl.gz
```

The original archive SHA-256 is `5ef85daaa2f582f7466de5d122335eaedfa683d2804703ef18bdf36f22c0cfd9`. All 145 entries in its rank-four release hash manifest passed before replay. The archive was preserved; the certificate was split directly, without decompression or recompression. [`certificates/manifest.json`](certificates/manifest.json) records ordered part hashes, lengths, the complete-file commitment and provenance. [`certificates/SHA256SUMS`](certificates/SHA256SUMS) is also supplied for standard checksum tools.
