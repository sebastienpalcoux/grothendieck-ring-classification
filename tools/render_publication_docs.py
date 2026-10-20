#!/usr/bin/env python3
"""Render current publication guides from authoritative classification ledgers."""
import argparse
import json
from pathlib import Path
from rank6_publication import validate_identity, completed_bands, validate_document_revision
from publication_stages import load_stages, overview
from rank7_publication import summary as rank7_extension_summary, extension, remaining_ids, replay_status, STATUS_REPORT

ROOT = Path(__file__).resolve().parents[1]
CAUTION = '''> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.
'''
FRONTIER = '''### Rank-six open rings

| Open ring | Established necessary restrictions | Remaining question |
|---|---|---|
| `R6_4_155` | A unique rank-26 modular candidate and a rank-22 based module; odd cyclic Clifford constraints pass on all 1,144 tested blocks, and the all-order path divisibility condition holds. | Coherent associators and module-category structures, or a general obstruction. |
| `R6_8_1660` | In the positive spherical representative, all indicator sequences and central phase masses are determined; eight spin objects form four dual pairs, and 640 labelled restriction-data profiles remain in branches 68, 286, 286. | A categorification or an obstruction covering every possible profile. |
'''

def case_inventory(repo):
    # Render every case with current proof sources.
    all_cases=json.loads((repo/'evidence/rigidity_20261017/all_cases.json').read_text())
    decisions=json.loads((repo/'evidence/rigidity_20261017/decisions.json').read_text())
    accepted={d['id']:d for d in decisions}
    open_ids={'R6_4_155','R6_8_1660'}
    if len(all_cases)!=38 or len({x['id'] for x in all_cases})!=38:
        raise ValueError('Expected exactly 38 distinct case IDs')
    if len(accepted)!=36 or {x['id'] for x in all_cases} != set(accepted)|open_ids:
        raise ValueError('The current case inventory differs from the decision ledger')
    if sum(d['status']=='excluded' for d in decisions)!=29 or sum(d['status']=='unitarily_realized' for d in decisions)!=7:
        raise ValueError('Expected 29 general exclusions and seven unitary constructions')
    if any(d['scope']!='general_complex' for d in decisions):
        raise ValueError('Unexpected scope in accepted case inventory')
    # Entries identify the integrated manuscript and its stable LaTeX label.
    references={
      'quadratic_center_Galois_two_moment':('Galois symmetry and two center moments','rank7/papers/quadratic_center_trace.tex','thm:quadratic-center-trace'),
      'simple_center_prime_power_lattice':('Simple-center induction lattice','rank7/papers/r601_center_lattice.tex','thm:r601-center-lattice'),
      'inverse_V4_Morita_near_group':('Inverse V4 Morita reduction to a near-group obstruction','rank7/papers/inverse_v4_morita.tex','thm:r1022-general'),
      'C4_squared_orbifold_inversion_Morita':('Inversion orbifold and reflection Morita dual, from NG(C4 × C4,16)','rank7/papers/inversion_orbifold_model.tex','thm:inversion-v4'),
      'dihedral_Morita_R18_obstruction':('Dihedral Morita reduction to the R8_1_18 obstruction','rank7/papers/r2053_r18_reduction.tex','thm:r2053-final'),
      'twisted_v4_staged_morita_obstruction':('Twisted V4 Morita obstruction','rank7/papers/r2591_staged_morita.tex','thm:r2591-staged-morita'),
      'quadratic_center_reciprocity_two_moment':('Reciprocity and two center moments','rank7/papers/r2603_center_moments.tex','thm:r2603-center-moments'),
      'C16_orbifold_inversion_Morita':('Inversion orbifold and reflection Morita dual, from NG(C16,16)','rank7/papers/inversion_orbifold_model.tex','thm:inversion-orbifold'),
      'cyclic_induction_phase_multiplicity':('Cyclic induction phase multiplicities','rank8/paper/r9_pointed_class2.tex','thm:r9-center-trace'),
      'cyclic_induction_STS_fourth_moment':('Modular STS identity and a fourth-moment projection','rank8/paper/r18_center_trace.tex','thm:r18-sts-moments'),
      'pivotal_parity_inverse_morita':('Frobenius–Schur parity and inverse Morita reduction','rank8/paper/unified_20261016.tex','prop:r49-fs-morita'),
      'quadratic_prime_indicator_balance':('Conductor-seventeen indicator balance','rank8/paper/q17_indicator_balance.tex','thm:q17-five-exclusions'),
      'nonsplit_2D2_extension':('Nonsplit C2 extension of the unitary 2D2 category','rank8/paper/unified_20261016.tex','prop:r37-model'),
      'algebraic_2D2_planar_algebra':('Algebraic rigidity of the 2D2 module graph','rank8/paper/unified_20261016.tex','prop:2d2-four-general'),
      'odd_involution_morita_near_group':('Odd-involution Morita reduction to a near-group obstruction','rank8/paper/unified_20261016.tex','prop:r170-morita'),
      'Fibonacci_character_parity':('Fibonacci character parity','rank8/paper/unified_20261016.tex','thm:fib-character-parity'),
      'twisted_half_braiding_support':('Pointed support of a twisted half-braiding','rank8/paper/unified_20261016.tex','prop:twisted-two'),
      'PSU3_inverse_Morita_rigidity':('Quantum-group inverse-Morita rigidity','rank8/paper/unified_20261016.tex','prop:r342-morita'),
      'HI_C6_Q_system_dual':('Dual of the Q-system 1+rho in a unitary HI(C6) category','rank8/paper/unified_20261016.tex','prop:r535-model'),
      'quadratic_conductor_Galois_indicator':('Third-indicator triangle obstruction at conductor forty','rank8/paper/q630_weighted_indicator.tex','thm:q630-exclusion'),
      'C4_near_group_pointed_centralizer':('Pointed centralizer in the center of NG(C4,4)','rank8/paper/unified_20261016.tex','prop:c4-centralizer'),
      'quadratic_conductor40_center_trace':('Conductor-forty center trace obstruction','rank8/paper/r671_center_trace.tex','thm:r671-center-trace'),
      'C5_near_group_center_factor':('Nonpointed center factor of NG(C5,5)','rank8/paper/unified_20261016.tex','prop:near-group-centralizers'),
      'inner_square_torus_rigidity':('Inner-square obstruction from short gauge weights and tensor-functor rigidity','rank8/paper/r24_inner_square.tex','thm:r24-general-exclusion'),
    }
    open_references={
      'R6_4_155':('Odd cyclic Clifford constraints pass on 1,144 tested blocks, and the all-order path divisibility condition holds. The surviving modular and module data do not supply coherent associators.','rank6/papers/chapters/frontier_155_odd_clifford.tex','sec:r155-odd-clifford'),
      'R6_8_1660':('In the positive spherical representative, all indicators and central phase masses are determined; 640 labelled restriction profiles survive in branches 68, 286, 286. These necessary data do not construct a category or yield a general obstruction.','rank6/papers/chapters/frontier_1660_phase_masses.tex','sec:1660-all-indicators-phase-masses'),
    }
    def proof_link(path,label):
        source=repo/'manuscripts'/path
        if not source.is_file() or ('\\label{'+label+'}') not in source.read_text():
            raise ValueError('Missing current manuscript reference: '+path+' '+label)
        return f'[Source](../manuscripts/{path}) (`{label}`)'
    text='# Historical 38-case study and current proof references\n\n'+CAUTION+'''
**36 accepted decisions: 29 proposed general exclusions and seven unitary
constructions. Two general questions remain open.** This inventory covers
these 38 cases; it is not a count of every ring in the full census.

A general exclusion concerns arbitrary complex fusion categories, without an
initial pivotality, sphericality or unitarity assumption. A unitary construction
establishes at least one realization, not uniqueness or unitarity of every
realization. Necessary-condition witnesses do not settle a general question.
All accepted arguments remain subject to independent mathematical verification.

Read the [rank-six manuscript](../manuscripts/rank6/papers/manuscript.pdf),
[rank-seven manuscript](../manuscripts/rank7/papers/manuscript.pdf) and
[rank-eight manuscript](../manuscripts/rank8/paper/rank8.pdf).
The source links below identify the current integrated proof or open-case
section; the stable LaTeX label locates the exact statement in that source.

## Two open cases within the historical study

| Case | Current status and remaining task | Current manuscript section |
|---|---|---|
'''
    for rid in sorted(open_ids):
        note,path,label=open_references[rid]
        text+=f'| `{rid}` | **Open.** {note} | {proof_link(path,label)} |\n'
    for rank in (7,8):
        cases=[x for x in all_cases if x['rank']==rank and x['id'] in accepted]
        text+=f'\n## Rank {rank}: accepted decisions\n\n| Case | Scope of decision | Argument or construction | Current proof |\n|---|---|---|---|\n'
        for case in cases:
            d=accepted[case['id']]
            method,path,label=references[d['criterion']]
            if case['id']=='R8_2_820':method+='; auxiliary group C3 × C3'
            if case['id']=='R8_2_869':method+='; auxiliary group C9'
            status='General exclusion' if d['status']=='excluded' else 'Unitary construction'
            text+=f"| `{d['id']}` | {status} | {method} | {proof_link(path,label)} |\n"
    text+='''
## Classification boundary of the historical study

The following boundary describes the 17 October study; the current M5 extension is stated above.
Through multiplicity nine, rank six has 25,362 exclusions, 57 realizations and
two open cases. Rank seven is complete through multiplicity four with 4,172
exclusions and 29 models. Rank eight is complete through multiplicity two:
896 exclusions and 77 models, with no open case.

Run the current aggregate replay from the repository root:

```bash
python3 tools/restore_data.py
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

These checks validate the accepted inventory and its source-bound computational
dependencies. They do not replace the full base-certificate replays or prove
categorical coherence. See [verification scope](PREPUBLICATION_REVIEW.md),
[complete replay instructions](VERIFY.md) and [source provenance](PROVENANCE.md).
'''
    return text

def section(text,start,end,replacement):
    a=text.index(start);b=text.index(end,a)
    return text[:a]+replacement+text[b:]

def render(repo, identity):
    validate_identity(identity)
    validate_document_revision(identity, repo)
    status=json.loads((repo/'data/classification_status.json').read_text())
    stage=load_stages(repo,status)
    s=identity['summary']; bands=completed_bands(identity)
    rows={(r['rank'],r['multiplicity']):r for r in status['rows']}
    upper={r:status['inputs'][f'rank{r}'] for r in (7,8)}
    rank5=json.loads((repo/'evidence/prepublication_20261017/rank5/package.json').read_text())
    def totals(r):return {'unresolved':0,**upper[r]['status_totals']}
    def bound(r):return upper[r]['classified_through']
    def complete(r):return next((m-1 for m in range(1,bound(r)+1) if rows[r,m]['unresolved_general'] or rows[r,m]['unassessed']),bound(r))
    extension_text=rank7_extension_summary(repo)
    census_extension=json.loads((repo/'data/counts.json').read_text()).get('census_extensions',{}).get('rank7_m5')
    census_note=(f"The rank-seven M5 extension is pinned separately to census commit `{census_extension['census_commit']}`. "
                 "Its 5,805 new exact-multiplicity-five tensors and agreement with the earlier 4,201 tensors passed independent computational checks; exhaustive enumeration completeness relies on the supplied producer completion record. The optimized enumeration itself was not independently rerun." if census_extension else '')
    rank7_scope=(f"Through multiplicity {bound(7)}: {totals(7)['excluded']:,} exclusions, "
                 f"{totals(7)['unitarily_realized']} models and {totals(7)['unresolved']} unresolved; "
                 f"complete through {complete(7)}")
    rank7_frontier=(f"The rank-seven frontier contains {totals(7)['unresolved']} {'case' if totals(7)['unresolved']==1 else 'cases'} in exact multiplicity five. The exact tensors and recorded criterion results are in the [M5 frontier](../supplements/rank7/output/m5/survivors.json) and [continuation evidence](../evidence/rank7_m5_20261020/README.md). "
                    if totals(7)['unresolved'] else "Every supplied rank-seven fusion ring through multiplicity five has a recorded general exclusion or unitary model. The [continuation evidence](../evidence/rank7_m5_20261020/README.md) gives the accepted arguments and replay receipts. ")
    out={"docs/CASE_INVENTORY.md":case_inventory(repo)}
    out['docs/RESEARCH_STATUS.md']='# Research status and verification\n\n'+CAUTION+'''
The [public atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
connects the current manuscripts, fusion rules, classification tables and
reproducible evidence. Publication makes the material accessible; it does not
confer mathematical validation.

## Current classification

'''+overview(stage,'../')+'''

[All 38 cases and current proof references](CASE_INVENTORY.md).
'''+f'''
Rank six records **{s['excluded']:,} exclusions, {s['positive']} realizations and
{s['unresolved']} open cases** through multiplicity nine. Its complete contiguous
range ends at three; exact bands {bands} are complete. Rank seven records
**{totals(7)['excluded']:,} exclusions and {totals(7)['unitarily_realized']} realizations**,
with **{totals(7)['unresolved']} open cases through multiplicity {bound(7)}**; complete through multiplicity {complete(7)}. Rank eight records
**{totals(8)['excluded']} exclusions and {totals(8)['unitarily_realized']} realizations**,
with no open case through multiplicity two. The general exclusion of
`R8_2_24` uses an inner-square obstruction from short gauge weights and
tensor-functor rigidity.

'''+FRONTIER+f'''
### Rank-seven classification frontier

{rank7_frontier}[Download all {len(remaining_ids(repo))} current open tensors](../data/remaining_cases.py), including the two rank-six cases.

A necessary-condition witness is neither a categorification nor a general
nonexistence proof. Scoped unitary, pseudo-unitary, pivotal or braided
obstructions retain their assumptions and do not change a general open status.

## Reading the labels

| Label | Meaning within this project |
|---|---|
| **Realized** | A categorical construction is recorded, subject to mathematical review. |
| **Excluded** | An obstruction is recorded under its stated assumptions. |
| **Complete** | Each ring in the specified band has a recorded realization or general exclusion. |
| **Unresolved** | Neither a general exclusion nor a categorification is established. |
| **Certified**, **verified**, **PASS** | The stated program checks passed; read their scope and hypotheses. |

Reports described as independent audits are separate AI review passes unless
an explicitly identified human review says otherwise. They are not independent
human verification. Hashes establish source identity; they do not prove the
mathematics. Successful computation does not validate the categorical reduction
making that computation relevant.

Read the [verification scope](PREPUBLICATION_REVIEW.md), [replay guide](VERIFY.md)
and [provenance](PROVENANCE.md) together with the
[manuscripts](../manuscripts/README.md). A [repository issue](https://github.com/sebastienpalcoux/grothendieck-ring-classification/issues)
identifying the ring, theorem and exact failing step makes a reported gap actionable.
'''
    out['docs/PREPUBLICATION_REVIEW.md']='# Mathematical review and verification scope\n\n'+CAUTION+'''
The current manuscripts give one account of the classification and its open
questions. This guide states what the supporting review and computations
establish, and where mathematical verification is still needed.

## Mathematical scope

'''+overview(stage,'../')+'\n\n'+FRONTIER+'''
For `R8_2_24`, the general-complex proof passes to a pseudo-unitary Galois
conjugate, forces the neutral indicators by saturated modular compression,
and excludes the required square root of an inner tensor functor. The proof
uses a simultaneous pivotal chart, short associator weights and finiteness
of tensor functors. Its [theoretical argument and independent AI audits](../evidence/rigidity_20261017/README.md)
are separate from the source and finite-weight checks.

The review examines general versus pivotal or pseudo-unitary scope, cited
hypotheses, sphericalization and Galois reductions, Morita constructions,
indicator constraints and root-order completeness. Further expert review
should especially examine coherence of inverse-Morita constructions, the
algebraic 2D2 arguments and the conductor-equality reductions. An AI review
cannot certify that every mathematical step is correct.

## Computational coverage

| Check | Executed scope | Result and limit |
|---|---|---|
| Rank three | Bounded near-group enumeration, `b<50` | Five reduced tuples; categorical proof reviewed separately. |
| Rank four | Two complete 889,530-ring replays, each regenerating 6,470,006 signed orbits; separate unsigned recount | Passed: 15 models and 889,515 exclusions. |
| Rank five | All 40,999 classes, 17 models and 40,982 exclusion certificates in normal and optimized Python | Passed; complete reconstructed ledgers are byte-identical. |
| Rank six | Model/import pipeline and all 25,362 exclusion certificates, followed by the two post-loop checks | Combined coverage passed; the initial full process failed on seven certificates, each of which passed a separate complete Python-backend replay. |
| Rank seven base certificates through multiplicity four | 4,201 records: 4,116 exclusions, 26 models and 59 cases deferred to continuation proofs | Passed in normal Python. |
| Rank seven multiplicity-five extension | __M5_COVERAGE__ | __M5_REPLAY__ [Normal receipt](../supplements/rank7/output/m5/replay_normal.json), [optimized receipt](../supplements/rank7/output/m5/replay_optimized.json). Enumeration completeness remains producer-reported. |
| Rank eight base certificates | 973 records: 832 exclusions, 60 models and 81 cases deferred to continuation proofs | Passed in normal Python, including signed proof trees. |
| Continuation chain and current inventory | Source identities, accepted decisions and dependency replays in normal and optimized Python | Passed within each program's stated scope; does not prove categorical coherence. |

The [full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md),
[coverage audit](../evidence/prepublication_20261017/reviews/verification_coverage.md)
and [current inventory receipts](../evidence/prepublication_20261017/current_history/receipt.json)
identify the exact inputs and executed programs. Continuation checks supplement
the base loops; they do not rerun every base certificate. An optimized run alone
cannot check assertions removed by Python's `-O` option.

## Rank-six environment and coverage

The [complete packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records **25,355 initial passes plus seven complete Python-backend passes**,
exactly covering 25,362 distinct certificates. It also records the separately
executed post-loop counts and model registry and binds 299 source/input files.
This was a **combined verification campaign, not a successful single full run**.

The affected Galois-balance systems order some algebraic tuples by their string
representations. SymPy's Python and Flint backends can reorder or reverse these
equations, invalidating a positional Farkas vector for the other ordering.
Exact matrix comparisons establish equivalence; complete retries use the
unchanged checker with `SYMPY_GROUND_TYPES=python` set before importing SymPy.
The initial failed status and receipts remain in the packet. No inequality is
relaxed and a failed check is not counted as a pass.

The initial process did not record its loaded backend/version. The installed
Flint version changed from 0.8.0 to 0.9.0 during execution; no uniform measured
runtime is claimed. The portable complete-replay orchestrator has **not itself
been executed end to end**. Its identity, coverage and rejection controls were
tested. No all-Python full-census pass is claimed.

## Public reproducibility

The [rank-four replay](../supplements/rank4/PUBLIC_REPLAY.md) uses checksummed
public certificate parts. The [rank-five package](../evidence/prepublication_20261017/rank5/README.md)
reconstructs every class from recovered proof sources and pinned tensors;
the unavailable archive's ledger is not represented as recovered. Normal and
optimized replays independently produce the recorded reconstructed digest.
No private attachment is required for either public replay.

[Verification instructions](VERIFY.md) give executable commands.
[Provenance](PROVENANCE.md) records the exact ledger and archive identities.
'''
    ledger_rows=[('4','969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f','889,530','889,515 excluded; 15 realized'),('5',rank5['fresh_ledger_sha256'],'40,999','40,982 excluded; 17 realized'),('6',identity['ledger_sha256'],'25,421',f"{s['excluded']:,} excluded; {s['positive']} realized; {s['unresolved']} open")]
    ledger_rows += [(str(r),upper[r]['sha256'],f"{sum(totals(r).values()):,}",f"{totals(r)['excluded']:,} excluded; {totals(r)['unitarily_realized']} realized; {totals(r)['unresolved']} open") for r in (7,8)]
    out['docs/PROVENANCE.md']='# Provenance and boundaries\n\n'+CAUTION+f'''
The [fusion-ring-census repository](https://github.com/sebastienpalcoux/fusion-ring-census)
owns the based-ring enumeration and tensors. The original classification import is pinned
to [`{identity['census_commit']}`](https://github.com/sebastienpalcoux/fusion-ring-census/tree/{identity['census_commit']}).
Rank-specific source manifests identify the exact census revision used by each
certificate. Classification decisions are separate from census completeness.

## Current scope

| Rank | Census range | General classification |
|---:|---|---|
| 2 | Symbolic, all multiplicities | Two realized rings, both at multiplicity one. |
| 3 | Export through 1,000 | Unrestricted five-ring theorem. |
| 4 | Unrestricted | Exactly 15 models; every categorification is spherical; multiplicity at most 6. |
| 5 | Through 20 | Complete: 17 models and 40,982 exclusions. |
| 6 | Through 9 | Complete through 3 and exact bands {bands}; two open cases. |
| 7 | Through {bound(7)} | {rank7_scope}. |
| 8 | Through 2 | Complete: 77 models and 896 exclusions. |

'''+overview(stage,'../')+'''

The [current document manifest](../data/current_document_revision.json) binds
the manuscript sources, PDFs and web copies. The
[classification status](../data/classification_status.json) binds the decision
ledgers and records every exact-multiplicity partition.

## Ledger identity

| Rank | Ledger SHA-256 | Records | Partition |
|---:|---|---:|---|
'''+''.join(f'| {r} | `{h}` | {n} | {v} |\n' for r,h,n,v in ledger_rows)+f'''
Rank-six realizations comprise 56 unitary models and one spherical model whose
ring has no pseudo-unitary categorification. The rank-four certificate contains
one header and 889,530 decision records. Missing classification coverage is
recorded as `unassessed`, never inferred to be an exclusion.

The rank-five ledger is reconstructed; its [package manifest](../evidence/prepublication_20261017/rank5/package.json)
binds the exact public inputs. Its archive digest is `{rank5['sha256']}`.
The separately retained digest `{rank5['historical_ledger_reference_sha256']}`
identifies an unavailable source ledger and is not a claim to possess those bytes.

## Archive and source bindings

The rank-six source archive `{identity['archive']['name']}` has SHA-256
`{identity['archive']['sha256']}` and {identity['archive']['files']:,} files.
Its source-bound certificates and replay receipts are identifiable independently
of the current manuscript manifest. The [current research download](https://sebastienpalcoux.github.io/grothendieck-ring-classification/downloads/review-update-2026-10-17.zip)
collects the integrated manuscripts and supporting evidence.

The rank-four compressed certificate is 75,825,461 bytes with SHA-256
`969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f`;
its [public parts manifest](../supplements/rank4/certificates/manifest.json)
is checked during restoration. The 610-file computational source manifest has
SHA-256 `aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851`.
Hashes identify sources and do not certify their mathematics.

## Tensor crosswalks

The [rank-five crosswalk](../data/rank5_crosswalk.json) compares all 28,493
inputs at multiplicities 1–18 under all 24 unit-fixing basis permutations.
The two sets of canonical representatives agree at every multiplicity.
Labels may differ, so certificate transport requires the recorded based-ring
isomorphism. At multiplicities 19–20 the extension verifies 12,506 tensors
in the pinned source order. Its [report](../supplements/rank5/verification/extension19_20_verification.json)
binds tensor source SHA-256 `4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb`.

The [rank-six crosswalk](../data/rank6_crosswalk.json) compares all 25,421 full
tensor lines through multiplicity nine and identical compressed-file hashes.
The import additionally checks all 120 unit-fixing basis permutations and
retains 16,612 established representatives and identifiers.

For the exact scope of full-certificate and continuation checks, see
[verification coverage](PREPUBLICATION_REVIEW.md) and [replay commands](VERIFY.md).
The [AnyonWiki packet](../evidence/anyonwiki/README.md) binds the associators
and tensor identifications used by the positive constructions.
'''
    out['docs/VERIFY.md']='# Reproduce the data and mathematical checks\n\n'+CAUTION+'''
The [coverage report](PREPUBLICATION_REVIEW.md) states which computations were
actually executed. Program success checks its declared algebraic conditions;
it does not establish unproved categorical reductions or coherence.

## Restore and validate

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/validate_release.py
python3 tools/render_publication_docs.py --check
python3 tools/render_readme.py --check
```

Restoration needs only Python's standard library, works offline and checks
SHA-256 for every part and reconstructed file. `--check` verifies existing
restored files. The validation commands check publication identities, data
partitions and generated pages; they do not replay all mathematical proofs.

## Unrestricted rank-four classification

The theoretical proof gives FPdim < 1000 and multiplicity at most 31 without a pivotality hypothesis. The [self-contained replay package](../supplements/rank4/unrestricted/README.md) enumerates all 1,692 rings below that dimension bound and verifies 1,677 exclusions and 15 models. From its directory, run `python3 supplementary/check.py`; `--deep` adds unpruned and independent small-box checks. Mathematical hypotheses are proved in the [unrestricted manuscript](../manuscripts/rank4/papers/companion.pdf). Exact computation does not replace independent verification of those arguments.

## Complete rank-four and rank-five checks

Rank four requires Python 3.10 or newer and a C++17 `g++` compiler:

```bash
python3 supplements/rank4/restore_certificate.py
python3 -m pip install -r supplements/rank4/requirements.txt
cd supplements/rank4
python3 verify.py --workers 4
```

Return to the repository root for the rank-five public replay. Its
[package guide](../evidence/prepublication_20261017/rank5/README.md) gives the
pinned Python dependencies and C++17 requirement.

```bash
python3 evidence/prepublication_20261017/rank5/replay.py --check-package
python3 evidence/prepublication_20261017/rank5/replay.py --jobs 2
python3 -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

These are full checks of 889,530 rank-four classes and 40,999 rank-five classes.
The rank-five ledger is reconstructed and has its own source-bound digest.
Neither public route requires a private attachment.

## Complete rank-six route

**The portable complete-replay orchestrator has not been executed end to end.**
Its identity and rejection controls were tested. The executed campaign combines
25,355 passes in the initial full process with seven complete Python-backend
retries and two separate post-loop checks. The initial process's failed status
is preserved. This is not a single successful full run or an all-Python full
census replay. The [backend packet](../evidence/prepublication_20261017/rank6_backend/README.md)
records exact coverage, environment observations and matrix comparisons.

Use a fresh restored checkout, with no pre-existing native binaries beside
the rank-six C++ sources. In an isolated environment, from the repository root:

```bash
python3 -m pip install -r supplements/rank6/requirements.txt
python3 evidence/prepublication_20261017/rank6_backend/replay_complete.py \\
  --repo . --output-dir NEW_DIR --jobs 2
```

`NEW_DIR` must be a new directory outside `supplements/rank6`. The wrapper runs
normal Python: complete FLINT verification, complete Python-backend retries
for every failure, then the original post-loop checks. It rejects incomplete
coverage, changed inputs and unexpected failures. Read the
[full replay instructions](../evidence/prepublication_20261017/FULL_REPLAY.md#rank-six-combined-replay)
for native-cache and environment details. The initial audited process did not
capture its loaded backend/version; the installed Flint version changed during
execution, so no uniform measured runtime is claimed.

## Upper-rank and continuation checks

```bash
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The `--historical` option replays the complete dependency chain with each
source-bound program run in its isolated compatible input snapshot. Omitting
it does not execute all constructor dependencies. Both commands verify the
current accepted decision inventory and source identities. They do not replace
the original full base-certificate loops described in the
[full replay guide](../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for any checker whose proof checks use `assert`.

'''+overview(stage,'../')+'''

The [inner-square rigidity package](../evidence/rigidity_20261017/README.md)
records the general `R8_2_24` obstruction and its source-bound finite checks.
Run `python3 tools/verify_rigidity_20261017.py` from the repository root for
that package. Cited mathematical theorems and categorical coherence remain
explicit proof obligations. External Normaliz or Groebner calculations are
not claimed to have been rerun.

## Individual rank-six checks

From `supplements/rank6`, the following check the named components:

```bash
python3 -O software/conformal_models.py --verify
python3 -O software/release_consistency.py
python3 -O software/replay_m9.py --jobs 2
python3 -O software/replay_m9_structure.py
python3 software/replay_m9_completion.py --output verification/m9/completion/replay_normal.json
python3 -O software/replay_m9_completion.py --output verification/m9/completion/replay_optimized.json
python3 -O research/exclusions/R6_5_1204/verify_exclusion.py
python3 -O software/frontier_replay.py --check-receipts
python3 -O software/frontier_replay.py --select R6_4_155
python3 research/frontier/new_research/replay.py
```

A receipt audit checks source hashes and completion predicates, not the
mathematics. The multiplicity-nine completion replay checks eleven standalone
certificates; all 8,809 exact-multiplicity-nine rings have general exclusions.
Necessary frontier reductions do not settle either rank-six open case.

From the repository root, replay the exact fermion and all-exponent
Minkowski certificates with:

```bash
python3 evidence/unified_20261016/rank6/verify_fermion_crossing.py --repo .
python3 evidence/rank6_laptop_20261002/all_p_minkowski/verify.py \\
  --tensors supplements/rank6/data/unresolved_tensors.json
```

The [rank-six rigidity package](../evidence/rigidity_20261017/rank6/README.md)
checks the odd cyclic Clifford constraints, all indicator sequences and
phase-mass restrictions, including the exact 640-profile domain. Run:

```bash
python3 evidence/rigidity_20261017/rank6/run_checks.py --repo .
python3 -O evidence/rigidity_20261017/rank6/run_checks.py --repo .
```

These are necessary-condition checks. Both rank-six cases remain unresolved.

No timeout constitutes an exclusion. Component checks do not replace complete
base-certificate coverage.

## Historical base census import and publication exports

'''+f'''```bash
git clone https://github.com/sebastienpalcoux/fusion-ring-census.git
git -C fusion-ring-census checkout {identity['census_commit']}
python3 tools/generate_counts.py fusion-ring-census/results/census.json
```

'''+'''The [tensor crosswalks](PROVENANCE.md#tensor-crosswalks) compare based-ring
isomorphism classes at rank five and exact labelled tensor lines at rank six.
Count agreement alone does not establish tensor identification.

Refresh publication indexes from the authoritative ledgers with:

```bash
python3 tools/update_upper_rank_status.py
python3 tools/export_grothendieck_counts.py
python3 tools/render_readme.py
python3 tools/render_publication_docs.py
python3 tools/validate_release.py
```

An enumerated band is not classified until every record has been addressed.
Preserve the distinction between census, partial classification and complete
classification. Do not enter incomplete-band lower bounds as exact OEIS terms.
Archive identities must be updated only after rebuilding the corresponding
bundle. Source and document integrity checks do not replace mathematical review.
'''
    manuscript_rows=[('Rank two','rank2.tex','rank2.pdf','Unrestricted over ℂ; two realized rings'),('Rank three','rank3.tex','rank3.pdf','Unrestricted sphericality and five-ring classification'),('**Rank four, unrestricted classification**','rank4/papers/companion.tex','rank4/papers/companion.pdf','**No multiplicity bound or initial pivotality assumption**; 15 rings and automatic sphericality'),('Rank four, finite-range companion','rank4/papers/finite.tex','rank4/papers/finite.pdf','Complete through multiplicity 128'),('Rank four, verification guide','rank4/papers/verification_guide.tex','rank4/papers/verification_guide.pdf','Exact certificate checks'),('Rank five','rank5/papers/manuscript.tex','rank5/papers/manuscript.pdf','Complete through multiplicity 20'),('Rank five, verification guide','rank5/papers/verification_guide.tex','rank5/papers/verification_guide.pdf','Exact certificates, models and replay scope'),('Rank six','rank6/papers/manuscript.tex','rank6/papers/manuscript.pdf',f'25,362 exclusions, 57 realizations, two open through 9; complete through 3 and exact bands {bands}'),('Rank six, verification guide','rank6/papers/verification_guide.tex','rank6/papers/verification_guide.pdf','Models, certificates and open-case reductions'),('Rank seven','rank7/papers/manuscript.tex','rank7/papers/manuscript.pdf',rank7_scope),('Rank eight','rank8/paper/rank8.tex','rank8/paper/rank8.pdf','Complete through multiplicity 2: 896 exclusions and 77 models')]
    page_inventory=json.loads((repo/'data/manuscript_page_counts.json').read_text())
    page_counts={record['path'].removeprefix('manuscripts/'):record['pages'] for record in page_inventory['documents']}
    page_sums=page_inventory['totals']
    out['manuscripts/README.md']='# Manuscripts\n\n'+CAUTION+'''
Each paper is a current TeX/PDF pair with its classification scope stated in
its own text. Ranks two, three and four are unrestricted in multiplicity.
Ranks five to eight use pinned finite censuses and explicit criteria.

**Project overview:** [Five-page research announcement](../announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf), with the historical classification scope, seven construction candidates, and both rank-six open cases. This announcement is separate from the research-manuscript page count.

## Unrestricted rank-four classification · 88 pages

**[Read the main PDF](rank4/papers/companion.pdf)** ·
[LaTeX source](rank4/papers/companion.tex) ·
[Rank-four reading guide](rank4/README.md)

**No multiplicity bound; no initial pivotality assumption.** The main
rank-four manuscript gives the fifteen-ring classification over ℂ and proves
that every categorification admits a spherical structure. Its proof combines
a theoretical reduction with exact finite verification.

The 29-page finite-range classification companion treats the separate census
through multiplicity 128. The unrestricted manuscript is the primary account
of the general rank-four result.

Related work on the pivotal case: Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis, [Classifying Grothendieck rings of pivotal fusion categories of rank four](https://arxiv.org/abs/2609.33272), arXiv:2609.33272. Its hypothesis is pivotality.

## All manuscripts

| Manuscript | Source | PDF | Pages | Scope |
|---|---|---|---:|---|
'''+''.join(f'| {name} | [TeX]({tex}) | [PDF]({pdf}) | {page_counts[pdf]} | {scope} |\n' for name,tex,pdf,scope in manuscript_rows)+f'''
The eight mathematical manuscripts contain **{page_sums['mathematical_manuscript']} pages**.
Including the three verification guides gives **{page_sums['mathematical_manuscripts_and_guides']} pages**;
including the {page_sums['research_status_report']}-page [research-status report]({STATUS_REPORT})
gives **{page_sums['all_distinct_documents']} pages** across twelve distinct documents.
These counts include references and appendices and count duplicate download
copies only once. The [page inventory](../data/manuscript_page_counts.json)
records every path, count and PDF checksum. The [17 October status report](prepublication-review-2026-10-17.pdf) is retained as a historical snapshot and is not counted as a current document.

Download the [open fusion tensors as Python lists](../data/remaining_cases.py).
The file names each case and states the zero-based convention `N[i][j][k]`,
unit index, duality map and canonical source checksums.

'''+'''
The sources use sections and generated tables in their sibling directories.
The [document manifest](../data/current_document_revision.json) binds all
current papers and their website copies.

'''+overview(stage,'../')+'''

The rank-six treatment includes conformal-embedding constructions, fermion
Azumaya compatibility, odd cyclic Clifford constraints and fully-faithful
tensor-functor restrictions. For the positive spherical representative of
`R6_8_1660`, all indicator sequences and central phase masses are determined,
and 640 labelled restriction-data
profiles remain in branches 68, 286, 286. These profiles and the rank-22
based-module witness are necessary-condition evidence. Both rank-six
categorification questions remain open.

Read the [research status](../docs/RESEARCH_STATUS.md),
[verification scope](../docs/PREPUBLICATION_REVIEW.md) and
[replay guide](../docs/VERIFY.md) with the papers.
'''
    out['supplements/README.md']='# Classification software and evidence\n\n'+CAUTION+'''
Restore the source datasets with `python3 tools/restore_data.py` from the
repository root. Each rank's guide states its complete inputs, dependencies
and replay scope. A copy of `software/` alone is not a complete verification
package.

| Rank | Entry point | Classification scope |
|---:|---|---|
| 4 | [Guide](rank4/README.md) · [unrestricted replay](rank4/unrestricted/README.md) · [finite replay](rank4/PUBLIC_REPLAY.md) | Unrestricted: 15 models; theoretical bound and 1,692-input exact classification. Separate 889,530-input census through 128. |
| 5 | [Guide](rank5/README.md) · [complete public replay](../docs/VERIFY.md#complete-rank-four-and-rank-five-checks) | 40,999 inputs; 40,982 exclusions and 17 models through 20. |
| 6 | [Guide](rank6/README.md) · [combined full replay](../docs/VERIFY.md#complete-rank-six-route) | 25,421 inputs; 25,362 exclusions, 57 models and two open cases through 9. |
| 7 | [Guide](rank7/README.md) | __RANK7_SCOPE__. |
| 8 | [Guide](rank8/README.md) | Complete through 2: 896 exclusions and 77 models. |

'''+overview(stage,'../')+'''

Use the [verification guide](../docs/VERIFY.md) for full base loops and the
continuation chain. Their scopes are separate. The census and enumeration code
remain in [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
Copied census code retains its license and notices. Authoritative classification
ledgers are identified in [provenance](../docs/PROVENANCE.md).
'''
    for r in (7,8):
        mdir='rank7/papers/manuscript' if r==7 else 'rank8/paper/rank8'
        ledger='output/rank7_ledger.json' if r==7 else 'data/decisions.json'
        content=f'# Rank-{r} Grothendieck rings through multiplicity {bound(r)}\n\n'+CAUTION+f'\nThe authoritative decision ledger is [`{ledger}`]({ledger}). '
        if r == 7:
            content=content.replace(f'[`{ledger}`]({ledger})', f'`{ledger}`, restored by `python3 tools/restore_data.py`')
        content+=f'Classification is complete through multiplicity {complete(r)}.'
        if complete(r)<bound(r):content+=f' Multiplicity {bound(r)} has unresolved classification records.'
        content+='\n\n| Exact multiplicity | Rings | General exclusions | Unitary models | Open |\n|---:|---:|---:|---:|---:|\n'
        for m in range(1,bound(r)+1):
            row=rows[r,m]
            content+=f"| {m} | {row['rings']:,} | {row['excluded_general']:,} | {row['realized_unitary']} | {row['unresolved_general']} |\n"
        t=totals(r);content+=f"| **Total** | **{sum(t.values()):,}** | **{t['excluded']:,}** | **{t['unitarily_realized']}** | **{t['unresolved']}** |\n"
        content+=f'''\n[Manuscript source](../../manuscripts/{mdir}.tex) · [PDF](../../manuscripts/{mdir}.pdf) · [Research status](../../docs/RESEARCH_STATUS.md)

From the repository root:

```bash
python3 tools/restore_data.py
python3 tools/verify_current_publication.py --historical
python3 -O tools/verify_current_publication.py --historical
```

The history option checks source-bound dependencies in isolated compatible
snapshots. These continuation checks do not replace the complete base-certificate
loops in the [full replay guide](../../evidence/prepublication_20261017/FULL_REPLAY.md).
Use normal Python for assertion-based checkers. Positive counts in an incomplete
band are lower bounds; a timeout or surviving necessary system proves no exclusion.
See [verification scope](../../docs/PREPUBLICATION_REVIEW.md).
'''
        if r == 7:
            content += '''\n## Multiplicity-five continuation\n\nThe current continuation is replayed with Python 3.12 and a C++17 compiler:\n\n```bash\npython3 -m pip install -r supplements/rank7/requirements-m5.txt\npython3 supplements/rank7/software/verify_m5.py\npython3 -O supplements/rank7/software/verify_m5.py\n```\n\nUse `--metadata-only` only for source and partition checks; it does not replay mathematical certificates.\nThe older top-level `analyze.py` and `verify.py` retain their M4 source commitments; run them in the preserved M4 archive, not against the extended source file.\nThe M5 release archive uses repository-relative directories and includes the frozen M4 archive. NetworkX is required by the complete Morita-dual enumeration; SciPy is optional for discovery. The assertion-based R4982 components run in an isolated unoptimized child in both aggregate modes, preserving all their checks.\n'''
        out[f'supplements/rank{r}/README.md']=content
    oeis=(repo/'oeis/README.md').read_text().replace('rank-five multiplicities 18–20 are now included after general exclusion certificates closed the former residuals.','rank-five multiplicities 18–20 are included with general exclusion certificates.')
    oeis='\n\n'.join(block for block in oeis.split('\n\n') if not block.startswith(('The 19 October rank-seven extension addresses', 'The rank-seven multiplicity-five continuation addresses')))
    out['oeis/README.md']=section(oeis,'Rank-six general classification','The unrestricted rank-four theorem',f'''Rank-six general classification is complete at exact multiplicities
**{bands}**, contiguously through **3**. Two rings remain unresolved through 9.
The rank-six census value a(9)=8809 counts all based rings regardless of
categorifiability. The exporter proposes only the rank-four and rank-five
drafts above; no incomplete band is an exact sequence term.
''')
    out['oeis/update_2026-10-02.txt']=f'''Draft comment, not an OEIS submission:

Counts concern based-isomorphism classes of fusion rings admitting a fusion category over the complex numbers, at exact multiplicity m. __RANK7_SCOPE__. Rank eight is complete through multiplicity 2: 896 exclusions and 77 models, comprising 48 models at exact multiplicity one and 29 at exact multiplicity two. Rank six has 25,362 exclusions, 57 models and two open cases through multiplicity 9; all 8,809 exact-multiplicity-nine fusion rings have general exclusion certificates.

The remaining rank-six questions are R6_4_155 and R6_8_1660. __RANK7_EXTENSION__ The 38-case study records 36 decisions: 29 proposed general exclusions and 7 unitary constructions. The general R8_2_24 exclusion follows from inner-square tensor-functor rigidity. Necessary-condition evidence and obstructions with extra assumptions do not change general unresolved status.

Reference: https://github.com/sebastienpalcoux/grothendieck-ring-classification

All results and data are AI-generated, not independently human-verified and not Lean-formalized. Use with caution. Preserve the target entry's indexing and definition; never enter an incomplete-band lower bound as an exact sequence term.
'''
    for name, content in out.items():
        content = content.replace('__RANK7_SCOPE__', rank7_scope).replace('__RANK7_EXTENSION__', extension_text)
        m5 = extension(repo)
        content = content.replace('__M5_COVERAGE__',
            f"All {m5['rings']:,} new records: {m5['excluded']:,} general-exclusion certificates, "
            f"{m5['realized']} `Rep(AGL(1,7))` model and {m5['unresolved']} open cases")
        content = content.replace('__M5_REPLAY__', replay_status(repo))
        if name in ('docs/PROVENANCE.md','docs/VERIFY.md') and census_note:
            content += '\n' + census_note + '\n'
        if name == 'docs/VERIFY.md' and census_extension:
            content += ('\nTo reproduce the new rank-seven import, check out that census commit and run:\n\n```bash\n'
                        + f"git -C fusion-ring-census checkout {census_extension['census_commit']}\n"
                        + f"python3 tools/import_rank7_m5_counts.py fusion-ring-census/results/census.json --commit {census_extension['census_commit']}\n"
                        + 'python3 supplements/rank7/software/verify_m5.py\n```\n')
        if extension_text and name.endswith('.md'):
            title_end = content.find('\n\n')
            content = content[:title_end+2] + extension_text + '\n\n' + content[title_end+2:]
        out[name] = content
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=ROOT)
    p.add_argument('--identity',type=Path)
    p.add_argument('--output-dir',type=Path)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    identity=json.loads((args.identity or args.repo/'data/rank6_release_identity.json').read_text())
    files=render(args.repo,identity)
    for name,content in files.items():
        target=(args.output_dir or args.repo)/name
        if args.check:
            if not target.is_file() or target.read_text()!=content:raise ValueError('Regenerate '+name)
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
    print(('Checked' if args.check else 'Rendered'),len(files),'publication documents')
if __name__=='__main__':main()
