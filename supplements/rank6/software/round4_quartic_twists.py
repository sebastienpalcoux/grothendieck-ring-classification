"""Exact twist/profile refinement for the quartic frontier.

The certificate proves a finite necessary profile reduction. It never asserts
existence from a surviving induction or twist witness.
"""
import sys,json,itertools,math
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as s
from exact import require,evaluate
from induction import discover_roots,check_roots,low_failure
from character_induction import CharacterTable
from spectral_induction import Spectrum
from modular_character_induction import rational_rows
from cyclotomic_stabilizer_trace import data_for,system as base_system,forced_module_data
from higher_traces import indicator_choices,check_farkas
from modular_moments import check_congruence
ROOT=Path(__file__).resolve().parents[1]

def table_for(R,data):
    tab=CharacterTable.__new__(CharacterTable);tab.n=len(R);tab.du=data['ch'].du;tab.K=C=data['C'];tab.seed=[]
    roots=discover_roots(data['ch'].p,C);require(roots is not None,'characters do not split in ambient cyclotomic field');check_roots(data['ch'].p,C,roots)
    tab.rows=[tuple(evaluate(list(reversed(co)),r,C) for co in data['ch'].coeff) for r in roots]
    require(len(tab.rows)==len(R) and len(set(tab.rows))==len(R),'character table incomplete')
    require(all(row[i]*row[j]==sum((C(R[i][j][k])*row[k] for k in range(len(R))),C.zero) for row in tab.rows for i in range(len(R)) for j in range(len(R))),'character homomorphism')
    tab.codegrees=[sum((row[i]*row[tab.du[i]] for i in range(len(R))),C.zero) for row in tab.rows]
    tab.ds=data['dims'];tab.D=data['DD'];tab.fp=next(i for i,row in enumerate(tab.rows) if list(row)==tab.ds)
    tab.dims={};tab.values={};tab.allowed={};tab.compatibility={}
    tab._automorphisms=[C.unit**a for a in range(data['F']) if math.gcd(a,data['F'])==1]
    return tab

def stronger_system(data,tab,cols,lab,A,b,labels):
    C=data['C'];high=[(v,None) for v in dict.fromkeys(v for v,ti in labels)];spec=Spectrum(tab,cols,high)
    if spec.missing_low:return None,None,{'missing_low':spec.missing_low}
    # Galois multiplicities without fixed-twist-type refinement. For a
    # quartic trace field Galois squares need not fix the trace vector.
    rows,rhs=spec.balance(labels,len(A[0]),None);A+=rows;b+=rhs
    forbidden=set(map(tuple,spec.forbidden));keep=[j for j in range(len(A[0])) if j>=len(labels) or labels[j][0] not in forbidden]
    A=[[row[j] for j in keep] for row in A];tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,tab.n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=tab.D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+tuple(labels[j][0])]*data['phases'][labels[j][1]][0] if j<len(labels) else C.zero for j in keep]
        for row,value in rational_rows(coeff,rhs,C):A.append(row);b.append(value)
    return A,b,{**spec.metadata(),'variables':len(A[0]),'rows':len(A)}

def coupled(data,tab,cols,A,b,labels):
 C=data['C'];high=[(v,None) for v in dict.fromkeys(v for v,ti in labels)];sp=Spectrum(tab,cols,high)
 forbidden=set(map(tuple,sp.forbidden));keep=[j for j in range(len(labels)) if labels[j][0] not in forbidden]
 labs=[labels[j] for j in keep];types=data['phases'];idx=dict(zip(sp.vectors,sp.types));one=types.index(tuple(C.one for _ in types[0]));zero=types.index(tuple(C.zero for _ in types[0]));low=Counter((idx[tuple(c)],one) for c in cols)
 allpairs=set((idx[(0,)+tuple(v)],ti) for v,ti in labs)|set(low)
 nv=len(A[0]);seen=set();count=0
 from collections import defaultdict
 positions=defaultdict(list)
 for j,(v,ti) in enumerate(labs):positions[idx[(0,)+tuple(v)],ti].append(j)
 for a in range(data['F']):
  if math.gcd(a,data['F'])>1:continue
  z=C.unit**a;zz=C.unit**(a*a%data['F']);pmap={j:types.index(tuple(evaluate(x.to_list(),zz,C) for x in ty)) for j,ty in enumerate(types)}
  for t,ti in sorted(allpairs,key=str):
   tt=tuple(evaluate(x.to_list(),z,C) for x in t);tj=pmap[ti]
   if (t,ti)==(tt,tj):continue
   pair=tuple(sorted(((str(t),ti),(str(tt),tj))))
   if pair in seen:continue
   seen.add(pair)
   row=[0]*nv
   for j in positions[t,ti]:row[j]+=1
   for j in positions[tt,tj]:row[j]-=1
   rhs=low[tt,tj]-low[t,ti]
   if any(row) or rhs:A.append(row);b.append(rhs);count+=1
 return A,b,count

def verlinde(R,data,tab,cols,lab,A,b,labels,restriction=True):
 C=data['C'];n=len(R);sp=Spectrum(tab,cols,[(v,None) for v in dict.fromkeys(v for v,ti in labels)]);forbidden=set(map(tuple,sp.forbidden));labels=[(v,ti) for v,ti in labels if v not in forbidden];nv=len(A[0]);nh=len(labels);tuples=dict(zip(sp.vectors,sp.types));triple={};base=nv
 lowstar=[]
 for a in range(n):
  row=tab.rows[lab[a]];crow=tuple(evaluate(x.to_list(),C.unit**(data['F']-1),C) for x in row)
  lowstar.append(lab.index(tab.rows.index(crow)))
 for a,bb,c in itertools.combinations_with_replacement(range(1,n),3):
  ha,hb,hc=[lab[x] for x in (a,bb,c)]
  weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)}
  rhs=-sum((weights[v] for v in sp.low),C.zero)
  co=[weights[(0,)+tuple(v)] for v,ti in labels]+[C.zero]*(nv-nh)+[-C.one]
  for row in A:row.append(0)
  triple[(a,bb,c)]=nv;nv+=1
  for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
 if restriction:
  allowed=[v for v in sp.high if list(v[1:]) not in sp.forbidden]
  for a,bb in itertools.combinations_with_replacement(range(1,n),2):
   ca,cb=cols[a],cols[bb];fp=[sum(ca[i]*cb[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
   qvars={}
   for v in allowed:
    bound=min(fp[k]//v[k] for k in range(n) if v[k])
    if bound:qvars[v]=(nv,bound);nv+=1
   for row in A:row.extend([0]*(nv-len(row)))
   for k in range(n):
    row=[0]*nv
    for c in range(1,n):row[triple[tuple(sorted((a,bb,lowstar[c])))]]+=cols[c][k]
    for v,(j,B) in qvars.items():row[j]=v[k]
    A.append(row);b.append(fp[k]-int(a==lowstar[bb] and k==0))
   for v,(j,B) in qvars.items():
    row=[0]*(nv+1);row[j]=1;row[nv]=1
    for k,(w,ti) in enumerate(labels):
     if tuple(w)==v[1:]:row[k]-=B
    for rr in A:rr.append(0)
    A.append(row);b.append(0);nv+=1
 return A,b,labels,base

def recognize(R):
 n=len(R);one=[1]+[0]*(n-1);pointed=[];ising=[]
 for g in range(1,n):
  if R[g][g]!=one:continue
  fixed=[i for i in range(n) if R[g][i]==[int(j==i) for j in range(n)]]
  if fixed:pointed.append(g)
  for x in fixed:
   if R[x][x]==[int(j in (0,g)) for j in range(n)]:ising.append((g,x))
 return {'trivial_associator_involutions':pointed,'ising_pairs':list(map(list,ising))}


def projection_keep(R,data,cols,ep,labels,nv):
 C=data['C'];F=data['F'];height=len(data['phases'][0]);recognition=recognize(R)
 one=tuple(C.one for _ in range(height));minus=tuple(C((-1)**k) for k in range(1,height+1));allowed={};meta=dict(recognition=recognition)
 for g,x in recognition['ising_pairs']:
  require(F%16==0,'Ising twist field must be included in the ambient field')
  require(ep[x-1] in (-1,1),'invalid Ising second indicator')
  exponents=[a for a in range(1,16,2) if C.unit**(F*a//8)+C.unit**((-F*a//8)%F)==C(ep[x-1])*data['dims'][x]]
  require(len(exponents)==4,'incorrect Ising twist support')
  allowed[x]={tuple(C.unit**((F*a*k//16)%F) for k in range(1,height+1)) for a in exponents}
  require(all(not v[x] and v[g]<=v[0] for v in cols),'low Ising projection fails')
 def permitted(v,ti):
  phase=data['phases'][ti]
  if any(v[g-1] and phase not in (one,minus) for g in recognition['trivial_associator_involutions']):return False
  return all((not v[g-1] or phase==minus) and (not v[x-1] or phase in allowed[x]) for g,x in recognition['ising_pairs'])
 return [j for j in range(nv) if j>=len(labels) or permitted(*labels[j])],meta


def build_system(R,data,cols,ep,lab):
 tab=table_for(R,data);module=forced_module_data(R);require(module is not None,'forced cubic module unavailable')
 A,b,meta,labels=base_system(R,data,cols,ep,module['objects'],True)
 A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels)
 A,b,_=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
 keep,projection=projection_keep(R,data,cols,ep,labels,len(A[0]));A=[[row[j] for j in keep] for row in A]
 return A,b,labels,base,keep,projection


def fixed_profile(A,b,labels,base,keep,vectors,profile):
 counts=dict(zip(map(tuple,vectors),profile));kk=[k for k,j in enumerate(keep) if j>=len(labels) or counts[tuple(labels[j][0])]]
 AA=[[row[k] for k in kk] for row in A];bb=list(b)
 for v,count in counts.items():
  if count:AA.append([int(keep[k]<len(labels) and tuple(labels[keep[k]][0])==v) for k in kk]);bb.append(count)
 kept=[keep[k] for k in kk];integ=[int(j<len(labels) or j>=base) for j in kept]
 return AA,bb,kept,integ


def branch_cut(A,b,j,k,left):
 return [row+[0] for row in A]+[[int(i==j) for i in range(len(A[0]))]+[1 if left else -1]],b+[k]


def check_branch(A,b,integ,record):
 nodes=0
 def visit(A,b,c):
  nonlocal nodes
  nodes+=1
  if 'ray' in c:check_farkas(A,b,c['ray']);return
  j=c['split'];k=c['floor'];require(type(j) is int and 0<=j<len(integ) and integ[j] and type(k) is int,'invalid integer split')
  visit(*branch_cut(A,b,j,k,True),c['left']);visit(*branch_cut(A,b,j,k+1,False),c['right'])
 visit(A,b,record['tree']);require(nodes==record['nodes'],'wrong integer-branch count');return nodes


def preliminary_replay(R,data,record):
 tab=table_for(R,data);module=forced_module_data(R);require(module is not None and module['objects']==record['objects'],'preliminary forced module mismatch')
 expected=[];survivors=[];rays=0
 for ix,cols in enumerate(data['lows']):
  labs=tab.assignments(cols)
  if not labs:expected.append((ix,None,None));continue
  for ep in indicator_choices(R):
   A0,b0,_,labels=base_system(R,data,cols,ep,module['objects'],True)
   for lab in labs:
    expected.append((ix,list(lab),list(ep)));entry=next(x for x in record['branches'] if x.get('low')==ix and x.get('labelling')==list(lab) and x.get('indicators')==list(ep))
    if entry['excluded']:
     A,b,meta=stronger_system(data,tab,cols,lab,[row[:] for row in A0],b0[:],labels);require(meta==entry['meta'],'preliminary matrix changed');check_farkas(A,b,entry['ray']);rays+=1
    else:survivors.append((ix,list(lab),list(ep)))
 require([(x['low'],x.get('labelling'),x.get('indicators')) for x in record['branches']]==expected,'preliminary branch domain is incomplete')
 return survivors,rays


def verify(R,record):
 import round4_quartic_profiles as P
 require(record['kind']=='quartic_profile_frontier' and record['version']==1,'wrong quartic frontier record')
 report=P.verify(R,record['profiles']);data=data_for(R,3);prelim,nrays=preliminary_replay(R,data,record['preliminary']);require(record['recognized_subcategories']==recognize(R),'wrong subcategory recognizer')
 expected=[];survivors=[];nc=nb=nw=0
 for ix,lab,ep in prelim:
  br=record['profiles']['branches'][ix];case=next(x for x in br['cases'] if x['labelling']==lab);A,b,labels,base,keep,meta=build_system(R,data,data['lows'][ix],ep,lab)
  for profile in case['survivors']:
   expected.append((ix,lab,ep,profile['profile_index']))
   rec=next(x for x in record['cases'] if (x['low'],x['lab'],x['indicators'],x['profile_index'])==expected[-1])
   AA,bb,kept,integ=fixed_profile(A,b,labels,base,keep,br['high_vectors'],profile['counts']);require((rec['rows'],rec['columns'])==(len(AA),len(AA[0])),'wrong fixed-profile shape')
   if 'congruence' in rec:check_congruence(AA,bb,integ,rec['congruence']);nc+=1
   elif 'branch_certificate' in rec:check_branch(AA,bb,integ,rec['branch_certificate']);nb+=1
   elif 'ray' in rec:check_farkas(AA,bb,rec['ray']);nrays+=1
   elif 'variables' in rec:
    require(rec['keep']==kept,'wrong primal variable domain');v=list(map(Fraction,rec['variables']));require(len(v)==len(kept) and all(x>=0 for x in v),'invalid primal')
    require(all(not integ[j] or x.denominator==1 for j,x in enumerate(v)),'nonintegral primal count');require(all(sum(a*x for a,x in zip(row,v))==rhs for row,rhs in zip(AA,bb)),'primal equation failed');nw+=1;survivors.append(dict(low=ix,labelling=lab,profile_index=profile['profile_index'],rank=profile['rank']))
   elif rec.get('retained_without_exact_decision') is True:
    survivors.append(dict(low=ix,labelling=lab,profile_index=profile['profile_index'],rank=profile['rank'],feasibility_claimed=False))
   else:raise ValueError('unverified fixed-profile result')
 require([(x['low'],x['lab'],x['indicators'],x['profile_index']) for x in record['cases']]==expected,'fixed-profile coverage incomplete')
 if 'general_reduction' in record:
  import galois_pseudo_reduction as G
  report['general_reduction']=G.verify(R,record['general_reduction'])
 return dict(passed=True,optimizer_used=False,preliminary_rays=nrays,congruence_rejections=nc,branch_rejections=nb,exact_necessary_witnesses=nw,survivors=survivors,profile_report=report)
