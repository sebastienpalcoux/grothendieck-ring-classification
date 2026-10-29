import itertools,collections
def data(R):
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
 return active,mapping,bounds,gauge,eqs,du,dualorbits
