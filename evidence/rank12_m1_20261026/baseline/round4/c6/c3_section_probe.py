#!/usr/bin/env python3
import itertools,json,sympy as s
from pathlib import Path
P=Path(__file__).resolve().parent;x=s.symbols('x');out=[]
for target,tbase in [('R561',0),('R628',3)]:
 for group in ['C18','C6xC3']:
  if group=='C18':
   els=list(range(18));add=lambda a,b:(a+b)%18;neg=lambda a:-a%18;pi=lambda a:a%6;lift=lambda a,b:a+6*b;t=0 if tbase==0 else 9;zero=0;conductor=18
   chars=list(range(18));char=lambda r,a:(r*a)%18
  else:
   els=list(itertools.product(range(6),range(3)));add=lambda a,b:((a[0]+b[0])%6,(a[1]+b[1])%3);neg=lambda a:(-a[0]%6,-a[1]%3);pi=lambda a:a[0];lift=lambda a,b:(a,b);t=(tbase,0);zero=(0,0);conductor=6
   chars=list(itertools.product(range(6),range(3)));char=lambda r,a:(r[0]*a[0]+2*r[1]*a[1])%6
  phi=s.Poly(s.cyclotomic_poly(conductor,x),x);choices=[]
  if tbase==0:
   for i,j in itertools.product(range(3),repeat=2):
    z=9 if group=='C18'else(3,0);u,v=lift(1,i),lift(2,j);choices.append([zero,z,u,neg(u),v,neg(v)])
  else:
   for cs in itertools.product(range(3),repeat=3):
    ss=[]
    for a,b in zip([0,1,4],cs):u=lift(a,b);ss.extend([u,add(t,neg(u))])
    choices.append(ss)
  for S in choices:
   subgroup=zero in S and all(add(a,b)in S for a in S for b in S);obs=None;checks=[]
   for r in chars:
    sigma=sum(x**char(r,a)for a in S);epsilon=x**((-char(r,t))%conductor)
    h=s.Poly(epsilon*sigma**2+4,x).rem(phi);norm=abs(int(s.resultant(phi.as_expr(),h.as_expr(),x)));bad=[int(p)for p in s.factorint(norm)if p not in[2,3,5]]
    checks.append({'character':r,'h_plus_four':list(map(str,h.all_coeffs())),'norm':norm})
    if bad:obs={'character':r,'h_plus_four':list(map(str,h.all_coeffs())),'norm':norm,'bad_prime':bad[0]};break
   out.append({'ring':target,'group':group,'section':S,'subgroup':subgroup,'excluded':obs is not None,'obstruction':obs,'checks':checks})
  rr=[r for r in out if r['ring']==target and r['group']==group]
  print(target,group,'total',len(rr),'survive',sum(not r['excluded']for r in rr),'non-subgroup survivors',sum(not r['excluded']and not r['subgroup']for r in rr),flush=True)
(P/'c3_section_probe.json').write_text(json.dumps(out,indent=2)+'\n')
