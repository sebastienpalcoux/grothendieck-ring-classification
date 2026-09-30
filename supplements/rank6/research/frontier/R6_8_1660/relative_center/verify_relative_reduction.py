#!/usr/bin/env python3
"""Exact necessary rank-18 relative-center reduction of R6_8_1660.
No optimizers, floating point, induction matrices or full-center modular data.
Run from any directory. Requires SymPy only. ~10 seconds on the supplied runtime.
The proof of applicability is in relative_center_note.tex; surviving rings are
necessary alternatives, NOT asserted categorifications.
"""
import hashlib,itertools,json,math
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[3]/'data/census.json'
P=list(itertools.product(range(3),repeat=2));IX={x:i for i,x in enumerate(P)}
CH=[[(1,0),(1,0),(0,1)],[(1,0),(1,0),(0,-1)],[(1,0),(-1,0),(0,0)]]
def require(condition,message):
    if not condition:raise ArithmeticError(message)
def qm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def ev(A,ch):
    vals=[qm(CH[ch[0]][i],CH[ch[1]][j]) for i,j in P]
    return tuple(sum(a*v[k] for a,v in zip(A,vals)) for k in (0,1))
def gf(i):return 1-i if i<2 else 2
def perm(A,g,h):return tuple(A[IX[gf(i) if g else i,gf(j) if h else j]] for i,j in P)
def twist(A,s,u,v):
    out=[0]*9
    for n,(i,j) in zip(A,P):
        if i==2 and u:j=gf(j)
        if j==2 and v:i=gf(i)
        if s:i,j=j,i
        out[IX[i,j]]=n
    return tuple(out)
def orbits(rs):
    seen=set();out=[];keys={(r['L'],tuple(r['A'])) for r in rs}
    for r in rs:
        key=r['L'],tuple(r['A'])
        if key in seen:continue
        orb={(r['L'],perm(twist(r['A'],s,u,v),g,h)) for s,u,v,g,h in itertools.product(range(2),repeat=5)}
        require(orb<=keys,'survivors not relabelling invariant')
        seen|=orb;out.append(dict(L=r['L'],A=list(min(a for _,a in orb)),orbit_size=len(orb)))
    require(seen==keys,'incomplete orbits')
    return out

def main():
    blob=SOURCE.read_bytes();r=next(r for r in json.loads(blob) if r['id']=='R6_8_1660');N=r['N']
    require(r['dual']==list(range(6)),'wrong duality')
    require(N[1][1]==[1,0,0,0,0,0] and N[4][4]==[1,1,0,0,0,0],'not Ising')
    require(N[1][2]==[0,0,0,1,0,0] and N[4][2]==[0,0,0,0,0,1],'wrong complementary orbit')
    require(N[2][2]==[1,0,3,3,0,4],'wrong quadratic relation')
    z=sp.symbols('z');d=3+2*sp.sqrt(2)+2*sp.sqrt(3)+sp.sqrt(6);D=sp.expand(16*(1+d*d))
    require(sp.expand(d*d-1-(6+4*sp.sqrt(2))*d)==0,'wrong FP dimension')
    dp=sp.Poly(sp.minpoly(D,z),z);require(abs(int(dp.TC()))==2**22*3**2,'wrong global norm')
    raw=[]
    for t in range(4):
      for a in range(4-t):
       for c in range(4-t):
        for sig in itertools.product(range(5),repeat=4):
         if sum(sig)!=4:continue
         A=[0]*9
         for ij,n in [((0,0),a),((1,1),3-t-a),((0,1),c),((1,0),3-t-c),((2,2),t)]:A[IX[ij]]=n
         for ij,n in zip([(0,2),(1,2),(2,0),(2,1)],sig):A[IX[ij]]=n
         for L in (0,1):
          if L and tuple(A)!=perm(A,1,1):continue
          raw.append(dict(L=L,A=A,values=[ev(A,ch) for ch in P]))
    require(len(raw)==1056,'wrong categorical raw domain')
    normsurv=[];normreject=[]
    for r in raw:
      bad=None
      for j,(u,v) in enumerate(r['values']):
        p,q=P[j];l=-1 if r['L'] and ((p==2)!=(q==2)) else 1
        if l==-1:require((u,v)==(0,0),'star incompatible character');continue
        n=(u*u+2*v*v+4)**2-8*u*u*v*v;co=n
        for prime in (2,3):
          while co%prime==0:co//=prime
        if co!=1:bad=dict(character=j,norm=n,forbidden_factor=co);break
      (normsurv if bad is None else normreject).append(r if bad is None else dict(ring=r,witness=bad))
    require(len(normsurv)==158,'wrong norm survivors')
    cache={};intsurv=[];intreject=[]
    for r in normsurv:
      bad=None
      for j,(u,v) in enumerate(r['values']):
       p,q=P[j];fB=(2 if p==2 else 4)*(2 if q==2 else 4)
       if r['L'] and ((p==2)!=(q==2)):continue
       for sign in (1,-1):
        key=(sign*u,sign*v,fB)
        if key not in cache:
          aa=key[0]+key[1]*sp.sqrt(2);f=sp.simplify(fB*(2+aa*aa/2+aa*sp.sqrt(aa*aa+4)/2))
          poly=sp.Poly(sp.minpoly(sp.simplify(D/f),z),z)
          cache[key]=dict(integral=poly.LC()==1,primitive_minpoly=[int(c) for c in poly.all_coeffs()])
        if not cache[key]['integral']:bad=dict(character=j,sign=sign,cache_key=list(key));break
       if bad:break
      (intsurv if bad is None else intreject).append(r if bad is None else dict(ring=r,witness=bad))
    require(len(intsurv)==130,'wrong integral survivors')
    final=[];fieldreject=[]
    for r in intsurv:
      bad=None
      for j,(u,v) in enumerate(r['values']):
        n=(u*u+2*v*v+4)**2-8*u*u*v*v
        if math.isqrt(n)**2!=n:bad=dict(character=j,discriminant_norm=n);break
      (final if bad is None else fieldreject).append(r if bad is None else dict(ring=r,witness=bad))
    require(len(final)==58,'wrong final survivors');oo=orbits(final);require(len(oo)==14,'wrong final orbit count')
    report=dict(status='necessary_reduction_only_original_unresolved',source_sha256=hashlib.sha256(blob).hexdigest(),
      basis_B=[list(p) for p in P],L_meaning={'0':'unit','1':'g tensor g'},
      domain_counts=dict(star_compatible=1056,prime_norm=158,codegree_divisibility=130,dimension_field=58,relabelling_orbits=14),
      relative_dimension=str(D),relative_dimension_minpoly=[int(c) for c in dp.all_coeffs()],
      survivors=final,orbit_representatives=oo,
      norm_rejections=normreject,integrality_rejections=intreject,field_rejections=fieldreject,
      exact_integrality_checks={str(k):v for k,v in cache.items()})
    (HERE/'relative_reduction_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'counts':report['domain_counts'],'source_sha256':report['source_sha256']},indent=2))
if __name__=='__main__':main()
