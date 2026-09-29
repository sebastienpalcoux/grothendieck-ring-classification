#!/usr/bin/env python3
"""Exact arithmetic certificate for the unrestricted exclusion of R6_7_3582.

The categorical reductions and the all-orders Gauss-sum lemma are proved in
proof.tex. This program verifies the ring, every displayed algebraic identity,
and the two exhaustive finite induction-column enumerations. It does NOT
assume the earlier pseudo-unitary exclusion, enumerate pentagons, use numerical
optimization, or claim that Python is a formalization of fusion category theory.

Run: python verify.py --output verification.json
Also valid under python -O: no proof checks rely on assert statements.
Requires Python >=3.10 and SymPy (tested with 1.14.0).
"""
from __future__ import annotations
import argparse
import hashlib
import itertools as it
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path
import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def psd(rows: list[list[int | F]]) -> bool:
    """Exact positive-semidefiniteness by successive Schur complements."""
    a = [list(map(F, row)) for row in rows]
    if any(a[i][i] < 0 for i in range(len(a))):
        return False
    pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
    if pivot is None:
        return all(x == 0 for row in a for x in row)
    ix = [i for i in range(len(a)) if i != pivot]
    q = a[pivot][pivot]
    return psd([[a[i][j] - a[i][pivot]*a[pivot][j]/q for j in ix] for i in ix])


def verify_ring(N: list, report: dict) -> s.Matrix:
    require(len(N) == 6 and all(len(a) == 6 and all(len(b) == 6 for b in a) for a in N), 'shape')
    require(all(type(x) is int and x >= 0 for a in N for b in a for x in b), 'integer positivity')
    require(max(x for a in N for b in a for x in b) == 7, 'multiplicity')
    for i,j,k in it.product(range(6), repeat=3):
        require(N[i][j][k] == N[j][i][k] == N[i][k][j], 'Frobenius symmetry')
        require(N[0][i][j] == int(i == j), 'unit')
        require(N[i][j][0] == int(i == j), 'self-duality')
    require(all(5 <= N[i][j][k] <= 7 for i,j,k in it.product(range(1,6), repeat=3)), 'nonunit range')
    mats = list(map(s.Matrix, N))
    for i,j in it.product(range(6), repeat=2):
        require(mats[i]*mats[j] == sum((N[i][j][k]*mats[k] for k in range(6)), s.zeros(6)), 'associativity')
    r=s.sqrt(226); p=(1+s.sqrt(5))/2; q=(1-s.sqrt(5))/2
    C=s.Matrix([[1,14+r,14+r,15+r,16+r,16+r], [1,14-r,14-r,15-r,16-r,16-r],
                [1,p,q,-1,0,0], [1,q,p,-1,0,0], [1,0,0,1,-p,-q], [1,0,0,1,-q,-p]])
    for h,i,j in it.product(range(6), repeat=3):
        require(s.simplify(C[h,i]*C[h,j]-sum(N[i][j][k]*C[h,k] for k in range(6))) == 0, 'character identity')
    require(s.simplify(C.det()+250*r) == 0, 'character completeness')
    D=2260+150*r; expected=[D,2260-150*r,5,5,5,5]
    require(all(s.simplify(sum(C[h,i]**2 for i in range(6))-expected[h])==0 for h in range(6)), 'codegrees')
    G=sum((m*m for m in mats),s.zeros(6))
    j=s.ones(5,1); delta=s.Matrix([-1,-1,0,1,1])
    tail=5*s.eye(5)+901*j*j.T+30*(j*delta.T+delta*j.T)+delta*delta.T
    require(G[1:,1:]==tail and G[0,0]==6 and G[1:,0]==30*j+delta, 'Casimir formula')
    require(s.trace(G)==4540, 'trace budget')
    report['ring']={'rank':6,'multiplicity':7,'character_determinant':'-250*sqrt(226)',
                    'formal_codegrees':['2260+150*sqrt(226)','2260-150*sqrt(226)',5,5,5,5],
                    'Casimir_matrix':G.tolist(),'Casimir_trace':4540}
    return G


def verify_signed_reduction(N: list, report: dict) -> None:
    E=[s.eye(6)[:,i] for i in range(6)]
    red=lambda x:x.applyfunc(lambda y:int(y)%2)
    def mul(x,y):
        return red(sum((x[i]*y[j]*s.Matrix(N[i][j]) for i,j in it.product(range(6),repeat=2)),s.zeros(6,1)))
    one,a,b,c,d,e=E
    ell=red(a+b); h=red(d+e); e0=red(one+ell+h)
    u=red(one+a+c); v=red(one+c+d); z=red(one+c)
    idempotents=[e0,ell,h]
    for x in idempotents:
        require(mul(x,x)==x, 'mod-2 idempotent')
        require(len({tuple(mul(x,s.Matrix(w))) for w in it.product(range(2),repeat=6)})==4, 'rank-two factor')
    for x,y in it.combinations(idempotents,2):
        require(mul(x,y)==s.zeros(6,1), 'orthogonal mod-2 idempotents')
    require(mul(ell,a)==u and mul(u,u)==red(u+ell), 'first F4 factor')
    require(mul(h,d)==v and mul(v,v)==red(v+h), 'second F4 factor')
    require(mul(e0,z)==z and mul(z,z)==s.zeros(6,1), 'dual-number factor')
    require(s.Matrix.hstack(e0,z,ell,u,h,v).det()%2==1, 'mod-2 product basis')
    r=s.sqrt(226); S,B=s.symbols('S B');D=2260+150*r
    require(s.simplify((452*S+2*B*r)/D-((226*S-15*B)+(B-15*S)*r)/5)==0,'dimension ratio')
    require([(u,v) for u,v in it.product(range(5),repeat=2) if (226*u-15*v)%5==0 and (v-15*u)%5==0]==[(0,0)], 'mod-5 integrality')
    require(904*5+4 < 4540 < 904*6+4, 'S bound')
    require(4540-4*(5-1)==4520+4, 'strict trace saturation gap')
    Bmat=s.Matrix([[N[i][i][k] for k in range(1,6)] for i in range(1,6)])
    half=Bmat*s.ones(5,1)/2
    require(list(half)==[14,14,15,16,16] and sum(x*x for x in half)==226*5-1,'square-row saturation')
    # An independent finite check of the last elementary norm argument.
    beta_vectors=[b for b in it.product(range(-2,3),repeat=5) if sum(x*x for x in b)==5]
    solutions=[]
    for beta in beta_vectors:
        rhs=Bmat*s.Matrix(beta)
        if any(beta[i]==0 and rhs[i]!=0 for i in range(5)):continue
        require(all(beta), 'unexpected zero-coordinate solution')
        alpha=[rhs[i]/(2*beta[i]) for i in range(5)]
        if any(x.q!=1 for x in alpha) or sum(x*x for x in alpha)!=1129:continue
        solutions.append({'alpha':list(map(int,alpha)),'beta':list(beta)})
    require(solutions==[{'alpha':[14,14,15,16,16],'beta':[-1]*5},{'alpha':[14,14,15,16,16],'beta':[1]*5}], 'dimension solutions')
    report['signed_reduction']={'mod2_factors':['F2[z]/(z^2)','F4','F4'],
        'ramified_quadratic':'Q_2(sqrt(226))','quadratic_dimension_norm_parameter':5,
        'square_coefficients':Bmat.tolist(),'norm5_vectors_checked':len(beta_vectors),'dimension_solutions':solutions}


# Twice the four codegree-five characters, in coordinates (1,sqrt(5)).
SMALL_CHARS=[[(2,0),(1,1),(1,-1),(-2,0),(0,0),(0,0)],
             [(2,0),(1,-1),(1,1),(-2,0),(0,0),(0,0)],
             [(2,0),(0,0),(0,0),(2,0),(-1,-1),(-1,1)],
             [(2,0),(0,0),(0,0),(2,0),(-1,1),(-1,-1)]]


def labellings(columns: list[tuple]) -> list[tuple]:
    values=[[tuple(sum(c[k]*row[k][a] for k in range(6)) for a in range(2)) for c in columns] for row in SMALL_CHARS]
    return [p for p in it.permutations(range(4)) if all(values[p[i]][j]==values[p[j]][i] for i,j in it.product(range(4),repeat=2))]


def low_branches(G: s.Matrix, report: dict) -> list[dict]:
    delta=(-1,-1,0,1,1)
    norm=lambda v:sum(x*x for x in v)
    ws=[v for v in it.product(range(-3,4),repeat=5) if sum(v)==0 and sum(delta[i]*v[i] for i in range(5))==1 and norm(v)<=10]
    require(len(ws)==32, 'number of bounded low deviations')
    stages=[0,0,0,0]; branches=[]
    for inds in it.combinations_with_replacement(range(len(ws)),4):
        w=[ws[i] for i in inds]
        if sum(map(norm,w))>16 or any(sum(v[i] for v in w)!=delta[i] for i in range(5)):continue
        stages[0]+=1
        cols=[(1,)+tuple(6+x for x in v) for v in w]
        labs=labellings(cols)
        if not labs:continue
        stages[1]+=1
        full=[(1,0,0,0,0,0),(1,6,6,6,6,6)]+cols
        Q=[[int(G[i,j])-sum(c[i]*c[j] for c in full) for j in range(6)] for i in range(6)]
        if any(x<0 for row in Q for x in row):continue
        stages[2]+=1
        if not psd(Q):continue
        stages[3]+=1
        branches.append({'columns':full,'labellings':labs,'Q':Q})
    require(stages==[59,11,11,3], 'exhaustive low-stage counts')
    report['low_enumeration']={'deviation_vectors':len(ws),'stages':stages,'stage_meanings':['sum and norm','modular reciprocity','entrywise Gram positivity','positive-semidefinite Gram'], 'branches':branches}
    return branches


def high_columns(branch: dict) -> tuple[list[tuple], list[int]]:
    Q=s.Matrix(branch['Q'])[1:,1:]; rank=Q.rank()
    ix=next(ii for ii in it.combinations(range(5),rank) if Q.extract(ii,ii).det()!=0)
    sub=Q.extract(ix,ix);adj=[[int(x) for x in row] for row in sub.adjugate().tolist()];det=int(sub.det())
    null=[]
    for z in Q.nullspace():
        den=math.lcm(*(int(x.q) for x in z));null.append([int(x*den) for x in z])
    entries=[[int(x) for x in row] for row in Q.tolist()]
    caps=[math.isqrt(entries[i][i]) for i in range(5)]
    da=math.isqrt(entries[0][0]+entries[1][1]-2*entries[0][1])
    de=math.isqrt(entries[3][3]+entries[4][4]-2*entries[3][4])
    require(Q*s.Matrix([1,1,-4,1,1])==s.zeros(5,1), 'common null equation')
    result=[];counts=[0,0,0]
    # The common null equation determines c; two difference inequalities
    # follow from Q-vv^T >=0. Thus this box includes EVERY possible column.
    for a,d,x,y in it.product(range(caps[0]+1),range(caps[3]+1),range(-da,da+1),range(-de,de+1)):
        b=a+x;e=d+y;total=a+b+d+e
        if not(0<=b<=caps[1] and 0<=e<=caps[4]) or total%4:continue
        c=total//4
        if c>caps[2]:continue
        v=(a,b,c,d,e)
        if not any(v):continue
        counts[0]+=1
        if any(sum(v[i]*z[i] for i in range(5)) for z in null):continue
        vv=[v[i] for i in ix]
        if sum(vv[i]*adj[i][j]*vv[j] for i,j in it.product(range(rank),repeat=2))>det:continue
        if any(v[i]*v[j]>entries[i][j] for i in range(5) for j in range(i,5)):continue
        counts[1]+=1
        ar=sum(v[i]*[14,14,15,16,16][i] for i in range(5));br=sum(v)
        norm=ar*ar-226*br*br
        if norm==0:continue
        qr=F(2260*ar-226*150*br,norm);qs=F(150*ar-2260*br,norm)
        # D/dim(Y) is integral; trace/norm is an exact quadratic integrality test.
        if (2*qr).denominator!=1 or (qr*qr-226*qs*qs).denominator!=1:continue
        counts[2]+=1;result.append(v)
    return sorted(result),counts


def verify_pseudo_unitary(G: s.Matrix, report: dict) -> None:
    branches=low_branches(G,report);j=s.ones(5,1);delta=s.Matrix([-1,-1,0,1,1]);E=[s.eye(5)[:,i] for i in range(5)]
    hs=[];counts=[]
    for b in branches:
        high,stages=high_columns(b);hs.append(high);counts.append(stages)
    require(counts==[[377,48,2],[4483,236,18],[377,48,2]], 'high-column enumeration counts')
    require(hs[0]==hs[2]==[(1,1,1,1,1),(2,2,2,2,2)], 'outer-branch high columns')
    require(s.Matrix(branches[0]['Q'])[1:,1:].rank()==2 and s.Matrix(branches[2]['Q'])[1:,1:].rank()==2, 'outer rank contradictions')
    expected=[tuple(k*j) for k in (1,2)]
    expected += [tuple(k*j+sg*(E[a]-E[b])) for k in (1,2) for sg in (-1,1) for a,b in [(0,1),(3,4)]]
    expected += [tuple(k*j-E[a]+E[b]) for k in (6,12) for a in (0,1) for b in (3,4)]
    require(sorted(expected)==hs[1], 'middle high-column families')
    Q=s.Matrix(branches[1]['Q'])[1:,1:];u=E[0]-E[1];v=E[3]-E[4]
    bil=lambda x,y:int((x.T*Q*y)[0])
    require([bil(delta,delta),bil(delta,j),bil(u,u),bil(v,v),bil(delta,u),bil(delta,v),bil(u,v)]==[32,480,8,8,0,0,0], 'Gram count identities')
    B=[6*j-E[a]+E[b] for a in (0,1) for b in (3,4)]
    require(Q-2*sum((b*b.T for b in B),s.zeros(5))==434*j*j.T, 'uniform Gram remainder')
    r=s.sqrt(226);U=15+r;z=U**2;t=z+1;w=5*U
    require(s.simplify(z-(451+30*r))==0 and s.simplify(t-(452+30*r))==0, 'central dimensions')
    require(s.simplify((-6*z-12*t)/w-(-18-6*r))==0, 'first twist identity reduction')
    require(s.totient(904)==448 and F(2,448)==F(1,224), 'Gauss coefficient bound')
    require(434<6*224==1344, 'final contradiction')
    report['pseudo_unitary_exclusion']={'high_stage_counts':counts,'high_columns':hs,
        'outer_branches':'rank(Q)=2 but all admissible columns are parallel',
        'middle_branch_B_multiplicities':[2,2,2,2],'uniform_weight':434,
        'required_root_sum':'-18-6*sqrt(226)','minimum_root_count_from_Gauss_bound':1344,
        'higher_indicators_used':False,'old_exclusion_certificate_used':False}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);here=Path(__file__).resolve().parent
    p.add_argument('--input',type=Path,default=here/'ring.json');p.add_argument('--output',type=Path,default=here/'verification.json')
    args=p.parse_args();start=time.monotonic();raw=args.input.read_bytes();data=json.loads(raw)
    report={'id':data['id'],'input_sha256':hashlib.sha256(raw).hexdigest(),'sympy_version':s.__version__}
    G=verify_ring(data['N'],report);verify_signed_reduction(data['N'],report);verify_pseudo_unitary(G,report)
    report.update(result='PASS',seconds=round(time.monotonic()-start,4),scope='Exact finite arithmetic for the proof in proof.tex; categorical and all-orders number-theoretic arguments are proved in the text.')
    args.output.write_text(json.dumps(report,indent=2,default=lambda x:int(x))+'\n')
    print('PASS: ring, characters, mod-2 algebra, dimension arithmetic, all low/high columns, Gram identities, and 434 < 1344.')
    print(f'Elapsed: {report["seconds"]} seconds. Report: {args.output}')
if __name__=='__main__':
    main()
