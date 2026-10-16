#!/usr/bin/env python3
"""Exact source-bound arithmetic for FIB_PAIR_THEORETICAL_GALOIS_PU.md."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)
def flat(R):return tuple(c for a in R for b in a for c in b)
B=list(itertools.product(range(2),repeat=3));pos={x:i for i,x in enumerate(B)}
def model(epsilon):
    def product(x,y):
        terms={tuple(a+b for a,b in zip(x,y)):1};out=[0]*8
        while terms:
            (g,t,z),c=terms.popitem()
            if g>=2:news=[(g%2,t,z)]
            elif t>=2:news=[(g,t-1,z),(g,t-2,z)]
            elif z>=2:news=[(g+epsilon,t,z-2),(g,t+1,z-1),(g+1,t+1,z-1)]
            else:out[pos[g,t,z]]+=c;continue
            for q in news:terms[q]=terms.get(q,0)+c
        return out
    return [[product(x,y) for y in B] for x in B]
def remainder(a,b,p):
    a=[c%p for c in a]
    while len(a)>=len(b):
        c=a[-1]*pow(b[-1],-1,p)%p
        for i,z in enumerate(b):a[len(a)-len(b)+i]=(a[len(a)-len(b)+i]-c*z)%p
        while a and a[-1]==0:a.pop()
    return a
def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--output',type=Path);a=ap.parse_args()
    source=a.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    rs=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(source,'rt')]
    rs=sorted((r for r in rs if max(flat(r))==2),key=flat)
    cases=[]
    for idx,eps,g,t,x in [(190,1,7,5,1),(489,0,1,7,3)]:
        R=rs[idx-1]
        def single(i,j):
            need(sum(R[i][j])==1,'monomial product is simple');return R[i][j].index(1)
        perm=[]
        for gi,ti,xi in B:
            z=0
            for power,gen in [(gi,g),(ti,t),(xi,x)]:
                if power:z=single(z,gen)
            perm.append(z)
        need(sorted(perm)==list(range(8)),'monomial basis')
        M=model(eps)
        need(all(M[i][j][k]==R[perm[i]][perm[j]][perm[k]] for i,j,k in itertools.product(range(8),repeat=3)),'full presentation tensor match')
        dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        need(dual[x]==(single(g,x) if eps else x),'x duality')
        need(all(R[i][j][k]==R[j][i][k] for i,j,k in itertools.product(range(8),repeat=3)),'commutativity')
        need(all(sum(R[i][j][b]*R[b][k][l] for b in range(8))==sum(R[j][k][b]*R[i][b][l] for b in range(8)) for i,j,k,l in itertools.product(range(8),repeat=4)),'associativity')
        if not eps:
            gt=single(g,t)
            cube=[sum(R[x][x][j]*R[j][x][k] for j in range(8))%2 for k in range(8)]
            gcube=[sum(R[gt][gt][j]*R[j][gt][k] for j in range(8))%2 for k in range(8)]
            need(cube==[int(k in (x,t,gt)) for k in range(8)] and gcube==[int(k==g) for k in range(8)],'odd cube indicators')
        cases.append({'id':f'R8_2_{idx}','epsilon':eps,'model_basis_g_tau_x_exponents':B,'model_to_census':perm,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'tensor_entries_matched':512,'x_dual':dual[x]})
    f=[1,2,-6,-2,1]
    need(all(remainder(f,[c,1],3) for c in range(3)),'no linear mod3 factor')
    need(all(remainder(f,[c,d,1],3) for c,d in itertools.product(range(3),repeat=2)),'no quadratic mod3 factor')
    # Eliminating d from d^2=u gives u^4-16u^3+46u^2-16u+1.
    q=[1,-16,46,-16,1];out=[0]*5
    for i,c in enumerate(q):
        term=[1]
        for _ in range(i):term=pmul(term,[2,-1])
        for j,z in enumerate(term):out[4-i+j]+=c*z
    need(out==[16,-160,400,-320,80],'ratio polynomial elimination')
    report={'status':'PASS','classification_changes':0,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'general sphericality and Galois pseudo-unitarity for both; actual regular C2 algebra additionally for R489','cases':cases,'nonintegral_ratio_primitive_polynomial_ascending':[1,-10,25,-20,5]}
    text=json.dumps(report,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
