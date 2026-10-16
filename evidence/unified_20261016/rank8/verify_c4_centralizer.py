#!/usr/bin/env python3
"""Exact restricted Verlinde calculation for BRW's hyperbolic rank-28 category."""
import argparse, gzip, hashlib, itertools, json
from functools import lru_cache
from pathlib import Path

ZERO=(0,)*16
ONE=(1,)+(0,)*15

def check(x,msg):
    if not x: raise ValueError(msg)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def scale(a,k): return tuple(k*x for x in a)
def root(k):
    k%=32
    return tuple((1 if k<16 else -1) if j==k%16 else 0 for j in range(16))
@lru_cache(None)
def mul(a,b):
    out=[0]*16
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: out[(i+j)%16]+=x*y*(1 if i+j<16 else -1)
    return tuple(out)
def conj(a):
    out=ZERO
    for i,x in enumerate(a):
        if x: out=add(out,scale(root(-i),x))
    return out
SQRT2=add(root(4),root(-4))

def model():
    K=[(i,i) for i in range(4)]
    G=[(1,0),(2,0),(2,1),(3,0),(3,1),(3,2)]
    H=[(1,0),(2,0),(3,0),(4,0),(5,0),(9,0),(10,0),(0,1),(1,1),(2,1),(5,1),(6,1),(7,1),(13,1)]
    labels=[('k',p) for p in K]+[('p',p) for p in K]+[('g',p) for p in G]+[('h',p) for p in H]
    def gamma(p): return (4*p[0]%16,p[0]%2)
    def bg(p,q): return root(8*(p[0]*q[1]+p[1]*q[0]))
    def bh(p,q): return root(-6*p[0]*q[0]-16*p[1]*q[1])
    def th(p): return ((3*p[0]+8*p[1])%16,(p[0]+p[1])%2)
    lo=add(scale(ONE,2),neg(SQRT2)); hi=add(scale(ONE,2),SQRT2)
    def entry(x,y):
        t,p=x; u,q=y
        if 'h' in (t,u):
            if t!='h': return entry(y,x)
            if u=='g': return ZERO
            if u=='h': return scale(mul(SQRT2,add(bh(p,q),bh(th(p),q))),-2)
            return scale(mul(SQRT2,bh(p,gamma(q))),2 if u=='k' else -2)
        if 'g' in (t,u):
            if t!='g': return entry(y,x)
            if u=='g': return scale(add(bg(p,q),bg((p[1],p[0]),q)),4)
            return scale(bg(p,q),4)
        return mul(lo if t==u else hi,bg(p,q))
    U=[[entry(x,y) for y in labels] for x in labels]
    # U=16S. Test exact unitarity; no floating point or chosen numerical embedding.
    for i,j in itertools.product(range(28),repeat=2):
        v=ZERO
        for l in range(28): v=add(v,mul(U[i][l],conj(U[j][l])))
        check(v==scale(ONE,256 if i==j else 0),f'unitarity {i,j}')
    inverse4=[]
    for t,p in labels:
        inverse4.append(add(scale(ONE,4),scale(SQRT2,2)) if t=='k' else add(scale(ONE,4),scale(SQRT2,-2)) if t=='p' else ONE if t=='g' else SQRT2)
    for l in range(28): check(mul(U[0][l],inverse4[l])==scale(ONE,4),'inverse first row')
    chosen=[('k',(0,0)),('k',(2,2)),('p',(0,0)),('p',(2,2)),('g',(3,1)),('h',(2,1)),('h',(6,1)),('h',(4,0))]
    ids=[labels.index(x) for x in chosen]
    # Centralizer of the entire pointed category, checked from S entries.
    pointed=range(4)
    actual=[j for j in range(28) if all(U[i][j]==U[0][j] for i in pointed)]
    check(set(actual)==set(ids),'complete pointed centralizer')
    R=[[[0]*8 for j in ids] for i in ids]
    for ai,i in enumerate(ids):
        for aj,j in enumerate(ids):
            pair=[mul(mul(U[i][l],U[j][l]),inverse4[l]) for l in range(28)]
            for k in range(28):
                v=ZERO
                for l in range(28): v=add(v,mul(pair[l],conj(U[k][l])))
                check(not any(v[1:]) and v[0]%1024==0,'integral Verlinde')
                n=v[0]//1024
                check(n>=0,'nonnegative Verlinde')
                if k in ids: R[ai][aj][ids.index(k)]=n
                else: check(n==0,'centralizer fusion closure')
    return R, labels, ids

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('repo'));ap.add_argument('--output',type=Path);args=ap.parse_args()
    R,labels,ids=model()
    source=args.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    rows=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.decompress(source.read_bytes()).decode().splitlines()]
    flat=lambda r:tuple(n for a in r for b in a for n in b)
    rows=sorted((r for r in rows if max(flat(r))==2),key=flat)
    target=rows[665]
    check(hashlib.sha256(json.dumps(target,separators=(',',':')).encode()).hexdigest()=='cfbe81aa760b11ab636b164d65c6985bafe05d675eeae0404a42b0ebc4c0d35b','bound source tensor SHA256')
    matches=[]
    for xp in itertools.permutations([3,4]):
        for zp in itertools.permutations([2,5,6]):
            f=[0,1,*xp,7,*zp]
            if all(R[i][j][k]==target[f[i]][f[j]][f[k]] for i,j,k in itertools.product(range(8),repeat=3)):matches.append(f)
    check([0,1,3,4,7,2,5,6] in matches,'specified source tensor identification')
    for i,j,k,l in itertools.product(range(8),repeat=4):
        check(sum(R[i][j][a]*R[a][k][l] for a in range(8))==sum(R[j][k][a]*R[i][a][l] for a in range(8)),'associativity')
    check(all(R[i][j][0]==int(i==j) for i,j in itertools.product(range(8),repeat=2)),'selfduality')
    digest=hashlib.sha256(json.dumps(target,separators=(',',':')).encode()).hexdigest()
    result={'status':'PASS','case':'R8_2_666','tensor_sha256':digest,'model_to_source_maps':matches,'rank28_unitarity_checks':784,'centralizer_rank':8,'restricted_verlinde_and_closure_checks':1792,'all_512_tensor_coefficients_match':True,'model_tensor':R,'labels':labels,'centralizer_indices':ids}
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['model_tensor','labels']},indent=2))
if __name__=='__main__':main()
