#!/usr/bin/env python3
"""Exact short check of the two residual ring characters and center dimensions."""
import json
from pathlib import Path
import sympy as s
from r1154_rank10 import tensor,check
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
a=6+3*s.sqrt(5);D=540+240*s.sqrt(5)
rows=[]
for t in (0,1):
 N=tensor(1,1,t);d=check(N)['dual'];chars=[]
 for x,y in ((a,2*a+2),(s.conjugate(a).subs(s.sqrt(5),-s.sqrt(5)),None),(1,-1)):
  if y is None:y=2*x+2
  chars.append([1,1,1,1,x,x,x,x,y,y])
 for x,y in ((1,0),(-1,1),(-1,-4)):
  chars.append([1,1,-1,-1,x,x,-x,-x,y,-y])
 for v in (1,-1):
  for z in (1,-1):
   x=z*(1 if t==0 else s.I)
   chars.append([1,-1,v,-v,x,-x,v*x,-v*x,0,0])
 for c in chars:
  for i in range(10):
   for j in range(10):assert s.expand(c[i]*c[j]-sum(N[i][j][k]*c[k] for k in range(10)))==0
 assert len(set(map(str,chars)))==10
 fs=[s.simplify(sum(c[i]*c[d[i]] for i in range(10))) for c in chars]
 assert sum(f==8 for f in fs)==5
 rows.append({'t':t,'characters':[[str(z) for z in c] for c in chars],'formal_codegrees':[str(f) for f in fs],'nonreal_characters':sum(any(s.im(z)!=0 for z in c) for c in chars)})
p=ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json'
r=json.loads(p.read_text());dims=[1,a+1,a+1,1,a,a,a+1,a+1]
lo=[s.expand(sum(x*y for x,y in zip(c,dims))) for c in r['low_columns']]
hi=[s.expand(sum(x*y for x,y in zip([0]+c,dims))) for c in r['high_columns']]
for pid in (6971,8766,8772):
 actual=lo+[z for z,n in zip(hi,r['completions'][pid]) for _ in range(n)]
 assert sum(s.expand(z-D/4)==0 for z in actual)==5
 assert all(z not in actual for z in (15+6*s.sqrt(5),255+114*s.sqrt(5)))
for sig in (1,-1):
 assert s.simplify(2*D/(40+sig*16*s.sqrt(5))-(15+6*s.sqrt(5) if sig==1 else 255+114*s.sqrt(5)))==0
N=tensor(1,1,1)
def mul2(x,y):
 return [sum(x[i]*y[j]*N[i][j][k] for i in range(10) for j in range(10))%2 for k in range(10)]
y=[int(i==8) for i in range(10)]
y2=mul2(y,y);y3=mul2(y2,y);y4=mul2(y2,y2)
assert y2==[1,1,0,0,0,0,1,1,0,1]
assert y3==[0,0,1,1,1,1,0,0,1,0]
assert y4==y2
signs=[1,1,-1,-1,0,0,0,0,-1,1]
dimB=[1]*4+[a]*4+[2*a+2]*2
assert s.expand(sum(x*y for x,y in zip(signs,dimB)))==0
receipt={'second_indicators':signs,'total_second_indicator':0,'parity_y_squared':y2,'parity_y_cubed':y3,'parity_y_fourth_equals_y_squared':True,'result':'PASS exact arithmetic only','rings':rows,'source_center_pattern_ids':[6971,8766,8772],'source_dim_D_over4_count':5,'source_required_missing_dimensions':['15+6sqrt5','255+114sqrt5'],'categorical_status':'unresolved; two-ring arithmetic filter, further categorical duality argument leaves t=1 (u) only'}
(HERE/'r1154_character_check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: character tables, codegrees, and three-pattern dimension filter')
