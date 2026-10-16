#!/usr/bin/env python3
"""Exact source-bound quadratic center trace obstruction; standard library only.
No optimizer is imported or called.  The finite certificate consists solely of
integer separating covectors; every domain and every matrix is reconstructed.
"""
import argparse,collections,functools,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path

TARGETS={
 'R7_4_106':{'rad':3,'labels':[1,2,3,6], 'sha':'bb2c9203bd767a0cc9665b5a32cf532226d79d48d1a9ab3c00733e470de7b1aa','other_field':2,'separating_factors':[[1,-1860],[1,66],[1,494],[1,-16448,-12738752],[1,-124,-171388]]},
 'R7_4_2155':{'rad':3,'labels':[3,1,5,4], 'sha':'221cd17606540aa298594ad057adeb294447409679625811588adac87f27676b','other_field':-2,'separating_factors':[[1,-1314],[1,-654],[1,1064],[1,-19656,889872],[1,1452,527204]]},
 'R7_3_146':{'rad':6,'labels':[1,2,3,6], 'sha':'853cd9cae2095b8ecb37ada145045562cbaaeb0fb622b127e63f70997b67479b','other_field':1,'separating_factors':[[1,-654],[1,-184],[1,66],[1,234],[1,1852],[1,-15896,12501688]]}}
PAIRS=[(i,j) for i in range(6) for j in range(i+1)]
WEIGHTS=[1,3,11,37,101,307,997]

def require(b,m):
    if not b:raise RuntimeError(m)

def mul(z,w,r):return z[0]*w[0]+r*z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def quadratic_sign(z,r):
    a,b=z
    if a>=0 and b>=0:return int(bool(a or b))
    if a<=0 and b<=0:return -int(bool(a or b))
    t=a*a-r*b*b
    return (1 if t>0 else -1)*(1 if a>0 else -1)
def outer(v):return [v[i]*v[j] for i,j in PAIRS]
def polyprod(factors):
    p=[1]
    for q in factors:
        out=[0]*(len(p)+len(q)-1)
        for i,x in enumerate(p):
            for j,y in enumerate(q):out[i+j]+=x*y
        p=out
    return p

def charpoly(M):
    n=len(M);A=[[int(i==j) for j in range(n)] for i in range(n)];cs=[1]
    for k in range(1,n+1):
        A=[[sum(M[i][l]*A[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        tr=sum(A[i][i] for i in range(n));require(tr%k==0,'integral characteristic recurrence')
        c=-tr//k;cs.append(c)
        for i in range(n):A[i][i]+=c
    return cs

def psd(M):
    A=[[F(x) for x in row] for row in M];n=len(A)
    for k in range(n):
        p=A[k][k]
        if p<0:return False
        if not p:
            if any(A[k][j] for j in range(k+1,n)):return False
            continue
        for i in range(k+1,n):
            for j in range(i,n):A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
    return True

def principal_inverse(R):
    A=[[F(x) for x in row] for row in R];I=[]
    for k in range(6):
        p=A[k][k];require(p>=0,'PSD principal pivot')
        if not p:
            require(not any(A[k][j] for j in range(k+1,6)),'zero pivot row');continue
        I.append(k)
        for i in range(k+1,6):
            for j in range(i,6):A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
    n=len(I);P=[[F(R[i][j]) for j in I]+[F(i==j) for j in I] for i in I]
    for k in range(n):
        p=P[k][k];require(p!=0,'invertible principal matrix');P[k]=[x/p for x in P[k]]
        for i in range(n):
            if i!=k:
                c=P[i][k];P[i]=[x-c*y for x,y in zip(P[i],P[k])]
    inv=[row[n:] for row in P];h=math.lcm(*(x.denominator for row in inv for x in row))
    H=[[int(x*h) for x in row] for row in inv]
    return I,h,H

def span_contains(rows,b,p):
    piv={}
    for row in rows:
        v=[x%p for x in row]
        for k,w in piv.items():
            c=v[k]
            if c:v=[(x-c*y)%p for x,y in zip(v,w)]
        k=next((i for i,x in enumerate(v) if x),None)
        if k is not None:
            c=pow(v[k],-1,p);piv[k]=[(x*c)%p for x in v]
    v=[x%p for x in b]
    for k,w in piv.items():
        c=v[k]
        if c:v=[(x-c*y)%p for x,y in zip(v,w)]
    return not any(v)

def sign_branches(N,dual):
    """Pivotal odd-isotypic forms give equal signs; nonselfdual indicators are zero."""
    n=7;parent=list(range(n))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    def join(i,j):parent[root(i)]=root(j)
    sd=[i for i in range(n) if dual[i]==i]
    for X in range(n):
        for Y in sd:
            v=[sum(N[X][Y][k]*N[k][dual[X]][j] for k in range(n)) for j in range(n)]
            for j in sd:
                if v[j]%2:join(Y,j)
    for X in sd:
        v=[sum(N[X][X][k]*N[k][X][j] for k in range(n)) for j in range(n)]
        for j in sd:
            if v[j]%2:join(X,j)
    roots=sorted({root(i) for i in sd}-{root(0)});out=[]
    for signs in itertools.product([1,-1],repeat=len(roots)):
        choices={root(0):1,**dict(zip(roots,signs))}
        out.append([choices[root(i)] if i in sd else 0 for i in range(7)])
    return out

def source_data(N,config):
    r=config['rad'];g,a,b,f=config['labels'];dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    require(all(N[i][j]==N[j][i] for i in range(7) for j in range(7)),'source commutative')
    perm=[N[g][i].index(1) for i in range(7)];d=[None]*7
    for i in [0,g]:d[i]=(1,0)
    for i in [a,perm[a]]:d[i]=(4,2)
    for i in [b,perm[b]]:d[i]=(7,4) if r==3 else (5,2)
    d[f]=(6,4) if r==3 else (6,2)
    require(all(d),'dimension labels')
    for i in range(7):
        for j in range(7):
            require(mul(d[i],d[j],r)==tuple(sum(N[i][j][k]*d[k][l] for k in range(7)) for l in range(2)),'dimension character')
    D=tuple(sum(mul(z,z,r)[j] for z in d) for j in range(2))
    require(D==((336,192) if r==3 else (240,96)),'global dimension')
    require((D[0]//48)**2-r*(D[1]//48)**2==1,'D/48 unit')
    B=[[sum(N[k][i][j]*N[k][l][j] for k in range(7) for j in range(7)) for l in range(7)] for i in range(7)]
    fs=[12,8,8,8,4] if r==3 else [12,8,6,6,4]
    require(charpoly(B)==polyprod([[1,-z] for z in fs]+[[1,-2*D[0],2304]]),'formal codegrees')
    M=[[sum(WEIGHTS[k]*N[k][j][i] for k in range(7)) for j in range(7)] for i in range(7)]
    require(charpoly(M)==polyprod(config['separating_factors']),'separating matrix fields')
    # The displayed linear/quadratic factors have distinct roots; other quadratic
    # fields are disjoint from Q(sqrt(r)), so the desired Galois extension exists.
    zs=[(D[0]//z,D[1]//z) for z in fs]+[(97,56) if r==3 else (49,20)]
    zs.sort(key=functools.cmp_to_key(lambda z,w:quadratic_sign((z[0]-w[0],z[1]-w[1]),r)))
    irr=[z[1] for z in d]
    def transport(v):
        aa,bb=[sum(x*z[j] for x,z in zip(v,d)) for j in range(2)]
        p,q=(4*aa-7*bb,4) if r==3 else (2*aa-5*bb,2)
        w=[x*q+y*p for x,y in zip(v,irr)]
        require(all(x%q==0 for x in w),'integral row transport')
        return tuple(x//q for x in w)
    T=[transport(tuple(int(i==j) for i in range(7))) for j in range(7)]
    for j,v in enumerate(T):require(transport(v)==tuple(int(i==j) for i in range(7)),'transport involution')
    return d,D,B,zs,transport,sign_branches(N,dual)

def enumerate_low(B,d,zs,transport):
    unit=(1,0,0,0,0,0,0);forced=transport(unit);forced_z=tuple(sum(x*z[j] for x,z in zip(forced,d)) for j in range(2))
    domains={};nodes=[0]*7
    for z in set(zs):
        if z==forced_z:domains[z]=[forced];continue
        out=[]
        def rec(i,v,left):
            if i==7:
                if left==(0,0):out.append((1,)+tuple(v))
                return
            for k in range(min(B[0][i],math.isqrt(B[i][i]))+1):
                rem=(left[0]-k*d[i][0],left[1]-k*d[i][1])
                if min(rem)>=0:rec(i+1,v+[k],rem)
        rec(1,[],(z[0]-1,z[1]));domains[z]=out
    sols=[]
    def rec(k,rem,C,chosen):
        nodes[k]+=1
        if k==6:
            if not any(rem):
                require(collections.Counter([unit]+chosen)==collections.Counter(transport(v) for v in [unit]+chosen),'I1 transport stability')
                sols.append(chosen)
            return
        z=zs[k]
        for v in domains[z]:
            if k and zs[k-1]==z and v<chosen[-1]:continue
            if any(x>y for x,y in zip(v,rem)):continue
            CC=[[C[i][j]-v[i]*v[j] for j in range(7)] for i in range(7)]
            if any(x<0 for row in CC for x in row):continue
            if any(CC[i][i]*CC[j][j]<CC[i][j]**2 for i in range(7) for j in range(i)):continue
            if not psd(CC):continue
            rec(k+1,[x-y for x,y in zip(rem,v)],CC,chosen+[v])
    rec(0,[B[i][0]-int(i==0) for i in range(7)],[[B[i][j]-int(i==j==0) for j in range(7)] for i in range(7)],[])
    return sols,nodes,forced

def global_rows(B,d,r):
    base=[]
    for v in itertools.product(*(range(math.isqrt(B[i][i])+1) for i in range(1,7))):
        a,b=[sum(x*z[j] for x,z in zip(v,d[1:])) for j in range(2)];norm=a*a-r*b*b
        if not norm or 48*a%norm or 48*b%norm:continue
        q=outer(v)
        if any(z>B[i+1][j+1] for z,(i,j) in zip(q,PAIRS)):continue
        base.append((v,q,(a,b)))
    return base

def compatible_pairs(base,B,low,transport):
    R=[[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in low) for j in range(6)] for i in range(6)];bound=[R[i][j] for i,j in PAIRS]
    I,h,H=principal_inverse(R);valid={}
    for v,q,z in base:
        if any(x>y for x,y in zip(q,bound)):continue
        u=[sum(x*v[j] for x,j in zip(row,I)) for row in H]
        if any(sum(R[j][k]*x for k,x in zip(I,u))!=h*v[j] for j in range(6)):continue
        if sum(v[j]*x for j,x in zip(I,u))>h:continue
        valid[v]=(q,z)
    pairs=[]
    for v,(q,z) in valid.items():
        w=transport((0,)+v)[1:]
        if all(x<=0 for x in w):w=tuple(-x for x in w)
        if min(w)<0 or w not in valid or v>w:continue
        qq,zz=valid[w];pairs.append([(v,q,z)] if v==w else [(v,q,z),(w,qq,zz)])
    return R,bound,pairs,len(I)

def trace_columns(pairs,D,r):
    basic=[(4,0,4,0),(-4,0,4,0),(2,0,-2,0),(-2,0,-2,0),(0,0,-4,0)]
    h,s=(2,2) if r==3 else (1,0)
    restricted=basic+[(0,-h,s,0)];unrestricted=basic+[(0,h,s,0),(0,-h,s,0),(0,0,0,h),(0,0,0,-h)]
    cols=[]
    for orbit in pairs:
        z=orbit[0][2];rational=z[0]*D[1]==z[1]*D[0]
        require(not rational or len(orbit)==1,'rational ratio row fixed')
        q=[sum(row[1][j] for row in orbit) for j in range(21)]
        for ph in unrestricted if rational else restricted:
            c=[4*x for x in q]
            for degree in range(2):
                values=[mul(row[2],ph[2*degree:2*degree+2],r) for row in orbit]
                c.extend(sum(row[0][i]*value[k] for row,value in zip(orbit,values)) for i in range(6) for k in range(2))
            cols.append(c)
    return cols

def lowkey(low):return json.dumps(low,separators=(',',':'))

def verify(repo,certificate,only=None):
    cert=json.loads(certificate.read_text());counts=collections.Counter();sources={}
    for line in gzip.open(repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'));m=max(x for a in N for b in a for x in b);counts[m]+=1;rid=f'R7_{m}_{counts[m]}'
        if rid in TARGETS and (not only or rid in only):sources[rid]=N
    require(set(sources)==(set(only) if only else set(TARGETS)),'source coverage')
    results=[]
    for rid,N in sources.items():
        cfg=TARGETS[rid];r=cfg['rad'];sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest();require(sha==cfg['sha'],'source hash')
        d,D,B,zs,transport,signs=source_data(N,cfg);lows,nodes,forced=enumerate_low(B,d,zs,transport);base=global_rows(B,d,r)
        data=cert['cases'][rid];pool=data['separators'];stats=collections.Counter();ranks=collections.Counter();require(len(pool) in [1,len(signs)],'universal separator sign coverage')
        for low in lows:
            R,bound,pairs,rank=compatible_pairs(base,B,low,transport);ranks[rank]+=1
            gramcols=[[sum(row[1][j] for row in orbit) for j in range(21)] for orbit in pairs]
            bad=next((p for p in [2,3,5,7,11,13] if not span_contains(gramcols,bound,p)),None)
            if bad:stats['modular_excluded']+=1;continue
            cols=trace_columns(pairs,D,r);known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
            for signid,si in enumerate(signs):
                y=pool[0 if len(pool)==1 else signid];require(len(y)==45 and all(type(x)==int for x in y),'integer separator')
                rhs=[4*x for x in bound]+[-4*x for z in known for x in z]+[4*(D[k]*si[i+1]-known[i][k]) for i in range(6) for k in range(2)]
                require(dot(rhs,y)<0,'strict separating target')
                require(all(dot(c,y)>=0 for c in cols),'separating every allowed moment column')
                stats['trace_systems_excluded']+=1
            stats['trace_blocks_excluded']+=1
        result={'id':rid,'tensor_sha256':sha,'low_blocks':len(lows),'low_nodes':nodes,'forced_Galois_unit_row':forced,'global_rows':len(base),'pivotal_sign_branches':signs,'residual_ranks':dict(ranks),'separators':len(pool),**stats,'status':'PASS'}
        require(stats['modular_excluded']+stats['trace_blocks_excluded']==len(lows),'exhaustive exclusion')
        results.append(result)
    return {'status':'PASS','criterion':'quadratic_center_Galois_two_moment','scope':'general_complex_after_Galois_pseudo_unitarity_reduction','optimizer_used':False,'cases':results}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('quadratic_center_trace_certificate.json'));ap.add_argument('--output',type=Path);ap.add_argument('--only',nargs='*');args=ap.parse_args()
    out=verify(args.repo,args.certificate,args.only)
    text=json.dumps(out,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text)
if __name__=='__main__':main()
