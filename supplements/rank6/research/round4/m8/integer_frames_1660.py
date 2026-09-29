import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising_verlinde as M
from integer_gram import frames,GramSearchBudget
from higher_traces import farkas,check_farkas
from frontier_feasibility import rational_feasible
st=time.monotonic();R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_1660');outpath=P/'research/round4/m8/1660_integer_frames.json';out={'scope':'pseudo_unitary_necessary_single_low_labelling_indicator_branch','height':3,'low':0,'labelling':[0,5,4,1,3,2],'indicators':[1,1,1,-1,1]}
def stop(*a):raise TimeoutError('explicit 800 second integral-frame budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(800)
try:
 d=M.data_for(R,3,24);cols=d['lows'][0];ep=out['indicators'];A,b,meta=M.system(R,d,cols,ep,out['labelling']);out['system']=meta
 C=d['C'];types=d['phases'];G,vs,spec=d['_branch_cache'][tuple(map(tuple,cols))];bad=set(map(tuple,spec.forbidden));vs=[v for v in vs if v not in bad]
 labels=[(v,ti) for v in vs for ti in range(len(types)) if all((not v[g-1] and not v[ss-1]) or (v[g-1] and not v[ss-1] and types[ti]==tuple(C((-1)**k) for k in range(1,4))) or (v[ss-1] and not v[g-1] and types[ti] in d['ising_types'][ss][ep[ss-1]]) for g,ss in d['ising_labels'])]
 vectors=sorted({v for v,ti in labels});ff=frames(G,[(v,None) for v in vectors],60);out.update(high_columns=vectors,frames=list(map(list,ff)),frame_count=len(ff),cases=[]);print('complete integer frames',len(ff),'columns',len(vectors),flush=True)
 outpath.write_text(json.dumps(out,separators=(',',':'))+'\n')
 for k,counts in enumerate(ff):
  keep=[j for j,(v,ti) in enumerate(labels) if counts[vectors.index(v)]]+list(range(len(labels),len(A[0])))
  AA=[[row[j] for j in keep] for row in A];bb=list(b)
  for v,c in zip(vectors,counts):
   if c:AA.append([int(j<len(labels) and labels[j][0]==v) for j in keep]);bb.append(c)
  y=farkas(AA,bb)
  if y is not None:check_farkas(AA,bb,y)
  rec={'frame':k,'rows':len(AA),'variables':len(AA[0]),'ray':y,'excluded':y is not None};out['cases'].append(rec)
  if y is None:
   x=rational_feasible(AA,bb);rec.update(primal=x,kept_variables=keep,center_rank=6+sum(counts));out['outcome']='exact_integral_gram_relaxation_survives' if x else 'no_exact_obstruction';print('surviving frame',k,'rank',6+sum(counts),'exactprimal',x is not None,flush=True);break
  if k%50==0:print(k,'excluded',flush=True)
 else:out['outcome']='selected_branch_excluded_by_all_integer_frames'
except (TimeoutError,GramSearchBudget) as e:out.update(outcome='budget_incomplete',reason=str(e))
finally:signal.alarm(0)
out['seconds']=time.monotonic()-st;outpath.write_text(json.dumps(out,separators=(',',':'))+'\n');print({k:v for k,v in out.items() if k not in ('frames','cases','high_columns','system')},flush=True)
