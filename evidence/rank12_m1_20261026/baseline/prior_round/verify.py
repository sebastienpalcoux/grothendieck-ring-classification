"""Exact accepted third-round replay and complete ledger binding."""
from pathlib import Path
import collections,csv,hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
LOG=ROOT/'verification';LOG.mkdir(exist_ok=True)
def need(c,m):
 if not c:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
mode='normal'if __debug__ else'optimized';start=time.monotonic()
steps=['d120/verify.py','d32/r240_model.py','d32/r408_model.py','d48/verify.py','c6/verify.py','d120/audit_R350.py','d144/verify.py','independent/verify.py','independent/audit_graph_twist.py','independent/audit_ising_dual.py','independent/audit_d48.py']
checks=[]
for j,rel in enumerate(steps,1):
 script=ROOT/'round3'/rel;t=time.monotonic()
 result=subprocess.run([sys.executable,*([]if __debug__ else['-O']),str(script)],cwd=script.parent,capture_output=True,text=True,env=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1'))
 (LOG/f'{mode}_{j:02}.log').write_text(result.stdout+result.stderr)
 if result.returncode:print((result.stdout+result.stderr)[-5000:]);raise RuntimeError('failed: '+rel)
 checks.append(dict(script=rel,status='PASS',seconds=time.monotonic()-t));print(f'{j:02}/{len(steps)} PASS {rel}',flush=True)
baseline=read(ROOT/'prior_round/ledger.json');old={r['id']:r for r in baseline['records']}
T=read(ROOT/'prior_round/evidence/rank12-m1-offline-20261025/tensors.json')
ledger=read(ROOT/'ledger.json');summary=read(ROOT/'summary.json');new=read(ROOT/'new_decisions.json')
need(ledger['summary']==summary,'summary binding')
need((summary['excluded'],summary['modeled'],summary['unresolved'])==(438,148,46),'totals')
need(summary['online_revision_performed']is False,'offline flag')
pos=new['models'];neg=new['exclusions'];need(len(pos)==7 and len(neg)==13 and not set(pos)&set(neg),'new counts')
need(all(old[r]['status']=='unresolved'for r in set(pos)|set(neg)),'only unresolved statuses changed')
rows=ledger['records'];by={r['id']:r for r in rows};need(len(rows)==len(by)==632 and set(by)==set(T),'all IDs exactly once')
for rid,R in T.items():
 expected='unitarily_realized'if rid in pos else'excluded'if rid in neg else old[rid]['status']
 need(by[rid]['status']==expected and by[rid]['tensor_sha256']==sha(R),'decision/input binding '+rid)
for rid,m in pos.items():
 p=m['basis_map_source_to_model'];N=m['model_tensor']
 need(p[0]==0 and sorted(p)==list(range(12)),'unit preserving bijection')
 need(all(T[rid][i][j][k]==N[p[i]][p[j]][p[k]]for i in range(12)for j in range(12)for k in range(12)),'complete model match '+rid)
 for key in ['proof','evidence','independent_audit']:need((ROOT/m[key]).is_file(),'model evidence link')
for rid,n in neg.items():
 need(n['scope']=='general_complex_fusion_category','exclusion scope')
 for key in ['proof','replay','independent_audit']:need((ROOT/n[key]).is_file(),'exclusion evidence link')
remaining=read(ROOT/'unresolved_tensors.json');remids={r['id']for r in remaining}
need(len(remaining)==len(remids)==46 and remids=={r for r in by if by[r]['status']=='unresolved'},'complete unresolved list')
for r in remaining:need(r['tensor']==T[r['id']] and r['tensor_sha256']==sha(T[r['id']]),'unresolved tensor binding')
need(dict(collections.Counter(r['exact_dimension_character']['family']for r in remaining))==summary['remaining_family_counts'],'family counts')
with(ROOT/'ledger.csv').open(newline='')as f:csvrows=list(csv.DictReader(f))
need(len(csvrows)==632 and {r['id']for r in csvrows}==set(T),'CSV IDs')
need(all(r['status']==by[r['id']]['status']and r['tensor_sha256']==by[r['id']]['tensor_sha256']for r in csvrows),'CSV binding')
for rel,digest in read(ROOT/'prior_snapshot_manifest.json').items():
 need(hashlib.sha256((ROOT/'prior_round'/rel).read_bytes()).hexdigest()==digest,'frozen prior-round file '+rel)
receipt=dict(status='PASS',excluded=438,modeled=148,unresolved=46,new_exclusions=13,new_models=7,optimized_python=not __debug__,steps=checks,elapsed_seconds=time.monotonic()-start)
(LOG/f'{mode}.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items()if k!='steps'},indent=2))
