#!/usr/bin/env python3
"""Exact standard-library replay of the R489 sphericality reduction.

This checks finite algebraic hypotheses of FIB_R489_GALOIS_PU.md. It does not
claim a categorification exists. No optimizer, compiler, Sage, or SymPy is used.
"""
import argparse,collections,gzip,hashlib,itertools,json,time
from pathlib import Path

HASHES={820:'88d4e0d03d1f45b727bb5d973ee4c47ef114ff4870f397d9f08342d5db1d0373',869:'6fd67687c6a4590e43cf539442042092ebc28973b626127f40d6f27fb66de112'}
def need(ok,message):
    if not ok:raise ValueError(message)
def flat(R):return tuple(c for a in R for b in a for c in b)

def check(R,idx):
    n=len(R);need(n==8,'rank');need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==HASHES[idx],'tensor hash')
    for i,j,k in itertools.product(range(n),repeat=3):
        need(R[0][i][j]==int(i==j) and R[i][j][0]==int(i==j),'selfdual unit')
        need(R[i][j][k]==R[j][i][k]==R[i][k][j],'full symmetry')
    for i,j,k,l in itertools.product(range(n),repeat=4):
        need(sum(R[i][j][a]*R[a][k][l] for a in range(n))==sum(R[j][k][a]*R[i][a][l] for a in range(n)),'associativity')
    triples=[v for v in itertools.combinations_with_replacement(range(1,n),3) if R[v[0]][v[1]][v[2]]]
    # Positive-indicator lifts force every repeated coefficient of size one.
    # All multiplicity-two coefficients in these tensors have a repeated label.
    unknown=[]
    for tri in triples:
        bound=R[tri[0]][tri[1]][tri[2]]
        need(bound in (1,2),'multiplicity')
        if len(set(tri))==3:need(bound==1,'distinct multiplicity-two channel')
        if len(set(tri))==3 or bound==2:unknown.append(tri)
    positions={tri:k for k,tri in enumerate(unknown)};m=len(unknown)
    def term(i,j,k):
        c=R[i][j][k];tri=tuple(sorted((i,j,k)))
        return c,1<<positions[tri] if tri in positions else 0
    equations={}
    for ijkl in itertools.product(range(1,n),repeat=4):
        i,j,k,l=ijkl;row=collections.defaultdict(int)
        for a in range(n):
            c,u=term(i,j,a);d,v=term(a,k,l);row[u^v]+=c*d
            c,u=term(j,k,a);d,v=term(i,a,l);row[u^v]-=c*d
        row={u:c for u,c in row.items() if c}
        if row:
            need(sum(row.values())==0,'positive source solution')
            key=tuple(sorted(row.items()));neg=tuple((u,-c) for u,c in key)
            equations[min(key,neg)]=ijkl
    eqs=list(equations);supports=[set(i for u,c in e for i in range(m) if u>>i&1) for e in eqs]
    left=set(range(m));order=[]
    while left:
        available=[x&left for x in supports if x&left]
        candidate=min(available,key=lambda x:(len(x),sorted(x))) if available else {min(left)}
        chosen=min(candidate,key=lambda i:(-sum(i in x for x in supports),i))
        order.append(chosen);left.remove(chosen)
    at={v:i for i,v in enumerate(order)};levels=[[] for _ in range(m+1)]
    for e,support in zip(eqs,supports):
        need(bool(support),'nonzero constant equation')
        levels[max(at[i] for i in support)+1].append(e)
    nodes=0;solutions=[]
    def dfs(level,negative):
        nonlocal nodes
        nodes+=1
        for e in levels[level]:
            if sum(-c if (u&negative).bit_count()%2 else c for u,c in e):return
        if level==m:solutions.append(negative);return
        dfs(level+1,negative)
        dfs(level+1,negative|(1<<order[level]))
    dfs(0,0)
    need(sorted(solutions)==[0,7,57,62], 'complete four-quotient list')
    gauges=[]
    for sol in solutions:
        signs={tri:(-1 if sol>>i&1 else 1) for i,tri in enumerate(unknown)}
        candidates=[]
        for tail in itertools.product((1,-1),repeat=7):
            ss=(1,)+tail
            if all(ss[i]*ss[j]*ss[k]==signs.get(tuple(sorted((i,j,k))),1) for i,j,k in itertools.product(range(n),repeat=3) if R[i][j][k]):candidates.append(ss)
        need(len(candidates)==1,'unique coboundary')
        gauges.append(candidates[0])
    need(set(gauges)=={(1,g,h,1,1,1,1,1) for g in (1,-1) for h in (1,-1)},'gauge support')
    g,tau,x=1,7,3
    def product(v,w):return [sum(v[i]*w[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
    unit=lambda i:[int(j==i) for j in range(n)]
    need(R[g][g]==unit(0) and R[tau][tau]==[int(j in (0,tau)) for j in range(n)],'g and tau relations')
    gx=R[g][x].index(1);tx=R[tau][x].index(1);gtx=R[g][tx].index(1);gtau=R[g][tau].index(1)
    need(R[x][x]==[int(j in (0,tx,gtx)) for j in range(n)],'x square')
    cube=product(R[x][x],unit(x));gcube=product(R[gtau][gtau],unit(gtau))
    need([z%2 for z in cube]==[int(j in (x,tau,gtau)) for j in range(n)],'x cube parity')
    need([z%2 for z in gcube]==unit(g),'g tau cube parity')
    # f(X)=X^4-2X^3-6X^2+2X+1 is irreducible modulo 3.
    f=[1,2,-6,-2,1]
    def remainder(a,b,p):
        a=[c%p for c in a]
        while len(a)>=len(b):
            c=a[-1]*pow(b[-1],-1,p)%p
            for i,z in enumerate(b):a[len(a)-len(b)+i]=(a[len(a)-len(b)+i]-c*z)%p
            while a and a[-1]==0:a.pop()
        return a
    need(all(remainder(f,[a,1],3) for a in range(3)),'no linear mod3 factor')
    need(all(remainder(f,[a,b,1],3) for a,b in itertools.product(range(3),repeat=2)),'no quadratic mod3 factor')
    # Eliminate u=X^2 from f: (u^2-6u+1)^2-4u(u-1)^2.
    # Substitution u=2/y-1, followed by multiplication by y^4, equals
    # 16*(5y^4-20y^3+25y^2-10y+1).
    def pmul(a,b):
        c=[0]*(len(a)+len(b)-1)
        for i,x0 in enumerate(a):
            for j,y0 in enumerate(b):c[i+j]+=x0*y0
        return c
    def padd(a,b):return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
    q=[1,-16,46,-16,1] # eliminated polynomial in u
    out=[0]*5
    for i,c in enumerate(q):
        term=[1]
        for _ in range(i):term=pmul(term,[2,-1])
        term=[0]*(4-i)+[c*z for z in term]
        out=padd(out,term)
    need(out==[16,-160,400,-320,80],'nonintegral ratio polynomial')
    return {'id':'R8_2_489','tensor_sha256':HASHES[idx],'unknown_signs':m,'associativity_equations':len(eqs),'nodes':nodes,'signed_quotients':len(solutions),'gauges':gauges,'ring_generators':{'g':g,'tau':tau,'x':x,'gx':gx,'tau_x':tx,'g_tau_x':gtx,'g_tau':gtau},'nonintegral_ratio_polynomial':[1,-10,25,-20,5],'scope':'sphericality, Galois pseudo-unitarity, and trivial pointed C2 associator; no categorification decision'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--output',type=Path);args=ap.parse_args()
    source=args.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    tensors=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(source,'rt')]
    tensors=sorted((R for R in tensors if max(flat(R))==2),key=flat)
    HASHES[489]='23cae0639e4ce7e54428705a66098747319e26d5f29ad8dff05914a6d43caef1'
    report={'status':'PASS','classification_changes':0,'case':check(tensors[488],489)}
    result=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(result)
    print(result,end='')
if __name__=='__main__':main()
