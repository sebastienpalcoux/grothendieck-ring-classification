"""Check the finite positive update and preserve previously replayed exclusions.

This does not solve new pentagon equations or infer exclusions from missing data.
The three published rank-seven associators are replayed with exact arithmetic.
"""
import collections,gzip,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'evidence/anyonwiki'

def require(ok,message):
    if not ok:raise ValueError(message)

def load(path):return json.loads(path.read_text())
def digest_json(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tensor_sha(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def ty3_crossed():
    A=[[[0]*4 for _ in range(4)]for _ in range(4)]
    for i in range(3):
        for j in range(3):A[i][j][(i+j)%3]=1
        A[i][3][3]=A[3][i][3]=A[3][3][i]=1
    X=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for a in range(4):
        for b in range(4):
            for u in range(2):
                for v in range(2):
                    acted=(-b)%3 if u and b!=3 else b
                    for c in range(4):X[2*a+u][2*b+v][2*c+(u^v)]=A[a][acted][c]
    return X

def main():
    imported=load(EVIDENCE/'positive_import.json')
    baseline=load(EVIDENCE/'baseline_ledger_fingerprints.json')
    ledgers={7:load(ROOT/'supplements/rank7/output/rank7_ledger.json'),8:load(ROOT/'supplements/rank8/data/decisions.json')}
    tensors={x['id']:x['tensor']for x in ledgers[7]if x['multiplicity']==1}
    tables=[json.loads(line.replace('{','[').replace('}',']'))for line in gzip.open(ROOT/'supplements/rank8/data/rank8_tables.txt.gz','rt')if line.strip()]
    tables=sorted([T for T in tables if max(v for A in T for row in A for v in row)==1],key=lambda T:tuple(v for A in T for row in A for v in row))
    tensors.update({f'R8_1_{i}':T for i,T in enumerate(tables,1)})
    crosswalk=load(EVIDENCE/'crosswalk.json');require(len(crosswalk['matches'])==139,'crosswalk coverage')
    require({x['census_id']for x in crosswalk['matches']}==set(tensors),'crosswalk identities')
    for record in crosswalk['matches']:
        rid=record['census_id'];T=tensors[rid];W=record['match']['tensor'];p=record['match']['census_to_wiki'];n=len(T)
        require(tensor_sha(T)==record['census_tensor_sha256'],'source tensor hash '+rid)
        require(tensor_sha(W)==record['match']['tensor_sha256'],'wiki tensor hash '+rid)
        require(p[0]==0 and sorted(p)==list(range(n)),'permutation '+rid)
        require(all(T[a][b][c]==W[p[a]][p[b]][p[c]]for a in range(n)for b in range(n)for c in range(n)),'full-tensor match '+rid)
    for rank,ledger in ledgers.items():
        changed=set(imported[f'rank{rank}_ids']);ids={x['id']for x in ledger}
        require(len(ids)==len(ledger)==baseline[str(rank)]['records'],'ledger coverage')
        unchanged=[x for x in ledger if x['id']not in changed]
        negatives=[x for x in ledger if x['status']=='excluded']
        require(digest_json(unchanged)==baseline[str(rank)]['unchanged_records_sha256'],'unaffected record changed')
        require(digest_json(negatives)==baseline[str(rank)]['negative_records_sha256'],'previous exclusion altered')
        models=load(ROOT/f'supplements/rank{rank}/data/anyonwiki_models.json')
        require({x['id']for x in models}==changed,'positive import inventory')
        by={x['id']:x for x in ledger}
        for record in models:
            rid=record['id'];T=tensors[rid];require(by[rid]['status']=='unitarily_realized','positive status')
            require(record['tensor']==T,'positive census basis')
            ctors=[dict(tensor=record['model_tensor'],basis_map_source_to_model=record['census_to_wiki'])]if rank==7 else record['constructors']
            for ctor in ctors:
                p=ctor['basis_map_source_to_model'];M=ctor['tensor'];n=rank
                require(sorted(p)==list(range(n))and p[0]==0,'constructor permutation')
                require(all(T[a][b][c]==M[p[a]][p[b]][p[c]]for a in range(n)for b in range(n)for c in range(n)),'constructor tensor')
            if rid=='R8_1_36':require(record['constructors'][0]['tensor']==ty3_crossed(),'TY crossed-product construction')
    spec=importlib.util.spec_from_file_location('aw_associators',EVIDENCE/'verify_associators.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    results=[]
    for code,conductor in [('7_1_2_3_1_0_1',8),('7_1_2_12_1_0_1',28),('7_1_4_3_1_0_1',16)]:results.append(module.check(code,conductor))
    require(results==load(EVIDENCE/'associator_report.json')['results'],'exact associator report changed')
    totals={str(r):dict(collections.Counter(x['status']for x in ledger))for r,ledger in ledgers.items()}
    report=dict(status='PASS',crosswalk_tensors=139,additional_rank7_models=3,additional_rank8_models=5,
                exact_pentagon_equations=sum(r['pentagon_equations']for r in results),
                previous_negative_records_unchanged=True,unaffected_records_unchanged=True,status_totals=totals,
                scope='Independent exact rank-seven associator replay; exact crosswalk and rank-eight model tensor replay. Rank-eight categorical existence and unitary gauges rely on the cited constructions.')
    (EVIDENCE/'verification_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
