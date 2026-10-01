"""Cross-check live human-readable exports against the authoritative JSON ledger."""
import collections,csv,json,time,hashlib
from pathlib import Path
from exact import require
from existence import STRUCTURES,verify_ledger
ROOT=Path(__file__).resolve().parents[1]


def verify_consistency():
    start=time.monotonic()
    ledger=json.loads((ROOT/'data/decisions.json').read_text());verify_ledger(ledger)
    csvrows=list(csv.DictReader((ROOT/'data/decisions.csv').open(newline='')))
    require(len(csvrows)==len(ledger),'CSV ledger cardinality')
    for a,b in zip(ledger,csvrows):
        require((a['id'],a['m'],a['index'],a['status'])==(b['id'],int(b['multiplicity']),int(b['index']),b['status']),'CSV ledger identity mismatch')
        require(all(a['existence'][s]==b[s] for s in STRUCTURES),'CSV structure mismatch')
    counts=json.loads((ROOT/'data/classification_counts.json').read_text())
    report=json.loads((ROOT/'verification/release_summary.json').read_text())
    require(report['counts']==counts,'release summary counts are stale')
    require(report['excluded']==sum(r['status']=='excluded' for r in ledger)
            and report['unresolved']==sum(r['status']=='unresolved' for r in ledger),'release summary totals are stale')
    require(report['ledger_sha256']==hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest(),'release summary ledger hash')
    require(report['general_multiplicity_three_complete']==(not any(r['m']<=3 and r['status']=='unresolved' for r in ledger)),'release summary completion flag')
    multiplicities=sorted({d['m'] for d in ledger})
    require(multiplicities==list(range(1,max(multiplicities)+1)),'census multiplicities are not consecutive')
    require([c['multiplicity'] for c in counts]==multiplicities,'classification counts omit or duplicate a multiplicity')
    for c in counts:
        part=[d for d in ledger if d['m']==c['multiplicity']];actual=collections.Counter(d['status'] for d in part)
        require(c['classes']==len(part) and all(c[k]==actual[k] for k in ('excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved')),'classification count mismatch')
    census_rows=json.loads((ROOT/'data/census.json').read_text())
    census={r['id']:r for r in census_rows}
    require(len(census)==len(census_rows) and [(r['id'],r['m'],r['index']) for r in census_rows]
            ==[(r['id'],r['m'],r['index']) for r in ledger],'ledger/census identity or ordering mismatch')
    require(report['census_sha256']==hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest(),
            'release summary source hash')
    from release import historical_cohort,m9_records,m9_stage_reports,m9_structure_records,retained_historical_continuation,CONTINUATION_PATHS,M9_PATHS
    old_summary=json.loads((ROOT/'verification/classification/summary.json').read_text())
    historical=historical_cohort(census_rows,old_summary)
    if report.get('historical_continuation_receipt') is not None:
        _,retained=retained_historical_continuation(census_rows)
        require(report['historical_continuation_receipt']==retained,'retained M8 exact-replay receipt changed')
    new_receipts=[]
    if max(multiplicities)>=9:
        new_records,new_receipts=m9_records(census_rows)
        scoped_records,scoped_receipt=m9_structure_records(census_rows)
        require(report.get('m9_structure_only_receipt')==scoped_receipt,'M9 structure-only replay receipt is stale')
        new_by={r['id']:r for r in new_records}
        new_negative={r['id']:r for r in ledger if r['m']==9 and r['status']=='excluded'}
        require(set(new_by)==set(new_negative) and all(new_by[rid]['certificate']==new_negative[rid]['certificate'] for rid in new_by),
                'new M9 ledger certificates differ from independently replayed campaign')
        require(report['m9_campaigns']==new_receipts and report['m9_excluded']==len(new_records),
                'M9 release replay receipts are stale')
        stages=m9_stage_reports(census_rows,ledger)
        stagecsv=list(csv.DictReader((ROOT/'data/exclusion_stages_m9.csv').open(newline='')))
        require(len(stagecsv)==len(stages),'M9 stage CSV cardinality')
        for stage,row in zip(stages,stagecsv):
            require(row['criterion']==stage['stage'] and row['campaign']==stage['campaign'] and int(row['multiplicity'])==9
                    and [int(row[k]) for k in ('entered','newly_excluded','remaining')]==[stage[k] for k in ('entered','removed','remaining')],
                    'M9 stage CSV differs from committed attempts')
        oldstages=list(csv.DictReader((ROOT/'data/exclusion_stages.csv').open(newline='')))
        require(all(int(r['multiplicity'])<=max(r['m'] for r in historical) for r in oldstages),
                'historical stage table improperly includes new multiplicity')
    res=json.loads((ROOT/'data/unresolved_tensors.json').read_text())
    require([r['id'] for r in res]==[r['id'] for r in ledger if r['status']=='unresolved'],'residual export mismatch')
    require(all(r['N']==census[r['id']]['N'] for r in res),'residual tensor mismatch')
    byid={r['id']:r for r in ledger}
    require(all(r['existence']==byid[r['id']]['existence'] and r['diagnostic']==byid[r['id']]['diagnostic'] for r in res),'residual structure or diagnostic mismatch')
    catalog=json.loads((ROOT/'data/model_catalog.json').read_text())
    modelcsv=list(csv.DictReader((ROOT/'data/model_catalog.csv').open(newline='')))
    flat=[(r,c) for r in catalog for c in r['constructors']]
    require(len(modelcsv)==len(flat),'constructor CSV cardinality')
    for (r,c),s in zip(flat,modelcsv):
        require(s['id']==r['id'] and s['status']==r['status'] and s['constructor']==c['name'],'constructor CSV match')
        require(json.loads(s['basis_permutation'])==c['basis_permutation'] and all(s[k]==r['existence'][k] for k in STRUCTURES),'constructor CSV structure/permutation')
    models=(ROOT/'papers/generated_models.tex').read_text()
    require(sum(line.startswith('$R_{') for line in models.splitlines())==len(catalog),'TeX model-table cardinality')
    bfile=[line for line in (ROOT/'oeis/bfile_rank6_unassigned.txt').read_text().splitlines() if line and not line.startswith('#')]
    require([list(map(int,line.split())) for line in bfile]==[[m,sum(r['m']==m for r in ledger)] for m in multiplicities],'OEIS b-file differs from census')
    countcsv=list(csv.DictReader((ROOT/'data/rank6_counts.csv').open(newline='')))
    require([[int(r['multiplicity']),int(r['classes'])] for r in countcsv]
            ==[[m,sum(r['m']==m for r in census_rows)] for m in multiplicities], 'counting CSV differs from census')
    mechanismcsv=list(csv.DictReader((ROOT/'data/proof_mechanisms.csv').open(newline='')))
    negatives={r['id']:r for r in ledger if r['status']=='excluded'}
    require(len(mechanismcsv)==len(negatives) and {r['id'] for r in mechanismcsv}==set(negatives),
            'proof-mechanism export is incomplete or duplicates a negative')
    stageby={}
    for path in [ROOT/'certificates/classification.jsonl',*CONTINUATION_PATHS,*M9_PATHS]:
        if path.exists():
            for line in path.read_text().splitlines():
                rec=json.loads(line)
                require(rec['id'] not in stageby,'overlapping accepted certificate files')
                stageby[rec['id']]=rec['stage']
    require(all(r['first_accepted_stage']==stageby[r['id']] and int(r['multiplicity'])==negatives[r['id']]['m']
                for r in mechanismcsv),'proof-mechanism accepted stage mismatch')
    frontier=None
    if max(multiplicities)>=9:
        from frontier_m9 import verify_current
        frontier=verify_current()
    return {'passed':True,'optimized_python':not __debug__,'seconds':time.monotonic()-start,
            'census_sha256':hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest(),
            'ledger_sha256':hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest(),
            'historical_census_sha256':old_summary['census_sha256'],
            'historical_rows_preserved':len(historical),'m9_campaign_receipts':new_receipts,
            'current_frontier':frontier,
            'ledger_rows':len(ledger),'model_rows':len(catalog),'constructor_rows':len(modelcsv),'residual_rows':len(res),
            'five_structure_CSV_checks':True,'residual_structure_checks':True,'constructor_macro_checked':True,
            'separate_campaign_stage_tables_checked':True,'proof_mechanism_rows':len(mechanismcsv),
            'OEIS_prefix_preserved':True,'OEIS_complete_terms':len(multiplicities)}


if __name__=='__main__':
    result=verify_consistency();name='release_consistency_optimized.json' if not __debug__ else 'release_consistency_normal.json'
    (ROOT/'verification/current').mkdir(parents=True,exist_ok=True)
    (ROOT/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
