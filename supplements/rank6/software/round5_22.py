"""Optimizer-free certificate checker for the quartic rank-30 exclusion."""
from pathlib import Path
import json,itertools,time
from fractions import Fraction
from exact import require
import round4_quartic_twists as T
import round3_m4 as M
from round5_unified import low_word_data,joint_coefficient_domains
from round5_balancing import build_coupled
ROOT=Path(__file__).resolve().parents[1]

def active_cases(old):
 return [r for r in old['cases']if 'variables'in r or r.get('retained_without_exact_decision')]

def build(R,old,rec):
 data=T.data_for(R,3);data['tab']=T.table_for(R,data);md=M.data_for(R,3,data['F'])
 br=old['profiles']['branches'][rec['low']]
 pf=next(p for c in br['cases']if c['labelling']==rec['lab']for p in c['survivors']if p['profile_index']==rec['profile_index'])
 cols=data['lows'][rec['low']];words=[w for k in (2,3)for w in itertools.combinations_with_replacement(range(1,len(cols)),k)]
 wd=low_word_data(R,md,cols,br['high_vectors'],pf['counts'],rec['lab'],words=words)
 dom=joint_coefficient_domains(wd,node_limit=5000000,time_limit=180)
 require(dom['complete'],'joint coefficient domain enumeration interrupted')
 require(not dom['impossible'],'this record expects nonempty domains')
 A,b,labels,base,keep,_=T.build_system(R,data,cols,rec['indicators'],rec['lab'])
 A,b,kept,integ=T.fixed_profile(A,b,labels,base,keep,br['high_vectors'],pf['counts'])
 ss=build_coupled(R,data,cols,rec['lab'],A,b,labels,kept,integ,wd,dom)
 return ss,{'rank':pf['rank'],'words':len(words),'coefficient_types':len(ss['coefficient_labels']),'rows':len(ss['rows']),'variables':len(ss['labels'])}

def sparse_ray(ss,y):
 require(len(y)==len(ss['rhs'])and all(type(z)is int for z in y),'invalid exact separating vector')
 lhs=[0]*len(ss['labels'])
 for row,z in zip(ss['rows'],y):
  if z:
   for j,v in row.items():lhs[int(j)]+=z*v
 require(all(z>=0 for z in lhs)and sum(x*y for x,y in zip(y,ss['rhs']))<0,'exact separating inequality failed')

def verify(R,old,cert,verify_inherited=True):
 require(cert['kind']=='joint_word_twist_profile_reduction'and cert['version']==1,'wrong certificate kind')
 if verify_inherited:T.verify(R,old)
 expected=active_cases(old);require(len(cert['cases'])==len(expected),'incomplete inherited profile domain')
 survivors=[];exclusions=0
 for rec,c in zip(expected,cert['cases']):
  key={k:rec[k]for k in ('low','lab','indicators','profile_index')}
  require(c['key']==key,'wrong profile key')
  ss,meta=build(R,old,rec);require(c['meta']==meta,'wrong regenerated system metadata')
  if 'ray'in c:sparse_ray(ss,c['ray']);exclusions+=1
  elif 'point'in c:
   x=list(map(Fraction,c['point']));require(len(x)==len(ss['labels'])and all(z>=0 for z in x),'invalid point')
   require(all(not k or z.denominator==1 for z,k in zip(x,ss['integrality'])),'nonintegral count')
   require(all(sum(x[int(j)]*z for j,z in row.items())==b for row,b in zip(ss['rows'],ss['rhs'])),'point equality failed')
   survivors.append(key|{'rank':meta['rank']})
  else:
   require(c.get('retained') is True,'unverified branch outcome');survivors.append(key|{'rank':meta['rank']})
 return {'passed':True,'optimizer_used':False,'exact_profile_exclusions':exclusions,'survivors':survivors}

def main():
 import argparse,hashlib,sys
 import scipy.optimize as opt
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,default=ROOT/'verification/current/R6_4_22_balancing_replay.json')
 args=parser.parse_args()
 def forbidden(*a,**kw):raise RuntimeError('Numerical optimizers are disabled during exact replay')
 opt.linprog=opt.milp=forbidden
 started=time.monotonic()
 R=next(x['N']for x in json.loads((ROOT/'data/census.json').read_text())if x['id']=='R6_4_22')
 old_path=ROOT/'research/round4/quartic_front/R6_4_22_frontier_certificate.json'
 cert_path=ROOT/'research/round5/fermion/R6_4_22_certificate.json'
 old=json.loads(old_path.read_text())['certificate']
 report=verify(R,old,json.loads(cert_path.read_text()),verify_inherited=True)
 report.update(python_optimized=not __debug__,inherited_frontier_replayed=True,seconds=time.monotonic()-started,
  tensor_sha256=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest())
 sources={Path(m.__file__).resolve()for m in list(sys.modules.values())if getattr(m,'__file__',None)}
 sources={p for p in sources if p.is_file()and p.is_relative_to(ROOT/'software')}
 sources.update([old_path,cert_path])
 report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(sources)}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in ('passed','exact_profile_exclusions','seconds')}),flush=True)

if __name__=='__main__':main()
