#!/usr/bin/env python3
"""Source-bound exact signed-plus quotient reduction for three rank-seven cases."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
import sympy as s


def require(value,message):
    if not value: raise RuntimeError(message)


def matrices(v):
    A,B,C,D,r,w,z,l,m,n=v
    return [s.eye(4),
        s.Matrix([[0,1,0,0],[1,A,B,r],[0,B,C,w],[0,2*r,2*w,l]]).T,
        s.Matrix([[0,0,1,0],[0,B,C,w],[1,C,D,z],[0,2*w,2*z,m]]).T,
        s.Matrix([[0,0,0,1],[0,2*r,2*w,l],[0,2*w,2*z,m],[2,2*l,2*m,n]]).T]


def equations(v):
    A,B,C,D,r,w,z,l,m,n=v
    return [A*C-B*B+B*D-C*C+2*r*z-2*w*w+1,
        A*l+B*m-l*l+n*r-2*r*r-2*w*w+1,
        A*w-B*r+B*z-C*w-l*w+m*r,
        B*l+C*m-l*m+n*w-2*r*w-2*w*z,
        B*w-C*r+C*z-D*w-l*z+m*w,
        C*l+D*m-m*m+n*z-2*w*w-2*z*z+1]


def enumerate_quotients(bounds):
    dom=[list(range(-q,q+1,2)) for q in bounds]
    if bounds[0]:dom[0]=[a for a in dom[0] if a>0]
    dom[1]=[b for b in dom[1] if b>0]
    dom[4]=[r for r in dom[4] if r>=0]
    found=[]
    for A,B,C,r,w,z,l in itertools.product(*(dom[i] for i in [0,1,2,4,5,6,7])):
        D=s.Rational(B*B+C*C-A*C-2*r*z+2*w*w-1,B)
        if D not in dom[3]: continue
        ms=[s.Rational(-A*w+B*r-B*z+C*w+l*w,r)] if r else dom[8]
        for m in ms:
            if m not in dom[8]:continue
            ns=[s.Rational(-A*l-B*m+l*l+2*r*r+2*w*w-1,r)] if r else dom[9]
            for n in ns:
                if n not in dom[9]:continue
                v=list(map(int,[A,B,C,D,r,w,z,l,m,n]))
                if all(z==0 for z in equations(v)):found.append(v)
    return sorted(found)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);args=ap.parse_args()
    targets={'R7_4_106':(1,2,3,6,3),'R7_4_2155':(3,1,5,4,3),'R7_3_146':(1,2,3,6,6)}
    counts=collections.Counter(); sources={};x=s.Symbol('x')
    for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'));m=max(v for a in N for b in a for v in b);counts[m]+=1;rid=f'R7_{m}_{counts[m]}'
        if rid in targets:sources[rid]=N
    require(set(sources)==set(targets),'Exact source coverage')
    family={};cases=[]
    for rid,(g,a,b,f,rad) in targets.items():
        N=sources[rid];G=[s.Matrix(z).T for z in N];dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
        perm=[next(j for j in range(7) if N[g][i][j]) for i in range(7)];ga,gb=perm[a],perm[b]
        require(perm==[next(j for j in range(7) if N[i][g][j]) for i in range(7)],'g central')
        require(perm[f]==f and perm[a]!=a and perm[b]!=b and G[g]**2==s.eye(7),'Involution orbit pattern')
        require(set([0,g,a,ga,b,gb,f])==set(range(7)),'All seven labels in prescribed orbits')
        require(all(dual[i] in {i,perm[i]} for i in range(7)),'Duality trivial modulo g')
        bounds=[N[a][a][a]+N[a][a][ga],N[a][a][b]+N[a][a][gb],N[a][b][b]+N[a][b][gb],N[b][b][b]+N[b][b][gb],N[a][a][f],N[a][b][f],N[b][b][f],N[a][f][f],N[b][f][f],N[f][f][f]]
        expected=[0,3,4,8,1,2,4,2,3,4] if rad==3 else [3,3,4,4,2,2,2,2,3,2]
        require(bounds==expected,'Source-derived coefficient bounds')
        # The unsigned g=1 quotient must itself equal the displayed multiplication.
        representatives=[0,a,b,f];orbits=[[0,g],[a,ga],[b,gb],[f]]
        quotient=[s.Matrix([[sum(N[i][j][k] for k in orb) for orb in orbits] for j in representatives]).T for i in representatives]
        require(quotient==matrices(bounds),'Weighted quotient normalization')
        D=336+192*s.sqrt(3) if rad==3 else 240+96*s.sqrt(6)
        va,vb,vf=(4+2*s.sqrt(3),7+4*s.sqrt(3),6+4*s.sqrt(3)) if rad==3 else (4+2*s.sqrt(6),5+2*s.sqrt(6),6+2*s.sqrt(6))
        dims=[None]*7
        for i in [0,g]:dims[i]=s.Integer(1)
        for i in [a,ga]:dims[i]=va
        for i in [b,gb]:dims[i]=vb
        dims[f]=vf
        require(all(s.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(7)))==0 for i,j in itertools.product(range(7),repeat=2)),'Exact source FP dimensions')
        require(s.expand(sum(d*d for d in dims)-D)==0,'Exact global FP dimension')
        for i,j in itertools.product(range(7),repeat=2):
            require(G[i]*G[j]==sum((N[i][j][k]*G[k] for k in range(7)),s.zeros(7)),'Source associativity')
            for k in range(7):require(N[i][j][k]==N[dual[i]][k][j]==N[k][dual[j]][i],'Source Frobenius reciprocity')
        casimir=sum((G[i]*G[dual[i]] for i in range(7)),s.zeros(7));source_poly=s.factor(casimir.charpoly(x).as_expr())
        require(s.expand(source_poly.subs(x,D))==0,'D is a source formal codegree')
        unit=D/48
        require(s.expand(unit*unit.xreplace({s.sqrt(rad):-s.sqrt(rad)}))==1,'D/48 is an algebraic unit')
        if rad not in family:
            rows=[];survivors=[]
            for v in enumerate_quotients(bounds):
                M=matrices(v);require(all(p*q==q*p for p,q in itertools.combinations(M,2)),'Quotient associativity')
                Q=2*M[0]+2*M[1]**2+2*M[2]**2+M[3]**2
                poly=s.factor(Q.charpoly(x).as_expr());good=[]
                for factor,mul in s.factor_list(poly)[1]:
                    scaled=s.Poly(factor.subs(x,48*x),x).monic()
                    if all(c.q==1 for c in scaled.all_coeffs()):
                        good.append({'factor':str(factor),'multiplicity':mul,'delta_over_48_minpoly':str(scaled.as_expr())})
                        require(s.degree(factor,x)==2 and s.expand(factor.subs(x,D))==0,'Every admissible delta is FPdim or its conjugate')
                row={'coefficients':v,'signed_plus_Casimir':str(poly),'admissible_delta_factors':good}
                rows.append(row)
                if good:survivors.append(row)
            require(len(rows)==(8 if rad==3 else 11),'Complete bounded solution count')
            require(len(survivors)==(2 if rad==3 else 1),'Dimension-integrality survivor count')
            family[rad]={'bounds':bounds,'normalized_solutions':rows,'survivors':survivors,'conclusion':'global dimension is FPdim or quadratic conjugate'}
        cases.append({'id':rid,'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'g_a_b_f':[g,a,b,f],'radicand':rad,'FP_dimensions':list(map(str,dims)),'source_Casimir':str(source_poly),'D_over_48_unit':str(unit),'conclusion':'every categorification is Galois conjugate to a pseudo-unitary category','classification_status':'unresolved'})
    result={'status':'PASS','scope':'general_complex_to_Galois_pseudo_unitary','classification_changes':0,'cases':cases,'families':family,'optimizer_used':False,'proof':'THREE_CASE_GALOIS_PU.md'}
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
