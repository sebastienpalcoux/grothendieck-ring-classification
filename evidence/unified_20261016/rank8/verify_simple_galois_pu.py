#!/usr/bin/env python3
"""Exact standard-library replay of the R820/R869 sphericality reduction.

This checks the finite algebraic hypotheses of SIMPLE_GALOIS_PU.md. It does not
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
    b=2 if idx==820 else 3;aa=[i for i in range(1,6) if i!=b];cc=[6,7]
    need(R[b][b]==[1]*n,'distinguished square')
    for a in aa:
        need(R[b][a]==[int(i!=0 and i!=a) for i in range(n)],'dimension relation for a')
    for c in cc:
        need(R[b][c]==[0]+[1+int(i==c) for i in range(1,n)],'dimension relation for c')
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
    need(solutions==[0],'a non-original oriented signed quotient survives')
    return {'id':f'R8_2_{idx}','tensor_sha256':HASHES[idx],'unknown_signs':m,'associativity_equations':len(eqs),'nodes':nodes,'signed_quotients':1,'only_quotient':'original tensor','dimension_character_relation':'b^2-7*b+1=0','mathematical_status':'every categorification admits a spherical structure and becomes pseudo-unitary after Galois conjugation; existence proved separately by the near-group centralizer construction'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--output',type=Path);args=ap.parse_args()
    source=args.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    tensors=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(source,'rt')]
    tensors=sorted((R for R in tensors if max(flat(R))==2),key=flat)
    report={'status':'PASS','verdict':'PASS','scope':'necessary structural reduction, no categorical realization or exclusion','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':[check(tensors[i-1],i) for i in HASHES]}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
