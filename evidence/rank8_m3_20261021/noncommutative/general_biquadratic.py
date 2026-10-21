"""Additive relative-trace adapter for coprime squarefree biquadratic fields."""
from pathlib import Path
import itertools,json,math,sys,time
from fractions import Fraction as F
from types import SimpleNamespace
import biquadratic_traces as bq
from exact import vector,discover_roots,check_roots,ec
from proofs import multiplication_matrix
from rings import Characters,codegree_poly
from induction import low_matrices
from scalar_sieve import ScalarCharacters
sys.path.insert(0,str(Path(__file__).parent.parent/'performance'))
import low_frames_rank8
low_frames_rank8.install()
s=bq.s;require=bq.require
Q1=Q2=None;PRIMES=None


def conductor(q):return q if q%4==1 else 4*q


def configure(q,r):
    global Q1,Q2
    require(q>1 and r>1 and math.gcd(q,r)==1 and all(e==1 for e in s.factorint(q*r).values()),'coprime squarefree radicands required')
    Q1=q;Q2=r


def mul(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i^j]+=x*y*(Q1 if i&j&1 else 1)*(Q2 if i&j&2 else 1)
    return tuple(out)


def trace_types(height,orders=None,powers=None):
    if powers is None:powers=list(range(1,height+1))
    conductors=[conductor(Q1),conductor(Q2),conductor(Q1*Q2)]
    if orders is None:
        require(PRIMES is not None,'dimension prime support not initialized')
        bound=1
        for p in PRIMES:
            c=max([1]+[int(s.factorint(f).get(p,0)) for f in conductors]);e=0
            while p**(e+1)<=height:e+=1
            bound*=p**(c+e)
        orders=s.divisors(bound);out={tuple((F(0),)*4 for k in powers)}
    else:bound=None;out=set()
    for order in orders:
        order=int(order)
        for sign1,sign2 in itertools.product((-1,1),repeat=2):
            values=[]
            for k in powers:
                g=math.gcd(order,k);n=order//g;phi=int(s.totient(n));a=[F(int(s.mobius(n)),phi)]
                for q,f,sign in zip([Q1,Q2,Q1*Q2],conductors,[sign1,sign2,sign1*sign2]):
                    z=n//f;v=F(0)
                    if n%f==0 and math.gcd(z,f)==1:
                        v=F(sign*int(s.mobius(z))*int(s.kronecker_symbol(f,z))*int(s.kronecker_symbol(f,k//g))*math.isqrt(f//q),phi)
                    a.append(v)
                values.append(tuple(a))
            out.add(tuple(values))
    return sorted(out),bound


def spectral(R):
    if any(R[i][j]!=R[j][i] for i in range(8) for j in range(i)):return bq.w.spectral(R)
    ch=Characters(R);f,K,ds,D,pD,e=ch.fp();roots=discover_roots(codegree_poly(R),K)
    require(roots is not None,'formal codegrees do not split');check_roots(codegree_poly(R),K,roots)
    require(D in roots and len(roots)==8,'incomplete scalar codegrees');roots.remove(D)
    return dict(n=8,N=ch.N,du=ch.du,generator=ch.k,factor=f,K=K,ds=ds,D=D,embedding=e,
                Casimir=ch.C,Gram=ch.C,codegrees=[D]+roots,multiplicities=[1]*8)


def data(R):
    global PRIMES
    a=spectral(R);K=a['K'];f=a['factor'];e=a['embedding'];require(f.degree()==4,'quartic FP field required')
    roots=[]
    for q in (Q1,Q2):
        rr=discover_roots(s.Poly(bq.w.t*bq.w.t-q,bq.w.t),K)
        require(rr is not None and len(rr)==2,'required quadratic subfield absent')
        roots.append(next(x for x in rr if e.sign(x)>0))
    V=s.Matrix.hstack(*(vector(x,4) for x in [K.one,roots[0],roots[1],roots[0]*roots[1]]));require(V.det()!=0,'singular field basis');inv=V.inv()
    def coords(x):return tuple(F(str(c)) for c in inv*vector(x,4))
    norm=multiplication_matrix(a['D'],K,f).det();require(norm.q==1,'nonintegral dimension norm')
    PRIMES=sorted(map(int,s.factorint(abs(int(norm)))))
    require(set(s.factorint(math.lcm(conductor(Q1),conductor(Q2))))<=set(PRIMES),'field conductor outside exponent prime support')
    cs=[bq.w.core.restriction(a['ds'],a['D']/fc,r,K,a['Gram']) for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:])]
    if len(cs)==7:
        import induction
        lows=induction.low_matrices(cs,a['Gram'],gram_prune=True)
    else:lows=bq.low_frames(cs,a['multiplicities'][1:],a['Gram'])
    return dict(a,coords=coords,dimensions=list(map(coords,a['ds'])),global_dimension=coords(a['D']),columns=cs,lows=lows)


bq.data=data;bq.mul=mul;bq.trace_types=trace_types


def sphere(R):
    from scalar_sieve import character_obstructions
    from proofs import positive_sign_embedding
    a=ScalarCharacters(R);fp=spectral(R)['factor'];branches=character_obstructions(R,a.cf)
    for (f,m),b in zip(a.components,branches):
        if b['obstruction'] is not None:continue
        K,ds,D,pD=a.component(f);b['obstruction']={'kind':'galois_fp'} if f==fp else positive_sign_embedding(R,f,ds)
    return branches


def lift(R,pseudo):
    import biquadratic_lift as bl
    original=bl.sphere;bl.sphere=sphere
    try:return bl.discover(R,pseudo)
    finally:bl.sphere=original


def verify(R,c):
    require(c['kind']=='rank8_general_biquadratic_lift','wrong generalized biquadratic proof')
    configure(*c['radicands']);expected,report=lift(R,c['pseudo'])
    require(expected is not None,'general signed branches survive')
    expected['kind']='rank8_general_biquadratic_lift';expected['radicands']=list(c['radicands'])
    require(expected==c,'general biquadratic proof changed')


if __name__=='__main__':
    base=Path(__file__).parent;rows=json.loads((base.parent/'pipeline/survivors_m3.json').read_text())
    families={'R8_3_901':(3,5),'R8_3_1463':(3,5),'R8_3_347':(3,7),'R8_3_448':(3,7),'R8_3_455':(3,13)};out=[]
    for r in rows:
        if r['id'] not in families or len(sys.argv)>1 and r['id']!=sys.argv[1]:continue
        configure(*families[r['id']]);start=time.monotonic()
        try:
            pseudo,report=bq.discover(r['tensor'],4)
            c,lr=lift(r['tensor'],pseudo) if pseudo else (None,None)
            if c:c['kind']='rank8_general_biquadratic_lift';c['radicands']=list(families[r['id']]);verify(r['tensor'],c)
            item={'id':r['id'],'outcome':'excluded' if c else 'no_conclusion','certificate':c,'report':report,'lift_report':lr}
        except Exception as e:item={'id':r['id'],'outcome':'error','error':type(e).__name__+': '+str(e)}
        item['radicands']=list(families[r['id']]);item['seconds']=round(time.monotonic()-start,3);out.append(item)
        (base/('general_biquadratic_results.json' if len(sys.argv)==1 else f'general_biquadratic_{r["id"]}.json')).write_text(json.dumps(out,indent=2)+'\n')
        print(r['id'],item['outcome'],item['seconds'],flush=True)
