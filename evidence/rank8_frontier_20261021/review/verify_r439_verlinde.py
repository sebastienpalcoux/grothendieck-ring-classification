#!/usr/bin/env python3
"""Independent raw-box/Gram/Verlinde review of the forced R439 rank-five dual."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import argparse
import hashlib
import itertools as it
import json
import math
import sympy as s

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
REPO=BASE.parents[1]
ZERO=(F(0),F(0));ONE=(F(1),F(0))

def need(x,message):
    if not x: raise ValueError(message)

def pair(a,b=0):return (F(a),F(b))
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def mul(x,y):return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(n,x):return (n*x[0],n*x[1])
def inv(x):
    n=x[0]*x[0]-3*x[1]*x[1]
    need(n!=0,'nonzero divisor')
    return (x[0]/n,-x[1]/n)
def div(x,y):return mul(x,inv(y))
def total(xs):
    v=ZERO
    for x in xs:v=add(v,x)
    return v
def value(chi,col):return total(scale(n,x)for n,x in zip(col,chi))
def norm(x):return x[0]*x[0]-3*x[1]*x[1]
def ai(x):return (2*x[0]).denominator==1 and norm(x).denominator==1
def nonnegative_integer(x):return x[1]==0 and x[0].denominator==1 and x[0]>=0
def encode(x):return [str(c)for c in x]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def psd(M):
    # All principal minors, without native Gram enumeration or eigenvalue floats.
    return all(M.extract(ix,ix).det()>=0 for k in range(1,M.rows+1)
               for ix in it.combinations(range(M.rows),k))

def gram_patterns(Q,H,allowed):
    """Memoized coefficient extraction for the nonnegative Gram generating series."""
    ij=list(it.combinations_with_replacement(range(4),2))
    order=sorted(allowed,key=lambda i:(next(j for j,x in enumerate(H[i])if x),H[i]))
    vv=[tuple(H[i][j]*H[i][k]for j,k in ij)for i in order]
    last=[max((at for at,v in enumerate(vv)if v[k]),default=-1)for k in range(10)]
    @lru_cache(None)
    def solve(at,residual):
        if any(x<0 for x in residual):return ()
        if any(x and last[k]<at for k,x in enumerate(residual)):return ()
        if at==len(order):return ((),)if not any(residual)else()
        v=vv[at]
        bound=min(x//z for x,z in zip(residual,v)if z)
        answers=[]
        for m in range(bound+1):
            tail=tuple(x-m*z for x,z in zip(residual,v))
            answers.extend((m,)+a for a in solve(at+1,tail))
        return tuple(answers)
    compressed=solve(0,tuple(int(Q[i,j])for i,j in ij))
    answers=[]
    for row in compressed:
        full=[0]*len(H)
        for i,m in zip(order,row):full[i]=m
        answers.append(tuple(full))
    need(len(answers)==len(set(answers)),'no duplicate Gram coefficient terms')
    return sorted(answers),solve.cache_info().currsize

def group_control():
    """All 27 distinguished Verlinde coefficients in the actual center Z(Rep S3)."""
    dims=[1,1,2];chars=[[1,1,2],[1,-1,0],[1,1,-1]];f=[6,2,3]
    # Conjugacy-class/centralizer induction: three distinguished objects,
    # plus sign, three copies of V, and sign+V.
    restrictions=[((1,0,0),1),((1,0,1),1),((1,1,0),1),
                  ((0,1,0),1),((0,0,1),3),((0,1,1),1)]
    need(sum(m*sum(v*d for v,d in zip(col,dims))**2 for col,m in restrictions)==36,'S3 center dimension')
    values=[]
    for E,G,J in it.product(range(3),repeat=3):
        summation=sum(F(m*math.prod(sum(v*x for v,x in zip(col,chars[k]))for k in (E,G,J)),
                         sum(v*d for v,d in zip(col,dims)))for col,m in restrictions)
        z=F(6,f[E]*f[G]*f[J])*summation
        need(z.denominator==1 and z>=0,'known S3 distinguished Verlinde coefficient')
        if E==0:need(z==int(G==J),'known unit fusion normalization')
        values.append(int(z))
    need(values[-1]==1,'known nonzero cubic control')
    return {'known_category':'Z(Rep(S3))','distinguished_triple_count':27,
            'all_coefficients':values,'last_nontrivial_cubic':1}

def compute():
    binding_path=BASE/'structural_models/rank5_route_bindings.json'
    binding=next(r for r in json.loads(binding_path.read_text())['records']if r['route_tensor']=='S3_dual_selfdual_a3')
    R=binding['constructor_tensor'];n=5
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(digest=='84487a759f44be4a988082680fa8c3b28bcd0d159d639f38409825e19c5761e6','source tensor')
    need(R==binding['rank5_source_tensor'],'source based isomorphism')
    need(all(R[i][j]==R[j][i]and R[i][j][0]==int(i==j)for i,j in it.product(range(n),repeat=2)),'commutative selfdual source')
    matrices=[s.Matrix(n,n,lambda k,j:R[i][j][k])for i in range(n)]
    G=sum((M*M for M in matrices),s.zeros(n))
    need(G==s.Matrix([[5,1,3,6,6],[1,5,3,6,6],[3,3,9,12,12],[6,6,12,44,40],[6,6,12,40,44]]),'induction Gram from tensor')
    ds=[ONE,ONE,pair(2),pair(3,2),pair(3,2)]
    chars=[ds,[ONE,ONE,pair(2),pair(3,-2),pair(3,-2)],
           [ONE,ONE,pair(-1),ZERO,ZERO],[ONE,pair(-1),ZERO,ONE,pair(-1)],
           [ONE,pair(-1),ZERO,pair(-1),ONE]]
    for chi in chars:
        need(all(mul(chi[i],chi[j])==value(chi,R[i][j])for i,j in it.product(range(n),repeat=2)),'explicit character homomorphism')
    f=[total(mul(x,x)for x in chi)for chi in chars];D=f[0]
    need(f==[pair(48,24),pair(48,-24),pair(3),pair(4),pair(4)],'complete codegrees')
    need(all(total(mul(x,y)for x,y in zip(chars[i],chars[j]))==(f[i]if i==j else ZERO)
             for i,j in it.product(range(n),repeat=2)),'five independent characters')
    beta=[div(D,x)for x in f]
    boxes=[range(math.isqrt(int(G[i,i]))+1)for i in range(1,n)]
    candidates=[tuple((1,)+v)for v in it.product(*boxes)]
    domains=[[c for c in candidates if value(ds,c)==beta[i]]for i in range(1,n)]
    low=[];row_pass=0;psd_pass=0
    for cols in it.product(*domains):
        if cols[-2]>cols[-1]:continue
        full=((1,0,0,0,0),)+cols
        if tuple(map(sum,zip(*full)))!=tuple(G[0,j]for j in range(n)):continue
        row_pass+=1
        L=s.Matrix.hstack(*map(s.Matrix,full));remaining=G-L*L.T
        if not psd(remaining):continue
        psd_pass+=1
        good=[]
        for perm in [(0,1,2,3,4),(0,1,2,4,3)]:
            S=[[mul(beta[i],value(chars[i],full[perm[j]]))for j in range(n)]for i in range(n)]
            if all(S[i][j]==S[j][i]for i,j in it.product(range(n),repeat=2)):good.append(perm)
        if good:low.append((full,remaining,good))
    need(len(low)==1 and len(low[0][2])==2,'unique full-S frame and both equal-codegree labels')
    cols,remaining,perms=low[0];Q=remaining.extract(range(1,n),range(1,n))
    H=[];raw_gram_count=0
    for v in it.product(*(range(math.isqrt(int(Q[i,i]))+1)for i in range(4))):
        if not any(v):continue
        residual=Q-s.Matrix(v)*s.Matrix(v).T
        if any(x<0 for x in residual)or not psd(residual):continue
        raw_gram_count+=1;z=value(ds,(0,)+v)
        if not ai(div(D,z)):continue
        if z[1] and ((2*z[0])**2/norm(z)).denominator!=1:continue
        H.append(v)
    need(len(H)==38,'independent full high-box domain')
    integral=[i for i,v in enumerate(H)if value(ds,(0,)+v)[1]==0]
    spectral=[]
    for i,v in enumerate(H):
        z=value(ds,(0,)+v)
        for E in range(n):
            eigenvalue=div(mul(beta[E],value(chars[E],(0,)+v)),z)
            if not ai(eigenvalue):
                spectral.append((i,E,encode(eigenvalue)));break
    need(integral==[9,17,19,27]and[s[0]for s in spectral]==[37],'necessary filters')
    allowed=[i for i in range(len(H))if i not in integral+[r[0]for r in spectral]]
    patterns,state_count=gram_patterns(Q,H,allowed)
    primary=json.loads((BASE/'rank5_integer_gram/results.json').read_text())
    need([list(v)for v in H]==primary['high_vectors'],'independent high-vector agreement')
    need([list(c)for c in cols]==primary['low_columns'],'independent low-frame agreement')
    need([list(m)for m in patterns]==primary['solutions']and len(patterns)==58,'independent complete integer coefficient extraction')
    cubic=[];hist=Counter()
    for m in patterns:
        restrictions=[(c,1)for c in cols]+[((0,)+v,mv)for v,mv in zip(H,m)if mv]
        first=total(scale(mult,div(mul(mul(value(chars[1],c),value(chars[1],c)),value(chars[1],c)),value(ds,c)))for c,mult in restrictions)
        coefficient=mul(div(D,mul(mul(f[1],f[1]),f[1])),first)
        Srow=[(mul(beta[1],value(chars[1],c)),value(ds,c),mult)for c,mult in restrictions]
        direct=div(total(scale(mult,div(mul(mul(x,x),x),z))for x,z,mult in Srow),mul(D,D))
        need(direct==coefficient,'two Verlinde normalizations')
        need(total(scale(mult,mul(x,x))for x,z,mult in Srow)==mul(D,D),'distinguished S-row orthogonality')
        need(not nonnegative_integer(coefficient),'every pattern fails cubic integrality')
        hist[tuple(encode(coefficient))]+=1;cubic.append(encode(coefficient))
    expected={('7/6','-1/6'):16,('1/3','0'):16,('19/12','-5/12'):16,('2','-1/3'):6,('1/3','2/3'):4}
    need(dict(hist)==expected,'independent radical-basis coefficient histogram')
    inputs=[binding_path,BASE/'rank5_integer_gram/verify.py',BASE/'rank5_integer_gram/results.json',
            BASE/'r439_centerless_rank5/verify.py',BASE/'r439_centerless_rank5/verlinde_exclusion.py',
            BASE/'r439_centerless_rank5/verlinde_exclusion.json',HERE/'INTEGRAL_CENTER_SUBCATEGORY.md',
            BASE/'structural_models/pointed_s3_scope.json',BASE/'structural_models/s3_full_condensation.json',
            BASE/'noncommutative_followup/additional_scope_gates.json']
    return {'kind':'independent_complete_domain_and_cubic_Verlinde_review_R439',
            'source_sha256':{str(p.relative_to(REPO)):sha(p)for p in inputs},
            'rank5_tensor_sha256':digest,'low_column_counts':list(map(len,domains)),
            'unit_row_compatible_low_frames':row_pass,'positive_semidefinite_low_frames':psd_pass,
            'full_S_low_frames':1,'symmetric_labelings':2,'low_columns':cols,
            'raw_high_Gram_columns':raw_gram_count,'high_columns':H,
            'integral_center_forbidden':integral,'spectral_forbidden':spectral,
            'independent_integer_pattern_count':len(patterns),'memoized_Gram_states':state_count,
            'all_cubic_coefficients_in_basis_1_sqrt3':cubic,
            'cubic_histogram':[{'value':list(k),'count':v}for k,v in sorted(hist.items())],
            'known_model_control':group_control(),
            'result':'PASS; conditional rank-five obstruction and, with the separately verified scope chain, general R439 exclusion'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result=json.loads(json.dumps(compute(),default=int));path=HERE/'r439_verlinde_direct.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'independent review receipt mismatch')
    print('PASS: independent R439 raw low/high boxes, complete 58 integer patterns, exact cubic obstruction, and 27 known-model control coefficients.')
