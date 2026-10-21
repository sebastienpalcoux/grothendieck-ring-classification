"""Bounded numerical discovery and exact SU3_7 family checks; no general exclusion."""
from pathlib import Path
import json,math,itertools,argparse
import sympy as s
HERE=Path(__file__).resolve().parent

def require(v,msg):
 if not v:raise ValueError(msg)
def classical_dimension(typ,r,k):
 if typ=='A':
  rho=[(r+2-2*i)/2 for i in range(1,r+2)];dots=[rho[i]-rho[j]for i in range(r+1)for j in range(i+1,r+1)];h,index=r+1,r+1
 elif typ=='B':
  rho=[r-i-.5 for i in range(r)];dots=[rho[i]+t*rho[j]for i in range(r)for j in range(i+1,r)for t in[-1,1]]+rho;h,index=2*r-1,4
 elif typ=='C':
  rho=[r-i for i in range(r)];dots=[(rho[i]+t*rho[j])/2 for i in range(r)for j in range(i+1,r)for t in[-1,1]]+rho;h,index=r+1,2**r
 else:
  rho=[r-i-1 for i in range(r)];dots=[rho[i]+t*rho[j]for i in range(r)for j in range(i+1,r)for t in[-1,1]];h,index=2*r-2,4
 return math.exp(math.log(index)+r*math.log(k+h)-2*sum(math.log(2*math.sin(math.pi*x/(k+h)))for x in dots))
def audit():
 quartic=144+96*math.sqrt(2)+80*math.sqrt(3)+56*math.sqrt(6);ratios=[.125,.25,.5,1,2,3,4,6,8,9,12,16,24,32];matches=[];dimensions=[]
 for typ in 'ABCD':
  for r in range(1 if typ=='A'else 2 if typ in'BC'else 4,13):
   for k in range(1,36):
    d=classical_dimension(typ,r,k);dimensions.append((typ,r,k,d))
    for q in ratios:
     if abs(d/quartic-q)<1e-7:matches.append([typ,r,k,q])
 require(not matches,'unexpected quartic discovery lead')
 profiles=json.loads((HERE.parent/'pipeline/survivor_profiles.json').read_text());per_ring=[]
 for row in profiles:
  target=row.get('global_dimension_approx',row.get('FP_global_dimension_approximate'));leads=[]
  for typ,r,k,value in dimensions:
   for ratio in ratios:
    if abs(value/target-ratio)<1e-7:leads.append(dict(type=typ,rank=r,level=k,dimension_ratio=ratio))
  per_ring.append(dict(id=row['id'],target_dimension_approximate=round(target,10),matches=leads))
 u=s.pi/10;weights=[(a,b)for a in range(8)for b in range(8-a)];adj=[(a,b)for a,b in weights if(a+2*b)%3==0]
 dims=[s.sin((a+1)*u)*s.sin((b+1)*u)*s.sin((a+b+2)*u)/(s.sin(u)**2*s.sin(2*u))for a,b in adj];D=s.simplify(sum(x*x for x in dims));require(D==250+110*s.sqrt(5),'exact SU3_7 adjoint dimension')
 shifted=[(a+1,b+1)for a,b in weights];units=[l for l in range(1,10)if math.gcd(l,10)==1]
 vacuum=[(a,b)for a,b in shifted if(a*a+a*b+b*b-3)%30==0 and all(((l*a)%10+(l*b)%10<10)==(l<5)for l in units)];require(vacuum==[(1,1)],'vacuum coupling')
 return dict(scope='Model-family investigation only; no general fusion-categorification exclusion.',all_baseline_numerical_scan=dict(tested_classical_models=len(dimensions),dimension_ratios=ratios,tolerance=1e-7,per_ring=per_ring,status='heuristic dimension-ratio leads only; neither tensor matches nor exclusions'),quartic_numerical_scan=dict(target_dimension_expression='144+96sqrt(2)+80sqrt(3)+56sqrt(6)',target_dimension_approximate=round(quartic,12),types='A1–A12,B2–B12,C2–C12,D4–D12',levels=[1,35],tested=len(dimensions),dimension_ratios=ratios,tolerance=1e-7,matches=matches,status='heuristic negative search; not an exact family-exclusion certificate'),su3_7=dict(full_rank=len(weights),adjoint_rank=len(adj),adjoint_weights=[list(x)for x in adj],adjoint_dimension=str(D),vacuum_coupling_candidates=[list(x)for x in vacuum],unitary_Morita_dual_rank=12,excluded_model_family_for=['R8_3_65','R8_3_1453'],proof='evidence/rank8_m3_20261021/models/QUANTUM_MODEL_SEARCH.md'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();out=audit();f=HERE/'quantum_model_attempts.json'
 if a.write:f.write_text(json.dumps(out,indent=2)+'\n')
 else:require(out==json.loads(f.read_text()),'saved quantum audit mismatch')
 print('PASS: bounded numerical search and exact SU3_7 follow-up freshly replayed.')
