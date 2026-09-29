"""Cyclic-three pointed subcategory twist-support criterion."""
from round3_m4 import *
from round4_higher_fast import cyclic_three_subrings,cyclic_three_allowed,coupled_balance_cached
coupled_balance=coupled_balance_cached
def _core(R,data,cols,ep,g,h,omega):
    C=data['C'];D=data['DD'];dims=data['dims'];tab=data['tab'];height=data['height'];F=data['F'];types=data['phases'];n=len(R)
    cache=data.setdefault('_branch_cache',{});ck=tuple(map(tuple,cols))
    if ck not in cache:
        G,vectors=high_vectors(data,cols);spec=Spectrum(tab,cols,[(v,None) for v in vectors]);cache[ck]=(G,vectors,spec)
    G,vectors,spec=cache[ck]
    if spec.missing_low:return None,None,{'spectrum':spec.metadata()}
    bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types)) if cyclic_three_allowed(data,v,ti,g,h,omega)];nv=len(labels)
    zv={v:sum((C(v[i])*dims[i+1] for i in range(n-1)),C.zero) for v in vectors}
    low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(n)),C.zero) for i in range(n)]
    A=[];b=[]
    def add(co,rhs):
        for row,value in rational_rows(co,rhs,C):A.append(row);b.append(value)
    for i in range(n-1):
        for j in range(i,n-1):add([C(v[i]*v[j]) for v,ti in labels],C(int(G[i,j])))
    for obj in range(1,n):
        for power,target in [(1,0),(2,ep[obj-1])]:add([C(v[obj-1])*zv[v]*types[ti][power-1] for v,ti in labels],C(target)*D-low[obj])
    # Every divisor moment of the cyclic rotation on Hom(1,X^order).
    rotation_blocks=[]
    for obj in range(1,n):
        powers=[[1]+[0]*(n-1)]
        for k in range(height):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(n)) for j in range(n)])
        for order in range(3,height+1):
            rs=[int(r) for r in s.divisors(order) if r<order]
            rt=sorted({tuple(relative_root(C,F,order,a*r) for r in rs) for a in range(order)},key=str)
            old=len(A[0]);count=len(rt)
            for row in A:row.extend([0]*count)
            add([C.zero]*old+[C.one]*count,C(powers[order][0]))
            for j,r in enumerate(rs):
                k=order//r;constant=sum((C(powers[r][i])*low[i] for i in range(n)),C.zero)
                co=[-C(sum(powers[r][i]*v[i-1] for i in range(1,n)))*zv[v]*types[ti][k-1] for v,ti in labels]+[C.zero]*(old-nv)+[D*tt[j] for tt in rt]
                add(co,constant)
            rotation_blocks.append((obj,order,old,count))
    # Galois-orbit count equality, without invalid fixed-trace refinement.
    rows,rhs=(coupled_balance(data,spec,cols,labels,len(A[0])) if data.get('coupled',True) else spec.balance(labels,len(A[0]),None));A+=rows;b+=rhs
    return A,b,dict(C=C,D=D,dims=dims,tab=tab,height=height,F=F,types=types,n=n,spec=spec,vectors=vectors,labels=labels,nv=nv,rotation_blocks=rotation_blocks)

def system(R,data,cols,ep,lab,g,h,omega):
    ck=(tuple(map(tuple,cols)),tuple(ep),g,h,omega);cache=data.setdefault('_core_cache',{})
    if ck not in cache:cache[ck]=_core(R,data,cols,ep,g,h,omega)
    aa,bb,state=cache[ck]
    if aa is None:return aa,bb,state
    A=[list(row)for row in aa];b=list(bb)
    C=state['C'];D=state['D'];dims=state['dims'];tab=state['tab'];height=state['height'];F=state['F'];types=state['types'];n=state['n'];spec=state['spec'];vectors=state['vectors'];labels=state['labels'];nv=state['nv'];rotation_blocks=state['rotation_blocks']
    def add(co,rhs):
        for row,value in rational_rows(co,rhs,C):A.append(row);b.append(value)
    tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v]*types[ti][0] for v,ti in labels]+[C.zero]*(len(A[0])-nv)
        add(coeff,rhs)
    return A,b,{'spectrum':spec.metadata(),'vectors':len(vectors),'trace_types':len(types),'variables':len(A[0]),'equations':len(A),'rotation_blocks':rotation_blocks}


def certificate(R,progress=None):
 sub=cyclic_three_subrings(R)
 if not sub:raise Ineligible('no cyclic pointed subcategory of order three')
 data=data_for(R,3,24);g,h=sub[0];tab=data['tab'];out={'kind':'cyclic_three_projection','version':1,'scope':'pseudo_unitary','metadata':metadata(data),'subring':[0,g,h],'branches':[]}
 for ix,cols in enumerate(data['lows']):
  br={'low':ix,'columns':list(map(list,cols))};out['branches'].append(br);why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:br['ordinary']=why;continue
  labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
  for lab in labs:
   for omega in range(3):
    for ep in indicator_choices(R):
     A,b,meta=system(R,data,cols,ep,lab,g,h,omega);y=None if A is None else cached_farkas(A,b)
     if A is not None and y is None:return None
     br['cases'].append({'labelling':list(lab),'associator_class':omega,'indicators':list(ep),'system':meta,'ray':y,'excluded':True})
     if progress:progress(ix,lab,omega,ep)
 out['outcome']='pseudo_unitary_excluded';return out

def verify(R,c):
 require(c['kind']=='cyclic_three_projection' and c['version']==1 and c['scope']=='pseudo_unitary' and c['outcome']=='pseudo_unitary_excluded','wrong cyclic-three projection certificate')
 sub=cyclic_three_subrings(R);require(bool(sub),'no cyclic-three subcategory');g,h=sub[0];data=data_for(R,3,24);tab=data['tab']
 require(c['metadata']==metadata(data) and c['subring']==[0,g,h],'wrong trace domain or pointed subcategory')
 require(len(c['branches'])==len(data['lows']),'omitted low frame');rays=0
 for ix,(cols,br)in enumerate(zip(data['lows'],c['branches'])):
  require(br['low']==ix and br['columns']==list(map(list,cols)),'wrong low frame')
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:require(br['ordinary']==why,'wrong ordinary obstruction');continue
  labs=tab.assignments(cols);require(br['labellings']==list(map(list,labs)),'omitted character labelling')
  expected=[(list(lab),omega,list(ep))for lab in labs for omega in range(3)for ep in indicator_choices(R)]
  require([(r['labelling'],r['associator_class'],r['indicators'])for r in br['cases']]==expected,'omitted associator or indicator branch')
  for r in br['cases']:
   A,b,meta=system(R,data,cols,r['indicators'],r['labelling'],g,h,r['associator_class']);require(json.loads(json.dumps(meta))==r['system'] and r['excluded']is True,'incorrect projection system')
   if A is None:require(r['ray']is None,'unexpected ray')
   else:check_farkas(A,b,r['ray']);rays+=1
 return {'passed':True,'low_frames':len(data['lows']),'exact_rays':rays,'associator_classes':3,'optimizer_used':False}

def verify_general(R,c):
 require(c['kind']=='general_cyclic_three_projection'and c['version']==1 and c['scope']=='general','wrong general cyclic-three certificate')
 require(c['reduction']=={'kind':'two_FP_values'},'wrong general-scope gate')
 ch=Characters(R);f,K,ds,D,pD,embedding=ch.fp();require(len(set(ds))==2 and K.one in ds,'two-FP-value reduction does not apply')
 ans=verify(R,c['pseudo']);ans['reduction']={'kind':'two_FP_values','galois_pseudo_unitary':True};return ans
