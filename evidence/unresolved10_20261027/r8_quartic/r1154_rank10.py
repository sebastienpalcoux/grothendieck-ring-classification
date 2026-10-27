#!/usr/bin/env python3
"""Small exact ring check for anomaly-cancelled R1154 candidates.
This verifies ring arithmetic, not the categorical derivation/existence.
"""
import json, hashlib, itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent

def action(g,i):
    return g^i if i<4 else 4+(g^(i-4)) if i<8 else 8+((g>>1)^(i-8))
def shift(g,z):
    out=[0]*10
    for i,c in enumerate(z): out[action(g,i)]+=c
    return out

def tensor(m,n,t):
    xx=[0]*10;xx[t]=1;xx[4:8]=[m,2-m,n,2-n];xx[8:10]=[2,2]
    xy=[0]*4+[2]*4+[4,5]
    yy=[1,1,0,0,4,4,5,5,8,11]
    N=[]
    for i in range(10):
        rows=[]
        for j in range(10):
            if i<4: z=[int(k==action(i,j)) for k in range(10)]
            elif j<4:z=[int(k==action(j,i)) for k in range(10)]
            elif i<8 and j<8:z=shift((i-4)^(j-4),xx)
            elif i<8:z=shift((i-4)^((j-8)<<1),xy)
            elif j<8:z=shift((j-4)^((i-8)<<1),xy)
            else:z=shift(((i-8)^(j-8))<<1,yy)
            rows.append(z)
        N.append(rows)
    return N

def check(N):
    dual=[]
    for i in range(10):
        d=[j for j in range(10) if N[i][j][0]]
        if len(d)!=1 or N[i][d[0]][0]!=1:return {'failure':'duality'}
        dual.append(d[0])
    for i,j,k,l in itertools.product(range(10),repeat=4):
        if sum(N[i][j][z]*N[z][k][l] for z in range(10))!=sum(N[j][k][z]*N[i][z][l] for z in range(10)):
            return {'failure':'associativity','indices':[i,j,k,l]}
    for i,j,k in itertools.product(range(10),repeat=3):
        if N[i][j][k]!=N[dual[i]][k][j]:return {'failure':'Frobenius','indices':[i,j,k]}
    ad={0}
    for i in range(10):ad|={k for k,c in enumerate(N[i][dual[i]]) if c}
    while True:
        nxt=ad|{k for i in ad for j in ad for k,c in enumerate(N[i][j]) if c}
        if nxt==ad:break
        ad=nxt
    return {'fusion_ring':True,'dual':dual,'adjoint_closure':sorted(ad),'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()}

def main():
    candidates=[]
    for t,m,n in itertools.product(range(2),range(3),range(3)):
        N=tensor(m,n,t);result=check(N)
        if result.get('fusion_ring'):candidates.append({'t':t,'m':m,'n':n,**result,'N':N})
    print('Associative based rings:',[(c['t'],c['m'],c['n']) for c in candidates])
    (HERE/'r1154_rank10.json').write_text(json.dumps(candidates,indent=2)+'\n')
if __name__=='__main__':main()
