"""Transfer frozen general nonexistence along a verified based subring."""
from pathlib import Path
import argparse,functools,hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/software'))
from prepare import key
from analyze import proper_closed_subrings,dual
from exact import require

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def file_digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

@functools.lru_cache(None)
def catalog():
    c6path=ROOT/'supplements/rank6/data/census.json';d6path=ROOT/'supplements/rank6/data/decisions.json';d7path=ROOT/'supplements/rank7/output/rank7_ledger.json'
    c6={r['id']:r for r in json.loads(c6path.read_text()) if r['m']<=3}
    negatives=[]
    for d in json.loads(d6path.read_text()):
        if d['id'] in c6 and d.get('existence',{}).get('general')=='no':
            negatives.append({'id':d['id'],'tensor':c6[d['id']]['N'],'decision_path':str(d6path.relative_to(ROOT)),'decision_sha256':digest(d),'tensor_path':str(c6path.relative_to(ROOT))})
    for d in json.loads(d7path.read_text()):
        if d['multiplicity']<=3 and d['status']=='excluded':
            require(d.get('certificate') is not None,'rank-seven negative lacks frozen proof')
            negatives.append({'id':d['id'],'tensor':d['tensor'],'decision_path':str(d7path.relative_to(ROOT)),'decision_sha256':digest(d),'tensor_path':str(d7path.relative_to(ROOT))})
    bykey={}
    for row in negatives:
        canonical,order=key(row['tensor'],witness=True);row['order']=order;row['tensor_sha256']=digest(row['tensor']);bykey.setdefault((len(row['tensor']),canonical),row)
    return negatives,bykey

def discover(R):
    negatives,bykey=catalog()
    for subset,S in proper_closed_subrings(R,max_rank=7):
        if len(S) not in (6,7):continue
        canonical,order=key(S,witness=True);row=bykey.get((len(S),canonical))
        if row is None:continue
        permutation=[None]*len(S)
        for i,j in zip(order,row['order']):permutation[i]=j
        c={'kind':'certified_negative_subring_transfer','subset':list(subset),'basis_map':permutation,'source_id':row['id'],'source_tensor_sha256':row['tensor_sha256'],'source_decision_path':row['decision_path'],'source_decision_sha256':row['decision_sha256'],'source_tensor_path':row['tensor_path']}
        verify(R,c);return c
    return None

def verify(R,c):
    require(c['kind']=='certified_negative_subring_transfer','wrong subring kind');subset=c['subset'];n=len(R)
    require(subset==sorted(set(subset)) and subset[0]==0 and len(subset) in (6,7) and all(0<=i<n for i in subset),'invalid proper basis subset')
    I=set(subset);du=dual(R);require(all(du[i] in I for i in I),'subset not dual closed')
    require(all(not R[i][j][k] for i in I for j in I for k in range(n) if k not in I),'subset not multiplication closed')
    rows=json.loads((ROOT/c['source_decision_path']).read_text());d=next(r for r in rows if r['id']==c['source_id'])
    require(digest(d)==c['source_decision_sha256'],'frozen negative decision changed')
    require(d.get('existence',{}).get('general')=='no' if len(subset)==6 else d['status']=='excluded' and d.get('certificate') is not None,'source is not a general negative')
    if c['source_tensor_path']==c['source_decision_path']:T=d['tensor']
    else:T=next(r['N'] for r in json.loads((ROOT/c['source_tensor_path']).read_text()) if r['id']==c['source_id'])
    require(digest(T)==c['source_tensor_sha256'],'source tensor changed');p=c['basis_map'];m=len(subset)
    require(p[0]==0 and sorted(p)==list(range(m)),'invalid based isomorphism')
    require(all(R[subset[i]][subset[j]][subset[k]]==T[p[i]][p[j]][p[k]] for i in range(m) for j in range(m) for k in range(m)),'subring tensor does not match known negative')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();dest=HERE/'subring_transfer.json'
    rows=json.loads((HERE.parent/'pipeline/survivors_m3.json').read_text());byid={r['id']:r for r in rows}
    if args.verify:
        saved=json.loads(dest.read_text())
        for rec in saved['records']:
            row=byid[rec['id']];require(rec['tensor_sha256']==row['tensor_sha256'],'source tensor hash mismatch');verify(row['tensor'],rec['certificate'])
        print('PASS',len(saved['records']));return
    records=[]
    for row in rows:
        c=discover(row['tensor'])
        if c:records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category','certificate':c})
    negatives,_=catalog();out={'result':'PASS','catalog_counts':{str(n):sum(len(r['tensor'])==n for r in negatives) for n in (6,7)},'records':records}
    dest.write_text(json.dumps(out,separators=(',',':'))+'\n');excluded={r['id'] for r in records};(HERE/'survivors_after_subrings.json').write_text(json.dumps([r for r in rows if r['id'] not in excluded],separators=(',',':'))+'\n')
    print(json.dumps({'excluded':len(records),'catalog_counts':out['catalog_counts']}))
if __name__=='__main__':main()
