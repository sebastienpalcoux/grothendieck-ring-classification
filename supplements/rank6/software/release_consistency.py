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
    census={r['id']:r for r in json.loads((ROOT/'data/census.json').read_text())}
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
    return {'passed':True,'optimized_python':not __debug__,'seconds':time.monotonic()-start,'ledger_rows':len(ledger),'model_rows':len(catalog),'constructor_rows':len(modelcsv),'residual_rows':len(res),'five_structure_CSV_checks':True,'residual_structure_checks':True,'constructor_macro_checked':True,'OEIS_prefix_preserved':True,'OEIS_complete_terms':len(multiplicities)}


if __name__=='__main__':
    result=verify_consistency();name='release_consistency_optimized.json' if not __debug__ else 'release_consistency_normal.json'
    (ROOT/'verification/current').mkdir(parents=True,exist_ok=True)
    (ROOT/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
