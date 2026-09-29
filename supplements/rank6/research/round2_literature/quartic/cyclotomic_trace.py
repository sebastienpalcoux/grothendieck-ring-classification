"""Exact exploratory cyclotomic trace extension; no ledger allocation.

All rays are checked exactly. A failure to find a ray is inconclusive.
The finite trace domain includes the zero vector for all orders outside
its proved conductor box. The field embedding is checked algebraically.
"""
import sys,json,math,itertools,argparse,time
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
from sympy.polys.numberfields import field_isomorphism
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from induction import Characters,codegree_poly,discover_roots,check_roots,restriction_columns,low_matrices,low_failure
from exact import require,vector,field,embeddings,evaluate,key
from higher_traces import indicator_choices,farkas,check_farkas
from gram_vectors_general import native
from modular_character_induction import rational_rows


def trace_domain(F,primes,height):
    bound=1
    for p in primes:
        e=0
        while p**(e+1)<=height:e+=1
        c=0;n=F
        while n%p==0:n//=p;c+=1
        bound*=p**(max(1,c)+e)
    require(bound%F==0,'ambient conductor is not in the exponent support')
    t=s.Symbol('t');K=field(s.Poly(s.cyclotomic_poly(F,t),t));z=K.unit
    W=field(s.Poly(s.cyclotomic_poly(bound,t),t));w=W.unit
    powers=[w**i for i in range(bound)];step=bound//F
    M=s.Matrix.hstack(*(vector(powers[(step*i)%bound],W.mod.degree()) for i in range(K.mod.degree())))
    invrows=list(M.T.rref()[1]);left=M.extract(invrows,range(M.cols)).inv()
    def down(a):
        rhs=vector(a,W.mod.degree());v=left*rhs.extract(invrows,[0]);require(M*v==rhs,'relative trace not in base field')
        return sum((K(v[i])*z**i for i in range(len(v))),K.zero)
    kernel=[i for i in range(bound) if math.gcd(i,bound)==1 and i%F==1]
    out={tuple(K.zero for _ in range(height))}
    for order in s.divisors(bound):
        order=int(order)
        for a in range(order):
            if math.gcd(a,order)!=1:continue
            out.add(tuple(down(sum((powers[(a*j*u*(bound//order))%bound] for u in kernel),W.zero)/W(len(kernel))) for j in range(1,height+1)))
    return K,sorted(out,key=lambda v:tuple(tuple(key(a)) for a in v)),bound


def data_for(R,height):
    ch=Characters(R);f,K,ds,D,pD,emb=ch.fp();require(f.degree()==4 and pD.degree()==4,'expected quartic FP field')
    F=None;iso=None
    for ff in (16,20,24):
        u=2*s.cos(2*s.pi/ff)
        ii=field_isomorphism(s.AlgebraicNumber(s.CRootOf(pD.as_expr(),3)),s.AlgebraicNumber(u))
        if ii is not None:F,iso=ff,ii;break
    require(F is not None,'no supported exact cyclotomic embedding')
    norm=abs(int(pD.TC()));primes=sorted(map(int,s.factorint(norm)))
    C,phases,bound=trace_domain(F,primes,height);u=C.unit+C.unit**(F-1)
    DD=evaluate(iso,u,C);require(not evaluate(pD.all_coeffs(),DD,C),'invalid global-dimension embedding')
    change=s.Matrix.hstack(*(vector(D**i,4) for i in range(4))).inv()
    dco=[change*vector(v,4) for v in ds]
    dims=[sum((C(v[i])*DD**i for i in range(4)),C.zero) for v in dco]
    # Verify the positive real embedding with isolating rational intervals.
    uf=s.Poly(s.minpoly(2*s.cos(2*s.pi/F)),s.Symbol('_x')) if False else s.Poly(s.minpoly(2*s.cos(2*s.pi/F),s.Symbol('t')),s.Symbol('t'))
    U=field(uf);uu=U.unit;DU=evaluate(iso,uu,U);ee=embeddings(uf)[-1]
    du=[sum((U(v[i])*DU**i for i in range(4)),U.zero) for v in dco]
    require(all(ee.sign(x)>0 for x in du),'nonpositive dimension embedding')
    require(all(dims[i]*dims[j]==sum((C(R[i][j][k])*dims[k] for k in range(len(R))),C.zero) for i in range(len(R)) for j in range(len(R))),'dimension homomorphism failed')
    roots=discover_roots(codegree_poly(R),K);require(roots is not None,'codegrees outside FP field');check_roots(codegree_poly(R),K,roots)
    rest=list(roots);rest.remove(D);cs=[restriction_columns(ds,D/r,K,ch.C) for r in rest];lows=low_matrices(cs,ch.C,gram_prune=True)
    return dict(ch=ch,K=K,ds=ds,D=D,embedding=emb,C=C,dims=dims,DD=DD,F=F,primes=primes,phases=phases,bound=bound,lows=lows,columns=cs,iso=list(map(str,iso)))


def integral_charpoly(x,K):
    degree=K.mod.degree();M=s.Matrix.hstack(*(vector(x*K.unit**i,degree) for i in range(degree)))
    co=list(M.charpoly().all_coeffs())
    return list(map(int,co)) if all(a.q==1 for a in co) else None


def system(R,data,cols,ep,objects,return_state=False):
    C=data['C'];dims=data['dims'];D=data['DD'];types=data['phases'];n=len(R)
    L=s.Matrix.hstack(*map(s.Matrix,cols));G=(data['ch'].C-L*L.T).extract(range(1,n),range(1,n));vectors=[]
    for v in native(G):
        z0=sum((data['K'](v[i])*data['ds'][i+1] for i in range(n-1)),data['K'].zero)
        if not z0 or integral_charpoly(data['D']/z0,data['K']) is None:continue
        co=integral_charpoly(z0,data['K']);require(co is not None,'central dimension nonintegral')
        degree=len(co)-1;norm=abs(co[-1])
        if any(co[j]**degree%norm**j for j in range(1,degree+1)):continue
        vectors.append(tuple(v))
    labels=[(v,ti) for v in vectors for ti in range(len(types))];count=len(labels)
    zv={v:sum((C(v[i])*dims[i+1] for i in range(n-1)),C.zero) for v in vectors}
    low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(n)),C.zero) for i in range(n)]
    A=[];b=[]
    def add(co,rhs):
        for row,value in rational_rows(co,rhs,C):A.append(row);b.append(value)
    for i in range(n-1):
        for j in range(i,n-1):add([C(v[i]*v[j]) for v,ti in labels],C(int(G[i,j])))
    for obj in range(1,n):
        for power,target in [(1,0),(2,ep[obj-1])]:
            add([C(v[obj-1])*zv[v]*types[ti][power-1] for v,ti in labels],C(target)*D-low[obj])
    # Third indicators are rational because 3 is absent from both F and
    # exponent support. Append two nonnegative cyclic multiplicities,
    # whose normalized third-root orbit traces are 1 and -1/2.
    require(3 not in data['primes'] and data['F']%3,'third rationality unavailable')
    for obj in range(1,n):
        H=sum(R[obj][obj][k]*R[k][obj][0] for k in range(n))
        upper=H-3 if obj in objects and H>0 else H
        require(upper>=-Q(H,2),'incompatible local rotation bound')
        old=len(A[0]);total=old+3
        for row in A:row.extend([0]*3)
        coeff=[C(v[obj-1])*zv[v]*types[ti][2] for v,ti in labels]+[C.zero]*(old-count)+[-D,D/C(2),C.zero]
        add(coeff,-low[obj])
        add([C.zero]*old+[C.one,C.one,C.zero],C(H))
        add([C.zero]*old+[C.one,-C.one/C(2),C.one],C(upper))
    meta=dict(vectors=len(vectors),types=len(types),variables=len(A[0]),rows=len(A),order_bound=data['bound'])
    return (A,b,meta,labels) if return_state else (A,b,meta)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='+');ap.add_argument('--output',default=str(Path(__file__).with_name('trace_scan.json')));args=ap.parse_args()
    rings={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};patterns={r['id']:r for r in json.load(open(ROOT/'research/round2_theory/higher_stabilizer_patterns.json'))};out=[]
    for rid in args.ids:
        started=time.monotonic();R=rings[rid]['N'];data=data_for(R,3);pat=patterns[rid]
        objects=[y for y,h in zip(pat['fixed'],pat['cubic_dimensions']) if y in pat['forced_minus_objects'] and h>0]
        rec={'id':rid,'F':data['F'],'primes':data['primes'],'order_bound':data['bound'],'types':len(data['phases']),'lows':len(data['lows']),'objects':objects,'branches':[],'scope':'conditional_pseudo_unitary'}
        print({k:v for k,v in rec.items() if k!='branches'},flush=True)
        for ix,cols in enumerate(data['lows']):
            why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
            if why:rec['branches'].append({'low':ix,'ordinary':why});continue
            for ep in indicator_choices(R):
                A,b,meta=system(R,data,cols,ep,objects);y=farkas(A,b)
                case={'low':ix,'indicators':ep,'meta':meta,'excluded':y is not None}
                if y is not None:check_farkas(A,b,y);case['ray']=y
                rec['branches'].append(case);print(rid,ix,ep,meta,'ray',y is not None,flush=True)
        rec['seconds']=time.monotonic()-started;out.append(rec);Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
