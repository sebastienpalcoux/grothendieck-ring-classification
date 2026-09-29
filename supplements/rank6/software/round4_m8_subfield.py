"""Galois-subfield cyclotomic rotation constraints, with exact replay.

The complete character field may be a proper subfield of its cyclotomic
ambient field. Normalized traces and rotation spectra are projected into it;
this preserves every necessary equation while reducing arithmetic degree.
"""
import argparse,itertools,json,math,signal,time
from pathlib import Path
import sympy as s
from sympy.polys.numberfields import field_isomorphism
import round3_m4 as ambient
from round3_m4 import (require,vector,field,embeddings,evaluate,key,Ineligible,
 Characters,validate,discover_roots,check_roots,restriction_columns,low_matrices,
 CharacterTable,indicator_choices,low_failure,high_vectors,Spectrum,rational_rows,
 cached_farkas,check_farkas)
ROOT=Path(__file__).resolve().parents[1]


def data_for(R,height,F):
    if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):raise Ineligible('commutative input required')
    if not any(R[a][a]==[int(k==0)+int(k==a) for k in range(len(R))] for a in range(1,len(R))):raise Ineligible('no Fibonacci based subcategory')
    validate(R);ch=Characters(R);f,K,ds,D,pD,emb=ch.fp();degree=f.degree()
    if degree!=pD.degree() or degree>4:raise Ineligible('FP dimension does not generate a supported field')
    roots=discover_roots(ch.p,K)
    if roots is None:raise Ineligible('full character field exceeds the FP field')
    check_roots(ch.p,K,roots)
    fproots=discover_roots(f,K)
    if fproots is None:raise Ineligible('FP field is not Galois')
    check_roots(f,K,fproots)
    if any(evaluate(r.to_list(),r,K)!=K.unit for r in fproots):raise Ineligible('subfield exponent is greater than two')
    norm=abs(int(pD.TC()));primes=sorted(map(int,s.factorint(norm)))
    if any(int(p) not in primes for p in s.factorint(F)):raise Ineligible('conductor primes outside global-dimension norm')
    C=field(s.Poly(s.cyclotomic_poly(F,s.Symbol('t')),s.Symbol('t')))
    iso=field_isomorphism(s.AlgebraicNumber(s.CRootOf(pD.as_expr(),degree-1)),s.AlgebraicNumber(2*s.cos(2*s.pi/F)))
    if iso is None:raise Ineligible('FP field not in selected conductor')
    DD=evaluate(iso,C.unit+C.unit**(F-1),C)
    require(not evaluate(pD.all_coeffs(),DD,C),'wrong positive global-dimension embedding')
    change=s.Matrix.hstack(*(vector(D**i,degree) for i in range(degree))).inv()
    xco=change*vector(K.unit,degree)
    xx=sum((C(xco[i])*DD**i for i in range(degree)),C.zero)
    matrix=s.Matrix.hstack(*(vector(xx**i,C.mod.degree()) for i in range(degree)))
    piv=list(matrix.T.rref()[1]);left=matrix.extract(piv,range(degree)).inv()
    kernel=[a for a in range(F) if math.gcd(a,F)==1 and evaluate(xx.to_list(),C.unit**a,C)==xx]
    require(len(kernel)*degree==int(s.totient(F)),'wrong fixed-subfield degree')
    projection_cache={}
    def project(value):
        if value in projection_cache:return projection_cache[value]
        trace=sum((evaluate(value.to_list(),C.unit**a,C) for a in kernel),C.zero)/C(len(kernel))
        rhs=vector(trace,C.mod.degree());co=left*rhs.extract(piv,[0]);require(matrix*co==rhs,'trace leaves fixed field')
        ans=sum((K(co[i])*K.unit**i for i in range(degree)),K.zero);projection_cache[value]=ans;return ans
    cyclotomic_root=ambient.relative_root
    def relative(order,power):return project(cyclotomic_root(C,F,order,power))
    bound=1
    for p in primes:
        h=0;c=0;n=F
        while p**(h+1)<=height:h+=1
        while n%p==0:n//=p;c+=1
        bound*=p**(max(1,c)+h)
    phases={tuple(K.zero for _ in range(height))}
    for nn in s.divisors(bound):
        nn=int(nn)
        for a in range(nn):
            if math.gcd(a,nn)==1:phases.add(tuple(relative(nn,a*j) for j in range(1,height+1)))
    phases=sorted(phases,key=lambda v:tuple(tuple(key(x)) for x in v))
    cr=discover_roots(ambient.codegree_poly(R),K)
    require(cr is not None,'formal codegrees outside character field');check_roots(ambient.codegree_poly(R),K,cr)
    rest=list(cr);rest.remove(D);cs=[restriction_columns(ds,D/r,K,ch.C) for r in rest];lows=low_matrices(cs,ch.C,gram_prune=True)
    tab=CharacterTable.__new__(CharacterTable);tab.n=len(R);tab.du=ch.du;tab.K=K;tab.seed=[]
    tab.rows=[tuple(evaluate(list(reversed(co)),r,K) for co in ch.coeff) for r in roots]
    require(len(set(tab.rows))==len(R),'incomplete characters')
    tab.codegrees=[sum((row[i]*row[tab.du[i]] for i in range(len(R))),K.zero) for row in tab.rows]
    tab.ds=ds;tab.D=D;tab.fp=next(i for i,row in enumerate(tab.rows) if list(row)==ds)
    tab.dims={};tab.values={};tab.allowed={};tab.compatibility={};tab._automorphisms=fproots
    return dict(ch=ch,K=K,ds=ds,D=D,embedding=emb,C=K,dims=ds,DD=D,F=F,primes=primes,phases=phases,bound=bound,lows=lows,columns=cs,tab=tab,height=height,relative=relative,kernel=kernel,fibonacci_labels=[a for a in range(1,len(R)) if R[a][a]==[int(k==0)+int(k==a) for k in range(len(R))]])


def system(R,data,cols,ep,lab):
    C=data['C'];D=data['DD'];dims=data['dims'];tab=data['tab'];height=data['height'];F=data['F'];types=data['phases'];n=len(R)
    cache=data.setdefault('_branch_cache',{});ck=tuple(map(tuple,cols))
    if ck not in cache:
        G,vectors=high_vectors(data,cols);spec=Spectrum(tab,cols,[(v,None) for v in vectors]);cache[ck]=(G,vectors,spec)
    G,vectors,spec=cache[ck]
    if spec.missing_low:return None,None,{'spectrum':spec.metadata()}
    bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types)) if all(not v[a-1] or types[ti]==tuple(data['relative'](5,2*k) for k in range(1,height+1)) for a in data['fibonacci_labels'])];nv=len(labels)
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
            rt=sorted({tuple(data['relative'](order,a*r) for r in rs) for a in range(order)},key=str)
            old=len(A[0]);count=len(rt)
            for row in A:row.extend([0]*count)
            add([C.zero]*old+[C.one]*count,C(powers[order][0]))
            for j,r in enumerate(rs):
                k=order//r;constant=sum((C(powers[r][i])*low[i] for i in range(n)),C.zero)
                co=[-C(sum(powers[r][i]*v[i-1] for i in range(1,n)))*zv[v]*types[ti][k-1] for v,ti in labels]+[C.zero]*(old-nv)+[D*tt[j] for tt in rt]
                add(co,constant)
            rotation_blocks.append((obj,order,old,count))
    # Galois-orbit count equality, without invalid fixed-trace refinement.
    one=types.index(tuple(C.one for _ in types[0]));rows,rhs=spec.balance(labels,len(A[0]),one);A+=rows;b+=rhs
    tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v]*types[ti][0] for v,ti in labels]+[C.zero]*(len(A[0])-nv)
        add(coeff,rhs)
    return A,b,{'spectrum':spec.metadata(),'vectors':len(vectors),'trace_types':len(types),'variables':len(A[0]),'equations':len(A),'rotation_blocks':rotation_blocks}


def metadata(d):
    return dict(ambient.metadata(d),character_degree=d['K'].mod.degree(),fixed_subfield_kernel=d['kernel'],fibonacci_labels=d['fibonacci_labels'],subcategory_twist_pruning=True)


def run(R,height,F,output=None,prepared=None):
    d=prepared if prepared is not None else data_for(R,height,F);report={'kind':'subfield_full_character_rotation','version':1,'scope':'pseudo_unitary_necessary','metadata':metadata(d),'branches':[]}
    print(report['metadata'],flush=True)
    for ix,cols in enumerate(d['lows']):
        why=low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
        br={'low':ix,'columns':list(map(list,cols))};report['branches'].append(br)
        if why:br['ordinary']=why;continue
        bad=next(((j,a) for j,c in enumerate(cols) for a in d['fibonacci_labels'] if c[a]>c[0]),None)
        if bad:br['fibonacci_twist_one_failure']=list(bad);continue
        labs=d['tab'].assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
        for lab in labs:
            for ep in indicator_choices(R):
                A,b,meta=system(R,d,cols,ep,lab);ray=None if A is None else cached_farkas(A,b)
                if ray is not None:check_farkas(A,b,ray)
                rec={'labelling':list(lab),'indicators':list(ep),'system':meta,'excluded':A is None or ray is not None,'ray':ray};br['cases'].append(rec)
                print(ix,lab,ep,meta.get('variables'),rec['excluded'],flush=True)
                if not rec['excluded']:report['outcome']='no_exact_obstruction';return report
        if output:output.write_text(json.dumps(report,separators=(',',':'))+'\n')
    report['outcome']='pseudo_unitary_excluded';return report


def verify(R,c):
    require(c['kind']=='subfield_full_character_rotation' and c['version']==1 and c['scope']=='pseudo_unitary_necessary','wrong subfield certificate')
    require(c['outcome']=='pseudo_unitary_excluded','incomplete exclusion')
    md=c['metadata'];d=data_for(R,md['height'],md['F']);require(md==metadata(d),'wrong subfield/trace domain')
    require(len(c['branches'])==len(d['lows']),'missing low frames');rays=0
    for ix,(cols,br) in enumerate(zip(d['lows'],c['branches'])):
        require(br['low']==ix and br['columns']==list(map(list,cols)),'wrong low frame')
        why=low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
        if why:require(br['ordinary']==why,'incorrect ordinary failure');continue
        bad=next(((j,a) for j,c in enumerate(cols) for a in d['fibonacci_labels'] if c[a]>c[0]),None)
        if bad:require(br['fibonacci_twist_one_failure']==list(bad),'wrong Fibonacci low projection');continue
        labs=d['tab'].assignments(cols);require(br['labellings']==list(map(list,labs)),'missing label assignments')
        expected=[(list(lab),list(ep)) for lab in labs for ep in indicator_choices(R)]
        require([(cc['labelling'],cc['indicators']) for cc in br['cases']]==expected,'missing indicator branches')
        for cc in br['cases']:
            A,b,meta=system(R,d,cols,cc['indicators'],cc['labelling'])
            require(json.loads(json.dumps(meta))==cc['system'] and cc['excluded'] is True,'incorrect system metadata')
            if A is None:require(cc['ray'] is None,'unexpected ray')
            else:check_farkas(A,b,cc['ray']);rays+=1
    return dict(passed=True,low_frames=len(d['lows']),exact_rays=rays,optimizer_used=False)

def verify_general(R,c):
    import galois_pseudo_reduction as reduction
    require(c.get('kind')=='general_fibonacci_subfield_rotation' and c.get('version')==1 and c.get('scope')=='general','wrong general subfield certificate')
    red=reduction.verify(R,c['reduction']);out=verify(R,c['pseudo']);return dict(out,reduction=red)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--height',type=int,default=3);ap.add_argument('--conductor',type=int,required=True);ap.add_argument('--seconds',type=int,default=800);ap.add_argument('--verify',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==a.id);st=time.monotonic()
    if a.verify:print(verify(R,json.load(open(a.output))));raise SystemExit
    def stop(*_):raise TimeoutError('explicit discovery budget')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds)
    try:rec=run(R,a.height,a.conductor,a.output)
    except Ineligible as e:rec={'outcome':'ineligible','reason':str(e)}
    except TimeoutError as e:
        rec=json.loads(a.output.read_text()) if a.output.exists() else {};rec.update(outcome='budget_incomplete',reason=str(e))
    finally:signal.alarm(0)
    rec.update(id=a.id,seconds=time.monotonic()-st);a.output.write_text(json.dumps(rec,separators=(',',':'))+'\n');print({k:v for k,v in rec.items() if k!='branches'},flush=True)
