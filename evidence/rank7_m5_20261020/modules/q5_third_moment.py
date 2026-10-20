"""Exact q5 three-moment hull; exploratory source-bound LP separators."""
import json,itertools,math,sys,time,functools,argparse
from fractions import Fraction as F
from pathlib import Path
import sympy as s
HERE=Path(__file__).parent;P=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_center_trace as q
base=q.base

def hull():
 x=s.Symbol('x');mod=s.Poly(s.cyclotomic_poly(180,x),x);deg=mod.degree()
 def coeff(p):return tuple(F(p.nth(i)) for i in range(deg))
 powers=[coeff(s.rem(s.Poly(x**k,x),mod)) for k in range(180)]
 sq=tuple(F(int(i==0))+2*powers[36][i]+2*powers[144][i] for i in range(deg))
 units=[r for r in range(180) if math.gcd(r,180)==1 and r%5 in [1,4]];assert len(units)==24
 index=next(i for i in range(1,deg) if sq[i]);phases=set()
 for e in range(180):
  vals=[]
  for j in [1,2,3]:
   vec=tuple(sum(powers[(e*j*r)%180][i] for r in units)/24 for i in range(deg));b=vec[index]/sq[index];a=vec[0]-b*sq[0]
   assert all(vec[i]==a*int(i==0)+b*sq[i] for i in range(deg))
   vals.extend([a,b])
  phases.add(tuple(vals))
 endpoints=phases|{tuple(-v/6 for v in p) for p in phases}
 scaled=sorted({tuple(int(48*v) for v in p) for p in endpoints})
 assert all(F(z,48)==v for p in endpoints for z,v in zip([int(48*v) for v in p],p))
 out={'conductor':180,'relative_degree':24,'base_phase_count':len(phases),'endpoint_count':len(endpoints),'scale':48,'phases':scaled}
 (HERE/'q5_third_hull.json').write_text(json.dumps(out,indent=2)+'\n')
 return scaled

def columns(orbits,phases,dual,multiplicities,D):
 dorbits=[];seen=set()
 for i in range(1,7):
  if i not in seen:
   orb=sorted({i,dual[i]});seen.update(orb);dorbits.append(orb)
 n=57+len(dorbits);cols=[]
 for orbit in orbits:
  gram=[sum(row[1][j] for row in orbit) for j in range(21)]
  for ph in phases:
   col=[48*x for x in gram]
   for degree in range(3):
    vals=[base.mul(row[2],ph[2*degree:2*degree+2],5) for row in orbit]
    col.extend(sum(row[0][i]*v[k] for row,v in zip(orbit,vals)) for i in range(6) for k in range(2))
   cols.append(col+[0]*len(dorbits))
 for oi,orb in enumerate(dorbits):
  lower=-F(multiplicities[orb[0]],2);upper=multiplicities[orb[0]];span=upper-lower
  t=[0]*n;u=[0]*n;t[57+oi]=u[57+oi]=48
  for i in orb:
   assert multiplicities[i]==multiplicities[orb[0]]
   for k in range(2):t[45+2*(i-1)+k]=int(-48*D[k]*span)
  cols.extend([t,u])
 return cols,dorbits

def main(rid):
 start=time.monotonic();phases=hull();print('hull endpoints',len(phases),flush=True)
 N=next(row['tensor'] for row in json.load(open(P/'supplements/rank7/output/m5/census.json')) if row['id']==rid)
 d,D,B,zs,T,signs=q.source_data(N,rid);lows,nodes,forced=q.enumerate_low(B,d,zs,T)
 rows=q.global_rows(B,d);print('rows ready',len(rows),'seconds',time.monotonic()-start,flush=True)
 dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)];multiplicities=[N[i][i][dual[i]] for i in range(7)]
 selected={'R7_5_3895':[6,8],'R7_5_5039':[3,5]}[rid];reports=[]
 baseline=json.load(open(HERE.parent/'criteria'/(rid+'_q5_two_orbit_baseline.json')))
 lows=[tuple(tuple(v) for v in branch['low']) for branch in baseline['branches']]
 from tensor_rotation import farkas
 for ix in selected:
  low=lows[ix];R,bound,orbits,rank=q.compatible_orbits(rows,B,low,T);cols,dorbits=columns(orbits,phases,dual,multiplicities,D)
  known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
  for sign in signs:
   rhs=[48*x for x in bound]+[-48*x for z in known for x in z]+[48*(D[k]*sign[i+1]-known[i][k]) for i in range(6) for k in range(2)]
   rhs += [int(48*(-D[k]*F(multiplicities[i+1],2)-known[i][k])) for i in range(6) for k in range(2)]+[48]*len(dorbits)
   print('LP',ix,sign,'orbits',len(orbits),'columns',len(cols),'rows',len(rhs),flush=True)
   A=[list(row) for row in zip(*cols)];y=farkas(A,rhs)
   if y is not None:
    assert base.dot(rhs,y)<0 and all(base.dot(c,y)>=0 for c in cols)
   report={'low_index':ix,'low':low,'sign':sign,'row_orbits':len(orbits),'columns':len(cols),'separator':y,'excluded':y is not None}
   if y is None:
    import numpy as np
    from scipy.optimize import milp,LinearConstraint,Bounds
    from scipy.sparse import csc_matrix
    AA=np.array(A,dtype=float);rr=np.array(rhs,dtype=float);integrality=np.zeros(len(cols),dtype=int)
    for oi,orb in enumerate(dorbits):
     ci=len(cols)-2*len(dorbits)+2*oi;mm=multiplicities[orb[0]];AA[45:57,ci]/=mm;rr[57+oi]*=mm;integrality[ci]=1
    result=milp(np.zeros(len(cols)),integrality=integrality,bounds=Bounds(0,np.inf),constraints=LinearConstraint(csc_matrix(AA),rr,rr),options={'time_limit':60})
    report['integer_rotation_status']=int(result.status);report['integer_rotation_message']=result.message
    if result.x is not None:report['integer_rotation_multiplicities']=[float(result.x[len(cols)-2*len(dorbits)+2*oi]) for oi in range(len(dorbits))]
    print('integer rotation',ix,result.message,report.get('integer_rotation_multiplicities'),flush=True)
   reports.append(report)
   print('result',ix,'excluded',y is not None,'seconds',time.monotonic()-start,flush=True)
 (HERE/(rid+'_third_moment.json')).write_text(json.dumps({'id':rid,'dimension':D,'nu3_rotation_multiplicities':multiplicities,'results':reports,'seconds':time.monotonic()-start},indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ring',choices=['R7_5_3895','R7_5_5039']);a=p.parse_args();main(a.ring)
