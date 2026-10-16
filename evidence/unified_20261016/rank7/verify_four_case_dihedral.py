#!/usr/bin/env python3
"""Exact source-bound four-case dihedral Morita reduction certificate."""
import argparse, collections, gzip, hashlib, itertools, json
from pathlib import Path
import sympy as s

def need(v,m):
    if not v:raise RuntimeError(m)

def sha(N):return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()

def fusion_check(N,dims):
    n=len(N);M=[s.Matrix(z).T for z in N]
    dual=[]
    for i in range(n):
        hits=[j for j in range(n) if N[i][j][0]];need(len(hits)==1 and N[i][hits[0]][0]==1,'unique dual');dual.append(hits[0])
    need(M[0]==s.eye(n),'unit')
    for i,j in itertools.product(range(n),repeat=2):
        need(M[i]*M[j]==sum((N[i][j][k]*M[k] for k in range(n)),s.zeros(n)),'all associativity identities')
        need(s.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(n)))==0,'FP dimension character')
        for k in range(n):need(N[i][j][k]==N[dual[i]][k][j]==N[k][dual[j]][i],'Frobenius reciprocity')
    return dual,M

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    targets={35:([0,1,2,5],6,3,4,5,'V4',True),2053:([0,1,2,6],4,3,5,6,'C4',True),2603:([0,3,4,5],6,1,2,3,'V4',False),2665:([0,1,2,6],5,3,4,6,'C4',False)}
    counts=collections.Counter();sources={};t=2+s.sqrt(5)
    for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'));m=max(v for a in N for b in a for v in b);counts[m]+=1
        if m==4 and counts[m] in targets:sources[counts[m]]=N
    need(set(sources)==set(targets),'source coverage')
    source_rows=[]
    for rid,N in sorted(sources.items()):
        G,X,Y,Z,h,kind,selfdual=targets[rid];dims=[1 if i in G else 2 if i==X else 2*t for i in range(7)]
        dual,M=fusion_check(N,dims)
        need(N[X][X]==[int(i in G) for i in range(7)],'TY square')
        need(N[h][h][0]==1,'common involution')
        need(all(N[h][w][w]==N[w][h][w]==1 for w in [X,Y,Z]),'three fixed objects')
        need(N[X][Y]==N[Y][X]==[int(i in [Y,Z]) for i in range(7)],'odd-multiplicity product')
        need(N[Y][dual[Y]][X]==1,'odd X summand')
        need((dual[Y]==Y and dual[Z]==Z)==selfdual,'duality type')
        order2=sum(N[g][g][0] for g in G)
        need(order2==(4 if kind=='V4' else 2),'invertible group type')
        need(s.expand(sum(d*d for d in dims)-(16+32*t))==0,'Morita dimension')
        source_rows.append({'id':f'R7_4_{rid}','tensor_sha256':sha(N),'G':G,'X':X,'Y':Y,'Z':Z,'h':h,'invertible_group':kind,'irrational_selfdual':selfdual,'fusion_checks':'all associativity, duality, Frobenius reciprocity and FP dimensions'})
    G=list(itertools.product(range(4),range(2)));idx={g:i for i,g in enumerate(G)};e=(0,0)
    mul=lambda g,h:((g[0]+(-1)**g[1]*h[0])%4,(g[1]+h[1])%2)
    inv=lambda g:next(h for h in G if mul(g,h)==e)
    conj=lambda a,g:mul(mul(a,g),inv(a))
    def power(g,k):
        out=e
        for _ in range(k):out=mul(out,g)
        return out
    aut=[]
    for u in [1,3]:
        for v in range(4):aut.append({g:mul(power((u,0),g[0]),power((v,1),g[1])) for g in G})
    def perm(co,p):
        out=[0]*8
        for g,c in zip(G,co):out[idx[p(g)]]=c
        return tuple(out)
    def trans(co,b,left=True):return perm(co,lambda g:mul(b,g) if left else mul(g,b))
    def normal(phi,a,co):
        out=[]
        for b in G:
            pp={g:conj(b,phi[g]) for g in G};aa=mul(mul(b,phi[b]),a);cc=trans(co,b)
            for psi in aut:
                ii={v:k for k,v in psi.items()}
                out.append((tuple(idx[psi[pp[ii[g]]]] for g in G),idx[psi[aa]],perm(cc,psi.__getitem__)))
        return min(out)
    coeffs=[]
    for inds in itertools.combinations_with_replacement(range(8),4):
        co=[0]*8
        for i in inds:co[i]+=1
        coeffs.append(tuple(co))
    discovered=set();raw=0
    for phi in aut:
        if not any(g[1]==1 and (phi[g][0]-g[0])%2 for g in G):continue
        for a in G:
            if phi[a]!=a or any(phi[phi[g]]!=conj(a,g) for g in G):continue
            for co in coeffs:
                if any(trans(co,g,False)!=trans(co,phi[g]) for g in G):continue
                if perm(co,phi.__getitem__)!=co or perm(co,inv)!=trans(co,inv(a)):continue
                raw+=1;discovered.add(normal(phi,a,co))
    phi={g:mul(power((3,0),g[0]),power((1,1),g[1])) for g in G}
    explicit=[]
    for a in [e,(2,0)]:
        explicit.extend([(a,tuple(int(g[1]==b) for g in G),('rotations' if b==0 else 'reflections')) for b in [0,1]])
    explicit.append((e,tuple(2*int(g in [(0,1),(1,1)]) for g in G),'exceptional'))
    need(raw==24 and len(discovered)==5,'complete enumeration count')
    need(discovered=={normal(phi,a,co) for a,co,label in explicit},'all five normalized representatives')
    z=s.Symbol('z');rows=[]
    # Rank-eight census identifiers use lexical tensor order within multiplicity.
    rank8=[]
    for line in gzip.open(args.repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'))
        if max(v for aa in N for b in aa for v in b)==1:rank8.append(N)
    rank8.sort();neutral_sources={i:rank8[i-1] for i in [12,15,18]}
    def isomap(T,N):
        A=[i for i in range(1,8) if sum(T[i][j][0] for j in range(8))==1 and any(T[i][j][0] and sum(T[i][j])==1 for j in range(8))]
        # Invertibles are detected from the full product with their dual.
        A=[i for i in range(1,8) if any(T[i][j]==[1]+[0]*7 for j in range(8))]
        B=[i for i in range(1,8) if any(N[i][j]==[1]+[0]*7 for j in range(8))]
        for ip in itertools.permutations(B):
            for np in itertools.permutations([i for i in range(1,8) if i not in B]):
                p=[0]*8
                for i,j in zip(A,ip):p[i]=j
                for i,j in zip([i for i in range(1,8) if i not in A],np):p[i]=j
                if all(T[i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)):return p
        raise RuntimeError('rank-eight tensor match')
    for a,co,label in explicit:
        N=[[[0]*16 for _ in range(16)] for _ in range(16)]
        for i,g in enumerate(G):
            for j,h in enumerate(G):
                N[i][j][idx[mul(g,h)]]=1;N[i][8+j][8+idx[mul(g,h)]]=1;N[8+i][j][8+idx[mul(g,phi[h])]]=1
                gh=mul(g,phi[h]);N[8+i][8+j][idx[mul(gh,a)]]=1
                for k,c in enumerate(co):N[8+i][8+j][8+idx[mul(gh,G[k])]]+=c
        dual,M=fusion_check(N,[1]*8+[t]*8);C=sum((M[i]*M[dual[i]] for i in range(16)),s.zeros(16));cp=s.factor(C.charpoly(z).as_expr())
        expected=(z-16)**4*(z*z-160*z+1280)**2*(z*z-96*z+768)**4 if label=='exceptional' else (z-16)**12*(z*z-160*z+1280)**2
        need(s.expand(cp-expected)==0,'Casimir polynomial')
        row={'a':a,'N_support':label,'N':co,'tensor_sha256':sha(N),'Casimir':str(cp),'excluded_by_codegree_field':label=='exceptional'}
        if label!='exceptional':
            base=0 if label=='rotations' else 1;sub=[idx[(i,0)] for i in range(4)]+[8+idx[(i,base)] for i in range(4)]
            need(all(N[i][j][k]==0 for i,j in itertools.product(sub,repeat=2) for k in set(range(16))-set(sub)),'neutral subring closed')
            T=[[[N[i][j][k] for k in sub] for j in sub] for i in sub];rid=18 if label=='reflections' else 15 if a==e else 12;target=neutral_sources[rid]
            p=isomap(T,target);row.update(neutral_id=f'R8_1_{rid}',neutral_tensor_sha256=sha(target),neutral_to_census=p)
        rows.append(row)
    result={'status':'PASS','scope':'general complex structural reduction only','classification_changes':0,'sources':source_rows,'raw_systems':raw,'normal_forms':rows,'remaining_extension_families':4,'optimizer_used':False}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','source_cases':4,'raw_systems':raw,'normal_forms':5,'remaining_extension_families':4}))

if __name__=='__main__':main()
