#!/usr/bin/env python3
"""Bounded exact modular indicators and cyclic spectra for orders1 through10."""
from pathlib import Path
from math import gcd
import hashlib,json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'rank10_case189/metric_modular_completion.py'
raw=SOURCE.read_text();s={'__file__':str(SOURCE)}
exec(compile(raw.split('\nresults=[]',1)[0],str(SOURCE),'exec'),s)
cv,mul,add,total,conj,enc=[s[n] for n in ['cv','mul','add','total','conj','enc']]
Q=s['Q'];zp=s['zp'];zero=cv(0)
def power(x,n):
 out=cv(1)
 for _ in range(n):out=mul(out,x)
 return out
def gal(x,a):return total(mul(x[j],zp[j*a%5]) for j in range(4))
S,T,dual,dims=s['build'](1,2,1)
p=SOURCE.with_name('metric_candidate_q1_c2.json');candidate=json.loads(p.read_text());N=candidate['fusion_tensor']
assert candidate['S']==[[enc(x) for x in row] for row in S]
assert candidate['theta']==[enc(x) for x in T]
D=total(mul(x,x) for x in dims);Dinv=mul(S[0][0],S[0][0]);assert mul(D,Dinv)==cv(1)
# Direct Ng-Schauenburg double sum; all arithmetic is inQ(zeta5).
nu={}
for n in range(1,11):
 phase=[power(x,n) for x in T]
 weights=[[mul(mul(mul(dims[i],dims[j]),phase[i]),conj(phase[j])) for j in range(14)] for i in range(14)]
 nu[n]=[mul(Dinv,total(mul(N[i][j][k],weights[i][j]) for i in range(14) for j in range(14))) for k in range(14)]
assert nu[1]==[cv(int(i==0)) for i in range(14)]
assert all(v in [cv(-1),cv(1)] if dual[i]==i else v==zero for i,v in enumerate(nu[2]))
assert nu[10]==dims
# Tensor powers, including the empty power, using independently exportedN.
powers=[]
for x in range(14):
 row=[[int(k==0) for k in range(14)]]
 for r in range(1,11):row.append([sum(row[-1][i]*N[i][x][k] for i in range(14)) for k in range(14)])
 powers.append(row)
def trace_block(x,n,r):return total(mul(powers[x][r][i],nu[n//r][i]) for i in range(14))
def mobius(n):
 ans=1;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;ans=-ans
   if n%p==0:return 0
   while n%p==0:n//=p
  p+=1
 return -ans if n>1 else ans
def ramanujan(q,e):return sum(d*mobius(q//d) for d in range(1,q+1) if q%d==0 and e%d==0)
records=[];viol=[]
for n in range(1,11):
 for x in range(14):
  h=powers[x][n][0]
  if n in [5,10]:
   omega=zp[1] if n==5 else s['neg'](zp[3])
   traces=[cv(h)]
   for k in range(1,n):
    r=gcd(n,k);v=trace_block(x,n,r)
    traces.append(gal(v,k//r))
   mult=[mul(Q(1,n),total(mul(traces[k],power(omega,(-e*k)%n)) for k in range(n))) for e in range(n)]
  else:
   vals={r:trace_block(x,n,r) for r in range(1,n+1) if n%r==0}
   assert all(v==cv(v[0]) for v in vals.values()),('nonrational trace outside5-conductor',n,x,vals)
   mult=[cv(sum(vals[r][0]*ramanujan(n//r,e) for r in vals)/n) for e in range(n)]
  bad=[e for e,v in enumerate(mult) if v!=cv(v[0]) or v[0].denominator!=1 or v[0]<0]
  assert total(mult)==cv(h)
  if bad:viol.append({'order':n,'simple':x,'bad_eigenvalue_exponents':bad})
  records.append({'order':n,'simple':x,'unit_multiplicity_in_power':h,'rotation_eigenvalue_multiplicities':[str(v[0]) if v==cv(v[0]) else enc(v) for v in mult],'pass':not bad})
out={'status':'PASS' if not viol else 'FAIL','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parameters':[1,2,1],'field':'Q(zeta5), basis1,zeta5,zeta5^2,zeta5^3','basis':candidate['basis'],'orders':list(range(1,11)),'indicators':{str(n):[enc(x) for x in nu[n]] for n in nu},'nu1_correct':True,'nu2_correct':True,'nu10_equals_dimensions':True,'rotation_checks':140,'rotation_spectra':records,'violations':viol,'scope':'Bounded necessary checks through order10. No associators, categorification or original-ring model constructed.'}
(HERE/'metric_c5_higher_indicator_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['indicators','rotation_spectra']},indent=2))
for n in range(1,11):print('nu'+str(n),[str(x[0]) if x==cv(x[0]) else enc(x) for x in nu[n]])
