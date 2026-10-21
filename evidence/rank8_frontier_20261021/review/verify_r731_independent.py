#!/usr/bin/env python3
"""Independent, read-only R731 low-frame and exact-ray verification.

Imports no discovery or producer code. Rebuilds the Gram matrix, low
restriction sets, complete row-sum frames, allowed high columns, and
Ramanujan-averaged joint tensor-rotation equations from the source tensor.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib,itertools,json,math
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
STAGE=HERE.parent
DIM=[1,5,5,10,10,11,12,12]
FP=660
SOURCE='ee54e287f01aec4e2079b7f66309d89a659742e38164a3e47de1fea650eec48b'

def need(ok,text):
    if not ok: raise ValueError(text)

def sha(value): return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def psd(A):
    """Rational LDL elimination, including zero pivots; no native arithmetic."""
    A=[[F(z) for z in row] for row in A]
    for k in range(len(A)):
        p=A[k][k]
        if p<0: return False
        if not p:
            if any(A[k][j] for j in range(k+1,len(A))): return False
            continue
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                A[i][j]=A[j][i]=A[i][j]-A[i][k]*A[k][j]/p
    return True

def vectors(Q,weights,targets,first=None):
    """Exact prefix ellipsoid enumeration with rational inverse matrices.

Here all Gram matrices are positive definite, independently checked by
Sylvester's criterion. Prefix inverse tests describe necessary Schur
complement ellipsoids and the final test is sufficient for Q-vv^T PSD.
"""
    n=len(Q); inverses=[]
    for k in range(1,n+1):
        M=s.Matrix([row[:k] for row in Q[:k]])
        need(M.det()>0,'Gram must be positive definite')
        inverse=M.inv();den=math.lcm(*(int(x.q) for x in inverse))
        inverses.append(([[int(x*den) for x in row] for row in inverse.tolist()],den))
    bounds=[math.isqrt(Q[i][i]) for i in range(n)]
    targets=set(targets); maximum=max(targets); out=[];v=[]
    def visit(k,weight):
        if k==n:
            if weight in targets and any(v): out.append(tuple(v))
            return
        choices=[first] if k==0 and first is not None else range(min(bounds[k],(maximum-weight)//weights[k])+1)
        A,denominator=inverses[k]
        old=sum(v[i]*A[i][j]*v[j] for i in range(k) for j in range(k))
        cross=sum(A[k][i]*v[i] for i in range(k))*2
        for z in choices:
            if any(z*v[j]>Q[k][j] for j in range(k)):continue
            if old+cross*z+A[k][k]*z*z>denominator:continue
            v.append(z);visit(k+1,weight+weights[k]*z);v.pop()
    visit(0,0)
    return out

def gram_difference(B,columns):
    return [[B[i][j]-sum(v[i]*v[j] for v in columns) for j in range(len(B))] for i in range(len(B))]

def low_frames(sets,B):
    """Fixed 3+4 meet-in-the-middle, without the producer's PSD/Cauchy pruning."""
    target=B[0][1:];unit=(1,0,0,0,0,0,0,0)
    def tuples(side):
        for chosen in itertools.product(*(sets[i] for i in side)):
            if any(sets[side[i]]==sets[side[j]] and chosen[i]>chosen[j] for i in range(len(side)) for j in range(i+1,len(side))):continue
            total=tuple(sum(v[k] for v in chosen) for k in range(1,8))
            if all(x<=t for x,t in zip(total,target)):yield total,chosen
    buckets=defaultdict(list)
    for total,chosen in tuples([0,1,2]):buckets[total].append(chosen)
    found=[];matches=0
    for total,right in tuples([3,4,5,6]):
        key=tuple(t-x for t,x in zip(target,total))
        for left in buckets.get(key,[]):
            cols=(unit,)+left+right;matches+=1;Q=gram_difference(B,cols)
            if any(x<0 for row in Q for x in row):continue
            if psd([row[1:] for row in Q[1:]]):found.append(cols)
    need(len(found)==len(set(found)),'duplicate low frame')
    return sorted(found),matches

def ramanujan(order,power):
    # Divisor-sum formula, independent of producer's reduced-order formula.
    return F(sum(int(d*s.mobius(order//d)) for d in s.divisors(math.gcd(order,power))),int(s.totient(order)))

def primitive(row,rhs):
    denominator=math.lcm(F(rhs).denominator,*(F(v).denominator for v in row.values()))
    row={j:int(v*denominator) for j,v in row.items() if v};rhs=int(rhs*denominator)
    divisor=math.gcd(rhs,*row.values()) or 1
    return {j:v//divisor for j,v in row.items()},rhs//divisor

def check_ray(rows,rhs,ray,nvars):
    need(len(rows)==len(rhs)==len(ray),'ray size')
    need(all(type(y) is int for y in ray),'integer ray')
    totals=[0]*nvars;bty=0
    for row,b,y in zip(rows,rhs,ray):
        row,b=primitive(row,b);bty+=b*y
        if y:
            for j,a in row.items():totals[j]+=a*y
    need(min(totals,default=0)>=0 and bty<0,'exact Farkas inequalities')
    return {'columns':nvars,'rows':len(rows),'minimum_column_pairing':min(totals,default=0),'rhs_pairing':bty}

def rotation_rows(R,B,cols,high):
    height=6;bound=19800
    types=sorted({tuple(ramanujan(order,k) for k in range(1,height+1)) for order in s.divisors(bound)}|{(F(0),)*height})
    need(len(types)==53,'trace types')
    labels=[(v,z,t) for v,z in high for t in types];nextvar=len(labels)
    Q=[row[1:] for row in gram_difference(B,cols)[1:]]
    LL=[[B[i][j]-gram_difference(B,cols)[i][j] for j in range(8)] for i in range(8)]
    low=[sum(LL[i][j]*DIM[j] for j in range(8)) for i in range(8)]
    need(low[0]==FP,'low dimension')
    rows=[];rhs=[]
    for i,j in itertools.combinations_with_replacement(range(7),2):
        rows.append({k:v[i]*v[j] for k,(v,z,t) in enumerate(labels) if v[i]*v[j]});rhs.append(Q[i][j])
    ep=[0,0,0,0,1,1,1]
    for power in [1,2]:
        for i in range(7):
            rows.append({k:v[i]*z*t[power-1] for k,(v,z,t) in enumerate(labels) if v[i]*z*t[power-1]});rhs.append((FP*ep[i] if power==2 else 0)-low[i+1])
            rows.append({});rhs.append(0)
    for obj in range(1,8):
        powers=[[1]+[0]*7]
        for order in range(1,7):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
        for order in range(3,7):
            divisors=[int(r) for r in s.divisors(order) if r<order]
            rotations=sorted({tuple(ramanujan(d,r) for r in divisors) for d in s.divisors(order)})
            offset=nextvar;nextvar+=len(rotations)
            rows.append({offset+k:1 for k in range(len(rotations))});rhs.append(powers[order][0])
            for at,r in enumerate(divisors):
                row={}
                for k,(v,z,t) in enumerate(labels):
                    value=-sum(powers[r][i]*v[i-1] for i in range(1,8))*z*t[order//r-1]
                    if value:row[k]=value
                row.update({offset+k:FP*t[at] for k,t in enumerate(rotations) if t[at]})
                rows.append(row);rhs.append(sum(powers[r][i]*low[i] for i in range(8)))
                rows.append({});rhs.append(0)
    return rows,rhs,nextvar

def run():
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    R=next(x['tensor'] for x in census if x['id']=='R8_3_731')
    need(sha(R)==SOURCE,'source fingerprint')
    du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    need(all(sum(R[i][j][k]*DIM[k] for k in range(8))==DIM[i]*DIM[j] for i in range(8) for j in range(8)),'dimension character')
    B=[[sum(R[u][j][v]*R[v][du[u]][i] for u in range(8) for v in range(8)) for i in range(8)] for j in range(8)]
    targets=[165,132,132,60,60,55,55]
    t=s.Symbol('t');need(s.Matrix(B).charpoly(t).as_expr()==s.expand((t-660)*(t-4)*(t-5)**2*(t-11)**2*(t-12)**2),'complete formal codegrees')
    lowvectors=vectors(B,DIM,set(targets),first=1)
    print('independent low vectors complete',len(lowvectors),flush=True)
    sets=[sorted(v for v in lowvectors if sum(d*x for d,x in zip(DIM,v))==target) for target in targets]
    saved=json.loads((STAGE/'integral/central_731_sieve.json').read_text())
    need(list(map(len,sets))==saved['column_counts'],'independent low restriction sets')
    frames,matches=low_frames(sets,B)
    print('independent row-sum and PSD frames complete',matches,len(frames),flush=True)
    need(json.loads(json.dumps(frames))==saved['frames'],'independent complete low-frame list')
    counts=Counter();ray_reports=[];rot=json.loads((STAGE/'integral/central_731_rotation_h6.json').read_text())
    allowed=[int(d) for d in s.divisors(FP) if d>1 and len(s.factorint(d))>1]
    for ix,cols in enumerate(frames):
        record=saved['records'][ix]
        if Counter(cols)!=Counter(tuple(v[j] for j in du) for v in cols):
            need(record['outcome']=='duality_failure','duality case');counts['duality']+=1;continue
        Q=[row[1:] for row in gram_difference(B,cols)[1:]]
        high=sorted((v,sum(d*x for d,x in zip(DIM[1:],v))) for v in vectors(Q,DIM[1:],allowed))
        need(len(high)==record['high_columns_after'],'independent high restriction enumeration')
        if record['outcome']=='gram_obstruction':
            pairs=list(itertools.combinations_with_replacement(range(7),2))
            # Producer Gram rows are unnormalized; preserve its ray convention.
            ray=record['ray'];sums=[sum(ray[k]*v[i]*v[j] for k,(i,j) in enumerate(pairs)) for v,z in high]
            bty=sum(ray[k]*Q[i][j] for k,(i,j) in enumerate(pairs))
            need(min(sums,default=0)>=0 and bty<0,'independent Gram ray');counts['gram']+=1
            ray_reports.append({'low_index':ix,'kind':'gram','columns':len(high),'minimum_column_pairing':min(sums,default=0),'rhs_pairing':bty})
        else:
            need(record['outcome']=='gram_not_excluded','unexpected case')
            item=next(r for r in rot['records'] if r['low_index']==ix)
            rows,rhs,nvars=rotation_rows(R,B,cols,high)
            ray_reports.append({'low_index':ix,'kind':'rotation',**check_ray(rows,rhs,item['ray'],nvars)})
            counts['rotation']+=1
        print('checked low frame',ix,record['outcome'],flush=True)
    need(dict(counts)=={'duality':434,'gram':13,'rotation':3},'complete branch counts')
    return {'id':'R8_3_731','tensor_sha256':SOURCE,'independent_imports':True,
            'low_column_counts':list(map(len,sets)),'row_sum_frames_before_psd':matches,
            'complete_psd_frames':len(frames),'excluded_counts':dict(counts),'exact_ray_checks':ray_reports}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=run();path=HERE/'r731_independent.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(path.read_text())==result,'independent receipt changed')
    print('PASS: independent complete R731 frame enumeration and all 16 exact rays')
