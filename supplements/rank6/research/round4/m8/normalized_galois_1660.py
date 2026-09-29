import sys,json,time,signal,math,collections
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising_verlinde as M
from exact import evaluate,key
from higher_traces import farkas,check_farkas
from frontier_feasibility import rational_feasible
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_1660');old=json.load(open(P/'research/round4/m8/1660_necessary_witness.json'));st=time.monotonic();out={}
def stop(*a):raise TimeoutError('explicit 800 second augmented signature budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(800)
try:
 d=M.data_for(R,3,24);cols=tuple(map(tuple,old['columns']));ep=old['indicators'];A,b,meta=M.system(R,d,cols,ep,old['labelling']);C=d['C'];types=d['phases'];tab=d['tab'];G,vs,sp=d['_branch_cache'][cols];vs=[v for v in vs if list(v) not in sp.forbidden]
 labels=[(v,ti) for v in vs for ti in range(len(types)) if all((not v[g-1] and not v[ss-1]) or (v[g-1] and not v[ss-1] and types[ti]==tuple(C((-1)**k) for k in range(1,4))) or (v[ss-1] and not v[g-1] and types[ti] in d['ising_types'][ss][ep[ss-1]]) for g,ss in d['ising_labels'])]
 sigs={v:(tab.dims[v]**2/tab.D**2,)+tt for v,tt in zip(sp.vectors,sp.types)};one=types.index(tuple(C.one for _ in range(3)));low=collections.Counter((sigs[v],one) for v in cols);pos=collections.defaultdict(list)
 for j,(v,ti) in enumerate(labels):pos[sigs[(0,)+v],ti].append(j)
 allpairs=set(pos)|set(low);seen=set();rows=[];rhs=[]
 for a in range(24):
  if math.gcd(a,24)>1:continue
  M.require(a*a%24==1,'trace-field Galois square is not the identity')
  for sig,ti in sorted(allpairs,key=str):
   nsig=tuple(evaluate(z.to_list(),C.unit**a,C) for z in sig);pair=tuple(sorted(((str(sig),ti),(str(nsig),ti))))
   if pair in seen or sig==nsig:continue
   seen.add(pair);row=[0]*len(A[0])
   for j in pos[sig,ti]:row[j]+=1
   for j in pos[nsig,ti]:row[j]-=1
   value=low[nsig,ti]-low[sig,ti]
   if any(row) or value:rows.append(row);rhs.append(value)
 xx={j:Fraction(num,den) for j,num,den in old['primal']};fails=sum(sum(Fraction(row[j])*v for j,v in xx.items())!=rv for row,rv in zip(rows,rhs));A+=rows;b+=rhs
 y=farkas(A,b)
 if y is not None:check_farkas(A,b,y)
 x=None if y else rational_feasible(A,b)
 out={'id':'R6_8_1660','scope':'pseudo_unitary_necessary_single_branch','existing_witness_failed_augmented_equations':fails,'added_equations':len(rows),'equations':len(A),'variables':len(A[0]),'outcome':'single_branch_excluded' if y else 'exact_augmented_necessary_relaxation_survives' if x else 'no_exact_obstruction','ray':y,'primal':x,'height':3,'conductor':24,'columns':old['columns'],'indicators':ep,'labelling':old['labelling']}
except TimeoutError as e:out={'outcome':'budget_incomplete','reason':str(e)}
finally:signal.alarm(0)
out['seconds']=time.monotonic()-st;(P/'research/round4/m8/1660_normalized_galois.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print({k:v for k,v in out.items() if k not in ('ray','primal')},flush=True)
