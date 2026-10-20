#!/usr/bin/env python3
"""Write the current M5 continuation overview from replayed ledger decisions."""
from collections import Counter
from pathlib import Path
import hashlib
import json
from rank7_publication import replay_status

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence/rank7_m5_20261020'
LABELS = {
    'quadratic_casimir_compression': 'Quadratic Casimir compression for arbitrary categorifications',
    'oriented_signed_compression': 'Complete signed quotient followed by spherical compression',
    'quadratic_center_Galois_two_moment_q60': 'Galois pseudo-unitary reduction and conductor-60 center moments',
    'cyclic3_full_morita_rank13_descent': 'Complete cyclic Morita dual and dimension-148 subcategory descent',
    'oriented_dimension_order': 'Complete signed quotient and dimension-order obstruction',
    'character': 'Complete signed character cover and exact induction obstruction',
    'general_induction': 'Complete signed reduction and exact induction obstruction',
}


def main():
    path = ROOT / 'supplements/rank7/output/rank7_ledger.json'
    ledger = json.loads(path.read_text())
    rows = {row['id']: row for row in ledger}
    accepted = json.loads((EVIDENCE / 'accepted/decisions.json').read_text())
    for item in accepted:
        if rows[item['id']]['status'] != 'excluded' or rows[item['id']]['certificate'] != item['certificate']:
            raise ValueError('Accepted decision has not reached the ledger: ' + item['id'])
    receipt = json.loads((ROOT / 'supplements/rank7/output/m5/replay_normal.json').read_text())
    if receipt['status'] != 'PASS' or receipt['mode'] != 'full_exact_replay' or receipt['ledger_sha256'] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError('A current full exact replay is required')
    counts = Counter(row['status'] for row in ledger if row['multiplicity'] == 5)
    total = Counter(row['status'] for row in ledger)
    remaining = [row['id'] for row in ledger if row['status'] == 'unresolved']
    groups = {}
    for item in accepted:
        groups.setdefault(item['criterion'], []).append(item['id'])
    text = '''# Rank-seven multiplicity-five continuation: 20 October 2026

AI-generated research; independent human verification and Lean formalization
remain pending. This page reports source-bound, exactly replayed decisions.

'''
    text += f'This continuation resolves {len(accepted)} of the 15 cases left open on 19 October.\n\n'
    text += '| Scope | Supplied rings | General exclusions | Unitary models | Open |\n|---|---:|---:|---:|---:|\n'
    text += f"| Exact multiplicity five | 5,805 | {counts['excluded']:,} | {counts['unitarily_realized']} | {counts['unresolved']} |\n"
    text += f"| Rank seven through multiplicity five | 10,006 | {total['excluded']:,} | {total['unitarily_realized']} | {total['unresolved']} |\n\n"
    text += '''The [accepted decisions](accepted/decisions.json) are integrated into the
[current ledger](../../supplements/rank7/output/rank7_ledger.json). All 4,201
earlier records through multiplicity four remain unchanged. The input tensor
identities, fusion axioms, uniqueness and old-ID transport were checked
independently in the earlier extension. Exhaustive census completeness is
still producer-reported; the optimized enumeration was not independently rerun.

## General exclusion arguments

| Argument | Cases resolved in this continuation |
|---|---|
'''
    for criterion, ids in groups.items():
        text += '| ' + LABELS.get(criterion, criterion) + ' | ' + ', '.join('`' + rid + '`' for rid in ids) + ' |\n'
    text += '''
The current [rank-seven manuscript](../../manuscripts/rank7/papers/manuscript.pdf)
contains the full categorical reductions and finite-domain descriptions.
The main new combined arguments and their exact evidence are:

- [Quadratic compression](criteria/QUADRATIC_COMPRESSION_PROOF.md): the general bound is four; the stronger spherical bound alone is not promoted to a general exclusion.
- [Signed compression](criteria/R4569_GENERAL_PROOF.md): complete oriented enumeration forces a tensor section of sphericalization before the spherical obstruction is applied.
- [Conductor-sixty center trace](criteria/Q60_CENTER_TRACE_PROOF.md): an all-order two-moment hull and exact integer separators, combined with the [source-bound general reduction](sqrt15_reduction/PROOF.md). Relative traces are paired under Galois symmetry; individual paired twists need not coincide.
- [Integral Morita descent](modules/README.md): all necessary module actions and complete dual fusion frames are exhausted, forcing a dimension-148 subcategory with forbidden Klein-four invertibles. The proof also gives a general cyclic-invertible restriction in dimension `4p`.
- [Scope review of inherited proof trees](criteria/INDEPENDENT_SCOPE_AUDIT.md) and [independent structural audit](structure/INDEPENDENT_AUDIT.md).
- [Complete induction proof trees](computation/README.md): R1964, R5343, R5623 and R5778 each have 5,025 Frobenius--Perron frames, all closed by ordinary moment obstructions. The [machine-counted summary](computation/proof_tree_summary.json) records the additional exhaustive signed-character covers.

No additional categorical model is established by this continuation.
The known `Rep(AGL(1,7))` realization of `R7_5_5678` remains the single
realized based-ring type added in exact multiplicity five. The two
[sqrt(5) structural reductions](sqrt5_reduction/PROOF.md) establish
sphericality and Galois pseudo-unitarity, without by themselves deciding
existence or nonexistence.

## Replay and dependencies

__CURRENT_REPLAY__

From the repository root, using Python 3.12 and a C++17 compiler:

```sh
python -m pip install -r supplements/rank7/requirements-m5.txt
python supplements/rank7/software/verify_m5.py --jobs 4
python -O supplements/rank7/software/verify_m5.py --jobs 4
```

The aggregate verifier binds every accepted certificate to its actual source
tensor. It rebuilds finite domains and verifies exact arithmetic rather than
trusting discovery diagnostics. The R4982 assertion-based components run in
an isolated unoptimized child in both aggregate modes, so their assertions
remain active. NetworkX is required for that finite permutation computation.
SciPy is optional for discovery and is not needed by exact replay.

See the [normal receipt](../../supplements/rank7/output/m5/replay_normal.json),
[optimized receipt](../../supplements/rank7/output/m5/replay_optimized.json),
and [standalone archive](../../supplements/rank7/release/rank7-certified-through-m5.zip).
The archive contains the complete imported helper-source closure, current
manuscript and preserved earlier archive. Compiled scratch executables and
partial logs are excluded. `--metadata-only` checks source bindings and
partitions; it does not replay mathematical certificates.

## Remaining frontier

'''
    text += (', '.join('`' + rid + '`' for rid in remaining) + '.\n\n' if remaining else 'Every supplied rank-seven ring through multiplicity five has a recorded decision.\n\n')
    text += '''[Exact remaining tensors](../../supplements/rank7/output/m5/survivors.json)
and [all ranks' open tensors](../../data/remaining_cases.py) follow the current
ledger. A feasible necessary system does not provide coherent associators;
a failed or time-limited model search is not an exclusion. Scoped reductions
retain their hypotheses until a general argument closes the remaining gap.

For the quadratic pair, [full character transport](models/sqrt5/TRANSPORT_PROOF.md)
and [low-block compression](models/sqrt5/LOW_COMPRESSION_PROOF.md) reduce the
possible induction data. The [independent equality audit](modules/Q5_SATURATION_INDEPENDENT_AUDIT.md)
proves level-five descent and the primitive residue sign. The manuscript also
proves the uniform version for every prime congruent to one modulo four.
The [odd conductor-eight projection ladder](modules/CHI_MINUS8_PARTIAL_PROJECTION_AUDIT.md)
gives exact two-primary mass ratios through order eight. The [sign-safe dichotomy](modules/CHI_MINUS8_SIGN_SAFE_DICHOTOMY.md) restricts active twist orders to two finite alternatives; the [full source phase domain](models/sqrt5/FULL_SOURCE_PHASES_PROOF.md) supplies exact parity and divisibility restrictions.
The [third-moment note](modules/Q5_THIRD_MOMENT_NOTES.md) forces trivial third
rotations in any possible category. These remain necessary restrictions;
feasible integral phase systems are not categorifications.

For R3895, the [complete frame-six proof](integral_gram/PROOF.md) and
[canonical-source verifier](integral_gram/verify_frame6.py) exclude the
distinct-codegree-sixteen frame, leaving the repeated-row frame. Both
[normal](integral_gram/frame6_replay_normal.json) and
[optimized](integral_gram/frame6_replay_optimized.json) replays pass. The
certificate exhausts 20,508 active allocations and closes the final sixteen
integer branches with 775 exact leaves. This changes the necessary low frame,
not the whole ring's unresolved classification status.

Both rings have [no braided categorification](criteria/BRAIDED_FRONTIER_EXCLUSION.md).
The [canonical-source verifier](criteria/verify_braided_frontier.py) replays the
positive Galois reduction and the fusion-simple-to-modular argument. R5039
fails the modular formal-codegree condition. For R3895, Galois symmetry bounds
all twists by order forty; exhaustive balancing and exact second indicators
exclude every candidate. Both [normal](criteria/braided_frontier_normal.json)
and [optimized](criteria/braided_frontier_optimized.json) replays pass. These
are braided-only exclusions and do not alter the general survivor ledger.
Higher-word and Gram searches are diagnostic; earlier truncated witnesses
do not assert compatibility with subsequent constraints or provide models.
'''
    text = text.replace('__CURRENT_REPLAY__', replay_status(ROOT))
    (EVIDENCE / 'README.md').write_text(text)
    prior = ROOT / 'evidence/rank7_m5_20261019/README.md'
    historical = '> **Historical 19 October stage.** The counts and frontier below describe that stage. See the [20 October continuation](../rank7_m5_20261020/README.md) for current decisions; links to current ledgers and replay receipts follow the revised edition.\n\n'
    old = prior.read_text()
    if historical not in old:
        first, rest = old.split('\n\n', 1)
        prior.write_text(first + '\n\n' + historical + rest)
    print(json.dumps({'status': 'PASS', 'new_decisions': len(accepted), 'remaining_rank7': remaining}))


if __name__ == '__main__':
    main()
