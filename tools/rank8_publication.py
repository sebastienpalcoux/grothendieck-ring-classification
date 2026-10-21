"""Current rank-eight M3 publication, preserving frozen lower-band inputs.

The extension becomes current only when its accepted publication ledger exists.
Discovery outputs under evidence/ never activate a publication by themselves.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import rank8_frontier as frontier

HISTORICAL_LEDGER = 'supplements/rank8/data/decisions.json'
HISTORICAL_TABLES = 'supplements/rank8/data/rank8_tables.txt.gz'
HISTORICAL_MODELS = 'supplements/rank8/data/model_catalog.json'
HISTORICAL_ARCHIVE = 'supplements/rank8/rank8-verified-supplement.zip'
HISTORICAL_HASHES = {
    HISTORICAL_LEDGER: '7f50213174f1020bb9d90d5981892c332448cf909a56bf60b29e1143228f3f24',
    HISTORICAL_TABLES: '35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed',
    HISTORICAL_MODELS: 'c94dd9c14df15c306760e8378baf4469506670a27cc6d3c72c04d7f2d996b78a',
}
LEDGER = 'supplements/rank8/output/m3/ledger.json'
MODELS = 'supplements/rank8/output/m3/model_catalog.json'
TABLES = 'supplements/rank8/data/rank8_m3_tables.txt.gz'
ARCHIVE = 'supplements/rank8/release/rank8-certified-through-m3.zip'
EVIDENCE = 'evidence/rank8_m3_20261021'
PUBLICATION_DATE = '2026-10-21'
PUBLICATION_DATE_LONG = '21 October 2026'
STATUS_REPORT = 'prepublication-review-2026-10-21.pdf'
REALIZED_STATUSES = {'unitarily_realized', 'pseudo_unitarily_realized'}

def active(repo):
    return (Path(repo) / LEDGER).is_file()

def ledger_path(repo):
    if frontier.active(repo): return frontier.LEDGER
    return LEDGER if active(repo) else HISTORICAL_LEDGER

def model_path(repo):
    return MODELS if active(repo) else HISTORICAL_MODELS

def archive_path(repo):
    if frontier.active(repo): return frontier.ARCHIVE
    return ARCHIVE if active(repo) else HISTORICAL_ARCHIVE

def current_date(repo):
    from rank7_publication import PUBLICATION_DATE as previous
    return PUBLICATION_DATE if active(repo) else previous

def current_report(repo):
    from rank7_publication import STATUS_REPORT as previous
    return STATUS_REPORT if active(repo) else previous

def historical_sources(repo):
    result = {}
    for relative, digest in HISTORICAL_HASHES.items():
        raw = (Path(repo) / relative).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('Historical rank-eight input changed: ' + relative)
        result[relative] = raw
    if active(repo):
        current = json.loads((Path(repo) / ledger_path(repo)).read_text())
        if [r for r in current if r['multiplicity'] <= 2] != json.loads(result[HISTORICAL_LEDGER]):
            raise ValueError('M3 extension changes a historical rank-eight decision')
        models = json.loads((Path(repo) / MODELS).read_text())
        if [r for r in models if r['multiplicity'] <= 2] != json.loads(result[HISTORICAL_MODELS]):
            raise ValueError('M3 extension changes a historical rank-eight model')
        accepted = json.loads((Path(repo) / EVIDENCE / 'models/consolidated_models.json').read_text())
        if isinstance(accepted, dict): accepted = accepted['models']
        new_models = [r for r in models if r['multiplicity'] == 3]
        if new_models != accepted:
            raise ValueError('Published M3 model catalogue differs from the accepted manifest')
        positives = {r['id']:r['status'] for r in current if r['multiplicity']==3 and r['status'] in REALIZED_STATUSES}
        if {r['id']:r['status'] for r in new_models} != positives:
            raise ValueError('Published M3 models and classification ledger differ')
    return result

def extension(repo):
    if not active(repo): return None
    historical_sources(repo)
    continuation = frontier.validate_ledger(repo) if frontier.active(repo) else None
    path = Path(repo) / ledger_path(repo)
    records = json.loads(path.read_text())
    rows = [r for r in records if r['multiplicity'] == 3]
    if len(records) != 4500 or [r['id'] for r in rows] != [f'R8_3_{i}' for i in range(1,3528)]:
        raise ValueError('Rank-eight extension does not cover the supplied M3 band')
    counts = Counter(r['status'] for r in rows)
    if set(counts)-({'excluded','unresolved'}|REALIZED_STATUSES):
        raise ValueError('Unknown rank-eight extension status')
    return {'date':PUBLICATION_DATE,'rank':8,'multiplicity':3,'rings':len(rows),
            'excluded':counts['excluded'],'realized':sum(counts[s] for s in REALIZED_STATUSES),
            'unitarily_realized':counts['unitarily_realized'],'pseudo_unitarily_realized':counts['pseudo_unitarily_realized'],
            'unresolved':counts['unresolved'],
            'remaining_ids':[r['id'] for r in rows if r['status']=='unresolved'],
            'unitary_excluded_ids':[r['id'] for r in rows if r['status']=='unresolved' and r.get('unitary_status')=='excluded'],
            'realized_ids':[r['id'] for r in rows if r['status'] in REALIZED_STATUSES],
            'ledger':ledger_path(repo),'ledger_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'historical_ledger':HISTORICAL_LEDGER,'historical_ledger_sha256':HISTORICAL_HASHES[HISTORICAL_LEDGER],
            'source':TABLES,'source_sha256':hashlib.sha256((Path(repo)/TABLES).read_bytes()).hexdigest(),
            'evidence':frontier.EVIDENCE if continuation else EVIDENCE,
            'baseline_evidence':EVIDENCE, 'frontier':continuation,
            'attempts_source':(frontier.EVIDENCE+'/structural_models/per_ring_research_audit.json'
                               if continuation else EVIDENCE+'/pipeline/residual_attempts.json')}

def summary(repo):
    item=extension(repo)
    if item is None:
        return 'Rank eight is complete through multiplicity two, with 896 exclusions and 77 unitary models.'
    text=(f"The rank-eight multiplicity-three continuation addresses all {item['rings']:,} supplied exact-multiplicity-three rings: "
          f"{item['excluded']:,} general exclusions, {item['realized']} models and {item['unresolved']} unresolved cases. ")
    if item['pseudo_unitarily_realized']:
        text+=(f"The models comprise {item['unitarily_realized']} unitary constructions and {item['pseudo_unitarily_realized']} further pseudo-unitary "
               + ('construction. ' if item['pseudo_unitarily_realized']==1 else 'constructions. '))
    else: text+='Every recorded model admits a unitary realization. '
    return text+('The remaining rings retain unresolved status for general complex categorification.' if item['unresolved']
                else 'The classification of the supplied census is complete through multiplicity three.')
