"""Exact finite checks on the completed quartic center modular data.

These checks do not construct a fusion category. They certify coprime higher
central charges, Galois covariance, and all generalized rotation eigenspaces
at tensor powers 2 through 16 for each original simple object.
"""
import argparse,itertools,json,math,time
from functools import lru_cache
from pathlib import Path
import sympy as s
from exact import require,evaluate,vector,field,embeddings,t
from round3_m4 import data_for
from round5_quartic_pair import digest
ROOT=Path(__file__).resolve().parents[1]


def centers(rid,cert,R):
    F=16 if rid=='R6_4_91' else 20;data=data_for(R,3,F);C=data['C']
    if F==20:
        orb=cert['orbits'][0];m=orb['modular'][0];chars=[[C(list(map(s.Rational,v))) for v in row] for row in m['characters']];ds=[C(list(map(s.Rational,v))) for v in m['dimensions']];W=orb['W']
        for li,lc in enumerate(m['labellings']):
            for case in lc['cases']:
                if not case['consistent']:continue
                ass=lc['assignments'][case['S']];S=[[ds[j]*chars[ass[j]][i]/data['DD'] for j in range(len(ds))] for i in range(len(ds))]
                yield data,dict(labelling=li,S=case['S']),W,ds,S,case['twist_exponents']
    else:
        m=next(p for p in cert['profiles'] if p['center_rank']==42)['fusion_orbits'][0]['modular'];chars=[[C(list(map(s.Rational,v))) for v in row] for row in m['characters']];ds0=[C(list(map(s.Rational,v))) for v in m['dimension_coefficients']];q=data['dims'][3];SI=[[C.one,C.one,q],[C.one,C.one,-q],[q,-q,C.zero]];mul=lambda i,v:[sum(R[i][j][k]*v[j] for j in range(6)) for k in range(6)]
        for case in m['cases']:
            if not case['consistent']:continue
            ass=m['assignments'][case['S']];SE=[[ds0[j]*chars[ass[j]][i] for j in range(14)] for i in range(14)];S=[[SI[a][b]*SE[i][j]/data['DD'] for b in range(3) for j in range(14)] for a in range(3) for i in range(14)];W=[mul(a,v) for a in [0,4,3] for v in m['restriction']];ds=[d*v for d in [C.one,C.one,q] for v in ds0];ee=[(x+e)%16 for x in [0,8,case['ising_twist_exponent']] for e in case['twist_exponents']]
            yield data,dict(S=case['S'],ising_twist_exponent=case['ising_twist_exponent']),W,ds,S,ee


def check_variant(R,data,W,ds,S,ee,orders):
    C=data['C'];F=data['F'];r=len(W);theta=[C.unit**e for e in ee];real=C.unit+C.unit**(F-1);B=s.Matrix.hstack(*[vector(real**j,C.mod.degree()) for j in range(4)]);piv=list(B.T.rref()[1]);inv=B[piv,:].inv();p=s.Poly({15:t**4-t**3-4*t**2+4*t+1,16:t**4-4*t**2+2,20:t**4-5*t**2+5}[F],t);Kreal=field(p);E=embeddings(p)[-1];gauss=[]
    require(sum((v*v for v in ds),C.zero)==data['DD']**2,'center dimension')
    require(all(sum((S[i][j]*C(W[j][0]) for j in range(r)),C.zero)==C(W[i][0]) and (not W[i][0] or ee[i]==0) for i in range(r)),'unit induction S,T invariance')
    for n in range(F):
        if math.gcd(n,F)!=1:continue
        tau=sum((d*d*C.unit**(e*n%F) for d,e in zip(ds,ee)),C.zero);vv=vector(tau,C.mod.degree());co=inv*vv[piv,:];require(B*co==vv,'nonreal coprime Gauss sum');value=evaluate(list(reversed(co)),Kreal.unit,Kreal);sgn=E.sign(value);require(sgn==1,'nonpositive coprime Gauss sum');gauss.append(dict(n=n,real_coefficients=[str(x) for x in co],sign=sgn))
    pos={tuple(row):(i,1) for i,row in enumerate(S)};pos.update({tuple(-v for v in row):(i,-1) for i,row in enumerate(S)});galois=[]
    for a in range(F):
        if math.gcd(a,F)!=1:continue
        pp=[pos.get(tuple(evaluate(v.to_list(),C.unit**a,C) for v in row)) for row in S];require(all(p is not None for p in pp),'Galois row is not a signed permutation');require(len(set(p[0] for p in pp))==r,'nonbijective Galois action');require(all(theta[p[0]]==theta[i]**(a*a) for i,p in enumerate(pp)),'Galois twist compatibility');galois.append(dict(a=a,permutation=[list(p) for p in pp]))
    powers={}
    for a in range(len(R)):
        powers[a,0]=[1]+[0]*(len(R)-1)
        for k in range(1,max(orders)+1):powers[a,k]=[sum(powers[a,k-1][i]*R[i][a][j] for i in range(len(R))) for j in range(len(R))]
    nu={m:[[sum((S[b][j]*theta[j]**m*C(W[j][a]) for j in range(r)),C.zero) for a in range(len(R))] for b in range(r)] for n in orders for m in s.divisors(n)}
    require(all(nu[1][b][a]==C(W[b][a])/theta[b] for b in range(r) for a in range(len(R))),'first generalized indicator')
    rotation=[]
    for n in orders:
        K=field(s.Poly(s.cyclotomic_poly(F*n,t),t));z=K.unit;degree=K.mod.degree();embed=lambda v:evaluate(v.to_list(),z**n,K);NUn={m:[[embed(v) for v in row] for row in nu[m]] for m in s.divisors(n)}
        @lru_cache(None)
        def subfield(m):
            B=s.Matrix.hstack(*[vector(z**(F*(n//m)*j),degree) for j in range(int(s.totient(m)))]);piv=list(B.T.rref()[1]);return B,piv,B[piv,:].inv()
        vals=[]
        for b in range(r):
            rows=[]
            for a in range(len(R)):
                dimension=sum(W[b][k]*powers[a,n][k] for k in range(len(R)));traces=[K(dimension)]
                for k in range(1,n):
                    g=math.gcd(n,k);m=n//g;x=z**(ee[b]*g)*sum((K(powers[a,g][i])*NUn[m][b][i] for i in range(len(R))),K.zero);B,piv,inv=subfield(m);xx=vector(x,degree);co=inv*xx[piv,:];require(B*co==xx,'generalized trace outside its cyclic field');traces.append(sum((K(v)*z**(F*k*j) for j,v in enumerate(co)),K.zero))
                row=[]
                for j in range(n):
                    value=sum((traces[k]*z**((-F*j*k)%(F*n)) for k in range(n)),K.zero)/K(n);co=value.to_list();require(len(co)<=1 and (not co or co[0].denominator==1 and co[0]>=0),'nonintegral/negative generalized rotation eigenspace');row.append(int(co[0]) if co else 0)
                require(sum(row)==dimension,'wrong total eigenspace dimension');rows.append(row)
            vals.append(rows)
        rotation.append(dict(order=n,spaces=r*len(R),multiplicities_sha256=digest(vals)))
    return dict(higher_gauss=gauss,galois=galois,generalized_rotations=rotation,passed=True,categorification_claimed=False)


def reconstruct(progress=None):
    out=[]
    for rid in ['R6_4_22','R6_4_91']:
        R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==rid);cert=json.load(open(ROOT/f'research/round5/quartic_pair/{rid}_center_reconstruction.json'))['certificate'];variants=[]
        for data,label,W,ds,S,ee in centers(rid,cert,R):
            checks=check_variant(R,data,W,ds,S,ee,list(range(2,17)));variants.append(dict(label=label,checks=checks))
            if progress:progress(rid,label)
        out.append(dict(id=rid,source_sha256=digest(cert),variants=variants))
    return dict(kind='quartic_modular_finite_checks',version=1,results=out,categorification_claimed=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    if a.verify:
        import scipy.optimize
        def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied
    st=time.monotonic();cert=reconstruct(lambda *x:print(x,flush=True))
    if a.verify:require(cert==json.load(open(a.output)),'modular checks differ')
    else:a.output.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print(json.dumps(dict(passed=True,optimizer_used=False,variants=sum(len(x['variants']) for x in cert['results']),seconds=time.monotonic()-st)),flush=True)
