#!/usr/bin/env python3
"""Saturation masks on the frozen whole-domain R982 joint phase system."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys
from dimension_mask import conductor_types,need,cosines24,spectral_capacities
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_next_20261021/r982'
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/global_induction'))
import column_generation as cg
sys.path.insert(0,str(ROOT/'evidence/rank8_m3_20261021/noncommutative'))
import biquadratic_traces as bq

class System:
 def __init__(self,columns,rhs):self.columns=columns;self.rhs=rhs;self.nvars=len(columns);self.nrows=len(rhs)
 def column(self,j):return self.columns[j]

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--conductor',action='store_true');p.add_argument('--spectral',action='store_true');a=p.parse_args();a.conductor=a.conductor or a.spectral
 system=json.loads((OLD/'joint_phase_system.json').read_text());profile=json.loads((ROOT/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json').read_text())['records'][2]
 dimrow=next(r for r in json.loads((ROOT/'evidence/rank8_research_20261022/pointed_followup/dimension_block/verification.json').read_text())['records']if r['id']=='R8_3_982')
 dims=[tuple(map(F,v))for v in dimrow['FP_dimensions']];vectors={r['index']:(0,)+tuple(r['vector'])for r in profile['high_vectors']}
 orbitdims=[];limits=[]
 for orbit in profile['duality_orbits']:
  ds=[tuple(sum(d[k]*v for d,v in zip(dims,vectors[i]))for k in range(4))for i in orbit['indices']]
  need(len(set(ds))==1,'dual orbit dimensions')
  orbitdims.append(ds[0]);aa,b,c,e=ds[0];limits.append(12 if aa+b!=3*c else 24 if aa+2*b!=6*e else 0)
 types=bq.trace_types(4)[0];need(len(types)==system['phase_types']==34,'complete inherited phase indexing')
 one=next(i for i,t in enumerate(types)if t==tuple((F(1),F(0),F(0),F(0))for k in range(4)))
 finite,_=conductor_types(4)
 removed=[]
 for j,label in enumerate(system['labels']):
  if label[0]!='high_phase':continue
  _,oi,globaloi,ti=label;limit=limits[oi]
  if limit and (ti==one or (a.conductor and tuple(types[ti])not in finite[limit])):removed.append(j)
 keep=[j for j in range(len(system['columns']))if j not in set(removed)]
 J=System([{int(i):v for i,v in system['columns'][j].items()}for j in keep],system['rhs'])
 if a.spectral:
  capacities=spectral_capacities();cos=cosines24();fixed=[tuple(sum(d[k]*v for d,v in zip(dims,vec))for k in range(4))for vec in profile['low_columns']]
  def L(d):
   aa,b,c,e=d;return {12:3*c-aa-b,24:6*e-aa-2*b}
  rhs=list(J.rhs);cols=[dict(c)for c in J.columns]
  for (f,k),cap in capacities.items():
   ri=len(rhs);rhs.append(int(cap-sum(L(d)[f]**2 for d in fixed)if k==0 else cap))
   for local,globalj in enumerate(keep):
    label=system['labels'][globalj]
    if label[0]!='high_phase':continue
    _,oi,globaloi,ti=label;mask=L(orbitdims[oi])[f]
    if not mask:continue
    matches=[m for m in range(0,24,24//limits[oi])if tuple(cos[(m*j)%24]for j in range(1,5))==types[ti]]
    need(matches,'root bound covers retained phase')
    values={int(min((m*f//24)%f,(-m*f//24)%f)==k)for m in matches}
    need(len(values)==1,'unique conjugate fibre')
    coeff=int(mask**2*len(profile['duality_orbits'][oi]['indices'])*values.pop())
    if coeff:cols[local][ri]=coeff
  J=System(cols,rhs)
 path=HERE/('R982_spectral_mask.json'if a.spectral else'R982_conductor_mask.json'if a.conductor else'R982_dimension_mask.json')
 meta={'source_system_sha256':hashlib.sha256((OLD/'joint_phase_system.json').read_bytes()).hexdigest(),'removed_global_columns':removed,'rows':J.nrows,'variables':J.nvars,'saturated_conductor_support_applied':a.conductor,'all_conjugate_spectral_fibre_capacities_applied':a.spectral,'inherited_complete_low_frame':2,'inherited_indicator_branch':4,'equivalent_frame':3,'twist_order_bounds':limits}
 if a.write:
  prior=json.loads((OLD/'joint_phase_result.json').read_text())['certificate'];lookup={g:j for j,g in enumerate(keep)}
  if not a.spectral and all(j in lookup for j in prior['indices']):
   report={'status':'exact_feasible_relaxation','certificate':{'indices':[lookup[j]for j in prior['indices']],'weights':prior['weights']},'origin':'prior exact witness respects saturation mask'}
  else:
   rows=cg.active_rows(J,range(J.nvars));sol,diag=cg.phase_one(rows,J.rhs,J.nvars,120);report={'status':'no_exact_conclusion','numerical':diag}
   if sol.success and sol.fun<1e-7:
    cert=cg.exact_feasible(J,list(range(J.nvars)),J.rhs,sol.x[:J.nvars])
    if cert is not None:report.update(status='exact_feasible_relaxation',certificate=cert)
   if report['status']=='no_exact_conclusion':
    ray=cg.reuse_dual(rows,J.rhs,J.nvars,sol)
    if ray is not None:report.update(status='exact_infeasible_relaxation',certificate={'covector':ray})
  result={'metadata':meta,'decision':report,'scope':'Inherited whole-domain R982 joint phase relaxation with rigorous saturation support masks; no category model follows from feasibility.'}
 else:
  result=json.loads(path.read_text());need(result['metadata']==meta,'R982 mask matrix identity');report=result['decision']
 if report['status']=='exact_feasible_relaxation':
  total=[F(0)]*J.nrows;c=report['certificate'];need(len(c['indices'])==len(set(c['indices'])),'distinct primal support')
  for j,v in zip(c['indices'],c['weights']):
   v=F(v);need(v>=0,'nonnegative primal')
   for i,b in J.column(j).items():total[i]+=v*b
  need(total==J.rhs,'all exact R982 equations')
 elif report['status']=='exact_infeasible_relaxation':
  y=report['certificate']['covector'];need(all(sum(y[i]*v for i,v in c.items())>=0 for c in J.columns),'nonnegative dual columns');need(sum(v*b for v,b in zip(y,J.rhs))<0,'negative dual right side')
 else:raise ValueError('No exact certificate reconstructed')
 if a.write:path.write_text(json.dumps(result,indent=2)+'\n')
 print('PASS R982',len(removed),'removed',report['status'],flush=True)
if __name__=='__main__':main()
