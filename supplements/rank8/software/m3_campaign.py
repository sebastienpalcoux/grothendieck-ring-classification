"""Additive rank-eight M3 ingestion and exact baseline discovery.

Historical M<=2 inputs are immutable. IDs sort the complete flattened M3
source tensors, independently of the interleaved source-line transport.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[_k]='1'
import argparse,collections,concurrent.futures,gzip,hashlib,json,shutil,signal,sys,time,traceback
from pathlib import Path
REPO=Path(__file__).resolve().parents[3];P=REPO/'supplements/rank8';OUT=REPO/'evidence/rank8_m3_20261021/pipeline'
HERE=P/'software'
sys.path.insert(0,str(HERE))
from analyze import fp,commutes,mult
from prepare import flatten
STAGES=('near_group','rank_two','zero_spectrum','lower_rank_subring','rank7_certified_subring','dnumber','noncomm_dnumber','integral_drinfeld','cyclotomic','involution_module','field_automorphisms','subring_dimension','primitive_codegree')
RAW_SHA='7baaa0a2018e11a0464c3f19da9030195421f04a73806c22363cf9d5eeb92a84'
GZ_SHA='1003a7684ec62797e63885eeb5af42fd094adc9ff3fec6caf049620b3afd0952'
OLD_SHA='7f50213174f1020bb9d90d5981892c332448cf909a56bf60b29e1143228f3f24'
INPUT_SHA=RAW_SHA
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_tables(path):
 raw=gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)
 with raw:return [json.loads(line.replace('{','[').replace('}',']')) for line in raw if line.strip()]
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(obj,separators=(',',':'))+'\n');q.replace(p)
def ingest(source):
 data=source.read_bytes();raw=gzip.decompress(data);require(hashlib.sha256(raw).hexdigest()==RAW_SHA,'new raw source hash');require(hashlib.sha256(data).hexdigest()==GZ_SHA,'new gzip source hash')
 entries=[(i,json.loads(line.replace('{','[').replace('}',']'))) for i,line in enumerate(raw.decode().splitlines(),1) if line.strip()]
 require(len(entries)==4500 and collections.Counter(mult(R) for _,R in entries)=={1:96,2:877,3:3527},'complete source counts')
 require(len({flatten(R) for _,R in entries})==4500,'literal duplicate source')
 oldraw=gzip.decompress((P/'data/rank8_tables.txt.gz').read_bytes());oldR=[json.loads(line.replace('{','[').replace('}',']')) for line in oldraw.decode().splitlines() if line.strip()]
 require([R for _,R in entries if mult(R)<=2]==oldR,'historical source is not preserved as ordered subsequence')
 old_path=P/'data/decisions.json';require(sha(old_path)==OLD_SHA,'historical decisions changed')
 old=json.loads(old_path.read_text());oldby={r['tensor_sha256']:r for r in old}
 grouped=sorted(((line,R) for line,R in entries if mult(R)==3),key=lambda z:flatten(z[1]));rows=[]
 for j,(line,R) in enumerate(grouped,1):
  rows.append({'id':f'R8_3_{j}','rank':8,'multiplicity':3,'index':j,'source_line':line,'input_source_line':line,'tensor_sha256':fp(R),'commutative':commutes(R),'tensor':R})
 byhash={r['tensor_sha256']:r for r in rows};oldlines={fp(R):i for i,R in enumerate(oldR,1)}
 transport=[]
 for line,R in entries:
  h=fp(R);r=oldby[h] if mult(R)<=2 else byhash[h]
  transport.append({'id':r['id'],'input_source_line':line,**({'old_source_line':oldlines[h]} if mult(R)<=2 else {})})
 target=P/'data/rank8_m3_tables.txt.gz';target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():shutil.copyfile(source,target)
 require(sha(target)==GZ_SHA,'additive source differs')
 write('census_m3.json',rows);write('source_transport.json',transport)
 write('source_manifest.json',{'source':str(target.relative_to(REPO)),'source_gzip_sha256':GZ_SHA,'source_raw_sha256':RAW_SHA,'old_decisions_sha256':OLD_SHA,'old_records':973,'new_records':3527,'cumulative_records':4500,'old_ordered_subsequence_preserved':True,'identifier_convention':'R8_3_i: lexicographic sorting of flattened exact-multiplicity-three source tensors; historical identifiers unchanged.'})
 return rows
_REG=None;_NEG=None
def registries():
 global _REG,_NEG
 if _REG is None:
  from analyze import model_registry,rank7_negative_registry
  _REG=model_registry()[0];_NEG=rank7_negative_registry()
 return _REG,_NEG
def certificate(stage,R):
 import analyze as a
 if stage=='near_group':return a.near_group_certificate(R)
 if stage=='rank_two':return a.rank2_certificate(R)
 if stage=='lower_rank_subring':return a.lower_subring_certificate(R,registries()[0])
 if stage=='rank7_certified_subring':return a.rank7_certified_subring_certificate(R,registries()[1])
 if stage=='dnumber':return a.dnumber_certificate(a.casimir_poly(R)) if a.commutes(R) else None
 if stage=='noncomm_dnumber':return a.noncomm_dnumber_certificate(R,a.casimir_poly(R)) if not a.commutes(R) else None
 if stage=='integral_drinfeld':return a.integral_drinfeld_certificate(R)
 if stage=='cyclotomic' and a.commutes(R):
  from rings import matrices
  from exact import cyclotomic_failure,t
  c=cyclotomic_failure([M.charpoly(t).as_poly() for M in matrices(R)])
  return {'kind':'cyclotomic',**c,'criterion':'ENO cyclotomicity of based-ring characters'} if c else None
 if stage=='involution_module' and a.commutes(R):
  import involution_module
  return involution_module.certificate(R)
 if stage=='field_automorphisms' and a.commutes(R):
  import field_automorphisms
  return field_automorphisms.certificate(R)
 if stage=='subring_dimension' and a.commutes(R) and next(a.proper_closed_subrings(R,max_rank=7),None):return a.subring_dimension_certificate(R)
 if stage=='primitive_codegree' and a.commutes(R):return a.primitive_certificate(a.casimir_poly(R))
 return None
def verify_certificate(R,c):
 from verify import verify_certificate as check
 reg,neg=registries();check(R,c,reg,neg,{}, {})
def worker(task):
 stage,row,budget=task;start=time.monotonic();out={'id':row['id'],'stage':stage,'status':'no_conclusion','scope':'general_complex_fusion_category'}
 def alarm(*a):raise TimeoutError('discovery budget exhausted')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(budget)
 try:
  c=certificate(stage,row['tensor'])
  if c:
   c=json.loads(json.dumps(c));verify_certificate(row['tensor'],c);out.update(status='excluded',certificate=c,exact_checked=True)
 except TimeoutError as e:out.update(status='timeout',diagnostic=str(e))
 except Exception as e:out.update(status='error',diagnostic=repr(e),traceback=traceback.format_exc())
 finally:signal.alarm(0)
 out['seconds']=time.monotonic()-start;return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--ingest-only',action='store_true');ap.add_argument('--jobs',type=int,default=8);ap.add_argument('--budget',type=int,default=120);ap.add_argument('--through',choices=STAGES,default=STAGES[-1]);args=ap.parse_args()
 rows=ingest(args.source) if args.source else json.loads((OUT/'census_m3.json').read_text())
 if args.ingest_only:print('INGESTED',len(rows));return
 records={r['id']:{k:v for k,v in r.items() if k!='tensor'}|{'status':'unresolved'} for r in rows};byid={r['id']:r for r in rows};attemptfile=OUT/'attempts.jsonl';donefile=OUT/'stages.json'
 attempts=[json.loads(s) for s in attemptfile.read_text().splitlines()] if attemptfile.exists() else []
 for a in attempts:
  if a['status']=='excluded':records[a['id']].update(status='excluded',criterion=a['stage'],certificate=a['certificate'])
 stages=json.loads(donefile.read_text()) if donefile.exists() else []
 for stage in STAGES[:STAGES.index(args.through)+1]:
  if stage in [r['stage'] for r in stages]:continue
  active=[byid[r['id']] for r in records.values() if r['status']=='unresolved'];start=time.monotonic();print('START',stage,len(active),flush=True)
  if stage=='zero_spectrum':
   import zero_spectrum
   cs=zero_spectrum.batch([r['tensor'] for r in active]);results=[{'id':r['id'],'stage':stage,'status':'excluded' if c else 'no_conclusion','scope':'general_complex_fusion_category',**({'certificate':c,'exact_checked':True} if c else {})} for r,c in zip(active,cs)]
  else:
   with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(worker,((stage,r,args.budget) for r in active)))
  with attemptfile.open('a') as f:
   for result in results:
    f.write(json.dumps(result,separators=(',',':'))+'\n')
    if result['status']=='excluded':records[result['id']].update(status='excluded',criterion=stage,certificate=result['certificate'])
  counts=collections.Counter(r['status'] for r in results);stages.append({'stage':stage,'entered':len(active),'outcomes':dict(counts),'seconds':time.monotonic()-start});write('stages.json',stages)
  write('decisions_m3.json',list(records.values()));write('survivors_baseline.json',[byid[r['id']] for r in records.values() if r['status']=='unresolved']);write('survivors_m3.json',[byid[r['id']] for r in records.values() if r['status']=='unresolved']);print('DONE',stage,dict(counts),flush=True)
 summary={'records':len(records),'counts':dict(collections.Counter(r['status'] for r in records.values())),'stages':stages};write('baseline_summary.json',summary);print(json.dumps(summary['counts']))
if __name__=='__main__':main()
