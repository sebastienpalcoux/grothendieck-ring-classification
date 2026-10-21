"""Distinguished-center S symmetry and STS equations, with full characters."""
import itertools,math
from fractions import Fraction as Q
import central_support as c
import full_rotation as full
from exact import discover_roots,vector
s=c.s

def characters(R,a):
    sc=c.w.ScalarCharacters(R);K=a['K'];out=[]
    for f,m in sc.components:
        roots=discover_roots(f,K);c.require(roots is not None,'scalar characters split in FP field')
        for z in roots:out.append([sum((K(co)*z**j for j,co in enumerate(cf)),K.zero) for cf in sc.coeff])
    c.require(len(out)==4,'four scalar characters')
    out.append([(K(int(s.trace(N)))-sum((ch[i] for ch in out),K.zero))/K(2) for i,N in enumerate(a['N'])])
    codegrees=[sum((ch[i]*ch[a['du'][i]] for i in range(8)),K.zero)/K(m) for ch,m in zip(out,[1,1,1,1,2])]
    order=[]
    for fc,m in zip(a['codegrees'],a['multiplicities']):
        at=next(i for i,ff in enumerate(codegrees) if ff==fc and i not in order and (i==4)==(m==2));order.append(at)
    out=[out[i] for i in order]
    for i,ch in enumerate(out):
        for j,other in enumerate(out):
            norm=sum((ch[k]*other[a['du'][k]] for k in range(8)),K.zero)
            c.require(norm==(a['codegrees'][i]*K(a['multiplicities'][i]) if i==j else K.zero),'full character orthogonality')
    return out

def value(ch,v,K):return sum((K(z)*x for z,x in zip(v,ch)),K.zero)

def assignments(a,chs,cols):
    K=a['K'];out=[]
    for perm in itertools.permutations(range(5)):
        if perm[0]!=0:continue
        if any(a['codegrees'][i]!=a['codegrees'][perm[i]] or a['multiplicities'][i]!=a['multiplicities'][perm[i]] for i in range(5)):continue
        S=[[a['D']/a['codegrees'][i]/K(a['multiplicities'][i])*value(chs[i],cols[perm[j]],K) for j in range(5)] for i in range(5)]
        if all(S[i][j]==S[j][i] for i in range(5) for j in range(5)):out.append(perm)
    return out

def append_sts(R,a,cols,perm,A,b,meta,height):
    K=a['K'];chs=characters(R,a);quartic=a['factor'].degree()==4
    c.require(perm in assignments(a,chs,cols),'symmetric distinguished S assignment')
    if quartic:
        high=full.base.bq.high_columns(a,cols)[2];types,_=full.base.bq.trace_types(height);coords=a['coords']
        fieldbasis=[K.one]
        for q in (2,3):fieldbasis.append(next(x for x in discover_roots(s.Poly(c.w.t**2-q,c.w.t),K) if a['embedding'].sign(x)>0))
        fieldbasis.append(fieldbasis[1]*fieldbasis[2])
    else:
        L=s.Matrix.hstack(*map(s.Matrix,cols));high=full.base.grams.high_columns(a,L)[1];types,_=full.h.trace_types(a['q'],a['primes'],height)
        root=next(x for x in discover_roots(s.Poly(c.w.t**2-a['q'],c.w.t),K) if a['embedding'].sign(x)>0)
        fieldbasis=[K.one,root];V=s.Matrix.hstack(*(vector(x,2) for x in fieldbasis));Vinv=V.inv()
        coords=lambda x:tuple(Q(str(v)) for v in Vinv*vector(x,2))
    width=len(fieldbasis);trace1=[sum((K(s.Rational(v.numerator,v.denominator))*basis for v,basis in zip(typ[0],fieldbasis)),K.zero) for typ in types]
    highvalues=[[value(ch,(0,)+tuple(v),K) for ch in chs] for v,z in high]
    lowvalues=[[value(ch,v,K) for ch in chs] for v in cols]
    rows=[];rhs=[]
    for E,F in itertools.combinations_with_replacement(range(5),2):
        target=a['codegrees'][F]*K(a['multiplicities'][F])*value(chs[E],cols[perm[F]],K)-sum((v[E]*v[F] for v in lowvalues),K.zero)
        columns=[coords(v[E]*v[F]*tr) for v in highvalues for tr in trace1]
        target=coords(target)
        for k in range(width):
            row=[v[k] for v in columns]+[Q(0)]*(len(A[0])-len(columns));constant=target[k]
            den=math.lcm(constant.denominator,*(v.denominator for v in row));row=[int(v*den) for v in row];constant=int(constant*den);g=math.gcd(constant,*row) or 1
            rows.append([x//g for x in row]);rhs.append(constant//g)
    return A+rows,b+rhs,dict(meta,sts_rows=len(rows),character_assignment=list(perm))
