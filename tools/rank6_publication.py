"""Current rank-six publication text, derived from one release identity."""
DATE='2026-10-01'
REVISION='m9-v1'
def require(test,message):
    if not test:raise ValueError(message)
def validate_identity(identity):
    require(identity['revision']==REVISION and identity['date']==DATE,'Incorrect rank-six release identity')
    counts=identity['counts'];s=identity['summary']
    require(len(counts)==9 and sum(r[0] for r in counts)==25421 and counts[-1][0]==8809,'Incorrect source census')
    require(all(sum(r[1:])==r[0] for r in counts),'Incorrect band partition')
    require(s['excluded']==sum(r[1] for r in counts) and s['positive']==sum(r[2]+r[3] for r in counts) and s['unresolved']==sum(r[4] for r in counts),'Incorrect rank-six totals')
    require(identity['new_exclusions']==counts[-1][1],'Incorrect multiplicity-nine exclusions')
    require(len({x['id'] for x in identity['research_progress']})==s['unresolved'],'Incorrect unresolved frontier')
    require(set(identity['conformal_models'])=={'R6_4_22','R6_4_91','R6_4_629'},'Missing conformal realizations')
    require(len(identity['census_commit'])==40,'Missing pinned census revision')
def archive_url(identity):
    return 'https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/'+identity['archive']['name']
def completed_bands(identity):
    return ', '.join(str(m) for m,row in enumerate(identity['counts'],1) if row[-1]==0)
def progress_table(identity):
    return '\n'.join(['| Unresolved ring | Necessary reduction |','|---|---|']+[f"| `{x['id']}` | {x['result']} |" for x in identity['research_progress']])
def continuation_text(identity):
    validate_identity(identity);s=identity['summary'];last=identity['counts'][-1]
    return f'''The rank-six release covers **25,421 fusion rings through multiplicity 9**:
**{s['excluded']:,} excluded, {s['positive']} realized and {s['unresolved']} unresolved**.
The new stratum contains 8,809 rings, of which {last[1]:,} have exact general
exclusion certificates and {last[4]} remain unresolved. The previous decisions,
representatives and proof certificates are preserved.

The positive catalogue includes the three neutral module categories from
`(B2)_7 ⊂ (D7)_1`, `(C3)_4 ⊂ (B10)_1`, and `(B2)_12 ⊂ (E8)_1`, with full tensor identifications.

{progress_table(identity)}

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[Multiplicity-nine evidence](supplements/rank6/verification/m9/) ·
[Current frontier](supplements/rank6/research/frontier/README.md) ·
[Complete release]({archive_url(identity)})
'''
