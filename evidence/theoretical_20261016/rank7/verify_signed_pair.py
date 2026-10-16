#!/usr/bin/env python3
"""Exact one-matrix completion for R7_4_1212 and R7_4_1213.

Dependencies: Python 3, SymPy, and a C++17 compiler. No floating-point arithmetic.
Run: python3 verify_signed_pair.py --repo /path/to/grothendieck-ring-classification
The mathematical field/global-dimension prerequisite is QUADRATIC_REMAINDER.md.
"""
import argparse, collections, gzip, hashlib, itertools, json, math
from pathlib import Path
import subprocess, tempfile
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))
IDS=('R7_4_1212','R7_4_1213')
X=s.Symbol('x')

def require(condition,message):
    if not condition: raise RuntimeError(message)

def source_tensors(repo):
    census=repo/'supplements/rank7/data/rank7_tables.txt.gz'
    counts=collections.Counter(); out={}
    with gzip.open(census,'rt') as stream:
        for line in stream:
            if not line.strip(): continue
            n=json.loads(line.replace('{','[').replace('}',']'))
            m=max(v for a in n for b in a for v in b);counts[m]+=1
            rid=f'R7_{m}_{counts[m]}'
            if rid in IDS: out[rid]=n
    require(set(out)==set(IDS),'Missing source ring')
    return out

def verify_quadratic_prerequisite(data):
    """Replay every finite part of the prior quadratic-field reduction."""
    tested=0
    for a in range(1,6):
        for b,c,d in itertools.product(range(1,3*a*a//8+1),range(1,a**3//16+1),range(1,a**4//256+1)):
            p=s.Poly(X**4-a*X**3+b*X**2-c*X+d,X);tested+=1
            require(not (p.is_irreducible and p.count_roots(0,s.oo)==4),'Totally positive irreducible quartic of trace at most5')
    residual=[]
    for k in range(1,8):
        p=s.Poly(X**2-43*k*X+90*k,X)
        require(p.is_irreducible and s.Rational(43*43*k,90).q!=1,'Degree-four branch survives d-number test')
        residual.append(str(p.as_expr()))
    candidates=[(a,b) for a in range(1,6) for b in range(-5,6) if a%2==b%2 and a*a>5*b*b]
    require(candidates==[(2,0),(3,-1),(3,1),(4,0),(5,-1),(5,1)],'Quadratic dimension list changed')
    sources=[]
    for rid,n in data.items():
        mats=list(map(s.Matrix,n));casimir=sum((m*m.T for m in mats),s.zeros(7))
        f=casimir.charpoly(X).as_expr();factors=s.factor_list(f)[1]
        require(s.rem(f,X**2-900*X+6480,X)==0,'Missing quadratic source formal codegrees')
        ints=[int(-s.Poly(p,X).TC()) for p,m in factors if s.degree(p,X)==1]
        require(math.lcm(*ints)==180,'Integer formal-codegree lcm is not180')
        b=int(s.trace(casimir));require(b=={'R7_4_1212':1036,'R7_4_1213':1020}[rid],'Casimir bound changed')
        require(6*180+2>b and 4*180+2<=b<4*360+2,'Field-degree trace bounds changed')
        sources.append({'id':rid,'Casimir_polynomial':str(s.factor(f)),'Casimir_trace':b,'integer_codegree_lcm':180})
    return {'source_reduction':'evidence/upper_residual_20261002c/scoped_research/QUADRATIC_REMAINDER.md','source_commit':'1592905dc573227ad03659a6370a9459d40db26c','quartic_polynomials_checked':tested,'degree_four_residual_polynomials':residual,'global_dimension_pairs':[[90*a,90*b] for a,b in candidates],'source_checks':sources}

def matrix(c,ix):
    a=s.zeros(6);a[0,1]=1;a[1,0]=2
    for v,(i,j) in zip(c,ix): a[i,j]=a[j,i]=v
    return a

def verify_case(rid,n,exe):
    require(len(n)==7 and all(len(a)==7 and all(len(b)==7 for b in a) for a in n),'Bad tensor shape')
    require(all(n[i][j][k]==n[j][i][k]==n[i][k][j] for i,j,k in itertools.product(range(7),repeat=3)),'Not self-dual symmetric')
    require(all(n[0][i][j]==int(i==j) for i,j in itertools.product(range(7),repeat=2)),'Unit failure')
    require(all(n[1][i][j]==int(i==j) for i in range(2,7) for j in range(7)),'g not fixing noninvertibles')
    require(n[1][1][0]==1,'g not order two')
    ix=[];domains=[]
    for i in range(2,7):
        for j in range(i,7):
            a=n[2][i][j]
            ds=[v for v in range(-a,a+1,2) if (i!=2 and i!=j) or (v-a)%4==0]
            ix.append((i-1,j-1));domains.append(ds)
    total=math.prod(map(len,domains))
    require(total=={'R7_4_1212':97200,'R7_4_1213':259200}[rid],'Unexpected domain size')
    inp=f'{len(ix)}\n'+''.join(f'{i} {j} {len(ds)} '+' '.join(map(str,ds))+'\n' for (i,j),ds in zip(ix,domains))
    run=subprocess.run([str(exe)],input=inp,text=True,capture_output=True,check=True)
    counts=run.stderr.strip().split()
    require(counts[::2]==['total','pass1009','pass1013'],'Bad enumerator counts')
    counts=dict(zip(counts[::2],map(int,counts[1::2])))
    require(counts['total']==total,'Incomplete enumeration')
    rows=[list(map(int,line.split())) for line in run.stdout.splitlines()]
    require(len(rows)==counts['pass1013']=={'R7_4_1212':372,'R7_4_1213':288}[rid],'Unexpected surviving matrices')
    require(len(set(map(tuple,rows)))==len(rows),'Duplicate matrix')
    branches=collections.Counter();weights=collections.Counter();exceptional=[]
    for c in rows:
        require(len(c)==len(domains) and all(v in ds for v,ds in zip(c,domains)),'Invalid retained matrix')
        a=matrix(c,ix);f=a.charpoly(X).as_expr();q=a[1:,1:].charpoly(X).as_expr();d=2*s.diff(f,X)
        factors=s.factor_list(f)[1]
        repeated=s.prod(g for g,e in factors if e>1)
        checks=[s.gcd(f,d-180*q),s.gcd(f,d-360*q)]+[s.gcd(f,(d-u*q)**2-40500*q**2) for u in (270,450)]
        for h in checks:
            if s.degree(h,X)<=0: continue
            sf=s.quo(h,s.gcd(h,s.diff(h,X)),X)
            require(s.rem(repeated,sf,X)==0,'A possible simple dimension eigenvalue survives')
        for g,multiplicity in factors:
            if multiplicity<=1: continue
            require(s.degree(g,X)==1 and multiplicity in (2,3),'Unexpected repeated branch')
            lam=s.solve(g,X)[0]
            require(lam!=0,'Unexpected zero branch')
            v=s.Matrix.hstack(*(a-lam*s.eye(6)).nullspace());metric=s.diag(2,1,1,1,1,1)
            projection=v*(v.T*metric*v).inv()*v.T*metric
            w=projection[0,0]
            weights[(str(lam),multiplicity,str(w))]+=1
            # Both conjugate dimension characters occur. The base is their
            # total weight at the first coordinate in the g=+1 block.
            for delta_name,base in [('180',s.Rational(1,45)),('360',s.Rational(1,90)),('270+-90sqrt5',s.Rational(1,30)),('450+-90sqrt5',s.Rational(1,90))]:
                if multiplicity==2:
                    if w!=base:branches['multiplicity_two_weight_mismatch']+=1;continue
                    require(rid=='R7_4_1213' and lam==-3 and delta_name=='180','Unexpected matching repeated branch')
                    expected=(X-2)*(X+3)**2*(X**3-3*X**2-5*X+3)
                    require(s.expand(f-expected)==0,'Unexpected exceptional characteristic polynomial')
                    require(s.Poly(X**3-3*X**2-5*X+3,X).is_irreducible,'Cubic must be irreducible')
                    h2=s.cancel(d.subs(X,2)/q.subs(X,2))
                    require(h2==10,'Unexpected codegree of the eigenvalue 2')
                    # The three cubic characters have a common rational
                    # formal codegree h (degree divides both 3 and 2).
                    h=s.cancel(3/(1-s.Rational(1,2)-s.Rational(2,180)-1/h2))
                    require(h==s.Rational(54,7) and h.q!=1,'Expected algebraic-integrality contradiction')
                    exceptional.append(c);branches['cubic_nonintegral_codegree']+=1
                else:
                    if w<=base:branches['multiplicity_three_nonpositive_weight']+=1;continue
                    h=s.cancel(2/(w-base))
                    require(h.q!=1,'An integral third codegree survives')
                    branches['multiplicity_three_nonintegral_codegree']+=1
    require(len(exceptional)==(4 if rid.endswith('1213') else 0),'Exceptional count changed')
    return {'id':rid,'decision':'excluded_general','method':'signed sphericalization; one multiplication matrix; exact modular and rational arithmetic','prerequisite':'QUADRATIC_REMAINDER.md: K=Q(sqrt(5)), delta in {180,360,270+-90sqrt(5),450+-90sqrt(5)}','tensor_sha256':hashlib.sha256(json.dumps(n,separators=(',',':')).encode()).hexdigest(),'matrix_domains':domains,'counts':counts,'retained_sha256':hashlib.sha256(run.stdout.encode()).hexdigest(),'branch_counts':dict(branches),'repeated_weights':[{'eigenvalue':v,'multiplicity':m,'weight':w,'count':c} for (v,m,w),c in sorted(weights.items())],'exceptional_matrices':exceptional}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=ROOT);parser.add_argument('--output',type=Path)
    args=parser.parse_args();data=source_tensors(args.repo);prerequisite=verify_quadratic_prerequisite(data)
    require(s.isprime(1009) and s.isprime(1013),'Bad moduli')
    with tempfile.TemporaryDirectory(prefix='signed_pair_') as td:
        exe=Path(td)/'one_matrix'
        subprocess.run(['g++','-std=c++17','-O3',str(HERE/'one_matrix.cpp'),'-o',str(exe)],check=True)
        results=[verify_case(rid,data[rid],exe) for rid in IDS]
    output={'status':'PASS','floating_point_used':False,'quadratic_prerequisite':prerequisite,'results':results}
    if args.output:args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'PASS','results':[{'id':r['id'],'counts':r['counts'],'branch_counts':r['branch_counts']} for r in results]},indent=2))

if __name__=='__main__':main()
