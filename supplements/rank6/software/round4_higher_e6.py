"""Half-E6 subcategory center branching and exact twist-mass constraints."""
from round3_m4 import *
from round4_higher_fast import SmallFieldSpectrum,half_e6_subrings,half_e6_high_allowed,half_e6_low_allowed,coupled_balance_cached
coupled_balance=coupled_balance_cached
def system(R,data,cols,ep,lab,g,x,conjugate):
    C=data['C'];D=data['DD'];dims=data['dims'];tab=data['tab'];height=data['height'];F=data['F'];types=data['phases'];n=len(R)
    cache=data.setdefault('_branch_cache',{});ck=tuple(map(tuple,cols))
    if ck not in cache:
        G,vectors=high_vectors(data,cols);spec=SmallFieldSpectrum(tab,cols,[(v,None) for v in vectors],data);cache[ck]=(G,vectors,spec)
    G,vectors,spec=cache[ck]
    if spec.missing_low:return None,None,{'spectrum':spec.metadata()}
    bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types)) if half_e6_high_allowed(data,v,ti,g,x,conjugate)];nv=len(labels)
    zv={v:sum((C(v[i])*dims[i+1] for i in range(n-1)),C.zero) for v in vectors}
    low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(n)),C.zero) for i in range(n)]
    A=[];b=[]
    def add(co,rhs):
        for row,value in rational_rows(co,rhs,C):A.append(row);b.append(value)
    for i in range(n-1):
        for j in range(i,n-1):add([C(v[i]*v[j]) for v,ti in labels],C(int(G[i,j])))
    for obj in range(1,n):
        for power,target in [(1,0),(2,ep[obj-1])]:add([C(v[obj-1])*zv[v]*types[ti][power-1] for v,ti in labels],C(target)*D-low[obj])
    subD=C(2)+dims[x]**2
    # Relative-center projection respects the twist. The six twist masses
    # follow by the Fourier inversion of all intrinsic half-E6 indicators.
    source=[(-3,dims[x]),(5,2*dims[x]),(2,dims[x]),(-4,dims[x]),(6,dims[x]+C.one),(0,2*dims[x]+C(3))]
    for exponent,mass in source:
        exponent=-exponent if conjugate else exponent
        phase=tuple(C.unit**((F//12)*exponent*k%F)for k in range(1,height+1))
        coeff=[C(v[x-1])*zv[v] if types[ti]==phase else C.zero for v,ti in labels]
        target=D/subD*mass-(low[x] if exponent%12==0 else C.zero)
        add(coeff,target)
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
    tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v]*types[ti][0] for v,ti in labels]+[C.zero]*(len(A[0])-nv)
        add(coeff,rhs)
    return A,b,{'spectrum':spec.metadata(),'vectors':len(vectors),'trace_types':len(types),'variables':len(A[0]),'equations':len(A),'rotation_blocks':rotation_blocks}


def verify(R,c):
 require(c['kind']=='half_e6_projection'and c['version']==1 and c['scope']=='pseudo_unitary'and c['outcome']=='pseudo_unitary_excluded','wrong half-E6 projection certificate')
 require(c['complex_conjugation_reduction']is True,'missing conjugation reduction')
 sub=half_e6_subrings(R);require(bool(sub),'no half-E6 subcategory');g,x=sub[0];data=data_for(R,3,60);tab=data['tab']
 require(c['metadata']==metadata(data)and c['subring']==[0,g,x],'wrong trace domain or subcategory')
 require(len(c['branches'])==len(data['lows']),'omitted low frame');rays=0
 for ix,(cols,br)in enumerate(zip(data['lows'],c['branches'])):
  require(br['low']==ix and br['columns']==list(map(list,cols)),'wrong low frame')
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:require(br['ordinary']==why,'wrong ordinary obstruction');continue
  if not half_e6_low_allowed(cols,g,x):require(br['center_branching_rejected']is True,'wrong low branching obstruction');continue
  labs=tab.assignments(cols);require(br['labellings']==list(map(list,labs)),'omitted character labelling')
  expected=[(list(lab),False,list(ep))for lab in labs for ep in indicator_choices(R)if ep[g-1]==1 and ep[x-1]==1]
  require([(r['labelling'],r['conjugate'],r['indicators'])for r in br['cases']]==expected,'omitted indicator branch')
  for r in br['cases']:
   A,b,meta=system(R,data,cols,r['indicators'],r['labelling'],g,x,False);require(json.loads(json.dumps(meta))==r['system']and r['excluded']is True,'incorrect projection system')
   if A is None:require(r['ray']is None,'unexpected ray')
   else:check_farkas(A,b,r['ray']);rays+=1
 return {'passed':True,'low_frames':len(data['lows']),'exact_rays':rays,'half_e6_twist_tables_covered':2,'complex_conjugation_reduction':True,'optimizer_used':False}

def verify_general(R,c):
 import galois_pseudo_reduction as G
 require(c['kind']=='general_half_e6_projection'and c['version']==1 and c['scope']=='general','wrong general half-E6 projection certificate')
 red=G.verify(R,c['reduction']);ans=verify(R,c['pseudo']);ans['reduction']=red;return ans
