#!/usr/bin/env python3
"""Independent cyclotomic-quotient check of all bounded joint trace types."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math
import numpy as np
import sympy as s
from flint import fmpz_poly
import sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'r455_center_integer'))
import joint_rotation as producer
class Adapter:
    @staticmethod
    def conductor(q):return q if q%4==1 else 4*q
    @staticmethod
    def configure(q,r):pass
    @staticmethod
    def trace_types(height,orders=None,powers=None):return producer.trace_types(height,orders=orders,powers=powers)
gb=Adapter()

def require(ok,msg):
    if not ok:raise ValueError(msg)

def validate(q,r,height,primes):
    gb.configure(q,r);gb.PRIMES=primes
    all_types,bound=gb.trace_types(height)
    L=math.lcm(int(bound),math.lcm(*range(1,height+1)));x=s.Symbol('x');phi=s.Poly(s.cyclotomic_poly(L,x),x)
    degree=phi.degree();co=np.array(list(reversed(list(map(int,phi.all_coeffs())))),dtype=np.int64)
    powers=np.zeros((L,degree),dtype=np.int64);powers[0,0]=1
    for j in range(1,L):
        old=powers[j-1]
        require(max(map(abs,map(int,old)))*(1+max(map(abs,map(int,co))))<2**60,'cyclotomic recurrence overflow bound')
        powers[j,1:]=old[:-1];powers[j]-=int(old[-1])*co[:-1]
    max_power=max(map(abs,map(int,powers.flat)))
    require(max_power*L<2**50 and L**3*height<2**60,'cyclotomic summation/index overflow bound')
    modulus=fmpz_poly(list(map(int,co)))
    def gauss(d):
        D=gb.conductor(d);scale=math.isqrt(D//d);out=np.zeros(degree,dtype=np.int64)
        require(L%D==0,'field conductor absent')
        for a in range(D):out+=int(s.kronecker_symbol(D,a))*powers[(a*(L//D))%L]
        require(all(int(v)%scale==0 for v in out),'Gauss basis not divisible')
        return out//scale
    b0=np.zeros(degree,dtype=np.int64);b0[0]=1
    basis=[b0,gauss(q),gauss(r),gauss(q*r)]
    polynomials=[fmpz_poly(list(map(int,b))) for b in basis]
    require((polynomials[1]**2-q)%modulus==0,'first Gauss square')
    require((polynomials[2]**2-r)%modulus==0,'second Gauss square')
    require((polynomials[1]*polynomials[2]-polynomials[3])%modulus==0,'correlated third Gauss sign')
    B=s.Matrix(np.stack(basis,axis=1).tolist());pivots=list(B.T.rref()[1]);require(len(pivots)==4,'degree-four Gauss basis')
    inverse=B.extract(pivots,range(4)).inv()
    units=[u for u in range(L) if math.gcd(u,L)==1]
    signs=lambda u:(int(s.kronecker_symbol(gb.conductor(q),u)),int(s.kronecker_symbol(gb.conductor(r),u)))
    H=np.array([u for u in units if signs(u)==(1,1)],dtype=np.int64)
    require(len(H)*4==len(units),'fixed subgroup index')
    representatives={signs(u):u for u in units};require(len(representatives)==4,'all four field automorphisms')
    def exact_trace(n,k,u):
        sums=powers[(H*(L//n)*k*u)%L].sum(axis=0)
        values=inverse*s.Matrix([int(sums[p]) for p in pivots])/len(H)
        coords=tuple(F(int(v.p),int(v.q)) for v in values)
        denominator=math.lcm(*(v.denominator for v in coords))
        predicted=[sum(int(basis[j][i])*int(coords[j]*denominator) for j in range(4)) for i in range(degree)]
        require(all(predicted[i]*len(H)==int(sums[i])*denominator for i in range(degree)),'full relative-trace polynomial identity')
        return coords
    records=[];joint=set()
    requests=[(int(n),list(range(1,height+1)),'central') for n in s.divisors(bound)]
    requests += [(int(n),[int(k) for k in s.divisors(m) if k<m],'rotation_'+str(m)) for m in range(3,height+1) for n in s.divisors(m)]
    for n,ps,kind in requests:
        actual={tuple(exact_trace(n,k,u) for k in ps) for u in representatives.values()}
        formula,_=gb.trace_types(height,[n],ps)
        require(actual==set(formula),'joint trace formula '+str((q,r,n,ps)))
        records.append(dict(kind=kind,order=n,powers=ps,types=len(actual)))
        if kind=='central':joint|=actual
    # The analytic prime-power bound proves that all orders outside the box
    # give the joint zero type; direct enumeration checks every in-box order.
    joint.add(tuple((F(0),)*4 for _ in range(height)))
    require(joint==set(all_types),'complete bounded joint types')
    return dict(radicands=[q,r],height=height,primes=primes,order_bound=int(bound),ambient_cyclotomic_order=L,cyclotomic_degree=degree,fixed_subgroup_size=len(H),joint_types=len(joint),checks=records)

def sts_check():
    data=producer.setup();R,a,chars,cols,Q,high,basis,coords,ds,D=data;K=a['K']
    saved=json.loads((BASE/'r455_center_integer/joint_rotation.json').read_text())
    case=saved['cases'][0];m=case['metadata']['fixed_high_multiplicities'];ep=case['metadata']['indicators']
    A,b,meta=producer.build(data,m,ep);types,_=producer.trace_types(6)
    require(meta==case['metadata'],'reference system identity')
    # Independently derive STS from the correctly normalized S rows, then
    # divide by beta_E beta_F. No producer coordinate multiplication is used.
    value=lambda chi,v:sum((K(int(x))*y for x,y in zip(v,chi)),K.zero)
    beta=[a['D']/f/K(r)for f,r in zip(a['codegrees'],a['multiplicities'])]
    for E,F_ in itertools.product(range(5),repeat=2):
        orth=sum((chars[E][i]*chars[F_][a['du'][i]]for i in range(8)),K.zero)
        require(orth==(a['codegrees'][E]*K(a['multiplicities'][E])if E==F_ else K.zero),'full character orthogonality')
        require(beta[E]*value(chars[E],cols[F_])==beta[F_]*value(chars[F_],cols[E]),'full low S symmetry')
    require(chars[0]==a['ds']and beta[0]==K.one,'FP-first unit normalization')
    low=[[beta[E]*value(chars[E],v)for v in cols]for E in range(5)]
    highS=[[beta[E]*value(chars[E],(0,)+v)for v,z in high]for E in range(5)]
    start=len(A)-len(high)-60;checked=0
    for E,F_ in itertools.combinations_with_replacement(range(5),2):
        target=(a['D']*low[E][F_]-sum((x*y for x,y in zip(low[E],low[F_])),K.zero))/(beta[E]*beta[F_])
        coefficient=[]
        for j in range(len(high)):
            for typ in types:
                trace=sum((K(s.Rational(x.numerator,x.denominator))*v for x,v in zip(typ[0],basis)),K.zero)
                coefficient.append(coords(highS[E][j]*highS[F_][j]*trace/(beta[E]*beta[F_])))
        target=coords(target)
        for k in range(4):
            row=[v[k]for v in coefficient]+[F(0)]*(len(A[0])-len(coefficient));constant=target[k]
            den=math.lcm(constant.denominator,*(x.denominator for x in row));ints=[int(x*den)for x in row];rhs=int(constant*den)
            div=math.gcd(rhs,*ints)or 1
            require([x//div for x in ints]==A[start+checked]and rhs//div==b[start+checked],'independent normalized STS coefficient row')
            checked+=1
    require(checked==60,'complete STS row count')
    return {'all_S_character_pairs':25,'independent_STS_coordinate_rows':checked,'high_trace_columns':len(high)*len(types),
            'full_system_matrix_sha256':meta['matrix_sha256'],'noncommutative_normalization':'D/(f_E dim(E))',
            'canonical_FP_character_first':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    record=validate(3,13,6,[2,3,13]);sts=sts_check()
    files=[Path(__file__),BASE/'r455_center_integer/joint_rotation.py',BASE/'r455_center_integer/joint_rotation.json',
           BASE/'r455_center_integer/verify.py',BASE/'r455_center_integer/results.json']
    result={'schema':'independent-R455-trace-STS-review-v1','status':'PASS',
            'method':'Full exact cyclotomic quotient averaging for every bounded order and retained power; independently normalized complete STS rows',
            'trace_review':record,'STS_review':sts,'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}
    target=HERE/'r455_trace_sts_review.json'
    if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
    else:require(json.loads(target.read_text())==result,'independent review receipt differs')
    print('PASS R455: complete cyclotomic trace domain and all normalized STS rows',flush=True)
if __name__=='__main__':main()
