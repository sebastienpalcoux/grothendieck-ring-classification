"""Complete five Gram branches forced by the saturated quadratic37 sector."""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'evidence/rank8_research_20261022/pointed_followup'))
import c2_fibres as f
class FiniteFibresCone(f.PointedCone):
 def __init__(self,base,j):
  super().__init__(base,-1);f.require(j in range(5),'five complete branches')
  self.j=j;self.u=16-4*j
  t=[(-Q(1,36),-Q(l,36))for l in [1,-1,1,1]]
  ti=self.types.index(t)
  vectors=[(0,0,0,1,0,1,1),(0,1,1,0,1,0,0),(0,1,1,1,1,1,1)]
  indices=[]
  for v in vectors:
   hi=next(i for i,(w,z)in enumerate(self.a['high'])if tuple(w)==v)
   orb=next(i for i,m in enumerate(self.orbits)if hi in m)
   f.require(len(self.orbits[orb])==1,'selfdual singletonorbit')
   indices.append(self.offset+orb*self.nt+ti)
  weights=[9*self.u,9*self.u,18*j]
  self.fixed=[sum(w*self.column(c).get(i,0)for c,w in zip(indices,weights))for i in range(self.nrows)]
  for orb,members in enumerate(self.orbits):
   if any(6*self.a['high'][i][1][0]!=37*self.a['high'][i][1][1]for i in members):
    self.allowed.difference_update(self.offset+orb*self.nt+t for t in range(self.nt))
  self.meta={**self.meta,'prime':37,'nonsquare_trace_index':ti,'finite_fibre_branch':j,'u':self.u,'fixed_column_indices':indices,'fixed_column_weights':weights,'fixed_contribution_sha256':f.st.digest(self.fixed),'allowed_columns':len(self.allowed),'allowed_domain_sha256':f.st.digest(sorted(self.allowed))}
 def rhs_for(self,ep):return [a-b for a,b in zip(super().rhs_for(ep),self.fixed)]

def run(seconds,verify=False,setup=None):
 source,base,old=f.setup(1768)if setup is None else setup;path=HERE/'finite_fibres_cone.json'
 eligible=[list(ep)for ep in f.st.old.ht.indicator_choices(base.R)if ep[0]==-1]
 if verify:
  out=json.loads(path.read_text());f.require(out['tensor_sha256']==source['tensor_sha256'],'tensor')
  f.require([r['j']for r in out['fibres']]==list(range(5)),'all five branches')
  checked=0
  for r in out['fibres']:
   C=FiniteFibresCone(base,r['j']);f.require(f.st.encode(C.meta)==r['metadata'],'domainmetadata');seen=[]
   rays=set()
   for b in r['branches']:
    ep=b['indicators'];f.require(ep in eligible and ep not in seen,'eligiblebranch');seen.append(ep)
    cert=b['certificate']
    if b['status']=='exact_feasible':C.check_feasible(cert['indices'],cert['weights'],ep)
    else:
     f.require(b['status']=='exact_infeasible','status');key=tuple(cert['y'])
     if key not in rays:f.require(C.oracle(cert['y'],1)['negative_columns']==0,'oracle');rays.add(key)
     value=sum(a*b for a,b in zip(cert['y'],C.rhs_for(ep)));f.require(value==cert['bTy']and value<0,'rhs')
    checked+=1
   if r['status']=='all_indicators_exact_infeasible':f.require(sorted(seen)==sorted(eligible),'completeindicatorcoverage')
   elif r['status']=='necessary_relaxation_survives':f.require(any(b['status']=='exact_feasible'for b in r['branches']),'survivalwitness')
   else:f.require(False,'inconclusivefibrenoacceptance')
  f.require(checked==40,'all forty fibre/indicator branches')
  rejected=[(r['j'],b['indicators'])for r in out['fibres']for b in r['branches']if b['status']=='exact_infeasible']
  survivors=[(r['j'],b['indicators'])for r in out['fibres']for b in r['branches']if b['status']=='exact_feasible']
  f.require(len(rejected)==39 and survivors==[(4,[-1,1,1,1,1,1,1])],'claimed unique necessary branch')
  f.require(out['status']=='no_complete_exclusion','saved final status')
  print('PASS',checked,'exact branch checks: 39 rejected, one survives',flush=True);return {'checked':checked,'rejected':len(rejected),'survivors':survivors}
 out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'scope':'necessary pseudo-unitary five integer primitive37 Gram branches; requires saturated conductor and modular Galois proofs','fibres':[]}
 def save():path.write_text(json.dumps(f.st.encode(out),separators=(',',':'))+'\n')
 shared=[]
 for j in range(5):
  C=FiniteFibresCone(base,j);r={'j':j,'metadata':C.meta,'branches':[]};out['fibres'].append(r);save()
  active=C.initial_columns();rays=shared
  print('FIBRE',j,'allowed',len(C.allowed),flush=True)
  for ep in eligible:
   b={'indicators':ep};r['branches'].append(b)
   reuse=next((y for y in rays if sum(a*z for a,z in zip(y,C.rhs_for(ep)))<0),None)
   if reuse is not None:
    value=C.check_farkas(reuse,ep);b.update(status='exact_infeasible',certificate={'y':reuse,'bTy':value},reused=True);save();continue
   # Any negative Gram right-hand-side is already an exact separator.
   neg=next((i for i,z in enumerate(C.rhs_for(ep))if C.rows[i][0]=='gram'and z<0),None)
   if neg is not None:
    y=[int(i==neg)for i in range(C.nrows)];value=C.check_farkas(y,ep);rays.append(y);b.update(status='exact_infeasible',certificate={'y':y,'bTy':value});save();continue
   def progress(it):b['iterations']=it;save();print('ROUND',j,ep,it[-1]['outcome'],flush=True)
   cert,feas,active,it=f.cg.solve_case(C,ep,active,512,seconds,progress)
   if cert:b.update(status='exact_infeasible',certificate=cert);rays.append(cert['y'])
   elif feas:b.update(status='exact_feasible',certificate=feas);r['status']='necessary_relaxation_survives';save();break
   else:b['status']='inconclusive';r['status']='inconclusive';save();break
   save()
  else:r['status']='all_indicators_exact_infeasible';save()
 out['status']='all_fibres_exact_infeasible'if all(r['status']=='all_indicators_exact_infeasible'for r in out['fibres'])else'no_complete_exclusion';save()
 print(out['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=180);p.add_argument('--verify',action='store_true');a=p.parse_args();run(a.seconds,a.verify)
