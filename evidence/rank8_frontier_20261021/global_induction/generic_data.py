"""Isolated exact data for coprime biquadratic relative-trace cones.

The formulas are the published general_biquadratic formulas, bound to an
immutable Field object rather than module-global radicands/prime support.
No published module is reconfigured by this adapter.
"""
import itertools,math
from fractions import Fraction as Q
from types import SimpleNamespace
import streaming as st
from exact import require,vector,discover_roots,check_roots
from rings import Characters,codegree_poly
from proofs import multiplication_matrix
s=st.old.s

class Field:
    def __init__(self,q,r,primes):
        require(q>1 and r>1 and math.gcd(q,r)==1 and all(e==1 for e in s.factorint(q*r).values()),'coprime squarefree radicands required')
        self.q=q;self.r=r;self.primes=tuple(primes)
    @staticmethod
    def conductor(q):return q if q%4==1 else 4*q
    def mul(self,a,b):
        out=[Q(0)]*4
        for i,x in enumerate(a):
            for j,y in enumerate(b):out[i^j]+=x*y*(self.q if i&j&1 else 1)*(self.r if i&j&2 else 1)
        return tuple(out)
    def traces(self,height,orders=None,powers=None):
        if powers is None:powers=list(range(1,height+1))
        qs=[self.q,self.r,self.q*self.r];fs=list(map(self.conductor,qs))
        if orders is None:
            bound=1
            for p in self.primes:
                c=max([1]+[int(s.factorint(f).get(p,0)) for f in fs]);e=0
                while p**(e+1)<=height:e+=1
                bound*=p**(c+e)
            orders=s.divisors(bound);out={tuple((Q(0),)*4 for k in powers)}
        else:bound=None;out=set()
        for order in orders:
            order=int(order)
            for sign1,sign2 in itertools.product((-1,1),repeat=2):
                values=[]
                for k in powers:
                    g=math.gcd(order,k);n=order//g;phi=int(s.totient(n));a=[Q(int(s.mobius(n)),phi)]
                    for q,f,sign in zip(qs,fs,[sign1,sign2,sign1*sign2]):
                        z=n//f;v=Q(0)
                        if n%f==0 and math.gcd(z,f)==1:v=Q(sign*int(s.mobius(z))*int(s.kronecker_symbol(f,z))*int(s.kronecker_symbol(f,k//g))*math.isqrt(f//q),phi)
                        a.append(v)
                    values.append(tuple(a))
                out.add(tuple(values))
        return sorted(out),bound
    def rotations(self,order,rs):return self.traces(order,s.divisors(order),rs)[0]

def setup(R,q=3,r=5):
    import rank8_signed_bridge
    rank8_signed_bridge.install()
    import biquadratic_traces as bq
    require(len(R)==8 and all(R[i][j]==R[j][i] for i in range(8) for j in range(8)),'commutative rank8 required')
    ch=Characters(R);f,K,ds,D,pD,e=ch.fp();require(f.degree()==4,'quartic FP field required')
    roots=discover_roots(codegree_poly(R),K);require(roots is not None,'formal codegrees do not split');check_roots(codegree_poly(R),K,roots)
    require(D in roots and len(roots)==8,'incomplete formal codegrees');roots.remove(D)
    radicals=[];t=s.Symbol('t')
    for n in (q,r):
        rr=discover_roots(s.Poly(t*t-n,t),K);require(rr is not None and len(rr)==2,'required radical absent');radicals.append(next(x for x in rr if e.sign(x)>0))
    V=s.Matrix.hstack(*(vector(x,4) for x in [K.one,radicals[0],radicals[1],radicals[0]*radicals[1]]));require(V.det()!=0,'singular radical basis');inv=V.inv()
    def coords(x):return tuple(Q(str(c)) for c in inv*vector(x,4))
    norm=multiplication_matrix(D,K,f).det();require(norm.q==1,'nonintegral dimension norm');primes=sorted(map(int,s.factorint(abs(int(norm)))))
    field=Field(q,r,primes);require(set(s.factorint(math.lcm(field.conductor(q),field.conductor(r))))<=set(primes),'field conductor outside exponent prime support')
    columns=[bq.w.core.restriction(ds,D/fc,1,K,ch.C) for fc in roots]
    a=dict(n=8,N=ch.N,du=ch.du,generator=ch.k,factor=f,K=K,ds=ds,D=D,embedding=e,Casimir=ch.C,Gram=ch.C,B=ch.C,codegrees=[D]+roots,multiplicities=[1]*8,coords=coords,dimensions=list(map(coords,ds)),global_dimension=coords(D),columns=columns,lows=[],width=4,mul=field.mul,traces=field.traces,rotations=field.rotations,field={'degree':4,'radicands':[q,r],'primes':primes})
    a['high']=st.old.biquadratic_high(a,SimpleNamespace(native=bq.native,mul=field.mul))
    require(all(columns),'empty low restriction set');return a
