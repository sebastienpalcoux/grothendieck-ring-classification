"""Current rank-six publication text, derived from one release identity."""
DATE='2026-09-30'
REVISION='v7'
CASE_IDS=('R6_4_155','R6_8_1660')
def require(test,message):
    if not test:raise ValueError(message)
def validate_identity(identity):
    require(identity['revision']==REVISION and identity['date']==DATE,'Incorrect rank-six release identity')
    require(identity['new_exclusions']==1,'Unexpected new categorical exclusion')
    require(identity['summary']['positive']==57 and identity['summary']['unresolved']==2,'Incorrect rank-six partition')
    require({x['id'] for x in identity['research_progress']}==set(CASE_IDS),'Incorrect unresolved frontier')
    require(set(identity['new_realizations'])=={'R6_4_22','R6_4_91','R6_4_629'},'Missing conformal realizations')
def archive_url(identity):
    return 'https://grothendieck-ring-atlas.sebastien-palcoux.chatgpt.site/downloads/'+identity['archive']['name']
def completed_bands(identity):
    return ', '.join(str(m) for m,row in enumerate(identity['counts'],1) if row[-1]==0)
def progress_table(identity):
    return '\n'.join(['| Unresolved ring | Necessary reduction |','|---|---|']+[f"| `{x['id']}` | {x['result']} |" for x in identity['research_progress']])
def continuation_text(identity):
    validate_identity(identity)
    return f'''The rank-six release constructs three unitary models from conformal embeddings:
`R6_4_22` from `(B2)_7 ⊂ (D7)_1`, `R6_4_91` from `(C3)_4 ⊂ (B10)_1`,
and `R6_4_629` from `(B2)_12 ⊂ (E8)_1`. Each is the neutral module category,
with all 216 fusion coefficients verified. The census now has **16,553 excluded,
57 realized and 2 unresolved rings**.

R6_5_1204 is excluded by a complete exact center-integrality certificate.

{progress_table(identity)}

[Manuscript](manuscripts/rank6/papers/manuscript.pdf) ·
[Exact constructors](supplements/rank6/software/conformal_models.py) ·
[Current frontier](supplements/rank6/research/frontier/README.md) ·
[Complete release]({archive_url(identity)})
'''
