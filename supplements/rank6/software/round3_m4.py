"""Full-character cyclotomic rotation/moment necessary conditions.

The Möbius relative trace evaluates in Q(zeta_F), avoiding construction of
Q(zeta_lcm(F,n)).  All linear infeasibility certificates replay exactly.
No identifiers enter the criterion. Surviving linear systems are inconclusive.
"""
import argparse,json,math,itertools,time,signal
from pathlib import Path
import sympy as s
from sympy.polys.numberfields import field_isomorphism
from exact import require,vector,field,embeddings,evaluate,key,VerificationError
from rings import Characters,codegree_poly,validate
from induction import discover_roots,check_roots,restriction_columns,low_matrices,low_failure
from cyclotomic_stabilizer_trace import integral_charpoly
from higher_traces import indicator_choices,farkas,check_farkas
from gram_vectors_general import native
from modular_character_induction import rational_rows
from character_induction import CharacterTable,Ineligible
from spectral_induction import Spectrum
ROOT=Path(__file__).resolve().parents[1]


def relative_root(C,F,n,a):
    """Normalized Tr_{Q(zeta_lcm(F,n))/Q(zeta_F)}(zeta_n^a)."""
    g=math.gcd(n,a);n//=g;a//=g
    d=math.gcd(n,F);r=n//d
    if math.gcd(r,F)>1:return C.zero
    mu=int(s.mobius(r))
    if not mu:return C.zero
    e=0 if d==1 else (a*pow(r,-1,d))%d
    return C(s.Rational(mu,int(s.totient(r))))*C.unit**((F//d)*e)


def trace_domain(F,primes,height):
    C=field(s.Poly(s.cyclotomic_poly(F,s.Symbol('t')),s.Symbol('t')))
    bound=1
    for p in primes:
        h=0;c=0;k=F
        while p**(h+1)<=height:h+=1
        while k%p==0:k//=p;c+=1
        bound*=p**(max(1,c)+h)
    if bound%F:raise Ineligible('ambient field primes outside global-dimension support')
    out={tuple(C.zero for _ in range(height))}
    for n0 in s.divisors(bound):
        n=int(n0)
        for a in range(n):
            if math.gcd(a,n)==1:out.add(tuple(relative_root(C,F,n,a*j) for j in range(1,height+1)))
    return C,sorted(out,key=lambda v:tuple(tuple(key(x)) for x in v)),bound


def data_for(R,height,F=None):
    
    if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):raise Ineligible('commutative input required')
    validate(R);ch=Characters(R);f,K,ds,D,pD,emb=ch.fp();degree=f.degree()
    if pD.degree()!=degree or degree>4:raise Ineligible('global dimension does not generate supported FP field')
    candidates=[F] if F else [1,3,4,5,8,12,15,16,20,24]
    norm=abs(int(pD.TC()));primes=sorted(map(int,s.factorint(norm)));selected=None
    for ff in candidates:
        if any(int(p) not in primes for p in s.factorint(ff)):continue
        u=2*s.cos(2*s.pi/ff)
        try:iso=field_isomorphism(s.AlgebraicNumber(s.CRootOf(pD.as_expr(),degree-1)),s.AlgebraicNumber(u))
        except (ValueError,NotImplementedError):continue
        if iso is None:continue
        C=field(s.Poly(s.cyclotomic_poly(ff,s.Symbol('t')),s.Symbol('t')))
        roots=discover_roots(ch.p,C)
        if roots is None:continue
        check_roots(ch.p,C,roots);selected=(ff,iso,roots);break
    if selected is None:raise Ineligible('no supported full-character cyclotomic embedding')
    F,iso,roots=selected;C,phases,bound=trace_domain(F,primes,height);u=C.unit+C.unit**(F-1)
    DD=evaluate(iso,u,C);require(not evaluate(pD.all_coeffs(),DD,C),'wrong global embedding')
    change=s.Matrix.hstack(*(vector(D**i,degree) for i in range(degree))).inv()
    dco=[change*vector(v,degree) for v in ds]
    dims=[sum((C(v[i])*DD**i for i in range(degree)),C.zero) for v in dco]
    # Algebraic equality and the positive real embedding identify FPdim.
    uf=s.Poly(s.minpoly(2*s.cos(2*s.pi/F),s.Symbol('t')),s.Symbol('t'))
    U=field(uf);DU=evaluate(iso,U.unit,U);ee=embeddings(uf)[-1]
    require(all(ee.sign(sum((U(v[i])*DU**i for i in range(degree)),U.zero))>0 for v in dco),'nonpositive dimensions')
    require(all(dims[i]*dims[j]==sum((C(R[i][j][k])*dims[k] for k in range(len(R))),C.zero) for i in range(len(R)) for j in range(len(R))),'dimension map')
    cr=discover_roots(codegree_poly(R),K)
    if cr is None:raise Ineligible('formal codegrees outside FP field')
    check_roots(codegree_poly(R),K,cr);rest=list(cr);rest.remove(D)
    cs=[restriction_columns(ds,D/r,K,ch.C) for r in rest];lows=low_matrices(cs,ch.C,gram_prune=True)
    tab=CharacterTable.__new__(CharacterTable);tab.n=len(R);tab.du=ch.du;tab.K=C;tab.seed=[]
    tab.rows=[tuple(evaluate(list(reversed(co)),r,C) for co in ch.coeff) for r in roots]
    require(len(set(tab.rows))==len(R),'incomplete characters')
    tab.codegrees=[sum((row[i]*row[tab.du[i]] for i in range(len(R))),C.zero) for row in tab.rows]
    tab.ds=dims;tab.D=DD;tab.fp=next(i for i,row in enumerate(tab.rows) if list(row)==dims)
    tab.dims={};tab.values={};tab.allowed={};tab.compatibility={};tab._automorphisms=[C.unit**a for a in range(F) if math.gcd(a,F)==1]
    return dict(ch=ch,K=K,ds=ds,D=D,embedding=emb,C=C,dims=dims,DD=DD,F=F,primes=primes,phases=phases,bound=bound,lows=lows,columns=cs,iso=list(map(str,iso)),tab=tab,height=height)


def high_vectors(data,cols):
    n=len(data['ds']);L=s.Matrix.hstack(*map(s.Matrix,cols));G=(data['ch'].C-L*L.T).extract(range(1,n),range(1,n));vectors=[]
    require(all(0<=G[i,i]<=10**18 for i in range(n-1)),'native search bound')
    for v in native(G):
        z=sum((data['K'](v[i])*data['ds'][i+1] for i in range(n-1)),data['K'].zero)
        if not z or integral_charpoly(data['D']/z,data['K']) is None:continue
        co=integral_charpoly(z,data['K']);require(co is not None,'nonintegral dimension')
        degree=len(co)-1;norm=abs(co[-1])
        if any(co[j]**degree%norm**j for j in range(1,degree+1)):continue
        vectors.append(tuple(v))
    return G,vectors


_RAYS={}
def cached_farkas(A,b):
    rays=_RAYS.setdefault((len(A),len(A[0])),[])
    for y in rays:
        support=[(i,v) for i,v in enumerate(y) if v]
        if sum(b[i]*v for i,v in support)>=0:continue
        if all(sum(A[i][j]*v for i,v in support)>=0 for j in range(len(A[0]))):return y
    y=farkas(A,b)
    if y is not None:
        check_farkas(A,b,y)
        if len(rays)<128:rays.append(y)
    return y

def coupled_balance(data,spec,cols,labels,nv):
    """Galois acts on joint eigenvalues by sigma, on twists by sigma squared."""
    from collections import Counter,defaultdict
    C=data['C'];F=data['F'];types=data['phases'];idx=dict(zip(spec.vectors,spec.types))
    one=types.index(tuple(C.one for _ in types[0]));low=Counter((idx[tuple(c)],one) for c in cols)
    positions=defaultdict(list)
    for j,(v,ti) in enumerate(labels):positions[idx[(0,)+v],ti].append(j)
    allpairs=set(positions)|set(low);seen=set();rows=[];rhs=[]
    for a in range(F):
        if math.gcd(a,F)>1:continue
        z=C.unit**a;zz=C.unit**(a*a%F)
        pm={j:types.index(tuple(evaluate(v.to_list(),zz,C) for v in ty)) for j,ty in enumerate(types)}
        for typ,ti in sorted(allpairs,key=str):
            tt=tuple(evaluate(v.to_list(),z,C) for v in typ);tj=pm[ti]
            if (typ,ti)==(tt,tj):continue
            pair=tuple(sorted(((str(typ),ti),(str(tt),tj))))
            if pair in seen:continue
            seen.add(pair);row=[0]*nv
            for j in positions[typ,ti]:row[j]+=1
            for j in positions[tt,tj]:row[j]-=1
            b=low[tt,tj]-low[typ,ti]
            if any(row) or b:rows.append(row);rhs.append(b)
    return rows,rhs


def system(R,data,cols,ep,lab):
    C=data['C'];D=data['DD'];dims=data['dims'];tab=data['tab'];height=data['height'];F=data['F'];types=data['phases'];n=len(R)
    cache=data.setdefault('_branch_cache',{});ck=tuple(map(tuple,cols))
    if ck not in cache:
        G,vectors=high_vectors(data,cols);spec=Spectrum(tab,cols,[(v,None) for v in vectors]);cache[ck]=(G,vectors,spec)
    G,vectors,spec=cache[ck]
    if spec.missing_low:return None,None,{'spectrum':spec.metadata()}
    bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types))];nv=len(labels)
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
    tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v]*types[ti][0] for v,ti in labels]+[C.zero]*(len(A[0])-nv)
        add(coeff,rhs)
    return A,b,{'spectrum':spec.metadata(),'vectors':len(vectors),'trace_types':len(types),'variables':len(A[0]),'equations':len(A),'rotation_blocks':rotation_blocks}


def metadata(data):return {'F':data['F'],'prime_support':data['primes'],'order_bound':data['bound'],'height':data['height'],'types':len(data['phases']),'columns':list(map(len,data['columns'])),'lows':len(data['lows'])}


def run(R,height,F=None,output=None):
    data=data_for(R,height,F);tab=data['tab'];report={'kind':'ambient_full_character_rotation','engine_version':2,'scope':'pseudo_unitary_necessary','metadata':metadata(data),'branches':[]}
    print(report['metadata'],flush=True)
    for ix,cols in enumerate(data['lows']):
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        br={'low':ix,'columns':list(map(list,cols))}
        if why:br['ordinary']=why;report['branches'].append(br);continue
        labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[];report['branches'].append(br)
        for lab in labs:
            for ep in indicator_choices(R):
                A,b,meta=system(R,data,cols,ep,lab);ray=None if A is None else cached_farkas(A,b)
                if ray is not None:check_farkas(A,b,ray)
                rec={'labelling':list(lab),'indicators':list(ep),'system':meta,'excluded':A is None or ray is not None,'ray':ray};br['cases'].append(rec)
                print(ix,lab,ep,meta.get('variables'),rec['excluded'],flush=True)
                if not rec['excluded']:
                    report['outcome']='no_exact_obstruction';return report
        if output:output.write_text(json.dumps(report,separators=(',',':'))+'\n')
    report['outcome']='pseudo_unitary_excluded';return report


def verify(R,c):
    require(c['kind']=='ambient_full_character_rotation' and c['scope']=='pseudo_unitary_necessary','wrong ambient criterion/scope')
    require(c['outcome']=='pseudo_unitary_excluded','incomplete ambient exclusion')
    md=c['metadata'];data=data_for(R,md['height'],md['F']);data['coupled']=c.get('engine_version',1)>=2
    require(md==metadata(data),'wrong finite cyclotomic/low-frame domain')
    require(len(c['branches'])==len(data['lows']),'omitted low frame')
    tab=data['tab'];rays=0
    for ix,(cols,br) in enumerate(zip(data['lows'],c['branches'])):
        require(br['low']==ix and br['columns']==list(map(list,cols)),'wrong low frame')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:
            require(br['ordinary']==why,'wrong ordinary obstruction');continue
        labs=tab.assignments(cols);require(br['labellings']==list(map(list,labs)),'omitted low character labelling')
        expected=[(list(lab),list(ep)) for lab in labs for ep in indicator_choices(R)]
        require([(cc['labelling'],cc['indicators']) for cc in br['cases']]==expected,'omitted labelling/indicator branch')
        for cc in br['cases']:
            A,b,meta=system(R,data,cols,cc['indicators'],cc['labelling'])
            require(json.loads(json.dumps(meta))==cc['system'] and cc['excluded'] is True,'incorrect system metadata')
            if A is None:require(cc['ray'] is None,'unexpected ray in spectral exclusion')
            else:check_farkas(A,b,cc['ray']);rays+=1
    return {'passed':True,'low_frames':len(data['lows']),'exact_rays':rays,'optimizer_used':False}


def verify_general(R,c):
    import galois_pseudo_reduction as G
    require(c['kind']=='general_ambient_full_character_rotation' and c['version']==1 and c['scope']=='general','wrong general ambient certificate')
    red=G.verify(R,c['reduction']);answer=verify(R,c['pseudo']);return dict(answer,reduction=red)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--height',type=int,default=3);ap.add_argument('--conductor',type=int);ap.add_argument('--seconds',type=int,default=840);ap.add_argument('--verify',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==a.id);st=time.monotonic()
    if a.verify:
        record=json.loads(a.output.read_text());c=record.get('certificate',record)
        print(json.dumps((verify_general if c['kind']=='general_ambient_full_character_rotation' else verify)(R,c),indent=2));raise SystemExit(0)
    def stop(*_):raise TimeoutError('explicit discovery budget')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds)
    try:rec=run(R,a.height,a.conductor,a.output)
    except Ineligible as e:rec={'outcome':'ineligible','reason':str(e)}
    except TimeoutError as e:
        rec=json.loads(a.output.read_text()) if a.output.exists() else {}
        rec.update(outcome='budget_incomplete',reason=str(e))
    finally:signal.alarm(0)
    rec.update(id=a.id,seconds=time.monotonic()-st);a.output.write_text(json.dumps(rec,separators=(',',':'))+'\n');print({k:v for k,v in rec.items() if k!='branches'},flush=True)
