"""Independent S3 representation-category control for cyclic-root equations."""
import json,time
from fractions import Fraction
from pathlib import Path
import sympy as s
import rotation48 as T
from exact import field,require
R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,1]]]
C=field(s.Poly(s.cyclotomic_poly(48,s.Symbol('t')),s.Symbol('t')));d=dict(C=C,DD=C(6),F=48,dims=list(map(C,[1,1,2])));cols=[(1,0,0),(1,0,1),(1,1,0)];labels=[((1,0),0),((0,1),0),((1,1),24),((0,1),16),((0,1),32)];start=time.monotonic();rows,rhs,nv,md=T.append_rows(R,d,cols,labels,5,root_powers=(0,1));x=[1]*5
for block in md['blocks']:
 obj=block['object'];n=block['order'];e=block['root_power'];char=[1,-1,1]if obj==1 else[2,0,-1];traces=[]
 for r in range(n):
  if r==0:trace=sum(size*value**n for size,value in zip([1,3,2],char))//6
  else:
   g=__import__('math').gcd(n,r);m=n//g;values=[char[0],char[0]if m%2==0 else char[1],char[0]if m%3==0 else char[2]];trace=sum(size*value**g for size,value in zip([1,3,2],values))//6
  traces.append(trace)
 value=sum((C(z)*C.unit**((-e*r*(48//n))%48)for r,z in enumerate(traces)),C.zero)/C(n);co=value.to_list();require(len(co)<=1 and (not co or co[0].denominator==1) and (not co or co[0]>=0),'control multiplicity not nonnegative integer');x.append(int(co[0])if co else 0)
require(len(x)==nv and all(sum(a*x[j]for j,a in row.items())==b for row,b in zip(rows,rhs)),'cyclic rotation equation control fails');out=dict(passed=True,optimizer_used=False,model='Rep(S3), eight actual center simples',orders=md['orders'],root_powers=md['root_powers'],variables=nv,equations=len(rows),seconds=time.monotonic()-start);Path(__file__).with_name('rotation_control.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
