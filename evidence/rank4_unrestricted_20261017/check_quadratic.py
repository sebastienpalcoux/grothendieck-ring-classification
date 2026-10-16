def _require(condition, message):
    if not condition:
        raise RuntimeError(message)

from itertools import product,permutations
from math import isqrt,gcd
from fractions import Fraction
from functools import reduce, cmp_to_key
import json

def sf(d):return all(d%(p*p) for p in range(2,isqrt(d)+1))
def canon(t,s):
    out=[]
    for sig in (1,-1):
        for perm in permutations(range(3)):
            ts=[]
            for i in perm:
                ti,si=t[i],sig*s[i]
                if si<0 or si==0 and ti<0:ti,si=-ti,-si
                ts.append((si,ti))
            out.append(tuple(ts))
    return min(out)

def rows():
    out={}
    for d in range(2,50):
        if not sf(d):continue
        for s in product(range(isqrt(99//d)+1),repeat=3):
            if tuple(sorted(s))!=s or sum(x!=0 for x in s)<2:continue
            J=sum(x*x for x in s)
            if not 0<d*J<100:continue
            if d%4!=1 and any(x%2 for x in s):continue
            tt=d*J-4
            if tt<0:continue
            r=isqrt(tt)
            for t0,t1 in product(range(-r,r+1),repeat=2):
                t2q=tt-t0*t0-t1*t1
                if t2q<0:continue
                t2=isqrt(t2q)
                if t2*t2!=t2q:continue
                for x in set((t2,-t2)):
                    t=(t0,t1,x)
                    if d%4!=1 and any(x%2 for x in t):continue
                    if d%4==1 and any((x-y)%2 for x,y in zip(s,t)):continue
                    if any(ti<0 for ti,si in zip(t,s) if si==0):continue
                    C=sum(a*b for a,b in zip(t,s));L=Fraction(d*d*J*J-d*C*C,4)
                    if L.denominator!=1:continue
                    L=int(L)
                    if not d*J<L<100 or (d*J)**2%L:continue
                    k=(d,canon(t,s))
                    if k not in out:
                        P=[Fraction(d*(J*ti-C*si),2*L) for ti,si in zip(t,s)]
                        den=1
                        for p in P:den=den*p.denominator//gcd(den,p.denominator)
                        U=[int(p*den) for p in P];gg=reduce(gcd,U)
                        U=[x//gg for x in U]
                        out[k]={'d':d,'t':t,'s':s,'L':L,'ell':str(Fraction(d*J,L)),'normU':sum(x*x for x in U)}
    return out
chart=[(5,(2,-1,-1),(0,1,1),20,'1/2',1),(5,(2,-1,1),(0,1,1),25,'2/5',6),(5,(-3,-1,-1),(1,1,1),25,'3/5',6),(2,(2,-2,-2),(0,2,2),32,'1/2',1),(3,(0,-4,-2),(0,2,2),36,'2/3',2),(5,(-3,-1,1),(1,1,1),45,'1/3',2),(5,(-3,-1,-4),(1,1,2),45,'2/3',2),(13,(2,-3,-3),(0,1,1),52,'1/2',1),(2,(2,-2,2),(0,2,2),64,'1/4',3),(2,(-2,-2,-6),(2,2,4),64,'3/4',3),(2,(-4,-2,0),(2,2,2),72,'1/3',2),(5,(2,-4,-4),(0,2,2),80,'1/2',1),(3,(2,-4,0),(0,2,2),96,'1/4',3),(3,(-4,-4,-6),(2,2,4),96,'3/4',3)]
actual=rows();expected={(d,canon(t,s)):(L,ell,nU) for d,t,s,L,ell,nU in chart}
_require(actual.keys()==expected.keys(), (set(actual)-set(expected),set(expected)-set(actual)))
for k,v in actual.items():_require((v['L'],v['ell'],v['normU'])==expected[k], 'check_quadratic.py exact check at source line 58')
# k,t0 list in the h=3 codegree-two branch.
kt=[]
for k in range(1,7):
    for t in range(k+2,8):
        disc=t*t-4*k
        v=0
        while disc%3==0:disc//=3;v+=1
        if v%2:kt.append((k,t))
_require(kt==[(1,4),(1,5),(3,6),(4,7)], kt)
out={'status':'PASS','short_character_rows':len(actual),'rows':list(actual.values()),'codegree_two_kt_chart':kt}
out['arithmetic_chart_status']='PASS'
import sympy as S
P=S.symbols('a b c d e f g h i j');a,b,c,d,e,f,g,h,i,j=P
T={(1,1):(1,a,b,c),(1,2):(0,b,d,e),(1,3):(0,c,e,f),(2,2):(1,d,g,h),(2,3):(0,e,h,i),(3,3):(1,f,i,j)}
def char_equations(row,rad=None):
    eq=[]
    for (i,j),coeff in T.items():
        pol=S.expand(sum(x*y for x,y in zip(coeff,row))-row[i]*row[j])
        if rad is None:eq.append(pol)
        else:
            z=S.Symbol('z'); pp=S.Poly(pol.subs(S.sqrt(rad),z),z)
            rem=pp.rem(S.Poly(z*z-rad,z));eq.extend(rem.all_coeffs())
    return eq

def normalform(rows,rad=None):return list(S.linsolve(sum((char_equations(r,rad) for r in rows),[]),P))[0]
_require(normalform([(1,0,1,-1),(1,1,-1,0)])==(j-2,j-2,j-1,j-1,j-1,j-1,j-1,j-1,j,j), 'check_quadratic.py exact check at source line 84')
phi=(1+S.sqrt(5))/2;phip=(1-S.sqrt(5))/2
_require(normalform([(1,-1,phi,phip),(1,-1,phip,phi)],5)==(j,j,j,j-1,j,j-1,j,j-1,j-1,j), 'check_quadratic.py exact check at source line 86')
_require(normalform([(1,1,1,0),(1,-1,0,2)])==(8*j-8,8-8*j,4*j-4,8*j-7,4-4*j,2*j-3,7-8*j,4*j-4,2-2*j,j), 'check_quadratic.py exact check at source line 87')
# The codegree-two table restrictions from each rational character row.
aa,bb,cc,dd=S.symbols('aa bb cc dd');x,y=S.symbols('x y')
T2={(1,1):(1,0,0,0),(1,2):(0,0,1,0),(1,3):(0,0,0,1),(2,2):(1,1,aa,bb),(2,3):(0,0,bb,cc),(3,3):(1,1,cc,dd)}
def form2(r,t):
    row=(1,1,r,t)
    eq=[sum(x*y for x,y in zip(v,row))-row[i]*row[j] for (i,j),v in T2.items()]
    return list(S.linsolve(eq,(aa,bb,cc,dd)))[0]
_require(form2(1,-1)==(dd-3,dd-2,dd-1,dd), 'check_quadratic.py exact check at source line 95')
_require(form2(0,-2)==(aa,1,0,-1), 'check_quadratic.py exact check at source line 96')
_require(form2(1,-2)==(8*dd+3,4*dd+2,2*dd+2,dd), 'check_quadratic.py exact check at source line 97')
_require(form2(-1,2)==(8*dd-3,4*dd-2,2*dd-2,dd), 'check_quadratic.py exact check at source line 98')
_require(form2(2,-2)==(dd,dd-1,dd+1,dd), 'check_quadratic.py exact check at source line 99')
_require(form2(0,-1)==(aa,2,0,1), 'check_quadratic.py exact check at source line 100')
# Enumerate each ordinary endpoint dimension vector using both embedding equations.
def endpoint(d,A,B,half=False):
    # D=A+B sqrt(d); nonunit dimensions (t+s sqrt(d))/den.
    den=2 if half else 1
    sn=S.Rational(A*den*den,2*d);tn=S.Rational((A-2)*den*den,2);dot=S.Rational(B*den*den,2)
    _require(all(x.q==1 for x in (sn,tn,dot)), 'check_quadratic.py exact check at source line 106')
    sn,tn,dot=map(int,(sn,tn,dot));out=set();rad=isqrt(tn)
    for sv in product(range(isqrt(sn)+1),repeat=3):
        if tuple(sorted(sv))!=sv or sum(x*x for x in sv)!=sn:continue
        for tv in product(range(-rad,rad+1),repeat=3):
            if sum(x*x for x in tv)!=tn or sum(x*y for x,y in zip(sv,tv))!=dot:continue
            if half and any((x-y)%2 for x,y in zip(sv,tv)):continue
            # Independent signs of coordinate chosen to make positive FP dimensions, and all >=1.
            dims=sorted([abs((x+y*S.sqrt(d))/den) for x,y in zip(tv,sv)],key=cmp_to_key(lambda x,y:int(S.sign(S.simplify(x-y)))))
            if any(S.simplify(x-1).is_negative for x in dims):continue
            _require(all(S.simplify(x-1).is_nonnegative for x in dims),'exact endpoint dimension comparison')
            out.add(tuple(S.simplify(x) for x in dims))
    return out
eta=1+S.sqrt(2);eps=2+S.sqrt(3)
_require(endpoint(5,S.Rational(15,2),S.Rational(5,2),True)=={tuple([phi,phi,S.expand(phi**2)])}, 'check_quadratic.py exact check at source line 119')
_require(endpoint(3,12,6)==set(), 'check_quadratic.py exact check at source line 120')
_require(endpoint(5,15,6,True)=={tuple([phi,S.expand(phi**2),S.expand(phi**3)])}, 'check_quadratic.py exact check at source line 121')
_require(endpoint(5,75,33,True)=={tuple([S.expand(phi**2),S.expand(phi**3),S.expand(phi**5)])}, 'check_quadratic.py exact check at source line 122')
_require(endpoint(2,8,4)=={(S.Integer(1),eta,eta)}, 'check_quadratic.py exact check at source line 123')
_require(endpoint(2,24,16)=={(eta,eta,S.expand(eta**2))}, 'check_quadratic.py exact check at source line 124')
_require(endpoint(3,36,20)=={(eps,eps,2*eps-1)}, 'check_quadratic.py exact check at source line 125')
# Reconstruct the three impossibility endpoints from norm and inner-product constraints.
def impossible_endpoint(d,A,B):
    # Integer a_i,b_i, not assuming conjugate orthogonality, as in the proof.
    for B2 in range(A//d+1):
        A2=A-1-d*B2
        if A2<0 or A2*B2<(B//2)**2:continue
        for bv in product(range(isqrt(B2)+1),repeat=3):
            if sum(x*x for x in bv)!=B2 or tuple(sorted(bv))!=bv:continue
            for av in product(range(-isqrt(A2),isqrt(A2)+1),repeat=3):
                if sum(x*x for x in av)==A2 and sum(x*y for x,y in zip(av,bv))==B//2:
                    _require(any(x==y==0 for x,y in zip(av,bv)), (d,A,B,av,bv))
for args in [(3,12,6),(6,12,4),(6,60,24)]:impossible_endpoint(*args)
out['symbolic_normal_forms']='PASS'
out['ordinary_endpoint_reconstructions']='PASS'
# Independent Casimir characteristic polynomials of the three normal forms.
def matrices(tup):
    a,b,c,d,e,f,g,h,i,j=tup
    return [S.eye(4),S.Matrix([[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]]),S.Matrix([[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]]),S.Matrix([[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]])]
z=S.Symbol('z');m=S.Symbol('m')
for tup,prefix,N,Tsum in [
    ((m-1,m-1,m,m,m,m,m,m,m+1,m+1),(z-3)**2,9*(9*m*m+4),3*(9*m*m+4)),
    ((m,m,m,m-1,m,m-1,m,m-1,m-1,m),(z-5)**2,5*(9*m*m-8*m+4),3*(9*m*m-8*m+4)),
    ((8*m-8,8-8*m,4*m-4,8*m-7,4-4*m,2*m-3,7-8*m,4*m-4,2-2*m,m),(z-3)*(z-6),9*(162*m*m-312*m+152),9*(162*m*m-312*m+152)/2),
]:
    mats=matrices(tup);cas=sum((A*A for A in mats),S.zeros(4))
    _require(S.expand(cas.charpoly(z).as_expr()-prefix*(z*z-Tsum*z+N))==0, 'check_quadratic.py exact check at source line 151')
# All eight independent nonunit sign changes for the codegree-five pair.
viable=[]
for sig in product((-1,1),repeat=3):
    row1=(1,)+tuple(x*y for x,y in zip(sig,(-1,phi,phip)))
    row2=(1,)+tuple(x*y for x,y in zip(sig,(-1,phip,phi)))
    nf=normalform([row1,row2],5)
    domain=S.reduce_inequalities([q>=0 for q in nf],j)
    if domain!=S.false:viable.append((sig,str(domain)))
_require(len(viable)==2 and {x[0] for x in viable}=={(-1,-1,-1),(1,1,1)}, viable)
out['casimir_codegree_polynomials']='PASS'
out['constant_five_nonnegative_sign_choices']=viable
print(json.dumps(out,indent=2))
