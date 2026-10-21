"""Exact probe of Galois covariance for already forced R1154 center operators."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'evidence/rank8_next_20261021/r1154'))
import low_action_bounds as l
K=l.K
D=l.a['D']
def sigma(z):
 co=list(map(F,l.c.ec(z)))
 if len(co)<2:return z
 a,b=co;return -K(a)*K.unit+K(1684*a+b)
def enc(z):return l.c.ec(z)
def rat(z):
 v=l.c.ec(z);l.need(len(v)<=1,'rational forced operator');return F(v[0])if v else F(0)
def build(types, ix, pno):
 n=len(types);u=[[l.dims[t]*l.values[t][e]/D for t in types]for e in range(5)]
 l.need(all(sum((x*y for x,y in zip(ui,uj)),K.zero)==K(int(i==j))for i,ui in enumerate(u)for j,uj in enumerate(u)),'orthonormal low columns')
 # Reconstruct the complete forced A2 matrix for this pair histogram;
 # the five low eigencolumns alone do not exhaust its -1 eigenspace.
 import inspect
 source=inspect.getsource(l.build).replace('def build(ix):','def build_at(ix,pno):').replace("['pair11_histogram_solutions_by_high_type'][0]","['pair11_histogram_solutions_by_high_type'][pno]")
 env=dict(vars(l));exec(source,env);record=env['build_at'](ix,pno)
 need_types=[x['low']if 'low'in x else 5+x['type']for x in record['labels']]
 l.need(types==need_types,'witness basis order')
 specs=[('N2',lambda v:v[2],record['N2']),('N3-N1',lambda v:v[3]-v[1],record['K3']),('N4+N1',lambda v:v[4]+v[1],record['K4'])]
 out=[]
 for name,fn,raw in specs:
  M=[[F(x)for x in row]for row in raw]
  l.need(all(sigma(fn(l.values[t]))==fn(l.values[t])for t in types if t>=5),'rational high spectrum')
  shifts=[sigma(fn(l.values[e]))-fn(l.values[e])for e in range(5)]
  Q=[[rat(K(M[i][j])+sum((sh*ui[i]*ui[j]for sh,ui in zip(shifts,u)),K.zero))for j in range(n)]for i in range(n)]
  out.append((name,M,Q))
 return out

def main():
 path=Path(__file__).with_name('galois_fixed_review.json')
 data=json.loads(path.read_text());out=[]
 for r in data['results']:
  w=r.get('witness')
  if not w:continue
  types=[q['type']for q in w['classes']for _ in range(q['n'])]
  pi=w['expanded_permutation'];eps=w['expanded_signs'];ops=build(types,r['index'],r['histogram_solution'])
  forced=[]
  for label,operator in [(2,'N2'),(4,'N4+N1')]:
   name,M,Q=next(op for op in ops if op[0]==operator)
   candidates=[i for i,t in enumerate(types)if sigma(l.dims[label]/D)in(l.dims[t]/D,-l.dims[t]/D)]
   admissible=[i for i in candidates if M[label][label]==Q[i][i]]
   l.need(admissible==[label],'diagonal covariance forces distinguished label fixed')
   l.need(pi[label]==label,'witness obeys forced fixed labels')
   forced.append({'distinguished_label':label,'operator':name,'source_diagonal':str(M[label][label]),'dimension_class_indices':candidates,'conjugated_operator_diagonals':[str(Q[i][i])for i in candidates],'unique_admissible_image':label})
  failures=[]
  for name,M,Q in ops:
   bad=[(i,j,str(M[i][j]),str(eps[i]*eps[j]*Q[pi[i]][pi[j]]))for i in range(len(types))for j in range(len(types))if M[i][j]!=eps[i]*eps[j]*Q[pi[i]][pi[j]]]
   failures.append({'operator':name,'violations':len(bad),'first':bad[:1]})
  out.append({'pattern':r['index'],'pair_histogram':r['histogram_solution'],'forced_fixed_labels':forced,'operator_checks':failures})
 passed=all(not q['violations']for r in out for q in r['operator_checks'])
 l.need(len(out)==25 and passed,'all 25 witnesses satisfy full forced-operator covariance')
 sources=[path,Path(l.__file__)]
 print(json.dumps({'schema':'r1154-forced-operator-galois-covariance/v1','status':'PASS','scope':'Necessary modular Galois constraints only; all 25 current pair histograms still pass. These witnesses do not constitute fusion or modular data.','results':out,'all_fixed_witnesses_pass':passed,'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sources},'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
