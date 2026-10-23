from arithmetic import *
from prepare import key
from functools import lru_cache
import involution_module

@lru_cache(None)
def ckey(serial):return key(json.loads(serial))
def can(R):return ckey(json.dumps(R,separators=(',',':')))
def dual(R):return [next(j for j in range(len(R)) if R[i][j][0]) for i in range(len(R))]
def subrings(R):
 n=len(R);d=dual(R)
 for mask in range(1,(1<<(n-1))-1):
  J=[0]+[i for i in range(1,n) if mask>>(i-1)&1]
  if len(J)>8:continue
  S=set(J)
  if any(d[i] not in S for i in J):continue
  if any(R[i][j][k] and k not in S for i in J for j in J for k in range(n)):continue
  yield J,[[[R[i][j][k] for k in J] for j in J] for i in J]

def registry():
 p=ROOT/'repositories/classification-sparse/supplements'
 out=[]
 for n in [0,1]:
  out.append(dict(name=['Vec(C2)','Fibonacci'][n],tensor=[[[1,0],[0,1]],[[0,1],[1,n]]]))
 R=[[[int(k==(i+j)%3) for k in range(3)] for j in range(3)] for i in range(3)]
 out.append(dict(name='Vec(C3)',tensor=R))
 for name,(k,l,m,n) in [('Ising',(1,0,0,0)),('Rep(S3)',(1,0,1,0)),('PSU(2)5',(1,1,1,0))]:
  R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,m,k],[0,k,l]],[[0,0,1],[0,k,l],[1,l,n]]]
  out.append(dict(name=name,tensor=R))
 for rel in ['rank8/data/lower_rank_positive_models.json','rank8/data/rank6_positive_models.json','rank7/data/model_catalog.json','rank8/data/model_catalog.json']:
  for r in json.load(open(p/rel)):
   R=r['tensor']
   if max(v for A in R for row in A for v in row)>1:continue
   out.append(dict(name=r.get('name',r.get('id')),tensor=R,source=rel,source_reference=r.get('source_reference',r.get('reference'))))
 regs=collections.defaultdict(set)
 for r in out:regs[len(r['tensor'])].add(can(r['tensor']))
 counts={n:len(v) for n,v in regs.items()};assert counts=={2:2,3:4,4:9,5:10,6:21,7:13,8:48},counts
 (HERE/'lower_positive_registry.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 return regs

def main():
 regs=registry();rows=read();ar={r['id']:r for r in json.load(open(HERE/'arithmetic.json'))};sp={r['id']:r for r in json.load(open(HERE/'spectra/zero_spectrum.json'))['records']}
 out=[]
 for r in rows:
  R=r['tensor'];rec={k:v for k,v in r.items() if k!='tensor'};cs=[]
  for J,S in subrings(R):
   if can(S) not in regs[len(S)]:
    c=dict(kind='excluded_lower_subring',subset=J,subrank=len(J),subtensor_sha256=sha(S),scope='general_complex_fusion_category',criterion='Complete multiplicity-one classifications in ranks 2 through 8; closed based subring must categorify')
    direct=dnumber(S) or near_group(S) or cyclotomic(S) or integral_drinfeld(S)
    if direct:c['direct_subring_certificate']=direct
    cs.append(c);break
  # Run module test only if not already generally excluded.
  if not cs and not ar[r['id']]['certificates'] and not sp[r['id']]['certificate']:
   c=involution_module.certificate(R)
   if c:involution_module.verify(R,c);cs.append(c)
  rec['certificates']=cs;out.append(rec)
  if cs:print(r['id'],[(x['kind'],x.get('subrank')) for x in cs],flush=True)
  if len(out)%20==0:(HERE/'structural.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'structural.json').write_text(json.dumps(out,indent=2)+'\n')
 ex={r['id'] for r in out if r['certificates']}|{r['id'] for r in ar.values() if r['certificates']}|{r['id'] for r in sp.values() if r['certificate']}
 su=[{k:v for k,v in r.items() if k!='tensor'} for r in rows if r['id'] not in ex]
 (HERE/'survivors.json').write_text(json.dumps(su,indent=2)+'\n')
 print('EXCLUDED',len(ex),'SURVIVORS',len(su),collections.Counter(r['rank'] for r in su))
if __name__=='__main__':main()
