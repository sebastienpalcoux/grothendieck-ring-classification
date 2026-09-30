"""Actual mu48 necessary center equations after saturated Ising support.

All phases are actual roots in Q(zeta48), not normalized projected traces.
The individual Ising root masses are D*d_sigma/4.
"""
import sys,json,math,itertools,time
from pathlib import Path
from collections import Counter,defaultdict
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as M
import round5_1660 as T
from round4_m8_ising import ising_labels
from dimension_block_support import restriction_order_bounds
from exact import require,evaluate
from modular_character_induction import rational_rows

def prepare(R,height=6):
 d=M.data_for(R,height,48);C=d['C'];d['phases']=[tuple(C.unit**(a*k)for k in range(1,height+1))for a in range(48)];d['ising_labels']=ising_labels(R);d['actual48_domains']={};return d

def domain(R,d,low):
 if low in d['actual48_domains']:return d['actual48_domains'][low]
 cols=d['lows'][low];G,V,sp,_,_,bounds=T.domain(d,cols,R);support=restriction_order_bounds(d,[(0,)+v for v in V]);C=d['C'];allowed=[];metadata=[]
 for v,B,rec in zip(V,bounds,support['columns']):
  m=rec['order_bound'];bad=False;why=[];vv=(0,)+v;dvK=sum((d['K'](vv[i])*d['ds'][i]for i in range(len(R))),d['K'].zero)
  for g,ss in d['ising_labels']:
   if v[g-1] and v[ss-1]:bad=True;why.append('mixed_Ising_projection')
   if v[g-1]:m=math.gcd(m,2)if m else 2
   if v[ss-1]:
    m=math.gcd(m,16)if m else 16
    if d['embedding'].sign(d['D']*d['ds'][ss]/d['K'](4)-d['K'](v[ss-1])*dvK)<0:bad=True;why.append('single_object_exceeds_actual_Ising_root_mass')
  require(m>0 and 48%m==0,'unproved actual twist exponent cutoff')
  if not bad:allowed.append((v,B,m))
  metadata.append(dict(column=list(vv),order_bound=m,excluded=bad,reasons=why))
 result=(G,allowed,sp,metadata,support);d['actual48_domains'][low]=result;return result

def build(R,d,low,lab,ep):
 cols=d['lows'][low];C=d['C'];D=d['DD'];dims=d['dims'];tab=d['tab'];height=d['height'];ph=d['phases'];n=len(R);G,allowed,sp,md,support=domain(R,d,low);labels=[];bound_by_v={v:B for v,B,m in allowed};ising_exponents={}
 for g,ss in d['ising_labels']:
  aa=[a for a in range(48)if math.gcd(a,48)==3 and C.unit**(2*a)+C.unit**(-2*a)==C(ep[ss-1])*dims[ss]];require(len(aa)==4,'wrong actual Ising root domain');ising_exponents[ss]=aa
 for v,B,m in allowed:
  for a in range(48):
   if(a*m)%48:continue
   if any((v[g-1]and a!=24)or(v[ss-1]and a not in ising_exponents[ss])for g,ss in d['ising_labels']):continue
   labels.append((v,a))
 nh=len(labels);nv=nh;A=[];b=[];zv={v:sum((C(v[i])*dims[i+1]for i in range(n-1)),C.zero)for v,B,m in allowed};lowmass=[sum((C(sum(v[i]*v[j]for v in cols))*dims[j]for j in range(n)),C.zero)for i in range(n)]
 def add(co,rhs):
  for row,val in rational_rows(co,rhs,C):
   if any(row)or val:A.append(row);b.append(val)
 def add_int(row,rhs):
  if any(row)or rhs:A.append(row);b.append(int(rhs))
 def extend(k):
  nonlocal nv
  old=nv;nv+=k
  for row in A:row.extend([0]*k)
  return old
 for i in range(n-1):
  for j in range(i,n-1):add_int([v[i]*v[j]for v,a in labels],int(G[i,j]))
 for obj in range(1,n):
  for power,target in((1,0),(2,ep[obj-1])):add([C(v[obj-1])*zv[v]*ph[a][power-1]for v,a in labels],C(target)*D-lowmass[obj])
 # Exact projected cyclic rotation spectra; whenever the order divides48 these
 # are actual cyclic eigenvalues in the retained field.
 for obj in range(1,n):
  powers=[[1]+[0]*(n-1)]
  for k in range(height):powers.append([sum(powers[-1][i]*R[i][obj][j]for i in range(n))for j in range(n)])
  for order in range(3,height+1):
   rs=[r for r in range(1,order)if order%r==0];rt=sorted({tuple(M.relative_root(C,48,order,a*r)for r in rs)for a in range(order)},key=str);old=extend(len(rt));add([C.zero]*old+[C.one]*len(rt),C(powers[order][0]))
   for j,r in enumerate(rs):
    k=order//r;constant=sum((C(powers[r][i])*lowmass[i]for i in range(n)),C.zero);co=[-C(sum(powers[r][i]*v[i-1]for i in range(1,n)))*zv[v]*ph[a][k-1]for v,a in labels]+[C.zero]*(old-nh)+[D*t[j]for t in rt];add(co,constant)
 # Galois acts on spectral data by sigma and on actual twists by sigma^2.
 rows,rhs=M.coupled_balance(d,sp,cols,labels,nv)
 for row,val in zip(rows,rhs):add_int(row,val)
 tuples=dict(zip(sp.vectors,sp.types));sigs={v:(tab.dims[v]**2/tab.D**2,)+t for v,t in tuples.items()};lows=Counter((sigs[v],0)for v in cols);pos=defaultdict(list)
 for j,(v,a)in enumerate(labels):pos[sigs[(0,)+v],a].append(j)
 allpairs=set(pos)|set(lows);seen=set()
 for sigma in range(48):
  if math.gcd(sigma,48)>1:continue
  for sig,a in sorted(allpairs,key=str):
   sig1=tuple(evaluate(z.to_list(),C.unit**sigma,C)for z in sig);a1=a*sigma*sigma%48;pair=tuple(sorted(((str(sig),a),(str(sig1),a1))))
   if pair in seen:continue
   seen.add(pair);row=[0]*nv
   for j in pos[sig,a]:row[j]+=1
   for j in pos[sig1,a1]:row[j]-=1
   add_int(row,lows[sig1,a1]-lows[sig,a])
 for a,bb in itertools.combinations_with_replacement(range(1,n),2):
  ha,hb=lab[a],lab[bb];weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in tuples};rhs=D*tab.dims[cols[a]]*tab.values[ha,cols[bb]]-sum((weights[v]for v in sp.low),C.zero);add([weights[(0,)+v]*ph[t][0]for v,t in labels]+[C.zero]*(nv-nh),rhs)
 # Four ACTUAL roots, each mass D*sqrt2/4. No projected first-moment zero here.
 for g,ss in d['ising_labels']:
  for a in ising_exponents[ss]:add([C(v[ss-1])*zv[v]if t==a else C.zero for v,t in labels]+[C.zero]*(nv-nh),D*dims[ss]/C(4))
 # Per-type multiplicity bounds proven by the restriction-product unit test.
 for v,B,m in allowed:
  if B<=1:
   old=extend(1);row=[int(j<nh and labels[j][0]==v)for j in range(nv)];row[old]=1;add_int(row,B)
 triple={}
 for a,bb,cc in itertools.combinations_with_replacement(range(1,n),3):
  weights={v:tuples[v][lab[a]]*tuples[v][lab[bb]]*tuples[v][lab[cc]]*tab.dims[v]**2/D**2 for v in tuples};old=extend(1);triple[a,bb,cc]=old;add([weights[(0,)+v]for v,t in labels]+[C.zero]*(old-nh)+[-C.one],-sum((weights[v]for v in sp.low),C.zero))
 for a,bb in itertools.combinations_with_replacement(range(1,n),2):
  prod=[sum(cols[a][i]*cols[bb][j]*R[i][j][k]for i in range(n)for j in range(n))for k in range(n)];qvars={}
  for v in sorted({v for v,t in labels}):
   full=(0,)+v;B=min(prod[k]//full[k]for k in range(n)if full[k])
   if B:qvars[v]=(extend(1),B)
  for k in range(n):
   row=[0]*nv
   for cc in range(1,n):row[triple[tuple(sorted((a,bb,cc)))]]+=cols[cc][k]
   for v,(j,B)in qvars.items():row[j]=((0,)+v)[k]
   add_int(row,prod[k]-int(a==bb and k==0))
  for v,(j,B)in qvars.items():
   old=extend(1);row=[0]*nv;row[j]=row[old]=1
   for k,(w,t)in enumerate(labels):
    if w==v:row[k]-=B
   add_int(row,0)
 return A,b,dict(low=low,labelling=list(lab),indicators=list(ep),variables=nv,equations=len(A),high_labels=[[list(v),a]for v,a in labels],actual_root_exponent=48,ising_root_exponents=ising_exponents,column_support=md,actual_Ising_mass_denominator=4)
