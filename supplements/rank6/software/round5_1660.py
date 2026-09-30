"""Exact induction-profile refinements for R6_8_1660. Necessary data only."""
import argparse,collections,itertools,json,math,signal,time
from pathlib import Path
import sympy as s
from exact import require,evaluate
import round4_m8_ising_verlinde as M
import round4_quartic_profiles as P
ROOT=Path(__file__).resolve().parents[1]

def domain(data,cols,R):
    require(all(R[i][i][0]==1 for i in range(len(R))), 'self-dual source required')
    G,vs=M.high_vectors(data,cols);sp=M.Spectrum(data['tab'],cols,[(v,None) for v in vs]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad and all(not(v[g-1] and v[ss-1]) for g,ss in data['ising_labels'])]
    # Saturated Galois-character conductor support concerns actual twists.
    # The Ising object has a primitive sixteenth-root twist; each individual
    # central simple fits inside one actual-root mass D*sqrt(2)/4.
    from dimension_block_support import restriction_order_bounds
    conductor=restriction_order_bounds(data,[(0,)+v for v in vs])
    rejected=[];retained=[];effective_orders=[]
    for v,info in zip(vs,conductor['columns']):
        m=info['order_bound'];why=[]
        zv=sum((data['K'](v[i-1])*data['ds'][i] for i in range(1,len(R))),data['K'].zero)
        for g,ss in data['ising_labels']:
            if v[g-1] and m and m%2:why.append('involution_twist_order')
            if v[ss-1]:
                if m and m%16:why.append('Ising_twist_order')
                margin=data['D']*data['ds'][ss]/4-data['K'](v[ss-1])*zv
                if data['embedding'].sign(margin)<0:why.append('individual_Ising_root_mass')
            if v[g-1]:m=math.gcd(m,2) if m else 2
            if v[ss-1]:m=math.gcd(m,16) if m else 16
        if why:rejected.append({'column':[0]+list(v),'reasons':why})
        else:retained.append(v);effective_orders.append(m)
    require(all(effective_orders),'a surviving column has no proved twist-order bound')
    data.setdefault('_domain_summary',{})[tuple(map(tuple,cols))]={'conductor':conductor,'rejected_columns':rejected,'full_twist_exponent_divides':math.lcm(*effective_orders)}
    vs=retained
    A=[];b=[];n=len(cols)
    # A simple Z has exactly one copy of the central unit in Z Z*.  If
    # no other low column fits inside F(Z Z*), its unit-coordinate must be one.
    support_bounds={};removed=[]
    for v in vs:
        w=(0,)+v
        prod=[sum(w[i]*w[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
        compatible=[c for c in cols[1:] if all(c[k]<=prod[k] for k in range(n))]
        if not compatible:
            if prod[0]!=1:removed.append(v)
            else:support_bounds[v]=1
    vs=[v for v in vs if v not in removed]
    print('support_pruned',removed,'multiplicity_bounds',support_bounds,flush=True)
    for i in range(n-1):
        for j in range(i,n-1):A.append([v[i]*v[j] for v in vs]);b.append(int(G[i,j]))
    aa,bb=sp.balance([(v,None) for v in vs],len(vs));A+=aa;b+=bb
    C=data['C'];tab=data['tab'];sigs={v:(tab.dims[v]**2/tab.D**2,)+tt for v,tt in zip(sp.vectors,sp.types)}
    low=collections.Counter(sigs[v] for v in cols);pos=collections.defaultdict(list)
    for j,v in enumerate(vs):pos[sigs[(0,)+v]].append(j)
    allpairs=set(pos)|set(low);seen=set()
    for a in range(data['F']):
        if math.gcd(a,data['F'])>1:continue
        for sig in sorted(allpairs,key=str):
            nsig=tuple(evaluate(z.to_list(),C.unit**a,C) for z in sig);pair=tuple(sorted((str(sig),str(nsig))))
            if pair in seen or sig==nsig:continue
            seen.add(pair);row=[0]*len(vs)
            for j in pos[sig]:row[j]+=1
            for j in pos[nsig]:row[j]-=1
            value=low[nsig]-low[sig]
            if any(row) or value:A.append(row);b.append(value)
    bounds=[min(support_bounds.get(v,10**9),min(int(G[i,i])//(v[i]*v[i]) for i in range(n-1) if v[i])) for v in vs]
    return G,vs,sp,A,b,bounds

def bounded_profiles(R,data,cols,V,sp,A,b,bounds,lab,node_limit=20000000):
    """Bounded affine enumeration, with exact cubic congruences and product bounds."""
    from fractions import Fraction
    n=len(V);rr,piv=s.Matrix([list(row)+[rhs] for row,rhs in zip(A,b)]).rref()
    if n in piv:return [],{'inconsistent':True,'nodes':0}
    free=[j for j in range(n) if j not in piv];expr=[[Fraction(0)]+[Fraction(int(i==j)) for j in free] for i in range(n)]
    for row,i in enumerate(piv):expr[i]=[Fraction(rr[row,-1])]+[-Fraction(rr[row,j]) for j in free]
    def substitute(row):return [row[0]*int(k==0)+sum(row[i+1]*expr[i][k] for i in range(n)) for k in range(len(free)+1)]
    constraints=[]
    def add(expr,lo,hi,divisor=1):
        dd=math.lcm(*(x.denominator for x in expr));v=[int(x*dd) for x in expr]
        if not any(v[1:]):
            require(lo*dd<=v[0]<=hi*dd and v[0]%(divisor*dd)==0,'constant affine contradiction')
        else:constraints.append((v,lo*dd,hi*dd,divisor*dd))
    for e,B in zip(expr,bounds):add(e,0,B)
    triples={}
    for word,forms in P.word_forms(data,cols,V,sp,lab,3):
        den,row=forms[0];e=substitute(row);a,bb,c=word
        bound=min(sum(cols[a][i]*cols[bb][j]*R[i][j][k] for i in range(len(R)) for j in range(len(R)))//cols[c][k] for k in range(len(R)) if cols[c][k])
        add(e,0,den*bound,den);triples[word]=[x/den for x in e]
        for _,row in forms[1:]:add(substitute(row),0,0)
    for a,bb in itertools.combinations_with_replacement(range(1,len(R)),2):
        prod=[sum(cols[a][i]*cols[bb][j]*R[i][j][k] for i in range(len(R)) for j in range(len(R))) for k in range(len(R))]
        for k in range(len(R)):
            e=[Fraction(prod[k]-int(a==bb and k==0))]+[Fraction(0)]*len(free)
            for c in range(1,len(R)):
                for h,z in enumerate(triples[tuple(sorted((a,bb,c)))]):e[h]-=cols[c][k]*z
            add(e,0,0 if k==0 else prod[k])
    order=sorted(range(len(free)),key=lambda j:(bounds[free[j]],-sum(abs(c[0][j+1]) for c in constraints)))
    ub=[bounds[free[j]] for j in order];m=len(free);co=[[v[j+1] for j in order] for v,lo,hi,dd in constraints];const=[v[0] for v,lo,hi,dd in constraints];los=[lo for v,lo,hi,dd in constraints];his=[hi for v,lo,hi,dd in constraints];ds=[dd for v,lo,hi,dd in constraints];q=len(co)
    mn=[[0]*q for _ in range(m+1)];mx=[[0]*q for _ in range(m+1)];gg=[[d for d in ds] for _ in range(m+1)]
    for h in range(m-1,-1,-1):
        for i in range(q):
            z=co[i][h]*ub[h];mn[h][i]=mn[h+1][i]+min(0,z);mx[h][i]=mx[h+1][i]+max(0,z);gg[h][i]=math.gcd(gg[h+1][i],co[i][h])
    count=0;out=[];chosen=[0]*m
    def dfs(h,p):
        nonlocal count
        count+=1
        if count>node_limit:raise TimeoutError('exact constrained-profile node limit')
        if any(p[i]+mx[h][i]<los[i] or p[i]+mn[h][i]>his[i] or p[i]%gg[h][i] for i in range(q)):return
        if h==m:
            vals=[0]*m
            for j,z in zip(order,chosen):vals[j]=z
            profile=tuple(int(e[0]+sum(x*z for x,z in zip(e[1:],vals))) for e in expr);out.append(profile);return
        lo=0;hi=ub[h]
        for i in range(q):
            a=co[i][h]
            if a>0:lo=max(lo,-((p[i]+mx[h+1][i]-los[i])//a));hi=min(hi,(his[i]-p[i]-mn[h+1][i])//a)
            elif a<0:lo=max(lo,-((his[i]-p[i]-mn[h+1][i])//(-a)));hi=min(hi,(p[i]+mx[h+1][i]-los[i])//(-a))
        for x in range(lo,hi+1):chosen[h]=x;dfs(h+1,[p[i]+co[i][h]*x for i in range(q)])
    dfs(0,const);out.sort()
    require(all(all(sum(a*x for a,x in zip(row,v))==rhs for row,rhs in zip(A,b)) for v in out),'enumerated Gram equation failed')
    return out,dict(nodes=count,rank=len(piv),free_variables=m,constraints=q,free_bounds=ub)

def gram_filter(data,cols,V,sp,profiles,lab):
    forms=dict(P.word_forms(data,cols,V,sp,lab,4));triples=dict(P.word_forms(data,cols,V,sp,lab,3));words=list(itertools.combinations_with_replacement(range(1,len(cols)),2));out=[];rejected=[]
    for ix,p in enumerate(profiles):
        ts={w:P.moment_value(f,p)[1] for w,f in triples.items()};qs={w:P.moment_value(f,p)[1] for w,f in forms.items()}
        known=[[int(a==b)]+[ts[tuple(sorted((a,b,c)))] for c in range(1,len(cols))] for a,b in words]
        G=[[qs[tuple(sorted(wi+wj))]-sum(x*y for x,y in zip(known[i],known[j])) for j,wj in enumerate(words)] for i,wi in enumerate(words)]
        bad=next(((i,j,G[i][j]) for i in range(len(G)) for j in range(i,len(G)) if G[i][j]<0),None)
        if bad:rejected.append({'profile_index':ix,'negative_gram_entry':list(bad)})
        else:out.append(ix)
    return {'survivor_indices':out,'rejected':rejected}

def run(height=6,node_limit=20000000,low_select=None,checkpoint=None):
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_8_1660');d=M.data_for(R,3,24);out={'id':'R6_8_1660','scope':'pseudo_unitary_necessary','branches':[],'height':height,'selected_low':low_select,'outcome':'incomplete'}
    for ix,cols in enumerate(d['lows']):
        if low_select is not None and ix!=low_select:continue
        br={'low':ix,'columns':list(map(list,cols))};out['branches'].append(br)
        why=M.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du) or M.projection_failure(d,cols)
        if why:br['ordinary']=why;continue
        G,V,sp,A,b,bounds=domain(d,cols,R);print('domain',ix,len(V),len(A),'rank',s.Matrix(A).rank(),flush=True);br.update(high_vectors=V,column_refinement=d['_domain_summary'][tuple(map(tuple,cols))],cases=[])
        for lab in d['tab'].assignments(cols):
            pp,stats=bounded_profiles(R,d,cols,V,sp,A,b,bounds,lab,node_limit);case={'labelling':list(lab),'profiles':pp,'stats':stats};br['cases'].append(case);print('profiles',ix,lab,len(pp),stats,flush=True)
            case['word_filter']=P.filter_profiles(R,d,cols,V,sp,pp,lab,height)
            keep=[x['profile_index'] for x in case['word_filter']['survivors']];small=[pp[k] for k in keep]
            gg=gram_filter(d,cols,V,sp,small,lab);gg['survivor_indices']=[keep[j] for j in gg['survivor_indices']]
            for x in gg['rejected']:x['profile_index']=keep[x['profile_index']]
            case['gram_filter']=gg
            print('filtered',ix,lab,len(keep),len(gg['survivor_indices']),flush=True)
            if checkpoint:checkpoint.write_text(json.dumps(out,separators=(',',':'))+'\n')
    out['outcome']='complete_necessary_profile_enumeration';return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');ap.add_argument('--height',type=int,default=6);ap.add_argument('--low',type=int);ap.add_argument('--seconds',type=int,default=840);ap.add_argument('--nodes',type=int,default=20000000);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--receipt',type=Path);a=ap.parse_args();st=time.monotonic()
    def stop(*_):raise TimeoutError('explicit discovery deadline')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds)
    try:
        if a.verify:
            import scipy.optimize
            def denied(*_,**__):raise RuntimeError('optimizer disabled for exact replay')
            scipy.optimize.linprog=scipy.optimize.milp=denied
            c=json.loads(a.output.read_text())
            expected=dict(c);expected.pop('seconds',None);o=run(c['height'],a.nodes,c['selected_low']);require(json.loads(json.dumps(o))==expected,'profile replay mismatch');o={'passed':True,'optimizer_used':False,'low':c['selected_low'],'survivors':[len(x['gram_filter']['survivor_indices']) for br in c['branches'] for x in br['cases']]}
            if a.receipt:
                import hashlib,sys
                paths={Path(__file__).resolve(),a.output.resolve(),(ROOT/'data/census.json').resolve()}
                for module in list(sys.modules.values()):
                    name=getattr(module,'__file__',None)
                    if name:
                        q=Path(name).resolve()
                        if q.is_relative_to(ROOT) and q.suffix=='.py':paths.add(q)
                receipt=dict(o,optimized_python=not __debug__,files_sha256={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(paths)})
                a.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
            print(json.dumps(o,sort_keys=True));raise SystemExit
        o=run(a.height,a.nodes,a.low,a.output)
    except TimeoutError as e:
        o=json.loads(a.output.read_text()) if a.output.exists() else {};o.update(outcome='budget_incomplete',reason=str(e))
    signal.alarm(0);o['seconds']=time.monotonic()-st;a.output.write_text(json.dumps(o,separators=(',',':'))+'\n');print({k:v for k,v in o.items() if k!='branches'},flush=True)
