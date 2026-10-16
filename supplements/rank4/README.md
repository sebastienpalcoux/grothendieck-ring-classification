# Rank-four classification through multiplicity 128

> **AI-generated research — independent verification pending.** Treat these results, proofs, code and data with caution. They have not yet been independently verified by human experts or formalized in Lean. See the [verification scope](../../docs/PREPUBLICATION_REVIEW.md).

The bounded classification records **15 realized and 889,515 excluded rings among 889,530 inputs**, with no unresolved case through multiplicity 128. Every positive ring has a unitary model. The unrestricted fifteen-ring classification remains a conjecture.

## Read the research

- [Finite classification](../../site/dist/papers/rank4.pdf)
- [Unrestricted structural companion](../../site/dist/papers/rank4_companion.pdf)
- [Mathematical verification guide](../../site/dist/papers/rank4_guide.pdf)
- [LaTeX sources](../../manuscripts/rank4/papers)

## Reproduce the computation

The complete compressed certificate is publicly included as thirteen binary parts. **No private attachment is needed.** Follow the [public restoration and replay guide](PUBLIC_REPLAY.md), which explains the dependencies, checksums, full verifier, regression tests and separate unsigned census recount.

From the repository root:

```sh
python3 tools/restore_data.py
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

The certificate is exactly 75,825,461 bytes, with SHA-256 `969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`. Restoration checks every part and the complete stream before writing the final file. The full verifier reconstructs all tensors, audits their identities and fusion axioms, regenerates the shared signed catalog and checks every certificate.

The [complete replay report](../../evidence/prepublication_20261017/rank4/rank4_replay.md) supplies full-run logs and machine-readable receipts. Replays are computational evidence, subject to the independent-verification caution above.

## Data and scope

The rank-four census is pinned to [fusion-ring-census commit `7f1b36e74df53a8a1cf8597db45d261e408d61b2`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/7f1b36e74df53a8a1cf8597db45d261e408d61b2). `data/census_128_manifest.json` identifies its 889,530 tensors and all 128 exact-multiplicity counts. Census completeness and categorification have separate arguments and verification paths.

The dispatcher checks the uniform residual-involution criterion without recognizing a named tensor. The certificate tag `involution_propagation_42` remains for ledger compatibility. The 7,084 signed records contain 801,047 explicitly enumerated candidate tables after their stated necessary prefilters; these are not counts of every raw coefficient choice.

Criterion first-use statistics describe the recorded allocation, not a minimality theorem. The last newly used criterion family appears at multiplicity 18; a nested signed cyclotomic check first succeeds at 95 using the cyclotomicity theorem already applied at 9.
