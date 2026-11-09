#!/usr/bin/env python3
"""Second implementation of spherical arithmetic and finite central checks.

No production modules are imported. Characters use spectral adjugates, norms
use resultants, and nonabelian codegrees are detected by nonsplitting in a
root field, instead of a Galois-group algorithm. Induction rows are enumerated
in full integer boxes. This is exact
computational verification, not a formalization of the categorical theorems.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import time
import sympy as s

x=s.Symbol('x')

def require(test,message='independent check failed'):
    if not test:raise RuntimeError(message)

def pol(v):return s.Poly.from_list(list(map(s.Rational,v)),x,domain=s.QQ)

def enc(e,degree):
    c=list(map(s.Rational,e.to_list()))
    return (s.S.Zero,)*(degree-len(c))+tuple(c)

def eval_poly(p,a,K):
    v=K.zero
    for c in p.all_coeffs():v=v*a+K(c)
    return v

class RealPlace:
    def __init__(self,f,interval):self.f=f;self.lo,self.hi=interval
    def sign(self,z):
        if not z:return 0
        for _ in range(32):
            a=b=s.S.Zero
            for v in enc(z,self.f.degree()):
                products=(a*self.lo,a*self.hi,b*self.lo,b*self.hi)
                a=min(products)+v;b=max(products)+v
            if a>0:return 1
            if b<0:return -1
            require(self.lo!=self.hi,'unexpected zero evaluation')
            self.lo,self.hi=self.f.refine_root(self.lo,self.hi,eps=(self.hi-self.lo)/1000)
        raise RuntimeError('sign isolation failed; no numerical fallback')

def places(f):
    return [RealPlace(f,iv) for iv,m in f.intervals(eps=s.Rational(1,10**24))]

def characters(R,k):
    N=list(map(s.Matrix,R));H=N[0]+N[1]+k*N[2]+k*k*N[3]
    p=H.charpoly(x).as_poly().set_domain(s.QQ)
    require(s.gcd(p,p.diff()).degree()==0,'nonseparating character generator')
    adj=(x*s.eye(4)-H).adjugate()
    numer=[s.Poly(s.trace(n*adj),x,domain=s.QQ) for n in N]
    B=sum((n*n.T for n in N),s.zeros(4))
    du=[next(j for j in range(4) if R[i][j][0]==1) for i in range(4)]
    result=[]
    for f,m in p.factor_list()[1]:
        require(m==1,'repeated character factor')
        K=s.QQ.alg_field_from_poly(f);inv=s.invert(p.diff(),f)
        ds=[K((v*inv).rem(f).all_coeffs()) for v in numer]
        require(ds[0]==K.one,'incorrect unit character')
        D=sum((ds[i]*ds[du[i]] for i in range(4)),K.zero)
        result.append((f,K,ds,D))
    return N,B,du,result

@lru_cache(maxsize=None)
def nonsplit_in_root_field(coefficients):
    """A degree-three/four irreducible has abelian Galois group iff normal.

    A transitive abelian permutation group is regular. Conversely, a normal
    root field of degree three or four has Galois group of order three or
    four, hence abelian. Factoring in the root field therefore decides the
    required alternative without calling the production Galois-group code.
    """
    q=pol(coefficients);K=s.QQ.alg_field_from_poly(q)
    lifted=s.Poly.from_list(q.all_coeffs(),x,domain=K)
    unit,factors=lifted.factor_list()
    product=s.Poly(unit,x,domain=K)
    for factor,multiplicity in factors:product*=factor**multiplicity
    require(product==lifted,'incomplete independent root-field factorization')
    return any(factor.degree()>1 for factor,multiplicity in factors)

def check_nonabelian_witness(cp,why):
    q=pol(why['factor'])
    require(q.degree() in (3,4),'invalid nonabelian factor degree')
    require(q.is_irreducible and cp.rem(q).is_zero,
            'unrelated nonabelian codegree factor')
    require(nonsplit_in_root_field(tuple(q.all_coeffs())),
            'codegree root field is normal, hence abelian')

def verify(pair):
    row,rec=pair;R=row['tensor'];c=rec['certificate'];pseudo=c.get('pseudo')
    require(row['id']==rec['id'],'record identity mismatch')
    N,B,du,components=characters(R,c['generator'])
    cp=B.charpoly(x).as_poly().set_domain(s.QQ)
    require(len(components)==len(c['characters']),'missing character branches')
    counts=Counter();fp=None
    for f,K,ds,D in components:
        for e in places(f):
            if all(e.sign(z)>0 for z in ds):
                require(fp is None,'multiple positive characters');fp=(f,K,ds,D,e)
    require(fp is not None,'no positive character')
    fp_factors=[q for q,m in cp.factor_list()[1] if not eval_poly(q,fp[3],fp[1])]
    require(len(fp_factors)==1,'ambiguous FP global-dimension polynomial')
    for (f,K,ds,D),b in zip(components,c['characters']):
        require(f==pol(b['factor']),'wrong character factor')
        why=b['obstruction'];require(isinstance(why,dict),'missing character obstruction')
        kind=why['kind'];counts['orbit_'+kind]+=1
        if kind=='zero':require(ds[why['object']]==K.zero,'dimension is nonzero')
        elif kind=='duality':require(ds[why['object']]!=ds[du[why['object']]],'dual dimensions agree')
        elif kind=='norm':
            q=pol(why['polynomial']);prime=why['prime']
            require(s.isprime(prime),'nonprime norm witness')
            require(cp.rem(q).is_zero and q.is_irreducible,'unrelated norm factor')
            delta=pol(D.to_list());norm=abs(s.resultant(f,delta))
            require(norm.is_Integer and norm>0,'zero or nonintegral norm')
            def valuation(n):
                n=abs(int(n));v=0;require(n>0,'zero norm')
                while n%prime==0:n//=prime;v+=1
                return v
            require(valuation(norm)*q.degree()<valuation(q.TC())*f.degree(),
                    'norm inequality is not violated')
        elif kind=='spherical_first_moment':
            require(all(ds[i]==ds[du[i]] for i in range(4)),'not a spherical character')
            ee=places(f);idx=why['embedding']
            require(type(idx) is int and 0<=idx<len(ee),'invalid real embedding')
            w=s.trace(B.inv()**2);gap=K(2*w)*D-D-K.one
            require(str(w)==why['inverse_square_sum'] and ee[idx].sign(gap)>0
                    and gap==K(list(map(s.Rational,why['gap']))),'first-moment bound survives')
        elif kind=='nonabelian_codegrees':check_nonabelian_witness(cp,why)
        elif kind=='galois_global_dimension':
            require(not eval_poly(fp_factors[0],D,K),'global dimensions are not Galois conjugate')
        else:raise RuntimeError('unknown spherical witness: '+kind)
    used=counts['orbit_galois_global_dimension']>0
    require(not used or pseudo is not None,'FP orbit has no exclusion proof')
    require(used or pseudo is None,'unused positive-dimension proof')
    if pseudo is None:return dict(counts)
    f,K,ds,D,e=fp
    require(pseudo['kind']=='induction' and f==pol(pseudo['fp_factor'])
            and pseudo['generator']==c['generator'],'wrong induction character')
    roots=[K(list(map(s.Rational,r))) for r in pseudo['roots']]
    coeff=[K.one]
    for r in roots:
        new=[K.zero]*(len(coeff)+1)
        for i,v in enumerate(coeff):new[i]+=v;new[i+1]-=r*v
        coeff=new
    require(coeff==[K(v) for v in cp.all_coeffs()],'incomplete codegree roots')
    require(D in roots,'missing FP codegree');roots.remove(D)
    degree=f.degree();vectors=[enc(z,degree) for z in ds[1:]]
    scale=s.ilcm(*[int(v.q) for rowv in vectors for v in rowv])
    vectors=[tuple(int(scale*v) for v in rowv) for rowv in vectors]
    targets=[tuple(scale*v for v in enc(D/r-K.one,degree)) for r in roots]
    bounds=[min(int(B[0,i]),math.isqrt(int(B[i,i]))) for i in range(1,4)]
    cs=[[] for _ in roots]
    for v in itertools.product(*(range(b+1) for b in bounds)):
        total=tuple(sum(v[j]*vectors[j][h] for j in range(3)) for h in range(degree))
        for z,target in enumerate(targets):
            if total==target:cs[z].append((1,)+v)
    counts['full_box_columns_tested']+=math.prod(b+1 for b in bounds)
    require(list(map(len,cs))==pseudo['column_counts'],'induction-row enumeration differs')
    low=[];unquotiented=0
    for columns in itertools.product(*cs):
        cols=((1,0,0,0),)+columns
        if not all(sum(v[i] for v in cols)==B[0,i] for i in range(4)):continue
        unquotiented+=1
        # Canonicalize each equal-formal-codegree block, independently of production.
        canonical=list(columns)
        for r in set(roots):
            indices=[j for j,v in enumerate(roots) if v==r]
            ordered=sorted(columns[j] for j in indices)
            for j,v in zip(indices,ordered):canonical[j]=v
        if tuple(canonical)==columns:low.append(cols)
    counts['unquotiented_low_choices']+=unquotiented
    require(len(low)==pseudo['low_count']==len(pseudo['failures']),'missing low branches')
    recorded={tuple(map(tuple,b['columns'])):b['obstruction'] for b in pseudo['failures']}
    require(set(low)==set(recorded) and len(recorded)==len(low),'duplicated or wrong low branches')
    for cols in low:
        why=recorded[cols];require(isinstance(why,dict),'missing local witness')
        kind=why['kind'];i=why['object']
        require(type(i) is int and 1<=i<4,'invalid row object')
        L=s.Matrix(cols);G=L.T*L;Q=B-G
        W=[sum((K(G[i,j])*ds[j] for j in range(4)),K.zero) for i in range(4)]
        if kind=='polynomial_row':
            require(why['nonselfdual']==(du[i]!=i),'wrong row duality')
            gap=K(3)*W[i]-D*ds[i] if du[i]!=i else K(9)*W[i]-D*(K(3)*ds[i]+K(2))
        elif kind=='third_indicator_row':
            gap=K(36)*W[i]-D*(K(10)*ds[i]+K(8)+K(2*R[i][i][du[i]]))
        elif kind=='fourth_indicator_row':
            m=why.get('floor')
            require(type(m) is int,'invalid fourth-indicator floor')
            # Certify the supplied integer directly, independently of the
            # producer's floor search and without a numerical approximation.
            numerator=K(10)*ds[i]+K(71 if du[i]==i else 0)+K(30*R[i][i][du[i]])
            require(e.sign(numerator-K(9*m))>=0
                    and e.sign(K(9*(m+1))-numerator)>0,
                    'incorrect fourth-indicator floor')
            gap=K(32)*W[i]-D*(K(7)*ds[i]+K(m))
        elif kind=='involution_moment':
            g=why['involution']
            require(type(g) is int and 1<=g<4 and g!=i and du[g]==g
                    and ds[g]==K.one and Q[g,g]==2,'involution hypotheses fail')
            require(D/K(2)-W[g]==K.one and e.sign(W[g])>0,'wrong involution mass')
            gap=K(2)*W[i]+D*K(Q[g,i])-D*(ds[i]+K.one)
        else:raise RuntimeError('unknown local witness: '+kind)
        require(e.sign(gap)>0 and gap==K(list(map(s.Rational,why['gap']))),'local inequality survives')
        counts['low_'+kind]+=1
    counts['induction_certificates']+=1
    return dict(counts)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--workers',type=int,default=4)
    a=p.parse_args();start=time.monotonic();root=a.archive/'supplementary'
    rows=list(map(json.loads,(root/'census/data/rings.jsonl').read_text().splitlines()))
    certs=list(map(json.loads,(root/'classification/results/certificates.jsonl').read_text().splitlines()))
    require(len(rows)==len(certs) and all(r['id']==c['id'] for r,c in zip(rows,certs)),'ledger coverage differs')
    pairs=[(r,c) for r,c in zip(rows,certs) if c['stage'] in ('spherical_arithmetic','central_induction')]
    counts=Counter()
    with multiprocessing.Pool(a.workers) as pool:
        for c in pool.imap_unordered(verify,pairs,chunksize=2):counts.update(c)
    result={'passed':True,'spherical_records':len(pairs),
            'arithmetic_records':sum(c['stage']=='spherical_arithmetic' for r,c in pairs),
            'central_records':sum(c['stage']=='central_induction' for r,c in pairs),
            'counts':dict(sorted(counts.items())),'seconds':round(time.monotonic()-start,3),
            'independence':'No production imports; spectral-adjugate characters; resultant norms; independent root-field nonsplitting for nonabelian degree-three/four codegrees; full integer boxes and full products of induction rows before equal-formal-codegree quotienting; fourth-indicator floors checked by exact numerator inequalities.'}
    print(json.dumps(result,indent=2))
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
