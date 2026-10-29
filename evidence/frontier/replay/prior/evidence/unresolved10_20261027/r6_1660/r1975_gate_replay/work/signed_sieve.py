"""Unrestricted oriented sphericalization, reusing the project's signed bounds.

No Frobenius--Schur or commutativity normalization is imposed. Dual-compatible
basis signs are the only gauges. The finite associativity problem is encoded
over eight-bit vectors: every unreduced equation has absolute value <=72, so
zero modulo 256 is equivalent to zero over the integers.
"""
from common import *
from scalar_characters import chars
from sphere import char_obstruction
from arithmetic import dnumber
from exact import pc
import z3,itertools,collections,time
def problem(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 def orbit(t):
  a,b,c=t;u=(du[c],du[b],du[a]);return {t,(b,c,a),(c,a,b),u,(u[1],u[2],u[0]),(u[2],u[0],u[1])}
 todo=set(itertools.product(range(1,n),repeat=3));active=[];mapping={};bounds=[]
 while todo:
  tri=min(todo);o=orbit(tri);todo-=o;a,b,c=tri;bound=R[a][b][du[c]]
  assert all(R[i][j][du[k]]==bound for i,j,k in o)
  if not bound:continue
  v=len(active);active.append(sorted(o));bounds.append(bound)
  for i,j,k in o:mapping[i,j,du[k]]=v
 def ent(i,j,k):
  if not R[i][j][k]:return None
  if 0 in (i,j,k):return -1
  return mapping[i,j,k]
 eqs=set()
 for i,j,k,l in itertools.product(range(n),repeat=4):
  row=collections.Counter()
  for h in range(n):
   for sign,a,b in [(1,ent(i,j,h),ent(h,k,l)),(-1,ent(j,k,h),ent(i,h,l))]:
    if a is None or b is None:continue
    if a==b and a>=0 and bounds[a]==1:a=b=-1
    row[tuple(sorted((a,b)))]+=sign
  row={k:v for k,v in row.items() if v}
  if row:
   terms=tuple(sorted(row.items()))
   if terms[0][1]<0:terms=tuple((k,-v) for k,v in terms)
   eqs.add(terms)
 dualorbits=[];seen={0}
 for i in range(1,n):
  if i not in seen:dualorbits.append({i,du[i]});seen|=dualorbits[-1]
 piv={};gauge=[]
 for v in sorted(range(len(active)),key=lambda v:(bounds[v]%2==0,v)):
  tri=active[v][0];mask=sum((sum(i in o for i in tri)%2)<<j for j,o in enumerate(dualorbits));r=mask
  for p in sorted(piv,reverse=True):
   if r>>p&1:r^=piv[p]
  if r:piv[r.bit_length()-1]=r;gauge.append(v)
 solver=z3.SolverFor('QF_BV');solver.set(timeout=10000)
 vs=[z3.BitVec(f'v{i}',8) for i in range(len(active))]
 for i,v in enumerate(vs):
  vals=list(range(-bounds[i],bounds[i]+1,2))
  if i in gauge:vals=[x for x in vals if x>=0]
  solver.add(z3.Or(*(v==x for x in vals)))
 for eq in sorted(eqs):
  terms=[]
  for (a,b),co in eq:
   aa=1 if a==-1 else vs[a];bb=1 if b==-1 else vs[b];terms.append(co*aa*bb)
  solver.add(sum(terms)==0)
 return solver,vs,active,mapping,bounds,gauge,len(eqs)
def tensor(R,mapping,values):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 T=[[[int(j==k) if i==0 else int(i==k) if j==0 else int(du[i]==j) if k==0 else 0 for k in range(n)] for j in range(n)]for i in range(n)]
 for (i,j,k),v in mapping.items():T[i][j][k]=values[v]
 A=np.asarray(T,dtype=np.int64)
 assert np.array_equal(np.einsum('ijx,xkl->ijkl',A,A),np.einsum('jkx,ixl->ijkl',A,A))
 return T
def original_gauge(R,T):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 for tail in itertools.product((-1,1),repeat=n-1):
  s=(1,)+tail
  if any(s[i]!=s[du[i]] for i in range(n)):continue
  if all(T[i][j][k]==s[i]*s[j]*s[k]*R[i][j][k] for i,j,k in itertools.product(range(n),repeat=3)):return s
def discover(R,spherical_report,max_seconds=40,max_branches=256):
 start=time.time();src=chars(R);sol,vs,active,mapping,bounds,gauge,eqcount=problem(R);branches=[]
 while time.time()-start<max_seconds and len(branches)<max_branches:
  result=sol.check()
  if result==z3.unsat:return {'outcome':'excluded','complete':True,'variables':len(vs),'equations':eqcount,'gauge_coordinates':gauge,'branches':branches,'seconds':time.time()-start}
  if result!=z3.sat:return {'outcome':'no_conclusion','reason':str(result),'complete':False,'branches':branches,'seconds':time.time()-start}
  M=sol.model();values=[M.eval(v,model_completion=True).as_long() for v in vs];values=[x-256 if x>=128 else x for x in values]
  T=tensor(R,mapping,values);s=original_gauge(R,T)
  if s is not None:
   why={'kind':'original_gauge','signs':s,'spherical_report':spherical_report}
   assert spherical_report['spherical_excluded']
  else:
   why=dnumber(T)
   if why is None:
    a=chars(T);cb=[]
    for f,m in a.components:cb.append({'factor':pc(f),'obstruction':char_obstruction(a,f,list(src.cf)+list(a.cf))})
    if any(b['obstruction'] is None for b in cb):return {'outcome':'no_conclusion','reason':'a signed character survives the established necessary conditions','complete':False,'branches':branches,'surviving_values':values,'surviving_characters':cb,'seconds':time.time()-start}
    why={'kind':'all_signed_scalar_characters_excluded','characters':cb}
  branches.append({'values':values,'obstruction':why});sol.add(z3.Or(*(v!=x for v,x in zip(vs,values))))
 return {'outcome':'no_conclusion','reason':'finite discovery allowance exhausted','complete':False,'branches':branches,'seconds':time.time()-start}
def main():
 rows={r['id']:r for r in read()};out=load('signed_sieve.json') if (BASE/'work/signed_sieve.json').exists() else [];done={r['id']for r in out};start=time.time();pre={r['id']:r for r in load('sphere_original.json')};old={r['id'] for r in load('remaining_arithmetic.json') if r['certificate']}
 for rid,r in pre.items():
  if rid in done or rid in old or not r['report'].get('spherical_excluded'):continue
  report=discover(rows[rid]['tensor'],r['report']);out.append({'id':rid,'report':report});save('signed_sieve.json',out)
  print(rid,report['outcome'],'branches',len(report['branches']),'seconds',round(report['seconds'],2),'TOTAL',len(out),sum(x['report']['outcome']=='excluded' for x in out),flush=True)
 print('FINAL',len(out),sum(x['report']['outcome']=='excluded' for x in out),'seconds',time.time()-start,flush=True)
if __name__=='__main__':main()
