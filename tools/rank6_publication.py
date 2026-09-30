"""Shared rank-six publication text and the round-five evidence boundary."""
DATE = '2026-09-30'
REVISION = 'round5'
NEW_EXCLUSIONS = 0
RESEARCH_SUMMARY = (
    'Round five unifies joint restriction-word Gram constraints, exact bounded '
    'integer searches and modular-representation completion. The six unresolved '
    'rings have the finite necessary-data reductions recorded in the research '
    'coverage inventory. No categorical exclusion or realization is allocated.'
)
CASE_IDS = ('R6_4_22', 'R6_4_91', 'R6_4_155', 'R6_4_629', 'R6_5_1204', 'R6_8_1660')


def require(test, message):
    if not test:
        raise ValueError(message)

def validate_identity(identity):
    require(identity['revision'] == REVISION and identity['date'] == DATE,
            'Expected the final round5 identity dated 2026-09-30')
    require(identity['new_exclusions'] == 0, 'Round5 allocates no categorical exclusions')
    require(identity['summary']['unresolved'] == 6, 'Expected the six unresolved rings')
    require(identity['research_summary'] and isinstance(identity['research_summary'], str),
            'A nonempty research_summary is required by the atlas')
    require({x['id'] for x in identity['research_progress']} == set(CASE_IDS),
            'Research progress must cover exactly the six unresolved rings')

def archive_url(identity):
    return ('https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/'
            + identity['archive']['name'])

def completed_bands(identity):
    return ', '.join(str(m) for m, row in enumerate(identity['counts'], 1) if row[-1] == 0)

def progress_table(identity):
    rows = ['| Unresolved ring | Exact necessary-data reduction |', '|---|---|']
    rows += [f"| `{x['id']}` | {x['result']} |" for x in identity['research_progress']]
    return '\n'.join(rows)

def continuation_text(identity):
    validate_identity(identity)
    a, s = identity['archive'], identity['summary']
    return f"""The fifth rank-six continuation makes **no new categorical decisions**:
the partition remains **{s['excluded']:,} excluded, {s['positive']} realized and
{s['unresolved']} unresolved**. General classification is complete through
multiplicity three, and the exact bands **{completed_bands(identity)}** are
fully classified. All 577 rings through multiplicity three remain decided:
531 excluded and 46 realized, including 45 with unitary models.

The new joint restriction-word Gram criterion, exact bounded integer searches,
modular-word closure and finite modular-representation completion give:

{progress_table(identity)}

These are necessary data. A surviving modular matrix, fusion tensor or exact
integer witness supplies no associator or categorification. The joint-pattern result for `R6_8_1660` and its twist witness concern separate
necessary systems.

The four accepted exclusion continuation files still contain 7, 18, 12 and 4
disjoint general exclusions. Their original proof provenance is retained.
See the [revision notes](supplements/rank6/REVISION_NOTES.md),
[six remaining tensors](supplements/rank6/data/unresolved_tensors.json),
[round-five research](supplements/rank6/research/round5/README.md),
[coverage and replay inventory](supplements/rank6/research/round5/coverage.json),
and [verification instructions](docs/VERIFY.md).
The [complete revised rank-six ZIP]({archive_url(identity)}) contains all
{a['files']:,} released files. The preceding release's four general exclusions
remain accepted; this revision adds finite reductions of the unresolved cases.
"""
