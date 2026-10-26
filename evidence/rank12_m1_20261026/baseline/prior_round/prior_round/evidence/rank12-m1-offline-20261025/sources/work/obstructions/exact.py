"""Exact arithmetic. No floating-point value assigns a classification status."""
from functools import lru_cache
import sympy as s

t,z=s.symbols('t z')
class VerificationError(RuntimeError): pass

def require(test,message='certificate condition failed'):
    if not test: raise VerificationError(message)

def pc(p): return [str(v) for v in s.Poly(p,t).all_coeffs()]
def poly(c): return s.Poly.from_list([s.Rational(v) for v in c],t,domain=s.QQ)
def ec(a): return [str(s.Rational(v)) for v in a.to_list()]
def key(a): return tuple(s.Rational(v) for v in a.to_list())
def field(p): return s.QQ.alg_field_from_poly(p,alias='a')
def vector(a,d):
    c=list(key(a));return s.Matrix(list(reversed([s.S.Zero]*(d-len(c))+c)))
def evaluate(co,a,K):
    v=K.zero
    for c in co:v=v*a+K(s.Rational(c))
    return v

class Embedding:
    """Sign evaluation by rational interval refinement at a real root."""
    def __init__(self,p,interval):
        self.p=p;self.lo,self.hi=map(s.Rational,interval);self.cache={}
        require(self.lo==self.hi or p.count_roots(self.lo,self.hi)==1,'invalid isolating interval')
    def sign(self,a):
        if not a:return 0
        co=key(a)
        if co in self.cache:return self.cache[co]
        for _ in range(256):
            l=h=s.S.Zero
            for c in co:
                v=(l*self.lo,l*self.hi,h*self.lo,h*self.hi)
                l,h=min(v)+c,max(v)+c
            if l>0 or h<0:
                ans=1 if l>0 else -1;self.cache[co]=ans;return ans
            require(self.lo!=self.hi,'zero evaluation of nonzero field element')
            self.lo,self.hi=self.p.refine_root(self.lo,self.hi,steps=6)
        raise VerificationError('root-refinement safety limit')

def embeddings(p):
    return [Embedding(p,a) for a,m in p.intervals(eps=s.Rational(1,10**8))]

@lru_cache(maxsize=None)
def factors(co):return tuple(poly(co).factor_list()[1])
@lru_cache(maxsize=None)
def mod_factors(co,r):return tuple((q.degree(),m) for q,m in poly(co).set_modulus(r).factor_list()[1])

def norm_failure(p,required):
    d,n=p.degree(),abs(int(p.TC()));require(n>0,'zero norm')
    v=s.factorint(n)
    for q,m in required:
        for r,w in s.factorint(abs(int(q.TC()))).items():
            if int(v.get(r,0))*q.degree()<int(w)*d:
                return {'kind':'norm','polynomial':pc(q),'prime':int(r)}
    return None

def check_norm(p,required,c):
    q=poly(c['polynomial']);r=c['prime']
    require(any(q==g for g,m in required),'unrelated norm factor');require(s.isprime(r),'nonprime witness')
    def val(n):
        n=abs(int(n));v=0;require(n>0,'zero norm')
        while n%r==0:n//=r;v+=1
        return v
    require(val(p.TC())*q.degree()<val(q.TC())*p.degree(),'norm condition not violated')

def field_failure(p,required,limit=1000):
    for q,m in required:
        if p.degree()%q.degree():return {'kind':'field_degree','polynomial':pc(q)}
    for r in s.primerange(2,limit):
        if not all(d==1 and m==1 for d,m in mod_factors(tuple(pc(p)),int(r))):continue
        for q,m in required:
            if any(d>1 for d,m in mod_factors(tuple(pc(q)),int(r))):
                return {'kind':'field_prime','polynomial':pc(q),'prime':int(r)}
    return None

def check_field(p,required,c):
    q=poly(c['polynomial']);require(any(q==g for g,m in required),'unrelated field factor')
    if c['kind']=='field_degree':require(p.degree()%q.degree()!=0,'field degree condition not violated')
    else:
        r=c['prime'];require(s.isprime(r),'nonprime field witness')
        require(all(d==1 and m==1 for d,m in mod_factors(tuple(pc(p)),r)),'defining polynomial not split squarefree')
        require(any(d>1 for d,m in mod_factors(tuple(pc(q)),r)),'required polynomial also splits')

def cyclotomic_failure(polys,limit=120):
    for i,p in enumerate(polys):
        for q,m in p.factor_list()[1]:
            if q.degree()<3:continue
            for r in s.primerange(2,limit):
                a=mod_factors(tuple(pc(q)),int(r))
                if all(m==1 for d,m in a) and len({d for d,m in a})>1:
                    return {'kind':'cyclotomic','matrix':i,'polynomial':pc(q),'prime':int(r)}
    return None

def check_cyclotomic(polys,c):
    q=poly(c['polynomial']);r=c['prime'];p=polys[c['matrix']]
    require(q.is_irreducible and p.rem(q).is_zero,'invalid irreducible factor')
    require(s.isprime(r),'nonprime witness');a=mod_factors(tuple(pc(q)),r)
    require(all(m==1 for d,m in a) and len({d for d,m in a})>1,'cycle lengths compatible with abelianity')

def discover_roots(p,K):
    """Discovery only; checking multiplies all the proposed linear factors."""
    _,fac=s.Poly.from_list(p.all_coeffs(),z,domain=K).rep.factor_list()
    if any(g.degree()!=1 for g,m in fac):return None
    out=[]
    for g,m in fac:
        a,b=g.to_list();out.extend([-b/a]*m)
    return sorted(out,key=key)

def check_roots(p,K,roots):
    co=[K.one]
    for a in roots:
        out=[K.zero]*(len(co)+1)
        for i,v in enumerate(co):out[i]+=v;out[i+1]-=v*a
        co=out
    require(co==[K(s.Rational(a)) for a in p.all_coeffs()],'wrong or incomplete roots')
